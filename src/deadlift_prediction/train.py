"""Experiment plan and training runner.

Every run fits on its protocol's training partition, tunes/early-stops on its
validation partition, and saves predictions for all evaluation partitions.
Metrics are computed later by `evaluate` from saved predictions.
"""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

from .config import artifacts_dir, config_hash, package_versions, processed_dir, read_json, write_json
from .data import TARGET
from .features import CORE_ABLATION
from .metrics import summarize
from .models import build_model
from .prepare import load_prepared
from .splits import assert_disjoint, transfer_split


@dataclass
class RunSpec:
    experiment: str          # ablation | history | chrono | transfer | capacity | history_rich | quantile | expanded | objective
    protocol: str            # A | B | C:<field>=<value>
    feature_set: str
    model: str
    seed: int = 42
    history_only: bool = False   # restrict train/val/eval rows to history-eligible
    tune_from: str | None = None  # reuse LightGBM params selected in this run
    tags: dict = field(default_factory=dict)
    variant: str | None = None    # named capacity variant (appended to run_id)
    overrides: dict = field(default_factory=dict)  # model params overriding the config

    @property
    def run_id(self) -> str:
        proto = self.protocol.replace(":", "-").replace("=", "-").replace(" ", "_")
        parts = [self.experiment, proto, self.feature_set.replace("+", "-"), self.model]
        if self.history_only:
            parts.append("histrows")
        if self.variant:
            parts.append(self.variant)
        if self.model == "mlp":
            parts.append(f"s{self.seed}")
        return "__".join(parts)


# (feature set, history_only, base run whose tree settings are reused)
OBJECTIVE_TARGETS = [
    ("X_all+anyhist", False, "expanded__A__X_all-anyhist__lightgbm"),
    ("X_all+history_rich+anyhist", True, "expanded__A__X_all-history_rich-anyhist__lightgbm__histrows"),
]


