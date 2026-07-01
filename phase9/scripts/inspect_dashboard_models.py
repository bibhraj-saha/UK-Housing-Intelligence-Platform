import snowflake.connector
import pandas as pd

print("=" * 80)
print("UK Housing Intelligence Platform")
print("Dashboard Model Inspector")
print("=" * 80)

conn = snowflake.connector.connect(
    user="BIBHRAJSAHA",
    password="IntoTheWild@123",
    account="UGLGPMY-FW39691",
    warehouse="COMPUTE_WH",
    database="UK_HOUSING_DW",
    schema="MARTS",
    role="ACCOUNTADMIN",
)

MODELS = [
    "FCT_HOUSING_INTELLIGENCE",
    "MART_AREA_PROFILE",
    "MART_AREA_RANKINGS",
    "MART_AFFORDABILITY_ANALYTICS",
    "MART_INVESTMENT_OPPORTUNITIES",
    "MART_GROWTH_ANALYTICS",
]

for model in MODELS:

    print("\n" + "=" * 80)
    print(model)
    print("=" * 80)

    df = pd.read_sql(f"SELECT * FROM {model} LIMIT 5", conn)

    print("\nColumns:\n")

    for col in df.columns:
        print(col)

    print("\nShape:", df.shape)

conn.close()