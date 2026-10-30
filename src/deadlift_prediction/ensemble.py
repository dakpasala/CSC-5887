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
