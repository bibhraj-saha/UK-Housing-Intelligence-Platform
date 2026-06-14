import streamlit as st
import plotly.express as px

from utils.data_loader import load_housing_data
from utils.styles import apply_global_styling
from utils.sidebar_filters import create_filters


st.set_page_config(
    page_title="Investment Opportunities",
    page_icon="💰",
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

st.title("💰 Investment Opportunities")

st.markdown(
    """
    Explore investment potential, growth opportunities,
    and housing intelligence rankings across UK LSOAs.
    """
)

# =====================================================
# KPI SECTION
# =====================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Investment Score",
    round(
        df["investment_score"].mean(),
        2
    )
)

col2.metric(
    "Highest Investment Score",
    round(
        df["investment_score"].max(),
        2
    )
)

col3.metric(
    "Average Growth Score",
    round(
        df["growth_score"].mean(),
        2
    )
)

col4.metric(
    "Highest Growth Score",
    round(
        df["growth_score"].max(),
        2
    )
)

st.divider()

# =====================================================
# INVESTMENT SCORE DISTRIBUTION
# =====================================================

st.subheader(
    "Investment Score Distribution"
)

fig = px.histogram(
    df,
    x="investment_score",
    nbins=50,
    title="Distribution of Investment Scores"
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
# TOP INVESTMENT AREAS
# =====================================================

st.subheader(
    f"Top {top_n} Investment Areas"
)

top_investment = (
    df.sort_values(
        "investment_score",
        ascending=False
    )
    .head(top_n)
    .reset_index(drop=True)
)

st.dataframe(
    top_investment[
        [
            "lsoa_code",
            "investment_score",
            "growth_score",
            "housing_intelligence_index",
            "average_price"
        ]
    ],
    use_container_width=True
)

st.divider()

# =====================================================
# INVESTMENT VS GROWTH
# =====================================================

st.subheader(
    "Investment Score vs Growth Score"
)

fig = px.scatter(
    df,
    x="growth_score",
    y="investment_score",
    hover_data=[
        "lsoa_code"
    ],
    title="Investment Potential vs Growth Potential"
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
# BEST OPPORTUNITY AREAS
# =====================================================

st.subheader(
    f"Top {top_n} Opportunity Areas"
)

opportunity_areas = (
    df.sort_values(
        "investment_opportunity_score",
        ascending=False
    )
    .head(top_n)
    .reset_index(drop=True)
)

st.dataframe(
    opportunity_areas[
        [
            "lsoa_code",
            "investment_opportunity_score",
            "investment_score",
            "growth_score",
            "average_price"
        ]
    ],
    use_container_width=True
)