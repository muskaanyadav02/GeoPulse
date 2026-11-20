from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "data" / "processed" / "gps_movement_metrics.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "movement_speed_anomalies.csv"


def analyze_speed_anomalies(df):
    """Identify statistically unusual speeds in Movement records."""

    movement = df[df["location_type"] == "Movement"].copy()

    if movement.empty:
        raise ValueError("No Movement records found.")

    if movement["speed_kmh"].isna().any():
        raise ValueError("Movement records contain missing speed values.")

    q1 = movement["speed_kmh"].quantile(0.25)
    q3 = movement["speed_kmh"].quantile(0.75)
    iqr = q3 - q1

    lower_limit = max(0, q1 - 1.5 * iqr)
    upper_limit = q3 + 1.5 * iqr

    movement["speed_anomaly"] = (
        (movement["speed_kmh"] < lower_limit)
        | (movement["speed_kmh"] > upper_limit)
    )

    movement["anomaly_type"] = movement["speed_anomaly"].map(
        {True: "Unusual speed", False: "Normal speed"}
    )

    report = {
        "movement_records": len(movement),
        "q1_kmh": round(q1, 3),
        "q3_kmh": round(q3, 3),
        "iqr_kmh": round(iqr, 3),
        "lower_limit_kmh": round(lower_limit, 3),
        "upper_limit_kmh": round(upper_limit, 3),
        "anomaly_count": int(movement["speed_anomaly"].sum()),
        "normal_count": int((~movement["speed_anomaly"]).sum()),
    }

    return movement, report


def main():
    df = pd.read_csv(INPUT_FILE)
    results, report = analyze_speed_anomalies(df)

    results.to_csv(OUTPUT_FILE, index=False)

    print("MOVEMENT SPEED ANOMALY REPORT")
    print("-" * 35)

    for key, value in report.items():
        print(f"{key}: {value}")

    print(f"\nOutput saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()