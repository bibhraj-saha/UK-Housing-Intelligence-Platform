# Phase 10 Predictive Data-Gap Assessment

## Assessment Metadata

- **Project:** UK Housing Intelligence Platform
- **Phase:** 10
- **Generated at UTC:** 2026-07-07T09:21:04.628398+00:00
- **Overall decision:** **CONDITIONAL_GO_WITH_MAJOR_GAPS**

## Executive Summary

- Datasets assessed: 91
- Successfully assessed datasets: 91
- Failed dataset assessments: 0
- Available feature domains: affordability, crime, deprivation, geography, growth, housing, investment, price, temporal
- Maximum detected history in months: 11.96

## Candidate Horizon Feasibility

| Horizon | Status | Reason |
|---|---|---|
| 3_months | structurally_feasible | Detected history is at least twice the candidate horizon. Entity-level coverage and point-in-time target construction still require validation. |
| 6_months | weakly_feasible | Detected history exceeds the target horizon but provides limited room for training, validation, and testing. |
| 12_months | not_feasible | Maximum detected history (11.96 months) is shorter than the 12-month horizon. |
| 24_months | not_feasible | Maximum detected history (11.96 months) is shorter than the 24-month horizon. |

## Task Assessments

| Task | Status | Missing Required Domains | Missing Recommended Domains |
|---|---|---|---|
| price_prediction | major_gaps | None | None |
| growth_prediction | major_gaps | None | None |
| area_recommendation | candidate_ready | None | None |
| forecasting | major_gaps | None | None |
| investment_opportunity_prediction | major_gaps | None | None |

## Detailed Task Gaps

### price_prediction

- **Status:** major_gaps
- **Required domains:** price, geography, temporal
- **Available required domains:** price, geography, temporal
- **Missing required domains:** None
- **Missing recommended domains:** None
- **Required history months:** 24
- **Detected maximum history months:** 11.96
- **Required median periods per entity:** 12

#### Gaps

- **high — insufficient_history:** Task requires approximately 24 months of history, but detected maximum history is 11.96.
- **high — insufficient_repeated_entity_coverage:** The best detected entity-temporal candidate does not meet the configured median periods-per-entity requirement of 12.
- **high — future_target_not_defined:** Future target 'future_price' has not yet been formally defined through a prediction contract.

### growth_prediction

- **Status:** major_gaps
- **Required domains:** price, geography, temporal
- **Available required domains:** price, geography, temporal
- **Missing required domains:** None
- **Missing recommended domains:** None
- **Required history months:** 24
- **Detected maximum history months:** 11.96
- **Required median periods per entity:** 12

#### Gaps

- **high — insufficient_history:** Task requires approximately 24 months of history, but detected maximum history is 11.96.
- **high — insufficient_repeated_entity_coverage:** The best detected entity-temporal candidate does not meet the configured median periods-per-entity requirement of 12.
- **high — future_target_not_defined:** Future target 'future_price_growth' has not yet been formally defined through a prediction contract.

### area_recommendation

- **Status:** candidate_ready
- **Required domains:** geography
- **Available required domains:** geography
- **Missing required domains:** None
- **Missing recommended domains:** None
- **Required history months:** None
- **Detected maximum history months:** 11.96
- **Required median periods per entity:** None

#### Gaps

- No configured gaps detected.

### forecasting

- **Status:** major_gaps
- **Required domains:** price, geography, temporal
- **Available required domains:** price, geography, temporal
- **Missing required domains:** None
- **Missing recommended domains:** None
- **Required history months:** 36
- **Detected maximum history months:** 11.96
- **Required median periods per entity:** 24

#### Gaps

- **high — insufficient_history:** Task requires approximately 36 months of history, but detected maximum history is 11.96.
- **high — insufficient_repeated_entity_coverage:** The best detected entity-temporal candidate does not meet the configured median periods-per-entity requirement of 24.
- **high — future_target_not_defined:** Future target 'future_time_series_value' has not yet been formally defined through a prediction contract.

### investment_opportunity_prediction

- **Status:** major_gaps
- **Required domains:** price, geography, temporal
- **Available required domains:** price, geography, temporal
- **Missing required domains:** None
- **Missing recommended domains:** None
- **Required history months:** 24
- **Detected maximum history months:** 11.96
- **Required median periods per entity:** 12

#### Gaps

