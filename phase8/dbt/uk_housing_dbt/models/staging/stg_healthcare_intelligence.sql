{{ config(
    materialized='view'
) }}

SELECT

    "lsoa_code"                   AS lsoa_code,
    "healthcare_site_count"       AS healthcare_site_count,
    "healthcare_accessibility_score" AS healthcare_accessibility_score

FROM {{ source('raw', 'healthcare_intelligence') }}