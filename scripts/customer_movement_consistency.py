from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "data/processed/cleaned_gps_data.csv"
OUTPUT_FILE = BASE_DIR / "data/processed/customer_movement_consistency.csv"


def analyze_consistency(df):
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(["customer_id", "timestamp"])

    results = []

    for customer_id, group in df.groupby("customer_id"):
        group = group.sort_values("timestamp")
        timestamps = group["timestamp"]

        results.append({
            "customer_id": customer_id,
            "total_records": len(group),
            "movement_records": (group["location_type"] == "Movement").sum(),
            "store_records": (group["location_type"] == "Store").sum(),
            "duplicate_timestamps": int(timestamps.duplicated().sum()),
            "timestamp_order_valid": bool(timestamps.is_monotonic_increasing),
            "missing_coordinates": int(
                group[["latitude", "longitude"]].isna().any(axis=1).sum()
            ),
            "consistency_status": (
                "Consistent"
                if timestamps.is_monotonic_increasing
                and not timestamps.duplicated().any()
                and not group[["latitude", "longitude"]].isna().any().any()
                else "Needs review"
            )
        })

    return pd.DataFrame(results)


def main():
    df = pd.read_csv(INPUT_FILE)
    results = analyze_consistency(df)
    results.to_csv(OUTPUT_FILE, index=False)

    print("CUSTOMER MOVEMENT CONSISTENCY REPORT")
    print(results["consistency_status"].value_counts().to_string())
    print(f"\nOutput saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()