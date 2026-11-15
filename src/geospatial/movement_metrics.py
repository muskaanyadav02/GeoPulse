
import pandas as pd
import numpy as np
from pathlib import Path


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two GPS coordinates
    using the Haversine formula.
    Returns distance in kilometers.
    """

    earth_radius = 6371  # Earth's radius in kilometers

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        np.sin(delta_lat / 2) ** 2
        + np.cos(lat1) * np.cos(lat2)
        * np.sin(delta_lon / 2) ** 2
    )

    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return earth_radius * c


def calculate_movement_metrics(
    input_path="data/processed/cleaned_gps_data.csv",
    output_path="data/processed/gps_movement_metrics.csv"
):
    # Load cleaned GPS data
    df = pd.read_csv(input_path)

    print("Calculating customer movement metrics...")

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Sort records customer-wise and time-wise
    df = df.sort_values(
        ["customer_id", "timestamp"]
    ).reset_index(drop=True)

    # Get previous GPS coordinates for each customer
    df["previous_latitude"] = (
        df.groupby("customer_id")["latitude"].shift(1)
    )

    df["previous_longitude"] = (
        df.groupby("customer_id")["longitude"].shift(1)
    )

    # Get previous timestamp
    df["previous_timestamp"] = (
        df.groupby("customer_id")["timestamp"].shift(1)
    )

    # Calculate distance from previous GPS point
    df["distance_km"] = calculate_distance(
        df["previous_latitude"],
        df["previous_longitude"],
        df["latitude"],
        df["longitude"]
    )

    # First point of each customer has no previous point
    df["distance_km"] = df["distance_km"].fillna(0)

    # Calculate time difference in hours
    df["time_difference_hours"] = (
        df["timestamp"] - df["previous_timestamp"]
    ).dt.total_seconds() / 3600

    # Calculate movement speed in km/h
    df["speed_kmh"] = (
        df["distance_km"] / df["time_difference_hours"]
    ).replace([np.inf, -np.inf], np.nan).fillna(0)

    # Save enriched GPS dataset
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output, index=False)

    # Display summary
    print("\nMovement metrics calculated successfully!")
    print("------------------------------------------")
    print("Total GPS records:", len(df))
    print("Unique customers:", df["customer_id"].nunique())
    print("Total distance (km):", round(df["distance_km"].sum(), 3))
    print("Average movement speed (km/h):", round(df["speed_kmh"].mean(), 3))
    print("Output saved to:", output)

    return df


if __name__ == "__main__":
    calculate_movement_metrics()
