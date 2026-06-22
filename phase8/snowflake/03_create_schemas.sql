-- =====================================================
-- UK Housing Intelligence Platform
-- Phase 8 - Schema Creation
-- =====================================================

USE ROLE ACCOUNTADMIN;

USE DATABASE UK_HOUSING_DW;

CREATE SCHEMA IF NOT EXISTS RAW;
CREATE SCHEMA IF NOT EXISTS STAGING;
CREATE SCHEMA IF NOT EXISTS DIMENSIONS;
CREATE SCHEMA IF NOT EXISTS MARTS;
CREATE SCHEMA IF NOT EXISTS ANALYTICS;