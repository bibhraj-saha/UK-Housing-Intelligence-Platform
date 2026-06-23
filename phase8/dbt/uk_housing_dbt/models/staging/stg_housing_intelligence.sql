{{ config(
    materialized='view'
) }}

SELECT *

FROM {{ source('raw', 'housing_intelligence') }}