import pandas as pd
import numpy as np
from scipy.spatial import cKDTree

RADIUS_KM = 2

print("Loading transport dataset...")

transport = pd.read_csv(
    "data/external/transport/Stops.csv",
    low_memory=False,
    usecols=[
        "Latitude",
        "Longitude",
        "StopType",
        "Status"
    ]
)

transport = transport[
    (transport["Status"] == "active")
    &
    (transport["Latitude"].notna())
    &
    (transport["Longitude"].notna())
]

print("Transport Shape:")
print(transport.shape)

transport = transport[
    [
        "Latitude",
        "Longitude",
        "StopType"
    ]
].copy()

print("\nLoading LSOA geography...")

lsoa = pd.read_csv(
    "data/reference/geography/lsoa_geography_lookup.csv",
    usecols=[
        "lsoa_code",
        "latitude",
        "longitude"
    ]
)

housing = pd.read_parquet(
    "data/analytics/housing_intelligence.parquet",
    columns=["lsoa_code"]
)

housing_lsoas = (
    housing[["lsoa_code"]]
    .drop_duplicates()
)

lsoa = lsoa.merge(
    housing_lsoas,
    on="lsoa_code",
    how="inner"
)

print("LSOA Shape:")
print(lsoa.shape)

print("\nBuilding spatial index...")

transport_coords = np.radians(
    transport[
        [
            "Latitude",
            "Longitude"
        ]
    ].values
)

tree = cKDTree(transport_coords)

lsoa_coords = np.radians(
    lsoa[
        [
            "latitude",
            "longitude"
        ]
    ].values
)

earth_radius_km = 6371

radius_radians = (
    RADIUS_KM
    /
    earth_radius_km
)

print(
    f"Finding transport assets within "
    f"{RADIUS_KM} km..."
)

matches = tree.query_ball_point(
    lsoa_coords,
    r=radius_radians
)

results = []

for idx, stop_indexes in enumerate(matches):

    nearby = transport.iloc[stop_indexes]

    bus_count = nearby[
        nearby["StopType"].isin(
            [
                "BCT",
                "BCS"
            ]
        )
    ].shape[0]

    rail_count = nearby[
        nearby["StopType"].isin(
            [
                "RLY",
                "RSE"
            ]
        )
    ].shape[0]

    metro_count = nearby[
        nearby["StopType"] == "MET"
    ].shape[0]

    airport_count = nearby[
        nearby["StopType"] == "AIR"
    ].shape[0]

    ferry_count = nearby[
        nearby["StopType"] == "FER"
    ].shape[0]

    total_count = len(nearby)

    results.append(
        [
            lsoa.iloc[idx]["lsoa_code"],
            total_count,
            bus_count,
            rail_count,
            metro_count,
            airport_count,
            ferry_count
        ]
    )

transport_intelligence = pd.DataFrame(
    results,
    columns=[
        "lsoa_code",
        "transport_stop_count",
        "bus_stop_count",
        "rail_station_count",
        "metro_station_count",
        "airport_count",
        "ferry_terminal_count"
    ]
)

max_transport = (
    transport_intelligence[
        "transport_stop_count"
    ]
    .max()
)

transport_intelligence[
    "transport_accessibility_score"
] = (
    transport_intelligence[
        "transport_stop_count"
    ]
    /
    max_transport
    * 100
)

output_file = (
    "data/analytics/"
    "transport_intelligence.parquet"
)

transport_intelligence.to_parquet(
    output_file,
    index=False
)

print("\nTransport Intelligence Created")

print("\nShape:")
print(transport_intelligence.shape)

print("\nColumns:")
print(
    transport_intelligence.columns.tolist()
)

print("\nSample:")
print(
    transport_intelligence.head()
)