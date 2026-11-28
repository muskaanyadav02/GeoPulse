import unittest
import pandas as pd

from scripts.customer_store_visit_patterns import analyze_visit_patterns
from scripts.store_transition_analysis import analyze_store_transitions


class TestStorePatterns(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "customer_id": ["C1", "C1", "C1", "C2", "C2", "C2"],
            "timestamp": [
                "2026-11-01 09:00",
                "2026-11-01 10:00",
                "2026-11-01 11:00",
                "2026-11-01 09:00",
                "2026-11-01 10:00",
                "2026-11-01 11:00"
            ],
            "store_id": ["S1", "S2", "S1", "S2", "S3", "S1"],
            "location_type": ["Store"] * 6
        })

    def test_empty_transitions(self):
        df = pd.DataFrame({
            "customer_id": ["C1"],
            "timestamp": ["2026-11-01 09:00"],
            "store_id": ["S1"],
            "location_type": ["Store"]
        })

        result = analyze_store_transitions(df)

        self.assertTrue(result.empty)
        self.assertEqual(
            list(result.columns),
            [
                "from_store",
                "to_store",
                "transition_count",
                "unique_customers",
                "average_time_between_visits_hours",
                "transition_percentage"
            ]
        )

    def test_visit_pattern_counts(self):
        result = analyze_visit_patterns(self.df)
        self.assertEqual(len(result), 5)

    def test_visit_percentages(self):
        result = analyze_visit_patterns(self.df)
        customer = result[result["customer_id"] == "C1"]
        self.assertAlmostEqual(customer["visit_percentage"].sum(), 100)

    def test_top_visited_store(self):
        result = analyze_visit_patterns(self.df)
        customer = result[result["customer_id"] == "C1"]
        top = customer[customer["is_top_visited_store"]]
        self.assertEqual(top.iloc[0]["store_id"], "S1")

    def test_transition_count(self):
        result = analyze_store_transitions(self.df)
        self.assertEqual(result["transition_count"].sum(), 4)

    def test_transition_percentages(self):
        result = analyze_store_transitions(self.df)
        totals = result.groupby("from_store")["transition_percentage"].sum()
        for percentage in totals:
            self.assertAlmostEqual(percentage, 100)


if __name__ == "__main__":
    unittest.main()