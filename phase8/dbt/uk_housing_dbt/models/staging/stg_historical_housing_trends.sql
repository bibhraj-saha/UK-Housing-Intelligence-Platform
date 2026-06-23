{{ config(
    materialized='view'
) }}

SELECT *

FROM {{ source('raw', 'historical_housing_trends') }}