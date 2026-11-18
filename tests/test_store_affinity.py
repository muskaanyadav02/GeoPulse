import unittest
import pandas as pd

from scripts.store_affinity_analysis import calculate_store_affinity


class TestStoreAffinity(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "customer_id": ["C1", "C2", "C3", "C1", "C2", "C4"],
            "store_id": [
                "STORE_01", "STORE_01", "STORE_01",
                "STORE_02", "STORE_02", "STORE_02"
            ],
            "location_type": ["Store"] * 6
        })

    def test_shared_customers(self):
        _, overlap, _ = calculate_store_affinity(self.df)
        self.assertEqual(overlap.iloc[0]["shared_customers"], 2)

    def test_jaccard_similarity(self):
        _, overlap, _ = calculate_store_affinity(self.df)
        self.assertAlmostEqual(
            overlap.iloc[0]["jaccard_similarity"], 0.5
        )

    def test_similarity_matrix_symmetry(self):
        _, _, matrix = calculate_store_affinity(self.df)
        self.assertEqual(
            matrix.loc["STORE_01", "STORE_02"],
            matrix.loc["STORE_02", "STORE_01"]
        )

    def test_diagonal_values(self):
        _, _, matrix = calculate_store_affinity(self.df)
        for store in matrix.index:
            self.assertEqual(matrix.loc[store, store], 1.0)


if __name__ == "__main__":
    unittest.main()