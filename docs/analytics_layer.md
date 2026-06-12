# Analytics Layer

## Objectives

The Analytics & Intelligence Layer transforms processed housing datasets into business intelligence outputs.

This layer will generate:

- Housing KPIs
- Affordability Metrics
- Crime Metrics
- Growth Metrics
- Investment Metrics
- Composite Scores
- Rankings
- Housing Intelligence Index

---

## KPI Framework

KPIs will be created across:

- Housing
- Crime
- Investment
- Area Intelligence

---

## Scoring Methodology

Scores will be calculated using normalized metrics and weighted scoring models.

---

## Ranking Methodology

Areas will be ranked using score-based and percentile-based approaches.

---

## Housing Intelligence Index

The Housing Intelligence Index will combine multiple score categories into a single area intelligence metric.

---

## Outputs

Expected outputs:

- affordability_scores.parquet
- crime_scores.parquet
- growth_scores.parquet
- investment_scores.parquet
- housing_intelligence.parquet
- rankings.parquet

## KPI Definitions

### Housing KPIs

| KPI | Description |
|------|-------------|
| average_property_price | Average property price |
| median_property_price | Median property price |
| property_price_rank | Property price ranking |

### Crime KPIs

| KPI | Description |
|------|-------------|
| total_crime | Total recorded crimes |
| crime_rate | Crime relative to population |
| crime_rank | Crime ranking |

### Growth KPIs

| KPI | Description |
|------|-------------|
| growth_score | Area growth potential |
| growth_rank | Growth ranking |

### Investment KPIs

| KPI | Description |
|------|-------------|
| investment_score | Investment attractiveness |
| investment_rank | Investment ranking |

### Platform KPIs

| KPI | Description |
|------|-------------|
| housing_intelligence_index | Composite score |
| area_rank | Overall ranking |
| percentile_rank | Percentile ranking |

## Analytics Validation Findings

Two scoring methodologies were evaluated:

### Min-Max Normalization

Advantages:
- Simple
- Easy to interpret

Limitations:
- Highly sensitive to outliers
- Produced compressed score distributions

### Percentile-Based Scoring

Advantages:
- Resistant to outliers
- Balanced score distributions
- Better ranking performance

Decision:

Percentile-based scoring was adopted for:

- Affordability Score
- Crime Score

These scores will serve as inputs to the Growth Score, Investment Score and Housing Intelligence Index.

Growth Score

The Growth Score estimates future area potential using:

* Affordability Score
* Crime Score
* Deprivation Opportunity Score
* Market Activity Score

Investment Score

The Investment Score evaluates investment attractiveness using:

* Growth Score
* Affordability Score
* Crime Score
* Investment Opportunity Score

Housing Intelligence Index

The Housing Intelligence Index (HII) is the master score of the platform.

Components:

* Affordability Score (25%)
* Crime Score (20%)
* Growth Score (25%)
* Investment Score (30%)

Ranking Outputs

Generated outputs:

* rankings.parquet
* top_100_areas.parquet
* bottom_100_areas.parquet

Analytics Dataset

Final dataset:

housing_intelligence.parquet

Coverage:

* 35,671 LSOA areas
* Area rankings
* Percentile rankings
* Composite intelligence scores