from pathlib import Path
import sys

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from dashboard.utils.snowflake_loader import (
    load_area_profile,
    load_rankings,
)

print("=" * 70)
print("Dashboard Snowflake Validation")
print("=" * 70)

area = load_area_profile()

print(f"MART_AREA_PROFILE rows : {len(area)}")

ranking = load_rankings()

print(f"MART_AREA_RANKINGS rows : {len(ranking)}")

print()

print("Dashboard successfully connected to Snowflake.")