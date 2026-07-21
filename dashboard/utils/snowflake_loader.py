import pandas as pd
import snowflake.connector
import streamlit as st


def get_connection():
    """
    Create a brand-new Snowflake connection.

    A new connection is created for every request to avoid
    expired authentication tokens on Streamlit Cloud.
    """

    return snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"],
        role=st.secrets["snowflake"]["role"],
    )


@st.cache_data(ttl=3600)
def load_housing_data():
    """
    Load the housing mart from Snowflake.

    The result is cached for one hour to minimise
    database queries while ensuring a fresh
    authenticated connection whenever the cache expires.
    """

    query = """
    SELECT *
    FROM MART_AREA_PROFILE
    """

    conn = get_connection()

    try:

        df = pd.read_sql(query, conn)

        df.columns = df.columns.str.lower()

        return df

    finally:

        conn.close()