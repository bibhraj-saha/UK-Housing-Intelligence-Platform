{{ config(
    materialized='view'
) }}

SELECT *

FROM {{ source('raw', 'opportunity_explorer') }}