import pandas as pd
import snowflake.connector

conn = snowflake.connector.connect(
    user="BIBHRAJSAHA",
    password="IntoTheWild@123",
    account="UGLGPMY-FW39691",
    warehouse="COMPUTE_WH",
    database="UK_HOUSING_DW",
    schema="MARTS",
    role="ACCOUNTADMIN",
)


def load_housing_data():

    query = """
    SELECT *
    FROM MART_AREA_PROFILE
    """

    df = pd.read_sql(query, conn)

    # Convert Snowflake column names to lowercase
    df.columns = df.columns.str.lower()

    return df