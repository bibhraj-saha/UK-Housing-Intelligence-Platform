import pandas as pd

# =====================================================
# FILES
# =====================================================

ANALYTICS_FILES = [
    "data/analytics/area_analytics_base.parquet",
    "data/analytics/crime_scores.parquet",
    "data/analytics/growth_scores.parquet",
    "data/analytics/investment_scores.parquet",
    "data/analytics/rankings.parquet",
    "data/analytics/housing_intelligence.parquet",
    "data/analytics/top_100_areas.parquet",
    "data/analytics/bottom_100_areas.parquet"
]

# =====================================================
# LOAD GEOGRAPHY LOOKUP
# =====================================================

geo = pd.read_csv(
    "data/reference/geography/geography_master_lookup.csv"
)

geo = geo[
    [
        "lsoa_code",
        "lad_code"
    ]
]

print("\nGeography Lookup:")
print(geo.shape)

# =====================================================
# PROCESS FILES
# =====================================================

for file in ANALYTICS_FILES:

    print("\n-------------------------------------")
    print(file)

    df = pd.read_parquet(file)

    print("Before:", df.shape)

    # Remove lad_code if already exists
    if "lad_code" in df.columns:
        df = df.drop(
            columns=["lad_code"]
        )

    df = df.merge(
        geo,
        on="lsoa_code",
        how="left"
    )

    print("After:", df.shape)

    print(
        "Missing LAD Codes:",
        df["lad_code"].isna().sum()
    )

    df.to_parquet(
        file,
        index=False
    )

print("\nAll analytics datasets updated.")