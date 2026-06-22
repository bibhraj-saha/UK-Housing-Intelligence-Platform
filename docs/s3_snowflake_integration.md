# Snowflake S3 Integration

## Project

UK Housing Intelligence Platform

---

# Purpose

This document defines the integration between AWS S3 and Snowflake.

The integration enables Snowflake to read Gold Layer datasets directly from the AWS Data Lake.

---

# AWS Environment

## Data Lake Bucket

```text
uk-housing-intelligence-platform-datalake-883627150629
```

## Gold Layer Path

```text
s3://uk-housing-intelligence-platform-datalake-883627150629/gold/
```

---

# Snowflake Components

## Storage Integration

```text
UK_HOUSING_S3_INT
```

Purpose:

Secure connection between Snowflake and AWS S3.

---

## External Stage

```text
RAW.GOLD_STAGE
```

Purpose:

Provides access to all Gold Layer datasets stored in S3.

---

# Gold Layer Structure

```text
gold/
├── affordability/
├── crime_scores/
├── growth_scores/
├── healthcare_intelligence/
├── housing_index/
├── investment_scores/
├── location_intelligence/
├── opportunity_explorer/
├── rankings/
├── regional_intelligence/
├── school_intelligence/
├── transport_intelligence/
└── trends/
```

---

# Data Flow

```text
AWS S3 Gold Layer
        │
        ▼
Storage Integration
        │
        ▼
Snowflake External Stage
        │
        ▼
Snowflake RAW Tables
        │
        ▼
dbt Transformations
```

---

# Security Model

Snowflake accesses AWS S3 using an IAM trust relationship.

Permissions are restricted to:

```text
s3://uk-housing-intelligence-platform-datalake-883627150629/gold/
```

No write permissions are required.

---

# Validation Queries

```sql
SHOW STAGES;
```

```sql
DESC STAGE GOLD_STAGE;
```

```sql
LIST @GOLD_STAGE;
```

---

# Future Usage

Example data loading:

```sql
COPY INTO RAW.CRIME_SCORES
FROM @GOLD_STAGE/crime_scores;
```

```sql
COPY INTO RAW.RANKINGS
FROM @GOLD_STAGE/rankings;
```