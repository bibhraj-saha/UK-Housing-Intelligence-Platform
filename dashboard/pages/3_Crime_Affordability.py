import streamlit as st
import plotly.express as px

from utils.data_loader import load_housing_data
from utils.styles import apply_global_styling
from utils.sidebar_filters import create_filters


st.set_page_config(
    page_title="Crime & Affordability",
    page_icon="🛡️",
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

# =====================================================
# APPLY FILTERS
# =====================================================

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
# PAGE HEADER
# =====================================================

st.title("Crime & Affordability")

st.markdown(
    """
    Analyze crime levels, affordability,
    and their relationship across UK LSOAs.
    """
)

# =====================================================
# KPI CALCULATIONS
# =====================================================

low_crime_areas = len(
    df[
        df["crime_score"] >= 75
    ]
)

ideal_areas = len(
    df[
        (
            df["crime_score"] >= 75
        )
        &
        (
            df["affordability_score"] >= 75
        )
    ]
)

# =====================================================
# KPI CARDS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Crime Score",
    round(
        df["crime_score"].mean(),
        2
    )
)

col2.metric(
    "Average Affordability",
    round(
        df["affordability_score"].mean(),
        2
    )
)

col3.metric(
    "Low Crime Areas",
    f"{low_crime_areas:,}"
)

col4.metric(
    "Low Crime + High Affordability",
    f"{ideal_areas:,}"
)

with st.expander("KPI Guide"):
    st.markdown(
        """
        **Average Crime Score** – Average crime performance across selected areas.

        **Average Affordability** – Average affordability score across selected areas.

        **Low Crime Areas** – Areas with Crime Scores of 75 or higher.

        **Low Crime + High Affordability** – Areas scoring at least 75 in both crime and affordability.
        """
    )

st.divider()

# =====================================================
# CRIME SCORE DISTRIBUTION
# =====================================================

st.subheader(
    "Crime Score Distribution"
)

fig = px.histogram(
    df,
    x="crime_score",
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
# AFFORDABILITY DISTRIBUTION
# =====================================================

st.subheader(
    "Affordability Score Distribution"
)

fig = px.histogram(
    df,
    x="affordability_score",
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
# CRIME VS AFFORDABILITY
# =====================================================

st.subheader(
    "Crime Score vs Affordability Score"
)

fig = px.scatter(
    df,
    x="crime_score",
    y="affordability_score",
    hover_data=[
        "lsoa_code"
    ]
)

fig.update_layout(
    template="plotly_dark",
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# LOW CRIME + HIGH AFFORDABILITY
# =====================================================

st.subheader(
    f"Top {top_n} Areas: Low Crime & High Affordability"
)

best_areas = (
    df.sort_values(
        [
            "crime_score",
            "affordability_score"
        ],
        ascending=[
            False,
            False
        ]
    )
    .head(top_n)
    .reset_index(drop=True)
)

st.dataframe(
    best_areas[
        [
            "lsoa_code",
            "local_authority",
            "region",
            "country",
            "crime_score",
            "affordability_score",
            "investment_score",
            "housing_intelligence_index",
            "area_rank"
        ]
    ],
    use_container_width=True
)