def plan(cfg: dict, splits_info: dict) -> list[RunSpec]:
    seeds = cfg["models"]["mlp"]["seeds"]
    runs: list[RunSpec] = []

    # 1. Feature ablation (protocol A). Ratio baseline once (uses squat + Sex).
    runs.append(RunSpec("ablation", "A", "A_squat", "ratio"))
    for fs in CORE_ABLATION + ["E_plus_federation"]:
        runs += [RunSpec("ablation", "A", fs, "linear"), RunSpec("ablation", "A", fs, "lightgbm")]
        runs += [RunSpec("ablation", "A", fs, "mlp", seed=s) for s in (seeds if fs == "D_plus_equipment" else seeds[:1])]

    # 2. Previous-meet history (protocol A, history-eligible rows only for fitting the history model).
    runs.append(RunSpec("history", "A", "D_plus_equipment", "last_deadlift", history_only=True))
    for m in ["linear", "lightgbm"]:
        runs.append(RunSpec("history", "A", "D_plus_equipment", m, history_only=True))
        runs.append(RunSpec("history", "A", "D_plus_equipment+history", m, history_only=True))
    runs += [RunSpec("history", "A", "D_plus_equipment+history", "mlp", seed=s, history_only=True) for s in seeds[:1]]

    # 3. Chronological (protocol B). LightGBM params reused from protocol A selection.
    tf = "ablation__A__D_plus_equipment__lightgbm"
    runs.append(RunSpec("chrono", "B", "A_squat", "ratio"))
    runs += [RunSpec("chrono", "B", "D_plus_equipment", "linear"),
             RunSpec("chrono", "B", "D_plus_equipment", "lightgbm", tune_from=tf)]
    runs += [RunSpec("chrono", "B", "D_plus_equipment", "mlp", seed=s) for s in seeds[:1]]
    runs.append(RunSpec("chrono", "B", "D_plus_equipment", "last_deadlift", history_only=True))
    runs.append(RunSpec("chrono", "B", "D_plus_equipment", "lightgbm", history_only=True, tune_from=tf))
    runs.append(RunSpec("chrono", "B", "D_plus_equipment+history", "lightgbm", history_only=True))

    # 4. Transfer (protocol C). With-field model vs sensitivity model without the field.
    for g in splits_info["transfer_groups"]:
        proto = f"C:{g['field']}={g['value']}"
        with_field, without = (("D_plus_equipment", "C_plus_demographics") if g["field"] == "Equipment"
                               else ("E_plus_federation", "D_plus_equipment"))
        runs.append(RunSpec("transfer", proto, "A_squat", "ratio"))
        for fs in (with_field, without):
            runs.append(RunSpec("transfer", proto, fs, "linear"))
            runs.append(RunSpec("transfer", proto, fs, "lightgbm", tune_from=f"ablation__A__{fs}__lightgbm"))
        runs.append(RunSpec("transfer", proto, with_field, "mlp", seed=seeds[0]))

    # 5. Follow-up: career-summary history features (designed after the main test
    #    results were reported; tuned and selected on validation only).
    runs.append(RunSpec("history_rich", "A", "D_plus_equipment+history_rich", "lightgbm", history_only=True))
    runs.append(RunSpec("history_rich", "A", "D_plus_equipment+history_rich", "mlp", seed=seeds[0], history_only=True))
    runs.append(RunSpec("history_rich", "B", "D_plus_equipment+history_rich", "lightgbm", history_only=True))

    # 6. Follow-up: quantile LightGBM for prediction ranges (validation-calibrated).
    for fs, hist, tf in [("D_plus_equipment", False, "ablation__A__D_plus_equipment__lightgbm"),
                         ("D_plus_equipment+history_rich", True, "history_rich__A__D_plus_equipment-history_rich__lightgbm__histrows")]:
        for q in cfg.get("quantile", {}).get("levels", []):
            runs.append(RunSpec("quantile", "A", fs, "lightgbm", history_only=hist, tune_from=tf, variant=f"q{round(q * 100):02d}",
                                overrides={"objective": "quantile", "alpha": q}))

    # 7. Follow-up: expanded inputs (squat/bench attempts, context, any-event deadlift history).
    for fs in ["X_attempts", "X_context", "X_all", "X_all+anyhist"]:
        runs.append(RunSpec("expanded", "A", fs, "lightgbm"))
        runs.append(RunSpec("expanded", "A", fs, "mlp", seed=seeds[0]))
    runs.append(RunSpec("expanded", "A", "X_all+history_rich+anyhist", "lightgbm", history_only=True))
    runs.append(RunSpec("expanded", "A", "X_all+history_rich+anyhist", "mlp", seed=seeds[0], history_only=True))
    runs.append(RunSpec("expanded", "B", "X_all+anyhist", "lightgbm"))
    runs.append(RunSpec("expanded", "B", "X_all+history_rich+anyhist", "lightgbm", history_only=True))

    # 8. Follow-up: LightGBM objective / target variants for the best specialists.
    for fs, hist, base in OBJECTIVE_TARGETS:
        for name, ov in cfg.get("objective_variants", {}).items():
            runs.append(RunSpec("objective", "A", fs, "lightgbm", history_only=hist, tune_from=base, variant=name, overrides=ov))

    # 9. Capacity check: larger MLP / LightGBM variants, judged on validation only.
    for name, v in cfg.get("capacity", {}).get("variants", {}).items():
        for fs, hist in [("D_plus_equipment", False), ("D_plus_equipment+history", True)]:
            runs.append(RunSpec("capacity", "A", fs, v["model"], seed=seeds[0], history_only=hist,
                                variant=name, overrides=v["overrides"]))
    return runs


def partition_column(df: pd.DataFrame, spec: RunSpec) -> pd.Series:
    if spec.protocol == "A":
        return df["split_A"]
    if spec.protocol == "B":
        return df["split_B"]
    fld, value = spec.protocol[2:].split("=", 1)
    part = transfer_split(df, df["split_A"], fld, value)
    assert_disjoint(df, part, by_lifter=True)
    fit_rows = part.isin(["train", "val"])
    assert not (df.loc[fit_rows, fld] == value).any(), "held-out category leaked into fitting"
    return part


