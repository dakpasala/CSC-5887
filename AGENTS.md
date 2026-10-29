# CSC 5887 — Predicting Deadlift Performance

## Mission and scope

Build a reproducible research pipeline for Dakshesh Pasala, Kevin Beltran, and Dhanvi Ganti's final project. Predict a lifter's best successful competition deadlift from their squat, bench press, and personal/competition characteristics using OpenPowerlifting.

This is supervised regression within the same meet. It is not forecasting future strength gains, estimating a physiological maximum, recommending safe attempts, or diagnosing weaknesses. Predictions are references for comparing recorded performance among similar lifters.

Implement the pipeline, not just a notebook or a plan. Work in incremental, runnable milestones. Inspect any existing repository before changing it; preserve useful code and user changes. Resolve routine implementation choices autonomously and record assumptions. Do not invent dataset counts, results, citations, or successful test runs. If blocked by download/access, implement the rest with clearly labeled synthetic fixtures and report the specific blocker.

## Research questions

1. How accurately can competition deadlift be predicted from squat, bench, bodyweight, age, sex, and equipment?
2. Which feature groups improve prediction over simple baselines?
3. Do earlier competition results improve predictions on the same eligible test examples?
4. How does performance change on later competitions and on unseen federations/equipment categories?

## Source of truth

- Proposal: https://docs.google.com/document/d/1YimNspKupZ6xvUWPHU18sGuKJViZz0maEvuscEXxfnI
- Presentation: https://docs.google.com/presentation/d/1ZClUEf-Pcf6eBNUT5BeNYyyNqecK3uYa4StYi0GaZRM
- Official bulk data/documentation: https://openpowerlifting.gitlab.io/opl-csv/bulk-csv.html

This file is self-contained; connected Google Drive access is not necessary to begin. Read official dataset documentation before interpreting fields. Verify current download locations instead of guessing an archive URL. The proposal estimates around four million rows; actual counts must come from the downloaded snapshot.

## Implementation stack and repository layout

Use Python, pandas or Polars, Parquet, scikit-learn, LightGBM, PyTorch, matplotlib/seaborn, and pytest. Prefer CPU-friendly defaults; support CUDA for the MLP if available. No paid services, application UI, cloud deployment, or elaborate experiment platform is required.

Suggested structure (adapt to existing conventions):

```text
configs/                  # Versioned YAML experiment settings
src/deadlift_prediction/
  data.py                 # Download, snapshot metadata, validation, cleaning
  identity.py             # Lifter grouping and identity-quality audit
  features.py             # Feature allowlists, preprocessing, history
  splits.py               # Group, chronological, transfer protocols
  models.py               # Ratio, linear, LightGBM, MLP
  train.py
  evaluate.py
  reporting.py
tests/
data/raw/                 # Immutable downloaded snapshot; gitignored
data/processed/           # Parquet and split manifests; gitignored
artifacts/                # Saved models, predictions, metrics, plots; gitignored
reports/                  # Data audit, experiment table, interpretation
notebooks/                # Optional exploration using package functions
README.md
pyproject.toml
```

Expose documented CLI commands for download, prepare, train, evaluate, and summarize. A single smoke command should exercise the full pipeline on a small deterministic fixture. Keep substantial logic in importable modules rather than notebook cells. Pin or lock dependencies after confirming a working environment.

## Data preparation

1. Save the raw snapshot unchanged. Record source URL, retrieval date, checksum, schema, and raw row count. Do not repeatedly download a changing nightly dataset during experiments.
2. Retain Event == "SBD" and finite, strictly positive Best3SquatKg, Best3BenchKg, and Best3DeadliftKg. The target is Best3DeadliftKg in kilograms. Do not impute targets or failed lifts.
3. Parse Date, numerical measurements, and categorical values explicitly. Missing age must not cause all otherwise valid rows to be dropped. Document handling of missing bodyweight and invalid demographic values. Do not silently remove rare but plausible strong lifts.
4. Remove exact duplicate observations and audit potential repeated listings using documented meet identifiers/metadata where available. Never collapse distinct lifters solely because their performances match.
5. Report exclusions at each step, remaining rows, estimated unique lifters, date coverage, missingness, sex/equipment/federation distributions, and history-eligible counts.
6. Freeze cleaned row IDs and split manifests for fair model comparisons. Read only needed columns and use chunking/Parquet if necessary. Establish a working subset before attempting the full snapshot.

### Lifter identity

