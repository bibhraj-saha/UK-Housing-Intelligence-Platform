import pandas as pd

INPUT_FILE = "data/analytics/housing_intelligence.parquet"

OUTPUT_FILE = "data/analytics/opportunity_explorer.parquet"

df = pd.read_parquet(INPUT_FILE)

columns = [
    "lsoa_code",
    "local_authority",
    "region",
    "country",
    "average_price",
    "average_crime",
    "investment_score",
    "growth_score",
    "housing_intelligence_index",
    "area_rank"
]

df = df[columns].copy()

df.to_parquet(
    OUTPUT_FILE,
    index=False
)

print(df.shape)
print(df.head())