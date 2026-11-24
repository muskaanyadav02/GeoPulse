
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Main data directories
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
LOGS_DIR = DATA_DIR / "logs"

# GPS datasets
RAW_GPS_DATA = RAW_DATA_DIR / "gps_movement_data.csv"

CLEANED_GPS_CSV = PROCESSED_DATA_DIR / "cleaned_gps_data.csv"
MOVEMENT_METRICS_CSV = PROCESSED_DATA_DIR / "gps_movement_metrics.csv"

# Parquet datasets
CLEANED_GPS_PARQUET = PROCESSED_DATA_DIR / "cleaned_gps_data.parquet"
MOVEMENT_METRICS_PARQUET = PROCESSED_DATA_DIR / "gps_movement_metrics.parquet"

# Pipeline outputs
PIPELINE_REPORT = PROCESSED_DATA_DIR / "gps_pipeline_report.json"
PIPELINE_LOG = LOGS_DIR / "gps_pipeline.log"
