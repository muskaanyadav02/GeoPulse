import unittest
import pandas as pd

from scripts.movement_speed_anomaly import analyze_speed_anomalies
from scripts.customer_movement_consistency import analyze_consistency


class TestMovementAnalysis(unittest.TestCase):

    def test_speed_anomaly_analysis_uses_movement_records(self):
        df = pd.DataFrame({
            "location_type": ["Movement", "Movement", "Store"],
            "speed_kmh": [1.0, 3.0, 100.0]
        })

        result, report = analyze_speed_anomalies(df)

        self.assertEqual(len(result), 2)
        self.assertEqual(report["movement_records"], 2)

    def test_anomaly_column_is_created(self):
        df = pd.DataFrame({
            "location_type": ["Movement"] * 5,
            "speed_kmh": [1.0, 1.1, 1.2, 1.3, 10.0]
        })

        result, _ = analyze_speed_anomalies(df)

        self.assertIn("speed_anomaly", result.columns)

    def test_consistent_customer(self):
        df = pd.DataFrame({
            "customer_id": ["C1", "C1"],
            "timestamp": ["2026-11-01 09:00", "2026-11-01 10:00"],
            "latitude": [15.0, 15.1],
            "longitude": [74.0, 74.1],
            "location_type": ["Store", "Movement"]
        })

        result = analyze_consistency(df)

        self.assertEqual(result.iloc[0]["consistency_status"], "Consistent")

    def test_duplicate_timestamp_needs_review(self):
        df = pd.DataFrame({
            "customer_id": ["C1", "C1"],
            "timestamp": ["2026-11-01 09:00", "2026-11-01 09:00"],
            "latitude": [15.0, 15.1],
            "longitude": [74.0, 74.1],
            "location_type": ["Store", "Movement"]
        })

        result = analyze_consistency(df)

        self.assertEqual(result.iloc[0]["consistency_status"], "Needs review")


if __name__ == "__main__":
    unittest.main()