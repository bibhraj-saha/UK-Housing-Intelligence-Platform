-- ============================================================================
-- UK Housing Intelligence Platform
-- Phase 10: Machine Learning Layer
-- Predictive Data-Gap Assessment
-- Temporal Coverage Audit
-- ============================================================================
--
-- Purpose:
--   Inspect warehouse metadata and candidate historical sources before
--   defining predictive targets or training datasets.
--
-- Safety:
--   Read-only queries.
--   No tables, schemas, views, or data are modified.
--
-- Important:
--   This file intentionally begins with metadata discovery because Phase 10
--   must not assume a warehouse table name, date column, or geography grain
--   without evidence.
-- ============================================================================


-- ----------------------------------------------------------------------------
-- 1. Inventory candidate tables
-- ----------------------------------------------------------------------------

SELECT
    table_catalog,
    table_schema,
    table_name,
    table_type,
    row_count,
    bytes,
    created,
    last_altered
FROM UK_HOUSING_DW.INFORMATION_SCHEMA.TABLES
ORDER BY
    table_schema,
    table_name;


-- ----------------------------------------------------------------------------
-- 2. Find candidate temporal columns
-- ----------------------------------------------------------------------------

SELECT
    table_schema,
    table_name,
    ordinal_position,
    column_name,
    data_type,
    is_nullable
FROM UK_HOUSING_DW.INFORMATION_SCHEMA.COLUMNS
WHERE
       LOWER(column_name) LIKE '%date%'
    OR LOWER(column_name) LIKE '%time%'
    OR LOWER(column_name) LIKE '%timestamp%'
    OR LOWER(column_name) LIKE '%month%'
    OR LOWER(column_name) LIKE '%year%'
    OR LOWER(column_name) LIKE '%period%'
ORDER BY
    table_schema,
    table_name,
    ordinal_position;


-- ----------------------------------------------------------------------------
-- 3. Find candidate geography columns
-- ----------------------------------------------------------------------------

SELECT
    table_schema,
    table_name,
    ordinal_position,
    column_name,
    data_type,
    is_nullable
FROM UK_HOUSING_DW.INFORMATION_SCHEMA.COLUMNS
WHERE
       LOWER(column_name) LIKE '%lsoa%'
    OR LOWER(column_name) LIKE '%msoa%'
    OR LOWER(column_name) LIKE '%postcode%'
    OR LOWER(column_name) LIKE '%district%'
    OR LOWER(column_name) LIKE '%authority%'
    OR LOWER(column_name) LIKE '%region%'
    OR LOWER(column_name) LIKE '%country%'
ORDER BY
    table_schema,
    table_name,
    ordinal_position;


-- ----------------------------------------------------------------------------
-- 4. Find candidate price columns
-- ----------------------------------------------------------------------------

SELECT
    table_schema,
    table_name,
    ordinal_position,
    column_name,
    data_type,
    is_nullable
FROM UK_HOUSING_DW.INFORMATION_SCHEMA.COLUMNS
WHERE
    LOWER(column_name) LIKE '%price%'
ORDER BY
    table_schema,
    table_name,
    ordinal_position;


-- ----------------------------------------------------------------------------
-- 5. Find candidate entity-time tables
-- ----------------------------------------------------------------------------
--
-- Interpretation:
--   This query identifies tables containing at least one geography-like column
--   and at least one temporal-like column.
--
--   A returned table is only a candidate. It does not prove repeated
--   observations or stable frequency.
-- ----------------------------------------------------------------------------

WITH geography_tables AS (
    SELECT DISTINCT
        table_schema,
        table_name
    FROM UK_HOUSING_DW.INFORMATION_SCHEMA.COLUMNS
    WHERE
           LOWER(column_name) LIKE '%lsoa%'
        OR LOWER(column_name) LIKE '%msoa%'
        OR LOWER(column_name) LIKE '%postcode%'
        OR LOWER(column_name) LIKE '%district%'
        OR LOWER(column_name) LIKE '%authority%'
        OR LOWER(column_name) LIKE '%region%'
        OR LOWER(column_name) LIKE '%country%'
),

temporal_tables AS (
    SELECT DISTINCT
        table_schema,
        table_name
    FROM UK_HOUSING_DW.INFORMATION_SCHEMA.COLUMNS
    WHERE
           LOWER(column_name) LIKE '%date%'
        OR LOWER(column_name) LIKE '%time%'
        OR LOWER(column_name) LIKE '%timestamp%'
        OR LOWER(column_name) LIKE '%month%'
        OR LOWER(column_name) LIKE '%year%'
        OR LOWER(column_name) LIKE '%period%'
)

SELECT
    g.table_schema,
    g.table_name
FROM geography_tables AS g
INNER JOIN temporal_tables AS t
    ON g.table_schema = t.table_schema
   AND g.table_name = t.table_name
ORDER BY
    g.table_schema,
    g.table_name;


-- ----------------------------------------------------------------------------
-- 6. Find candidate price-time tables
-- ----------------------------------------------------------------------------

WITH price_tables AS (
    SELECT DISTINCT
        table_schema,
        table_name
    FROM UK_HOUSING_DW.INFORMATION_SCHEMA.COLUMNS
    WHERE
        LOWER(column_name) LIKE '%price%'
),

temporal_tables AS (
    SELECT DISTINCT
        table_schema,
        table_name
    FROM UK_HOUSING_DW.INFORMATION_SCHEMA.COLUMNS
    WHERE
           LOWER(column_name) LIKE '%date%'
        OR LOWER(column_name) LIKE '%time%'
        OR LOWER(column_name) LIKE '%timestamp%'
        OR LOWER(column_name) LIKE '%month%'
        OR LOWER(column_name) LIKE '%year%'
        OR LOWER(column_name) LIKE '%period%'
)

SELECT
    p.table_schema,
    p.table_name
FROM price_tables AS p
INNER JOIN temporal_tables AS t
    ON p.table_schema = t.table_schema
   AND p.table_name = t.table_name
ORDER BY
    p.table_schema,
    p.table_name;


-- ============================================================================
-- MANUAL FOLLOW-UP TEMPLATE
-- ============================================================================
--
-- Do not run the following template until a real candidate table, geography
-- column, and temporal column have been identified from the metadata queries.
--
-- Replace:
--   <SCHEMA_NAME>
--   <TABLE_NAME>
--   <ENTITY_COLUMN>
--   <DATE_COLUMN>
--
-- Example analytical purpose:
--   Determine whether entities have sufficient repeated monthly history.
--
-- SELECT
--     <ENTITY_COLUMN> AS entity_id,
--     COUNT(DISTINCT DATE_TRUNC('MONTH', <DATE_COLUMN>)) AS month_count,
--     MIN(<DATE_COLUMN>) AS min_date,
--     MAX(<DATE_COLUMN>) AS max_date
-- FROM UK_HOUSING_DW.<SCHEMA_NAME>.<TABLE_NAME>
-- WHERE
--     <ENTITY_COLUMN> IS NOT NULL
--     AND <DATE_COLUMN> IS NOT NULL
-- GROUP BY
--     <ENTITY_COLUMN>
-- ORDER BY
--     month_count DESC;
--
-- ============================================================================