- **high — insufficient_history:** Task requires approximately 24 months of history, but detected maximum history is 11.96.
- **high — insufficient_repeated_entity_coverage:** The best detected entity-temporal candidate does not meet the configured median periods-per-entity requirement of 12.
- **high — future_target_not_defined:** Future target 'future_investment_outcome' has not yet been formally defined through a prediction contract.

## Best Entity-Temporal Candidate

- **entity_column:** lsoa_code
- **temporal_column:** transfer_date
- **unique_entity_count:** 34984
- **entity_period_pair_count:** 159399
- **entities_with_multiple_periods:** 32704
- **repeated_entity_ratio:** 0.934827
- **minimum_periods_per_entity:** 1
- **median_periods_per_entity:** 4.0
- **maximum_periods_per_entity:** 12
- **entities_with_12_plus_periods:** 65
- **entities_with_24_plus_periods:** 0
- **entities_with_36_plus_periods:** 0
- **ratio_entities_with_12_plus_periods:** 0.001858
- **ratio_entities_with_24_plus_periods:** 0.0
- **ratio_entities_with_36_plus_periods:** 0.0
- **dataset_path:** data/processed/housing_master_dataset.csv

## Derived Analytical Target Risks

- **high — area_rank** in `data/analytics/bottom_100_areas.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — growth_score** in `data/analytics/bottom_100_areas.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — housing_intelligence_index** in `data/analytics/bottom_100_areas.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — investment_opportunity_score** in `data/analytics/bottom_100_areas.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — investment_score** in `data/analytics/bottom_100_areas.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — percentile_rank** in `data/analytics/bottom_100_areas.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — growth_score** in `data/analytics/growth_scores.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — area_rank** in `data/analytics/housing_intelligence.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — growth_score** in `data/analytics/housing_intelligence.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — housing_intelligence_index** in `data/analytics/housing_intelligence.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — investment_score** in `data/analytics/housing_intelligence.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — percentile_rank** in `data/analytics/housing_intelligence.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — area_rank** in `data/analytics/housing_map.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — growth_score** in `data/analytics/housing_map.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — housing_intelligence_index** in `data/analytics/housing_map.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — investment_score** in `data/analytics/housing_map.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — growth_score** in `data/analytics/investment_scores.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — investment_opportunity_score** in `data/analytics/investment_scores.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — investment_score** in `data/analytics/investment_scores.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — location_percentile_rank** in `data/analytics/location_intelligence.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — location_rank** in `data/analytics/location_intelligence.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — area_rank** in `data/analytics/opportunity_explorer.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — growth_score** in `data/analytics/opportunity_explorer.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — housing_intelligence_index** in `data/analytics/opportunity_explorer.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — investment_score** in `data/analytics/opportunity_explorer.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — area_rank** in `data/analytics/rankings.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — housing_intelligence_index** in `data/analytics/rankings.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — percentile_rank** in `data/analytics/rankings.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — growth_score** in `data/analytics/regional_intelligence.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — housing_intelligence_index** in `data/analytics/regional_intelligence.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — investment_score** in `data/analytics/regional_intelligence.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — regional_rank** in `data/analytics/regional_intelligence.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — area_rank** in `data/analytics/top_100_areas.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — growth_score** in `data/analytics/top_100_areas.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — housing_intelligence_index** in `data/analytics/top_100_areas.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — investment_opportunity_score** in `data/analytics/top_100_areas.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — investment_score** in `data/analytics/top_100_areas.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — percentile_rank** in `data/analytics/top_100_areas.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — deprivation_index** in `data/processed/housing_master_dataset.csv`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — deprivation_index** in `data/processed/housing_master_dataset.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — deprivation_index** in `data/processed/postcodes_clean.csv`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — deprivation_index** in `data/processed/postcodes_clean.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — deprivation_index** in `data/processed/property_geography.csv`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.
- **high — deprivation_index** in `data/processed/property_geography.parquet`: Derived analytical columns must not automatically be used as predictive labels or leakage-safe features without lineage review.

## Domain Inventory

### affordability

- `data/analytics/area_analytics_base.parquet`
- `data/analytics/bottom_100_areas.parquet`
- `data/analytics/crime_scores.parquet`
- `data/analytics/growth_scores.parquet`
- `data/analytics/housing_intelligence.parquet`
- `data/analytics/investment_scores.parquet`
- `data/analytics/rankings.parquet`
- `data/analytics/top_100_areas.parquet`
- `data/external/schools/edubasealldata20260615.csv`
- `data/reference/income/income_lookup.csv`
- `data/reference/income/regional_income_lookup.csv`

