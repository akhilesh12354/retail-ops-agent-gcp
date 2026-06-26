"""Agent tools wrapping deterministic retail operations services."""

from __future__ import annotations

from app.agent.citations import cite_capacity_row, cite_inventory_row
from app.services.anomaly_detection import detect_phantom_inventory
from app.services.inventory_repository import InventoryRepository
from app.services.routing_engine import route_order


class RetailOpsTools:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    def explain_phantom_inventory(self, store_id: str, sku: str) -> dict:
        row = self.repo.inventory_for(store_id, sku)
        recent_orders = self.repo.orders_for(store_id, sku)
        result = detect_phantom_inventory(row, recent_orders)
        sources = [cite_inventory_row(row)]
        return {
            "answer": result["explanation"],
            "decision": result["status"],
            "risk_score": result["risk_score"],
            "sources": sources,
        }

    def route_order(self, sku: str, quantity: int, destination_zip: str, channel: str, sla_hours: int) -> dict:
        result = route_order(
            inventory_rows=self.repo.inventory_by_sku(sku),
            capacity_rows=self.repo.capacity_rows(),
            sku=sku,
            quantity=quantity,
            destination_zip=destination_zip,
            channel=channel,
            sla_hours=sla_hours,
        )
        sources = []
        if result["inventory_row"] is not None:
            sources.append(cite_inventory_row(result["inventory_row"]))
        if result["capacity_row"] is not None:
            sources.append(cite_capacity_row(result["capacity_row"]))
        return {
            "answer": result["explanation"],
            "decision": result["decision"],
            "selected_store": result["store_id"],
            "score": result["fit_score"],
            "sources": sources,
        }

    def peak_season_recommendations(self) -> dict:
        overloaded = []
        for row in self.repo.capacity_rows():
            if not _is_valid_capacity_row(row):
                continue
            utilization = _capacity_utilization(row)
            if str(row["peak_season_mode"]).lower() == "true" and utilization >= 0.9:
                overloaded.append((row, utilization))

        if not overloaded:
            return {
                "answer": "No stores in the synthetic dataset need to stop ship-from-store intake.",
                "decision": "continue",
                "sources": [],
            }

        store_list = ", ".join(row["store_id"] for row, _ in overloaded)
        return {
            "answer": f"Stop or throttle ship-from-store intake for store(s) {store_list}; each is in peak-season mode above 90% fulfillment capacity.",
            "decision": "throttle_ship_from_store",
            "stores": [row["store_id"] for row, _ in overloaded],
            "sources": [cite_capacity_row(row) for row, _ in overloaded],
        }


def _is_valid_capacity_row(row: dict) -> bool:
    return row.get("store_id") and row.get("daily_capacity") is not None and row.get("open_orders") is not None


def _capacity_utilization(row: dict) -> float:
    daily_capacity = int(row["daily_capacity"])
    if daily_capacity <= 0:
        return 1.0
    return int(row["open_orders"]) / daily_capacity
