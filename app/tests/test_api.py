import unittest

from app.api.main import parse_json_object


class ApiFallbackTests(unittest.TestCase):
    def test_parse_json_object_rejects_invalid_json(self):
        payload, error = parse_json_object(b"{not-json")
        self.assertEqual(payload, {})
        self.assertEqual(error, "invalid_json")

    def test_parse_json_object_rejects_non_object_json(self):
        payload, error = parse_json_object(b"[]")
        self.assertEqual(payload, {})
        self.assertEqual(error, "invalid_json_object")

    def test_parse_json_object_accepts_object(self):
        payload, error = parse_json_object(b'{"question":"hello"}')
        self.assertEqual(payload, {"question": "hello"})
        self.assertIsNone(error)


if __name__ == "__main__":
    unittest.main()
