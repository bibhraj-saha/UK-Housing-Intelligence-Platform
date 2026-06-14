import streamlit as st
import pandas as pd

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

st.title("⚖️ Area Comparison")

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

st.subheader("Comparison Results")

st.dataframe(
    comparison,
    use_container_width=True
)

# =====================================================
# WINNER SUMMARY
# =====================================================

st.subheader("Quick Summary")

if (
    area1_df["housing_intelligence_index"]
    >
    area2_df["housing_intelligence_index"]
):
    st.success(
        f"{area_1} has the higher Housing Intelligence Index."
    )
else:
    st.success(
        f"{area_2} has the higher Housing Intelligence Index."
    )