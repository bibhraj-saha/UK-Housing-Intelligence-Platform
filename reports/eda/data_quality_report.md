# Data Quality Assessment Report

## Objective

The purpose of this assessment is to identify data quality issues before data transformation and integration activities begin.

---

# House Prices Dataset

## Record Count

* Total Records: 2,816,596

## Duplicate Analysis

Duplicate records identified:

* 0

Assessment:

* No duplicate transaction records detected.

## Missing Value Analysis

Initial assessment indicates a high level of completeness across key business fields.

Further validation rules will be implemented during ETL processing.

## Price Validation

Lowest observed transaction values:

* £1 transactions detected

These records likely represent:

* lease transfers
* ownership restructures
* non-market transactions

Highest observed transaction values:

* up to £793,020,000

These are likely:

* institutional transactions
* portfolio transfers
* commercial property transactions

rather than standard residential purchases.

## Data Quality Assessment

Status: Acceptable for ETL processing.

---

# Crime Dataset

## Record Count

* Total Records: 478,865

## Duplicate Analysis

Duplicate rows identified:

* 27,103

Duplicate Crime IDs identified:

* 81,505

Further investigation will be conducted during ETL processing to determine whether these represent true duplicates or expected reporting behaviour.

## Missing Value Analysis

| Field                 | Missing Values |
| --------------------- | -------------: |
| Crime ID              |         79,799 |
| Longitude             |          6,342 |
| Latitude              |          6,342 |
| LSOA code             |         17,733 |
| LSOA name             |         17,733 |
| Last outcome category |         87,385 |
| Context               |        478,865 |

Observations:

* Context is 100% null and provides no analytical value.
* Missing Crime IDs are largely associated with Anti-social Behaviour records.
* Missing geographic attributes affect a relatively small proportion of records.

## Data Quality Assessment

Status: Acceptable for ETL processing with documented remediation requirements.

---

# Recommended ETL Rules

## House Prices

1. Flag non-market transactions.
2. Identify and review extreme price outliers.
3. Validate postcodes.
4. Standardise dates.

## Crime Data

1. Remove or investigate duplicate records.
2. Drop Context column.
3. Handle missing outcome categories.
4. Handle missing geographic information.
5. Validate Crime IDs where present.

---

# Overall Assessment

Both datasets are suitable for progression into the ETL and data engineering phase.

The identified quality issues are manageable and do not prevent further analysis or integration activities.
