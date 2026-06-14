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

INCOME_FILE = (
    "data/reference/income/income_lookup.csv"
)

# =====================================================
# LOAD INCOME LOOKUP
# =====================================================

income = pd.read_csv(
    INCOME_FILE
)

income = income[
    [
        "lad_code",
        "median_weekly_income",
        "mean_weekly_income",
        "estimated_annual_income"
    ]
]

print("\nIncome Lookup:")
print(income.shape)

# =====================================================
# PROCESS FILES
# =====================================================

for file in ANALYTICS_FILES:

    print("\n-------------------------------------")
    print(file)

    df = pd.read_parquet(file)

    print("Before:", df.shape)

    # ==========================================
    # REMOVE OLD COLUMNS IF RERUN
    # ==========================================

    cols_to_remove = [
        "median_weekly_income",
        "mean_weekly_income",
        "estimated_annual_income",
        "price_to_income_ratio",
        "income_affordability_score"
    ]

    existing_cols = [
        col
        for col in cols_to_remove
        if col in df.columns
    ]

    if existing_cols:
        df = df.drop(
            columns=existing_cols
        )

    # ==========================================
    # JOIN INCOME
    # ==========================================

    df = df.merge(
        income,
        on="lad_code",
        how="left"
    )

    # ==========================================
    # PRICE-BASED METRICS
    # Only if average_price exists
    # ==========================================

    if "average_price" in df.columns:

        df["price_to_income_ratio"] = (
            df["average_price"]
            /
            df["estimated_annual_income"]
        )

        income_percentile = (
            df["estimated_annual_income"]
            .rank(pct=True)
            * 100
        )

        ratio_percentile = (
            (
                1
                /
                df["price_to_income_ratio"]
            )
            .rank(pct=True)
            * 100
        )

        df["income_affordability_score"] = (
            income_percentile * 0.50
            +
            ratio_percentile * 0.50
        )

    print("After:", df.shape)

    print(
        "Missing Income:",
        df["estimated_annual_income"]
        .isna()
        .sum()
    )

    df.to_parquet(
        file,
        index=False
    )

print("\nIncome enrichment complete.")