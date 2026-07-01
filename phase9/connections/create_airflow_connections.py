import subprocess

print("=" * 70)
print("UK Housing Intelligence Platform")
print("Airflow Connection Setup")
print("=" * 70)

connections = [
    [
        "snowflake_default",
        "snowflake",
        "UGLGPMY-FW39691",
        "BIBHRAJSAHA",
        "IntoTheWild@123",
        "COMPUTE_WH",
        "UK_HOUSING_DW",
        "RAW",
        "ACCOUNTADMIN",
    ]
]

for (
    conn_id,
    conn_type,
    account,
    username,
    password,
    warehouse,
    database,
    schema,
    role,
) in connections:

    subprocess.run(
        [
            "airflow",
            "connections",
            "delete",
            conn_id,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    subprocess.run(
        [
            "airflow",
            "connections",
            "add",
            conn_id,
            "--conn-type",
            conn_type,
            "--conn-login",
            username,
            "--conn-password",
            password,
            "--conn-extra",
            (
                "{"
                f"\"account\":\"{account}\","
                f"\"warehouse\":\"{warehouse}\","
                f"\"database\":\"{database}\","
                f"\"schema\":\"{schema}\","
                f"\"role\":\"{role}\""
                "}"
            ),
        ],
        check=True,
    )

print()
print("Airflow connections successfully created.")