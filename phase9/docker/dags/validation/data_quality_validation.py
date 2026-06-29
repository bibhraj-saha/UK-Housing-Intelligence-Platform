from datetime import datetime
from pathlib import Path

from airflow.sdk import DAG, task

# ---------------------------------------------------------------------
# Project Paths
# ---------------------------------------------------------------------

PROJECT_ROOT = Path("/opt/project")

ANALYTICS_DIRECTORY = PROJECT_ROOT / "data" / "analytics"

REPORT_DIRECTORY = PROJECT_ROOT / "phase9" / "data_quality" / "reports"


def discover_datasets():
    """
    Automatically discover every parquet dataset
    inside the analytics directory.
    """

    return sorted(
        ANALYTICS_DIRECTORY.glob("*.parquet")
    )


with DAG(
    dag_id="data_quality_validation",
    description="Production Data Quality Validation",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=[
        "phase9",
        "production",
        "validation",
    ],
) as dag:

    @task
    def discover_files():

        datasets = discover_datasets()

        print("=" * 70)
        print("Dataset Discovery")
        print("=" * 70)

        if not datasets:
            raise FileNotFoundError(
                "No parquet datasets found."
            )

        print(f"Datasets Found : {len(datasets)}\n")

        for dataset in datasets:
            print(dataset.name)

    @task
    def validate_file_sizes():

        datasets = discover_datasets()

        print("=" * 70)
        print("File Size Validation")
        print("=" * 70)

        for dataset in datasets:

            size_mb = dataset.stat().st_size / (1024 * 1024)

            print(f"{dataset.name:<45} {size_mb:10.2f} MB")

            if size_mb <= 0:
                raise ValueError(
                    f"{dataset.name} is empty."
                )

        print("\nAll datasets contain data.")

    @task
    def validate_dataset_readability():

        datasets = discover_datasets()

        print("=" * 70)
        print("Readability Validation")
        print("=" * 70)

        for dataset in datasets:

            with open(dataset, "rb") as f:
                f.read(32)

            print(f"{dataset.name} : OK")

    @task
    def generate_validation_report():

        REPORT_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        datasets = discover_datasets()

        report = (
            REPORT_DIRECTORY
            / f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        with open(report, "w") as file:

            file.write("UK Housing Intelligence Platform\n")
            file.write("Phase 9 Data Quality Validation\n")
            file.write(f"Execution Time : {datetime.now()}\n")
            file.write(f"Datasets Validated : {len(datasets)}\n\n")

            for dataset in datasets:

                size_mb = dataset.stat().st_size / (1024 * 1024)

                file.write(
                    f"{dataset.name:<45} "
                    f"{size_mb:.2f} MB\n"
                )

            file.write("\nValidation Status : SUCCESS\n")

        print(f"Validation report generated:\n{report}")

    (
        discover_files()
        >> validate_file_sizes()
        >> validate_dataset_readability()
        >> generate_validation_report()
    )