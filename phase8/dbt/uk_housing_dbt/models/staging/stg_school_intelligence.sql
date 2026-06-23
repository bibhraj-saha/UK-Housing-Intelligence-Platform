{{ config(
    materialized='view'
) }}

SELECT *

FROM {{ source('raw', 'school_intelligence') }}