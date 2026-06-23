{{ config(
    materialized='view'
) }}

SELECT *

FROM {{ source('raw', 'growth_scores') }}