import pandas as pd

INPUT_FILE = (
    "data/analytics/historical_housing_trends.parquet"
)

OUTPUT_FILE = (
    "data/analytics/local_authority_trends.parquet"
)

print("Loading historical trends...")

df = pd.read_parquet(INPUT_FILE)

print(df.shape)

# =====================================================
# LOCAL AUTHORITY AGGREGATION
# =====================================================

local_authority = (
    df.groupby(
        [
            "local_authority",
            "region",
            "country",
            "year",
            "month"
        ],
        as_index=False
    )
    .agg(
        average_price=(
            "average_price",
            "mean"
        ),
        median_price=(
            "median_price",
            "mean"
        ),
        transaction_count=(
            "transaction_count",
            "sum"
        )
    )
)

# =====================================================
# DATE COLUMN
# =====================================================

local_authority["year_month"] = pd.to_datetime(
    dict(
        year=local_authority["year"],
        month=local_authority["month"],
        day=1
    )
)

local_authority = local_authority.sort_values(
    [
        "local_authority",
        "year_month"
    ]
)

# =====================================================
# MONTH OVER MONTH GROWTH
# =====================================================

local_authority["mom_price_growth_pct"] = (
    local_authority.groupby(
        "local_authority"
    )["average_price"]
    .pct_change()
    * 100
)

# =====================================================
# YEAR OVER YEAR GROWTH
# =====================================================

local_authority["yoy_price_growth_pct"] = (
    local_authority.groupby(
        "local_authority"
    )["average_price"]
    .pct_change(periods=12)
    * 100
)

# =====================================================
# ROLLING 12 MONTH AVERAGE
# =====================================================

local_authority["rolling_12m_average_price"] = (
    local_authority.groupby(
        "local_authority"
    )["average_price"]
    .transform(
        lambda x: (
            x.rolling(
                window=12,
                min_periods=1
            )
            .mean()
        )
    )
)

local_authority = local_authority.drop(
    columns=["year_month"]
)

local_authority.to_parquet(
    OUTPUT_FILE,
    index=False
)

print("\nLocal Authority Trends Created")

print("\nShape:")
print(local_authority.shape)

print("\nColumns:")
print(local_authority.columns.tolist())

print("\nSample:")
print(local_authority.head())