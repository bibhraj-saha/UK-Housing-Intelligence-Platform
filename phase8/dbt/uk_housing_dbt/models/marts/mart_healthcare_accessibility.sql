{{ config(materialized='table') }}

SELECT

    dl.location_key,
    dla.local_authority_key,
    dr.region_key,

    h.lsoa_code,

    h.healthcare_site_count,
    h.healthcare_accessibility_score

FROM {{ ref('stg_healthcare_intelligence') }} h

LEFT JOIN {{ ref('dim_location') }} dl
    ON h.lsoa_code = dl.lsoa_code

LEFT JOIN {{ ref('dim_local_authority') }} dla
    ON dl.local_authority = dla.local_authority

LEFT JOIN {{ ref('dim_region') }} dr
    ON dl.region = dr.region