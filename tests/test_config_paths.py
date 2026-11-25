
from config.paths import (
    BASE_DIR,
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    LOGS_DIR,
    RAW_GPS_DATA,
    PIPELINE_REPORT,
    PIPELINE_LOG
)


def test_project_paths_are_absolute():
    assert BASE_DIR.is_absolute()
    assert DATA_DIR.is_absolute()


def test_data_directories():
    assert RAW_DATA_DIR == DATA_DIR / "raw"
    assert PROCESSED_DATA_DIR == DATA_DIR / "processed"
    assert LOGS_DIR == DATA_DIR / "logs"


def test_pipeline_file_paths():
    assert RAW_GPS_DATA == RAW_DATA_DIR / "gps_movement_data.csv"
    assert PIPELINE_REPORT == PROCESSED_DATA_DIR / "gps_pipeline_report.json"
    assert PIPELINE_LOG == LOGS_DIR / "gps_pipeline.log"
