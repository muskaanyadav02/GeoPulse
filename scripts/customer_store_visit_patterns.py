from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "data/processed/cleaned_gps_data.csv"
OUTPUT_FILE = BASE_DIR / "data/processed/customer_store_visit_patterns.csv"

OUTPUT_COLUMNS = [
    "customer_id",
    "store_id",
    "visit_count",
    "total_customer_visits",
    "visit_percentage",
    "is_top_visited_store"
]


def analyze_visit_patterns(df):
    required_columns = ["customer_id", "store_id", "location_type"]

    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    stores = df[
        df["location_type"].astype(str).str.strip().str.lower() == "store"
    ].copy()

    stores = stores.dropna(subset=["customer_id", "store_id"])

    if stores.empty:
        raise ValueError("No valid store visit records found.")

    visits = (
        stores.groupby(["customer_id", "store_id"])
        .size()
        .reset_index(name="visit_count")
    )

    visits["total_customer_visits"] = (
        visits.groupby("customer_id")["visit_count"].transform("sum")
    )

    visits["visit_percentage"] = (
        visits["visit_count"] /
        visits["total_customer_visits"] * 100
    ).round(2)

    visits["is_top_visited_store"] = (
        visits["visit_count"]
        == visits.groupby("customer_id")["visit_count"].transform("max")
    )

    return visits[OUTPUT_COLUMNS]


def main():
    df = pd.read_csv(INPUT_FILE)
    result = analyze_visit_patterns(df)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False)

    print("CUSTOMER STORE VISIT PATTERNS")
    print("Customers:", result["customer_id"].nunique())
    print("Customer-store combinations:", len(result))
    print("Top-visited store records:", result["is_top_visited_store"].sum())
    print("\nSample:")
    print(result.head(10).to_string(index=False))
    print("\nSaved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()