Inspect how the snapshot distinguishes same-name athletes, including any name suffixes. Names are not guaranteed perfect identifiers. Use documented canonical identities where available, preserve distinctions, and never fuzzy-merge automatically. Report unresolved identity limitations. Grouping errors can contaminate evaluation. Names and identity keys are for splitting/history lookup, never predictive features.

### Leakage prevention

Use explicit feature allowlists, not a blacklist-only strategy.

Allowed same-meet predictors: Best3SquatKg, Best3BenchKg, BodyweightKg, Age, Sex, Equipment; Federation only in a named configuration. Dates and identities support splitting/history and are not baseline predictors.

Never input current-meet Best3DeadliftKg, deadlift attempt columns, Best4DeadliftKg, TotalKg, Dots, Wilks, Glossbrenner, Goodlift, or any score/derived feature using the target. Exclude placement, final ranking, disqualification status, and other post-outcome fields from the baseline. Do not derive weight classes from the target or use meet aggregates containing test outcomes.

Fit imputers, scalers, categorical vocabularies, and other learned preprocessing only on each training partition. Handle unseen categories explicitly. Never use test labels for tuning, feature selection, early stopping, outlier decisions, or selecting a held-out group.

## Evaluation protocols

Keep protocols separate and name them in every output. Default choices below are implementation defaults, not claims from the proposal.

### A. Primary: unseen lifters

- Deterministic group split by canonical lifter identity, approximately 70/15/15 train/validation/test, seed 42.
- Every record for a lifter belongs to the same partition. Assert pairwise-disjoint lifter sets and row IDs.
- Check distribution balance and disclose material differences; never reshuffle to optimize test scores.
- Sample subsets by lifter before splitting or within frozen splits; do not allow a row sample to break grouping.

### B. Separate chronological evaluation

- Use non-overlapping meet-date intervals: earlier dates for training, intermediate for validation, later for testing. Choose boundaries using date coverage, not target performance, and record exact boundaries.
- A lifter may recur across periods. Clearly label this as future-meet evaluation, not unseen-person evaluation.
- Historical features are computed as of each target row, including for training rows. All history dates must be strictly earlier than the target date. Exclude same-day history when ordering is uncertain.

### C. Federation/equipment transfer

- Select sufficiently supported groups using counts only and record selection rules in advance.
- Exclude the selected category from both training and tuning. Evaluate on that group and report in-distribution comparison results from the same fitted model.
- For unseen-person transfer, remove all records of held-out test lifters from training/validation, even their records in other categories.
- Report test sizes and covariate differences. Equipment groups may have very different populations; do not interpret a score gap as a causal effect of equipment.
- An unseen category must map safely to an unknown encoding. Include a sensitivity comparison excluding the held-out categorical field, so transfer is not just a test of unsupported category encoding.

## Models

1. Ratio baseline: predict deadlift = r * squat. Fit r on training data separately by Sex using a documented objective, e.g. least squares through the origin. Provide a training-only pooled fallback for unseen/missing categories.
2. Linear regression: training-fitted numerical preprocessing and categorical one-hot encoding with unknown handling. A modest regularized variant is acceptable if documented and validation-selected.
3. LightGBM regression: modest parameter search and validation early stopping. Record the objective, categorical representation, best iteration, and settings.
4. Small multilayer perceptron: numerical/categorical inputs, scalar regression output; begin with hidden widths [128, 64], ReLU, optional dropout, Adam, and validation-based early stopping. Standardize numeric inputs, document target scaling if used, and convert predictions back to kilograms. Use MSE or MAE training loss consistently and explain the choice.

Keep the MLP results even if it loses. Compare identical splits, target rows, feature sets, and a reasonable documented tuning budget. Do not claim deep learning must outperform trees. Save fitted preprocessing alongside each model.

## Required experiments

### 1. Feature-group ablation

Freeze common target rows across stages so missingness does not change the evaluated population:

- A: squat only.
- B: squat + bench.
- C: B + bodyweight, age, sex.
- D: C + equipment.
- E: optional named extension adding federation; keep separate from the core ablation.

Report metrics and changes from simpler inputs. Improvements reflect predictive contribution, not causal effects or unique biological importance.

### 2. Previous-meet history

Start with previous eligible meet squat, bench, deadlift, days since that meet, and count of earlier meets. Use strictly earlier dates and verify sorting/shift logic. Previous deadlift is allowed; current/future deadlift is not.

On primary grouped splits, test lifters' earlier records may be queried as input context, but none of those lifters' rows may fit model parameters or preprocessing. Label this distinction clearly. All training examples must also use past-only history.

