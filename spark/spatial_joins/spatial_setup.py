import os
import sys
from sedona.spark import SedonaContext


os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


os.environ["HADOOP_HOME"] = "C:\\hadoop"
os.environ["PATH"] += os.pathsep + "C:\\hadoop\\bin"


def init_sedona():
  config = (
      SedonaContext.builder()
      .appName("GeoPulse-Spatial-Setup")
      .master("local[*]")
      .config(
          "spark.jars.packages",
          "org.apache.sedona:sedona-spark-3.5_2.12:1.6.1,"
          "org.datasyslab:geotools-wrapper:1.6.1-28.2",
      )
      .config(
          "spark.driver.extraJavaOptions",
          "-Djava.security.manager=allow "
          "--add-opens=java.base/java.lang=ALL-UNNAMED "
          "--add-opens=java.base/java.lang.invoke=ALL-UNNAMED "
          "--add-opens=java.base/java.lang.reflect=ALL-UNNAMED "
          "--add-opens=java.base/java.io=ALL-UNNAMED "
          "--add-opens=java.base/java.net=ALL-UNNAMED "
          "--add-opens=java.base/java.nio=ALL-UNNAMED "
          "--add-opens=java.base/java.util=ALL-UNNAMED "
          "--add-opens=java.base/java.util.concurrent=ALL-UNNAMED "
          "--add-opens=java.base/sun.nio.ch=ALL-UNNAMED",
      )
      .getOrCreate()
  )
  spark = SedonaContext.create(config)
  print("Sedona started successfully!")
  return spark


if __name__ == "__main__":
  init_sedona()
