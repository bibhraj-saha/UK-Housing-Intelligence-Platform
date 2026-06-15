import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Income Intelligence",
    layout="wide"
)

st.title("Income Intelligence")

@st.cache_data
def load_data():
    df = pd.read_parquet(
        "data/analytics/housing_intelligence.parquet"
    )

    return df

df = load_data()

df = df.dropna(
    subset=[
        "estimated_annual_income",
        "price_to_income_ratio",
        "income_affordability_score"
    ]
)

# =========================
# Sidebar Filters
# =========================

st.sidebar.header("Filters")

region = st.sidebar.selectbox(
    "Region",
    ["All"] + sorted(df["region"].dropna().unique().tolist())
)

if region != "All":
    df = df[
        df["region"] == region
    ]

local_authorities = (
    ["All"]
    +
    sorted(
        df["local_authority"]
        .dropna()
        .unique()
        .tolist()
    )
)

local_authority = st.sidebar.selectbox(
    "Local Authority",
    local_authorities
)

if local_authority != "All":
    df = df[
        df["local_authority"] == local_authority
    ]

# =========================
# KPI Cards
# =========================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Median Income",
        f"£{df['estimated_annual_income'].median():,.0f}"
    )

with col2:
    st.metric(
        "Average Income",
        f"£{df['estimated_annual_income'].mean():,.0f}"
    )

with col3:
    st.metric(
        "Best Affordability",
        f"{df['price_to_income_ratio'].min():.2f}"
    )

with col4:
    st.metric(
        "Most Affordable Score",
        f"{df['income_affordability_score'].max():.1f}"
    )

with col5:
    st.metric(
        "Areas",
        f"{len(df):,}"
    )

st.divider()

# =========================
# Income Distribution
# =========================

st.subheader("Income Distribution")

fig = px.histogram(
    df,
    x="estimated_annual_income",
    nbins=40
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================
# Top Income Areas
# =========================

st.subheader("Top 20 Highest Income Areas")

top_income = (
    df.sort_values(
        "estimated_annual_income",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_income[
        [
            "lsoa_code",
            "local_authority",
            "region",
            "estimated_annual_income"
        ]
    ],
    use_container_width=True
)

# =========================
# Most Affordable Areas
# =========================

st.subheader("Top 20 Most Affordable Areas")

top_affordable = (
    df.sort_values(
        "income_affordability_score",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_affordable[
        [
            "lsoa_code",
            "local_authority",
            "region",
            "price_to_income_ratio",
            "income_affordability_score"
        ]
    ],
    use_container_width=True
)

# =========================
# Price vs Income
# =========================

st.subheader("Property Price vs Income")

cap = (
    df["price_to_income_ratio"]
    .quantile(0.99)
)

scatter_df = df[
    df["price_to_income_ratio"] <= cap
]

fig = px.scatter(
    scatter_df,
    x="estimated_annual_income",
    y="average_price",
    color="region",
    hover_data=[
        "local_authority",
        "lsoa_code"
    ]
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================
# Regional Comparison
# =========================

st.subheader("Regional Income Comparison")

regional = (
    df.groupby("region")
    .agg(
        annual_income=(
            "estimated_annual_income",
            "mean"
        ),
        affordability_score=(
            "income_affordability_score",
            "mean"
        )
    )
    .reset_index()
)

fig = px.bar(
    regional,
    x="region",
    y="annual_income"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================
# Leaderboard
# =========================

st.subheader("Income Affordability Leaderboard")

leaderboard = (
    df.sort_values(
        "income_affordability_score",
        ascending=False
    )
)

st.dataframe(
    leaderboard[
        [
            "lsoa_code",
            "local_authority",
            "region",
            "estimated_annual_income",
            "average_price",
            "price_to_income_ratio",
            "income_affordability_score"
        ]
    ],
    use_container_width=True
)