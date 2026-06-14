import streamlit as st


def create_filters(df):

    st.sidebar.header("Dashboard Filters")

    # ==========================================
    # AREA RANK FILTER
    # ==========================================

    rank_min = int(
        df["area_rank"].min()
    )

    rank_max = int(
        df["area_rank"].max()
    )

    rank_range = st.sidebar.slider(
        "Area Rank Range",
        rank_min,
        rank_max,
        (rank_min, rank_max)
    )

    # ==========================================
    # INVESTMENT SCORE FILTER
    # ==========================================

    inv_min = float(
        df["investment_score"].min()
    )

    inv_max = float(
        df["investment_score"].max()
    )

    investment_range = st.sidebar.slider(
        "Investment Score Range",
        round(inv_min, 2),
        round(inv_max, 2),
        (
            round(inv_min, 2),
            round(inv_max, 2)
        )
    )

    # ==========================================
    # HOUSING INDEX FILTER
    # ==========================================

    index_min = float(
        df["housing_intelligence_index"].min()
    )

    index_max = float(
        df["housing_intelligence_index"].max()
    )

    housing_range = st.sidebar.slider(
        "Housing Index Range",
        round(index_min, 2),
        round(index_max, 2),
        (
            round(index_min, 2),
            round(index_max, 2)
        )
    )

    # ==========================================
    # TOP N
    # ==========================================

    top_n = st.sidebar.selectbox(
        "Top N Areas",
        [10, 20, 50, 100],
        index=1
    )

    return (
        rank_range,
        investment_range,
        housing_range,
        top_n
    )