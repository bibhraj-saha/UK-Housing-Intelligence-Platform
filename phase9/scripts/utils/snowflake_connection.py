from airflow.hooks.base import BaseHook
import snowflake.connector


def get_snowflake_connection():
    """
    Returns an authenticated Snowflake connection
    using the Airflow Connection:
    snowflake_default
    """

    conn = BaseHook.get_connection("snowflake_default")

    return snowflake.connector.connect(
        account=conn.extra_dejson["account"],
        user=conn.login,
        password=conn.password,
        warehouse=conn.extra_dejson["warehouse"],
        database=conn.extra_dejson["database"],
        schema=conn.schema,
        role=conn.extra_dejson["role"],
    )