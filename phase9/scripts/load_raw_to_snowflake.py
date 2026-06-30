import snowflake.connector
from pathlib import Path

print("=" * 70)
print("UK Housing Intelligence Platform")
print("RAW Data Loader")
print("=" * 70)

conn = snowflake.connector.connect(
    user="BIBHRAJSAHA",
    password="IntoTheWild@123",
    account="UGLGPMY-FW39691",
    warehouse="COMPUTE_WH",
    database="UK_HOUSING_DW",
    schema="RAW",
    role="ACCOUNTADMIN",
)

cursor = conn.cursor()

sql_file = (
    Path(__file__)
    .resolve()
    .parents[2]
    / "phase8"
    / "snowflake"
    / "09_load_raw_tables.sql"
)

print(f"\nExecuting SQL file:\n{sql_file}\n")

with open(sql_file, "r") as file:
    sql = file.read()

commands = [
    command.strip()
    for command in sql.split(";")
    if command.strip()
]

for command in commands:
    print("-" * 70)
    print(command)
    cursor.execute(command)

print("\nAll RAW tables loaded successfully.")

cursor.close()
conn.close()

print("\nSnowflake connection closed.")