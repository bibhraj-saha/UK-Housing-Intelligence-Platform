# Phase 8 Technical Design Document

## Project

UK Housing Intelligence Platform

## Phase

Phase 8 – Data Warehouse & Transformation Layer

## Version

1.0

## Status

In Progress

---

# 1. Executive Summary

Phase 8 introduces a modern cloud data warehouse architecture to the UK Housing Intelligence Platform using Snowflake and dbt.

The objective of this phase is to migrate analytical datasets from the AWS S3 Data Lake into Snowflake, establish a scalable warehouse architecture, implement transformation logic using dbt, create dimensional models and analytical data marts, and provide a production-ready analytics platform for reporting, dashboarding, and future machine learning workloads.

This phase transforms the platform from a file-based analytics solution into a cloud-native enterprise data platform.

---

# 2. Phase Objectives

The primary objectives of Phase 8 are:

- Implement Snowflake as the enterprise data warehouse
- Establish warehouse schemas and governance structures
- Load Gold Layer datasets from AWS S3 into Snowflake
- Implement dbt for transformation management
- Build staging, dimensional, and mart layers
- Implement data quality testing
- Create analytical data marts
- Generate automated documentation and lineage
- Integrate Streamlit dashboards with Snowflake
- Prepare the platform for future orchestration and machine learning workloads

---

# 3. Business Objectives

The warehouse implementation enables:

- Centralized analytical data storage
- Scalable query performance
- Consistent business definitions
- Reusable analytical datasets
- Data governance and lineage
- Enterprise reporting capabilities
- Future AI and machine learning integration
- Cloud-native architecture aligned with modern data engineering practices

---

# 4. Existing Architecture (End of Phase 7)

Current architecture:

```text
Raw Data Sources
        │
        ▼
Python Processing Pipelines
        │
        ▼
AWS S3 Data Lake
│
├── Bronze
├── Silver
└── Gold
        │
        ▼
Athena
        │
        ▼
Streamlit Dashboard
```

---

# 5. Target Architecture (End of Phase 8)

```text
Raw Data Sources
        │
        ▼
Python Processing Pipelines
        │
        ▼
AWS S3 Data Lake
│
├── Bronze
├── Silver
└── Gold
        │
        ▼
Snowflake RAW
        │
        ▼
dbt STAGING
        │
        ▼
dbt DIMENSIONS
        │
        ▼
dbt MARTS
        │
        ▼
Streamlit Dashboard
        │
        ▼
Machine Learning & Advanced Analytics
```

---

# 6. Technology Stack

| Component | Technology |
|------------|------------|
| Cloud Platform | AWS |
| Data Lake | Amazon S3 |
| Data Warehouse | Snowflake |
| Transformation Framework | dbt |
| Query Engine | Snowflake SQL |
| Data Format | Parquet |
| Infrastructure as Code | Terraform |
| CI/CD | GitHub Actions |
| Dashboard | Streamlit |
| Programming Language | Python |
| Version Control | GitHub |

---

# 7. Snowflake Architecture

## Database

```text
UK_HOUSING_DW
```

### Schemas

```text
RAW
STAGING
DIMENSIONS
MARTS
ANALYTICS
```

### Warehouse

```text
COMPUTE_WH
```

### Stage

```text
GOLD_STAGE
```

---

# 8. Schema Design

## RAW Schema

### Purpose

Stores data loaded directly from AWS S3 without business transformations.

### Example Tables

```text
RAW.AREA_ANALYTICS_BASE
RAW.HOUSING_INTELLIGENCE
RAW.CRIME_SCORES
RAW.GROWTH_SCORES
RAW.INVESTMENT_SCORES
```

---

## STAGING Schema

### Purpose

Performs standardization and cleaning.

### Responsibilities

- Data type standardization
- Column renaming
- Null handling
- Data validation
- Business rule preparation

### Example Models

```text
STG_AREA_ANALYTICS_BASE
STG_HOUSING_INTELLIGENCE
STG_LOCATION_INTELLIGENCE
```

---

## DIMENSIONS Schema

### Purpose

Stores reusable business dimensions.

### Example Models

```text
DIM_LOCATION
DIM_REGION
DIM_SCHOOL_ACCESSIBILITY
DIM_HEALTHCARE_ACCESSIBILITY
DIM_TRANSPORT_ACCESSIBILITY
```

---

## MARTS Schema

### Purpose

Business-facing analytical datasets.

### Example Models

```text
MART_AREA_RANKINGS
MART_INVESTMENT_OPPORTUNITIES
MART_HOUSING_TRENDS
MART_REGIONAL_PERFORMANCE
MART_LOCATION_INTELLIGENCE
```

---

## ANALYTICS Schema

### Purpose

Advanced analytical outputs and machine learning datasets.

### Example Models

```text
FACT_HOUSING_INTELLIGENCE
FACT_INVESTMENT_OPPORTUNITIES
FACT_HISTORICAL_TRENDS
```

---

# 9. Dataset Inventory Summary

## Total Gold Datasets

16

## Excluded Datasets

2

### Excluded Files

```text
top_100_areas.parquet
bottom_100_areas.parquet
```

### Exclusion Reason

These are generated reporting outputs that can be dynamically created from analytical marts and ranking datasets.

---

# 10. Data Domains

## Housing Intelligence

### Datasets

```text
area_analytics_base
housing_intelligence
housing_map
```

---

## Scoring Engine

### Datasets

```text
crime_scores
growth_scores
investment_scores
```

---

## Location Intelligence

### Datasets

```text
regional_intelligence
location_intelligence
school_intelligence
healthcare_intelligence
transport_intelligence
```

---

## Rankings

### Datasets

```text
rankings
opportunity_explorer
```

