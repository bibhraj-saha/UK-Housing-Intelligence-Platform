# Phase 10 ML Readiness Audit

## 1. Purpose

The Phase 10 ML Readiness Audit determines whether the existing UK Housing Intelligence Platform data architecture is suitable for reproducible machine learning.

The audit is intentionally completed before model training.

The objective is to prevent the project from treating existing analytical datasets as automatically valid machine-learning training datasets.

## 2. Architectural Context

The UK Housing Intelligence Platform has already established a multi-phase data platform containing:

- data acquisition pipelines
- data understanding and profiling
- data processing pipelines
- analytics and intelligence outputs
- a Streamlit customer application
- an AWS-based cloud data lake architecture
- Snowflake data warehousing
- dbt transformations
- Apache Airflow orchestration and automation

Phase 10 extends this platform with a reproducible machine-learning layer.

The machine-learning layer must build on the existing platform rather than operate as a disconnected collection of notebooks.

## 3. Phase 10 Readiness Principle

An analytical table is not automatically a valid training table.

Before a dataset can be used for model training, the platform must define:

1. the prediction entity
2. the observation timestamp
3. the prediction timestamp
4. the forecast horizon
5. the target variable
6. the feature availability cutoff
7. the temporal split strategy
8. the leakage policy
9. the evaluation policy

## 4. Audit Scope

The automated audit inspects supported datasets under:

- `data/analytics`
- `data/processed`
- `data/raw`
- `data/external`
- `data/reference`

The initial supported file formats are:

- Parquet
- CSV

## 5. Audit Dimensions

### 5.1 Dataset Discovery

The audit identifies machine-readable datasets available in the configured project data directories.

### 5.2 Schema Profiling

For each discovered dataset, the audit records:

- file path
- file type
- file size
- row count where available
- column count
- column names
- inferred data types
- missingness percentages
- duplicate rows within the profiled sample

### 5.3 Temporal Signal Detection

The audit identifies candidate temporal columns using:

- native datetime data types
- date-like column names
- configurable parsing thresholds

Temporal detection is a readiness signal only.

A detected date column does not prove that a dataset is suitable for forecasting or temporal supervised learning.

### 5.4 Geography Signal Detection

The audit identifies candidate geographic entities including:

- LSOA
- MSOA
- postcode
- district
- local authority
- region
- country
- latitude
- longitude

The long-term ML architecture requires explicit canonical entity definitions.

### 5.5 Candidate Target Detection

The audit identifies columns that may be related to:

- property prices
- growth
- investment outcomes
- forecasts
- explicit targets

Candidate detection does not approve a column as a target.

Every predictive target must later receive a formal prediction contract.

### 5.6 Leakage-Risk Detection

The audit flags columns whose names suggest possible leakage, including:

- future values
- target columns
- labels
- predictions
- forecasts

The audit also separately flags derived analytical fields such as:

- scores
- indices
- ranks
- rankings

Derived analytical fields are not automatically leakage.

They require lineage review before they can be admitted into a training feature set.

## 6. Readiness Decisions

The audit uses three conceptual decisions.

### 6.1 GO

A task may proceed to implementation because its entity, time, target, feature availability, and evaluation requirements are formally satisfied.

### 6.2 CONDITIONAL_GO

The data platform contains promising signals, but additional engineering controls are required before model training.

Typical missing controls include:

- future target engineering
- temporal cutoffs
- point-in-time feature generation
- leakage validation
- canonical entity definitions

### 6.3 NO_GO

The current data does not satisfy a fundamental requirement for the proposed task.

Examples include:

- no usable datasets
- no geographic entity for an area-level model
- no temporal history for a forecasting task

## 7. Expected Initial Architectural Decision

The expected initial state of the UK Housing Intelligence Platform is `CONDITIONAL_GO`.

This is intentional.

The existing platform contains strong analytical and data-engineering foundations, but Phase 10 must still formally engineer:

- prediction contracts
- future-looking targets
- canonical ML entities
- point-in-time features
- temporal validation
- leakage controls

## 8. Task-Specific Interpretation

### 8.1 Price Prediction

Price prediction requires:

- a clearly defined prediction entity
- a prediction timestamp
- a future prediction horizon
- a future price target
- features available before the prediction cutoff
- temporal validation

Current or aggregated price columns must not automatically be treated as future targets.

### 8.2 Growth Prediction

Growth prediction requires:

- historically ordered price observations
- a formal growth horizon
- a future growth calculation
- explicit handling of missing historical periods
- temporal validation

Existing analytical growth scores must not automatically become predictive labels.

### 8.3 Area Recommendation

Area recommendation requires:

- canonical area entities
- comparable features
- feature scaling
- explicit user preference inputs
- ranking logic
- recommendation evaluation

### 8.4 Forecasting

Forecasting requires:

- repeated observations through time
- stable geographic entities
- defined time frequency
- lag and rolling feature policies
- backtesting

A single current snapshot is insufficient for a genuine forecasting system.

### 8.5 Investment Opportunity Prediction

Investment opportunity prediction requires a future-outcome definition.

An existing investment score is not automatically a valid predictive target because it may be a contemporaneous analytical index rather than an observed future investment outcome.

## 9. Reproducibility

The readiness audit is implemented as reusable Python code and a command-line runner.

Primary implementation files:

- `phase10/config/readiness_audit.yml`
- `phase10/src/uk_housing_ml/audit/readiness.py`
- `phase10/scripts/run_ml_readiness_audit.py`
- `phase10/tests/unit/test_readiness.py`

Generated outputs:

- `phase10/reports/audits/ml_readiness_audit.json`
- `phase10/reports/audits/ml_readiness_audit.md`

## 10. Next Required Engineering Work

The next Phase 10 work must proceed in this order:

1. predictive data-gap assessment
2. prediction contracts
3. canonical entity and geography design
4. temporal leakage policy
5. target engineering
6. feature-store design
7. point-in-time feature generation
8. training-dataset construction
9. temporal train, validation, and test splitting
10. baseline model development

Model training must not begin before the relevant prediction contract and leakage controls are defined.