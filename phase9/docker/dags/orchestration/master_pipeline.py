from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.trigger_rule import TriggerRule

default_args = {
    "owner": "Bibhraj Saha",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(minutes=15),
    "execution_timeout": timedelta(minutes=60),
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

    load_raw_data = BashOperator(
        task_id="load_raw_data",
        bash_command="""
        python /opt/project/phase9/scripts/load_raw_to_snowflake.py
        """,
    )

    run_dbt_models = BashOperator(
        task_id="run_dbt_models",
        bash_command="""
        python /opt/project/phase9/scripts/run_dbt_models.py
        """,
    )

    run_dbt_tests = BashOperator(
        task_id="run_dbt_tests",
        bash_command="""
        python /opt/project/phase9/scripts/run_dbt_tests.py
        """,
    )

    refresh_dashboard = BashOperator(
        task_id="refresh_dashboard",
        bash_command="""
        python /opt/project/phase9/scripts/refresh_dashboard.py
        """,
    )

    notify_success = BashOperator(
        task_id="notify_success",
        bash_command="""
        python /opt/project/phase9/scripts/success_notification.py
        """,
        trigger_rule=TriggerRule.ALL_SUCCESS,
    )

    notify_failure = BashOperator(
        task_id="notify_failure",
        bash_command="""
        python /opt/project/phase9/scripts/failure_notification.py
        """,
        trigger_rule=TriggerRule.ONE_FAILED,
    )

    finish = EmptyOperator(
        task_id="pipeline_completed"
    )

    (
        start
        >> trigger_health_check
        >> trigger_snowflake_validation
        >> trigger_data_quality_validation
        >> load_raw_data
        >> run_dbt_models
        >> run_dbt_tests
        >> refresh_dashboard
        >> notify_success
        >> finish
    )

    trigger_health_check >> notify_failure
    trigger_snowflake_validation >> notify_failure
    trigger_data_quality_validation >> notify_failure
    load_raw_data >> notify_failure
    run_dbt_models >> notify_failure
    run_dbt_tests >> notify_failure
    refresh_dashboard >> notify_failure