import streamlit as st
import pandas as pd
import plotly.express as px

from utils.styles import apply_global_styling

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Regional Intelligence",
    layout="wide"
)

apply_global_styling()

st.title("Regional Intelligence")

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_parquet(
    "data/analytics/regional_intelligence.parquet"
)

# ==========================================
# KPI SECTION
# ==========================================

top_region = df.iloc[0]["region"]

regions_analysed = df["region"].nunique()

areas_represented = int(
    df["area_count"].sum()
)

top_10_areas = int(
    df["top_10_percent_areas"].sum()
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
    "Region Leader",
    top_region
)

with col2:
    st.metric(
        "Regions Analysed",
        f"{regions_analysed:,}"
    )

with col3:
    st.metric(
        "Areas Represented",
        f"{areas_represented:,}"
    )

with col4:
    st.metric(
    "Elite Areas",
    f"{top_10_areas:,}"
)

# ==========================================
# REGIONAL RANKINGS
# ==========================================

st.subheader(
    "Regional Housing Intelligence Rankings"
)

fig = px.bar(
    df.sort_values(
        "housing_intelligence_index",
        ascending=False
    ),
    x="region",
    y="housing_intelligence_index"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# INVESTMENT SCORE
# ==========================================

st.subheader(
    "Regional Investment Scores"
)

fig = px.bar(
    df.sort_values(
        "investment_score",
        ascending=False
    ),
    x="region",
    y="investment_score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# REGIONAL TABLE
# ==========================================

st.subheader(
    "Regional Intelligence Table"
)

st.dataframe(
    df,
    use_container_width=True
)