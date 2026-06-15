import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.data_loader import load_housing_data
from utils.styles import apply_global_styling


st.set_page_config(
    page_title="Area Comparison",
    page_icon="⚖️",
    layout="wide"
)

apply_global_styling()

st.sidebar.markdown(
    "## 🏠 UK Housing Intelligence"
)

df = load_housing_data()

st.title("Area Comparison")

st.markdown(
    """
    Compare housing intelligence metrics
    between any two LSOAs.
    """
)

# =====================================================
# AREA SELECTORS
# =====================================================

lsoa_list = sorted(
    df["lsoa_code"].unique().tolist()
)

col1, col2 = st.columns(2)

with col1:

    area_1 = st.selectbox(
        "Select Area 1",
        lsoa_list,
        index=0
    )

with col2:

    area_2 = st.selectbox(
        "Select Area 2",
        lsoa_list,
        index=1
    )

# =====================================================
# EXTRACT DATA
# =====================================================

area1_df = (
    df[
        df["lsoa_code"] == area_1
    ]
    .iloc[0]
)

area2_df = (
    df[
        df["lsoa_code"] == area_2
    ]
    .iloc[0]
)

# =====================================================
# AREA DETAILS
# =====================================================

st.subheader(
    "Area Details"
)

c1, c2 = st.columns(2)

with c1:

    st.info(
        f"""
LSOA: {area1_df['lsoa_code']}

Local Authority: {area1_df['local_authority']}

Region: {area1_df['region']}

Country: {area1_df['country']}
"""
    )

with c2:

    st.info(
        f"""
LSOA: {area2_df['lsoa_code']}

Local Authority: {area2_df['local_authority']}

Region: {area2_df['region']}

Country: {area2_df['country']}
"""
    )
st.divider()

# =====================================================
# COMPARISON TABLE
# =====================================================

comparison = pd.DataFrame(
    {
        "Metric": [
            "Average Price",
            "Crime Score",
            "Affordability Score",
            "Growth Score",
            "Investment Score",
            "Housing Intelligence Index",
            "Area Rank"
        ],
        area_1: [
            area1_df["average_price"],
            area1_df["crime_score"],
            area1_df["affordability_score"],
            area1_df["growth_score"],
            area1_df["investment_score"],
            area1_df["housing_intelligence_index"],
            area1_df["area_rank"]
        ],
        area_2: [
            area2_df["average_price"],
            area2_df["crime_score"],
            area2_df["affordability_score"],
            area2_df["growth_score"],
            area2_df["investment_score"],
            area2_df["housing_intelligence_index"],
            area2_df["area_rank"]
        ]
    }
)

st.subheader(
    "Comparison Results"
)

st.dataframe(
    comparison,
    use_container_width=True
)

with st.expander("Comparison Metrics Guide"):
    st.markdown(
        """
        **Average Price** – Average property price.

        **Crime Score** – Relative crime performance score.

        **Affordability Score** – Housing affordability measure.

        **Growth Score** – Property market growth potential.

        **Investment Score** – Overall investment attractiveness.

        **Housing Intelligence Index** – Composite housing intelligence metric.

        **Area Rank** – National ranking among analysed LSOAs.
        """
    )

st.divider()

# =====================================================
# RADAR CHART
# =====================================================

st.subheader(
    "Performance Comparison"
)

categories = [
    "Crime Score",
    "Affordability",
    "Growth",
    "Investment",
    "Housing Intelligence"
]

area1_values = [
    area1_df["crime_score"],
    area1_df["affordability_score"],
    area1_df["growth_score"],
    area1_df["investment_score"],
    area1_df["housing_intelligence_index"]
]

area2_values = [
    area2_df["crime_score"],
    area2_df["affordability_score"],
    area2_df["growth_score"],
    area2_df["investment_score"],
    area2_df["housing_intelligence_index"]
]

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=area1_values,
        theta=categories,
        fill="toself",
        name=area_1
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=area2_values,
        theta=categories,
        fill="toself",
        name=area_2
    )
)

fig.update_layout(
    template="plotly_dark",
    height=600,
    polar=dict(
        radialaxis=dict(
            visible=True
        )
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# QUICK SUMMARY
# =====================================================

st.subheader(
    "Quick Summary"
)

winner_count = {
    area_1: 0,
    area_2: 0
}

metrics = [
    (
        "housing_intelligence_index",
        True
    ),
    (
        "investment_score",
        True
    ),
    (
        "growth_score",
        True
    ),
    (
        "affordability_score",
        True
    ),
    (
        "crime_score",
        False
    )
]

for metric, higher_is_better in metrics:

    if higher_is_better:

        if area1_df[metric] > area2_df[metric]:
            winner_count[area_1] += 1
        else:
            winner_count[area_2] += 1

    else:

        if area1_df[metric] < area2_df[metric]:
            winner_count[area_1] += 1
        else:
            winner_count[area_2] += 1

winner = max(
    winner_count,
    key=winner_count.get
)

st.success(
    f"""
Overall Winner: {winner}

Comparison Score

{area_1}: {winner_count[area_1]}

{area_2}: {winner_count[area_2]}
"""
)