-- =====================================================
-- UK Housing Intelligence Platform
-- Phase 8
-- External Stage Creation
-- =====================================================

USE ROLE ACCOUNTADMIN;

USE DATABASE UK_HOUSING_DW;

USE SCHEMA RAW;

CREATE OR REPLACE STAGE GOLD_STAGE
URL='s3://uk-housing-intelligence-platform-datalake-883627150629/gold/'
STORAGE_INTEGRATION = UK_HOUSING_S3_INT
FILE_FORMAT = PARQUET_FILE_FORMAT;

SHOW STAGES;