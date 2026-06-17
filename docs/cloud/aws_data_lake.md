# AWS Data Lake Architecture

## Overview

Phase 7 introduces a cloud-native AWS Data Lake architecture for the UK Housing Intelligence Platform.

The platform uses Amazon S3 as the central storage layer and follows a Medallion Architecture approach:

- Bronze Layer
- Silver Layer
- Gold Layer

The architecture is designed to support scalable analytics, cloud querying, and future integration with Snowflake and dbt.

---

## Technology Stack

| Component | Technology |
|------------|------------|
| Cloud Storage | Amazon S3 |
| Metadata Catalog | AWS Glue Data Catalog |
| Query Engine | Amazon Athena |
| Infrastructure as Code | Terraform |
| Data Format | Parquet |
| Version Control | GitHub |

---

## S3 Bucket Structure

```text
s3://uk-housing-intelligence-platform-datalake-ACCOUNT_ID/

bronze/
silver/
gold/
```

---

## Bronze Layer

Stores raw source files exactly as received.

Examples:

- Land Registry
- ONS Income Data
- Crime Data
- School Data
- Transport Data
- Healthcare Data

No transformations occur here.

---

## Silver Layer

Stores cleaned and standardized datasets.

Examples:

- housing_master
- property_prices
- property_geography
- postcode_clean
- crime_clean

Silver datasets are converted to Parquet format for analytics performance.

---

## Gold Layer

Stores business-ready datasets.

Examples:

- housing_index
- rankings
- opportunity_explorer
- regional_intelligence
- transport_intelligence
- school_intelligence
- healthcare_intelligence

Gold datasets support dashboards and customer-facing analytics.

---

## Benefits

- Scalable
- Cost-efficient
- Cloud-native
- Analytics-ready
- Supports future Snowflake integration