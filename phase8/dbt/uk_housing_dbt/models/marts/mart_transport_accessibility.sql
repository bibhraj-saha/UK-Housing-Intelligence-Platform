{{ config(materialized='table') }}

SELECT

    dl.location_key,
    dla.local_authority_key,
    dr.region_key,

    t.lsoa_code,

    t.transport_stop_count,
    t.bus_stop_count,
    t.rail_station_count,
    t.metro_station_count,
    t.airport_count,
    t.ferry_terminal_count,
    t.transport_accessibility_score

FROM {{ ref('stg_transport_intelligence') }} t

LEFT JOIN {{ ref('dim_location') }} dl
    ON t.lsoa_code = dl.lsoa_code

LEFT JOIN {{ ref('dim_local_authority') }} dla
    ON dl.local_authority = dla.local_authority

LEFT JOIN {{ ref('dim_region') }} dr
    ON dl.region = dr.region