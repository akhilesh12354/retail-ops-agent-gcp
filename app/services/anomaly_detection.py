"""Inventory anomaly detection."""

from __future__ import annotations


def detect_phantom_inventory(inventory_row: dict, recent_orders: list[dict]) -> dict:
    available = int(inventory_row["on_hand"]) - int(inventory_row["reserved"]) - int(inventory_row["safety_stock"])
    failures = sum(1 for order in recent_orders if order["status"] == "PICKUP_FAILED")
    attempts = max(1, len(recent_orders))
    failure_rate = failures / attempts

    risk_score = round(min(1.0, (0.55 if available > 0 else 0.2) + failure_rate * 0.55), 2)
    status = "likely_phantom_inventory" if available > 0 and failures >= 2 else "inventory_signal_normal"

    if status == "likely_phantom_inventory":
        explanation = (
            f"{inventory_row['sku']} at Store {inventory_row['store_id']} shows {available} sellable units, "
            f"but {failures}/{attempts} recent pickup orders failed. Treat it as likely phantom inventory "
            "until a cycle count or store confirmation refreshes the inventory truth layer."
        )
    else:
        explanation = (
            f"{inventory_row['sku']} at Store {inventory_row['store_id']} does not show enough failed "
            "fulfillment signals to classify as phantom inventory."
        )

    return {
        "status": status,
        "risk_score": risk_score,
        "available": available,
        "failure_rate": failure_rate,
        "explanation": explanation,
    }

