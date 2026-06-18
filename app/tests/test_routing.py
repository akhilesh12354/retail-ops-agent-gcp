import unittest

from app.agent.tools import RetailOpsTools
from app.services.inventory_repository import InventoryRepository
from app.services.routing_engine import route_order


class RoutingTests(unittest.TestCase):
    def test_routes_bopis_to_viable_store(self):
        tools = RetailOpsTools(InventoryRepository.from_default_csvs())
        response = tools.route_order("SKU-1842", 1, "27701", "BOPIS", 2)
        self.assertEqual(response["decision"], "route_selected")
        self.assertEqual(response["selected_store"], "118")
        self.assertGreaterEqual(response["score"], 0)
        self.assertLessEqual(response["score"], 100)

    def test_peak_season_throttles_overloaded_stores(self):
        tools = RetailOpsTools(InventoryRepository.from_default_csvs())
        response = tools.peak_season_recommendations()
        self.assertEqual(response["decision"], "throttle_ship_from_store")
        self.assertIn("117", response["stores"])

    def test_unknown_sku_returns_no_safe_route_without_crashing(self):
        tools = RetailOpsTools(InventoryRepository.from_default_csvs())
        response = tools.route_order("SKU-DOES-NOT-EXIST", 1, "27701", "BOPIS", 2)
        self.assertEqual(response["decision"], "no_safe_route")
        self.assertIsNone(response["selected_store"])
        self.assertEqual(response["score"], 0)
        self.assertEqual(response["sources"], [])

    def test_bigquery_boolean_capacity_does_not_crash(self):
        response = route_order(
            inventory_rows=[
                {
                    "store_id": "118",
                    "sku": "SKU-1842",
                    "on_hand": 15,
                    "reserved": 3,
                    "safety_stock": 3,
                    "distance_to_zip_27701_miles": 23,
                    "default_distance_miles": 18,
                }
            ],
            capacity_rows=[
                {
                    "store_id": "118",
                    "daily_capacity": 140,
                    "open_orders": 72,
                    "peak_season_mode": True,
                }
            ],
            sku="SKU-1842",
            quantity=1,
            destination_zip="27701",
            channel="SHIP_FROM_STORE",
            sla_hours=24,
        )
        self.assertEqual(response["decision"], "route_selected")

    def test_zero_capacity_is_treated_as_fully_utilized(self):
        response = route_order(
            inventory_rows=[
                {
                    "store_id": "999",
                    "sku": "SKU-1842",
                    "on_hand": 15,
                    "reserved": 0,
                    "safety_stock": 1,
                    "distance_to_zip_27701_miles": 4,
                    "default_distance_miles": 4,
                }
            ],
            capacity_rows=[
                {
                    "store_id": "999",
                    "daily_capacity": 0,
                    "open_orders": 0,
                    "peak_season_mode": "true",
                }
            ],
            sku="SKU-1842",
            quantity=1,
            destination_zip="27701",
            channel="BOPIS",
            sla_hours=2,
        )
        self.assertEqual(response["decision"], "no_safe_route")


if __name__ == "__main__":
    unittest.main()
