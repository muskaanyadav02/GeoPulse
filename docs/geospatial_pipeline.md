# Geospatial Data Engineering Pipeline (Member 2)

## Overview
This module processes raw and cleaned GPS movement datasets using **PySpark** and **Apache Sedona** to analyze retail store footfall and customer movement patterns in Lucknow.

## Implemented Components

1. **Spatial Engine Setup (`spark/spatial_joins/spatial_setup.py`)**
   - Initializes PySpark with Apache Sedona spatial extensions (`SedonaContext`).

2. **Store Catchment & Spatial Join (`spark/spatial_joins/gps_spatial_join.py`)**
   - Converts customer latitude/longitude coordinates into spatial geometry points (`ST_Point`).
   - Generates 500-meter buffer catchment polygons (`ST_Buffer`) around retail stores (Hazratganj, Gomti Nagar, Indira Nagar).
   - Performs spatial joins (`ST_Contains`) to identify store visitors and exports results to `data/processed/matched_store_footfall.parquet`.

3. **Customer Movement Patterns (`spark/spatial_joins/movement_patterns.py`)**
   - Aggregates matched footfall by hour of the day to identify peak traffic hours and unique visitors per store.
   - Saves hourly analytics to `data/processed/hourly_movement_patterns.parquet`.

4. **Geospatial Utilities & Testing (`src/geospatial/geo_utils.py` & `tests/test_geospatial.py`)**
   - Includes Haversine distance calculations in meters and GPS coordinate boundary validation.
   - Verified with automated unit tests.


---

### 📍 Geospatial Data Engineering Module (By Pankaj)
- **Tech Stack:** PySpark, Apache Sedona, Python, Parquet
- **Key Features:**
  - 500-meter store catchment buffer zones (`ST_Buffer`) for Lucknow retail stores.
  - Spatial join (`ST_Contains`) matching customer GPS coordinates with store zones (`spark/spatial_joins/gps_spatial_join.py`).
  - Hourly peak customer traffic and movement pattern analysis (`spark/spatial_joins/movement_patterns.py`).
  - Haversine distance calculator, GPS validation utilities (`src/geospatial/geo_utils.py`), and automated unit tests (`tests/test_geospatial.py`).
