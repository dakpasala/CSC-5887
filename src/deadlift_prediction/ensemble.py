"""Follow-up: weighted average of LightGBM and MLP predictions from existing runs.

The weight w (prediction = w * LightGBM + (1 - w) * MLP) is chosen by validation
MAE from a fixed grid; test rows are never used for the choice. Each ensemble is
written as an ordinary run directory so `evaluate` treats it like any model.
"""

from __future__ import annotations

import time

import numpy as np
import pandas as pd

from .config import artifacts_dir, config_hash, package_versions, read_json, write_json
from .metrics import mae, summarize

WEIGHTS = [0.0, 0.25, 0.5, 0.75, 1.0]

# (ensemble run_id, LightGBM run_id, MLP run_id)
PAIRS = [
    ("ensemble__A__D_plus_equipment__lgbm_mlp",
     "ablation__A__D_plus_equipment__lightgbm", "ablation__A__D_plus_equipment__mlp__s42"),
    ("ensemble__A__D_plus_equipment-history_rich__lgbm_mlp__histrows",
     "history_rich__A__D_plus_equipment-history_rich__lightgbm__histrows",
     "history_rich__A__D_plus_equipment-history_rich__mlp__histrows__s42"),
    ("ensemble__B__D_plus_equipment__lgbm_mlp",
     "chrono__B__D_plus_equipment__lightgbm", "chrono__B__D_plus_equipment__mlp__s42"),
    ("ensemble__A__X_all-anyhist__lgbm_mlp",
     "expanded__A__X_all-anyhist__lightgbm", "expanded__A__X_all-anyhist__mlp__s42"),
    ("ensemble__A__X_all-history_rich-anyhist__lgbm_mlp__histrows",
     "expanded__A__X_all-history_rich-anyhist__lightgbm__histrows",
     "expanded__A__X_all-history_rich-anyhist__mlp__histrows__s42"),
]


def build_ensembles(cfg: dict) -> list[dict]:
    root = artifacts_dir(cfg) / "runs"
    out = []
    for run_id, lgbm_id, mlp_id in PAIRS:
        if not ((root / lgbm_id / "done.json").exists() and (root / mlp_id / "done.json").exists()):
            print(f"skip {run_id}: component runs missing")
            continue
        t0 = time.time()
        a = pd.read_parquet(root / lgbm_id / "predictions.parquet")
        b = pd.read_parquet(root / mlp_id / "predictions.parquet")
        m = a.merge(b[["row_id", "partition", "yhat"]], on=["row_id", "partition"], suffixes=("_lgbm", "_mlp"), validate="one_to_one")
        if len(m) != len(a) or len(m) != len(b):
            raise ValueError(f"{run_id}: component predictions cover different rows")
        v = m[m["partition"] == "val"]
        tuning = [{"w_lightgbm": w, "val_mae": mae(v["y"], w * v["yhat_lgbm"] + (1 - w) * v["yhat_mlp"])} for w in WEIGHTS]
        w = min(tuning, key=lambda t: t["val_mae"])["w_lightgbm"]
        m["yhat"] = w * m["yhat_lgbm"] + (1 - w) * m["yhat_mlp"]
        d = root / run_id
        d.mkdir(parents=True, exist_ok=True)
        m[["row_id", "lifter_key", "partition", "y", "yhat"]].to_parquet(d / "predictions.parquet", index=False)
        ma = read_json(root / lgbm_id / "meta.json")
        v = m[m["partition"] == "val"]
        meta = {
            "experiment": "ensemble", "protocol": ma["protocol"], "feature_set": ma["feature_set"], "model": "ensemble",
            "seed": ma["seed"], "history_only": ma["history_only"], "run_id": run_id, "components": [lgbm_id, mlp_id],
            "config_name": cfg["name"], "config_hash": config_hash(cfg), "dataset_sha256": ma.get("dataset_sha256"),
            "split_id": ma["split_id"], "synthetic": bool(cfg.get("synthetic")), "versions": package_versions(),
            "train_rows": ma["train_rows"], "train_lifters": ma["train_lifters"], "val_rows": ma["val_rows"],
            "selected": {"w_lightgbm": w, "rule": "argmin validation MAE over fixed weight grid"}, "tuning": tuning,
            "val_metrics": summarize(v["y"], v["yhat"], v["lifter_key"]), "fit_seconds": time.time() - t0,
        }
        write_json(d / "meta.json", meta)
        write_json(d / "done.json", {"ok": True})
        print(f"{run_id}: w_lightgbm={w}, val MAE {meta['val_metrics']['mae']:.3f} kg")
        out.append(meta)
    return out


# ---------------------------------------------------------------------------- objective follow-up

def _val_mae(root, run_id: str) -> float:
    return read_json(root / run_id / "meta.json")["val_metrics"]["mae"]


def best_objective_runs(cfg: dict) -> dict[str, str]:
    """Per specialist feature set, the LightGBM run (base or objective variant)
    with the lowest validation MAE in kg."""
    from .train import OBJECTIVE_TARGETS, RunSpec

    root = artifacts_dir(cfg) / "runs"
    out = {}
    for fs, hist, base in OBJECTIVE_TARGETS:
        cands = [base] + [RunSpec("objective", "A", fs, "lightgbm", history_only=hist, variant=v).run_id
                          for v in cfg.get("objective_variants", {})]
        cands = [c for c in cands if (root / c / "done.json").exists()]
        if cands:
            out[fs] = min(cands, key=lambda c: _val_mae(root, c))
    return out


