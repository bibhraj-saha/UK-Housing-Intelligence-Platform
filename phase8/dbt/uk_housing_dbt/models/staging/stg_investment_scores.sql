{{ config(
    materialized='view'
) }}

SELECT *

FROM {{ source('raw', 'investment_scores') }}