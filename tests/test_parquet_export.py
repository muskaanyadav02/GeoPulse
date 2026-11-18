import pandas as pd

from src.utils.export_parquet import export_csv_to_parquet


def test_parquet_file_is_created(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.parquet"

    df = pd.DataFrame({
        "customer_id": ["CUST_001", "CUST_002"],
        "latitude": [26.84, 26.85],
        "longitude": [80.94, 80.95]
    })

    df.to_csv(input_file, index=False)

    export_csv_to_parquet(input_file, output_file)

    assert output_file.exists()


def test_parquet_preserves_records_and_columns(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.parquet"

    df = pd.DataFrame({
        "customer_id": ["CUST_001", "CUST_002"],
        "latitude": [26.84, 26.85],
        "longitude": [80.94, 80.95]
    })

    df.to_csv(input_file, index=False)

    export_csv_to_parquet(input_file, output_file)

    result = pd.read_parquet(output_file)

    assert len(result) == len(df)
    assert list(result.columns) == list(df.columns)


def test_missing_input_file_raises_error(tmp_path):
    input_file = tmp_path / "missing.csv"
    output_file = tmp_path / "output.parquet"

    try:
        export_csv_to_parquet(input_file, output_file)
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        assert True
        