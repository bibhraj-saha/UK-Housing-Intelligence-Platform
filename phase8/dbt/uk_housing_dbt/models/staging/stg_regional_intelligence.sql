{{ config(
    materialized='view'
) }}

SELECT *

FROM {{ source('raw', 'regional_intelligence') }}