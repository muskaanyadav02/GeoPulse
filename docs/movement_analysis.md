# GeoPulse Movement Analysis

## 1. Movement Speed Anomaly Analysis

The movement speed anomaly module analyzes GPS movement records
using the Interquartile Range (IQR) method.

The method calculates Q1, Q3 and IQR to identify speeds outside
the statistical limits.

The analysis produces:
- Movement records analyzed
- Lower and upper speed limits
- Normal speed records
- Unusual speed records

The current dataset contains 600 movement records.

## 2. Customer Movement Consistency

The consistency module checks customer GPS records for:
- Duplicate timestamps
- Timestamp ordering
- Missing coordinates
- Movement and store record counts

Each customer receives a consistency status.

## 3. Output Files

- movement_speed_anomalies.csv
- customer_movement_consistency.csv

## 4. Testing

Automated unit tests verify movement filtering, anomaly detection,
customer consistency and duplicate timestamp handling.

## 5. Limitation

Statistical speed outliers are not automatically incorrect GPS
readings. They should be reviewed in the context of the dataset.