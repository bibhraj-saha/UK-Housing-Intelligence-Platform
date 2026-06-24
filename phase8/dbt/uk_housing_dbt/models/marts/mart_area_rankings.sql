SELECT

    dl.location_key,

    dla.local_authority_key,

    dr.region_key,

    dc.country_key,

    fhi.housing_intelligence_index,

    fhi.area_rank,

    fhi.percentile_rank,

    fhi.average_price,

    fhi.average_crime,

    fhi.affordability_score,

    fhi.growth_score,

    fhi.investment_score

FROM {{ ref('fct_housing_intelligence') }} fhi

LEFT JOIN {{ ref('dim_location') }} dl
    ON fhi.location_key = dl.location_key

LEFT JOIN {{ ref('dim_local_authority') }} dla
    ON fhi.local_authority_key = dla.local_authority_key

LEFT JOIN {{ ref('dim_region') }} dr
    ON fhi.region_key = dr.region_key

LEFT JOIN {{ ref('dim_country') }} dc
    ON dl.country = dc.country