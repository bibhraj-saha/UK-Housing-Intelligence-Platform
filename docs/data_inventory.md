# Data Inventory

## Overview

This document inventories all Gold Layer datasets that will be migrated from the AWS S3 Data Lake into Snowflake during Phase 8 of the UK Housing Intelligence Platform.

### Source Layer

```text
AWS S3 Gold Layer
s3://uk-housing-intelligence-platform/gold/
```

### Target Data Warehouse

```text
Database: UK_HOUSING_DW

Schemas:
- RAW
- STAGING
- DIMENSIONS
- MARTS
- ANALYTICS
```

### Loading Strategy

Datasets are first loaded into the RAW schema and subsequently transformed using dbt into STAGING, DIMENSIONS, MARTS, and ANALYTICS schemas.

---

# Inventory Summary

| Metric | Value |
|----------|----------|
| Total Gold Datasets | 18 |
| Datasets Loaded Into Snowflake | 16 |
| Excluded Datasets | 2 |
| Largest Dataset | historical_housing_trends.parquet |
| Largest Dataset Rows | 1,106,405 |
| Smallest Dataset | regional_intelligence.parquet |
| Smallest Dataset Rows | 10 |
| Primary Business Key | lsoa_code |
| Warehouse Platform | Snowflake |
| Transformation Tool | dbt |
| Data Lake Platform | AWS S3 |
| Query Engine | Athena |

---

# Dataset Catalog

| Dataset | Domain | Rows | Columns | Grain | Primary Key | Snowflake Table | Future dbt Model | Priority |
|----------|----------|----------|----------|----------|----------|----------|----------|----------|
| area_analytics_base.parquet | Housing Intelligence | 35,671 | 18 | One row per LSOA | lsoa_code | RAW.AREA_ANALYTICS_BASE | stg_area_analytics_base | P1 |
| housing_intelligence.parquet | Housing Intelligence | 35,671 | 28 | One row per LSOA | lsoa_code | RAW.HOUSING_INTELLIGENCE | stg_housing_intelligence | P1 |
| crime_scores.parquet | Scoring Engine | 35,671 | 19 | One row per LSOA | lsoa_code | RAW.CRIME_SCORES | stg_crime_scores | P1 |
| growth_scores.parquet | Scoring Engine | 35,671 | 26 | One row per LSOA | lsoa_code | RAW.GROWTH_SCORES | stg_growth_scores | P1 |
| investment_scores.parquet | Scoring Engine | 35,671 | 29 | One row per LSOA | lsoa_code | RAW.INVESTMENT_SCORES | stg_investment_scores | P1 |
| regional_intelligence.parquet | Location Intelligence | 10 | 9 | One row per Region | region | RAW.REGIONAL_INTELLIGENCE | stg_regional_intelligence | P2 |
| location_intelligence.parquet | Location Intelligence | 35,671 | 22 | One row per LSOA | lsoa_code | RAW.LOCATION_INTELLIGENCE | stg_location_intelligence | P2 |
| school_intelligence.parquet | Location Intelligence | 35,671 | 7 | One row per LSOA | lsoa_code | RAW.SCHOOL_INTELLIGENCE | stg_school_intelligence | P2 |
| healthcare_intelligence.parquet | Location Intelligence | 35,671 | 3 | One row per LSOA | lsoa_code | RAW.HEALTHCARE_INTELLIGENCE | stg_healthcare_intelligence | P2 |
| transport_intelligence.parquet | Location Intelligence | 35,671 | 8 | One row per LSOA | lsoa_code | RAW.TRANSPORT_INTELLIGENCE | stg_transport_intelligence | P2 |
| rankings.parquet | Rankings | 35,671 | 13 | One row per LSOA | lsoa_code | RAW.RANKINGS | stg_rankings | P3 |
| opportunity_explorer.parquet | Rankings | 35,671 | 10 | One row per LSOA | lsoa_code | RAW.OPPORTUNITY_EXPLORER | stg_opportunity_explorer | P3 |
| housing_map.parquet | Analytics | 35,671 | 10 | One row per LSOA | lsoa_code | RAW.HOUSING_MAP | stg_housing_map | P3 |
| historical_housing_trends.parquet | Trend Analytics | 1,106,405 | 11 | One row per LSOA-Year-Month | lsoa_code + year + month | RAW.HISTORICAL_HOUSING_TRENDS | stg_historical_housing_trends | P3 |
| local_authority_trends.parquet | Trend Analytics | 12,711 | 11 | One row per LocalAuthority-Year-Month | local_authority + year + month | RAW.LOCAL_AUTHORITY_TRENDS | stg_local_authority_trends | P3 |
| regional_housing_trends.parquet | Trend Analytics | 400 | 10 | One row per Region-Year-Month | region + year + month | RAW.REGIONAL_HOUSING_TRENDS | stg_regional_housing_trends | P3 |

---

# Excluded Datasets

These datasets will not be loaded as permanent Snowflake RAW tables.

## top_100_areas.parquet

### Reason

Generated reporting output derived from ranking datasets.

### Future Generation

```sql
SELECT *
FROM MARTS.AREA_RANKINGS
ORDER BY area_rank
LIMIT 100;
```

---

## bottom_100_areas.parquet

### Reason

Generated reporting output derived from ranking datasets.

### Future Generation

```sql
SELECT *
FROM MARTS.AREA_RANKINGS
ORDER BY area_rank DESC
LIMIT 100;
```

---

# Phase 8 Data Flow

```text
AWS S3 Gold Layer
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
Analytics & Dashboard Layer
```

---

# Future Warehouse Objects

## Core Fact Tables

- FACT_HOUSING_INTELLIGENCE
- FACT_HISTORICAL_HOUSING_TRENDS
- FACT_INVESTMENT_OPPORTUNITIES

## Dimension Tables

- DIM_LOCATION
- DIM_REGION
- DIM_SCHOOL_ACCESSIBILITY
- DIM_HEALTHCARE_ACCESSIBILITY
- DIM_TRANSPORT_ACCESSIBILITY

## Analytical Data Marts

- MART_AREA_RANKINGS
- MART_INVESTMENT_OPPORTUNITIES
- MART_HOUSING_TRENDS
- MART_REGIONAL_PERFORMANCE
- MART_LOCATION_INTELLIGENCE