import streamlit as st

from utils.data_loader import load_housing_data

from utils.styles import apply_global_styling


st.set_page_config(
    page_title="UK Housing Intelligence Platform",
    page_icon="🏠",
    layout="wide"
)

apply_global_styling()

st.sidebar.markdown(
    "## 🏠 UK Housing Intelligence"
)

df = load_housing_data()

st.title("🏠 UK Housing Intelligence Platform")

st.caption(
    """
    Housing Intelligence • Investment Analytics • Crime Analysis • Area Rankings
    """
)

st.markdown(
    """
    ### Housing Intelligence & Investment Analytics

    Analyze UK housing intelligence,
    investment opportunities,
    affordability,
    crime,
    and area rankings.
    """
)

avg_price = round(df["average_price"].mean(), 0)

avg_crime = round(df["average_crime"].mean(), 2)

avg_investment = round(
    df["investment_score"].mean(),
    2
)

avg_index = round(
    df["housing_intelligence_index"].mean(),
    2
)

st.subheader("Platform Highlights")

col1, col2 = st.columns(2)

with col1:
    st.info(
        f"""
        Analysing **{len(df):,} UK LSOAs**
        using housing intelligence,
        investment, affordability,
        crime and deprivation metrics.
        """
    )

with col2:
    st.success(
        """
        Interactive dashboards available:

        • Housing Intelligence

        • Investment Opportunities

        • Crime & Affordability

        • Area Comparison
        """
    )

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average House Price",
    f"£{avg_price:,.0f}"
)

col2.metric(
    "Average Crime",
    avg_crime
)

col3.metric(
    "Investment Score",
    avg_investment
)

col4.metric(
    "Housing Index",
    avg_index
)

st.divider()

st.subheader("Platform Overview")

st.write(
    """
    This platform provides housing intelligence,
    investment opportunity analysis,
    crime scoring,
    affordability scoring,
    and area ranking insights across UK LSOAs.
    """
)