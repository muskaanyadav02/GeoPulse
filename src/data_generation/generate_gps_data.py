
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

NUM_CUSTOMERS = 100
STORES_PER_CUSTOMER = 3
MOVEMENT_POINTS = 3

# Generate GPS journeys for 100 customers
for customer_num in range(1, NUM_CUSTOMERS + 1):

    customer_id = f"CUST_{customer_num:03d}"

    # Select 3 different stores for each customer
    selected_stores = np.random.choice(
        list(stores.keys()),
        size=STORES_PER_CUSTOMER,
        replace=False
    )

    timestamp = datetime(2026, 11, 1, 9, 0, 0)

    # Visit each selected store
    for i, store_id in enumerate(selected_stores):

        store_lat, store_lon = stores[store_id]

        # Record store visit
        records.append({
            "customer_id": customer_id,
            "timestamp": timestamp,
            "latitude": store_lat,
            "longitude": store_lon,
            "store_id": store_id,
            "location_type": "Store"
        })

        timestamp += timedelta(minutes=15)

        # Generate movement points towards the next store
        if i < STORES_PER_CUSTOMER - 1:

            next_store_id = selected_stores[i + 1]
            next_lat, next_lon = stores[next_store_id]

            for point in range(1, MOVEMENT_POINTS + 1):

                fraction = point / (MOVEMENT_POINTS + 1)

                latitude = (
                    store_lat +
                    fraction * (next_lat - store_lat) +
                    np.random.normal(0, 0.0002)
                )

                longitude = (
                    store_lon +
                    fraction * (next_lon - store_lon) +
                    np.random.normal(0, 0.0002)
                )

                records.append({
                    "customer_id": customer_id,
                    "timestamp": timestamp,
                    "latitude": latitude,
                    "longitude": longitude,
                    "store_id": None,
                    "location_type": "Movement"
                })

                timestamp += timedelta(minutes=15)

# Convert records into a DataFrame
df = pd.DataFrame(records)

# Save dataset
output_path = "data/raw/gps_movement_data.csv"

os.makedirs(os.path.dirname(output_path), exist_ok=True)

df.to_csv(output_path, index=False)

print("GPS journey dataset generated successfully!")
print("Total records:", len(df))
print("Unique customers:", df["customer_id"].nunique())
print("Store visits:", (df["location_type"] == "Store").sum())
print("Movement points:", (df["location_type"] == "Movement").sum())
print(df.head(10))
