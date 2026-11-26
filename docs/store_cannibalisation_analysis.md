GeoPulse – Store Cannibalisation Risk Analysis

1. Objective

The objective of this analysis is to identify stores that share a significant portion of their customer base. It helps understand customer overlap and identify potential store cannibalisation risks.

2. Methodology

The analysis uses anonymised customer-store visit records from the cleaned GPS dataset.

The following steps are performed:

1. Select records where location type is Store.
2. Remove records with missing or blank customer and store IDs.
3. Identify unique customers visiting each store.
4. Calculate customers shared between every pair of stores.
5. Calculate overlap percentage using the smaller store's customer count.
6. Calculate Jaccard similarity between each store pair.
7. Classify overlap into three levels.

3. Overlap Classification

The following proposed thresholds are used:

- High: 60% or above.
- Moderate: 30% to below 60%.
- Low: Below 30%.

These thresholds are analytical assumptions used for this project.

4. Key Findings

The analysis evaluated 10 store pairs.

- Highest overlap: STORE_01 and STORE_03 – 59.65%.
- Lowest overlap: STORE_01 and STORE_05 – 42.11%.
- All 10 store pairs were classified as Moderate overlap.
- No store pair reached the proposed High-overlap threshold.

5. Business Insights

- Stores with higher customer overlap may serve similar customer segments.
- Businesses can study customer preferences and store locations to understand this similarity.
- Stores with overlapping customers may benefit from differentiated offers and targeted promotions.
- The results can support further investigation when selecting locations for new stores.

6. Output

The analysis generates:

"data/processed/store_cannibalisation_risk.csv"

The report contains store pairs, shared customers, smaller-store customer counts, overlap percentage, Jaccard similarity and overlap classification.

7. Validation and Testing

Six automated tests were added to validate:

- Store-pair generation.
- Shared customer calculation.
- Overlap percentage.
- Overlap classification.
- Missing-column validation.
- Handling of datasets without valid store records.

All 36 project tests passed successfully.

8. Limitations

This analysis identifies customer overlap, not confirmed sales cannibalisation.

The dataset is simulated and does not contain actual sales, revenue or purchase information. Further sales and geographic analysis would be required to confirm whether stores are directly competing for the same business.

9. Conclusion

The analysis successfully identifies customer overlap among store pairs and classifies potential overlap levels. These findings provide a foundation for further retail mobility and location-planning analysis in GeoPulse.