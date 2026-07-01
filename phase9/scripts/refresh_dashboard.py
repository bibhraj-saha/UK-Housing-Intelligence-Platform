import pandas as pd
import snowflake.connector
from pathlib import Path

print("=" * 70)
print("UK Housing Intelligence Platform")
print("Dashboard Refresh")
print("=" * 70)

conn = snowflake.connector.connect(
    user="BIBHRAJSAHA",
    password="IntoTheWild@123",
    account="UGLGPMY-FW39691",
    warehouse="COMPUTE_WH",
    database="UK_HOUSING_DW",
    schema="MARTS",
    role="ACCOUNTADMIN",
)

query = """
SELECT *
FROM MART_AREA_PROFILE
ORDER BY AREA_RANK
"""

print("\nReading MART_AREA_PROFILE...")

df = pd.read_sql(query, conn)

conn.close()

output_path = (
    Path(__file__)
    .resolve()
    .parents[2]
    / "data"
    / "analytics"
    / "housing_intelligence.parquet"
)

print(f"\nWriting dashboard dataset:\n{output_path}")

df.columns = [c.lower() for c in df.columns]

df.to_parquet(
    output_path,
    index=False,
)

print(f"\nRows exported : {len(df):,}")
print(f"Columns       : {len(df.columns)}")

print("\nDashboard refresh completed.")