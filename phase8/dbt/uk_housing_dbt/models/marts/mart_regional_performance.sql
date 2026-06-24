SELECT

    dr.region_key,

    dc.country_key,

    frt.average_price,

    frt.mom_price_growth_pct,

    frt.yoy_price_growth_pct,

    frt.rolling_12m_average_price,

    frt.date_key

FROM {{ ref('fct_regional_trends') }} frt

LEFT JOIN {{ ref('dim_region') }} dr
    ON frt.region_key = dr.region_key

LEFT JOIN {{ ref('dim_country') }} dc
    ON frt.country_key = dc.country_key