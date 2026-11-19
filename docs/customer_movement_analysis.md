GeoPulse – Customer Movement Behaviour Analysis

1. Overview

Customer movement analysis summarizes GPS movement metrics for individual customers using the existing processed GPS movement dataset.

The analysis uses previously calculated distance and speed values rather than recalculating GPS distances.

2. Dataset Overview

- Total GPS records: 900
- Unique customers: 100
- Store-labelled records: 300
- Movement records: 600
- Records per customer: 9
- Observation duration: 2 hours

3. Metrics Generated

The analysis generates the following customer-level metrics:

- Total records
- Movement records
- Store-labelled records
- Total movement distance in kilometres
- Average movement speed in km/h
- Maximum recorded movement speed in km/h
- Observation duration in hours

4. Key Results

Metric| Result
Customers analyzed| 100
Average movement distance| 2.29 km
Average speed| 1.53 km/h
Maximum recorded speed| 3.19 km/h
Observation duration| 2 hours

5. Output File

"data/processed/customer_movement_summary.csv"

The output contains one summary row per customer.

6. Execution

Run the analysis using:

"py scripts/customer_movement_analysis.py"

7. Limitations

- The analysis uses the supplied dataset and its existing movement metrics.
- GPS records labelled as Store do not independently confirm physical store visits.
- Recorded speeds are calculated from consecutive GPS observations and do not establish actual travel modes.
- The dataset covers one date and cannot establish long-term mobility patterns.
- The dataset's synthetic nature limits real-world conclusions.

8. Conclusion

Customer-level movement analysis provides a summarized view of distance, speed and observation duration in the GeoPulse dataset. It supports further exploration of retail mobility patterns.