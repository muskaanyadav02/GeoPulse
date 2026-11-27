import pandas as pd
import pytest

from scripts.customer_mobility_store_analysis import (
    analyze_customer_store_preferences,
)


def test_customer_store_preferences():
    df = pd.DataFrame({
        "customer_id": ["C1", "C1", "C1", "C2"],
        "store_id": ["S1", "S1", "S2", "S3"],
        "location_type": ["Store", "Store", "Store", "Store"],
    })

    result = analyze_customer_store_preferences(df)

    c1 = result[result["customer_id"] == "C1"].iloc[0]

    assert c1["unique_stores_visited"] == 2
    assert c1["most_visited_store"] == "S1"
    assert c1["most_visited_store_visits"] == 2
    assert c1["total_store_visits"] == 3


def test_tied_store_visits_are_deterministic():
    df = pd.DataFrame({
        "customer_id": ["C1", "C1"],
        "store_id": ["S2", "S1"],
        "location_type": ["Store", "Store"],
    })

    result = analyze_customer_store_preferences(df)

    assert result.iloc[0]["most_visited_store"] == "S1"


def test_movement_records_are_ignored():
    df = pd.DataFrame({
        "customer_id": ["C1", "C1"],
        "store_id": ["S1", None],
        "location_type": ["Store", "Movement"],
    })

    result = analyze_customer_store_preferences(df)

    assert len(result) == 1
    assert result.iloc[0]["total_store_visits"] == 1


def test_blank_ids_are_ignored():
    df = pd.DataFrame({
        "customer_id": ["C1", " "],
        "store_id": ["S1", "S2"],
        "location_type": ["Store", "Store"],
    })

    result = analyze_customer_store_preferences(df)

    assert len(result) == 1
    assert result.iloc[0]["customer_id"] == "C1"


def test_missing_required_column():
    df = pd.DataFrame({
        "customer_id": ["C1"],
        "store_id": ["S1"],
    })

    with pytest.raises(ValueError, match="Missing required columns"):
        analyze_customer_store_preferences(df)


def test_no_store_visits():
    df = pd.DataFrame({
        "customer_id": ["C1"],
        "store_id": [None],
        "location_type": ["Movement"],
    })

    result = analyze_customer_store_preferences(df)

    assert result.empty