# GeoPulse Store Visit and Transition Analysis

## 1. Customer Store Visit Patterns

This analysis examines customer visits to individual stores.

It calculates:
- Number of visits by each customer to each store.
- Total store visits per customer.
- Percentage distribution of visits.
- Top-visited stores, including ties.

Output: `customer_store_visit_patterns.csv`

## 2. Store Transition Analysis

This analysis examines consecutive store visits by each customer.

It calculates:
- Previous store.
- Next store.
- Number of transitions.
- Transition percentage for each starting store.

Output: `store_transitions.csv`

## 3. Dataset Findings

The current dataset contains:
- 100 customers.
- 300 store visit records.
- 5 stores.
- 200 consecutive store transitions.

Each customer has three store observations, producing two transitions.

## 4. Limitation

These transitions represent consecutive observed store records.
They do not establish the actual travel route or travel time between stores.