"""BOPIS and ship-from-store routing decisions."""

from __future__ import annotations


def route_order(
    inventory_rows: list[dict],
    capacity_rows: list[dict],
    sku: str,
    quantity: int,
    destination_zip: str,
    channel: str,
    sla_hours: int,
) -> dict:
    capacity_by_store = {row["store_id"]: row for row in capacity_rows}
    candidates = []

    for row in inventory_rows:
        capacity = capacity_by_store[row["store_id"]]
        available = int(row["on_hand"]) - int(row["reserved"]) - int(row["safety_stock"])
        utilization = int(capacity["open_orders"]) / int(capacity["daily_capacity"])
        distance = int(row["distance_to_zip_27701_miles"]) if destination_zip == "27701" else int(row["default_distance_miles"])

        if available < quantity:
            continue
        if channel.upper() == "BOPIS" and distance > 25:
            continue
        if sla_hours <= 2 and utilization >= 0.95:
            continue

        score = round((available * 2.0) - (distance * 0.35) - (utilization * 20.0), 2)
        if capacity["peak_season_mode"].lower() == "true" and channel.upper() == "SHIP_FROM_STORE":
            score -= 8
        candidates.append((score, row, capacity, available, utilization, distance))

    if not candidates:
        return {
            "decision": "no_safe_route",
            "store_id": None,
            "score": 0,
            "inventory_row": inventory_rows[0],
            "capacity_row": capacity_rows[0],
            "explanation": f"No safe route found for {sku}; inventory, distance, or capacity constraints blocked fulfillment.",
        }

    score, row, capacity, available, utilization, distance = sorted(candidates, reverse=True, key=lambda item: item[0])[0]
    fit_score = _fit_score(available=available, utilization=utilization, distance=distance, channel=channel)
    return {
        "decision": "route_selected",
        "store_id": row["store_id"],
        "score": score,
        "fit_score": fit_score,
        "inventory_row": row,
        "capacity_row": capacity,
        "explanation": (
            f"Route {channel.upper()} order for {sku} to Store {row['store_id']}. "
            f"It has {available} sellable units, is {distance} miles from ZIP {destination_zip}, "
            f"is at {utilization:.0%} fulfillment utilization, and has a {fit_score}/100 route fit score."
        ),
    }


def _fit_score(available: int, utilization: float, distance: int, channel: str) -> int:
    stock_score = min(45, available * 4)
    capacity_score = max(0, round((1 - utilization) * 35))
    distance_score = max(0, 20 - round(distance / 2))
    if channel.upper() == "SHIP_FROM_STORE":
        distance_score = max(0, 20 - round(distance / 10))
    return max(0, min(100, stock_score + capacity_score + distance_score))
