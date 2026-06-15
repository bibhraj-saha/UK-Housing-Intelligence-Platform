import streamlit as st
import pandas as pd
import plotly.express as px

from utils.styles import apply_global_styling

st.set_page_config(
    page_title="Housing Intelligence Map",
    layout="wide"
)

apply_global_styling()

st.title("Housing Intelligence Map")

st.markdown(
    """
    Explore Housing Intelligence scores geographically across the UK.
    """
)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_parquet(
    "data/analytics/housing_map.parquet"
)

# =====================================================
# KPI SECTION
# =====================================================

mapped_areas = len(df)

regions_represented = (
    df["region"]
    .nunique()
)

elite_threshold = (
    df["housing_intelligence_index"]
    .quantile(0.90)
)

elite_areas = (
    df["housing_intelligence_index"]
    >= elite_threshold
).sum()

avg_score = round(
    df["housing_intelligence_index"].mean(),
    2
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Mapped Areas",
    f"{mapped_areas:,}"
)

col2.metric(
    "Regions Represented",
    f"{regions_represented:,}"
)

col3.metric(
    "Elite Areas",
    f"{elite_areas:,}"
)

col4.metric(
    "Average Intelligence",
    avg_score
)

with st.expander("KPI Guide"):
    st.markdown(
        """
        **Mapped Areas** – Total LSOAs displayed on the map.

        **Regions Represented** – Number of regions represented.

        **Elite Areas** – Areas within the top 10% Housing Intelligence scores.

        **Average Intelligence** – Mean Housing Intelligence score of all mapped areas.
        """
    )

st.divider()

# =====================================================
# REGION FILTER
# =====================================================

regions = ["All"] + sorted(
    df["region"]
    .dropna()
    .unique()
    .tolist()
)

selected_region = st.selectbox(
    "Select Region",
    regions
)

if selected_region != "All":
    df = df[
        df["region"]
        == selected_region
    ]

# =====================================================
# MAP
# =====================================================

st.subheader(
    "Housing Intelligence Map"
)

fig = px.scatter_map(
    df,
    lat="latitude",
    lon="longitude",
    color="housing_intelligence_index",
    hover_name="lsoa_code",
    hover_data={
        "local_authority": True,
        "region": True,
        "investment_score": ":.2f",
        "area_rank": True,
        "latitude": False,
        "longitude": False
    },
    zoom=4,
    height=700
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# TOP AREAS TABLE
# =====================================================

st.subheader(
    "Top Areas In Current Selection"
)

top_areas = (
    df.sort_values(
        "area_rank"
    )
    .head(25)
)

st.dataframe(
    top_areas[
        [
            "lsoa_code",
            "local_authority",
            "region",
            "housing_intelligence_index",
            "investment_score",
            "area_rank"
        ]
    ],
    use_container_width=True
)