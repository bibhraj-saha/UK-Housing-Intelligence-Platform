# Data Inventory

## Overview

This document inventories all Gold Layer datasets that will be loaded into Snowflake during Phase 8 of the UK Housing Intelligence Platform.

### Source Location

```text
data/analytics/
```

### Target Warehouse

```text
Snowflake
Database: UK_HOUSING_DW
Schema: RAW
```

### Data Warehouse Loading Strategy

The following datasets will be loaded into Snowflake RAW tables:

- Area Analytics
- Housing Intelligence
- Geographic Intelligence
- Scoring Models
- Rankings
- Trend Analysis

The following datasets will NOT be loaded as permanent RAW tables because they are report outputs generated from ranking datasets:

```text
top_100_areas.parquet
bottom_100_areas.parquet
```

These outputs will be generated from Snowflake MART tables and dashboard queries.

---

# Geography Intelligence Datasets

## regional_intelligence.parquet

### Source

```text
data/analytics/regional_intelligence.parquet
```

### File Type

Parquet

### File Size

6.7 KB

### Rows

INSERT_ROW_COUNT_HERE

### Columns

INSERT_COLUMN_COUNT_HERE

### Business Purpose

Provides regional-level housing intelligence metrics used for regional comparison, benchmarking, and strategic reporting.

### Target Snowflake Table

```sql
RAW.REGIONAL_INTELLIGENCE
```

### Primary Analytical Use Cases

- Regional benchmarking
- Market comparison
- Regional intelligence reporting

### Key Columns

- region_name
- average_price
- housing_intelligence_index

---

## location_intelligence.parquet

### Source

```text
data/analytics/location_intelligence.parquet
```

### File Type

Parquet

### File Size

896 KB

### Rows

INSERT_ROW_COUNT_HERE

### Columns

INSERT_COLUMN_COUNT_HERE

### Business Purpose

Provides location-level geographic intelligence including coordinates and area-level metadata.

### Target Snowflake Table

```sql
RAW.LOCATION_INTELLIGENCE
```

### Primary Analytical Use Cases

- Mapping
- Geographic analysis
- Area intelligence

### Key Columns

- lsoa_code
- latitude
- longitude

---

## school_intelligence.parquet

### Source

```text
data/analytics/school_intelligence.parquet
```

### File Type

Parquet

### File Size

402 KB

### Rows

INSERT_ROW_COUNT_HERE

### Columns

INSERT_COLUMN_COUNT_HERE

### Business Purpose

Provides school accessibility indicators to support residential and family-oriented housing decisions.

### Target Snowflake Table

```sql
RAW.SCHOOL_INTELLIGENCE
```

### Primary Analytical Use Cases

- School proximity analysis
- Family housing evaluation
- Area attractiveness scoring

### Key Columns

- lsoa_code
- school_count

---

## healthcare_intelligence.parquet

### Source

```text
data/analytics/healthcare_intelligence.parquet
```

### File Type

Parquet

### File Size

280 KB

### Rows

INSERT_ROW_COUNT_HERE

### Columns

INSERT_COLUMN_COUNT_HERE

### Business Purpose

Provides healthcare accessibility metrics for evaluating community infrastructure.

### Target Snowflake Table

```sql
RAW.HEALTHCARE_INTELLIGENCE
```

### Primary Analytical Use Cases

- Healthcare accessibility analysis
- Area comparison
- Investment evaluation

### Key Columns

- lsoa_code
- healthcare_score

---

## transport_intelligence.parquet

### Source

```text
data/analytics/transport_intelligence.parquet
```

### File Type

Parquet

### File Size

389 KB

### Rows

INSERT_ROW_COUNT_HERE

### Columns

INSERT_COLUMN_COUNT_HERE

### Business Purpose

Provides transport accessibility metrics used for commuter and connectivity analysis.

### Target Snowflake Table

```sql
RAW.TRANSPORT_INTELLIGENCE
```

### Primary Analytical Use Cases

- Commuter accessibility analysis
- Connectivity assessment
- Area desirability scoring

### Key Columns

- lsoa_code
- transport_score

---

# Housing Intelligence Datasets

## area_analytics_base.parquet

### Source

```text
data/analytics/area_analytics_base.parquet
```

### File Type

Parquet

### File Size

2.3 MB

### Rows

INSERT_ROW_COUNT_HERE

### Columns

INSERT_COLUMN_COUNT_HERE

### Business Purpose

Core analytical dataset containing area-level metrics used throughout the platform.

### Target Snowflake Table

```sql
RAW.AREA_ANALYTICS_BASE
```

---

## housing_intelligence.parquet

### Source

```text
data/analytics/housing_intelligence.parquet
```

### File Type

Parquet

### File Size

5.0 MB

### Rows

INSERT_ROW_COUNT_HERE

### Columns

INSERT_COLUMN_COUNT_HERE

### Business Purpose

Master housing intelligence dataset containing final area-level intelligence metrics.

