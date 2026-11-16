import pandas as pd

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

    monkeypatch.setattr(
        gps_pipeline,
        "preprocess_gps_data",
        mock_preprocessing
    )

    monkeypatch.setattr(
        gps_pipeline,
        "calculate_movement_metrics",
        mock_movement_metrics
    )

    gps_pipeline.run_gps_pipeline()

    assert execution_order == [
        "preprocessing",
        "movement_metrics"
    ]


def test_pipeline_returns_processed_data(monkeypatch):
    expected_data = pd.DataFrame({
        "customer_id": ["CUST_001"],
        "distance_km": [2.5],
        "speed_kmh": [10.0]
    })

    monkeypatch.setattr(
        gps_pipeline,
        "preprocess_gps_data",
        lambda: None
    )

    monkeypatch.setattr(
        gps_pipeline,
        "calculate_movement_metrics",
        lambda: expected_data
    )

    result = gps_pipeline.run_gps_pipeline()

    assert len(result) == 1
    assert result["customer_id"].iloc[0] == "CUST_001"