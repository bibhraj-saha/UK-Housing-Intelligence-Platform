# System Architecture

## Layer 1 - Data Sources

- UK Land Registry
- ONS Earnings Data
- Crime Data
- ONS Postcode Directory

↓

## Layer 2 - Ingestion

- Python ETL
- Data Profiling Pipelines
- Data Validation Pipelines

↓

## Layer 3 - Data Quality

- Validation Rules
- Data Profiling
- Rejected Records Handling
- Join Quality Assessment

↓

## Layer 4 - Processed Data Layer

Datasets:
- property_prices_clean.csv
- crime_clean.csv
- postcodes_clean.csv

↓

## Layer 5 - Integrated Data Layer

Datasets:
- property_geography.csv
- crime_lsoa_summary.csv
- housing_master_dataset.csv
- housing_master_dataset.parquet

Responsibilities:
- Geographic enrichment
- Crime aggregation
- Feature engineering
- Analytical dataset creation

↓

## Layer 6 - Storage

- AWS S3 (Raw / Processed / Curated Zones)

↓

## Layer 7 - Data Warehouse

- Snowflake

↓

## Layer 8 - Transformation

- dbt

↓

## Layer 9 - Governance

- Data Catalog
- Data Lineage
- Metadata Management
- Audit Tracking

↓

## Layer 10 - Analytics

- Power BI

↓

## Layer 11 - Machine Learning

- Scikit-Learn
- XGBoost
