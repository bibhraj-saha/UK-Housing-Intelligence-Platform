import subprocess

PROJECT_DIR = "/opt/project/phase8/dbt/uk_housing_dbt"

print("=" * 70)
print("UK Housing Intelligence Platform")
print("dbt Transformation Runner")
print("=" * 70)

print("\nRunning dbt debug...\n")

subprocess.run(
    [
        "dbt",
        "debug",
        "--project-dir",
        PROJECT_DIR,
    ],
    check=True,
)

print("\ndbt debug successful.\n")

print("Running dbt deps...\n")

subprocess.run(
    [
        "dbt",
        "deps",
        "--project-dir",
        PROJECT_DIR,
    ],
    check=True,
)

print("\nRunning dbt build...\n")

subprocess.run(
    [
        "dbt",
        "build",
        "--project-dir",
        PROJECT_DIR,
    ],
    check=True,
)

print("\nAll dbt models executed successfully.")