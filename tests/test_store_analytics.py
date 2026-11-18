import unittest
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"


class TestStoreAnalytics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.store_data = pd.read_csv(
            DATA_DIR / "store_summary.csv"
        )

        cls.hourly_data = pd.read_csv(
            DATA_DIR / "hourly_store_activity.csv"
        )

    def test_total_store_records(self):
        total = self.store_data["total_records"].sum()
        self.assertEqual(total, 300)

    def test_number_of_stores(self):
        self.assertEqual(len(self.store_data), 5)

    def test_unique_customers(self):
        total = self.store_data["unique_customers"].sum()
        self.assertEqual(total, 300)

    def test_hourly_record_count(self):
        total = self.hourly_data["total_records"].sum()
        self.assertEqual(total, 300)

    def test_hourly_distribution(self):
        expected = [100, 100, 100]
        actual = self.hourly_data["total_records"].tolist()
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()