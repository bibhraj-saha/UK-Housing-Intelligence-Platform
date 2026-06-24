SELECT

    dr.region_key,

    dc.country_key,

    dd.date_key,

    srt."average_price"              AS average_price,

    srt."median_price"               AS median_price,

    srt."transaction_count"          AS transaction_count,

    srt."mom_price_growth_pct"       AS mom_price_growth_pct,

    srt."yoy_price_growth_pct"       AS yoy_price_growth_pct,

    srt."rolling_12m_average_price"  AS rolling_12m_average_price

FROM {{ ref('stg_regional_housing_trends') }} srt

LEFT JOIN {{ ref('dim_region') }} dr
    ON srt."region" = dr.region

LEFT JOIN {{ ref('dim_country') }} dc
    ON srt."country" = dc.country

LEFT JOIN {{ ref('dim_date') }} dd
    ON srt."year" = dd.year
   AND srt."month" = dd.month