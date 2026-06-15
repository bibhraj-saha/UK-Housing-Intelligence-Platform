import pandas as pd

# =====================================================
# FILES
# =====================================================

PROPERTY_FILE = (
    "data/processed/property_geography.csv"
)

GEOGRAPHY_FILE = (
    "data/reference/geography/geography_master_lookup.csv"
)

OUTPUT_FILE = (
    "data/analytics/historical_housing_trends.parquet"
)

# =====================================================
# LOAD PROPERTY DATA
# =====================================================

print("Loading property geography dataset...")

df = pd.read_csv(
    PROPERTY_FILE,
    usecols=[
        "lsoa_code",
        "price",
        "transfer_year",
        "transfer_month"
    ]
)

print("Property Shape:")
print(df.shape)

# =====================================================
# LOAD GEOGRAPHY
# =====================================================

geo = pd.read_csv(
    GEOGRAPHY_FILE
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

print("\nGeography Shape:")
print(geo.shape)

# =====================================================
# DATA QUALITY
# =====================================================

df = df.dropna(
    subset=[
        "lsoa_code",
        "price",
        "transfer_year",
        "transfer_month"
    ]
)

# =====================================================
# HISTORICAL AGGREGATION
# =====================================================

historical = (
    df.groupby(
        [
            "lsoa_code",
            "transfer_year",
            "transfer_month"
        ],
        as_index=False
    )
    .agg(
        average_price=(
            "price",
            "mean"
        ),
        median_price=(
            "price",
            "median"
        ),
        transaction_count=(
            "price",
            "count"
        )
    )
)

# =====================================================
# RENAME
# =====================================================

historical = historical.rename(
    columns={
        "transfer_year": "year",
        "transfer_month": "month"
    }
)

# =====================================================
# ENRICH WITH GEOGRAPHY
# =====================================================

historical = historical.merge(
    geo,
    on="lsoa_code",
    how="left"
)

# =====================================================
# SORT
# =====================================================

historical = historical.sort_values(
    [
        "region",
        "local_authority",
        "lsoa_code",
        "year",
        "month"
    ]
)

# =====================================================
# SAVE
# =====================================================

historical.to_parquet(
    OUTPUT_FILE,
    index=False
)

print("\nHistorical Trends Created")

print("\nShape:")
print(historical.shape)

print("\nColumns:")
print(historical.columns.tolist())

print("\nMissing Geography:")
print(
    historical[
        [
            "local_authority",
            "region",
            "country"
        ]
    ]
    .isna()
    .sum()
)