### crime

- `data/analytics/area_analytics_base.parquet`
- `data/analytics/bottom_100_areas.parquet`
- `data/analytics/crime_scores.parquet`
- `data/analytics/growth_scores.parquet`
- `data/analytics/housing_intelligence.parquet`
- `data/analytics/investment_scores.parquet`
- `data/analytics/opportunity_explorer.parquet`
- `data/analytics/regional_intelligence.parquet`
- `data/analytics/top_100_areas.parquet`
- `data/external/crime/2026-04/2026-04-avon-and-somerset-street.csv`
- `data/external/crime/2026-04/2026-04-bedfordshire-street.csv`
- `data/external/crime/2026-04/2026-04-cambridgeshire-street.csv`
- `data/external/crime/2026-04/2026-04-cheshire-street.csv`
- `data/external/crime/2026-04/2026-04-city-of-london-street.csv`
- `data/external/crime/2026-04/2026-04-cleveland-street.csv`
- `data/external/crime/2026-04/2026-04-cumbria-street.csv`
- `data/external/crime/2026-04/2026-04-derbyshire-street.csv`
- `data/external/crime/2026-04/2026-04-devon-and-cornwall-street.csv`
- `data/external/crime/2026-04/2026-04-dorset-street.csv`
- `data/external/crime/2026-04/2026-04-durham-street.csv`
- `data/external/crime/2026-04/2026-04-dyfed-powys-street.csv`
- `data/external/crime/2026-04/2026-04-essex-street.csv`
- `data/external/crime/2026-04/2026-04-hampshire-street.csv`
- `data/external/crime/2026-04/2026-04-hertfordshire-street.csv`
- `data/external/crime/2026-04/2026-04-humberside-street.csv`
- `data/external/crime/2026-04/2026-04-kent-street.csv`
- `data/external/crime/2026-04/2026-04-lancashire-street.csv`
- `data/external/crime/2026-04/2026-04-leicestershire-street.csv`
- `data/external/crime/2026-04/2026-04-lincolnshire-street.csv`
- `data/external/crime/2026-04/2026-04-merseyside-street.csv`
- `data/external/crime/2026-04/2026-04-metropolitan-street.csv`
- `data/external/crime/2026-04/2026-04-norfolk-street.csv`
- `data/external/crime/2026-04/2026-04-north-wales-street.csv`
- `data/external/crime/2026-04/2026-04-north-yorkshire-street.csv`
- `data/external/crime/2026-04/2026-04-northamptonshire-street.csv`
- `data/external/crime/2026-04/2026-04-northern-ireland-street.csv`
- `data/external/crime/2026-04/2026-04-northumbria-street.csv`
- `data/external/crime/2026-04/2026-04-nottinghamshire-street.csv`
- `data/external/crime/2026-04/2026-04-south-wales-street.csv`
- `data/external/crime/2026-04/2026-04-south-yorkshire-street.csv`
- `data/external/crime/2026-04/2026-04-staffordshire-street.csv`
- `data/external/crime/2026-04/2026-04-suffolk-street.csv`
- `data/external/crime/2026-04/2026-04-surrey-street.csv`
- `data/external/crime/2026-04/2026-04-sussex-street.csv`
- `data/external/crime/2026-04/2026-04-thames-valley-street.csv`
- `data/external/crime/2026-04/2026-04-warwickshire-street.csv`
- `data/external/crime/2026-04/2026-04-west-mercia-street.csv`
- `data/external/crime/2026-04/2026-04-west-midlands-street.csv`
- `data/external/crime/2026-04/2026-04-west-yorkshire-street.csv`
- `data/external/crime/2026-04/2026-04-wiltshire-street.csv`
- `data/processed/crime_clean.csv`
- `data/processed/crime_lsoa_summary.csv`
- `data/processed/crime_lsoa_summary.parquet`
- `data/processed/housing_master_dataset.csv`
- `data/processed/housing_master_dataset.parquet`

### deprivation

