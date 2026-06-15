import pandas as pd

print("Loading School Intelligence...")

schools = pd.read_parquet(
    "data/analytics/school_intelligence.parquet"
)

print(schools.shape)

print("\nLoading Healthcare Intelligence...")

healthcare = pd.read_parquet(
    "data/analytics/healthcare_intelligence.parquet"
)

print(healthcare.shape)

print("\nLoading Transport Intelligence...")

transport = pd.read_parquet(
    "data/analytics/transport_intelligence.parquet"
)

print(transport.shape)

print("\nMerging datasets...")

location = (
    schools
    .merge(
        healthcare,
        on="lsoa_code",
        how="left"
    )
    .merge(
        transport,
        on="lsoa_code",
        how="left"
    )
)

numeric_cols = [
    col
    for col in location.columns
    if col != "lsoa_code"
]

for col in numeric_cols:
    location[col] = (
        location[col]
        .fillna(0)
    )

print("\nCreating percentile scores...")

location["school_percentile_score"] = (
    location["school_count"]
    .rank(pct=True)
    * 100
)

location["healthcare_percentile_score"] = (
    location["healthcare_site_count"]
    .rank(pct=True)
    * 100
)

location["transport_percentile_score"] = (
    location["transport_stop_count"]
    .rank(pct=True)
    * 100
)

location["location_intelligence_score"] = (
    (
        location["school_percentile_score"]
        +
        location["healthcare_percentile_score"]
        +
        location["transport_percentile_score"]
    )
    / 3
)

location = location.sort_values(
    "location_intelligence_score",
    ascending=False
).reset_index(drop=True)

location["location_rank"] = (
    location.index + 1
)

location["location_percentile_rank"] = (
    location["location_intelligence_score"]
    .rank(
        pct=True
    )
    * 100
)

location = location.sort_values(
    "location_rank"
)

output_file = (
    "data/analytics/"
    "location_intelligence.parquet"
)

location.to_parquet(
    output_file,
    index=False
)

print("\nLocation Intelligence Created")

print("\nShape:")
print(location.shape)

print("\nColumns:")
print(location.columns.tolist())

print("\nTop 10 Areas:")
print(
    location[
        [
            "lsoa_code",
            "location_intelligence_score",
            "location_rank"
        ]
    ]
    .head(10)
)