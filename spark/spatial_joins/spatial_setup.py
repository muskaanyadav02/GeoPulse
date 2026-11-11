from sedona.spark import SedonaContext

# 1. Initialize PySpark and Apache Sedona Context
config = SedonaContext.builder() \
    .appName("GeoPulse-Geospatial-Setup") \
    .getOrCreate()

spark = SedonaContext.create(config)
print("1. Spark and Sedona Context initialized successfully!")

# 2. Load the raw synthetic GPS movement dataset
df_gps = spark.read.csv("data/raw/gps_movement_data.csv", header=True, inferSchema=True)

print("2. GPS dataset loaded! Showing top 5 rows:")
df_gps.show(5)

# 3. Define sample retail store locations (Store ID, Name, Latitude, Longitude)
stores_list = [
    ("STORE_1", "Koramangala Coffee Shop", 12.9344, 77.6113),
    ("STORE_2", "Jayanagar Mall", 12.9069, 77.6013),
    ("STORE_3", "Electronic City Hub", 12.8452, 77.6602)
]
df_stores = spark.createDataFrame(stores_list, ["store_id", "store_name", "lat", "lon"])
df_stores.createOrReplaceTempView("stores_table")

# 4. Create a 500-meter catchment area (buffer zone) around each store
# Note: 0.0045 degrees is approximately equal to 500 meters
df_catchment = spark.sql("""
    SELECT 
        store_id, 
        store_name,
        ST_Buffer(ST_Point(lon, lat), 0.0045) AS catchment_zone
    FROM stores_table
""")

print("3. 500m Store Catchment Polygons generated:")
df_catchment.show()
