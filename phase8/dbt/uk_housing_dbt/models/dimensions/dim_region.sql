SELECT
    ROW_NUMBER() OVER (
        ORDER BY region
    ) AS region_key,

    region

FROM (

    SELECT DISTINCT
        "region" AS region

    FROM {{ ref('stg_housing_intelligence') }}

)