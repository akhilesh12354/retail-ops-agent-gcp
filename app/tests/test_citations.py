import unittest

from app.agent.citations import cite_capacity_row


class CitationTests(unittest.TestCase):
    def test_capacity_citation_accepts_native_boolean(self):
        citation = cite_capacity_row(
            {
                "store_id": "118",
                "daily_capacity": 140,
                "open_orders": 72,
                "peak_season_mode": True,
            }
        )
        self.assertIs(citation["peak_season_mode"], True)


if __name__ == "__main__":
    unittest.main()
