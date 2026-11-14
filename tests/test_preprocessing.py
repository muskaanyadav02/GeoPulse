
import pandas as pd
import pytest
from pathlib import Path

from src.utils.preprocess_gps_data import preprocess_gps_data


def test_preprocessed_file_is_created(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    data = {
        "customer_id": ["CUST_001"],
        "timestamp": ["2026-11-01 09:00:00"],
        "latitude": [26.8467],
        "longitude": [80.9462],
        "store_id": ["STORE_01"],
        "location_type": ["Store"]
    }

    pd.DataFrame(data).to_csv(input_file, index=False)

    preprocess_gps_data(input_file, output_file)

    assert output_file.exists()


def test_invalid_coordinates_are_removed(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    data = {
        "customer_id": ["CUST_001", "CUST_002"],
        "timestamp": ["2026-11-01 09:00:00", "2026-11-01 09:15:00"],
        "latitude": [26.8467, 120],
        "longitude": [80.9462, 80.9500],
        "store_id": ["STORE_01", "STORE_02"],
        "location_type": ["Store", "Store"]
    }

    pd.DataFrame(data).to_csv(input_file, index=False)

    result = preprocess_gps_data(input_file, output_file)

    assert len(result) == 1
    assert result["customer_id"].iloc[0] == "CUST_001"


def test_duplicate_records_are_removed(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    data = {
        "customer_id": ["CUST_001", "CUST_001"],
        "timestamp": ["2026-11-01 09:00:00"] * 2,
        "latitude": [26.8467, 26.8467],
        "longitude": [80.9462, 80.9462],
        "store_id": ["STORE_01", "STORE_01"],
        "location_type": ["Store", "Store"]
    }

    pd.DataFrame(data).to_csv(input_file, index=False)

    result = preprocess_gps_data(input_file, output_file)

    assert len(result) == 1


def test_missing_required_columns_raise_error(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    data = {
        "customer_id": ["CUST_001"],
        "timestamp": ["2026-11-01 09:00:00"]
    }

    pd.DataFrame(data).to_csv(input_file, index=False)

    with pytest.raises(ValueError, match="Missing columns"):
        preprocess_gps_data(input_file, output_file)


def test_output_is_sorted_by_customer_and_timestamp(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    data = {
        "customer_id": ["CUST_001", "CUST_001"],
        "timestamp": ["2026-11-01 09:30:00", "2026-11-01 09:00:00"],
        "latitude": [26.8500, 26.8467],
        "longitude": [80.9500, 80.9462],
        "store_id": ["STORE_02", "STORE_01"],
        "location_type": ["Store", "Store"]
    }

    pd.DataFrame(data).to_csv(input_file, index=False)

    result = preprocess_gps_data(input_file, output_file)

    timestamps = result["timestamp"].tolist()

    assert timestamps == sorted(timestamps)
