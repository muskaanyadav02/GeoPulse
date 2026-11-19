import pandas as pd
import pytest

from src.utils.parquet_validation import validate_parquet_data


def create_test_files(tmp_path, data):
    csv_file = tmp_path / "input.csv"
    parquet_file = tmp_path / "input.parquet"

    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    df.to_parquet(parquet_file, index=False)

    return csv_file, parquet_file


def test_valid_parquet_data_passes(tmp_path):
    csv_file, parquet_file = create_test_files(
        tmp_path,
        {
            "customer_id": ["C1", "C2"],
            "latitude": [26.84, 26.85],
            "longitude": [80.94, 80.95],
            "timestamp": ["2026-11-19", "2026-11-19"],
            "location_type": ["Store", "Movement"]
        }
    )

    result = validate_parquet_data(csv_file, parquet_file)

    assert result["validation_passed"] is True


def test_optional_missing_values_are_allowed(tmp_path):
    csv_file, parquet_file = create_test_files(
        tmp_path,
        {
            "customer_id": ["C1", "C2"],
            "latitude": [26.84, 26.85],
            "longitude": [80.94, 80.95],
            "timestamp": ["2026-11-19", "2026-11-19"],
            "location_type": ["Store", "Movement"],
            "store_id": ["STORE_01", None]
        }
    )

    result = validate_parquet_data(csv_file, parquet_file)

    assert result["total_missing_values"] == 1
    assert result["missing_required_values"] == 0
    assert result["validation_passed"] is True


def test_missing_required_values_fail(tmp_path):
    csv_file, parquet_file = create_test_files(
        tmp_path,
        {
            "customer_id": ["C1", None],
            "latitude": [26.84, 26.85],
            "longitude": [80.94, 80.95],
            "timestamp": ["2026-11-19", "2026-11-19"],
            "location_type": ["Store", "Movement"]
        }
    )

    result = validate_parquet_data(csv_file, parquet_file)

    assert result["missing_required_values"] == 1
    assert result["validation_passed"] is False


def test_duplicate_records_fail(tmp_path):
    csv_file, parquet_file = create_test_files(
        tmp_path,
        {
            "customer_id": ["C1", "C1"],
            "latitude": [26.84, 26.84],
            "longitude": [80.94, 80.94],
            "timestamp": ["2026-11-19", "2026-11-19"],
            "location_type": ["Store", "Store"]
        }
    )

    result = validate_parquet_data(csv_file, parquet_file)

    assert result["duplicate_records"] == 1
    assert result["validation_passed"] is False