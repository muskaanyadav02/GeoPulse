import pandas as pd
from pathlib import Path

# Load GPS data
file_path = Path("data/processed/cleaned_gps_data.csv")
df = pd.read_csv(file_path)

# Convert timestamp into datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Select only GPS records labelled as Store
store_data = df[df["location_type"] == "Store"].copy()

# 1. Store-wise GPS record count
store_summary = (
    store_data.groupby("store_id")
    .agg(
        total_records=("customer_id", "count"),
        unique_customers=("customer_id", "nunique")
    )
    .reset_index()
)

# 2. Hourly store activity
store_data["hour"] = store_data["timestamp"].dt.hour

hourly_summary = (
    store_data.groupby("hour")
    .size()
    .reset_index(name="total_records")
)

# Display results
print("\n===== GEOPULSE STORE ANALYTICS =====")

print("\n1. STORE-WISE SUMMARY")
print(store_summary.to_string(index=False))

print("\n2. HOURLY STORE ACTIVITY")
print(hourly_summary.to_string(index=False))

# Save reports
Path("data/processed").mkdir(parents=True, exist_ok=True)

store_summary.to_csv(
    "data/processed/store_summary.csv", index=False
)

hourly_summary.to_csv(
    "data/processed/hourly_store_activity.csv", index=False
)

print("\nAnalytics reports saved successfully!")