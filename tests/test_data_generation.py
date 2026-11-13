
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


def test_no_missing_required_values():
    df = load_data()

    required_columns = [
        "customer_id",
        "timestamp",
        "latitude",
        "longitude",
        "location_type"
    ]

    assert df[required_columns].isnull().sum().sum() == 0


def test_no_duplicate_records():
    df = load_data()
    assert df.duplicated().sum() == 0


def test_valid_coordinates():
    df = load_data()

    assert df["latitude"].between(-90, 90).all()
    assert df["longitude"].between(-180, 180).all()


def test_customer_record_count():
    df = load_data()

    # Each customer has 3 store visits and 6 movement points
    assert df.groupby("customer_id").size().eq(9).all()


def test_valid_location_types():
    df = load_data()

    valid_types = ["Store", "Movement"]

    assert df["location_type"].isin(valid_types).all()


def test_each_customer_visits_three_stores():
    df = load_data()

    store_visits = df[df["location_type"] == "Store"]

    assert store_visits.groupby("customer_id")["store_id"].nunique().eq(3).all()


def test_movement_points_have_no_store_id():
    df = load_data()

    movement = df[df["location_type"] == "Movement"]

    assert movement["store_id"].isnull().all()


def test_store_visits_have_store_id():
    df = load_data()

    visits = df[df["location_type"] == "Store"]

    assert visits["store_id"].notnull().all()


def test_timestamps_are_ordered():
    df = load_data()
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    for customer_id, group in df.groupby("customer_id"):
        assert group["timestamp"].is_monotonic_increasing
