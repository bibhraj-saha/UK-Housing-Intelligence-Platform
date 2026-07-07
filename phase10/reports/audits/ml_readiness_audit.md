# Phase 10 ML Readiness Audit

## Audit Metadata

- **Project:** UK Housing Intelligence Platform
- **Phase:** 10
- **Generated at UTC:** 2026-07-07T09:03:59.991559+00:00
- **Overall decision:** **NO_GO**

## Executive Summary

- Datasets discovered: 91
- Successfully profiled datasets: 91
- Failed dataset profiles: 0
- Temporal datasets: 53
- Geography datasets: 79
- Candidate-target datasets: 61
- Leakage-review datasets: 69

## Observed Data Signals

| Signal | Observed |
|---|---|
| `has_datasets` | Yes |
| `has_price_signal` | Yes |
| `has_growth_signal` | Yes |
| `has_investment_signal` | Yes |
| `has_geography_signal` | Yes |
| `has_temporal_signal` | Yes |
| `has_feature_signal` | Yes |
| `has_repeated_observation_signal` | Yes |

## Task Readiness

| Task | Status | Missing Signals | Missing Controls |
|---|---|---|---|

## Detailed Task Assessments

## Dataset Inventory

| Dataset | Status | Rows | Columns | Temporal | Geography | Candidate Targets |
|---|---|---:|---:|---|---|---|
| `data/analytics/area_analytics_base.parquet` | success | 35671 | 18 | None | latitude, longitude, lsoa_code, region | average_price, median_price, price_to_income_ratio |
| `data/analytics/bottom_100_areas.parquet` | success | 100 | 28 | None | latitude, longitude, lsoa_code, region | average_price, average_price_to_crime_ratio, growth_score, investment_opportunity_score, investment_score, median_price, price_to_income_ratio |
| `data/analytics/crime_scores.parquet` | success | 35671 | 19 | None | latitude, longitude, lsoa_code, region | average_price, median_price, price_to_income_ratio |
| `data/analytics/growth_scores.parquet` | success | 35671 | 26 | None | latitude, longitude, lsoa_code, region | average_price, growth_score, median_price, price_to_income_ratio |
| `data/analytics/healthcare_intelligence.parquet` | success | 35671 | 3 | None | lsoa_code | None |
| `data/analytics/historical_housing_trends.parquet` | success | 1106405 | 11 | month, year | latitude, longitude, lsoa_code, region | average_price, median_price |
| `data/analytics/housing_intelligence.parquet` | success | 35671 | 38 | warehouse_loaded_at | latitude, longitude, lsoa_code, region, region_key | average_price, growth_score, investment_score, median_price, price_to_income_ratio |
| `data/analytics/housing_map.parquet` | success | 35671 | 10 | None | latitude, longitude, lsoa_code, region | growth_score, investment_score |
| `data/analytics/investment_scores.parquet` | success | 35671 | 29 | None | latitude, longitude, lsoa_code, region | average_price, average_price_to_crime_ratio, growth_score, investment_opportunity_score, investment_score, median_price, price_to_income_ratio |
| `data/analytics/local_authority_trends.parquet` | success | 12711 | 11 | month, year | region | average_price, median_price, mom_price_growth_pct, rolling_12m_average_price, yoy_price_growth_pct |
| `data/analytics/location_intelligence.parquet` | success | 35671 | 22 | None | lsoa_code | None |
| `data/analytics/opportunity_explorer.parquet` | success | 35671 | 10 | None | lsoa_code, region | average_price, growth_score, investment_score |
| `data/analytics/rankings.parquet` | success | 35671 | 13 | None | latitude, longitude, lsoa_code, region | None |
| `data/analytics/regional_housing_trends.parquet` | success | 400 | 10 | month, year | region | average_price, median_price, mom_price_growth_pct, rolling_12m_average_price, yoy_price_growth_pct |
| `data/analytics/regional_intelligence.parquet` | success | 10 | 9 | None | region, regional_rank | average_price, growth_score, investment_score |
| `data/analytics/school_intelligence.parquet` | success | 35671 | 7 | None | lsoa_code | None |
| `data/analytics/top_100_areas.parquet` | success | 100 | 28 | None | latitude, longitude, lsoa_code, region | average_price, average_price_to_crime_ratio, growth_score, investment_opportunity_score, investment_score, median_price, price_to_income_ratio |
| `data/analytics/transport_intelligence.parquet` | success | 35671 | 8 | None | lsoa_code | None |
| `data/external/crime/2026-04/2026-04-avon-and-somerset-street.csv` | success | 16657 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-bedfordshire-street.csv` | success | 5171 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-cambridgeshire-street.csv` | success | 7047 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-cheshire-street.csv` | success | 6939 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-city-of-london-street.csv` | success | 736 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-cleveland-street.csv` | success | 7712 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-cumbria-street.csv` | success | 3320 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-derbyshire-street.csv` | success | 8993 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-devon-and-cornwall-street.csv` | success | 12193 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-dorset-street.csv` | success | 4696 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-durham-street.csv` | success | 6839 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-dyfed-powys-street.csv` | success | 3775 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-essex-street.csv` | success | 14073 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-hampshire-street.csv` | success | 13653 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-hertfordshire-street.csv` | success | 9070 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-humberside-street.csv` | success | 8528 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-kent-street.csv` | success | 14704 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-lancashire-street.csv` | success | 13737 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-leicestershire-street.csv` | success | 8332 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-lincolnshire-street.csv` | success | 6141 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-merseyside-street.csv` | success | 12146 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-metropolitan-street.csv` | success | 91664 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-norfolk-street.csv` | success | 5554 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-north-wales-street.csv` | success | 5594 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-north-yorkshire-street.csv` | success | 5140 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-northamptonshire-street.csv` | success | 6145 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-northern-ireland-street.csv` | success | 11508 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-northumbria-street.csv` | success | 12745 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-nottinghamshire-street.csv` | success | 11165 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-south-wales-street.csv` | success | 10502 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-south-yorkshire-street.csv` | success | 14700 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-staffordshire-street.csv` | success | 9150 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-suffolk-street.csv` | success | 4083 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-surrey-street.csv` | success | 7481 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-sussex-street.csv` | success | 14411 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-thames-valley-street.csv` | success | 16377 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-warwickshire-street.csv` | success | 4325 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-west-mercia-street.csv` | success | 8456 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-west-midlands-street.csv` | success | 26616 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-west-yorkshire-street.csv` | success | 24265 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/crime/2026-04/2026-04-wiltshire-street.csv` | success | 4522 | 12 | Month | LSOA code, LSOA name, Latitude, Longitude | Last outcome category |
| `data/external/healthcare/etr.csv` | success | 273 | 27 | None | None | None |
| `data/external/healthcare/ets.csv` | success | 45731 | 27 | None | None | None |
| `data/external/healthcare/wlhb.csv` | success | 6 | 27 | None | None | None |
| `data/external/healthcare/wlhbsite.csv` | success | 918 | 27 | None | None | None |
| `data/external/schools/edubasealldata20260615.csv` | success | 52397 | 135 | AccreditationExpiryDate, CensusDate, CloseDate, DateOfLastInspectionVisit | DistrictAdministrative (code), DistrictAdministrative (name), LSOA (code), LSOA (name), MSOA (code), MSOA (name), Postcode | None |
| `data/external/schools/wales/maintained_schools_wg.csv` | success | 1440 | 36 | None | postcode | None |
| `data/external/transport/Stops.csv` | success | 434935 | 43 | None | Latitude, Longitude | None |
| `data/processed/crime_clean.csv` | success | 478865 | 18 | crime_month, crime_year, month | latitude, longitude, lsoa_code, lsoa_name | last_outcome_category |
| `data/processed/crime_lsoa_summary.csv` | success | 32789 | 5 | None | lsoa_code | None |
| `data/processed/crime_lsoa_summary.parquet` | success | 32789 | 5 | None | lsoa_code | None |
| `data/processed/housing_master_dataset.csv` | success | 2816596 | 35 | transfer_date, transfer_month, transfer_year | district, latitude, longitude, lsoa_code, msoa_code, postcode | price, price_to_crime_ratio |
| `data/processed/housing_master_dataset.parquet` | success | 2816596 | 35 | transfer_date, transfer_month, transfer_year | district, latitude, longitude, lsoa_code, msoa_code, postcode | price, price_to_crime_ratio |
| `data/processed/postcodes_clean.csv` | success | 2723596 | 8 | None | latitude, longitude, lsoa_code, msoa_code, postcode | None |
| `data/processed/postcodes_clean.parquet` | success | 2723596 | 8 | None | latitude, longitude, lsoa_code, msoa_code, postcode | None |
| `data/processed/property_geography.csv` | success | 2816596 | 29 | transfer_date, transfer_month, transfer_year | district, latitude, longitude, lsoa_code, msoa_code, postcode | price |
| `data/processed/property_geography.parquet` | success | 2816596 | 29 | transfer_date, transfer_month, transfer_year | district, latitude, longitude, lsoa_code, msoa_code, postcode | price |
| `data/processed/property_prices_clean.csv` | success | 2816596 | 22 | transfer_date, transfer_month, transfer_year | district, postcode | price |
| `data/processed/property_prices_clean.parquet` | success | 2816596 | 22 | transfer_date, transfer_month, transfer_year | district, postcode | price |
| `data/raw/land_registry/pp-2023.csv` | success | 860329 | 16 | None | None | None |
| `data/raw/land_registry/pp-2024.csv` | success | 927622 | 16 | None | None | None |
| `data/raw/land_registry/pp-2025.csv` | success | 879385 | 16 | None | None | None |
| `data/raw/land_registry/pp-2026.csv` | success | 149256 | 16 | None | None | None |
| `data/reference/geography/country_lookup.csv` | success | 7 | 4 | None | None | None |
| `data/reference/geography/geography_master_lookup.csv` | success | 43916 | 9 | None | latitude, longitude, lsoa_code, region, region_code | None |
| `data/reference/geography/local_authority_lookup.csv` | success | 361 | 4 | None | None | None |
| `data/reference/geography/lsoa_geography_lookup.csv` | success | 43916 | 6 | None | latitude, longitude, lsoa_code, region_code | None |
| `data/reference/geography/region_lookup.csv` | success | 9 | 4 | None | None | None |
| `data/reference/healthcare/healthcare_lookup.csv` | success | 46649 | 5 | None | lsoa_code, postcode | None |
| `data/reference/income/income_lookup.csv` | success | 356 | 5 | None | None | None |
| `data/reference/income/regional_income_lookup.csv` | success | 10 | 5 | None | region, region_code | None |
| `data/reference/postcodes/ONS_Postcode_Directory_(February_2026)_for_the_UK_(Hosted_Table).csv` | success | 2723596 | 54 | None | lsoa01cd, lsoa11cd, lsoa21cd, msoa01cd, msoa11cd, msoa21cd | None |
| `data/reference/schools/school_lookup.csv` | success | 28153 | 5 | None | lsoa_code | None |

