"""Small deterministic planner for retail operations questions."""

from __future__ import annotations

from app.agent.guardrails import refusal_for
from app.agent.tools import RetailOpsTools
from app.agent.vertex_adapter import VertexAgentAdapter
from app.services.inventory_repository import InventoryRepository


class RetailOpsAgent:
    def __init__(self, tools: RetailOpsTools, adapter: VertexAgentAdapter | None = None):
        self.tools = tools
        self.adapter = adapter

    @classmethod
    def from_default_data(cls) -> "RetailOpsAgent":
        import os

        use_bq = os.environ.get("USE_BIGQUERY", "").lower() == "true"
        if use_bq:
            project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
            if not project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT must be set when USE_BIGQUERY=true")
            dataset = os.environ.get("BIGQUERY_DATASET", "retail_ops_demo")
            from app.services.bigquery_inventory import BigQueryInventoryRepository

            repo = BigQueryInventoryRepository(project_id, dataset)
        else:
            repo = InventoryRepository.from_default_csvs()

        tools = RetailOpsTools(repo)

        use_vertex = os.environ.get("USE_VERTEX_AI", "").lower() == "true"
        adapter = None
        if use_vertex:
            project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
            if not project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT must be set when USE_VERTEX_AI=true")
            location = os.environ.get("VERTEX_LOCATION", "us-central1")
            model = os.environ.get("VERTEX_MODEL", "gemini-2.5-flash")
            from app.agent.vertex_adapter import VertexAgentAdapter
            adapter = VertexAgentAdapter(project_id, location, model)

        return cls(tools, adapter)

    def answer(self, question: str) -> dict:
        refusal = refusal_for(question)
        if refusal:
            return {
                "answer": refusal,
                "decision": "refused",
                "sources": [],
            }

        if self.adapter is not None:
            try:
                tool_call = self.adapter.plan_tool_call(question)
                if tool_call.name == "explain_phantom_inventory":
                    return self.tools.explain_phantom_inventory(
                        store_id=tool_call.arguments["store_id"],
                        sku=tool_call.arguments["sku"],
                    )
                if tool_call.name == "route_order":
                    return self.tools.route_order(
                        sku=tool_call.arguments["sku"],
                        quantity=tool_call.arguments["quantity"],
                        destination_zip=tool_call.arguments["destination_zip"],
                        channel=tool_call.arguments["channel"],
                        sla_hours=tool_call.arguments["sla_hours"],
                    )
                if tool_call.name == "peak_season_recommendations":
                    return self.tools.peak_season_recommendations()
            except Exception:
                # Keep the portfolio demo runnable when optional live cloud planning is unavailable.
                pass

        q = question.lower()
        if _is_phantom_inventory_question(q):
            return self.tools.explain_phantom_inventory("117", "SKU-1842")
        if _is_peak_season_question(q):
            return self.tools.peak_season_recommendations()
        if _is_ship_from_store_question(q):
            return self.tools.route_order(
                sku="SKU-1842",
                quantity=1,
                destination_zip="27701",
                channel="SHIP_FROM_STORE",
                sla_hours=24,
            )
        if _is_bopis_question(q) or _is_evidence_question(q):
            return self.tools.route_order(
                sku="SKU-1842",
                quantity=1,
                destination_zip="27701",
                channel="BOPIS",
                sla_hours=2,
            )

        return {
            "answer": "I can answer inventory accuracy, BOPIS routing, ship-from-store routing, and peak-season capacity questions for the synthetic demo dataset.",
            "decision": "unsupported_question",
            "sources": [],
        }


def _is_phantom_inventory_question(q: str) -> bool:
    return (
        ("sku-1842" in q and ("store 117" in q or "117" in q))
        or "phantom inventory" in q
        or "failing pickup" in q
        or "inventory mismatch" in q
        or "stockout risk" in q
    )


def _is_bopis_question(q: str) -> bool:
    return any(term in q for term in ("bopis", "pickup", "buy online pick up", "curbside"))


def _is_ship_from_store_question(q: str) -> bool:
    return any(
        term in q
        for term in (
            "ship-from-store",
            "ship from store",
            "ship-to-home",
            "parcel route",
            "direct ship",
        )
    )


def _is_peak_season_question(q: str) -> bool:
    return any(
        term in q
        for term in (
            "black friday",
            "peak",
            "holiday surge",
            "stop accepting ship-from-store",
            "throttle",
            "capacity control",
        )
    )


def _is_evidence_question(q: str) -> bool:
    return any(
        term in q
        for term in (
            "evidence",
            "sources",
            "cite",
            "grounded",
            "why did you choose",
            "audit trail",
            "fulfillment decision",
        )
    )
