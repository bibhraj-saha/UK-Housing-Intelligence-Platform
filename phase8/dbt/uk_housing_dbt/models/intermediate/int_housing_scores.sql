SELECT

    "lsoa_code",

    "average_price",
    "median_price",
    "transaction_count",

    "average_crime",
    "crime_score",

    "affordability_score",

    "growth_score",

    "investment_score",

    "housing_intelligence_index",

    "area_rank",
    "percentile_rank",

    "local_authority",
    "region",
    "country",

    "latitude",
    "longitude",

    "lad_code",

    "median_weekly_income",
    "mean_weekly_income",

    "estimated_annual_income",

    "price_to_income_ratio",

    "income_affordability_score"

FROM {{ ref('stg_housing_intelligence') }}