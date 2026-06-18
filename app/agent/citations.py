"""Citation helpers for grounded retail operations responses."""

from __future__ import annotations


def cite_inventory_row(row: dict) -> dict:
    return {
        "type": "inventory_row",
        "store_id": row["store_id"],
        "sku": row["sku"],
        "on_hand": int(row["on_hand"]),
        "reserved": int(row["reserved"]),
        "safety_stock": int(row["safety_stock"]),
        "source": "data/sample_inventory.csv",
    }


def cite_capacity_row(row: dict) -> dict:
    return {
        "type": "store_capacity_row",
        "store_id": row["store_id"],
        "daily_capacity": int(row["daily_capacity"]),
        "open_orders": int(row["open_orders"]),
        "peak_season_mode": row["peak_season_mode"].lower() == "true",
        "source": "data/sample_store_capacity.csv",
    }

