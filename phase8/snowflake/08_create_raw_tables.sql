-- =====================================================
-- UK Housing Intelligence Platform
-- Phase 8
-- RAW Layer Table Creation
-- =====================================================

USE DATABASE UK_HOUSING_DW;
USE SCHEMA RAW;

-- Crime Scores

CREATE OR REPLACE TABLE CRIME_SCORES
USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
        INFER_SCHEMA(
            LOCATION => '@GOLD_STAGE/crime_scores/',
            FILE_FORMAT => 'PARQUET_FILE_FORMAT'
        )
    )
);

-- Growth Scores

CREATE OR REPLACE TABLE GROWTH_SCORES
USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
        INFER_SCHEMA(
            LOCATION => '@GOLD_STAGE/growth_scores/',
            FILE_FORMAT => 'PARQUET_FILE_FORMAT'
        )
    )
);

-- Healthcare Intelligence

CREATE OR REPLACE TABLE HEALTHCARE_INTELLIGENCE
USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
        INFER_SCHEMA(
            LOCATION => '@GOLD_STAGE/healthcare_intelligence/',
            FILE_FORMAT => 'PARQUET_FILE_FORMAT'
        )
    )
);

-- Housing Intelligence

CREATE OR REPLACE TABLE HOUSING_INTELLIGENCE
USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
        INFER_SCHEMA(
            LOCATION => '@GOLD_STAGE/housing_index/',
            FILE_FORMAT => 'PARQUET_FILE_FORMAT'
        )
    )
);

-- Investment Scores

CREATE OR REPLACE TABLE INVESTMENT_SCORES
USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
        INFER_SCHEMA(
            LOCATION => '@GOLD_STAGE/investment_scores/',
            FILE_FORMAT => 'PARQUET_FILE_FORMAT'
        )
    )
);

-- Location Intelligence

CREATE OR REPLACE TABLE LOCATION_INTELLIGENCE
USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
        INFER_SCHEMA(
            LOCATION => '@GOLD_STAGE/location_intelligence/',
            FILE_FORMAT => 'PARQUET_FILE_FORMAT'
        )
    )
);

-- Opportunity Explorer

CREATE OR REPLACE TABLE OPPORTUNITY_EXPLORER
USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
        INFER_SCHEMA(
            LOCATION => '@GOLD_STAGE/opportunity_explorer/',
            FILE_FORMAT => 'PARQUET_FILE_FORMAT'
        )
    )
);

-- Rankings

CREATE OR REPLACE TABLE RANKINGS
USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
        INFER_SCHEMA(
            LOCATION => '@GOLD_STAGE/rankings/',
            FILE_FORMAT => 'PARQUET_FILE_FORMAT'
        )
    )
);

-- Regional Intelligence

CREATE OR REPLACE TABLE REGIONAL_INTELLIGENCE
USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
        INFER_SCHEMA(
            LOCATION => '@GOLD_STAGE/regional_intelligence/',
            FILE_FORMAT => 'PARQUET_FILE_FORMAT'
        )
    )
);

-- School Intelligence

CREATE OR REPLACE TABLE SCHOOL_INTELLIGENCE
USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
        INFER_SCHEMA(
            LOCATION => '@GOLD_STAGE/school_intelligence/',
            FILE_FORMAT => 'PARQUET_FILE_FORMAT'
        )
    )
);

-- Transport Intelligence

CREATE OR REPLACE TABLE TRANSPORT_INTELLIGENCE
USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
        INFER_SCHEMA(
            LOCATION => '@GOLD_STAGE/transport_intelligence/',
            FILE_FORMAT => 'PARQUET_FILE_FORMAT'
        )
    )
);

-- Historical Trends

CREATE OR REPLACE TABLE HISTORICAL_HOUSING_TRENDS
USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
        INFER_SCHEMA(
            LOCATION => '@GOLD_STAGE/trends/historical/',
            FILE_FORMAT => 'PARQUET_FILE_FORMAT'
        )
    )
);

-- Local Authority Trends

CREATE OR REPLACE TABLE LOCAL_AUTHORITY_TRENDS
USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
        INFER_SCHEMA(
            LOCATION => '@GOLD_STAGE/trends/local_authority/',
            FILE_FORMAT => 'PARQUET_FILE_FORMAT'
        )
    )
);

-- Regional Trends

CREATE OR REPLACE TABLE REGIONAL_HOUSING_TRENDS
USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
        INFER_SCHEMA(
            LOCATION => '@GOLD_STAGE/trends/regional/',
            FILE_FORMAT => 'PARQUET_FILE_FORMAT'
        )
    )
);

SHOW TABLES IN SCHEMA UK_HOUSING_DW.RAW;