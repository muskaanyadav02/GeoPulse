# GeoPulse Store Visit and Transition Analysis

## 1. Customer Store Visit Patterns

This analysis examines customer visits to individual stores.

It calculates:
- Number of visits by each customer to each store.
- Total store visits per customer.
- Percentage distribution of visits.
- Top-visited stores, including ties.

Output: `customer_store_visit_patterns.csv`

## 2. Enhanced Store Transition Analysis

This analysis examines consecutive store visits by each customer using timestamped GPS records.

It calculates:
- Previous store (from_store).
- Next store (to_store).
- Total number of transitions between each store pair.
- Number of unique customers making each transition.
- Average time between consecutive store visits in hours.
- Transition percentage for each starting store.

### Data Validation

The analysis includes:
- Validation of required input columns.
- Removal of missing and blank customer/store identifiers.
- Conversion of timestamps into datetime format.
- Removal of invalid timestamps.
- Chronological sorting of customer store visits.
- Handling of customers with no valid consecutive store visits.

Output: `store_transitions.csv`

## 3. Dataset Findings

The current dataset contains:
- 100 customers.
- 300 store visit records.
- 5 stores.
- 200 consecutive store transitions.

Each customer has three store observations, producing two transitions.

### Transition Analysis Results

The enhanced analysis identifies:
- 20 distinct store-to-store transition pairs.
- 200 total transitions.
- 1 hour average time between consecutive store observations across the reported pairs.
- Unique customer counts for each transition pair.

### Business Insights

The transition analysis helps identify:
- Which stores frequently appear as consecutive visits.
- How many different customers follow each store-to-store pattern.
- The time interval between consecutive store observations.
- The distribution of outgoing transitions from each starting store.

These insights can support retail movement analysis and store relationship studies.

## 4. Limitation

These transitions represent consecutive observed store records.

They do not establish the actual travel route or travel time between stores. The calculated time interval represents the difference between recorded timestamps, not verified travel duration.