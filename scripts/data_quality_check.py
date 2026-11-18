import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "processed" / "cleaned_gps_data.csv"

# Load data
df = pd.read_csv(DATA_FILE)

print("\n========== GEOPULSE DATA QUALITY REPORT ==========")

# 1. Total records
print("\n1. Total records:", len(df))

# 2. Required columns
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

print("\n2. Missing columns:", missing_columns)

if missing_columns:
    raise ValueError("Required columns are missing. Check the input CSV.")

# 3. Missing values
print("\n3. Missing values:")
print(df.isnull().sum())

# 4. Duplicate GPS records
duplicates = df.duplicated(
    subset=["customer_id", "timestamp", "latitude", "longitude"]
).sum()

print("\n4. Duplicate GPS records:", duplicates)

# 5. Invalid coordinates
invalid_coordinates = (
    ~df["latitude"].between(-90, 90)
    | ~df["longitude"].between(-180, 180)
).sum()

print("\n5. Invalid coordinates:", invalid_coordinates)

# 6. Invalid timestamps
timestamps = pd.to_datetime(df["timestamp"], errors="coerce")
invalid_timestamps = timestamps.isna().sum()

print("\n6. Invalid timestamps:", invalid_timestamps)

# 7. Invalid location types
valid_types = ["Store", "Movement"]

invalid_types = (~df["location_type"].isin(valid_types)).sum()

print("\n7. Invalid location types:", invalid_types)

# 8. Store ID business-rule validation
store_missing_id = (
    (df["location_type"] == "Store")
    & (df["store_id"].isna() | (df["store_id"].astype(str).str.strip() == ""))
).sum()

movement_with_store_id = (
    (df["location_type"] == "Movement")
    & df["store_id"].notna()
).sum()

print("\n8. Store records without store ID:", store_missing_id)
print("   Movement records with store ID:", movement_with_store_id)

# 9. Empty customer IDs
empty_customers = (
    df["customer_id"].isna()
    | (df["customer_id"].astype(str).str.strip() == "")
).sum()

print("\n9. Empty customer IDs:", empty_customers)

# 10. Final summary
issues = (
    len(missing_columns)
    + duplicates
    + invalid_coordinates
    + invalid_timestamps
    + invalid_types
    + store_missing_id
    + movement_with_store_id
    + empty_customers
)

print("\n========== FINAL SUMMARY ==========")
print("Total records:", len(df))
print("Total validation issues:", issues)

if issues == 0:
    print("Result: All validation checks passed!")
else:
    print("Result: Some validation issues were found.")

print("\nData quality validation completed!")