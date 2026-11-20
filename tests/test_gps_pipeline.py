
import pandas as pd
import pytest

from src.utils import gps_pipeline


def test_pipeline_runs_all_steps(monkeypatch):
    execution_order = []

    def mock_preprocessing():
        execution_order.append("preprocessing")

    def mock_movement_metrics():
        execution_order.append("movement_metrics")
        return pd.DataFrame({
            "customer_id": ["CUST_001", "CUST_002"],
            "distance_km": [2.5, 3.5],
            "speed_kmh": [10.0, 15.0]
        })

    def mock_export(input_path, output_path):
        execution_order.append(f"export:{input_path}")

    def mock_validation(input_path, parquet_path):
        execution_order.append(f"validate:{input_path}")
        return {"validation_passed": True}

    monkeypatch.setattr(gps_pipeline, "preprocess_gps_data", mock_preprocessing)
    monkeypatch.setattr(gps_pipeline, "calculate_movement_metrics", mock_movement_metrics)
    monkeypatch.setattr(gps_pipeline, "export_csv_to_parquet", mock_export)
    monkeypatch.setattr(gps_pipeline, "validate_parquet_data", mock_validation)

    gps_pipeline.run_gps_pipeline()

    assert execution_order == [
        "preprocessing",
        "movement_metrics",
        "export:data/processed/cleaned_gps_data.csv",
        "export:data/processed/gps_movement_metrics.csv",
        "validate:data/processed/cleaned_gps_data.csv",
        "validate:data/processed/gps_movement_metrics.csv"
    ]


def test_pipeline_returns_processed_data(monkeypatch):
    expected_data = pd.DataFrame({
        "customer_id": ["CUST_001"],
        "distance_km": [2.5],
        "speed_kmh": [10.0]
    })

    monkeypatch.setattr(gps_pipeline, "preprocess_gps_data", lambda: None)
    monkeypatch.setattr(gps_pipeline, "calculate_movement_metrics", lambda: expected_data)
    monkeypatch.setattr(gps_pipeline, "export_csv_to_parquet", lambda *args: None)
    monkeypatch.setattr(
        gps_pipeline,
        "validate_parquet_data",
        lambda *args: {"validation_passed": True}
    )

    result = gps_pipeline.run_gps_pipeline()

    assert len(result) == 1
    assert result["customer_id"].iloc[0] == "CUST_001"


def test_pipeline_stops_when_validation_fails(monkeypatch):
    monkeypatch.setattr(gps_pipeline, "preprocess_gps_data", lambda: None)
    monkeypatch.setattr(
        gps_pipeline,
        "calculate_movement_metrics",
        lambda: pd.DataFrame({
            "customer_id": ["CUST_001"],
            "distance_km": [2.5],
            "speed_kmh": [10.0]
        })
    )
    monkeypatch.setattr(gps_pipeline, "export_csv_to_parquet", lambda *args: None)
    monkeypatch.setattr(
        gps_pipeline,
        "validate_parquet_data",
        lambda *args: {"validation_passed": False}
    )

    with pytest.raises(ValueError, match="GPS pipeline failed data quality validation"):
        gps_pipeline.run_gps_pipeline()
