Phase 10 — Price & Growth Prediction

Purpose

This component implements reproducible supervised machine-learning workflows for:

* future house-price prediction
* future house-price-growth prediction

The implementation consumes the point-in-time training datasets created by the Feature Store & Training Datasets step.

Design Principles

The modelling layer follows these principles:

1. chronological train, validation and test splits
2. no random reshuffling of temporal observations
3. model selection using validation performance
4. final evaluation using the untouched test split
5. baseline-first model development
6. reproducible model configuration
7. persisted model artifacts
8. machine-readable evaluation reports
9. prediction outputs suitable for later dashboard integration

Models

Each predictive task evaluates a controlled candidate set.

Mean Baseline

Predicts the mean target value observed in the training data.

This provides a minimum reference point for determining whether trained models add predictive value.

Naive Historical-Feature Baseline

Uses a historical feature directly as the prediction.

For price prediction, the baseline uses the prior price feature.

For growth prediction, the baseline uses prior observed price growth.

Linear Regression

Provides a transparent linear benchmark.

Ridge Regression

Provides a regularized linear model to reduce sensitivity to correlated features.

Random Forest Regression

Provides a nonlinear tree-based model capable of learning interactions between engineered housing-market features.

Model Selection

Models are trained using the training split and compared using the validation split.

The primary selection metric is:

* validation RMSE

The model with the lowest validation RMSE is selected.

The selected model is then evaluated once against the untouched test split.

Evaluation Metrics

The framework records:

* MAE
* RMSE
* R²
* evaluated row count

MAE measures average absolute prediction error.

RMSE penalizes larger prediction errors more heavily.

R² measures explained variance relative to a constant baseline.

Leakage Prevention

The modelling workflow consumes the feature and target definitions produced by the prior Feature Store & Training Datasets step.

Future targets are not included as model features.

Chronological splits are preserved.

Model selection uses validation data rather than test data.

The final test split is reserved for final generalization evaluation.

Artifacts

Best models are persisted under:

* phase10/artifacts/models/price_prediction
* phase10/artifacts/models/growth_prediction

Each task produces:

* best_model.joblib
* model_manifest.json

Evaluation Reports

Machine-readable reports are written under:

* phase10/reports/model_evaluation/price_prediction
* phase10/reports/model_evaluation/growth_prediction

Each task produces:

* evaluation_report.json

Prediction Outputs

Test-set predictions are written under:

* phase10/data/predictions/price_prediction
* phase10/data/predictions/growth_prediction

Each task produces:

* test_predictions.parquet

These outputs preserve available identifiers such as LSOA and timestamp and include:

* actual value
* predicted value
* residual
* absolute error
* selected model name

The prediction layer is designed for later integration with the Streamlit application and the wider automated data platform.

Current Scope Boundary

This component covers supervised price and growth prediction only.

It does not implement:

* area recommendation
* investment opportunity prediction
* time-series forecasting
* production model monitoring
* model registry lifecycle automation
* final dashboard integration

Those capabilities belong to later Phase 10 roadmap steps.