# CSC 5887 — Predicting Competition Deadlift

Dakshesh Pasala, Kevin Beltran, Dhanvi Ganti.

Same-meet supervised regression: predict a lifter's best successful competition deadlift
(`Best3DeadliftKg`) from that meet's squat, bench, and lifter characteristics, using the
OpenPowerlifting bulk CSV. Predictions are reference values for comparing recorded
performance among similar lifters. They are **not** forecasts, physiological maxima,
attempt recommendations, or diagnoses. See `AGENTS.md` for the full research spec.

## Setup (clean environment)

```bash
python3.13 -m venv .venv
.venv/bin/pip install -r requirements.lock   # pinned versions that were run
.venv/bin/pip install -e ".[dev]" --no-deps
```

## Commands

```bash
deadlift smoke                                   # synthetic end-to-end fixture (scores are NOT findings)
deadlift download                                # fetch + register snapshot once (sha256, schema, row count)
deadlift prepare   --config configs/subset.yaml  # clean, identity audit, past-only history, frozen splits
deadlift train     --config configs/subset.yaml  # all planned runs; finished runs are skipped
deadlift ensemble  --config configs/subset.yaml  # LightGBM+MLP blends (weight chosen on validation)
deadlift evaluate  --config configs/subset.yaml  # validation-only tables (development)
deadlift summarize --config configs/subset.yaml
deadlift evaluate  --config configs/default.yaml --final   # test scoring, only after configs are frozen
deadlift summarize --config configs/default.yaml --final
pytest -q
```

`train` accepts `--experiment {ablation,history,chrono,transfer,capacity,history_rich,quantile}` (repeatable) and `--only <substring>`.

## Layout

| Path | Contents |
|---|---|
| `configs/` | `default.yaml` (full snapshot), `subset.yaml` (10% of lifters), `smoke.yaml` (synthetic) |
| `src/deadlift_prediction/` | `data` (download/clean), `identity`, `features` (allowlists, preprocessing, history), `splits`, `models`, `metrics`, `train`, `evaluate`, `reporting`, `cli` |
| `tests/` | research-validity checks (leakage, splits, history ties, metrics, serialization, smoke) |
| `data/raw/` | immutable snapshot zip + `snapshot.json` (gitignored) |
| `data/processed/<config>/` | `clean.parquet`, `manifest.parquet` (frozen row IDs and splits), `splits.json`, `data_summary.json` (gitignored) |
| `artifacts/<config>/runs/<run_id>/` | `model.pkl` (model + fitted preprocessor), `predictions.parquet`, `meta.json` (gitignored) |
| `reports/<config>/` | data audit, results tables, figures (tracked) |

## Implementation notes

- **Identity**: OpenPowerlifting disambiguates same-name lifters with a `#n` suffix in `Name`. The full Name is the
  canonical identity, hashed to a pseudonymous `lifter_key`. Nothing is fuzzy-merged.
- **Process isolation**: on macOS the LightGBM and PyTorch wheels bundle conflicting OpenMP runtimes, which
  deadlock or segfault when both load in one process. `train` runs tree/linear models and MLP models in separate
  spawned processes.
- **Development vs final scoring**: `evaluate` scores validation partitions unless `--final` is given.

## Status

- [x] Package, configs, CLI, synthetic smoke pipeline, tests
- [x] Snapshot registered: `openpowerlifting-2026-10-24-0fc10dd9.zip`, 4,054,260 data rows
- [x] Subset (10% lifters): prepare + all 65 runs trained; validation-only tables in `reports/subset10/`
- [x] Full-snapshot experiments: 73 runs + 6 capacity-check + 3 career-history follow-up runs + 3 ensembles + 4 quantile-range runs; validation then frozen test scoring
- [x] Final report: [`reports/REPORT.md`](reports/REPORT.md) (tables in `reports/full/`)
