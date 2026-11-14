
import pandas as pd
from pathlib import Path


def preprocess_gps_data(
    input_path="data/raw/gps_movement_data.csv",
    output_path="data/processed/cleaned_gps_data.csv"
):
    # Load raw GPS data
    df = pd.read_csv(input_path)

    original_count = len(df)

    print("Starting GPS data preprocessing...")
    print("Original records:", original_count)

    # Check required columns
    required_columns = [
        "customer_id",
        "timestamp",
        "latitude",
        "longitude",
        "store_id",
        "location_type"
    ]

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    # Convert columns into correct data types
    df["timestamp"] = pd.to_datetime(
        df["timestamp"], errors="coerce"
    )

    df["latitude"] = pd.to_numeric(
        df["latitude"], errors="coerce"
    )

    df["longitude"] = pd.to_numeric(
        df["longitude"], errors="coerce"
    )

    # Remove rows with missing essential information
    df = df.dropna(
        subset=[
            "customer_id",
            "timestamp",
            "latitude",
            "longitude",
            "location_type"
        ]
    )

    # Keep only valid geographical coordinates
    df = df[
        df["latitude"].between(-90, 90)
        & df["longitude"].between(-180, 180)
    ]

    # Keep only valid location types
    valid_types = ["Store", "Movement"]
    df = df[df["location_type"].isin(valid_types)]

    # Remove duplicate records
    df = df.drop_duplicates()

    # Sort GPS records by customer and timestamp
    df = df.sort_values(
        by=["customer_id", "timestamp"]
    ).reset_index(drop=True)

    # Save cleaned dataset
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output, index=False)

    # Display preprocessing summary
    cleaned_count = len(df)
    removed_count = original_count - cleaned_count

    print("\nGPS preprocessing completed successfully!")
    print("------------------------------------------")
    print("Original records:", original_count)
    print("Cleaned records:", cleaned_count)
    print("Records removed:", removed_count)
    print("Unique customers:", df["customer_id"].nunique())
    print("Store visits:", (df["location_type"] == "Store").sum())
    print("Movement points:", (df["location_type"] == "Movement").sum())
    print("Output saved to:", output)

    return df


if __name__ == "__main__":
    preprocess_gps_data()
