# System Architecture

## Layer 1 - Data Sources

Current Sources:
- HM Land Registry Property Transactions
- UK Police Crime Data
- ONS Postcode Directory
- ONS Geographic Reference Data
- ONS Earnings (ASHE) Data

Planned Sources:
- Registers of Scotland
- Northern Ireland House Price Data

↓

## Layer 2 - Ingestion

Technologies:
- Python
- Pandas

Responsibilities:
- Data Acquisition
- Data Extraction
- Data Standardisation
- Data Profiling Pipelines
- Data Validation Pipelines

↓

## Layer 3 - Data Quality

Responsibilities:
- Validation Rules
- Data Profiling
- Rejected Records Handling
- Join Quality Assessment
- Geographic Key Verification
- Data Quality Reporting

↓

## Layer 4 - Processed Data Layer

Datasets:
- property_prices_clean.csv
- crime_clean.csv
- postcodes_clean.csv

Responsibilities:
- Dataset Cleaning
- Standardisation
- Transformation
- Validation

↓

## Layer 5 - Integrated Data Layer

Datasets:
- property_geography.csv
- crime_lsoa_summary.csv
- housing_master_dataset.csv
- housing_master_dataset.parquet

Responsibilities:
- Geographic Enrichment
- Crime Aggregation
- Income Enrichment
- Feature Engineering
- Analytical Dataset Creation

↓

## Layer 6 - Cloud Data Lake

Technology:
- AWS S3

Architecture:
- Bronze Layer
- Silver Layer
- Gold Layer

Supporting Services:
- AWS Glue Data Catalog
- Amazon Athena
- Terraform
- GitHub Actions

Responsibilities:
- Cloud Storage
- Data Lake Management
- Metadata Cataloging
- Query Layer
- Infrastructure as Code

↓

## Layer 7 - Data Warehouse

Technology:
- Snowflake

Responsibilities:
- Data Warehousing
- Structured Analytics Storage
- Warehouse Compute
- Secure Data Access
- Analytical Query Processing

↓

## Layer 8 - Analytics Engineering

Technology:
- dbt

Responsibilities:
- Data Transformations
- Business Logic
- Fact Tables
- Dimension Tables
- Star Schema Modelling
- Data Testing
- Documentation Generation
- Data Lineage

↓

## Layer 9 - Governance

Responsibilities:
- Data Catalog
- Data Lineage
- Metadata Management
- Audit Tracking
- Data Quality Controls
- Governance Documentation

↓

## Layer 10 - Analytics Applications

Technologies:
- Streamlit
- Plotly

Responsibilities:
- Dashboarding
- KPI Reporting
- Area Rankings
- Investment Analysis
- Regional Intelligence
- Interactive Visualisations

↓

## Layer 11 - Machine Learning

Technologies:
- Scikit-Learn
- XGBoost

Responsibilities:
- Price Prediction
- Growth Forecasting
- Recommendation Models
- Housing Intelligence Forecasting

---

## Orchestration Layer

Technology:
- Apache Airflow

Responsibilities:
- Pipeline Scheduling
- Workflow Automation
- Dependency Management
- Retry Logic
- Failure Handling
- Notifications
- End-to-End Pipeline Orchestration

Airflow Orchestrates:

Data Acquisition
↓
Data Processing
↓
Data Enrichment
↓
AWS S3 Data Lake Loads
↓
Snowflake Loads
↓
dbt Transformations
↓
Analytics Dataset Refresh
↓
Dashboard Refresh