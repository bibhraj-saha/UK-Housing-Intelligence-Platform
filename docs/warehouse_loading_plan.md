# Warehouse Loading Plan

## Overview

This document defines the loading strategy for migrating Gold Layer datasets from AWS S3 into Snowflake RAW tables.

---

# Source Architecture

```text
AWS S3 Gold Layer
```

Source Format:

```text
Parquet
```

Source Storage:

```text
Amazon S3
```

---

# Target Architecture

```text
Database:
UK_HOUSING_DW

Schemas:
RAW
STAGING
DIMENSIONS
MARTS
ANALYTICS
```

---

# Snowflake External Stage Strategy

A single Snowflake external stage will be used.

```text
GOLD_STAGE
```

All datasets will be loaded from the AWS S3 Gold layer through this stage.

---

# Dataset Loading Plan

| Load Order | Dataset | Snowflake Table | Priority |
|------------|----------|----------------|----------|
| 1 | area_analytics_base | RAW.AREA_ANALYTICS_BASE | P1 |
| 2 | housing_intelligence | RAW.HOUSING_INTELLIGENCE | P1 |
| 3 | crime_scores | RAW.CRIME_SCORES | P1 |
| 4 | growth_scores | RAW.GROWTH_SCORES | P1 |
| 5 | investment_scores | RAW.INVESTMENT_SCORES | P1 |
| 6 | school_intelligence | RAW.SCHOOL_INTELLIGENCE | P2 |
| 7 | healthcare_intelligence | RAW.HEALTHCARE_INTELLIGENCE | P2 |
| 8 | transport_intelligence | RAW.TRANSPORT_INTELLIGENCE | P2 |
| 9 | location_intelligence | RAW.LOCATION_INTELLIGENCE | P2 |
| 10 | regional_intelligence | RAW.REGIONAL_INTELLIGENCE | P2 |
| 11 | rankings | RAW.RANKINGS | P3 |
| 12 | opportunity_explorer | RAW.OPPORTUNITY_EXPLORER | P3 |
| 13 | housing_map | RAW.HOUSING_MAP | P3 |
| 14 | historical_housing_trends | RAW.HISTORICAL_HOUSING_TRENDS | P3 |
| 15 | local_authority_trends | RAW.LOCAL_AUTHORITY_TRENDS | P3 |
| 16 | regional_housing_trends | RAW.REGIONAL_HOUSING_TRENDS | P3 |

---

# Loading Workflow

```text
AWS S3 Gold Layer
        │
        ▼
Snowflake External Stage
        │
        ▼
Snowflake RAW Tables
        │
        ▼
dbt Staging Models
        │
        ▼
dbt Dimensions
        │
        ▼
dbt Marts
```

---

# Excluded Datasets

The following datasets will not be loaded into Snowflake RAW tables.

| Dataset | Reason |
|----------|---------|
| top_100_areas | Derived reporting output |
| bottom_100_areas | Derived reporting output |

These datasets will be generated dynamically from MART tables.

---

# Future Automation

Future phases will automate dataset loading using:

- Snowflake COPY INTO
- dbt
- GitHub Actions
- Scheduled warehouse refreshes