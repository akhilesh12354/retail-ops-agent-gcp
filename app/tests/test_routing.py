import unittest

from app.agent.tools import RetailOpsTools
from app.services.inventory_repository import InventoryRepository


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


if __name__ == "__main__":
    unittest.main()
