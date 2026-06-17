# AWS Glue Catalog

## Overview

AWS Glue provides metadata management for the UK Housing Intelligence Platform.

Glue Crawlers scan datasets stored in Amazon S3 and automatically create catalog tables.

Athena uses the catalog to query datasets without loading data into a database.

---

## Glue Database

```text
uk_housing_intelligence
```

---

## Silver Layer Tables

- property_prices
- housing_master
- property_geography
- postcode_clean
- crime_clean

---

## Gold Layer Tables

- housing_index
- rankings
- opportunity_explorer
- regional_intelligence
- transport_intelligence
- school_intelligence
- healthcare_intelligence
- trends

---

## Benefits

- Serverless metadata management
- Automatic schema discovery
- Athena integration
- Supports future Snowflake ingestion