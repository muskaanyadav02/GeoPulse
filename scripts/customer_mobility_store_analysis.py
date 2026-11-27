from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

MOVEMENT_FILE = BASE_DIR / "data/processed/customer_movement_summary.csv"
GPS_FILE = BASE_DIR / "data/processed/gps_movement_metrics.csv"
OUTPUT_FILE = BASE_DIR / "data/processed/customer_mobility_store_preferences.csv"


def analyze_customer_store_preferences(gps_df):
    required_columns = {"customer_id", "store_id", "location_type"}

    missing_columns = required_columns - set(gps_df.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    visits = gps_df[
        gps_df["location_type"].astype(str).str.strip().str.lower() == "store"
    ].copy()

    visits["customer_id"] = visits["customer_id"].astype("string").str.strip()
    visits["store_id"] = visits["store_id"].astype("string").str.strip()

    visits = visits.dropna(subset=["customer_id", "store_id"])
    visits = visits[
        (visits["customer_id"] != "") & (visits["store_id"] != "")
    ]

    results = []

    for customer_id, group in visits.groupby("customer_id"):
        store_counts = group["store_id"].value_counts()
        highest_count = store_counts.max()

        # Sort tied store IDs to make the result consistent.
        preferred_store = sorted(
            store_counts[store_counts == highest_count].index
        )[0]

        results.append({
            "customer_id": customer_id,
            "unique_stores_visited": store_counts.size,
            "most_visited_store": preferred_store,
            "most_visited_store_visits": int(highest_count),
            "total_store_visits": int(store_counts.sum()),
        })

    return pd.DataFrame(
        results,
        columns=[
            "customer_id",
            "unique_stores_visited",
            "most_visited_store",
            "most_visited_store_visits",
            "total_store_visits",
        ],
    )


def create_integrated_report():
    if not MOVEMENT_FILE.exists():
        raise FileNotFoundError(f"File not found: {MOVEMENT_FILE}")

    if not GPS_FILE.exists():
        raise FileNotFoundError(f"File not found: {GPS_FILE}")

    movement_df = pd.read_csv(MOVEMENT_FILE)
    gps_df = pd.read_csv(GPS_FILE)

    if "customer_id" not in movement_df.columns:
        raise ValueError("Movement summary must contain customer_id")

    if movement_df["customer_id"].duplicated().any():
        raise ValueError("Movement summary contains duplicate customer IDs")

    store_preferences = analyze_customer_store_preferences(gps_df)

    report = movement_df.merge(
        store_preferences,
        on="customer_id",
        how="left",
        validate="one_to_one",
    )

    report["unique_stores_visited"] = (
        report["unique_stores_visited"].fillna(0).astype(int)
    )
    report["most_visited_store_visits"] = (
        report["most_visited_store_visits"].fillna(0).astype(int)
    )
    report["total_store_visits"] = (
        report["total_store_visits"].fillna(0).astype(int)
    )
    report["most_visited_store"] = (
        report["most_visited_store"].fillna("No store visit")
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(OUTPUT_FILE, index=False)

    print("Integrated customer mobility report created successfully.")
    print(f"Customers analysed: {len(report)}")
    print(f"Output saved to: {OUTPUT_FILE}")
    print("\nReport preview:")
    print(report.head().to_string(index=False))


if __name__ == "__main__":
    create_integrated_report()