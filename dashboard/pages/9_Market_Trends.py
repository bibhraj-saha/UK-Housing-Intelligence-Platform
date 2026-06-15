import streamlit as st
import pandas as pd
import plotly.express as px

from utils.styles import apply_global_styling

st.set_page_config(
    page_title="Market Trends",
    layout="wide"
)

apply_global_styling()

st.title("Market Trends")

st.markdown(
    """
    Explore historical housing prices, transaction activity, and market growth trends over time.
    """
)

@st.cache_data
def load_data():

    historical = pd.read_parquet(
        "data/analytics/historical_housing_trends.parquet"
    )

    regional = pd.read_parquet(
        "data/analytics/regional_housing_trends.parquet"
    )

    local_authority = pd.read_parquet(
        "data/analytics/local_authority_trends.parquet"
    )

    return historical, regional, local_authority


historical, regional, local_authority = load_data()

# =====================================
# Create Date Columns
# =====================================

historical["date"] = pd.to_datetime(
    historical["year"].astype(str)
    + "-"
    + historical["month"].astype(str)
    + "-01"
)

regional["date"] = pd.to_datetime(
    regional["year"].astype(str)
    + "-"
    + regional["month"].astype(str)
    + "-01"
)

local_authority["date"] = pd.to_datetime(
    local_authority["year"].astype(str)
    + "-"
    + local_authority["month"].astype(str)
    + "-01"
)

# =====================================
# Sidebar Filters
# =====================================

st.sidebar.header("Filters")

region_options = (
    ["All"]
    + sorted(
        regional["region"]
        .dropna()
        .unique()
        .tolist()
    )
)

selected_region = st.sidebar.selectbox(
    "Region",
    region_options
)

regional_filtered = regional.copy()
local_filtered = local_authority.copy()

if selected_region != "All":

    regional_filtered = regional_filtered[
        regional_filtered["region"]
        == selected_region
    ]

    local_filtered = local_filtered[
        local_filtered["region"]
        == selected_region
    ]

local_authority_options = (
    ["All"]
    + sorted(
        local_filtered["local_authority"]
        .dropna()
        .unique()
        .tolist()
    )
)

selected_la = st.sidebar.selectbox(
    "Local Authority",
    local_authority_options
)

if selected_la != "All":

    local_filtered = local_filtered[
        local_filtered["local_authority"]
        == selected_la
    ]

# =====================================
# KPI Section
# =====================================

latest_region = regional.sort_values(
    ["year", "month"]
).iloc[-1]

latest_avg_price = latest_region["average_price"]

latest_transactions = (
    regional.sort_values(
        ["year", "month"]
    )
    .groupby(
        ["year", "month"]
    )["transaction_count"]
    .sum()
    .iloc[-1]
)

top_growth_region = (
    regional
    .dropna(
        subset=["yoy_price_growth_pct"]
    )
    .sort_values(
        "yoy_price_growth_pct",
        ascending=False
    )
    .iloc[0]
)

top_growth_la = (
    local_authority
    .dropna(
        subset=["yoy_price_growth_pct"]
    )
    .sort_values(
        "yoy_price_growth_pct",
        ascending=False
    )
    .iloc[0]
)

avg_yoy_growth = (
    regional["yoy_price_growth_pct"]
    .mean()
)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Latest Avg Price",
    f"£{latest_avg_price:,.0f}"
)

c2.metric(
    "Avg YoY Growth",
    f"{avg_yoy_growth:.2f}%"
)

c3.metric(
    "Top Growth Region",
    top_growth_region["region"]
)

c4.metric(
    "Top Growth LA",
    top_growth_la["local_authority"]
)

c5.metric(
    "Transactions",
    f"{latest_transactions:,.0f}"
)

with st.expander("KPI Guide"):
    st.markdown(
        """
        **Latest Avg Price** – Most recent average property price available.

        **Avg YoY Growth** – Average year-over-year property price growth.

        **Top Growth Region** – Region with the highest recorded annual growth.

        **Top Growth LA** – Local Authority with the highest annual growth.

        **Transactions** – Latest monthly transaction volume.
        """
    )

st.divider()

# =====================================
# UK Housing Trend
# =====================================

st.subheader(
    "Average House Price Trend"
)

uk_trend = (
    historical
    .groupby("date")
    .agg(
        average_price=(
            "average_price",
            "mean"
        )
    )
    .reset_index()
)

fig = px.line(
    uk_trend,
    x="date",
    y="average_price"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# Regional Comparison
# =====================================

st.subheader(
    "Regional Price Trends"
)

fig = px.line(
    regional_filtered,
    x="date",
    y="average_price",
    color="region"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# Regional Growth Leaderboard
# =====================================

st.subheader(
    "Top Regions By YoY Growth"
)

regional_growth = (
    regional
    .dropna(
        subset=["yoy_price_growth_pct"]
    )
    .sort_values(
        "yoy_price_growth_pct",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    regional_growth[
        [
            "region",
            "year",
            "month",
            "yoy_price_growth_pct"
        ]
    ],
    use_container_width=True
)

# =====================================
# Local Authority Leaderboard
# =====================================

st.subheader(
    "Top Local Authorities By YoY Growth"
)

la_growth = (
    local_filtered
    .dropna(
        subset=["yoy_price_growth_pct"]
    )
    .sort_values(
        "yoy_price_growth_pct",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    la_growth[
        [
            "local_authority",
            "region",
            "year",
            "month",
            "yoy_price_growth_pct"
        ]
    ],
    use_container_width=True
)

# =====================================
# Transaction Volume Trend
# =====================================

st.subheader(
    "Transaction Volume Trend"
)

transactions = (
    regional_filtered
    .groupby("date")
    .agg(
        transaction_count=(
            "transaction_count",
            "sum"
        )
    )
    .reset_index()
)

fig = px.bar(
    transactions,
    x="date",
    y="transaction_count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# Rolling 12 Month Trend
# =====================================

st.subheader(
    "Rolling 12-Month Price Trend"
)

fig = px.line(
    regional_filtered,
    x="date",
    y="rolling_12m_average_price",
    color="region"
)

st.plotly_chart(
    fig,
    use_container_width=True
)