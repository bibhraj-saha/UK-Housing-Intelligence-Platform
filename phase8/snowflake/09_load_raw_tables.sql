-- =====================================================
-- UK Housing Intelligence Platform
-- Phase 8
-- Load All RAW Tables
-- =====================================================

USE DATABASE UK_HOUSING_DW;
USE SCHEMA RAW;

---------------------------------------------------------
-- CRIME SCORES
---------------------------------------------------------

COPY INTO CRIME_SCORES
FROM @GOLD_STAGE/crime_scores/
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

---------------------------------------------------------
-- GROWTH SCORES
---------------------------------------------------------

COPY INTO GROWTH_SCORES
FROM @GOLD_STAGE/growth_scores/
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

---------------------------------------------------------
-- HEALTHCARE INTELLIGENCE
---------------------------------------------------------

COPY INTO HEALTHCARE_INTELLIGENCE
FROM @GOLD_STAGE/healthcare_intelligence/
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

---------------------------------------------------------
-- HOUSING INTELLIGENCE
---------------------------------------------------------

COPY INTO HOUSING_INTELLIGENCE
FROM @GOLD_STAGE/housing_index/
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

---------------------------------------------------------
-- INVESTMENT SCORES
---------------------------------------------------------

COPY INTO INVESTMENT_SCORES
FROM @GOLD_STAGE/investment_scores/
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

---------------------------------------------------------
-- LOCATION INTELLIGENCE
---------------------------------------------------------

COPY INTO LOCATION_INTELLIGENCE
FROM @GOLD_STAGE/location_intelligence/
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

---------------------------------------------------------
-- OPPORTUNITY EXPLORER
---------------------------------------------------------

COPY INTO OPPORTUNITY_EXPLORER
FROM @GOLD_STAGE/opportunity_explorer/
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

---------------------------------------------------------
-- RANKINGS
---------------------------------------------------------

COPY INTO RANKINGS
FROM @GOLD_STAGE/rankings/
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

---------------------------------------------------------
-- REGIONAL INTELLIGENCE
---------------------------------------------------------

COPY INTO REGIONAL_INTELLIGENCE
FROM @GOLD_STAGE/regional_intelligence/
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

---------------------------------------------------------
-- SCHOOL INTELLIGENCE
---------------------------------------------------------

COPY INTO SCHOOL_INTELLIGENCE
FROM @GOLD_STAGE/school_intelligence/
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

---------------------------------------------------------
-- TRANSPORT INTELLIGENCE
---------------------------------------------------------

COPY INTO TRANSPORT_INTELLIGENCE
FROM @GOLD_STAGE/transport_intelligence/
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

---------------------------------------------------------
-- HISTORICAL HOUSING TRENDS
---------------------------------------------------------

COPY INTO HISTORICAL_HOUSING_TRENDS
FROM @GOLD_STAGE/trends/historical/
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

---------------------------------------------------------
-- LOCAL AUTHORITY TRENDS
---------------------------------------------------------

COPY INTO LOCAL_AUTHORITY_TRENDS
FROM @GOLD_STAGE/trends/local_authority/
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

---------------------------------------------------------
-- REGIONAL HOUSING TRENDS
---------------------------------------------------------

COPY INTO REGIONAL_HOUSING_TRENDS
FROM @GOLD_STAGE/trends/regional/
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;