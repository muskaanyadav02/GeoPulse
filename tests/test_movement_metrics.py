
import pandas as pd
import pytest
from pathlib import Path

from src.geospatial.movement_metrics import (
    calculate_distance,
    calculate_movement_metrics
)


def create_sample_data(input_file):
    data = {
        "customer_id": ["CUST_001", "CUST_001"],
        "timestamp": [
            "2026-11-01 09:00:00",
            "2026-11-01 09:15:00"
        ],
        "latitude": [0.0, 0.0],
        "longitude": [0.0, 1.0],
        "store_id": ["STORE_01", None],
        "location_type": ["Store", "Movement"]
    }

    pd.DataFrame(data).to_csv(input_file, index=False)


def test_calculate_distance():
    distance = calculate_distance(0, 0, 0, 1)

    # One degree of longitude at the equator is approximately 111.2 km
    assert distance == pytest.approx(111.195, abs=0.1)


def test_movement_metrics_file_is_created(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    create_sample_data(input_file)

    calculate_movement_metrics(input_file, output_file)

    assert output_file.exists()


def test_first_point_has_zero_distance_and_speed(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    create_sample_data(input_file)

    result = calculate_movement_metrics(input_file, output_file)

    first_point = result.iloc[0]

    assert first_point["distance_km"] == 0
    assert first_point["speed_kmh"] == 0


def test_distance_and_speed_are_calculated(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    create_sample_data(input_file)

    result = calculate_movement_metrics(input_file, output_file)

    second_point = result.iloc[1]

    assert second_point["distance_km"] == pytest.approx(111.195, abs=0.1)
    assert second_point["speed_kmh"] == pytest.approx(444.78, abs=0.5)


def test_metrics_contain_no_infinite_values(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    create_sample_data(input_file)

    result = calculate_movement_metrics(input_file, output_file)

    assert result["distance_km"].map(
        lambda value: pd.notna(value) and value != float("inf")
    ).all()

    assert result["speed_kmh"].map(
        lambda value: pd.notna(value) and value != float("inf")
    ).all()