def run_one(spec: RunSpec, df: pd.DataFrame, cfg: dict, splits_info: dict, out_root: Path, force: bool = False) -> dict | None:
    out = out_root / "runs" / spec.run_id
    if (out / "done.json").exists() and not force:
        return None
    t0 = time.time()
    part = partition_column(df, spec).to_numpy()
    mask = np.ones(len(df), bool)
    if spec.history_only:
        mask &= df["has_history"].to_numpy()
    tr, va = (part == "train") & mask, (part == "val") & mask
    eval_parts = [p for p in pd.unique(part) if p not in ("train", "excluded")]

    overrides = {}
    if spec.model == "lightgbm" and spec.tune_from:
        src = out_root / "runs" / spec.tune_from / "meta.json"
        if src.exists():
            sel = read_json(src)["selected"]
            overrides["fixed_grid"] = [{"num_leaves": sel["num_leaves"], "min_child_samples": sel["min_child_samples"]}]
    overrides.update(spec.overrides)
    model = build_model(spec.model, spec.feature_set, cfg, spec.seed, overrides)
    train_df, val_df = df[tr], df[va]
    y_tr, y_va = train_df[TARGET].to_numpy(float), val_df[TARGET].to_numpy(float)
    model.fit(train_df, y_tr, val_df, y_va)
    fit_seconds = time.time() - t0

    preds = []
    for p in eval_parts:
        sel = (part == p) & mask
        sub = df[sel]
        preds.append(pd.DataFrame({"row_id": sub["row_id"].to_numpy(), "lifter_key": sub["lifter_key"].to_numpy(),
                                   "partition": p, "y": sub[TARGET].to_numpy(float), "yhat": model.predict(sub)}))
    pred = pd.concat(preds, ignore_index=True)
    out.mkdir(parents=True, exist_ok=True)
    pred.to_parquet(out / "predictions.parquet", index=False)
    model.save(out / "model.pkl")

    v = pred[pred["partition"] == "val"]
    val_metrics = summarize(v["y"], v["yhat"], v["lifter_key"]) if len(v) else {}
    meta = {
        **asdict(spec), "run_id": spec.run_id, "config_name": cfg["name"], "config_hash": config_hash(cfg),
        "config": {k: v for k, v in cfg.items() if not k.startswith("_")},
        "dataset_sha256": splits_info.get("dataset_sha256"), "split_id": splits_info["split_id"],
        "synthetic": bool(cfg.get("synthetic")), "versions": package_versions(),
        "train_rows": int(tr.sum()), "train_lifters": int(train_df["lifter_key"].nunique()),
        "val_rows": int(va.sum()), "eval_partitions": {p: int(((part == p) & mask).sum()) for p in eval_parts},
        "selected": model.selected, "tuning": model.tuning, "val_metrics": val_metrics,
        "preprocessor": {"numeric": model.prep.numeric, "categorical": model.prep.categorical,
                         "indicators": model.prep.indicator_cols, "fitted_rows": model.prep.fitted_rows,
                         "vocab_sizes": {k: len(v) for k, v in model.prep.vocab.items()}} if hasattr(model, "prep") else None,
        "fit_seconds": fit_seconds, "total_seconds": time.time() - t0,
    }
    write_json(out / "meta.json", meta)
    write_json(out / "done.json", {"ok": True})
    return meta


def _run_group(cfg: dict, specs: list[RunSpec], force: bool, offset: int, total: int) -> list[dict]:
    df, splits_info = load_prepared(cfg)
    ds = read_json(processed_dir(cfg) / "data_summary.json")
    splits_info = dict(splits_info, dataset_sha256=ds["snapshot"]["sha256"])
    out_root = artifacts_dir(cfg)
    metas = []
    for i, spec in enumerate(specs, offset + 1):
        t0 = time.time()
        meta = run_one(spec, df, cfg, splits_info, out_root, force=force)
        if meta is None:
            print(f"[{i}/{total}] skip (done) {spec.run_id}", flush=True)
            continue
        vm = meta["val_metrics"]
        print(f"[{i}/{total}] {spec.run_id}: train {meta['train_rows']:,} rows, val MAE {vm.get('mae', float('nan')):.2f} kg "
              f"({time.time() - t0:.1f}s)", flush=True)
        metas.append(meta)
    return metas


def run_isolated(fn, *args):
    """Run `fn(*args)` in a fresh spawned interpreter.

    LightGBM and PyTorch wheels each bundle their own OpenMP runtime on macOS;
    loading both in one process deadlocks or segfaults. Tree/linear runs and MLP
    runs therefore execute in separate processes."""
    import multiprocessing as mp

    with mp.get_context("spawn").Pool(1) as pool:
        return pool.apply(fn, args)


def train(cfg: dict, experiments: list[str] | None = None, force: bool = False, only: str | None = None) -> list[dict]:
    _, splits_info = load_prepared(cfg)
    specs = plan(cfg, splits_info)
    if experiments:
        specs = [s for s in specs if s.experiment in experiments]
    if only:
        specs = [s for s in specs if only in s.run_id]
    # Non-MLP first: chrono/transfer LightGBM runs reuse params selected in ablation runs.
    groups = [[s for s in specs if s.model != "mlp"], [s for s in specs if s.model == "mlp"]]
    metas, offset = [], 0
    for group in groups:
        if group:
            metas += run_isolated(_run_group, cfg, group, force, offset, len(specs))
        offset += len(group)
    return metas
