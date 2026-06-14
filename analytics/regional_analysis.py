import pandas as pd

INPUT_FILE = "data/analytics/housing_intelligence.parquet"

OUTPUT_FILE = "data/analytics/regional_intelligence.parquet"

df = pd.read_parquet(INPUT_FILE)

# ==========================================
# TOP 10% THRESHOLD
# ==========================================

top_10_threshold = (
    df["housing_intelligence_index"]
    .quantile(0.90)
)

df["is_top_10_percent"] = (
    df["housing_intelligence_index"]
    >= top_10_threshold
)

# ==========================================
# REGIONAL AGGREGATION
# ==========================================

regional = (
    df.groupby("region", as_index=False)
    .agg(
        {
            "housing_intelligence_index": "mean",
            "investment_score": "mean",
            "growth_score": "mean",
            "average_price": "mean",
            "average_crime": "mean",
            "lsoa_code": "count",
            "is_top_10_percent": "sum"
        }
    )
)

regional = regional.rename(
    columns={
        "lsoa_code": "area_count",
        "is_top_10_percent": "top_10_percent_areas"
    }
)

regional["regional_rank"] = (
    regional["housing_intelligence_index"]
    .rank(
        ascending=False,
        method="dense"
    )
    .astype(int)
)

regional = regional.sort_values(
    "regional_rank"
)

regional.to_parquet(
    OUTPUT_FILE,
    index=False
)

print(regional)