import pandas as pd
from pathlib import Path

analytics_path = Path("data/analytics")

files = sorted(analytics_path.glob("*.parquet"))

for file in files:

    print("\n" + "=" * 100)
    print(f"FILE: {file.name}")
    print("=" * 100)

    df = pd.read_parquet(file)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumn Information")

    for col in df.columns:
        print(f"{col} ({df[col].dtype})")