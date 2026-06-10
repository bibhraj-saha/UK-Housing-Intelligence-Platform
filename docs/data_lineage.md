# Data Lineage

## Property Transaction Data Flow

UK Land Registry
↓
Raw CSV Files
↓
AWS S3 Raw Zone
↓
Snowflake Raw Tables
↓
dbt Staging Models
↓
Fact Tables
↓
Power BI Dashboard
↓
Machine Learning Models

---

## Lineage Objectives

- Track source-to-report flow
- Enable auditability
- Improve transparency
- Support troubleshooting