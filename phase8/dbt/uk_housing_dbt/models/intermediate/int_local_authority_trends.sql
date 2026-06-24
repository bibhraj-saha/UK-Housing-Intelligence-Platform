SELECT

    "local_authority",
    "region",
    "country",

    "year",
    "month",

    "average_price",
    "median_price",
    "transaction_count",

    "mom_price_growth_pct",
    "yoy_price_growth_pct",

    "rolling_12m_average_price"

FROM {{ ref('stg_local_authority_trends') }}