- `data/analytics/area_analytics_base.parquet`
- `data/analytics/bottom_100_areas.parquet`
- `data/analytics/crime_scores.parquet`
- `data/analytics/growth_scores.parquet`
- `data/analytics/investment_scores.parquet`
- `data/analytics/top_100_areas.parquet`
- `data/processed/housing_master_dataset.csv`
- `data/processed/housing_master_dataset.parquet`
- `data/processed/postcodes_clean.csv`
- `data/processed/postcodes_clean.parquet`
- `data/processed/property_geography.csv`
- `data/processed/property_geography.parquet`
- `data/reference/postcodes/ONS_Postcode_Directory_(February_2026)_for_the_UK_(Hosted_Table).csv`

### geography

- `data/analytics/area_analytics_base.parquet`
- `data/analytics/bottom_100_areas.parquet`
- `data/analytics/crime_scores.parquet`
- `data/analytics/growth_scores.parquet`
- `data/analytics/healthcare_intelligence.parquet`
- `data/analytics/historical_housing_trends.parquet`
- `data/analytics/housing_intelligence.parquet`
- `data/analytics/housing_map.parquet`
- `data/analytics/investment_scores.parquet`
- `data/analytics/local_authority_trends.parquet`
- `data/analytics/location_intelligence.parquet`
- `data/analytics/opportunity_explorer.parquet`
- `data/analytics/rankings.parquet`
- `data/analytics/regional_housing_trends.parquet`
- `data/analytics/regional_intelligence.parquet`
- `data/analytics/school_intelligence.parquet`
- `data/analytics/top_100_areas.parquet`
- `data/analytics/transport_intelligence.parquet`
- `data/external/crime/2026-04/2026-04-avon-and-somerset-street.csv`
- `data/external/crime/2026-04/2026-04-bedfordshire-street.csv`
- `data/external/crime/2026-04/2026-04-cambridgeshire-street.csv`
- `data/external/crime/2026-04/2026-04-cheshire-street.csv`
- `data/external/crime/2026-04/2026-04-city-of-london-street.csv`
- `data/external/crime/2026-04/2026-04-cleveland-street.csv`
- `data/external/crime/2026-04/2026-04-cumbria-street.csv`
- `data/external/crime/2026-04/2026-04-derbyshire-street.csv`
- `data/external/crime/2026-04/2026-04-devon-and-cornwall-street.csv`
- `data/external/crime/2026-04/2026-04-dorset-street.csv`
- `data/external/crime/2026-04/2026-04-durham-street.csv`
- `data/external/crime/2026-04/2026-04-dyfed-powys-street.csv`
- `data/external/crime/2026-04/2026-04-essex-street.csv`
- `data/external/crime/2026-04/2026-04-hampshire-street.csv`
- `data/external/crime/2026-04/2026-04-hertfordshire-street.csv`
- `data/external/crime/2026-04/2026-04-humberside-street.csv`
- `data/external/crime/2026-04/2026-04-kent-street.csv`
- `data/external/crime/2026-04/2026-04-lancashire-street.csv`
- `data/external/crime/2026-04/2026-04-leicestershire-street.csv`
- `data/external/crime/2026-04/2026-04-lincolnshire-street.csv`
- `data/external/crime/2026-04/2026-04-merseyside-street.csv`
- `data/external/crime/2026-04/2026-04-metropolitan-street.csv`
- `data/external/crime/2026-04/2026-04-norfolk-street.csv`
- `data/external/crime/2026-04/2026-04-north-wales-street.csv`
- `data/external/crime/2026-04/2026-04-north-yorkshire-street.csv`
- `data/external/crime/2026-04/2026-04-northamptonshire-street.csv`
- `data/external/crime/2026-04/2026-04-northern-ireland-street.csv`
- `data/external/crime/2026-04/2026-04-northumbria-street.csv`
- `data/external/crime/2026-04/2026-04-nottinghamshire-street.csv`
- `data/external/crime/2026-04/2026-04-south-wales-street.csv`
- `data/external/crime/2026-04/2026-04-south-yorkshire-street.csv`
- `data/external/crime/2026-04/2026-04-staffordshire-street.csv`
- `data/external/crime/2026-04/2026-04-suffolk-street.csv`
- `data/external/crime/2026-04/2026-04-surrey-street.csv`
- `data/external/crime/2026-04/2026-04-sussex-street.csv`
- `data/external/crime/2026-04/2026-04-thames-valley-street.csv`
- `data/external/crime/2026-04/2026-04-warwickshire-street.csv`
- `data/external/crime/2026-04/2026-04-west-mercia-street.csv`
- `data/external/crime/2026-04/2026-04-west-midlands-street.csv`
- `data/external/crime/2026-04/2026-04-west-yorkshire-street.csv`
- `data/external/crime/2026-04/2026-04-wiltshire-street.csv`
- `data/external/schools/edubasealldata20260615.csv`
- `data/external/schools/wales/maintained_schools_wg.csv`
- `data/external/transport/Stops.csv`
- `data/processed/crime_clean.csv`
- `data/processed/crime_lsoa_summary.csv`
- `data/processed/crime_lsoa_summary.parquet`
- `data/processed/housing_master_dataset.csv`
- `data/processed/housing_master_dataset.parquet`
- `data/processed/postcodes_clean.csv`
- `data/processed/postcodes_clean.parquet`
- `data/processed/property_geography.csv`
- `data/processed/property_geography.parquet`
- `data/processed/property_prices_clean.csv`
- `data/processed/property_prices_clean.parquet`
- `data/reference/geography/geography_master_lookup.csv`
- `data/reference/geography/lsoa_geography_lookup.csv`
- `data/reference/healthcare/healthcare_lookup.csv`
- `data/reference/income/regional_income_lookup.csv`
- `data/reference/postcodes/ONS_Postcode_Directory_(February_2026)_for_the_UK_(Hosted_Table).csv`
- `data/reference/schools/school_lookup.csv`

