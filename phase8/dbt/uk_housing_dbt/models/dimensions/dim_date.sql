WITH dates AS (

    SELECT DISTINCT

        "year"  AS year,
        "month" AS month

    FROM {{ ref('stg_historical_housing_trends') }}

)

SELECT

    ROW_NUMBER() OVER (
        ORDER BY year, month
    ) AS date_key,

    year,

    month,

    CONCAT(
        year,
        '-',
        LPAD(month::VARCHAR, 2, '0')
    ) AS year_month

FROM dates