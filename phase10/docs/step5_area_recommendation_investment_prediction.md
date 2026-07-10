Phase 10 Step 5 — Area Recommendation & Investment Prediction

Purpose

Step 5 adds two decision-oriented ML capabilities to the UK Housing Intelligence Platform:

1. Area Recommendation
2. Investment Opportunity Prediction

These capabilities reuse the feature store and point-in-time training datasets created in Step 3.

Area Recommendation

The area recommendation workflow ranks LSOAs using the latest available feature snapshot for each area.

The initial ranking model combines:

* three-month price growth
* three-month rolling mean price
* transaction count
* three-month rolling transaction activity

Each feature is converted into a percentile-based component score. Directionality is explicit: some features reward higher values, while price level is treated inversely as an affordability-oriented proxy.

The final recommendation score is a configurable weighted combination of component scores.

This workflow is intentionally transparent and deterministic. It is a ranking model rather than a supervised prediction model because the current platform does not yet contain a validated historical user-preference label or recommendation outcome target.

Investment Opportunity Prediction

The investment workflow is a supervised binary classification problem.

The target is derived from the already point-in-time constructed future growth target:

* positive class: future price growth is greater than the configured threshold
* negative class: future price growth is less than or equal to the configured threshold

The initial threshold is zero.

Models compared are:

* majority-class baseline
* logistic regression
* random forest classifier

Model selection is performed using validation ROC AUC. The selected model is then retrained on the combined training and validation data and evaluated once on the chronological test split.

Reported metrics include:

* accuracy
* precision
* recall
* F1 score
* ROC AUC

Leakage Controls

The investment target is derived only from the future target already constructed by the Step 3 training-dataset workflow.

Future growth is used as the label and is not included in the feature list.

The model features remain historical or contemporaneously available engineered inputs.

Outputs

Area recommendation outputs:

* ranked LSOA recommendation Parquet dataset
* recommendation manifest JSON report

Investment prediction outputs:

* persisted best model artifact
* model manifest
* evaluation report
* test prediction Parquet dataset with opportunity probabilities

Current Limitation

The area recommendation score is not a personalized recommender system. It is a configurable area-ranking model.

The investment opportunity label is a future-growth proxy and should not be interpreted as financial advice or as a complete measure of investment return.

Future iterations can incorporate:

* rental yield
* transaction costs
* liquidity
* volatility
* deprivation
* crime
* schools
* transport accessibility
* user-selected preference weights
* calibrated probability thresholds
* richer historical coverage

This limitation is retained explicitly to keep the Phase 10 implementation technically honest and reproducible.