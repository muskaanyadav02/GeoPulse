GeoPulse – Data Quality Report

1. Dataset Overview

- Total GPS records: 900
- Store records: 300
- Movement records: 600

2. Data Quality Checks

Check| Result
Missing customer IDs| 0
Missing timestamps| 0
Missing latitude values| 0
Missing longitude values| 0
Missing store IDs| 600
Duplicate GPS records| 0
Invalid coordinates| 0
Invalid timestamps| 0

3. Observations

- No missing customer IDs, timestamps, latitude values, or longitude values were found.
- No duplicate GPS records were detected.
- All coordinates passed basic latitude and longitude range checks.
- All timestamps passed the timestamp parsing check.
- The 600 missing store IDs belong to Movement records, where store IDs are expected to be blank.

4. Conclusion

The dataset passed the basic structural data-quality checks performed by the Python validation script.

Limitation: These checks do not verify whether GPS points represent actual store visits or whether the location data is geographically accurate.