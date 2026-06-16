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

col1, col2 = st.columns(2)

with col1:
    st.info(
        f"""
### Platform Coverage

• Analysing **{len(df):,} UK LSOAs**

• **11 Interactive Dashboards**

• Housing Intelligence & Investment Analytics

• Crime, Affordability & Income Intelligence

• Schools, Healthcare & Transport Accessibility

• Historical Market Trends & Regional Analytics

• Coverage Across England & Wales
        """
    )

with col2:
    st.success(
        """
### Interactive Dashboards

**Core Intelligence**

• Housing Intelligence

• Investment Opportunities

• Crime & Affordability

• Area Comparison

**Regional & Geographic**

• Regional Intelligence

• Housing Intelligence Map

• Opportunity Explorer

**Advanced Analytics**

• Income Intelligence

• Market Trends

• Location Intelligence
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

with st.expander("KPI Guide"):
    st.markdown(
        """
        **Average House Price** – Mean property price across all analysed UK LSOAs.

        **Average Crime** – Average crime level across analysed areas.

        **Investment Score** – Composite score measuring investment attractiveness.

        **Housing Index** – Overall housing intelligence score combining multiple housing market indicators.
        """
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