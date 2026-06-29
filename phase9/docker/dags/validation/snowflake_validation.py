from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pathlib import Path


def validate_project_structure():
    print("=" * 60)
    print("SNOWFLAKE VALIDATION")
    print("=" * 60)

    analytics_path = Path("/opt/project/data/analytics")

    if analytics_path.exists():
        print("Analytics folder found.")
    else:
        raise FileNotFoundError("Analytics folder not found.")

    parquet_files = list(analytics_path.glob("*.parquet"))

    print(f"Found {len(parquet_files)} parquet files.")

    if len(parquet_files) == 0:
        raise Exception("No parquet files found.")

    print("Validation completed successfully.")


default_args = {
    "owner": "Bibhraj Saha",
}


with DAG(
    dag_id="snowflake_validation",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["snowflake", "validation", "phase9"],
) as dag:

    validate = PythonOperator(
        task_id="validate_snowflake_inputs",
        python_callable=validate_project_structure,
    )

    validate