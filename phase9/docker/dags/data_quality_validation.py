from datetime import datetime
from pathlib import Path

from airflow.sdk import DAG, task

# ---------------------------------------------------------------------
# Project Paths
# ---------------------------------------------------------------------

PROJECT_ROOT = Path("/opt/project")

DATASETS = [
    PROJECT_ROOT / "data" / "analytics" / "housing_intelligence.parquet",
    PROJECT_ROOT / "data" / "analytics" / "area_analytics_base.parquet",
    PROJECT_ROOT / "data" / "analytics" / "rankings.parquet",
    PROJECT_ROOT / "data" / "analytics" / "regional_intelligence.parquet",
]

REPORT_DIRECTORY = PROJECT_ROOT / "phase9" / "data_quality" / "reports"


with DAG(
    dag_id="data_quality_validation",
    description="Validate analytical datasets before orchestration",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["phase9", "data-quality", "validation"],
) as dag:

    @task
    def verify_required_files():

        print("=" * 70)
        print("Checking required datasets...")
        print("=" * 70)

        missing = []

        for dataset in DATASETS:

            if dataset.exists():
                print(f"FOUND : {dataset.name}")
            else:
                print(f"MISSING : {dataset.name}")
                missing.append(dataset.name)

        if missing:
            raise FileNotFoundError(
                f"Missing datasets: {', '.join(missing)}"
            )

        print("\nAll required datasets exist.")

    @task
    def validate_file_sizes():

        print("=" * 70)
        print("Checking file sizes...")
        print("=" * 70)

        for dataset in DATASETS:

            size_mb = dataset.stat().st_size / (1024 * 1024)

            print(f"{dataset.name} : {size_mb:.2f} MB")

            if size_mb <= 0:
                raise ValueError(
                    f"{dataset.name} appears empty."
                )

        print("\nAll dataset sizes look valid.")

    @task
    def validate_dataset_readability():

        print("=" * 70)
        print("Checking dataset readability...")
        print("=" * 70)

        for dataset in DATASETS:

            with open(dataset, "rb") as f:
                f.read(16)

            print(f"{dataset.name} : Read successful")

        print("\nAll datasets are readable.")

    @task
    def generate_validation_report():

        REPORT_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        report_file = (
            REPORT_DIRECTORY
            / f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        with open(report_file, "w") as report:

            report.write("UK Housing Intelligence Platform\n")
            report.write("Phase 9 Data Quality Validation\n")
            report.write(f"Execution Time: {datetime.now()}\n")
            report.write("\n")

            report.write("Validation Result: SUCCESS\n")

        print(f"Validation report created:\n{report_file}")

    (
        verify_required_files()
        >> validate_file_sizes()
        >> validate_dataset_readability()
        >> generate_validation_report()
    )