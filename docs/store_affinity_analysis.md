GeoPulse – Customer–Store Affinity Analysis

1. Objective

Analyze customer overlap between retail stores using customer IDs from the simulated GPS dataset. The analysis helps identify similarities between customer groups visiting different stores.

2. Methodology

- Filter records where "location_type" represents a store visit.
- Validate the required input columns.
- Normalize location types and remove missing or blank customer and store IDs.
- Identify unique customers for each store.
- Calculate shared customers between every pair of stores.
- Calculate Jaccard similarity to measure customer-group overlap.
- Generate a symmetric store similarity matrix.

3. Key Findings

- STORE_02 and STORE_03 have the highest customer overlap, with 38 shared customers.
- Their Jaccard similarity is 0.4043 (40.43%).
- STORE_01 and STORE_05 have the lowest similarity, at 0.2637 (26.37%).
- STORE_02 and STORE_03 demonstrate the strongest customer-group similarity in the dataset.

4. Output Files

- "store_affinity_counts.csv"
- "store_customer_overlap.csv"
- "store_similarity_matrix.csv"

5. Data Validation and Testing

The analysis includes input validation to handle:

- Missing required columns.
- Missing customer IDs.
- Missing store IDs.
- Blank customer and store identifiers.
- Inconsistent location-type formatting.
- Empty valid store-visit datasets.

Four automated affinity tests verify:

- Shared customer counts.
- Jaccard similarity calculation.
- Similarity matrix symmetry.
- Diagonal values equal to 1.

The complete project test suite passed with 30 tests passed after the implementation update.

6. Business Insights

- Stores with higher customer overlap may share similar customer groups.
- Customer overlap can help identify potential opportunities for cross-store promotions.
- Lower similarity may indicate differences in customer groups.
- Store affinity results can support further retail location and customer behaviour analysis.

7. Limitations

The dataset is simulated and covers a limited period. Store-labelled GPS records do not independently confirm physical store visits. Customer overlap indicates similarity between recorded customer groups, not proven store cannibalization.