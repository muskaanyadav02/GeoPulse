from src.utils.preprocess_gps_data import preprocess_gps_data
from src.geospatial.movement_metrics import calculate_movement_metrics


def run_gps_pipeline():
    print("\n========== GEOPULSE GPS PIPELINE ==========")

    # Step 1: Preprocess raw GPS data
    print("\nStep 1: GPS Data Preprocessing")
    preprocess_gps_data()

    # Step 2: Calculate movement metrics
    print("\nStep 2: GPS Movement Metrics")
    result = calculate_movement_metrics()

    print("\n========== PIPELINE COMPLETED ==========")
    print("Total records processed:", len(result))
    print("Unique customers:", result["customer_id"].nunique())
    print("Total distance (km):", round(result["distance_km"].sum(), 3))
    print("Average speed (km/h):", round(result["speed_kmh"].mean(), 3))

    return result


if __name__ == "__main__":
    run_gps_pipeline()