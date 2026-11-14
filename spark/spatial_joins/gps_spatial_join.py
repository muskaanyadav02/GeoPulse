import os
import sys


os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
os.environ["HADOOP_HOME"] = "C:\\hadoop"



from sedona.spark import SedonaContext

config = (
    SedonaContext.builder()
    .appName("GeoPulse-Spatial-Join")
    .config(
        "spark.jars.packages",
        "org.apache.sedona:sedona-spark-3.5_2.12:1.6.1,"
        "org.datasyslab:geotools-wrapper:1.6.1-28.2",
    )
    .getOrCreate()
)

spark = SedonaContext.create(config)
# 2. Load GPS data and convert coordinates into map points
df_gps = spark.read.csv("data/raw/gps_movement_data.csv", header=True, inferSchema=True)
df_gps.createOrReplaceTempView("raw_gps")

df_gps_points = spark.sql("""
    SELECT 
        customer_id, 
        timestamp, 
        ST_Point(longitude, latitude) AS user_point 
    FROM raw_gps
""")
df_gps_points.createOrReplaceTempView("gps_points_table")

# 3. Define stores and create 500m catchment zones around them
stores_list = [
    ("STORE_01", "Hazratganj Store", 26.8467, 80.9462),
    ("STORE_02", "Gomti Nagar Hub", 26.8500, 80.9500),
    ("STORE_05", "Indira Nagar Plaza", 26.8350, 80.9550)
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
        g.customer_id, 
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
import shutil

output_path = "data/processed/matched_store_footfall.parquet"
if os.path.isdir(output_path):
  shutil.rmtree(output_path)

os.makedirs("data/processed", exist_ok=True)
df_matched.toPandas().to_parquet(output_path, index=False)
print("Output saved successfully!")
