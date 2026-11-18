import pandas as pd
from pathlib import Path


def export_csv_to_parquet(input_path, output_path):
    """
    Convert a CSV dataset into Parquet format.
    """

    input_file = Path(input_path)
    output_file = Path(output_path)

    if not input_file.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_file}"
        )

    # Load CSV data
    df = pd.read_csv(input_file)

    # Create output directory if needed
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Export to Parquet
    df.to_parquet(
        output_file,
        engine="pyarrow",
        index=False
    )

    print(f"Exported successfully: {output_file}")
    print("Records:", len(df))
    print("Columns:", len(df.columns))

    return output_file


if __name__ == "__main__":
    export_csv_to_parquet(
        "data/processed/cleaned_gps_data.csv",
        "data/processed/cleaned_gps_data.parquet"
    )

    export_csv_to_parquet(
        "data/processed/gps_movement_metrics.csv",
        "data/processed/gps_movement_metrics.parquet"
    )