{{ config(
    materialized='table'
) }}

WITH housing AS (

    SELECT *
    FROM {{ ref('fct_housing_intelligence') }}

),

schools AS (

    SELECT
        location_key,
        school_count,
        total_pupils,
        primary_school_count,
        secondary_school_count,
        average_pupils_per_school,
        school_accessibility_score

    FROM {{ ref('mart_school_accessibility') }}

),

healthcare AS (

    SELECT
        location_key,
        healthcare_site_count,
        healthcare_accessibility_score

    FROM {{ ref('mart_healthcare_accessibility') }}

),

transport AS (

    SELECT
        location_key,
        transport_stop_count,
        bus_stop_count,
        rail_station_count,
        metro_station_count,
        airport_count,
        ferry_terminal_count,
        transport_accessibility_score

    FROM {{ ref('mart_transport_accessibility') }}

)

SELECT

    h.location_key,
    h.local_authority_key,
    h.region_key,

    dl.lsoa_code,
    dl.local_authority,
    dl.region,
    dl.country,

    dl.latitude,
    dl.longitude,

    dl.estimated_annual_income,
    dl.price_to_income_ratio,
    dl.income_affordability_score,

    h.average_price,
    h.median_price,
    h.transaction_count,

    h.crime_score,
    h.affordability_score,
    h.growth_score,
    h.investment_score,

    h.housing_intelligence_index,
    h.area_rank,
    h.percentile_rank,

    s.school_count,
    s.total_pupils,
    s.primary_school_count,
    s.secondary_school_count,
    s.average_pupils_per_school,
    s.school_accessibility_score,

    hc.healthcare_site_count,
    hc.healthcare_accessibility_score,

    t.transport_stop_count,
    t.bus_stop_count,
    t.rail_station_count,
    t.metro_station_count,
    t.airport_count,
    t.ferry_terminal_count,
    t.transport_accessibility_score,

    CURRENT_TIMESTAMP() AS warehouse_loaded_at

FROM housing h

LEFT JOIN {{ ref('dim_location') }} dl
    ON h.location_key = dl.location_key

LEFT JOIN schools s
    ON h.location_key = s.location_key

LEFT JOIN healthcare hc
    ON h.location_key = hc.location_key

LEFT JOIN transport t
    ON h.location_key = t.location_key