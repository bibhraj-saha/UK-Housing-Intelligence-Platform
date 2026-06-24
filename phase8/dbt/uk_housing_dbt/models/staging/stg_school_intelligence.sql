{{ config(
    materialized='view'
) }}

SELECT

    "lsoa_code"                    AS lsoa_code,
    "school_count"                 AS school_count,
    "total_pupils"                 AS total_pupils,
    "primary_school_count"         AS primary_school_count,
    "secondary_school_count"       AS secondary_school_count,
    "average_pupils_per_school"    AS average_pupils_per_school,
    "school_accessibility_score"   AS school_accessibility_score

FROM {{ source('raw', 'school_intelligence') }}