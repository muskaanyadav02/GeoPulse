
import pandas as pd
from pathlib import Path

# Load generated GPS dataset
DATA_PATH = Path("data/raw/gps_movement_data.csv")


def load_data():
    return pd.read_csv(DATA_PATH)


def test_dataset_exists():
    assert DATA_PATH.exists()


def test_dataset_not_empty():
    df = load_data()
    assert len(df) > 0


def test_no_missing_values():
    df = load_data()
    assert df.isnull().sum().sum() == 0


def test_no_duplicate_records():
    df = load_data()
    assert df.duplicated().sum() == 0


def test_valid_coordinates():
    df = load_data()

    assert df["latitude"].between(-90, 90).all()
    assert df["longitude"].between(-180, 180).all()


def test_customer_record_count():
    df = load_data()

    assert df.groupby("customer_id").size().eq(10).all()


def test_valid_location_types():
    df = load_data()

    valid_types = ["Store", "Movement"]

    assert df["location_type"].isin(valid_types).all()
