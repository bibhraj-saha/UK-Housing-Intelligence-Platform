-- =====================================================
-- Phase 8
-- Validate Snowflake Schema Inference
-- =====================================================

USE DATABASE UK_HOUSING_DW;
USE SCHEMA RAW;

SELECT *
FROM TABLE(
    INFER_SCHEMA(
        LOCATION => '@GOLD_STAGE/crime_scores/',
        FILE_FORMAT => 'PARQUET_FILE_FORMAT'
    )
);