def _write_pseudo_run(cfg, run_id, preds: pd.DataFrame, template: dict, selected: dict, components: list[str], experiment: str):
    root = artifacts_dir(cfg) / "runs"
    d = root / run_id
    d.mkdir(parents=True, exist_ok=True)
    preds[["row_id", "lifter_key", "partition", "y", "yhat"]].to_parquet(d / "predictions.parquet", index=False)
    v = preds[preds["partition"] == "val"]
    meta = {
        "experiment": experiment, "protocol": template["protocol"], "feature_set": template["feature_set"], "model": experiment,
        "seed": template["seed"], "history_only": template["history_only"], "run_id": run_id, "components": components,
        "config_name": cfg["name"], "config_hash": config_hash(cfg), "dataset_sha256": template.get("dataset_sha256"),
        "split_id": template["split_id"], "synthetic": bool(cfg.get("synthetic")), "versions": package_versions(),
        "train_rows": template["train_rows"], "train_lifters": template["train_lifters"], "val_rows": template["val_rows"],
        "selected": selected, "tuning": [], "val_metrics": summarize(v["y"], v["yhat"], v["lifter_key"]) if len(v) else {},
        "fit_seconds": 0.0,
    }
    write_json(d / "meta.json", meta)
    write_json(d / "done.json", {"ok": True})
    return meta


def _blend(root, lgbm_id, mlp_id):
    a = pd.read_parquet(root / lgbm_id / "predictions.parquet")
    b = pd.read_parquet(root / mlp_id / "predictions.parquet")
    m = a.merge(b[["row_id", "partition", "yhat"]], on=["row_id", "partition"], suffixes=("_lgbm", "_mlp"), validate="one_to_one")
    v = m[m["partition"] == "val"]
    tuning = [{"w_lightgbm": w, "val_mae": mae(v["y"], w * v["yhat_lgbm"] + (1 - w) * v["yhat_mlp"])} for w in WEIGHTS]
    w = min(tuning, key=lambda t: t["val_mae"])["w_lightgbm"]
    m["yhat"] = w * m["yhat_lgbm"] + (1 - w) * m["yhat_mlp"]
    return m, w, tuning


ROUTED = {
    # name: (first-timer run, returning-lifter run)
    "routed__A__original_specialists": ("ablation__A__D_plus_equipment__lightgbm",
                                        "ensemble__A__D_plus_equipment-history_rich__lgbm_mlp__histrows"),
    "routed__A__expanded_specialists": ("ensemble__A__X_all-anyhist__lgbm_mlp",
                                        "ensemble__A__X_all-history_rich-anyhist__lgbm_mlp__histrows"),
    "routed__A__objective_specialists": ("ensemble__A__X_all-anyhist__bestobj_mlp",
                                         "ensemble__A__X_all-history_rich-anyhist__bestobj_mlp__histrows"),
}


def build_objective_ensembles(cfg: dict, has_history: pd.Series) -> list[dict]:
    """Best-objective LightGBM + MLP blends, then routed two-specialist systems.

    `has_history` is indexed by row_id. Routing uses only whether a strictly
    earlier full-power meet exists (known before the deadlift)."""
    root = artifacts_dir(cfg) / "runs"
    best = best_objective_runs(cfg)
    metas = []
    mlps = {"X_all+anyhist": ("expanded__A__X_all-anyhist__mlp__s42", "ensemble__A__X_all-anyhist__bestobj_mlp"),
            "X_all+history_rich+anyhist": ("expanded__A__X_all-history_rich-anyhist__mlp__histrows__s42",
                                           "ensemble__A__X_all-history_rich-anyhist__bestobj_mlp__histrows")}
    for fs, lgbm_id in best.items():
        mlp_id, run_id = mlps[fs]
        if not (root / mlp_id / "done.json").exists():
            continue
        m, w, tuning = _blend(root, lgbm_id, mlp_id)
        tmpl = read_json(root / lgbm_id / "meta.json")
        meta = _write_pseudo_run(cfg, run_id, m, tmpl, {"w_lightgbm": w, "best_lightgbm": lgbm_id, "weight_tuning": tuning},
                                 [lgbm_id, mlp_id], "ensemble")
        print(f"{run_id}: best LightGBM {lgbm_id}, w={w}, val MAE {meta['val_metrics']['mae']:.3f}")
        metas.append(meta)
    for name, (first_id, hist_id) in ROUTED.items():
        if not all((root / r / "done.json").exists() for r in (first_id, hist_id)):
            continue
        f = pd.read_parquet(root / first_id / "predictions.parquet").set_index(["row_id", "partition"])
        h = pd.read_parquet(root / hist_id / "predictions.parquet").set_index(["row_id", "partition"])
        f = f[f.index.get_level_values("partition").isin(["val", "test"])]
        use_h = has_history.reindex(f.index.get_level_values("row_id")).to_numpy(bool)
        out = f.copy()
        hk = f.index[use_h]
        out.loc[hk, "yhat"] = h.loc[hk, "yhat"].to_numpy()
        tmpl = read_json(root / first_id / "meta.json")
        tmpl = {**tmpl, "feature_set": "routed", "history_only": False}
        meta = _write_pseudo_run(cfg, name, out.reset_index(), tmpl,
                                 {"first_timers": first_id, "returning_lifters": hist_id,
                                  "rule": "returning-lifter model when a strictly earlier full-power meet exists"},
                                 [first_id, hist_id], "routed")
        print(f"{name}: val MAE {meta['val_metrics']['mae']:.3f}")
        metas.append(meta)
    return metas
