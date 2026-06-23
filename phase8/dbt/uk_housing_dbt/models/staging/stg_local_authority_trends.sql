{{ config(
    materialized='view'
) }}

SELECT *

FROM {{ source('raw', 'local_authority_trends') }}