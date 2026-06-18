"""Small deterministic planner for retail operations questions."""

from __future__ import annotations

from app.agent.guardrails import refusal_for
from app.agent.tools import RetailOpsTools
from app.services.inventory_repository import InventoryRepository


class RetailOpsAgent:
    def __init__(self, tools: RetailOpsTools):
        self.tools = tools

    @classmethod
    def from_default_data(cls) -> "RetailOpsAgent":
        return cls(RetailOpsTools(InventoryRepository.from_default_csvs()))

    def answer(self, question: str) -> dict:
        refusal = refusal_for(question)
        if refusal:
            return {
                "answer": refusal,
                "decision": "refused",
                "sources": [],
            }

        q = question.lower()
        if "sku-1842" in q and ("store 117" in q or "117" in q):
            return self.tools.explain_phantom_inventory("117", "SKU-1842")
        if "bopis" in q or "pickup" in q:
            return self.tools.route_order(
                sku="SKU-1842",
                quantity=1,
                destination_zip="27701",
                channel="BOPIS",
                sla_hours=2,
            )
        if "black friday" in q or "peak" in q or "stop accepting ship-from-store" in q:
            return self.tools.peak_season_recommendations()
        if "evidence" in q:
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

