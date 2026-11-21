
import json
from pathlib import Path
from datetime import datetime


def generate_pipeline_report(
    df,
    validation_results,
    output_path="data/processed/gps_pipeline_report.json"
):
    total_records = len(df)

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "pipeline_status": "SUCCESS",
        "data_summary": {
            "total_records": total_records,
            "unique_customers": int(df["customer_id"].nunique()),
            "store_visits": int(
                (df["location_type"] == "Store").sum()
            ),
            "movement_points": int(
                (df["location_type"] == "Movement").sum()
            ),
            "total_distance_km": round(
                float(df["distance_km"].sum()), 3
            ),
            "average_speed_kmh": round(
                float(df["speed_kmh"].mean()), 3
            )
        },
        "parquet_validation": {
            "cleaned_gps_data": validation_results[0],
            "gps_movement_metrics": validation_results[1],
            "overall_status": (
                "PASSED"
                if all(
                    item["validation_passed"]
                    for item in validation_results
                )
                else "FAILED"
            )
        }
    }

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("\nGPS Pipeline Report Generated!")
    print("--------------------------------")
    print("Report saved to:", output_file)

    return report
