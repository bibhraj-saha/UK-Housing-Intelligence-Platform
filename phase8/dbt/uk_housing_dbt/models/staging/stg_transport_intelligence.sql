{{ config(
    materialized='view'
) }}

SELECT *

FROM {{ source('raw', 'transport_intelligence') }}