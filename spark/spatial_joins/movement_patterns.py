from sedona.spark import SedonaContext
from pyspark.sql.functions import count, countDistinct, desc

# 1. Start Spark and Apache Sedona Session
config = (
    SedonaContext.builder()
    .appName("GeoPulse-Movement-Patterns")
    .config(
        "spark.jars.packages",
        "org.apache.sedona:sedona-spark-3.5_2.12:1.6.1,"
        "org.datasyslab:geotools-wrapper:1.6.1-28.2",
    )
    .getOrCreate()
)
spark = SedonaContext.create(config)

# 2. Load raw GPS dataset and extract the hour of each visit
df_gps = spark.read.csv("GeoPulse/data/raw/gps_movement_data.csv", header=True, inferSchema=True)
df_gps.createOrReplaceTempView("raw_gps")

df_gps_hourly = spark.sql("""
    SELECT 
        customer_id,
        timestamp,
        HOUR(timestamp) AS visit_hour,
        ST_Point(longitude, latitude) AS user_point
    FROM raw_gps
""")
df_gps_hourly.createOrReplaceTempView("gps_hourly_table")

# 3. Create 500m Store Catchment Areas
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

# 4. Match visitors and find Peak Customer Movement Hours
df_matched = spark.sql("""
    SELECT 
        g.customer_id,
        g.visit_hour,
        s.store_id,
        s.store_name
    FROM gps_hourly_table g
    JOIN catchment_table s
    ON ST_Contains(s.catchment_zone, g.user_point)
""")

df_peak_hours = df_matched.groupBy("store_id", "store_name", "visit_hour") \
    .agg(
        count("customer_id").alias("total_pings"),
        countDistinct("customer_id").alias("unique_visitors")
    ) \
    .orderBy("store_id", desc("unique_visitors"))

print("Peak Customer Movement Hours per Store:")
df_peak_hours.show(15)

# 5. Save hourly movement patterns for Member 3 (Analytics) & Member 4 (Dashboard)
df_peak_hours.write.mode("overwrite").parquet("GeoPulse/data/processed/hourly_movement_patterns.parquet")
print("Movement patterns saved successfully!")
