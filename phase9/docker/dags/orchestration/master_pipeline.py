from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

default_args = {
    "owner": "Bibhraj Saha",
    "retries": 2,
}

with DAG(
    dag_id="uk_housing_master_pipeline",
    description="Master orchestration pipeline for the UK Housing Intelligence Platform",
    start_date=datetime(2026, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    default_args=default_args,
    tags=["master", "orchestration", "phase9"],
) as dag:

    start = EmptyOperator(
        task_id="start_pipeline"
    )

    trigger_health_check = TriggerDagRunOperator(
        task_id="trigger_health_check",
        trigger_dag_id="uk_housing_platform_healthcheck",
        wait_for_completion=True,
        poke_interval=10,
    )

    trigger_snowflake_validation = TriggerDagRunOperator(
        task_id="trigger_snowflake_validation",
        trigger_dag_id="snowflake_validation",
        wait_for_completion=True,
        poke_interval=10,
    )

    trigger_data_quality_validation = TriggerDagRunOperator(
        task_id="trigger_data_quality_validation",
        trigger_dag_id="data_quality_validation",
        wait_for_completion=True,
        poke_interval=10,
    )

    finish = EmptyOperator(
        task_id="pipeline_completed"
    )

    (
        start
        >> trigger_health_check
        >> trigger_snowflake_validation
        >> trigger_data_quality_validation
        >> finish
    )