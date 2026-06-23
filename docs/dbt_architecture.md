# dbt Architecture

## Project

UK Housing Intelligence Platform

---

# Purpose

dbt is used to transform RAW Snowflake tables into analytical models.

---

# Warehouse Layers

```text
RAW
    ↓
STAGING
    ↓
DIMENSIONS
    ↓
MARTS
```

---

# STAGING Layer

Purpose:

- Standardize column names
- Apply data typing
- Remove duplicates
- Basic cleansing

Examples:

```text
stg_crime_scores
stg_growth_scores
stg_housing_intelligence
```

---

# DIMENSIONS Layer

Purpose:

Reusable business entities.

Examples:

```text
dim_area
dim_region
dim_local_authority
```

---

# MARTS Layer

Purpose:

Business-ready analytical datasets.

Examples:

```text
mart_housing_intelligence
mart_investment_opportunities
mart_location_intelligence
```

---

# Data Flow

```text
AWS S3
    ↓
Snowflake RAW
    ↓
dbt STAGING
    ↓
dbt DIMENSIONS
    ↓
dbt MARTS
    ↓
Dashboard
```