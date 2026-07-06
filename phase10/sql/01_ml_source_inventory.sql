-- ============================================================================
-- UK Housing Intelligence Platform
-- Phase 10: Machine Learning Layer
-- ML Source Inventory
-- ============================================================================
--
-- Purpose:
--   Inventory candidate Snowflake tables and views that may supply Phase 10
--   machine-learning features, targets, entities, or historical observations.
--
-- Safety:
--   Read-only metadata queries.
--   No tables, views, schemas, or data are modified.
-- ============================================================================


-- ----------------------------------------------------------------------------
-- 1. Inventory all tables in the project database
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
-- 2. Inventory all columns
-- ----------------------------------------------------------------------------

SELECT
    table_catalog,
    table_schema,
    table_name,
    ordinal_position,
    column_name,
    data_type,
    is_nullable
FROM UK_HOUSING_DW.INFORMATION_SCHEMA.COLUMNS
ORDER BY
    table_schema,
    table_name,
    ordinal_position;


-- ----------------------------------------------------------------------------
-- 3. Find candidate temporal columns
-- ----------------------------------------------------------------------------

SELECT
    table_schema,
    table_name,
    column_name,
    data_type
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
    column_name;


-- ----------------------------------------------------------------------------
-- 4. Find candidate geography columns
-- ----------------------------------------------------------------------------

SELECT
    table_schema,
    table_name,
    column_name,
    data_type
FROM UK_HOUSING_DW.INFORMATION_SCHEMA.COLUMNS
WHERE
       LOWER(column_name) LIKE '%lsoa%'
    OR LOWER(column_name) LIKE '%msoa%'
    OR LOWER(column_name) LIKE '%postcode%'
    OR LOWER(column_name) LIKE '%district%'
    OR LOWER(column_name) LIKE '%authority%'
    OR LOWER(column_name) LIKE '%region%'
    OR LOWER(column_name) LIKE '%country%'
    OR LOWER(column_name) LIKE '%latitude%'
    OR LOWER(column_name) LIKE '%longitude%'
ORDER BY
    table_schema,
    table_name,
    column_name;


-- ----------------------------------------------------------------------------
-- 5. Find candidate price, growth, and investment signals
-- ----------------------------------------------------------------------------

SELECT
    table_schema,
    table_name,
    column_name,
    data_type
FROM UK_HOUSING_DW.INFORMATION_SCHEMA.COLUMNS
WHERE
       LOWER(column_name) LIKE '%price%'
    OR LOWER(column_name) LIKE '%growth%'
    OR LOWER(column_name) LIKE '%investment%'
    OR LOWER(column_name) LIKE '%target%'
    OR LOWER(column_name) LIKE '%forecast%'
ORDER BY
    table_schema,
    table_name,
    column_name;


-- ----------------------------------------------------------------------------
-- 6. Find derived score, index, and ranking columns requiring lineage review
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
ORDER BY
    table_schema,
    table_name,
    column_name;