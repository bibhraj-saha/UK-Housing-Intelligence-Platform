import subprocess

print("=" * 70)
print("UK Housing Intelligence Platform")
print("dbt Test Runner")
print("=" * 70)

PROJECT_DIR = "/opt/project/phase8/dbt/uk_housing_dbt"

PROFILE_DIR = "/home/airflow/.dbt"

print("\nRunning dbt tests...\n")

subprocess.run(
    [
        "dbt",
        "test",
        "--project-dir",
        PROJECT_DIR,
        "--profiles-dir",
        PROFILE_DIR,
    ],
    check=True,
)

print("\nAll dbt tests passed successfully.")