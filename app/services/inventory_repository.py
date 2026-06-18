"""CSV-backed inventory repository with a BigQuery-shaped interface."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"


class InventoryRepository:
    def __init__(self, inventory: list[dict], orders: list[dict], capacity: list[dict]):
        self.inventory = inventory
        self.orders = orders
        self.capacity = capacity

    @classmethod
    def from_default_csvs(cls) -> "InventoryRepository":
        return cls(
            inventory=_read_csv(DATA_DIR / "sample_inventory.csv"),
            orders=_read_csv(DATA_DIR / "sample_orders.csv"),
            capacity=_read_csv(DATA_DIR / "sample_store_capacity.csv"),
        )

    def inventory_for(self, store_id: str, sku: str) -> dict:
        for row in self.inventory:
            if row["store_id"] == store_id and row["sku"] == sku:
                return row
        raise KeyError(f"No inventory for store={store_id} sku={sku}")

    def inventory_by_sku(self, sku: str) -> list[dict]:
        return [row for row in self.inventory if row["sku"] == sku]

    def orders_for(self, store_id: str, sku: str) -> list[dict]:
        return [row for row in self.orders if row["store_id"] == store_id and row["sku"] == sku]

    def capacity_rows(self) -> list[dict]:
        return list(self.capacity)


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

