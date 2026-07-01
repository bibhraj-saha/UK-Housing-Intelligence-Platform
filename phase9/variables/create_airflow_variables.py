import subprocess

print("=" * 70)
print("UK Housing Intelligence Platform")
print("Airflow Variable Setup")
print("=" * 70)

variables = {

    "SNOWFLAKE_DATABASE": "UK_HOUSING_DW",

    "SNOWFLAKE_SCHEMA": "RAW",

    "SNOWFLAKE_WAREHOUSE": "COMPUTE_WH",

    "DBT_PROJECT_DIR": "/opt/project/phase8/dbt/uk_housing_dbt",

    "RAW_SQL_FILE": "/opt/project/phase8/snowflake/09_load_raw_tables.sql",

    "DASHBOARD_DATASET": "/opt/project/data/analytics/housing_intelligence.parquet"

}

for key, value in variables.items():

    subprocess.run(
        [
            "airflow",
            "variables",
            "set",
            key,
            value
        ],
        check=True
    )

print()
print("Airflow Variables successfully created.")