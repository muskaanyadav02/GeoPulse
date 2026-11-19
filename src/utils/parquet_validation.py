import pandas as pd
from pathlib import Path


def validate_parquet_data(csv_path, parquet_path):

    csv_file = Path(csv_path)
    parquet_file = Path(parquet_path)

    if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_file}")

    if not parquet_file.exists():
        raise FileNotFoundError(f"Parquet file not found: {parquet_file}")

    csv_df = pd.read_csv(csv_file)
    parquet_df = pd.read_parquet(parquet_file)

    # Essential columns that must not contain missing values
    required_columns = [
        "customer_id",
        "timestamp",
        "latitude",
        "longitude",
        "location_type",
        "distance_km",
        "speed_kmh"
    ]

    required_columns = [
        col for col in required_columns
        if col in parquet_df.columns
    ]

    missing_required = int(
        parquet_df[required_columns].isnull().sum().sum()
    )

    results = {
        "row_count_match": len(csv_df) == len(parquet_df),
        "column_match": list(csv_df.columns) == list(parquet_df.columns),
        "total_missing_values": int(
            parquet_df.isnull().sum().sum()
        ),
        "missing_required_values": missing_required,
        "duplicate_records": int(parquet_df.duplicated().sum())
    }

    results["validation_passed"] = (
        results["row_count_match"]
        and results["column_match"]
        and results["missing_required_values"] == 0
        and results["duplicate_records"] == 0
    )

    print("\nParquet Data Quality Report")
    print("---------------------------")

    for key, value in results.items():
        print(f"{key}: {value}")

    return results


if __name__ == "__main__":

    validate_parquet_data(
        "data/processed/cleaned_gps_data.csv",
        "data/processed/cleaned_gps_data.parquet"
    )

    validate_parquet_data(
        "data/processed/gps_movement_metrics.csv",
        "data/processed/gps_movement_metrics.parquet"
    )