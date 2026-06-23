{{ config(
    materialized='view'
) }}

SELECT *

FROM {{ source('raw', 'location_intelligence') }}