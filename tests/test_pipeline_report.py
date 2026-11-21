
import json
import pandas as pd

from src.utils.pipeline_report import generate_pipeline_report


def sample_data():
    return pd.DataFrame({
        "customer_id": ["CUST_001", "CUST_001", "CUST_002"],
        "location_type": ["Store", "Movement", "Store"],
        "distance_km": [0.0, 2.5, 0.0],
        "speed_kmh": [0.0, 10.0, 0.0]
    })


def sample_validation():
    return [
        {
            "row_count_match": True,
            "column_match": True,
            "total_missing_values": 0,
            "missing_required_values": 0,
            "duplicate_records": 0,
            "validation_passed": True
        },
        {
            "row_count_match": True,
            "column_match": True,
            "total_missing_values": 0,
            "missing_required_values": 0,
            "duplicate_records": 0,
            "validation_passed": True
        }
    ]


def test_report_generates_successfully(tmp_path):
    output_path = tmp_path / "report.json"

    report = generate_pipeline_report(
        sample_data(),
        sample_validation(),
        output_path
    )

    assert output_path.exists()
    assert report["pipeline_status"] == "SUCCESS"


def test_report_contains_correct_data_summary(tmp_path):
    report = generate_pipeline_report(
        sample_data(),
        sample_validation(),
        tmp_path / "report.json"
    )

    summary = report["data_summary"]

    assert summary["total_records"] == 3
    assert summary["unique_customers"] == 2
    assert summary["store_visits"] == 2
    assert summary["movement_points"] == 1
    assert summary["total_distance_km"] == 2.5
    assert summary["average_speed_kmh"] == round(10 / 3, 3)


def test_report_contains_validation_status(tmp_path):
    report = generate_pipeline_report(
        sample_data(),
        sample_validation(),
        tmp_path / "report.json"
    )

    assert report["parquet_validation"]["overall_status"] == "PASSED"


def test_report_is_valid_json(tmp_path):
    output_path = tmp_path / "report.json"

    generate_pipeline_report(
        sample_data(),
        sample_validation(),
        output_path
    )

    with open(output_path, encoding="utf-8") as file:
        saved_report = json.load(file)

    assert saved_report["pipeline_status"] == "SUCCESS"
    assert saved_report["data_summary"]["total_records"] == 3
