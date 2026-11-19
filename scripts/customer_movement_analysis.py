import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "gps_movement_metrics.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "customer_movement_summary.csv"


def analyze_customer_movement(df):
    """Generate movement and activity metrics for each customer."""

    required_columns = [
        "customer_id",
        "timestamp",
        "location_type",
        "distance_km",
        "speed_kmh",
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["distance_km"] = pd.to_numeric(df["distance_km"], errors="coerce")
    df["speed_kmh"] = pd.to_numeric(df["speed_kmh"], errors="coerce")

    results = []

    for customer_id, group in df.groupby("customer_id"):
        movement = group[group["location_type"] == "Movement"]
        store_records = group[group["location_type"] == "Store"]

        movement_speeds = movement["speed_kmh"].dropna()

        valid_times = group["timestamp"].dropna()

        duration_hours = (
            (valid_times.max() - valid_times.min()).total_seconds() / 3600
            if len(valid_times) > 1
            else 0
        )

        results.append({
            "customer_id": customer_id,
            "total_records": len(group),
            "movement_records": len(movement),
            "store_records": len(store_records),
            "total_movement_distance_km": round(
                movement["distance_km"].sum(), 3
            ),
            "average_speed_kmh": round(
                movement_speeds.mean(), 3
            ) if not movement_speeds.empty else 0,
            "maximum_speed_kmh": round(
                movement_speeds.max(), 3
            ) if not movement_speeds.empty else 0,
            "observation_duration_hours": round(duration_hours, 2),
        })

    return pd.DataFrame(results)


def main():
    df = pd.read_csv(INPUT_FILE)

    summary = analyze_customer_movement(df)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUTPUT_FILE, index=False)

    print("Customer movement analysis completed!")
    print("Customers analyzed:", len(summary))
    print("\nSample results:")
    print(summary.head().to_string(index=False))
    print("\nSaved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()