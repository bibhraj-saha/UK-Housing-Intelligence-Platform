import streamlit as st


def apply_global_styling():

    st.markdown(
        """
        <style>

        .main {
            padding-top: 1rem;
        }

        /* KPI Cards */

        div[data-testid="stMetric"] {

            background-color: #111827;

            border: 1px solid rgba(
                255,
                255,
                255,
                0.08
            );

            padding: 18px;

            border-radius: 16px;

            box-shadow:
                0px 4px 20px
                rgba(0,0,0,0.35);
        }

        /* Tables */

        .stDataFrame {

            border-radius: 16px;
        }

        /* Sidebar */

        section[data-testid="stSidebar"] {

            background-color: #111827;
        }

        h1, h2, h3 {

            font-weight: 700;
        }

        </style>
        """,
        unsafe_allow_html=True
    )