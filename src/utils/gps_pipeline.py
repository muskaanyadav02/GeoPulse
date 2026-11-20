from src.utils.preprocess_gps_data import preprocess_gps_data
from src.geospatial.movement_metrics import calculate_movement_metrics
from src.utils.export_parquet import export_csv_to_parquet
from src.utils.parquet_validation import validate_parquet_data


def run_gps_pipeline():

    print("\n========== GEOPULSE GPS PIPELINE ==========")

    # Step 1: Preprocessing
    print("\nStep 1: GPS Data Preprocessing")
    preprocess_gps_data()

    # Step 2: Movement metrics
    print("\nStep 2: GPS Movement Metrics")
    result = calculate_movement_metrics()

    # Step 3: Export to Parquet
    print("\nStep 3: Parquet Export")

    export_csv_to_parquet(
        "data/processed/cleaned_gps_data.csv",
        "data/processed/cleaned_gps_data.parquet"
    )

    export_csv_to_parquet(
        "data/processed/gps_movement_metrics.csv",
        "data/processed/gps_movement_metrics.parquet"
    )

    # Step 4: Parquet validation
    print("\nStep 4: Parquet Data Quality Validation")

    validation_results = []

    validation_results.append(
        validate_parquet_data(
            "data/processed/cleaned_gps_data.csv",
            "data/processed/cleaned_gps_data.parquet"
        )
    )

    validation_results.append(
        validate_parquet_data(
            "data/processed/gps_movement_metrics.csv",
            "data/processed/gps_movement_metrics.parquet"
        )
    )

    if not all(item["validation_passed"] for item in validation_results):
        raise ValueError("GPS pipeline failed data quality validation!")

    # Final summary
    print("\n========== PIPELINE COMPLETED ==========")
    print("Total records:", len(result))
    print("Unique customers:", result["customer_id"].nunique())
    print("Total distance (km):", round(result["distance_km"].sum(), 3))
    print("Average speed (km/h):", round(result["speed_kmh"].mean(), 3))
    print("Parquet validation: PASSED")

    return result


if __name__ == "__main__":
    run_gps_pipeline()