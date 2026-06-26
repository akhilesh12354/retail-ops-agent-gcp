"""Vertex AI / Gemini adapter boundary with strict tool-call validation.

The local MVP uses deterministic planning so the project is runnable without cloud
credentials. This adapter defines the safe handoff point for Gemini tool calling:
the model may suggest a tool, but code validates the tool name and arguments before
execution.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, List, Callable


logger = logging.getLogger(__name__)


ALLOWED_TOOLS = {
    "explain_phantom_inventory": {"store_id": str, "sku": str},
    "route_order": {
        "sku": str,
        "quantity": int,
        "destination_zip": str,
        "channel": str,
        "sla_hours": int,
    },
    "peak_season_recommendations": {},
}


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]


class VertexAgentAdapter:
    def __init__(self, project_id: str, location: str, model: str):
        self.project_id = project_id
        self.location = location
        self.model = model

    def validate_tool_call(self, raw: dict[str, Any]) -> ToolCall:
        name = raw.get("name")
        arguments = raw.get("arguments", {})

        if name not in ALLOWED_TOOLS:
            raise ValueError(f"Unsupported tool call: {name}")
        if not isinstance(arguments, dict):
            raise ValueError("Tool arguments must be a dictionary")

        schema = ALLOWED_TOOLS[name]
        for key, expected_type in schema.items():
            if key not in arguments:
                raise ValueError(f"Missing required argument for {name}: {key}")
            if not isinstance(arguments[key], expected_type):
                raise TypeError(
                    f"Argument {key} for {name} must be {expected_type.__name__}, "
                    f"got {type(arguments[key]).__name__}"
                )

        extra_keys = set(arguments) - set(schema)
        if extra_keys:
            raise ValueError(f"Unexpected argument(s) for {name}: {sorted(extra_keys)}")

        return ToolCall(name=name, arguments=arguments)

    def plan_tool_call(self, question: str) -> ToolCall:
        """Return the intended tool call for a question.

        Calls Gemini via the Vertex AI SDK and passes the model-selected call
        through `validate_tool_call`.
        """
        try:
            from google import genai
            from google.genai import types
        except ImportError:
            raise ImportError(
                "GCP dependencies are required for live Vertex AI planning. "
                "Install them using: pip install '.[gcp]'"
            )
        client = genai.Client(vertexai=True, project=self.project_id, location=self.location)
        response = client.models.generate_content(
            model=self.model,
            contents=question,
            config=types.GenerateContentConfig(
                tools=self._get_tool_definitions(),
                system_instruction=(
                    "You are a retail operations assistant. Your job is to translate the user's "
                    "question into one of the allowed tool calls. Do not try to answer the question "
                    "directly; you must call one of the provided tools if the question is supported. "
                    "If the question cannot be answered by any tool, do not make any tool call."
                ),
                temperature=0.0,
            ),
        )

        if not response.function_calls:
            raise ValueError("Gemini did not plan any tool call for the question.")

        call = response.function_calls[0]
        arguments = dict(call.args) if call.args else {}

        # Handle type casting for arguments (e.g., float/str returned by Gemini to int)
        schema = ALLOWED_TOOLS.get(call.name, {})
        for key, expected_type in schema.items():
            if key in arguments:
                if expected_type is int and isinstance(arguments[key], (float, str)):
                    try:
                        arguments[key] = int(arguments[key])
                    except ValueError as e:
                        logger.warning("Failed to cast argument %s to int: %s", key, e)

        return self.validate_tool_call({
            "name": call.name,
            "arguments": arguments,
        })

    def _get_tool_definitions(self) -> List[Callable]:
        """Returns the list of dummy functions representing the tool schemas."""

        def explain_phantom_inventory(store_id: str, sku: str) -> None:
            """Explain if there is a phantom inventory issue for a store and SKU.

            Args:
                store_id: The ID of the store.
                sku: The SKU of the item.
            """
            pass

        def route_order(
            sku: str, quantity: int, destination_zip: str, channel: str, sla_hours: int
        ) -> None:
            """Route a BOPIS or ship-from-store order.

            Args:
                sku: The SKU of the item.
                quantity: The quantity to route.
                destination_zip: The target ZIP code.
                channel: The fulfillment channel (e.g. BOPIS, Ship-From-Store).
                sla_hours: The SLA window in hours.
            """
            pass

        def peak_season_recommendations() -> None:
            """Get recommendations for stores that should stop accepting ship-from-store orders during peak season."""
            pass

        return [explain_phantom_inventory, route_order, peak_season_recommendations]
