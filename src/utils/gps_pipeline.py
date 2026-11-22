
from src.utils.preprocess_gps_data import preprocess_gps_data
from src.geospatial.movement_metrics import calculate_movement_metrics
from src.utils.export_parquet import export_csv_to_parquet
from src.utils.parquet_validation import validate_parquet_data
from src.utils.pipeline_report import generate_pipeline_report
from src.utils.logger import setup_logger


logger = setup_logger("GeoPulse.GPS")


def run_gps_pipeline():

    logger.info("========== GEOPULSE GPS PIPELINE STARTED ==========")

    try:
        # Step 1: GPS Data Preprocessing
        logger.info("Step 1: GPS Data Preprocessing started")

        preprocess_gps_data()

        logger.info("GPS preprocessing completed")

        # Step 2: GPS Movement Metrics
        logger.info("Step 2: GPS Movement Metrics started")

        result = calculate_movement_metrics()

        logger.info("GPS movement metrics calculated successfully")

        # Step 3: Parquet Export
        logger.info("Step 3: Parquet Export started")

        export_csv_to_parquet(
            "data/processed/cleaned_gps_data.csv",
            "data/processed/cleaned_gps_data.parquet"
        )

        export_csv_to_parquet(
            "data/processed/gps_movement_metrics.csv",
            "data/processed/gps_movement_metrics.parquet"
        )

        logger.info("Parquet export completed")

        # Step 4: Parquet Data Quality Validation
        logger.info("Step 4: Parquet Data Quality Validation started")

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

        if not all(
            item["validation_passed"]
            for item in validation_results
        ):
            raise ValueError(
                "GPS pipeline failed data quality validation!"
            )

        logger.info("Parquet data quality validation PASSED")

        # Step 5: Generate GPS Pipeline Report
        logger.info("Step 5: Generating GPS Pipeline Report")

        generate_pipeline_report(
            result,
            validation_results
        )

        logger.info("GPS pipeline report generated successfully")

        # Final Pipeline Summary
        logger.info("========== PIPELINE COMPLETED ==========")
        logger.info("Total records: %s", len(result))
        logger.info(
            "Unique customers: %s",
            result["customer_id"].nunique()
        )
        logger.info(
            "Total distance (km): %.3f",
            result["distance_km"].sum()
        )
        logger.info(
            "Average speed (km/h): %.3f",
            result["speed_kmh"].mean()
        )
        logger.info("Parquet validation: PASSED")
        logger.info("Pipeline report: GENERATED")

        return result

    except Exception:
        logger.exception("GPS pipeline execution FAILED")
        raise


if __name__ == "__main__":
    run_gps_pipeline()
