-- =====================================================
-- UK Housing Intelligence Platform
-- Phase 8 - Snowflake Warehouse Creation
-- =====================================================

USE ROLE ACCOUNTADMIN;

CREATE WAREHOUSE IF NOT EXISTS COMPUTE_WH
WITH
WAREHOUSE_SIZE = 'XSMALL'
AUTO_SUSPEND = 60
AUTO_RESUME = TRUE
INITIALLY_SUSPENDED = TRUE
COMMENT = 'Warehouse for UK Housing Intelligence Platform';