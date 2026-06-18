import unittest

from app.services.inventory_repository import InventoryRepository


class InventoryRepositoryTests(unittest.TestCase):
    def test_loads_default_csvs(self):
        repo = InventoryRepository.from_default_csvs()
        self.assertGreaterEqual(len(repo.inventory), 1)
        self.assertEqual(repo.inventory_for("117", "SKU-1842")["store_name"], "Durham South")


if __name__ == "__main__":
    unittest.main()