## Dataset Profile Failures

No dataset profile failures were detected.

## Leakage Review Candidates

| Dataset | Column | Reason |
|---|---|---|
| `data/analytics/area_analytics_base.parquet` | `affordability_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/area_analytics_base.parquet` | `average_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/area_analytics_base.parquet` | `income_affordability_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/area_analytics_base.parquet` | `median_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/area_analytics_base.parquet` | `price_to_income_ratio` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/bottom_100_areas.parquet` | `affordability_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/bottom_100_areas.parquet` | `area_rank` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/bottom_100_areas.parquet` | `average_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/bottom_100_areas.parquet` | `average_price_to_crime_ratio` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/bottom_100_areas.parquet` | `crime_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/bottom_100_areas.parquet` | `deprivation_opportunity_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/bottom_100_areas.parquet` | `growth_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/bottom_100_areas.parquet` | `housing_intelligence_index` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/bottom_100_areas.parquet` | `income_affordability_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/bottom_100_areas.parquet` | `investment_opportunity_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/bottom_100_areas.parquet` | `investment_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/bottom_100_areas.parquet` | `market_activity_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/bottom_100_areas.parquet` | `median_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/bottom_100_areas.parquet` | `percentile_rank` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/bottom_100_areas.parquet` | `price_to_income_ratio` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/crime_scores.parquet` | `affordability_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/crime_scores.parquet` | `average_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/crime_scores.parquet` | `crime_score_v2` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/crime_scores.parquet` | `income_affordability_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/crime_scores.parquet` | `median_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/crime_scores.parquet` | `price_to_income_ratio` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/growth_scores.parquet` | `affordability_percentile` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/growth_scores.parquet` | `affordability_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/growth_scores.parquet` | `affordability_score_v2` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/growth_scores.parquet` | `average_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/growth_scores.parquet` | `crime_percentile` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/growth_scores.parquet` | `crime_score_v2` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/growth_scores.parquet` | `crime_score_v3` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/growth_scores.parquet` | `deprivation_opportunity_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/growth_scores.parquet` | `growth_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/growth_scores.parquet` | `income_affordability_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/growth_scores.parquet` | `market_activity_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/growth_scores.parquet` | `median_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/growth_scores.parquet` | `price_to_income_ratio` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/healthcare_intelligence.parquet` | `healthcare_accessibility_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/historical_housing_trends.parquet` | `average_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/historical_housing_trends.parquet` | `median_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/housing_intelligence.parquet` | `affordability_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/housing_intelligence.parquet` | `area_rank` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/housing_intelligence.parquet` | `average_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/housing_intelligence.parquet` | `crime_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/housing_intelligence.parquet` | `growth_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/housing_intelligence.parquet` | `healthcare_accessibility_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/housing_intelligence.parquet` | `housing_intelligence_index` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/housing_intelligence.parquet` | `income_affordability_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/housing_intelligence.parquet` | `investment_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/housing_intelligence.parquet` | `median_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/housing_intelligence.parquet` | `percentile_rank` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/housing_intelligence.parquet` | `price_to_income_ratio` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/housing_intelligence.parquet` | `school_accessibility_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/housing_intelligence.parquet` | `transport_accessibility_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/housing_map.parquet` | `area_rank` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/housing_map.parquet` | `growth_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/housing_map.parquet` | `housing_intelligence_index` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/housing_map.parquet` | `investment_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/investment_scores.parquet` | `affordability_percentile` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/investment_scores.parquet` | `affordability_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/investment_scores.parquet` | `affordability_score_v2` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/investment_scores.parquet` | `average_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/investment_scores.parquet` | `average_price_to_crime_ratio` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/investment_scores.parquet` | `crime_percentile` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/investment_scores.parquet` | `crime_score_v2` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/investment_scores.parquet` | `crime_score_v3` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/investment_scores.parquet` | `deprivation_opportunity_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/investment_scores.parquet` | `growth_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/investment_scores.parquet` | `income_affordability_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/investment_scores.parquet` | `investment_opportunity_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/investment_scores.parquet` | `investment_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/investment_scores.parquet` | `market_activity_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/investment_scores.parquet` | `median_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/investment_scores.parquet` | `price_to_income_ratio` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/local_authority_trends.parquet` | `average_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/local_authority_trends.parquet` | `median_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/local_authority_trends.parquet` | `mom_price_growth_pct` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/local_authority_trends.parquet` | `rolling_12m_average_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/local_authority_trends.parquet` | `yoy_price_growth_pct` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/location_intelligence.parquet` | `healthcare_accessibility_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/location_intelligence.parquet` | `healthcare_percentile_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/location_intelligence.parquet` | `location_intelligence_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/location_intelligence.parquet` | `location_percentile_rank` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/location_intelligence.parquet` | `location_rank` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/location_intelligence.parquet` | `school_accessibility_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/location_intelligence.parquet` | `school_percentile_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/location_intelligence.parquet` | `transport_accessibility_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/location_intelligence.parquet` | `transport_percentile_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/opportunity_explorer.parquet` | `area_rank` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/opportunity_explorer.parquet` | `average_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/opportunity_explorer.parquet` | `growth_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/opportunity_explorer.parquet` | `housing_intelligence_index` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/opportunity_explorer.parquet` | `investment_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/rankings.parquet` | `area_rank` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/rankings.parquet` | `housing_intelligence_index` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/rankings.parquet` | `percentile_rank` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/regional_housing_trends.parquet` | `average_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/regional_housing_trends.parquet` | `median_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/regional_housing_trends.parquet` | `mom_price_growth_pct` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/regional_housing_trends.parquet` | `rolling_12m_average_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/regional_housing_trends.parquet` | `yoy_price_growth_pct` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/regional_intelligence.parquet` | `average_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/regional_intelligence.parquet` | `growth_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/regional_intelligence.parquet` | `housing_intelligence_index` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/regional_intelligence.parquet` | `investment_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/regional_intelligence.parquet` | `regional_rank` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/school_intelligence.parquet` | `school_accessibility_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/top_100_areas.parquet` | `affordability_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/top_100_areas.parquet` | `area_rank` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/top_100_areas.parquet` | `average_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/top_100_areas.parquet` | `average_price_to_crime_ratio` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/top_100_areas.parquet` | `crime_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/top_100_areas.parquet` | `deprivation_opportunity_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/top_100_areas.parquet` | `growth_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/top_100_areas.parquet` | `housing_intelligence_index` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/top_100_areas.parquet` | `income_affordability_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/top_100_areas.parquet` | `investment_opportunity_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/top_100_areas.parquet` | `investment_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/top_100_areas.parquet` | `market_activity_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/top_100_areas.parquet` | `median_price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/top_100_areas.parquet` | `percentile_rank` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/top_100_areas.parquet` | `price_to_income_ratio` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/analytics/transport_intelligence.parquet` | `transport_accessibility_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-avon-and-somerset-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-bedfordshire-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-cambridgeshire-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-cheshire-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-city-of-london-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-cleveland-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-cumbria-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-derbyshire-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-devon-and-cornwall-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-dorset-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-durham-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-dyfed-powys-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-essex-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-hampshire-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-hertfordshire-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-humberside-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-kent-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-lancashire-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-leicestershire-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-lincolnshire-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-merseyside-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-metropolitan-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-norfolk-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-north-wales-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-north-yorkshire-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-northamptonshire-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-northern-ireland-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-northumbria-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-nottinghamshire-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-south-wales-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-south-yorkshire-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-staffordshire-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-suffolk-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-surrey-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-sussex-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-thames-valley-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-warwickshire-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-west-mercia-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-west-midlands-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-west-yorkshire-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/crime/2026-04/2026-04-wiltshire-street.csv` | `Last outcome category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/external/schools/edubasealldata20260615.csv` | `NextInspectionVisit` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/processed/crime_clean.csv` | `last_outcome_category` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/processed/housing_master_dataset.csv` | `crime_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/processed/housing_master_dataset.csv` | `deprivation_index` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/processed/housing_master_dataset.csv` | `price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/processed/housing_master_dataset.csv` | `price_to_crime_ratio` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/processed/housing_master_dataset.parquet` | `crime_score` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/processed/housing_master_dataset.parquet` | `deprivation_index` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/processed/housing_master_dataset.parquet` | `price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/processed/housing_master_dataset.parquet` | `price_to_crime_ratio` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/processed/postcodes_clean.csv` | `deprivation_index` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/processed/postcodes_clean.parquet` | `deprivation_index` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/processed/property_geography.csv` | `deprivation_index` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/processed/property_geography.csv` | `price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/processed/property_geography.parquet` | `deprivation_index` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/processed/property_geography.parquet` | `price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/processed/property_prices_clean.csv` | `price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |
| `data/processed/property_prices_clean.parquet` | `price` | Column name or derived analytical role indicates potential target leakage and requires lineage review. |

## Leakage Interpretation

Columns flagged by this audit are **review candidates**, not automatically confirmed leakage. Derived scores, ranks, indices, future-labelled columns, predictions, and target-like columns must be traced to their source calculations before being admitted into a training feature set.

## Architectural Decision

Task readiness is evaluated from configuration-defined requirements. Fundamental data signals are derived from observed dataset evidence. Engineering controls are read from the control registry and remain incomplete until the corresponding Phase 10 engineering work is implemented and validated.

The ML layer must not train directly from analytical tables without explicit prediction contracts, target engineering, temporal cutoffs, and point-in-time feature validation.

## Required Next Actions

1. Complete the predictive data-gap assessment.
2. Define prediction contracts for every ML task.
3. Define canonical geography entities and observation time.
4. Engineer future-looking targets separately from features.
5. Create a temporal leakage policy.
6. Build point-in-time-correct feature datasets.
7. Construct temporal train, validation, and test datasets.

