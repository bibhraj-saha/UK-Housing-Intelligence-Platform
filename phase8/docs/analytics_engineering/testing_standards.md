Testing Standards

Required Tests

Dimensions

* unique
* not_null

Facts

* not_null
* relationships

Analytics Marts

* not_null for KPI fields

⸻

Deployment Requirement

All dbt tests must pass before deployment.

⸻

Validation Requirement

Every new model requires:

* row count validation
* schema validation
* lineage verification