### growth

- `data/analytics/bottom_100_areas.parquet`
- `data/analytics/growth_scores.parquet`
- `data/analytics/housing_intelligence.parquet`
- `data/analytics/housing_map.parquet`
- `data/analytics/investment_scores.parquet`
- `data/analytics/local_authority_trends.parquet`
- `data/analytics/opportunity_explorer.parquet`
- `data/analytics/regional_housing_trends.parquet`
- `data/analytics/regional_intelligence.parquet`
- `data/analytics/top_100_areas.parquet`

### housing

- `data/analytics/area_analytics_base.parquet`
- `data/analytics/bottom_100_areas.parquet`
- `data/analytics/crime_scores.parquet`
- `data/analytics/growth_scores.parquet`
- `data/analytics/historical_housing_trends.parquet`
- `data/analytics/housing_intelligence.parquet`
- `data/analytics/investment_scores.parquet`
- `data/analytics/local_authority_trends.parquet`
- `data/analytics/regional_housing_trends.parquet`
- `data/analytics/top_100_areas.parquet`
- `data/processed/housing_master_dataset.csv`
- `data/processed/housing_master_dataset.parquet`
- `data/processed/property_geography.csv`
- `data/processed/property_geography.parquet`
- `data/processed/property_prices_clean.csv`
- `data/processed/property_prices_clean.parquet`

### investment

- `data/analytics/bottom_100_areas.parquet`
- `data/analytics/housing_intelligence.parquet`
- `data/analytics/housing_map.parquet`
- `data/analytics/investment_scores.parquet`
- `data/analytics/opportunity_explorer.parquet`
- `data/analytics/regional_intelligence.parquet`
- `data/analytics/top_100_areas.parquet`

### price

- `data/analytics/area_analytics_base.parquet`
- `data/analytics/bottom_100_areas.parquet`
- `data/analytics/crime_scores.parquet`
- `data/analytics/growth_scores.parquet`
- `data/analytics/historical_housing_trends.parquet`
- `data/analytics/housing_intelligence.parquet`
- `data/analytics/investment_scores.parquet`
- `data/analytics/local_authority_trends.parquet`
- `data/analytics/opportunity_explorer.parquet`
- `data/analytics/regional_housing_trends.parquet`
- `data/analytics/regional_intelligence.parquet`
- `data/analytics/top_100_areas.parquet`
- `data/processed/housing_master_dataset.csv`
- `data/processed/housing_master_dataset.parquet`
- `data/processed/property_geography.csv`
- `data/processed/property_geography.parquet`
- `data/processed/property_prices_clean.csv`
- `data/processed/property_prices_clean.parquet`

### temporal