---

## Trend Analytics

### Datasets

```text
historical_housing_trends
local_authority_trends
regional_housing_trends
```

---

# 11. Data Loading Strategy

## Source

```text
AWS S3 Gold Layer
```

## Source Format

```text
Parquet
```

## Loading Method

```text
Snowflake External Stage
+
COPY INTO
```

---

## Loading Sequence

### Priority 1

```text
AREA_ANALYTICS_BASE
HOUSING_INTELLIGENCE
CRIME_SCORES
GROWTH_SCORES
INVESTMENT_SCORES
```

### Priority 2

```text
SCHOOL_INTELLIGENCE
HEALTHCARE_INTELLIGENCE
TRANSPORT_INTELLIGENCE
LOCATION_INTELLIGENCE
REGIONAL_INTELLIGENCE
```

### Priority 3

```text
RANKINGS
OPPORTUNITY_EXPLORER
HOUSING_MAP
HISTORICAL_HOUSING_TRENDS
LOCAL_AUTHORITY_TRENDS
REGIONAL_HOUSING_TRENDS
```

---

# 12. dbt Architecture

## Layer 1 – Source Models

### Purpose

Reference Snowflake RAW tables.

### Examples

```text
source('raw', 'housing_intelligence')
source('raw', 'crime_scores')
```

---

## Layer 2 – Staging Models

### Purpose

Clean and standardize source datasets.

### Examples

```text
stg_housing_intelligence
stg_growth_scores
stg_location_intelligence
```

---

## Layer 3 – Dimension Models

### Purpose

Create reusable business dimensions.

### Examples

```text
dim_location
dim_region
dim_school_accessibility
```

---

## Layer 4 – Mart Models

### Purpose

Create business-ready analytical datasets.

### Examples

```text
mart_area_rankings
mart_investment_opportunities
mart_housing_trends
```

---

# 13. Data Quality Framework

The platform will implement dbt tests for:

## Uniqueness Tests

Examples:

```text
lsoa_code
region
```

---

## Not Null Tests

Examples:

```text
lsoa_code
housing_intelligence_index
investment_score
```

---

## Accepted Values Tests

Examples:

```text
country
region
```

---

## Relationship Tests

Examples:

```text
Fact Tables
↔
Dimension Tables
```

---

# 14. Documentation & Lineage

dbt documentation will provide:

- Data catalog
- Data lineage
- Model descriptions
- Column descriptions
- Dependency tracking

### Benefits

- Improved maintainability
- Faster onboarding
- Better governance
- Easier debugging

---

# 15. Dashboard Integration Strategy

## Current Dashboard Source

```text
Local Parquet Files
```

## Future Dashboard Source

```text
Snowflake
```

### Benefits

- Centralized data access
- Reduced local storage dependencies
- Faster updates
- Better scalability
- Enterprise architecture alignment

---

# 16. Security & Governance

## Access Control

Role-Based Access Control (RBAC) will be implemented.

### Example Roles

```text
SYSADMIN
DEVELOPER_ROLE
ANALYST_ROLE
```

---

## Principle of Least Privilege

Users will receive only the permissions required for their responsibilities.

---

## Auditability

Snowflake query history and warehouse monitoring will be used for auditing and operational visibility.

---

# 17. Performance Strategy

The platform will leverage:

- Parquet-based loading
- Warehouse auto-suspend
- Warehouse auto-resume
- Optimized dbt models
- Efficient Snowflake storage architecture
- Incremental processing (future enhancement)
- Clustering strategies (future enhancement)

---

# 18. Future Integration Roadmap

## Phase 9 – Workflow Orchestration

Potential technologies:

```text
Apache Airflow
GitHub Actions
Snowflake Tasks
```

### Objectives

- Automated pipeline scheduling
- Dependency management
- Monitoring and alerting
- Production orchestration

---

## Phase 10 – Machine Learning Platform

Potential use cases:

```text
Price Prediction
Investment Forecasting
Market Trend Forecasting
Regional Growth Prediction
```

### Objectives

- Predictive analytics
- Investment recommendation engines
- Housing market forecasting
- AI-powered intelligence generation

---

# 19. Expected Deliverables

At completion of Phase 8 the platform will contain:

- Snowflake Data Warehouse
- Snowflake Database
- Warehouse Schemas
- Snowflake Compute Warehouse
- External Stage Integration
- Raw Data Loads
- dbt Project
- dbt Models
- Data Quality Tests
- Documentation & Lineage
- Analytical Data Marts
- Snowflake-Powered Dashboard Integration

---

# 20. Success Criteria

Phase 8 will be considered complete when:

- All Gold datasets are successfully loaded into Snowflake
- Snowflake schemas are operational
- dbt transformations are implemented
- Data quality tests pass successfully
- Documentation and lineage are generated
- Analytical data marts are available
- Dashboard consumes Snowflake datasets
- Warehouse architecture is production-ready
- Platform is ready for orchestration and machine learning expansion

---

# Deliverables Produced During Phase 8

## Documentation

- docs/data_inventory.md
- docs/warehouse_loading_plan.md
- docs/snowflake_architecture.md
- docs/phase8_design.md

## Snowflake Components

- UK_HOUSING_DW Database
- RAW Schema
- STAGING Schema
- DIMENSIONS Schema
- MARTS Schema
- ANALYTICS Schema
- COMPUTE_WH Warehouse
- GOLD_STAGE External Stage

## dbt Components

- Source Definitions
- Staging Models
- Dimension Models
- Mart Models
- Tests
- Documentation
- Lineage Graph

## Business Outputs

- Area Rankings Mart
- Investment Opportunities Mart
- Housing Trends Mart
- Regional Performance Mart
- Location Intelligence Mart