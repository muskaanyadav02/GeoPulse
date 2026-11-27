
from inspect import signature

from config.paths import (
    BASE_DIR,
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    LOGS_DIR,
    RAW_GPS_DATA,
    CLEANED_GPS_CSV,
    MOVEMENT_METRICS_CSV,
    PIPELINE_REPORT,
    PIPELINE_LOG
)

from src.utils.preprocess_gps_data import preprocess_gps_data
from src.geospatial.movement_metrics import calculate_movement_metrics


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


def test_preprocessing_uses_centralized_paths():
    params = signature(preprocess_gps_data).parameters

    assert params["input_path"].default == RAW_GPS_DATA
    assert params["output_path"].default == CLEANED_GPS_CSV


def test_movement_metrics_uses_centralized_paths():
    params = signature(calculate_movement_metrics).parameters

    assert params["input_path"].default == CLEANED_GPS_CSV
    assert params["output_path"].default == MOVEMENT_METRICS_CSV