- `data/analytics/historical_housing_trends.parquet`
- `data/analytics/local_authority_trends.parquet`
- `data/analytics/regional_housing_trends.parquet`
- `data/external/crime/2026-04/2026-04-avon-and-somerset-street.csv`
- `data/external/crime/2026-04/2026-04-bedfordshire-street.csv`
- `data/external/crime/2026-04/2026-04-cambridgeshire-street.csv`
- `data/external/crime/2026-04/2026-04-cheshire-street.csv`
- `data/external/crime/2026-04/2026-04-city-of-london-street.csv`
- `data/external/crime/2026-04/2026-04-cleveland-street.csv`
- `data/external/crime/2026-04/2026-04-cumbria-street.csv`
- `data/external/crime/2026-04/2026-04-derbyshire-street.csv`
- `data/external/crime/2026-04/2026-04-devon-and-cornwall-street.csv`
- `data/external/crime/2026-04/2026-04-dorset-street.csv`
- `data/external/crime/2026-04/2026-04-durham-street.csv`
- `data/external/crime/2026-04/2026-04-dyfed-powys-street.csv`
- `data/external/crime/2026-04/2026-04-essex-street.csv`
- `data/external/crime/2026-04/2026-04-hampshire-street.csv`
- `data/external/crime/2026-04/2026-04-hertfordshire-street.csv`
- `data/external/crime/2026-04/2026-04-humberside-street.csv`
- `data/external/crime/2026-04/2026-04-kent-street.csv`
- `data/external/crime/2026-04/2026-04-lancashire-street.csv`
- `data/external/crime/2026-04/2026-04-leicestershire-street.csv`
- `data/external/crime/2026-04/2026-04-lincolnshire-street.csv`
- `data/external/crime/2026-04/2026-04-merseyside-street.csv`
- `data/external/crime/2026-04/2026-04-metropolitan-street.csv`
- `data/external/crime/2026-04/2026-04-norfolk-street.csv`
- `data/external/crime/2026-04/2026-04-north-wales-street.csv`
- `data/external/crime/2026-04/2026-04-north-yorkshire-street.csv`
- `data/external/crime/2026-04/2026-04-northamptonshire-street.csv`
- `data/external/crime/2026-04/2026-04-northern-ireland-street.csv`
- `data/external/crime/2026-04/2026-04-northumbria-street.csv`
- `data/external/crime/2026-04/2026-04-nottinghamshire-street.csv`
- `data/external/crime/2026-04/2026-04-south-wales-street.csv`
- `data/external/crime/2026-04/2026-04-south-yorkshire-street.csv`
- `data/external/crime/2026-04/2026-04-staffordshire-street.csv`
- `data/external/crime/2026-04/2026-04-suffolk-street.csv`
- `data/external/crime/2026-04/2026-04-surrey-street.csv`
- `data/external/crime/2026-04/2026-04-sussex-street.csv`
- `data/external/crime/2026-04/2026-04-thames-valley-street.csv`
- `data/external/crime/2026-04/2026-04-warwickshire-street.csv`
- `data/external/crime/2026-04/2026-04-west-mercia-street.csv`
- `data/external/crime/2026-04/2026-04-west-midlands-street.csv`
- `data/external/crime/2026-04/2026-04-west-yorkshire-street.csv`
- `data/external/crime/2026-04/2026-04-wiltshire-street.csv`
- `data/external/schools/edubasealldata20260615.csv`
- `data/external/transport/Stops.csv`
- `data/processed/crime_clean.csv`
- `data/processed/housing_master_dataset.csv`
- `data/processed/housing_master_dataset.parquet`
- `data/processed/property_geography.csv`
- `data/processed/property_geography.parquet`
- `data/processed/property_prices_clean.csv`
- `data/processed/property_prices_clean.parquet`

## Dataset-Level Assessment

