SELECT
    ROW_NUMBER() OVER (
        ORDER BY lad_code
    ) AS local_authority_key,

    lad_code,
    local_authority

FROM (

    SELECT DISTINCT
        "lad_code" AS lad_code,
        "local_authority" AS local_authority

    FROM {{ ref('stg_housing_intelligence') }}

)