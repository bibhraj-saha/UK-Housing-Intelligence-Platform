Analytics Engineering Framework

Purpose

This framework defines how analytical data products are designed, developed, tested, deployed, and maintained within the UK Housing Intelligence Platform.

⸻

Architecture Layers

RAW

↓

STAGING

↓

INTERMEDIATE

↓

DIMENSIONS

↓

FACTS

↓

ANALYTICS MARTS

↓

CONSUMPTION LAYER

⸻

Primary Technologies

* AWS S3
* Snowflake
* dbt
* GitHub
* Streamlit

⸻

Analytics Principles

1. Single Source of Truth
2. Reusable Models
3. Tested Transformations
4. Documented Assets
5. Business-Friendly Metrics
6. Reproducible Pipelines

⸻

Consumption Layer

Primary consumer:

* Streamlit Dashboard

Future consumers:

* Airflow Pipelines
* ML Models
* External APIs
* Data Analysts