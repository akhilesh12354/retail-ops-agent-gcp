import unittest

from app.agent.vertex_adapter import VertexAgentAdapter


class VertexAdapterTests(unittest.TestCase):
    def setUp(self):
        self.adapter = VertexAgentAdapter("demo-project", "us-central1", "gemini-demo")

    def test_validates_allowed_tool_call(self):
        call = self.adapter.validate_tool_call(
            {
                "name": "route_order",
                "arguments": {
                    "sku": "SKU-1842",
                    "quantity": 1,
                    "destination_zip": "27701",
                    "channel": "BOPIS",
                    "sla_hours": 2,
                },
            }
        )
        self.assertEqual(call.name, "route_order")

    def test_rejects_unknown_tool(self):
        with self.assertRaises(ValueError):
            self.adapter.validate_tool_call({"name": "delete_inventory", "arguments": {}})

    def test_rejects_extra_argument(self):
        with self.assertRaises(ValueError):
            self.adapter.validate_tool_call(
                {
                    "name": "peak_season_recommendations",
                    "arguments": {"extra": "nope"},
                }
            )


if __name__ == "__main__":
    unittest.main()
