WITH countries AS (

    SELECT DISTINCT
        "country" AS country

    FROM {{ ref('stg_housing_intelligence') }}

    WHERE "country" IS NOT NULL

)

SELECT

    ROW_NUMBER() OVER (
        ORDER BY country
    ) AS country_key,

    country

FROM countries