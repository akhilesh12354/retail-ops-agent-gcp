"""Vertex AI / Gemini adapter boundary with strict tool-call validation.

The local MVP uses deterministic planning so the project is runnable without cloud
credentials. This adapter defines the safe handoff point for Gemini tool calling:
the model may suggest a tool, but code validates the tool name and arguments before
execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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

        Future implementation should call Gemini with the system prompt and bounded
        tool schema, then pass the model-selected call through `validate_tool_call`.
        """
        raise NotImplementedError(
            "Live Vertex AI / Gemini tool calling is intentionally not enabled in the local MVP."
        )
