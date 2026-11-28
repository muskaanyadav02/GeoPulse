from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "cleaned_gps_data.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "store_transitions.csv"

OUTPUT_COLUMNS = [
    "from_store",
    "to_store",
    "transition_count",
    "unique_customers",
    "average_time_between_visits_hours",
    "transition_percentage",
]


def analyze_store_transitions(df):
    required_columns = [
        "customer_id",
        "timestamp",
        "store_id",
        "location_type",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    stores = df[
        df["location_type"].astype(str).str.strip().str.lower() == "store"
    ].copy()

    # Remove missing and blank customer/store identifiers.
    stores["customer_id"] = stores["customer_id"].astype("string").str.strip()
    stores["store_id"] = stores["store_id"].astype("string").str.strip()

    stores = stores.dropna(subset=["customer_id", "store_id"])

    stores = stores[
        (stores["customer_id"] != "")
        & (stores["store_id"] != "")
    ].copy()

    # Convert timestamps and remove invalid values.
    stores["timestamp"] = pd.to_datetime(
        stores["timestamp"], errors="coerce"
    )

    stores = stores.dropna(subset=["timestamp"])

    if stores.empty:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    # Preserve original order when timestamps are equal.
    stores = stores.sort_values(
        ["customer_id", "timestamp"],
        kind="mergesort",
    )

    grouped = stores.groupby("customer_id")

    stores["next_store"] = grouped["store_id"].shift(-1)
    stores["next_timestamp"] = grouped["timestamp"].shift(-1)

    transitions = stores.dropna(
        subset=["next_store", "next_timestamp"]
    ).copy()

    if transitions.empty:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    transitions["time_between_visits_hours"] = (
        transitions["next_timestamp"] - transitions["timestamp"]
    ).dt.total_seconds() / 3600

    # Summarise each store-to-store transition.
    summary = (
        transitions.groupby(["store_id", "next_store"])
        .agg(
            transition_count=("customer_id", "size"),
            unique_customers=("customer_id", "nunique"),
            average_time_between_visits_hours=(
                "time_between_visits_hours", "mean"
            ),
        )
        .reset_index()
        .rename(
            columns={
                "store_id": "from_store",
                "next_store": "to_store",
            }
        )
    )

    summary["average_time_between_visits_hours"] = (
        summary["average_time_between_visits_hours"].round(2)
    )

    summary["transition_percentage"] = (
        summary["transition_count"]
        / summary.groupby("from_store")[
            "transition_count"
        ].transform("sum")
        * 100
    ).round(2)

    return summary[OUTPUT_COLUMNS]


def main():
    df = pd.read_csv(INPUT_FILE)
    result = analyze_store_transitions(df)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False)

    print("ENHANCED STORE TRANSITION ANALYSIS")
    print("Total transitions:", result["transition_count"].sum())
    print(result.to_string(index=False))
    print("\nSaved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()