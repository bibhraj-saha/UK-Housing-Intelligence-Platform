SELECT

    dla.local_authority_key,

    dr.region_key,

    dc.country_key,

    dd.date_key,

    slat."average_price"              AS average_price,

    slat."median_price"               AS median_price,

    slat."transaction_count"          AS transaction_count,

    slat."mom_price_growth_pct"       AS mom_price_growth_pct,

    slat."yoy_price_growth_pct"       AS yoy_price_growth_pct,

    slat."rolling_12m_average_price"  AS rolling_12m_average_price

FROM {{ ref('stg_local_authority_trends') }} slat

LEFT JOIN {{ ref('dim_local_authority') }} dla
    ON slat."local_authority" = dla.local_authority

LEFT JOIN {{ ref('dim_region') }} dr
    ON slat."region" = dr.region

LEFT JOIN {{ ref('dim_country') }} dc
    ON slat."country" = dc.country

LEFT JOIN {{ ref('dim_date') }} dd
    ON slat."year" = dd.year
   AND slat."month" = dd.month