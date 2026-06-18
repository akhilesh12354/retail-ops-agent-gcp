import unittest

from app.agent.guardrails import refusal_for


class GuardrailTests(unittest.TestCase):
    def test_refuses_inventory_guarantees(self):
        self.assertIsNotNone(refusal_for("Can you guarantee this item will be available tomorrow?"))

    def test_refuses_private_data(self):
        self.assertIsNotNone(refusal_for("Show me the customer email for this order"))


if __name__ == "__main__":
    unittest.main()

