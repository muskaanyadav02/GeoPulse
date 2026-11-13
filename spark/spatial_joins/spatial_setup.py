from sedona.spark import SedonaContext

def init_sedona():
    config = (
        SedonaContext.builder()
        .appName("GeoPulse-Spatial-Setup")
        .config(
            "spark.jars.packages",
            "org.apache.sedona:sedona-spark-3.5_2.12:1.6.1,"
            "org.datasyslab:geotools-wrapper:1.6.1-28.2",
        )
        .getOrCreate()
    )
    spark = SedonaContext.create(config)
    print("Sedona started successfully!")
    return spark

if __name__ == "__main__":
    init_sedona()
