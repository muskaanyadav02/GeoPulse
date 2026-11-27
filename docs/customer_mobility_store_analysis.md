GeoPulse – Customer Mobility and Store Preference Analysis

1. Overview

The integrated customer mobility and store preference analysis combines existing customer movement summaries with store visit records.

The analysis provides a consolidated view of customer movement behaviour and recorded store-visit patterns.

2. Dataset Overview

- Total GPS records: 900
- Unique customers: 100
- Store-labelled records: 300
- Movement records: 600
- Records per customer: 9
- Observation duration: 2 hours

3. Metrics Generated

The integrated report contains the following customer-level metrics:

Movement Metrics

- Total GPS records
- Movement records
- Store-labelled records
- Total movement distance in kilometres
- Average movement speed in km/h
- Maximum recorded speed in km/h
- Observation duration in hours

Store Visit Metrics

- Number of unique stores visited
- Most frequently recorded store
- Number of visits to the most frequently recorded store
- Total recorded store visits

4. Methodology

- Load the existing customer movement summary.
- Load the processed GPS movement dataset.
- Filter records labelled as Store.
- Validate required customer and store columns.
- Remove missing and blank customer and store identifiers.
- Count store visits for each customer.
- Identify the most frequently recorded store.
- Combine store preference metrics with the existing movement summary using customer ID.
- Generate one integrated report row per customer.

When multiple stores have the same visit count, alphabetical order is used to select a consistent result.

5. Key Findings

- Customers analysed: 100
- Total recorded store visits: 300
- Each customer has 3 store-labelled records in the dataset.

Most Frequently Recorded Store Distribution

Store| Customers
STORE_01| 57
STORE_02| 33
STORE_03| 10

STORE_01 was the most frequently recorded store for the largest number of customers.

6. Output File

"data/processed/customer_mobility_store_preferences.csv"

The output contains one integrated summary row per customer, combining movement metrics and store visit information.

7. Data Validation and Testing

The analysis includes validation for:

- Missing required columns.
- Missing customer IDs.
- Missing store IDs.
- Blank customer and store identifiers.
- Movement records being excluded from store visit analysis.
- Customers without valid store visits.
- Consistent handling of tied store visit counts.

Six automated tests verify customer store preferences, tie handling, movement record filtering, blank identifier handling, missing columns and empty store visit results.

The complete project test suite passed with 42 tests passed.

8. Business Insights

- Store visit patterns can help identify customer-store relationships.
- Movement distance and speed provide additional context for customer mobility.
- Store preference summaries can support further retail behaviour analysis.
- Integrated customer metrics can help identify patterns for future location and marketing analysis.

9. Limitations

- The dataset is simulated and covers a limited observation period.
- Store-labelled GPS records do not independently confirm physical store visits.
- The most frequently recorded store does not necessarily represent actual purchase preference.
- Alphabetical tie-breaking provides consistency but does not indicate a stronger preference.
- The analysis cannot independently establish sales cannibalisation or long-term customer behaviour.

10. Conclusion

The integrated customer mobility and store preference analysis combines movement behaviour with recorded store visit patterns. It provides a consolidated customer-level report that supports further geospatial and retail analytics in the GeoPulse project.