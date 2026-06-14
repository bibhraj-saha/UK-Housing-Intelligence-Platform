# UK Housing Intelligence Platform

An end-to-end Data Engineering and Data Science project designed to analyze the UK housing market.

Live Dashboard

https://uk-housing-intelligence-platform.streamlit.app/

## Architecture Diagram

![UK Housing Intelligence Platform Architecture](docs/architecture_diagram.png)

## Project Overview

The UK Housing Intelligence Platform combines multiple UK datasets to create an intelligence-driven view of housing markets at LSOA level.

The platform provides:

* Housing Intelligence Scoring
* Investment Opportunity Analysis
* Crime & Affordability Analysis
* Area Rankings
* Area Comparison Tools
* Interactive Dashboard

## Dashboard Screenshots

## Home

![Home] (docs/screenshots/Home.png)

## Housing Intelligence

![Housing_Intelligence_1] (docs/screenshots/Housing_Intelligence_1.png)
![Housing_Intelligence_2] (docs/screenshots/Housing_Intelligence_2.png)

## Investment Opportunities

![Investment_Opportunities_1] (docs/screenshots/Investment_Opportunities_1.png)
![Investment_Opportunities_2] (docs/screenshots/Investment_Opportunities_2.png)

## Crime & Affordability

![Crime_Affordability_1] (docs/screenshots/Crime_Affordability_1.png)
![Crime_Affordability_2] (docs/screenshots/Crime_Affordability_2.png)
![Crime_Affordability_3] (docs/screenshots/Crime_Affordability_3.png)
![Crime_Affordability_4] (docs/screenshots/Crime_Affordability_4.png)

## Area Comparision

![Area_Comparision] (docs/screenshots/Area_Comparision.png)

## Technology Stack

### Data Engineering

* Python
* Pandas
* AWS S3
* Snowflake
* dbt
* GitHub

### Analytics

* Streamlit
* Plotly

### Data Science

* Scikit-learn
* XGBoost

### Data Governance

* Data Quality Validation (Python)
* dbt Tests
* Metadata Management
* Data Catalog
* Data Lineage Documentation

## Data Governance

The platform incorporates data governance practices throughout the data lifecycle, including:

* Data quality validation
* Metadata management
* Data lineage tracking
* Data cataloging
* Auditability and traceability

Governance controls will be implemented using Python validation rules, Snowflake metadata columns, dbt tests, and project documentation.

## Documentation

* Project Scope
* Business Questions
* Data Sources
* Architecture
* Data Governance
* Data Catalog
* Data Lineage
* Roadmap

## External Data Sources

The following datasets are not stored in this repository because of their size:

- ONS Postcode Directory
- UK House Price Data
- UK Crime Data

Place downloaded datasets in:

data/reference/
data/external/
data/raw/

See the data acquisition instructions below for download links.

## Exploratory Data Analysis Highlights

The project includes exploratory analysis of major UK housing and crime datasets.

## Property Market Analysis

* UK Land Registry property transactions (2023–2026)
* Property price distributions
* Property type analysis
* County-level housing market analysis
* Data quality assessment

## Crime Analysis

* UK Police crime data (April 2026)
* Crime category analysis
* Police force analysis
* Crime distribution analysis

Outputs

Visualisations generated during the EDA phase are available in:

outputs/plots/

EDA reports are available in:

reports/eda/

## Current Status

Phase 6 Completed