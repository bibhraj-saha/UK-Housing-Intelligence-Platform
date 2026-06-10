# Data Volume Assessment

## UK Land Registry Dataset

Files:

- pp-2023.csv
- pp-2024.csv
- pp-2025.csv
- pp-2026.csv

Assessment:

Current dataset volume is suitable for processing using Python and Pandas.

Rationale:

- Data fits comfortably on a single machine.
- No distributed processing required.
- Simpler development workflow.
- Easier debugging and maintenance.

Future Enhancement:

Evaluate migration to PySpark if:

- Additional years are added.
- Data volume grows significantly.
- Distributed processing becomes necessary.