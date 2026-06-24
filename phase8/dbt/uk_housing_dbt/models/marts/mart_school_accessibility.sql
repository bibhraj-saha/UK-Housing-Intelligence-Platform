{{ config(materialized='table') }}

SELECT

    dl.location_key,
    dla.local_authority_key,
    dr.region_key,

    s.lsoa_code,

    s.school_count,
    s.total_pupils,
    s.primary_school_count,
    s.secondary_school_count,
    s.average_pupils_per_school,
    s.school_accessibility_score

FROM {{ ref('stg_school_intelligence') }} s

LEFT JOIN {{ ref('dim_location') }} dl
    ON s.lsoa_code = dl.lsoa_code

LEFT JOIN {{ ref('dim_local_authority') }} dla
    ON dl.local_authority = dla.local_authority

LEFT JOIN {{ ref('dim_region') }} dr
    ON dl.region = dr.region