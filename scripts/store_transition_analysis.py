from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "processed" / "cleaned_gps_data.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "store_transitions.csv"

OUTPUT_COLUMNS = [
    "from_store",
    "to_store",
    "transition_count",
    "transition_percentage"
]


def analyze_store_transitions(df):
    required_columns = [
        "customer_id",
        "timestamp",
        "store_id",
        "location_type"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    stores = df[
        df["location_type"].astype(str).str.strip().str.lower() == "store"
    ].copy()

    stores["timestamp"] = pd.to_datetime(
        stores["timestamp"], errors="coerce"
    )

    stores = stores.dropna(
        subset=["customer_id", "store_id", "timestamp"]
    )

    stores = stores.sort_values(
        ["customer_id", "timestamp"],
        kind="mergesort"
    )

    stores["next_store"] = (
        stores.groupby("customer_id")["store_id"].shift(-1)
    )

    transitions = stores.dropna(subset=["next_store"])

    if transitions.empty:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    summary = (
        transitions.groupby(["store_id", "next_store"])
        .size()
        .reset_index(name="transition_count")
        .rename(columns={
            "store_id": "from_store",
            "next_store": "to_store"
        })
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

    print("STORE TRANSITION ANALYSIS")
    print("Total transitions:", result["transition_count"].sum())
    print(result.to_string(index=False))
    print("\nSaved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()