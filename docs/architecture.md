# System Architecture

## Layer 1 - Data Sources

- UK Land Registry
- ONS
- Crime Data
- Postcode Data

↓

## Layer 2 - Ingestion

- Python ETL

↓

## Layer 3 - Data Quality

- Validation Rules
- Data Profiling
- Rejected Records Handling

↓

## Layer 4 - Storage

- AWS S3

↓

## Layer 5 - Data Warehouse

- Snowflake

↓

## Layer 6 - Transformation

- dbt

↓

## Layer 7 - Governance

- Data Catalog
- Data Lineage
- Metadata Management
- Audit Tracking

↓

## Layer 8 - Analytics

- Power BI

↓

## Layer 9 - Machine Learning

- Scikit-Learn
- XGBoost