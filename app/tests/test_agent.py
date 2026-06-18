import unittest

from app.agent.planner import RetailOpsAgent


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.agent = RetailOpsAgent.from_default_data()

    def test_phantom_inventory_question(self):
        response = self.agent.answer("Why is SKU-1842 showing available but failing pickup orders in Store 117?")
        self.assertEqual(response["decision"], "likely_phantom_inventory")
        self.assertGreater(response["risk_score"], 0.8)

    def test_bopis_question_routes_order(self):
        response = self.agent.answer("Route this BOPIS order for ZIP 27701 with SLA under 2 hours.")
        self.assertEqual(response["decision"], "route_selected")
        self.assertIn("selected_store", response)
        self.assertTrue(response["sources"])
        self.assertGreaterEqual(response["score"], 0)
        self.assertLessEqual(response["score"], 100)


if __name__ == "__main__":
    unittest.main()
