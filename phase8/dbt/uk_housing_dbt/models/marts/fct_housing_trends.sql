SELECT

    dl.location_key,

    dla.local_authority_key,

    dr.region_key,

    dc.country_key,

    dd.date_key,

    sht."average_price"       AS average_price,

    sht."median_price"        AS median_price,

    sht."transaction_count"   AS transaction_count

FROM {{ ref('int_housing_trends') }} sht

LEFT JOIN {{ ref('dim_location') }} dl
    ON sht."lsoa_code" = dl.lsoa_code

LEFT JOIN {{ ref('dim_local_authority') }} dla
    ON sht."local_authority" = dla.local_authority

LEFT JOIN {{ ref('dim_region') }} dr
    ON sht."region" = dr.region

LEFT JOIN {{ ref('dim_country') }} dc
    ON sht."country" = dc.country

LEFT JOIN {{ ref('dim_date') }} dd
    ON sht."year" = dd.year
   AND sht."month" = dd.month