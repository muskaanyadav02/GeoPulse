GeoPulse – Store Analytics Findings

1. Overview

Store analytics was performed using the cleaned GPS dataset.

The analysis focuses on GPS records labelled as Store and examines store-wise activity and hourly activity.

2. Store-wise Analysis

Store ID| Total GPS Records| Unique Customers
STORE_01| 57| 57
STORE_02| 66| 66
STORE_03| 66| 66
STORE_04| 53| 53
STORE_05| 58| 58
Total| 300| 300

3. Hourly Activity

Hour| Total GPS Records
09:00| 100
10:00| 100
11:00| 100

4. Key Observations

- STORE_02 and STORE_03 recorded the highest number of GPS records.
- STORE_04 recorded the lowest number.
- Each of the three observed hours had 100 Store-labelled GPS records.
- The dataset contains 300 Store-labelled GPS records.

5. Limitations

- GPS records labelled as Store do not independently confirm physical customer visits.
- The available dataset covers only one date.
- More data is required to identify daily, weekly and long-term trends.
- Further spatial validation is required before drawing conclusions about store catchment areas or cannibalization.

6. Output Files

- "data/processed/store_summary.csv"
- "data/processed/hourly_store_activity.csv"

7. Conclusion

The analysis provides an initial overview of store-wise and hourly GPS activity in the GeoPulse dataset. Further spatial analysis and additional dates of data are required for deeper retail mobility insights.