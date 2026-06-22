# Snowflake Data Warehouse Architecture

## Database

UK_HOUSING_DW

## Schemas

RAW
STAGING
MARTS
ANALYTICS

## Warehouse

COMPUTE_WH

## Data Source

AWS S3 Gold Layer

## Transformation Layer

dbt

## Consumption Layer

- Streamlit Dashboard
- Machine Learning Models
- Athena Queries

## High-Level Architecture

AWS S3
    ↓
Snowflake Stage
    ↓
RAW Schema
    ↓
STAGING Schema
    ↓
MARTS Schema
    ↓
ANALYTICS Schema
    ↓
Dashboard / ML / Reporting