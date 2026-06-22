-- =====================================================
-- UK Housing Intelligence Platform
-- Phase 8 - File Formats
-- =====================================================

USE ROLE ACCOUNTADMIN;

USE DATABASE UK_HOUSING_DW;

CREATE FILE FORMAT IF NOT EXISTS PARQUET_FILE_FORMAT
TYPE = PARQUET
COMMENT = 'Parquet format used for AWS S3 Gold Layer datasets';