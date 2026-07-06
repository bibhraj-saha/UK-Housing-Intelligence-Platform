# Phase 10 ML Readiness Audit

## Audit Metadata

- **Project:** UK Housing Intelligence Platform
- **Phase:** 10
- **Generated at UTC:** 2026-07-06T10:00:58.627216+00:00
- **Overall decision:** **CONDITIONAL_GO**

## Executive Summary

- Discovered datasets: 91
- Successfully profiled datasets: 90
- Failed dataset profiles: 1
- Datasets with temporal signals: 52
- Datasets with geography signals: 78
- Datasets with candidate target signals: 62
- Datasets requiring leakage review: 21

## Task Readiness

| ML Task | Status | Engineering Requirement |
|---|---|---|
| price_prediction | conditional_go | Requires a formally engineered future price target and point-in-time feature validation before training. |
| growth_prediction | conditional_go | Requires future growth target engineering from historically ordered price observations. |
| area_recommendation | conditional_go | Requires explicit user preference contracts, feature scaling, ranking logic, and offline evaluation. |
| forecasting | conditional_go | Requires repeated observations through time at a stable geography and frequency. |
| investment_opportunity_prediction | conditional_go | Existing investment scores are not automatically valid predictive labels. A future-outcome target must be defined. |

## Dataset Inventory

