-- =====================================================
-- UK Housing Intelligence Platform
-- Phase 8
-- AWS S3 Storage Integration
-- =====================================================

USE ROLE ACCOUNTADMIN;

CREATE OR REPLACE STORAGE INTEGRATION UK_HOUSING_S3_INT
TYPE = EXTERNAL_STAGE
STORAGE_PROVIDER = S3
STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::883627150629:role/UKHousingSnowflakeS3Role'
ENABLED = TRUE
STORAGE_ALLOWED_LOCATIONS = (
    's3://uk-housing-intelligence-platform-datalake-883627150629/gold/'
);

DESC INTEGRATION UK_HOUSING_S3_INT;