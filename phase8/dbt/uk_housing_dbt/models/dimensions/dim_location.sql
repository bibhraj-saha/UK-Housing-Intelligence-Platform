{{ config(
    materialized='table'
) }}

SELECT

    ROW_NUMBER() OVER (
        ORDER BY "lsoa_code"
    ) AS location_key,

    "lsoa_code" AS lsoa_code,

    "local_authority" AS local_authority,

    "region" AS region,

    "country" AS country,

    "latitude" AS latitude,

    "longitude" AS longitude,

    "estimated_annual_income" AS estimated_annual_income,

    "price_to_income_ratio" AS price_to_income_ratio,

    "income_affordability_score" AS income_affordability_score

FROM {{ ref('stg_housing_intelligence') }}