from datetime import datetime

from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeCheckOperator

default_args = {
    "owner": "Bibhraj Saha",
    "retries": 2,
}

with DAG(
    dag_id="snowflake_validation",
    description="Validate Snowflake environment before running warehouse pipelines",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["snowflake", "validation", "phase9"],
) as dag:

    warehouse_check = SnowflakeCheckOperator(
        task_id="verify_warehouse",
        snowflake_conn_id="snowflake_default",
        sql="""
        SELECT CURRENT_WAREHOUSE() IS NOT NULL;
        """,
    )

    database_check = SnowflakeCheckOperator(
        task_id="verify_database",
        snowflake_conn_id="snowflake_default",
        sql="""
        SELECT CURRENT_DATABASE() = 'UK_HOUSING_DW';
        """,
    )

    schema_check = SnowflakeCheckOperator(
        task_id="verify_schema",
        snowflake_conn_id="snowflake_default",
        sql="""
        SELECT CURRENT_SCHEMA() = 'RAW';
        """,
    )

    table_check = SnowflakeCheckOperator(
        task_id="verify_raw_tables",
        snowflake_conn_id="snowflake_default",
        sql="""
        SELECT COUNT(*)
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA='RAW';
        """,
    )

    warehouse_check >> database_check >> schema_check >> table_check