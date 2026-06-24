SELECT

    dl.location_key,

    dla.local_authority_key,

    dr.region_key,

    shi."average_price"                    AS average_price,
    shi."median_price"                     AS median_price,
    shi."transaction_count"                AS transaction_count,

    shi."average_crime"                    AS average_crime,
    shi."crime_score"                      AS crime_score,

    shi."affordability_score"              AS affordability_score,

    shi."growth_score"                     AS growth_score,

    shi."investment_score"                 AS investment_score,

    shi."housing_intelligence_index"       AS housing_intelligence_index,

    shi."area_rank"                        AS area_rank,
    shi."percentile_rank"                  AS percentile_rank

FROM {{ ref('stg_housing_intelligence') }} shi

LEFT JOIN {{ ref('dim_location') }} dl
    ON shi."lsoa_code" = dl.lsoa_code

LEFT JOIN {{ ref('dim_local_authority') }} dla
    ON shi."lad_code" = dla.lad_code

LEFT JOIN {{ ref('dim_region') }} dr
    ON shi."region" = dr.region