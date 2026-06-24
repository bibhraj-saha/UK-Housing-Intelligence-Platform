SELECT

    "lsoa_code",

    "year",
    "month",

    "average_price",
    "median_price",
    "transaction_count",

    "local_authority",
    "region",
    "country",

    "latitude",
    "longitude"

FROM {{ ref('stg_historical_housing_trends') }}