| Dataset | Profile Mode | Rows Profiled | Temporal Columns | Primary Geography | Price Columns | Domains | Status |
|---|---|---:|---|---|---|---|---|
| data/analytics/area_analytics_base.parquet | full | 35671 | None | lsoa_code | average_price, median_price, price_to_income_ratio | affordability, crime, deprivation, geography, housing, price | success |
| data/analytics/bottom_100_areas.parquet | full | 100 | None | lsoa_code | average_price, average_price_to_crime_ratio, median_price, price_to_income_ratio | affordability, crime, deprivation, geography, growth, housing, investment, price | success |
| data/analytics/crime_scores.parquet | full | 35671 | None | lsoa_code | average_price, median_price, price_to_income_ratio | affordability, crime, deprivation, geography, housing, price | success |
| data/analytics/growth_scores.parquet | full | 35671 | None | lsoa_code | average_price, median_price, price_to_income_ratio | affordability, crime, deprivation, geography, growth, housing, price | success |
| data/analytics/healthcare_intelligence.parquet | full | 35671 | None | lsoa_code | None | geography | success |
| data/analytics/historical_housing_trends.parquet | head_sample | 250000 | month, year | lsoa_code | average_price, median_price | geography, housing, price, temporal | success |
| data/analytics/housing_intelligence.parquet | full | 35671 | warehouse_loaded_at | lsoa_code | average_price, median_price, price_to_income_ratio | affordability, crime, geography, growth, housing, investment, price | success |
| data/analytics/housing_map.parquet | full | 35671 | None | lsoa_code | None | geography, growth, investment | success |
| data/analytics/investment_scores.parquet | full | 35671 | None | lsoa_code | average_price, average_price_to_crime_ratio, median_price, price_to_income_ratio | affordability, crime, deprivation, geography, growth, housing, investment, price | success |
| data/analytics/local_authority_trends.parquet | full | 12711 | month, year | local_authority | average_price, median_price, mom_price_growth_pct, rolling_12m_average_price, yoy_price_growth_pct | geography, growth, housing, price, temporal | success |
| data/analytics/location_intelligence.parquet | full | 35671 | None | lsoa_code | None | geography | success |
| data/analytics/opportunity_explorer.parquet | full | 35671 | None | lsoa_code | average_price | crime, geography, growth, investment, price | success |
| data/analytics/rankings.parquet | full | 35671 | None | lsoa_code | None | affordability, geography | success |
| data/analytics/regional_housing_trends.parquet | full | 400 | month, year | region | average_price, median_price, mom_price_growth_pct, rolling_12m_average_price, yoy_price_growth_pct | geography, growth, housing, price, temporal | success |
| data/analytics/regional_intelligence.parquet | full | 10 | None | region | average_price | crime, geography, growth, investment, price | success |
| data/analytics/school_intelligence.parquet | full | 35671 | None | lsoa_code | None | geography | success |
| data/analytics/top_100_areas.parquet | full | 100 | None | lsoa_code | average_price, average_price_to_crime_ratio, median_price, price_to_income_ratio | affordability, crime, deprivation, geography, growth, housing, investment, price | success |
| data/analytics/transport_intelligence.parquet | full | 35671 | None | lsoa_code | None | geography | success |
| data/external/crime/2026-04/2026-04-avon-and-somerset-street.csv | full | 16657 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-bedfordshire-street.csv | full | 5171 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-cambridgeshire-street.csv | full | 7047 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-cheshire-street.csv | full | 6939 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-city-of-london-street.csv | full | 736 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-cleveland-street.csv | full | 7712 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-cumbria-street.csv | full | 3320 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-derbyshire-street.csv | full | 8993 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-devon-and-cornwall-street.csv | full | 12193 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-dorset-street.csv | full | 4696 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-durham-street.csv | full | 6839 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-dyfed-powys-street.csv | full | 3775 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-essex-street.csv | full | 14073 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-hampshire-street.csv | full | 13653 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-hertfordshire-street.csv | full | 9070 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-humberside-street.csv | full | 8528 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-kent-street.csv | full | 14704 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-lancashire-street.csv | full | 13737 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-leicestershire-street.csv | full | 8332 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-lincolnshire-street.csv | full | 6141 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-merseyside-street.csv | full | 12146 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-metropolitan-street.csv | full | 91664 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-norfolk-street.csv | full | 5554 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-north-wales-street.csv | full | 5594 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-north-yorkshire-street.csv | full | 5140 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-northamptonshire-street.csv | full | 6145 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-northern-ireland-street.csv | full | 11508 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-northumbria-street.csv | full | 12745 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-nottinghamshire-street.csv | full | 11165 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-south-wales-street.csv | full | 10502 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-south-yorkshire-street.csv | full | 14700 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-staffordshire-street.csv | full | 9150 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-suffolk-street.csv | full | 4083 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-surrey-street.csv | full | 7481 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-sussex-street.csv | full | 14411 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-thames-valley-street.csv | full | 16377 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-warwickshire-street.csv | full | 4325 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-west-mercia-street.csv | full | 8456 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-west-midlands-street.csv | full | 26616 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-west-yorkshire-street.csv | full | 24265 | Month | None | None | crime, geography, temporal | success |
| data/external/crime/2026-04/2026-04-wiltshire-street.csv | full | 4522 | Month | None | None | crime, geography, temporal | success |
| data/external/healthcare/etr.csv | full | 273 | None | None | None | None | success |
| data/external/healthcare/ets.csv | full | 45731 | None | None | None | None | success |
| data/external/healthcare/wlhb.csv | full | 6 | None | None | None | None | success |
| data/external/healthcare/wlhbsite.csv | full | 918 | None | None | None | None | success |
| data/external/schools/edubasealldata20260615.csv | full | 52397 | AccreditationExpiryDate, CensusDate, CloseDate, DateOfLastInspectionVisit | Postcode | None | affordability, geography, temporal | success |
| data/external/schools/wales/maintained_schools_wg.csv | full | 1440 | None | postcode | None | geography | success |
| data/external/transport/Stops.csv | head_sample | 250000 | None | None | None | geography, temporal | success |
| data/processed/crime_clean.csv | head_sample | 250000 | crime_month, crime_year, month | lsoa_code | None | crime, geography, temporal | success |
| data/processed/crime_lsoa_summary.csv | full | 32789 | None | lsoa_code | None | crime, geography | success |
| data/processed/crime_lsoa_summary.parquet | full | 32789 | None | lsoa_code | None | crime, geography | success |
| data/processed/housing_master_dataset.csv | head_sample | 250000 | transfer_date, transfer_month, transfer_year | lsoa_code | price, price_to_crime_ratio | crime, deprivation, geography, housing, price, temporal | success |
| data/processed/housing_master_dataset.parquet | head_sample | 250000 | transfer_date, transfer_month, transfer_year | lsoa_code | price, price_to_crime_ratio | crime, deprivation, geography, housing, price, temporal | success |
| data/processed/postcodes_clean.csv | head_sample | 250000 | None | lsoa_code | None | deprivation, geography | success |
| data/processed/postcodes_clean.parquet | head_sample | 250000 | None | lsoa_code | None | deprivation, geography | success |
| data/processed/property_geography.csv | head_sample | 250000 | transfer_date, transfer_month, transfer_year | lsoa_code | price | deprivation, geography, housing, price, temporal | success |
| data/processed/property_geography.parquet | head_sample | 250000 | transfer_date, transfer_month, transfer_year | lsoa_code | price | deprivation, geography, housing, price, temporal | success |
| data/processed/property_prices_clean.csv | head_sample | 250000 | transfer_date, transfer_month, transfer_year | postcode | price | geography, housing, price, temporal | success |
| data/processed/property_prices_clean.parquet | head_sample | 250000 | transfer_date, transfer_month, transfer_year | postcode | price | geography, housing, price, temporal | success |
| data/raw/land_registry/pp-2023.csv | head_sample | 250000 | None | None | None | None | success |
| data/raw/land_registry/pp-2024.csv | head_sample | 250000 | None | None | None | None | success |
| data/raw/land_registry/pp-2025.csv | head_sample | 250000 | None | None | None | None | success |
| data/raw/land_registry/pp-2026.csv | full | 149256 | None | None | None | None | success |
| data/reference/geography/country_lookup.csv | full | 7 | None | None | None | None | success |
| data/reference/geography/geography_master_lookup.csv | full | 43916 | None | lsoa_code | None | geography | success |
| data/reference/geography/local_authority_lookup.csv | full | 361 | None | None | None | None | success |
| data/reference/geography/lsoa_geography_lookup.csv | full | 43916 | None | lsoa_code | None | geography | success |
| data/reference/geography/region_lookup.csv | full | 9 | None | None | None | None | success |
| data/reference/healthcare/healthcare_lookup.csv | full | 46649 | None | lsoa_code | None | geography | success |
| data/reference/income/income_lookup.csv | full | 356 | None | None | None | affordability | success |
| data/reference/income/regional_income_lookup.csv | full | 10 | None | region | None | affordability, geography | success |
| data/reference/postcodes/ONS_Postcode_Directory_(February_2026)_for_the_UK_(Hosted_Table).csv | head_sample | 250000 | None | None | None | deprivation, geography | success |
| data/reference/schools/school_lookup.csv | full | 28153 | None | lsoa_code | None | geography | success |

## Architectural Interpretation

This assessment measures structural predictive feasibility. It does not authorize model training.

A future prediction task still requires a formal prediction contract, target engineering policy, point-in-time feature policy, temporal split policy, and leakage validation.

