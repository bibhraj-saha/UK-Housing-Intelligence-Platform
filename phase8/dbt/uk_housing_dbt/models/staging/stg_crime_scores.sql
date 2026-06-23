{{ config(
    materialized='view'
) }}

SELECT *

FROM {{ source('raw', 'crime_scores') }}