import unittest
from unittest.mock import MagicMock, patch
import os
import sys
from types import ModuleType, SimpleNamespace

from app.agent.vertex_adapter import VertexAgentAdapter
from app.agent.planner import RetailOpsAgent
from app.services.bigquery_inventory import BigQueryInventoryRepository


class LiveAdapterTests(unittest.TestCase):
    def setUp(self):
        self.env_patches = {}
        # Clear existing env vars to avoid pollution
        for var in [
            "USE_BIGQUERY",
            "USE_VERTEX_AI",
            "GOOGLE_CLOUD_PROJECT",
            "BIGQUERY_DATASET",
            "VERTEX_LOCATION",
            "VERTEX_MODEL",
        ]:
            if var in os.environ:
                self.env_patches[var] = os.environ[var]
                del os.environ[var]

    def tearDown(self):
        # Restore env vars
        for var, val in self.env_patches.items():
            os.environ[var] = val

    def test_config_initializes_csv_by_default(self):
        agent = RetailOpsAgent.from_default_data()
        self.assertNotIsInstance(agent.tools.repo, BigQueryInventoryRepository)
        self.assertIsNone(agent.adapter)

    def test_config_initializes_bigquery_when_enabled(self):
        os.environ["USE_BIGQUERY"] = "true"
        os.environ["GOOGLE_CLOUD_PROJECT"] = "test-project"
        os.environ["BIGQUERY_DATASET"] = "custom_dataset"

        agent = RetailOpsAgent.from_default_data()
        self.assertIsInstance(agent.tools.repo, BigQueryInventoryRepository)
        self.assertEqual(agent.tools.repo.project_id, "test-project")
        self.assertEqual(agent.tools.repo.dataset, "custom_dataset")

    def test_config_raises_error_if_use_bq_without_project(self):
        os.environ["USE_BIGQUERY"] = "true"
        with self.assertRaises(ValueError) as context:
            RetailOpsAgent.from_default_data()
        self.assertIn("GOOGLE_CLOUD_PROJECT must be set", str(context.exception))

    def test_config_initializes_vertex_when_enabled(self):
        os.environ["USE_VERTEX_AI"] = "true"
        os.environ["GOOGLE_CLOUD_PROJECT"] = "test-project"
        os.environ["VERTEX_LOCATION"] = "europe-west1"
        os.environ["VERTEX_MODEL"] = "gemini-test"

        agent = RetailOpsAgent.from_default_data()
        self.assertIsNotNone(agent.adapter)
        self.assertEqual(agent.adapter.project_id, "test-project")
        self.assertEqual(agent.adapter.location, "europe-west1")
        self.assertEqual(agent.adapter.model, "gemini-test")

    def test_config_raises_error_if_use_vertex_without_project(self):
        os.environ["USE_VERTEX_AI"] = "true"
        with self.assertRaises(ValueError) as context:
            RetailOpsAgent.from_default_data()
        self.assertIn("GOOGLE_CLOUD_PROJECT must be set", str(context.exception))

    def test_plan_tool_call_successful_routing(self):
        mock_client = MagicMock()
        mock_client_cls = MagicMock(return_value=mock_client)

        mock_response = MagicMock()
        mock_call = MagicMock()
        mock_call.name = "route_order"
        mock_call.args = {
            "sku": "SKU-1842",
            "quantity": 2.0,  # Test float-to-int conversion
            "destination_zip": "27701",
            "channel": "BOPIS",
            "sla_hours": "3",  # Test str-to-int conversion
        }
        mock_response.function_calls = [mock_call]
        mock_client.models.generate_content.return_value = mock_response

        with _fake_google_genai_modules(mock_client_cls):
            adapter = VertexAgentAdapter("test-project", "us-central1", "gemini-2.5-flash")
            tool_call = adapter.plan_tool_call("Route 2 of SKU-1842 to 27701 BOPIS in 3 hours")

        self.assertEqual(tool_call.name, "route_order")
        self.assertEqual(tool_call.arguments["sku"], "SKU-1842")
        self.assertEqual(tool_call.arguments["quantity"], 2)
        self.assertEqual(tool_call.arguments["destination_zip"], "27701")
        self.assertEqual(tool_call.arguments["channel"], "BOPIS")
        self.assertEqual(tool_call.arguments["sla_hours"], 3)

        # Assert correct Client initialization
        mock_client_cls.assert_called_once_with(
            vertexai=True, project="test-project", location="us-central1"
        )

    def test_plan_tool_call_raises_error_when_no_calls(self):
        mock_client = MagicMock()
        mock_client_cls = MagicMock(return_value=mock_client)

        mock_response = MagicMock()
        mock_response.function_calls = []
        mock_client.models.generate_content.return_value = mock_response

        with _fake_google_genai_modules(mock_client_cls):
            adapter = VertexAgentAdapter("test-project", "us-central1", "gemini-2.5-flash")
            with self.assertRaises(ValueError) as context:
                adapter.plan_tool_call("Hello, are you there?")
        self.assertIn("Gemini did not plan any tool call", str(context.exception))


def _fake_google_genai_modules(mock_client_cls):
    google_module = ModuleType("google")
    genai_module = ModuleType("google.genai")
    types_module = ModuleType("google.genai.types")
    types_module.GenerateContentConfig = lambda **kwargs: SimpleNamespace(**kwargs)
    genai_module.Client = mock_client_cls
    genai_module.types = types_module
    google_module.genai = genai_module
    return patch.dict(
        sys.modules,
        {
            "google": google_module,
            "google.genai": genai_module,
            "google.genai.types": types_module,
        },
    )


if __name__ == "__main__":
    unittest.main()
