from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator

default_args = {
    "owner": "Bibhraj Saha",
    "depends_on_past": False,
    "retries": 2,
}

with DAG(
    dag_id="uk_housing_master_pipeline",
    description="Master orchestration pipeline for the UK Housing Intelligence Platform",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=[
        "uk-housing",
        "master",
        "orchestration",
        "snowflake",
        "dbt",
    ],
) as dag:

    start = EmptyOperator(
        task_id="start_pipeline"
    )

    health_check = EmptyOperator(
        task_id="health_check"
    )

    snowflake_validation = EmptyOperator(
        task_id="snowflake_validation"
    )

    snowflake_refresh = EmptyOperator(
        task_id="snowflake_refresh"
    )

    dbt_transformation = EmptyOperator(
        task_id="dbt_transformation"
    )

    data_quality_validation = EmptyOperator(
        task_id="data_quality_validation"
    )

    dashboard_refresh = EmptyOperator(
        task_id="dashboard_refresh"
    )

    end = EmptyOperator(
        task_id="pipeline_complete"
    )

    (
        start
        >> health_check
        >> snowflake_validation
        >> snowflake_refresh
        >> dbt_transformation
        >> data_quality_validation
        >> dashboard_refresh
        >> end
    )