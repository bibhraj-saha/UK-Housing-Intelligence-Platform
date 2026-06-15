import pandas as pd

INPUT_FILE = (
    "data/analytics/historical_housing_trends.parquet"
)

OUTPUT_FILE = (
    "data/analytics/regional_housing_trends.parquet"
)

print("Loading historical trends...")

df = pd.read_parquet(INPUT_FILE)

print(df.shape)

# =====================================================
# REGIONAL AGGREGATION
# =====================================================

regional = (
    df.groupby(
        [
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

regional["year_month"] = pd.to_datetime(
    dict(
        year=regional["year"],
        month=regional["month"],
        day=1
    )
)

regional = regional.sort_values(
    [
        "region",
        "year_month"
    ]
)

# =====================================================
# MONTH OVER MONTH GROWTH
# =====================================================

regional["mom_price_growth_pct"] = (
    regional.groupby("region")["average_price"]
    .pct_change()
    * 100
)

# =====================================================
# YEAR OVER YEAR GROWTH
# =====================================================

regional["yoy_price_growth_pct"] = (
    regional.groupby("region")["average_price"]
    .pct_change(periods=12)
    * 100
)

# =====================================================
# ROLLING 12 MONTH AVERAGE
# =====================================================

regional["rolling_12m_average_price"] = (
    regional.groupby("region")["average_price"]
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

regional = regional.drop(
    columns=["year_month"]
)

regional.to_parquet(
    OUTPUT_FILE,
    index=False
)

print("\nRegional Trends Created")

print("\nShape:")
print(regional.shape)

print("\nColumns:")
print(regional.columns.tolist())

print("\nSample:")
print(regional.head())