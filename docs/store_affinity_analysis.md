GeoPulse – Customer–Store Affinity Analysis

1. Objective

Analyze customer overlap between retail stores using customer IDs from the simulated GPS dataset.

2. Methodology

- Filter records where "location_type" is "Store".
- Identify unique customers for each store.
- Calculate shared customers between every pair of stores.
- Calculate Jaccard similarity to measure customer-group overlap.
- Generate a store similarity matrix.

3. Key Findings

- STORE_02 and STORE_03 have the highest customer overlap, with 38 shared customers.
- Their Jaccard similarity is 0.4043 (40.43%).
- STORE_01 and STORE_05 have the lowest similarity, at 0.2637 (26.37%).

4. Output Files

- "store_affinity_counts.csv"
- "store_customer_overlap.csv"
- "store_similarity_matrix.csv"

5. Testing

Four automated tests were added to verify:

- Shared customer counts.
- Jaccard similarity calculation.
- Similarity matrix symmetry.
- Diagonal values equal to 1.

All four affinity tests and all five existing store analytics tests passed.

6. Limitations

The dataset is simulated and covers a limited period. Store-labelled GPS records do not independently confirm physical store visits. Customer overlap indicates similarity between recorded customer groups, not proven store cannibalization.