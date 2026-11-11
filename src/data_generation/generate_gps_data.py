
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Reproducible random data
np.random.seed(42)

# Generate fictional stores around Lucknow
stores = {
    "STORE_01": (26.8467, 80.9462),
    "STORE_02": (26.8500, 80.9500),
    "STORE_03": (26.8400, 80.9400),
    "STORE_04": (26.8550, 80.9350),
    "STORE_05": (26.8350, 80.9550)
}

records = []

# Generate GPS movement for 100 customers
for customer_num in range(1, 101):

    customer_id = f"CUST_{customer_num:03d}"

    # Each customer visits a randomly selected store
    store_id = np.random.choice(list(stores.keys()))
    store_lat, store_lon = stores[store_id]

    start_time = datetime(2026, 11, 1, 9, 0, 0)

    # Generate 10 GPS observations per customer
    for point in range(10):

        latitude = store_lat + np.random.normal(0, 0.003)
        longitude = store_lon + np.random.normal(0, 0.003)

        timestamp = start_time + timedelta(
            minutes=point * 15
        )

        records.append({
            "customer_id": customer_id,
            "timestamp": timestamp,
            "latitude": latitude,
            "longitude": longitude,
            "store_id": store_id,
            "location_type": "Store" if point == 0 else "Movement"
        })

# Convert records into a DataFrame
df = pd.DataFrame(records)

# Save dataset
output_path = "data/raw/gps_movement_data.csv"

os.makedirs(os.path.dirname(output_path), exist_ok=True)

df.to_csv(output_path, index=False)

print("GPS dataset generated successfully!")
print("Total records:", len(df))
print(df.head())
