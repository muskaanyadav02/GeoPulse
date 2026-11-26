from pathlib import Path
from itertools import combinations

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "cleaned_gps_data.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "store_cannibalisation_risk.csv"

OUTPUT_COLUMNS = [
    "store_a",
    "store_b",
    "shared_customers",
    "smaller_store_customers",
    "overlap_percentage",
    "jaccard_similarity",
    "overlap_level"
]

HIGH_OVERLAP_THRESHOLD = 60
MODERATE_OVERLAP_THRESHOLD = 30


def analyze_cannibalisation(df):
    required_columns = ["customer_id", "store_id", "location_type"]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    stores_df = df.copy()

    stores_df["location_type"] = (
        stores_df["location_type"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    stores_df = stores_df[
        stores_df["location_type"] == "store"
    ].copy()

    stores_df["customer_id"] = (
        stores_df["customer_id"].astype("string").str.strip()
    )

    stores_df["store_id"] = (
        stores_df["store_id"].astype("string").str.strip()
    )

    stores_df = stores_df.dropna(
        subset=["customer_id", "store_id"]
    )

    stores_df = stores_df[
        (stores_df["customer_id"] != "")
        & (stores_df["store_id"] != "")
    ]

    stores_df = stores_df.drop_duplicates(
        subset=["customer_id", "store_id"]
    )

    if stores_df.empty:
        raise ValueError("No valid store visit records found.")

    customer_sets = {
        store_id: set(group["customer_id"])
        for store_id, group in stores_df.groupby("store_id")
    }

    results = []

    for store_a, store_b in combinations(sorted(customer_sets), 2):
        customers_a = customer_sets[store_a]
        customers_b = customer_sets[store_b]

        shared = customers_a & customers_b
        union = customers_a | customers_b

        smaller_store_customers = min(
            len(customers_a),
            len(customers_b)
        )

        overlap_percentage = (
            len(shared) / smaller_store_customers * 100
            if smaller_store_customers else 0
        )

        jaccard_similarity = (
            len(shared) / len(union)
            if union else 0
        )

        if overlap_percentage >= HIGH_OVERLAP_THRESHOLD:
            overlap_level = "High"
        elif overlap_percentage >= MODERATE_OVERLAP_THRESHOLD:
            overlap_level = "Moderate"
        else:
            overlap_level = "Low"

        results.append({
            "store_a": store_a,
            "store_b": store_b,
            "shared_customers": len(shared),
            "smaller_store_customers": smaller_store_customers,
            "overlap_percentage": round(overlap_percentage, 2),
            "jaccard_similarity": round(jaccard_similarity, 4),
            "overlap_level": overlap_level
        })

    return pd.DataFrame(results, columns=OUTPUT_COLUMNS)


def main():
    df = pd.read_csv(INPUT_FILE)

    result = analyze_cannibalisation(df)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False)

    print("\n===== GEOPULSE STORE CANNIBALISATION ANALYSIS =====")

    print("\nStore pairs analysed:", len(result))

    if not result.empty:
        print("\nOverlap analysis:")
        print(result.to_string(index=False))

        print("\nOverlap level summary:")
        print(result["overlap_level"].value_counts().to_string())

    print("\nReport saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()