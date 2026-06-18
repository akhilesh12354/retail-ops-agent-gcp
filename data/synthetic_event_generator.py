"""Generate synthetic inventory update events for future Pub/Sub demos."""

from __future__ import annotations

import json
from random import randint


def generate_event(store_id: str = "117", sku: str = "SKU-1842") -> dict:
    return {
        "event_type": "inventory_adjustment",
        "store_id": store_id,
        "sku": sku,
        "delta": randint(-3, 5),
        "source_system": "synthetic_pos",
    }


if __name__ == "__main__":
    print(json.dumps(generate_event(), indent=2))