### Target Snowflake Table

```sql
RAW.HOUSING_INTELLIGENCE
```

---

## housing_map.parquet

### Source

```text
data/analytics/housing_map.parquet
```

### File Type

Parquet

### File Size

2.2 MB

### Rows

INSERT_ROW_COUNT_HERE

### Columns

INSERT_COLUMN_COUNT_HERE

### Business Purpose

Optimized dataset supporting geographic visualization and mapping functionality.

### Target Snowflake Table

```sql
RAW.HOUSING_MAP
```

---

# Scoring Datasets

## crime_scores.parquet

### Source

```text
data/analytics/crime_scores.parquet
```

### File Type

Parquet

### File Size

2.4 MB

### Rows

INSERT_ROW_COUNT_HERE

### Columns

INSERT_COLUMN_COUNT_HERE

### Business Purpose

Crime risk scoring model outputs used in housing intelligence calculations.

### Target Snowflake Table

```sql
RAW.CRIME_SCORES
```

---

## growth_scores.parquet

### Source

```text
data/analytics/growth_scores.parquet
```

### File Type

Parquet

### File Size

3.3 MB

### Rows

INSERT_ROW_COUNT_HERE

### Columns

INSERT_COLUMN_COUNT_HERE

### Business Purpose

Property growth scoring model outputs used to identify high-growth housing markets.

### Target Snowflake Table

```sql
RAW.GROWTH_SCORES
```

---

## investment_scores.parquet

### Source

```text
data/analytics/investment_scores.parquet
```

### File Type

Parquet

### File Size

4.3 MB

### Rows

INSERT_ROW_COUNT_HERE

### Columns

INSERT_COLUMN_COUNT_HERE

### Business Purpose

Investment attractiveness scoring outputs used for opportunity identification.

### Target Snowflake Table

```sql
RAW.INVESTMENT_SCORES
```

---

# Rankings & Opportunities

## rankings.parquet

### Source

```text
data/analytics/rankings.parquet
```

### File Type

Parquet

### File Size

1.8 MB

### Rows

INSERT_ROW_COUNT_HERE

### Columns

INSERT_COLUMN_COUNT_HERE

### Business Purpose

Stores final area ranking outputs generated by the Housing Intelligence Platform.

### Target Snowflake Table

```sql
RAW.RANKINGS
```

### Primary Analytical Use Cases

- Dashboard rankings
- Leaderboards
- Area comparison

### Key Columns

- area_rank
- percentile_rank

---

## opportunity_explorer.parquet

### Source

```text
data/analytics/opportunity_explorer.parquet
```

### File Type

Parquet

### File Size

1.8 MB

### Rows

INSERT_ROW_COUNT_HERE

### Columns

INSERT_COLUMN_COUNT_HERE

### Business Purpose

Provides investment opportunity intelligence for identifying high-potential housing markets.

### Target Snowflake Table

```sql
RAW.OPPORTUNITY_EXPLORER
```

### Primary Analytical Use Cases

- Opportunity screening
- Investment analysis
- Market prioritization

### Key Columns

- investment_score
- growth_score
- housing_intelligence_index

---

# Trend Analysis Datasets

## historical_housing_trends.parquet

### Source

```text
data/analytics/historical_housing_trends.parquet
```

### File Type

Parquet

### File Size

7.3 MB

### Rows

INSERT_ROW_COUNT_HERE

### Columns

INSERT_COLUMN_COUNT_HERE

### Business Purpose

Historical housing trend analysis across time periods.

### Target Snowflake Table

```sql
RAW.HISTORICAL_HOUSING_TRENDS
```

---

## local_authority_trends.parquet

### Source

```text
data/analytics/local_authority_trends.parquet
```

### File Type

Parquet

### File Size

588 KB

### Rows

INSERT_ROW_COUNT_HERE

### Columns

INSERT_COLUMN_COUNT_HERE

### Business Purpose

Local authority-level trend analysis and reporting.

### Target Snowflake Table

```sql
RAW.LOCAL_AUTHORITY_TRENDS
```

---

## regional_housing_trends.parquet

### Source

```text
data/analytics/regional_housing_trends.parquet
```

### File Type

Parquet

### File Size

26 KB

### Rows

INSERT_ROW_COUNT_HERE

### Columns

INSERT_COLUMN_COUNT_HERE

### Business Purpose

Regional housing trend analysis and comparison.

### Target Snowflake Table

```sql
RAW.REGIONAL_HOUSING_TRENDS
```

---

# Excluded Datasets

The following datasets will not be loaded into Snowflake as permanent RAW tables.

## top_100_areas.parquet

### Reason

Generated reporting output derived from rankings.

## bottom_100_areas.parquet

### Reason

Generated reporting output derived from rankings.

### Future Implementation

These datasets will be generated dynamically from:

```sql
MARTS.AREA_RANKINGS
```

using Snowflake SQL and dashboard queries rather than being stored physically.