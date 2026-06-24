Data Governance Framework

Purpose

This document defines governance standards for the UK Housing Intelligence Platform Data Warehouse.

⸻

Data Domains

Housing Market

Owner: Analytics Team

Assets:

* FCT_HOUSING_INTELLIGENCE
* FCT_HOUSING_TRENDS

⸻

Geographic Intelligence

Owner: Analytics Team

Assets:

* DIM_LOCATION
* DIM_LOCAL_AUTHORITY
* DIM_REGION
* DIM_COUNTRY

⸻

Accessibility Intelligence

Owner: Analytics Team

Assets:

* MART_SCHOOL_ACCESSIBILITY
* MART_HEALTHCARE_ACCESSIBILITY
* MART_TRANSPORT_ACCESSIBILITY

⸻

Data Refresh Policy

RAW:
Daily

STAGING:
Daily

INTERMEDIATE:
Daily

DIMENSIONS:
Daily

FACTS:
Daily

MARTS:
Daily

⸻

Data Quality Requirements

Critical datasets:

* DIM_LOCATION
* FCT_HOUSING_INTELLIGENCE
* MART_AREA_PROFILE

Requirements:

* No null primary keys
* Referential integrity
* Successful dbt tests