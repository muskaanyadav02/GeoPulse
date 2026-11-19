import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "processed" / "cleaned_gps_data.csv"

REQUIRED_COLUMNS = [
    "customer_id",
    "timestamp",
    "latitude",
    "longitude",
    "store_id",
    "location_type",
]


def validate_gps_data(df):
    """Validate GPS records and return a summary of data-quality issues."""

    missing_columns = [
        col for col in REQUIRED_COLUMNS if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    invalid_coordinates = (
        ~df["latitude"].between(-90, 90)
        | ~df["longitude"].between(-180, 180)
    ).sum()

    invalid_timestamps = pd.to_datetime(
        df["timestamp"], errors="coerce"
    ).isna().sum()

    duplicates = df.duplicated(
        subset=["customer_id", "timestamp", "latitude", "longitude"]
    ).sum()

    invalid_types = (~df["location_type"].isin(["Store", "Movement"])).sum()

    store_missing_id = (
        (df["location_type"] == "Store")
        & (
            df["store_id"].isna()
            | (df["store_id"].astype(str).str.strip() == "")
        )
    ).sum()

    movement_with_store_id = (
        (df["location_type"] == "Movement")
        & df["store_id"].notna()
    ).sum()

    empty_customers = (
        df["customer_id"].isna()
        | (df["customer_id"].astype(str).str.strip() == "")
    ).sum()

    return {
        "total_records": len(df),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_records": int(duplicates),
        "invalid_coordinates": int(invalid_coordinates),
        "invalid_timestamps": int(invalid_timestamps),
        "invalid_location_types": int(invalid_types),
        "store_records_without_id": int(store_missing_id),
        "movement_records_with_store_id": int(movement_with_store_id),
        "empty_customer_ids": int(empty_customers),
    }


def print_report(results):
    """Display the data-quality validation report."""

    print("\n========== GEOPULSE DATA QUALITY REPORT ==========")

    for check, value in results.items():
        print(f"{check.replace('_', ' ').title()}: {value}")

    issue_keys = [
        "duplicate_records",
        "invalid_coordinates",
        "invalid_timestamps",
        "invalid_location_types",
        "store_records_without_id",
        "movement_records_with_store_id",
        "empty_customer_ids",
    ]

    total_issues = sum(results[key] for key in issue_keys)

    print("\nTotal validation issues:", total_issues)
    print("Result:", "PASSED" if total_issues == 0 else "FAILED")


def main():
    """Load the dataset and run validation."""

    df = pd.read_csv(DATA_FILE)
    results = validate_gps_data(df)
    print_report(results)


if __name__ == "__main__":
    main()