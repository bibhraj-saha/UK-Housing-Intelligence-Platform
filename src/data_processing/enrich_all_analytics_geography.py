import pandas as pd

FILES = [
    "area_analytics_base.parquet",
    "crime_scores.parquet",
    "growth_scores.parquet",
    "investment_scores.parquet",
    "rankings.parquet",
    "top_100_areas.parquet",
    "bottom_100_areas.parquet"
]

geo = pd.read_csv(
    "data/reference/geography/geography_master_lookup.csv"
)

geo = geo[
    [
        "lsoa_code",
        "local_authority",
        "region",
        "country",
        "latitude",
        "longitude"
    ]
]

for file in FILES:

    path = f"data/analytics/{file}"

    print(f"\nProcessing: {file}")

    df = pd.read_parquet(path)

    geography_cols = [
        "local_authority",
        "region",
        "country",
        "latitude",
        "longitude"
    ]

    existing = [
        c for c in geography_cols
        if c in df.columns
    ]

    if existing:
        df = df.drop(columns=existing)

    df = df.merge(
        geo,
        on="lsoa_code",
        how="left"
    )

    df.to_parquet(
        path,
        index=False
    )

    print(df.shape)

print("\nAll analytics datasets enriched.")