Evaluate no-history and history-enabled models on exactly the same history-eligible test rows. Report how many lifters/rows qualify. Also compare a last-deadlift baseline on that subset to show whether the learned model adds value beyond repeating the previous result. Handle no-history lifters separately rather than fabricating previous performance.

### 3. Temporal and group transfer

Run protocols B and C after the core pipeline is validated. Report distribution sizes and uncertainty. Do not expand scope to generative modeling or future strength forecasting without an explicit request.

## Metrics and analysis

- Primary: MAE in kilograms.
- Secondary: MAPE in percent and R-squared. MAPE uses strictly positive targets; R-squared may be negative. Return undefined with an explanation for groups too small or with constant targets.
- Report test rows and unique lifters with every table. Overall row-weighted scores are primary; include lifter-averaged MAE as a useful sensitivity analysis because prolific competitors contribute many rows.
- Break down errors by Sex, fixed BodyweightKg bins, and history availability. Define bins before seeing test results; include sample counts and flag sparse groups.
- Plot actual vs predicted, residuals vs actual deadlift, model MAE comparison, ablation improvements, and subgroup errors.
- Use paired comparisons on the same rows. Where feasible, estimate confidence intervals by bootstrapping whole lifters, not individual correlated meet rows. Repeat final MLP runs across a few recorded seeds if runtime permits.
- Validation results may guide decisions. Freeze configurations before final test reporting. Do not repeatedly optimize using test scores.
- Never infer undertraining, injury risk, safe lifting capacity, or causal effects from residuals.

## Reproducibility and artifacts

Every run should save config, dataset checksum, split ID, seed, package versions, model/preprocessor, tuning summary, validation metrics, test metrics when finalized, runtime, and per-example predictions with row/group IDs. Use pseudonymous keys in shared reports; do not publish names unnecessarily.

Save tidy CSV/JSON experiment tables and publication-readable figures. Keep raw data, large models, and environment files out of Git. Track small configs, code, and report summaries. Record what was actually run versus what remains planned.

## Required correctness checks

Write focused tests for research-validity risks:

- Target/post-outcome columns cannot enter model features.
- Nonpositive targets/lifts are excluded and missing age is handled.
- Lifter split sets are disjoint; chronological dates are ordered.
- History never includes current/future or ambiguous same-day meets. Test ties explicitly.
- Transfer groups and held-out identities do not leak into fitting/tuning.
- Learned preprocessing uses training data only; unseen categories predict successfully.
- MAE/MAPE/R-squared match hand-calculated examples, including undefined R-squared cases.
- Models serialize/reload with consistent predictions, including preprocessing.
- Synthetic smoke pipeline trains, predicts, and writes metrics. Synthetic scores are never presented as research findings.

## Build order and completion criteria

1. Inspect repository/environment; establish package, configs, README, and a short implementation checklist.
2. Implement ingestion, snapshot metadata, cleaning, identity audit, and data-quality report.
3. Implement and test frozen splits, allowed features, preprocessing, and past-only history.
4. Run ratio and linear baselines end to end on a manageable subset.
5. Add LightGBM and MLP; verify outputs and save artifacts.
6. Run the feature ablation and paired history experiment.
7. Run chronological and transfer evaluations with the same documented safeguards.
8. Generate summary tables/figures and a short report answering each research question, including limitations and failed hypotheses.

Start implementing immediately. Do not stop after scaffolding if the environment permits execution. Scale gradually; never launch an unbounded search. If full runs exceed resources, finish a reproducible subset run, label its scope, and provide exact commands for larger runs.

Final handoff: working commands from a clean environment, checks run, data counts, completed experiments, measured results, saved artifact paths, and remaining blockers. Do not claim experiments are complete merely because their code exists.

## Related work supplied in the proposal

Verify bibliographic metadata and contents before making specific claims; the descriptions below are pointers, not verified findings:

- Future performance prediction: https://sportsmedicine-open.springeropen.com/articles/10.1186/s40798-025-00903-z
- Medina-Romero et al., Applying Data Mining and Machine Learning Techniques to Predict Powerlifting Results (2023): https://doi.org/10.3390/engproc2023039020
- Attempt selection/success study: https://doras.dcu.ie/31743/1/Darraghetal_2025_PredictingPowerliftingSuccess.pdf
- Ke et al., LightGBM: A Highly Efficient Gradient Boosting Decision Tree (2017).

Our distinction is same-meet cross-lift prediction with controlled feature comparisons, past-only history, and generalization tests. Do not claim novelty beyond what a literature review supports.
