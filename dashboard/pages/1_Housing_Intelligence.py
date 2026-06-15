import streamlit as st
import plotly.express as px


from utils.data_loader import load_housing_data
from utils.styles import apply_global_styling
from utils.sidebar_filters import create_filters


st.set_page_config(
    page_title="Housing Intelligence",
    page_icon="📊",
    layout="wide"
)

apply_global_styling()

st.sidebar.markdown(
    "## 🏠 UK Housing Intelligence"
)

df = load_housing_data()

(
    rank_range,
    investment_range,
    housing_range,
    top_n
) = create_filters(df)

df = df[
    (
        df["area_rank"]
        >= rank_range[0]
    )
    &
    (
        df["area_rank"]
        <= rank_range[1]
    )
    &
    (
        df["investment_score"]
        >= investment_range[0]
    )
    &
    (
        df["investment_score"]
        <= investment_range[1]
    )
    &
    (
        df["housing_intelligence_index"]
        >= housing_range[0]
    )
    &
    (
        df["housing_intelligence_index"]
        <= housing_range[1]
    )
]

# =====================================================
# TOP RANKED AREA
# =====================================================

top_area = (
    df.sort_values("area_rank")
    .iloc[0]
)

# =====================================================
# PAGE HEADER
# =====================================================

st.title("Housing Intelligence")

st.markdown(
    """
    Explore housing intelligence scores,
    rankings and area performance.
    """
)

# =====================================================
# KPI SECTION
# =====================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Areas Analysed",
    f"{len(df):,}"
)

elite_areas = (
    df["housing_intelligence_index"]
    >=
    df["housing_intelligence_index"]
    .quantile(0.90)
).sum()

col2.metric(
    "Elite Areas",
    f"{elite_areas:,}"
)

col3.metric(
    "Average Score",
    round(
        df["housing_intelligence_index"].mean(),
        2
    )
)

col4.metric(
    "Top Ranked LSOA",
    top_area["lsoa_code"]
)

with st.expander("KPI Guide"):
    st.markdown(
        """
        **Areas Analysed** – Number of LSOAs currently included after filtering.

        **Elite Areas** – Areas in the top 10% of Housing Intelligence scores.

        **Average Score** – Mean Housing Intelligence score of the current selection.

        **Top Ranked LSOA** – Highest ranked area within the filtered dataset.
        """
    )

st.divider()

# =====================================================
# HOUSING INTELLIGENCE DISTRIBUTION
# =====================================================

st.subheader(
    "Housing Intelligence Distribution"
)

fig = px.histogram(
    df,
    x="housing_intelligence_index",
    nbins=50
)

fig.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# TOP 20 AREAS
# =====================================================

st.subheader(
    f"Top {top_n} Areas"
)

top_20 = (
    df.sort_values(
        "area_rank"
    )
    .head(top_n)
    .reset_index(drop=True)
)

st.dataframe(
    top_20[
        [
            "lsoa_code",
            "local_authority",
            "region",
            "country",
            "housing_intelligence_index",
            "investment_score",
            "area_rank"
        ]
    ],
    use_container_width=True
)

st.divider()

# =====================================================
# BOTTOM 20 AREAS
# =====================================================

st.subheader(
    f"Bottom {top_n} Areas"
)

bottom_20 = (
    df.sort_values(
        "area_rank",
        ascending=False
    )
    .head(top_n)
    .reset_index(drop=True)
)

st.dataframe(
    bottom_20[
        [
            "lsoa_code",
            "local_authority",
            "region",
            "country",
            "housing_intelligence_index",
            "investment_score",
            "area_rank"
        ]
    ],
    use_container_width=True
)