from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "data/processed/cleaned_gps_data.csv"
OUTPUT_FILE = BASE_DIR / "data/processed/customer_store_visit_patterns.csv"


def analyze_visit_patterns(df):
    stores = df[df["location_type"] == "Store"].copy()

    if stores.empty:
        raise ValueError("No store visit records found.")

    visits = (
        stores.groupby(["customer_id", "store_id"])
        .size()
        .reset_index(name="visit_count")
    )

    visits["total_customer_visits"] = (
        visits.groupby("customer_id")["visit_count"].transform("sum")
    )

    visits["visit_percentage"] = (
        visits["visit_count"] / visits["total_customer_visits"] * 100
    ).round(2)

    visits["is_top_visited_store"] = (
    visits["visit_count"]
    == visits.groupby("customer_id")["visit_count"].transform("max")
)

    return visits


def main():
    df = pd.read_csv(INPUT_FILE)
    result = analyze_visit_patterns(df)
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