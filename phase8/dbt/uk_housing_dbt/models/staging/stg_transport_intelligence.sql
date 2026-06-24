{{ config(
    materialized='view'
) }}

SELECT

    "lsoa_code"                  AS lsoa_code,
    "transport_stop_count"       AS transport_stop_count,
    "bus_stop_count"             AS bus_stop_count,
    "rail_station_count"         AS rail_station_count,
    "metro_station_count"        AS metro_station_count,
    "airport_count"              AS airport_count,
    "ferry_terminal_count"       AS ferry_terminal_count,
    "transport_accessibility_score" AS transport_accessibility_score

FROM {{ source('raw', 'transport_intelligence') }}