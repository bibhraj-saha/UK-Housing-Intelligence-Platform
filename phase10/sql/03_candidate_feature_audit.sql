-- ============================================================================
-- UK Housing Intelligence Platform
-- Phase 10: Machine Learning Layer
-- Predictive Data-Gap Assessment
-- Candidate Feature Audit
-- ============================================================================
--
-- Purpose:
--   Discover candidate feature domains and identify analytical columns that
--   require lineage and leakage review before model training.
--
-- Safety:
--   Read-only metadata queries.
-- ============================================================================


-- ----------------------------------------------------------------------------
-- 1. Candidate price and transaction features
-- ----------------------------------------------------------------------------

SELECT
    table_schema,
    table_name,
    column_name,
    data_type
FROM UK_HOUSING_DW.INFORMATION_SCHEMA.COLUMNS
WHERE
       LOWER(column_name) LIKE '%price%'
    OR LOWER(column_name) LIKE '%transaction%'
ORDER BY
    table_schema,
    table_name,
    column_name;


-- ----------------------------------------------------------------------------
-- 2. Candidate crime features
-- ----------------------------------------------------------------------------

SELECT
    table_schema,
    table_name,
    column_name,
    data_type
FROM UK_HOUSING_DW.INFORMATION_SCHEMA.COLUMNS
WHERE
       LOWER(column_name) LIKE '%crime%'
    OR LOWER(column_name) LIKE '%offence%'
    OR LOWER(column_name) LIKE '%offense%'
ORDER BY
    table_schema,
    table_name,
    column_name;


-- ----------------------------------------------------------------------------
-- 3. Candidate affordability and earnings features
-- ----------------------------------------------------------------------------

SELECT
    table_schema,
    table_name,
    column_name,
    data_type
FROM UK_HOUSING_DW.INFORMATION_SCHEMA.COLUMNS
WHERE
       LOWER(column_name) LIKE '%affordability%'
    OR LOWER(column_name) LIKE '%income%'
    OR LOWER(column_name) LIKE '%earning%'
    OR LOWER(column_name) LIKE '%salary%'
    OR LOWER(column_name) LIKE '%wage%'
ORDER BY
    table_schema,
    table_name,
    column_name;


-- ----------------------------------------------------------------------------
-- 4. Candidate deprivation features
-- ----------------------------------------------------------------------------

SELECT
    table_schema,
    table_name,
    column_name,
    data_type
FROM UK_HOUSING_DW.INFORMATION_SCHEMA.COLUMNS
WHERE
       LOWER(column_name) LIKE '%deprivation%'
    OR LOWER(column_name) LIKE '%imd%'
ORDER BY
    table_schema,
    table_name,
    column_name;


-- ----------------------------------------------------------------------------
-- 5. Candidate housing and property features
-- ----------------------------------------------------------------------------

SELECT
    table_schema,
    table_name,
    column_name,
    data_type
FROM UK_HOUSING_DW.INFORMATION_SCHEMA.COLUMNS
WHERE
       LOWER(column_name) LIKE '%property%'
    OR LOWER(column_name) LIKE '%house%'
    OR LOWER(column_name) LIKE '%flat%'
    OR LOWER(column_name) LIKE '%tenure%'
    OR LOWER(column_name) LIKE '%dwelling%'
ORDER BY
    table_schema,
    table_name,
    column_name;


-- ----------------------------------------------------------------------------
-- 6. Candidate growth and investment columns
-- ----------------------------------------------------------------------------

SELECT
    table_schema,
    table_name,
    column_name,
    data_type
FROM UK_HOUSING_DW.INFORMATION_SCHEMA.COLUMNS
WHERE
       LOWER(column_name) LIKE '%growth%'
    OR LOWER(column_name) LIKE '%investment%'
ORDER BY
    table_schema,
    table_name,
    column_name;


-- ----------------------------------------------------------------------------
-- 7. Derived analytical columns requiring lineage review
-- ----------------------------------------------------------------------------
--
-- Important:
--   These columns are not automatically invalid.
--   They must be traced to source calculations before being used as:
--     - model features
--     - predictive targets
--     - recommendation labels
--
-- ----------------------------------------------------------------------------

SELECT
    table_schema,
    table_name,
    column_name,
    data_type
FROM UK_HOUSING_DW.INFORMATION_SCHEMA.COLUMNS
WHERE
       LOWER(column_name) LIKE '%score%'
    OR LOWER(column_name) LIKE '%index%'
    OR LOWER(column_name) LIKE '%rank%'
    OR LOWER(column_name) LIKE '%ranking%'
    OR LOWER(column_name) LIKE '%percentile%'
ORDER BY
    table_schema,
    table_name,
    column_name;


-- ----------------------------------------------------------------------------
-- 8. Explicit future, prediction, target, and label risk columns
-- ----------------------------------------------------------------------------

SELECT
    table_schema,
    table_name,
    column_name,
    data_type
FROM UK_HOUSING_DW.INFORMATION_SCHEMA.COLUMNS
WHERE
       LOWER(column_name) LIKE '%future%'
    OR LOWER(column_name) LIKE '%target%'
    OR LOWER(column_name) LIKE '%label%'
    OR LOWER(column_name) LIKE '%prediction%'
    OR LOWER(column_name) LIKE '%predicted%'
    OR LOWER(column_name) LIKE '%forecast%'
ORDER BY
    table_schema,
    table_name,
    column_name;