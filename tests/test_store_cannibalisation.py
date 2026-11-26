import pandas as pd
import pytest

from scripts.store_cannibalisation_analysis import analyze_cannibalisation


def sample_data():
    return pd.DataFrame({
        "customer_id": [
    "C1", "C2", "C3", "C4",
    "C1", "C2", "C5", "C6",
    None, None, None, None
],
"store_id": [
    "A", "A", "A", "A",
    "B", "B", "B", "B",
    None, None, None, None
],
"location_type": [
    "Store", "Store", "Store", "Store",
    "Store", "Store", "Store", "Store",
    "Movement", "Movement", "Movement", "Movement"
]
    })


def test_store_pairs_are_generated():
    result = analyze_cannibalisation(sample_data())

    assert len(result) == 1
    assert result.iloc[0]["store_a"] == "A"
    assert result.iloc[0]["store_b"] == "B"


def test_shared_customer_count():
    result = analyze_cannibalisation(sample_data())

    assert result.iloc[0]["shared_customers"] == 2


def test_overlap_percentage():
    result = analyze_cannibalisation(sample_data())

    assert result.iloc[0]["overlap_percentage"] == 50.0


def test_overlap_level():
    result = analyze_cannibalisation(sample_data())

    assert result.iloc[0]["overlap_level"] == "Moderate"


def test_missing_columns():
    df = pd.DataFrame({"customer_id": ["C1"]})

    with pytest.raises(ValueError, match="Missing required columns"):
        analyze_cannibalisation(df)


def test_no_valid_store_records():
    df = pd.DataFrame({
        "customer_id": ["C1"],
        "store_id": [None],
        "location_type": ["Movement"]
    })

    with pytest.raises(ValueError, match="No valid store visit records"):
        analyze_cannibalisation(df)