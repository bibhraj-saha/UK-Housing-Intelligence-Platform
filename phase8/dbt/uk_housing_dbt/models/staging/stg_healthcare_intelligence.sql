{{ config(
    materialized='view'
) }}

SELECT *

FROM {{ source('raw', 'healthcare_intelligence') }}