import pandas as pd
import snowflake.connector
import streamlit as st


def get_connection():

    return snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"],
        role=st.secrets["snowflake"]["role"],
    )


def load_housing_data():

    conn = get_connection()

    query = """
    SELECT *
    FROM MART_AREA_PROFILE
    """

    df = pd.read_sql(query, conn)

    df.columns = df.columns.str.lower()

    conn.close()

    return df