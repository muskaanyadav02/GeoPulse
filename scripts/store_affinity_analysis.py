import pandas as pd
from pathlib import Path
from itertools import combinations


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "processed" / "cleaned_gps_data.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

STORE_COUNT_COLUMNS = ["store_id", "unique_customers"]

OVERLAP_COLUMNS = [
    "store_a",
    "store_b",
    "shared_customers",
    "jaccard_similarity"
]


def calculate_store_affinity(df):
    required_columns = ["customer_id", "store_id", "location_type"]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    store_data = df.copy()

    store_data["location_type"] = (
        store_data["location_type"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    store_data = store_data[
        store_data["location_type"] == "store"
    ].copy()

    store_data["customer_id"] = (
        store_data["customer_id"].astype("string").str.strip()
    )

    store_data["store_id"] = (
        store_data["store_id"].astype("string").str.strip()
    )

    store_data = store_data.dropna(
        subset=["customer_id", "store_id"]
    )

    store_data = store_data[
        (store_data["customer_id"] != "")
        & (store_data["store_id"] != "")
    ]

    if store_data.empty:
        raise ValueError("No valid store visit records found.")

    customer_sets = {
        store: set(group["customer_id"])
        for store, group in store_data.groupby("store_id")
    }

    stores = sorted(customer_sets.keys())

    store_counts = pd.DataFrame([
        {
            "store_id": store,
            "unique_customers": len(customer_sets[store])
        }
        for store in stores
    ], columns=STORE_COUNT_COLUMNS)

    overlap_rows = []

    for store_a, store_b in combinations(stores, 2):
        customers_a = customer_sets[store_a]
        customers_b = customer_sets[store_b]

        common = customers_a & customers_b
        union = customers_a | customers_b

        similarity = len(common) / len(union) if union else 0

        overlap_rows.append({
            "store_a": store_a,
            "store_b": store_b,
            "shared_customers": len(common),
            "jaccard_similarity": round(similarity, 4)
        })

    overlap_df = pd.DataFrame(
        overlap_rows,
        columns=OVERLAP_COLUMNS
    )

    matrix = pd.DataFrame(
        0.0,
        index=stores,
        columns=stores
    )

    for store in stores:
        matrix.loc[store, store] = 1.0

    for row in overlap_rows:
        matrix.loc[row["store_a"], row["store_b"]] = (
            row["jaccard_similarity"]
        )
        matrix.loc[row["store_b"], row["store_a"]] = (
            row["jaccard_similarity"]
        )

    return store_counts, overlap_df, matrix


def main():
    df = pd.read_csv(DATA_FILE)

    store_counts, overlap, matrix = calculate_store_affinity(df)

    print("\n===== GEOPULSE CUSTOMER-STORE AFFINITY =====")

    print("\n1. STORE CUSTOMER COUNTS")
    print(store_counts.to_string(index=False))

    print("\n2. SHARED CUSTOMERS AND SIMILARITY")
    print(overlap.to_string(index=False))

    print("\n3. STORE SIMILARITY MATRIX")
    print(matrix.round(2).to_string())

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    store_counts.to_csv(
        OUTPUT_DIR / "store_affinity_counts.csv",
        index=False
    )

    overlap.to_csv(
        OUTPUT_DIR / "store_customer_overlap.csv",
        index=False
    )

    matrix.to_csv(
        OUTPUT_DIR / "store_similarity_matrix.csv"
    )

    print("\nAffinity reports generated successfully!")


if __name__ == "__main__":
    main()