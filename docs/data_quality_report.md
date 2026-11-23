GeoPulse – Data Quality Report



Dataset Overview



\- Total GPS records: 900

\- Store records: 300

\- Movement records: 600



Data Quality Checks



Check| Result

Missing customer IDs| 0

Missing timestamps| 0

Missing latitude values| 0

Missing longitude values| 0

Missing store IDs| 600

Duplicate GPS records| 0

Invalid coordinates| 0

Missing coordinates| 0

Non-numeric coordinates| 0

Out-of-range coordinates| 0

Invalid timestamps| 0

Invalid location types| 0

Store records without store IDs| 0

Movement records with store IDs| 0

Empty customer IDs| 0



Observations



\- No missing customer IDs, timestamps, latitude values, or longitude values were found.

\- No duplicate GPS records were detected.

\- All coordinates passed latitude and longitude range checks.

\- All timestamps passed the timestamp parsing check.

\- No non-numeric coordinate values were detected in the dataset.

\- The 600 missing store IDs belong to Movement records, where store IDs are expected to be blank.

\- Store records contained valid store IDs.

\- No invalid location types were detected.



Validation Improvements



The Python data-quality validation script was enhanced to:



\- Convert latitude and longitude values into numeric format for validation.

\- Detect missing coordinate values.

\- Identify non-numeric coordinate values.

\- Detect latitude and longitude values outside their valid ranges.

\- Generate separate counts for each coordinate-validation issue.



Automated tests were added to check missing, non-numeric, and out-of-range GPS coordinates.



Conclusion



The dataset passed the structural data-quality checks performed by the Python validation script.



The validation report showed zero detected coordinate, timestamp, duplicate-record, and location-type issues.



Limitation: These checks do not verify whether GPS points represent actual store visits or whether the location data is geographically accurate.