| Dataset | Rows | Columns | Temporal | Geography | Candidate Targets | Leakage Review | Status |
|---|---:|---:|---|---|---|---|---|
| data/analytics/area_analytics_base.parquet | 35671 | 18 | None detected | country, latitude, local_authority, longitude, lsoa_code, region | average_price, median_price, price_to_income_ratio | affordability_score, income_affordability_score | success |
| data/analytics/bottom_100_areas.parquet | 100 | 28 | None detected | country, latitude, local_authority, longitude, lsoa_code, region | average_price, average_price_to_crime_ratio, growth_score, housing_intelligence_index, investment_opportunity_score, investment_score, median_price, price_to_income_ratio | affordability_score, area_rank, crime_score, deprivation_opportunity_score, growth_score, housing_intelligence_index, income_affordability_score, investment_opportunity_score, investment_score, market_activity_score, percentile_rank | success |
| data/analytics/crime_scores.parquet | 35671 | 19 | None detected | country, latitude, local_authority, longitude, lsoa_code, region | average_price, median_price, price_to_income_ratio | affordability_score, crime_score_v2, income_affordability_score | success |
| data/analytics/growth_scores.parquet | 35671 | 26 | None detected | country, latitude, local_authority, longitude, lsoa_code, region | average_price, growth_score, median_price, price_to_income_ratio | affordability_score, affordability_score_v2, crime_score_v2, crime_score_v3, deprivation_opportunity_score, growth_score, income_affordability_score, market_activity_score | success |
| data/analytics/healthcare_intelligence.parquet | 35671 | 3 | None detected | lsoa_code | None detected | healthcare_accessibility_score | success |
| data/analytics/historical_housing_trends.parquet | 1106405 | 11 | month, year | country, latitude, local_authority, longitude, lsoa_code, region | average_price, median_price | None detected | success |
| data/analytics/housing_intelligence.parquet | 35671 | 38 | warehouse_loaded_at | country, latitude, local_authority, local_authority_key, longitude, lsoa_code, region, region_key | average_price, growth_score, housing_intelligence_index, investment_score, median_price, price_to_income_ratio | affordability_score, area_rank, crime_score, growth_score, healthcare_accessibility_score, housing_intelligence_index, income_affordability_score, investment_score, percentile_rank, school_accessibility_score, transport_accessibility_score | success |
| data/analytics/housing_map.parquet | 35671 | 10 | None detected | country, latitude, local_authority, longitude, lsoa_code, region | growth_score, housing_intelligence_index, investment_score | area_rank, growth_score, housing_intelligence_index, investment_score | success |
| data/analytics/investment_scores.parquet | 35671 | 29 | None detected | country, latitude, local_authority, longitude, lsoa_code, region | average_price, average_price_to_crime_ratio, growth_score, investment_opportunity_score, investment_score, median_price, price_to_income_ratio | affordability_score, affordability_score_v2, crime_score_v2, crime_score_v3, deprivation_opportunity_score, growth_score, income_affordability_score, investment_opportunity_score, investment_score, market_activity_score | success |
| data/analytics/local_authority_trends.parquet | 12711 | 11 | month, year | country, local_authority, region | average_price, median_price, mom_price_growth_pct, rolling_12m_average_price, yoy_price_growth_pct | None detected | success |
| data/analytics/location_intelligence.parquet | 35671 | 22 | None detected | lsoa_code | None detected | healthcare_accessibility_score, healthcare_percentile_score, location_intelligence_score, location_percentile_rank, location_rank, school_accessibility_score, school_percentile_score, transport_accessibility_score, transport_percentile_score | success |
| data/analytics/opportunity_explorer.parquet | 35671 | 10 | None detected | country, local_authority, lsoa_code, region | average_price, growth_score, housing_intelligence_index, investment_score | area_rank, growth_score, housing_intelligence_index, investment_score | success |
| data/analytics/rankings.parquet | 35671 | 13 | None detected | country, latitude, local_authority, longitude, lsoa_code, region | housing_intelligence_index | area_rank, housing_intelligence_index, percentile_rank | success |
| data/analytics/regional_housing_trends.parquet | 400 | 10 | month, year | country, region | average_price, median_price, mom_price_growth_pct, rolling_12m_average_price, yoy_price_growth_pct | None detected | success |
| data/analytics/regional_intelligence.parquet | 10 | 9 | None detected | region, regional_rank | average_price, growth_score, housing_intelligence_index, investment_score | growth_score, housing_intelligence_index, investment_score, regional_rank | success |
| data/analytics/school_intelligence.parquet | 35671 | 7 | None detected | lsoa_code | None detected | school_accessibility_score | success |
| data/analytics/top_100_areas.parquet | 100 | 28 | None detected | country, latitude, local_authority, longitude, lsoa_code, region | average_price, average_price_to_crime_ratio, growth_score, housing_intelligence_index, investment_opportunity_score, investment_score, median_price, price_to_income_ratio | affordability_score, area_rank, crime_score, deprivation_opportunity_score, growth_score, housing_intelligence_index, income_affordability_score, investment_opportunity_score, investment_score, market_activity_score, percentile_rank | success |
| data/analytics/transport_intelligence.parquet | 35671 | 8 | None detected | lsoa_code | None detected | transport_accessibility_score | success |
| data/external/crime/2026-04/2026-04-avon-and-somerset-street.csv | 16657 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-bedfordshire-street.csv | 5171 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-cambridgeshire-street.csv | 7047 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-cheshire-street.csv | 6939 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-city-of-london-street.csv | 736 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-cleveland-street.csv | 7712 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-cumbria-street.csv | 3320 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-derbyshire-street.csv | 8993 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-devon-and-cornwall-street.csv | 12193 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-dorset-street.csv | 4696 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-durham-street.csv | 6839 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-dyfed-powys-street.csv | 3775 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-essex-street.csv | 14073 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-hampshire-street.csv | 13653 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-hertfordshire-street.csv | 9070 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-humberside-street.csv | 8528 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-kent-street.csv | 14704 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-lancashire-street.csv | 13737 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-leicestershire-street.csv | 8332 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-lincolnshire-street.csv | 6141 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-merseyside-street.csv | 12146 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-metropolitan-street.csv | 91664 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-norfolk-street.csv | 5554 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-north-wales-street.csv | 5594 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-north-yorkshire-street.csv | 5140 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-northamptonshire-street.csv | 6145 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-northern-ireland-street.csv | 11508 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-northumbria-street.csv | 12745 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-nottinghamshire-street.csv | 11165 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-south-wales-street.csv | 10502 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-south-yorkshire-street.csv | 14700 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-staffordshire-street.csv | 9150 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-suffolk-street.csv | 4083 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-surrey-street.csv | 7481 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-sussex-street.csv | 14411 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-thames-valley-street.csv | 16377 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-warwickshire-street.csv | 4325 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-west-mercia-street.csv | 8456 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-west-midlands-street.csv | 26616 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-west-yorkshire-street.csv | 24265 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/crime/2026-04/2026-04-wiltshire-street.csv | 4522 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category | None detected | success |
| data/external/healthcare/etr.csv | 273 | 27 | None detected | None detected | None detected | None detected | success |
| data/external/healthcare/ets.csv | 45731 | 27 | None detected | None detected | None detected | None detected | success |
| data/external/healthcare/wlhb.csv | 6 | 27 | None detected | None detected | None detected | None detected | success |
| data/external/healthcare/wlhbsite.csv | 918 | 27 | None detected | None detected | None detected | None detected | success |
| data/external/schools/edubasealldata20260615.csv | unknown | unknown | None detected | None detected | None detected | None detected | failed |
| data/external/schools/wales/maintained_schools_wg.csv | 1440 | 36 | None detected | local_authority, postcode | None detected | None detected | success |
| data/external/transport/Stops.csv | 434935 | 43 | None detected | Latitude, Longitude | None detected | None detected | success |
| data/processed/crime_clean.csv | 478865 | 18 | crime_month, crime_year, month | latitude, longitude, lsoa_code, lsoa_name | last_outcome_category | None detected | success |
| data/processed/crime_lsoa_summary.csv | 32789 | 5 | None detected | lsoa_code | None detected | None detected | success |
| data/processed/crime_lsoa_summary.parquet | 32789 | 5 | None detected | lsoa_code | None detected | None detected | success |
| data/processed/housing_master_dataset.csv | 2816596 | 35 | transfer_date, transfer_month, transfer_year | country_code, district, latitude, local_authority_code, longitude, lsoa_code, msoa_code, postcode | price, price_to_crime_ratio | crime_score, deprivation_index | success |
| data/processed/housing_master_dataset.parquet | 2816596 | 35 | transfer_date, transfer_month, transfer_year | country_code, district, latitude, local_authority_code, longitude, lsoa_code, msoa_code, postcode | price, price_to_crime_ratio | crime_score, deprivation_index | success |
| data/processed/postcodes_clean.csv | 2723596 | 8 | None detected | country_code, latitude, local_authority_code, longitude, lsoa_code, msoa_code, postcode | None detected | deprivation_index | success |
| data/processed/postcodes_clean.parquet | 2723596 | 8 | None detected | country_code, latitude, local_authority_code, longitude, lsoa_code, msoa_code, postcode | None detected | deprivation_index | success |
| data/processed/property_geography.csv | 2816596 | 29 | transfer_date, transfer_month, transfer_year | country_code, district, latitude, local_authority_code, longitude, lsoa_code, msoa_code, postcode | price | deprivation_index | success |
| data/processed/property_geography.parquet | 2816596 | 29 | transfer_date, transfer_month, transfer_year | country_code, district, latitude, local_authority_code, longitude, lsoa_code, msoa_code, postcode | price | deprivation_index | success |
| data/processed/property_prices_clean.csv | 2816596 | 22 | transfer_date, transfer_month, transfer_year | district, postcode | price | None detected | success |
| data/processed/property_prices_clean.parquet | 2816596 | 22 | transfer_date, transfer_month, transfer_year | district, postcode | price | None detected | success |
| data/raw/land_registry/pp-2023.csv | 860329 | 16 | None detected | None detected | None detected | None detected | success |
| data/raw/land_registry/pp-2024.csv | 927622 | 16 | None detected | None detected | None detected | None detected | success |
| data/raw/land_registry/pp-2025.csv | 879385 | 16 | None detected | None detected | None detected | None detected | success |
| data/raw/land_registry/pp-2026.csv | 149256 | 16 | None detected | None detected | None detected | None detected | success |
| data/reference/geography/country_lookup.csv | 7 | 4 | None detected | None detected | None detected | None detected | success |
| data/reference/geography/geography_master_lookup.csv | 43916 | 9 | None detected | country, country_code, latitude, local_authority, longitude, lsoa_code, region, region_code | None detected | None detected | success |
| data/reference/geography/local_authority_lookup.csv | 361 | 4 | None detected | None detected | None detected | None detected | success |
| data/reference/geography/lsoa_geography_lookup.csv | 43916 | 6 | None detected | country_code, latitude, longitude, lsoa_code, region_code | None detected | None detected | success |
| data/reference/geography/region_lookup.csv | 9 | 4 | None detected | None detected | None detected | None detected | success |
| data/reference/healthcare/healthcare_lookup.csv | 46649 | 5 | None detected | country, lsoa_code, postcode | None detected | None detected | success |
| data/reference/income/income_lookup.csv | 356 | 5 | None detected | None detected | None detected | None detected | success |
| data/reference/income/regional_income_lookup.csv | 10 | 5 | None detected | region, region_code | None detected | None detected | success |
| data/reference/postcodes/ONS_Postcode_Directory_(February_2026)_for_the_UK_(Hosted_Table).csv | 2723596 | 54 | None detected | lsoa01cd, lsoa11cd, lsoa21cd, msoa01cd, msoa11cd, msoa21cd | None detected | None detected | success |
| data/reference/schools/school_lookup.csv | 28153 | 5 | None detected | country, lsoa_code | None detected | None detected | success |

## Leakage Interpretation

Columns flagged by this audit are **review candidates**, not automatically confirmed leakage. Derived scores, ranks, indices, future-labelled columns, predictions, and target-like columns must be traced to their source calculations before being admitted into a training feature set.

## Architectural Decision

The ML layer must not train directly from analytical tables without explicit prediction contracts, target engineering, temporal cutoffs, and point-in-time feature validation.

## Required Next Actions

1. Complete the predictive data-gap assessment.
2. Define prediction contracts for every ML task.
3. Define canonical geography entities and observation time.
4. Engineer future-looking targets separately from features.
5. Create a temporal leakage policy.
6. Build point-in-time-correct feature datasets.
7. Construct temporal train, validation, and test datasets.

