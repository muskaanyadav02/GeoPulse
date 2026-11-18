import pandas as pd
from pathlib import Path

# Load project data
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "processed" / "cleaned_gps_data.csv"

df = pd.read_csv(DATA_FILE)

print("GEOPULSE DATA QUALITY REPORT")
print("-" * 40)

# 1. Total records
print("Total records:", len(df))

# 2. Missing values
print("\nMissing values:")
print(df.isnull().sum())

# 3. Duplicate GPS records
duplicates = df.duplicated(
    subset=["customer_id", "timestamp", "latitude", "longitude"]
).sum()
print("\nDuplicate records:", duplicates)

# 4. Location type distribution
print("\nLocation type distribution:")
print(df["location_type"].value_counts())

# 5. Invalid coordinates
invalid_coordinates = (
    (df["latitude"] < -90) |
    (df["latitude"] > 90) |
    (df["longitude"] < -180) |
    (df["longitude"] > 180)
).sum()

print("\nInvalid coordinates:", invalid_coordinates)

# 6. Invalid timestamps
invalid_timestamps = pd.to_datetime(
    df["timestamp"], errors="coerce"
).isna().sum()

print("Invalid timestamps:", invalid_timestamps)

print("\nData quality check completed!")