Phase 10 Predictive Data-Gap Assessment

1. Purpose

The Predictive Data-Gap Assessment determines whether the existing UK Housing Intelligence Platform data estate contains sufficient historical, geographic, and domain structure to support the locked Phase 10 machine-learning tasks.

The assessment is completed before prediction contracts, target engineering, feature-store implementation, or model training.

2. Relationship to the ML Readiness Audit

The Phase 10 ML Readiness Audit identifies whether relevant signals appear to exist.

The Predictive Data-Gap Assessment performs a deeper structural analysis.

The distinction is:

ML Readiness Audit
        |
        v
Do relevant signals exist?
        |
        v
Predictive Data-Gap Assessment
        |
        v
Are those signals historically deep,
repeated, granular, and structurally
suitable for predictive modelling?

3. Assessment Questions

The assessment investigates:

* available feature domains
* temporal coverage
* approximate historical depth
* candidate time frequencies
* geography identifiers
* primary geography candidates
* repeated entity-period observations
* periods per entity
* candidate prediction horizons
* price signals
* growth signals
* investment signals
* derived analytical target risks
* missing required domains
* missing recommended domains
* future target-definition gaps

4. Candidate Prediction Horizons

The initial assessment evaluates structural feasibility for:

* 3 months
* 6 months
* 12 months
* 24 months

These horizons are candidates only.

A horizon is not approved for modelling merely because sufficient global date range exists.

Final horizon selection must also validate:

* entity-level historical depth
* target availability
* point-in-time correctness
* training-window size
* validation-window size
* test-window size
* business usefulness

5. Candidate Geography Hierarchy

The initial geography priority order is:

1. LSOA
2. MSOA
3. postcode
4. local authority
5. district
6. region
7. country

This priority order is a discovery heuristic.

The final canonical ML entity will be defined separately.

6. Why LSOA Is a Strong Candidate

The existing analytical platform already uses LSOA-level intelligence.

LSOA offers advantages for:

* local area intelligence
* affordability comparison
* crime analysis
* recommendation
* area-level growth modelling
* geographic feature aggregation

However, LSOA-level monthly modelling may be sparse because some areas may have limited property transactions in individual months.

Therefore the project must measure transaction and temporal density before locking the modelling grain.

7. Transaction-Level Versus Area-Period Modelling

7.1 Transaction-Level Modelling

A transaction-level price model could use one row per property transaction.

Potential advantages:

* large observation count
* direct price target
* property-level variation

Potential limitations:

* property attributes may be incomplete
* repeated sales are uneven
* area-level crime and earnings features require point-in-time joins
* future price prediction semantics must be explicit

7.2 Area-Period Modelling

An area-period model could use one row per geography and time period.

Example:

lsoa_code | observation_month | median_price | crime_rate | earnings | ...

Potential advantages:

* natural fit for growth prediction
* natural fit for forecasting
* easier temporal feature engineering
* clearer point-in-time semantics

Potential limitations:

* sparse monthly transactions
* unstable small-sample area prices
* aggregation can reduce property-level information

The final grain must be selected from measured evidence.

8. Temporal Coverage Requirements

The initial configured minimum historical depth is:

Task	Minimum Approximate History
Price Prediction	24 months
Growth Prediction	24 months
Forecasting	36 months
Investment Opportunity Prediction	24 months

These thresholds are engineering policy defaults and may be revised based on actual historical coverage and target design.

9. Repeated Entity Coverage

Global date range is insufficient.

For example, a dataset may span ten years while individual LSOAs appear only once.

Therefore the assessment measures candidate entity-period structure including:

* unique entities
* unique entity-month pairs
* entities with multiple periods
* repeated entity ratio
* minimum periods per entity
* median periods per entity
* maximum periods per entity
* entities with at least 12 periods
* entities with at least 24 periods
* entities with at least 36 periods

10. Feature Domains

The assessment detects candidate domains including:

* price
* crime
* affordability
* deprivation
* geography
* temporal
* housing
* growth
* investment

Domain detection is heuristic.

A detected domain does not prove:

* temporal correctness
* feature usefulness
* absence of leakage
* sufficient historical depth

11. Derived Analytical Target Risks

Existing analytical outputs may contain:

* growth scores
* investment scores
* housing intelligence indices
* rankings
* percentiles

These fields are not automatically valid predictive labels.

A contemporaneous analytical score may encode current information rather than an observed future outcome.

Before such a field is used for modelling, the project must establish:

* source lineage
* calculation formula
* feature dependencies
* timestamp semantics
* whether future information is included
* whether the field duplicates the intended target

12. Price Prediction Data Requirements

Price prediction requires:

* price signal
* geography signal
* temporal signal
* formal future price target
* prediction timestamp
* forecast horizon
* point-in-time features
* temporal evaluation

Recommended enrichment domains include:

* crime
* affordability
* deprivation
* housing characteristics

13. Growth Prediction Data Requirements

Growth prediction requires:

* historical price observations
* stable geography
* temporal ordering
* future growth horizon
* future growth target
* point-in-time features
* temporal evaluation

Existing growth_score fields must not automatically become targets.

14. Area Recommendation Data Requirements

Area recommendation requires:

* stable area entities
* comparable area features
* preference semantics
* scaling policy
* ranking policy
* offline evaluation

Potential domains include:

* price
* crime
* affordability
* deprivation
* housing
* growth
* investment

15. Forecasting Data Requirements

Forecasting requires:

* repeated observations
* stable entity identity
* stable or explicitly handled time frequency
* sufficient historical depth
* forecast horizon
* lag policy
* rolling-window policy
* backtesting

A date column alone does not prove forecasting readiness.

16. Investment Opportunity Prediction Requirements

Investment opportunity prediction requires an observable future outcome.

An existing investment_score is not automatically a valid label.

Potential future outcome definitions may later involve combinations of:

* future price appreciation
* downside risk
* affordability
* liquidity
* transaction activity
* risk-adjusted growth

The final definition belongs in the prediction-contract and target-engineering stages.

17. Local Profiling Versus Warehouse Validation

The local assessment supports:

* rapid discovery
* schema inspection
* temporal heuristics
* entity-period heuristics
* domain detection

Large datasets may be sampled locally.

Therefore local results must distinguish:

* full profiling
* sampled profiling

Full warehouse validation will use Snowflake for canonical historical sources.

18. Step 2 Outputs

Primary implementation files:

* phase10/config/predictive_data_gap.yml
* phase10/src/uk_housing_ml/audit/data_gap.py
* phase10/scripts/run_predictive_data_gap_assessment.py
* phase10/tests/unit/test_data_gap.py
* phase10/sql/02_temporal_coverage_audit.sql
* phase10/sql/03_candidate_feature_audit.sql

Generated evidence:

* phase10/reports/audits/predictive_data_gap_assessment.json
* phase10/reports/audits/predictive_data_gap_assessment.md

19. Decision Principle

The Predictive Data-Gap Assessment does not authorize model training.

Its purpose is to determine what the current platform can support and what must be engineered or acquired next.

The next architecture stage must use the measured evidence to define formal prediction contracts.