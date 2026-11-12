from sedona.spark import SedonaContext

# 1. Start Spark and Apache Sedona
config = SedonaContext.builder().appName("GeoPulse-Spatial-Join").getOrCreate()
spark = SedonaContext.create(config)

# 2. Load GPS data and convert coordinates into map points
df_gps = spark.read.csv("data/raw/gps_movement_data.csv", header=True, inferSchema=True)
df_gps.createOrReplaceTempView("raw_gps")

df_gps_points = spark.sql("""
    SELECT 
        device_id, 
        timestamp, 
        ST_Point(longitude, latitude) AS user_point 
    FROM raw_gps
""")
df_gps_points.createOrReplaceTempView("gps_points_table")

# 3. Define stores and create 500m catchment zones around them
stores_list = [
    ("STORE_1", "Koramangala Coffee Shop", 12.9344, 77.6113),
    ("STORE_2", "Jayanagar Mall", 12.9069, 77.6013),
    ("STORE_3", "Electronic City Hub", 12.8452, 77.6602)
]
df_stores = spark.createDataFrame(stores_list, ["store_id", "store_name", "lat", "lon"])
df_stores.createOrReplaceTempView("stores_table")

df_catchment = spark.sql("""
    SELECT 
        store_id, 
        store_name, 
        ST_Buffer(ST_Point(lon, lat), 0.0045) AS catchment_zone 
    FROM stores_table
""")
df_catchment.createOrReplaceTempView("catchment_table")

# 4. Spatial Join: Find which users entered which store's 500m zone
df_matched = spark.sql("""
    SELECT 
        g.device_id, 
        g.timestamp, 
        s.store_id, 
        s.store_name
    FROM gps_points_table g
    JOIN catchment_table s
    ON ST_Contains(s.catchment_zone, g.user_point)
""")

print("Matched store visitors:")
df_matched.show(10)

# 5. Save the final output for Member 3 (Analytics)
df_matched.write.mode("overwrite").parquet("data/processed/matched_store_footfall.parquet")
print("Output saved successfully!")
