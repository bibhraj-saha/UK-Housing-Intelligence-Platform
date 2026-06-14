import pandas as pd

# ==========================================
# LOAD DATA
# ==========================================

housing = pd.read_parquet(
    "data/analytics/housing_intelligence.parquet"
)

geo = pd.read_csv(
    "data/reference/geography/geography_master_lookup.csv"
)

print("Housing Shape:")
print(housing.shape)

print("\nGeography Shape:")
print(geo.shape)

# ==========================================
# SELECT REQUIRED GEOGRAPHY COLUMNS
# ==========================================

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

# ==========================================
# MERGE
# ==========================================

housing = housing.merge(
    geo,
    on="lsoa_code",
    how="left"
)

# ==========================================
# VALIDATION
# ==========================================

print("\nMerged Shape:")
print(housing.shape)

print("\nMissing Geography:")

print(
    housing[
        [
            "local_authority",
            "region",
            "country"
        ]
    ]
    .isna()
    .sum()
)

# ==========================================
# SAVE
# ==========================================

housing.to_parquet(
    "data/analytics/housing_intelligence.parquet",
    index=False
)

print("\nUpdated housing_intelligence.parquet")