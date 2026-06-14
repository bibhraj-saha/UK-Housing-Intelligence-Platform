import pandas as pd

INPUT_FILE = "data/analytics/housing_intelligence.parquet"

OUTPUT_FILE = "data/analytics/housing_map.parquet"

df = pd.read_parquet(INPUT_FILE)

map_df = df[
    [
        "lsoa_code",
        "local_authority",
        "region",
        "country",
        "latitude",
        "longitude",
        "housing_intelligence_index",
        "investment_score",
        "growth_score",
        "area_rank"
    ]
].copy()

map_df.to_parquet(
    OUTPUT_FILE,
    index=False
)

print(map_df.shape)

print(map_df.head())