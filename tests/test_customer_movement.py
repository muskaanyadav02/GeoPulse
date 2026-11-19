import unittest
import pandas as pd

from scripts.customer_movement_analysis import analyze_customer_movement
from scripts.data_quality_check import validate_gps_data


class TestCustomerMovement(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "customer_id": ["C001", "C001", "C001"],
            "timestamp": [
                "2026-11-01 09:00:00",
                "2026-11-01 09:15:00",
                "2026-11-01 09:30:00"
            ],
            "latitude": [26.85, 26.84, 26.83],
            "longitude": [80.95, 80.96, 80.97],
            "store_id": ["STORE_01", None, "STORE_02"],
            "location_type": ["Store", "Movement", "Store"],
            "distance_km": [0, 1.5, 1.2],
            "speed_kmh": [0, 6.0, 4.8]
        })

    def test_customer_count(self):
        result = analyze_customer_movement(self.df)
        self.assertEqual(len(result), 1)

    def test_movement_and_store_records(self):
        result = analyze_customer_movement(self.df)
        self.assertEqual(result.iloc[0]["movement_records"], 1)
        self.assertEqual(result.iloc[0]["store_records"], 2)

    def test_total_movement_distance(self):
        result = analyze_customer_movement(self.df)
        self.assertEqual(result.iloc[0]["total_movement_distance_km"], 1.5)

    def test_average_speed(self):
        result = analyze_customer_movement(self.df)
        self.assertEqual(result.iloc[0]["average_speed_kmh"], 6.0)

    def test_data_quality_validation(self):
        result = validate_gps_data(self.df)
        self.assertEqual(result["total_records"], 3)
        self.assertEqual(result["duplicate_records"], 0)
        self.assertEqual(result["invalid_coordinates"], 0)


if __name__ == "__main__":
    unittest.main()