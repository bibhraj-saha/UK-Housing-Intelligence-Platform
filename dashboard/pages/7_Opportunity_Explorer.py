import streamlit as st
import pandas as pd

from utils.styles import apply_global_styling

st.set_page_config(
    page_title="Opportunity Explorer",
    layout="wide"
)

apply_global_styling()

st.title("Opportunity Explorer")

st.markdown(
    """
    Discover areas matching your investment and housing criteria.
    """
)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_parquet(
    "data/analytics/opportunity_explorer.parquet"
)

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header(
    "Opportunity Criteria"
)

regions = ["All"] + sorted(
    df["region"].dropna().unique()
)

selected_region = st.sidebar.selectbox(
    "Region",
    regions
)

price_range = st.sidebar.slider(
    "Average Price (£)",
    int(df["average_price"].min()),
    int(df["average_price"].max()),
    (
        int(df["average_price"].min()),
        int(df["average_price"].max())
    )
)

investment_threshold = st.sidebar.slider(
    "Minimum Investment Score",
    0,
    100,
    50
)

housing_threshold = st.sidebar.slider(
    "Minimum Housing Intelligence",
    0,
    100,
    50
)

# =====================================================
# FILTERING
# =====================================================

filtered = df.copy()

if selected_region != "All":
    filtered = filtered[
        filtered["region"]
        == selected_region
    ]

filtered = filtered[
    (
        filtered["average_price"]
        >= price_range[0]
    )
    &
    (
        filtered["average_price"]
        <= price_range[1]
    )
    &
    (
        filtered["investment_score"]
        >= investment_threshold
    )
    &
    (
        filtered["housing_intelligence_index"]
        >= housing_threshold
    )
]

# =====================================================
# KPIs
# =====================================================

matches = len(filtered)

avg_investment = (
    round(
        filtered["investment_score"].mean(),
        2
    )
    if matches > 0
    else "-"
)

avg_score = (
    round(
        filtered[
            "housing_intelligence_index"
        ].mean(),
        2
    )
    if matches > 0
    else "-"
)

avg_price = (
    round(
        filtered["average_price"].mean(),
        0
    )
    if matches > 0
    else "-"
)

regions_found = (
    filtered["region"].nunique()
    if matches > 0
    else "-"
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Matching Areas",
    f"{matches:,}"
)

c2.metric(
    "Regions Found",
    regions_found
)

c3.metric(
    "Average Investment",
    avg_investment
)

c4.metric(
    "Average Price (£)",
    f"{avg_price:,.0f}"
    if avg_price != "-"
    else "-"
)

with st.expander("KPI Guide"):
    st.markdown(
        """
        **Matching Areas** – Areas meeting your selected criteria.

        **Regions Found** – Number of regions containing matching opportunities.

        **Average Investment** – Average Investment Score of matching areas.

        **Average Price (£)** – Average property price of matching areas.
        """
    )

st.divider()

# =====================================================
# RESULTS
# =====================================================

st.subheader(
    "Matching Opportunities"
)

results = (
    filtered
    .sort_values("area_rank")
)

st.dataframe(
    results,
    use_container_width=True
)