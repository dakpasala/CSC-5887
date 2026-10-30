"""Follow-up #6: prediction ranges from LightGBM quantile models.

Raw range: [q_lo, q_hi] from the two quantile models (sorted per row so it is
never inverted). Calibrated range: conformalized quantile regression (CQR,
Romano et al. 2019). The conformity score on validation rows is
s = max(q_lo - y, y - q_hi), and the range is widened (or narrowed, if s is
mostly negative) by the ceil((n+1)(1-a))/n quantile of s, where a = 1 - target
coverage. Only validation rows are used to estimate the correction; test coverage
is the independent check. Validation rows from the same lifter are correlated
and the quantile models also early-stopped on validation, so the guarantee is
approximate.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .config import artifacts_dir, write_json
from .train import RunSpec


def interval_runs(cfg: dict) -> list[dict]:
    levels = cfg.get("quantile", {}).get("levels", [])
    if len(levels) != 2:
        return []
    lo, hi = sorted(levels)
    out = []
    for fs, hist in [("D_plus_equipment", False), ("D_plus_equipment+history_rich", True)]:
        ids = [RunSpec("quantile", "A", fs, "lightgbm", history_only=hist, variant=f"q{round(q * 100):02d}").run_id for q in (lo, hi)]
        out.append({"feature_set": fs, "history_only": hist, "lo_run": ids[0], "hi_run": ids[1]})
    return out


def conformal_correction(y, lo, hi, coverage: float) -> float:
    s = np.maximum(np.asarray(lo, float) - np.asarray(y, float), np.asarray(y, float) - np.asarray(hi, float))
    n = len(s)
    level = min(1.0, np.ceil((n + 1) * coverage) / n)
    return float(np.quantile(s, level, method="higher"))


def _summ(y, lo, hi, groups) -> dict:
    y, lo, hi = map(lambda a: np.asarray(a, float), (y, lo, hi))
    inside = (y >= lo) & (y <= hi)
    return {"rows": int(len(y)), "lifters": int(pd.Series(groups).nunique()), "coverage": float(inside.mean()),
            "mean_width_kg": float(np.mean(hi - lo)), "median_width_kg": float(np.median(hi - lo)),
            "below": float((y < lo).mean()), "above": float((y > hi).mean())}


def evaluate_intervals(cfg: dict, final: bool, ctx: pd.DataFrame) -> pd.DataFrame:
    """`ctx` is indexed by row_id with Sex, bw_bin, has_history columns."""
    root = artifacts_dir(cfg) / "runs"
    target = cfg["quantile"]["target_coverage"]
    rows, meta = [], {}
    for spec in interval_runs(cfg):
        if not all((root / r / "done.json").exists() for r in (spec["lo_run"], spec["hi_run"])):
            continue
        a = pd.read_parquet(root / spec["lo_run"] / "predictions.parquet")
        b = pd.read_parquet(root / spec["hi_run"] / "predictions.parquet")
        m = a.merge(b[["row_id", "partition", "yhat"]], on=["row_id", "partition"], suffixes=("_a", "_b"), validate="one_to_one")
        m["lo"] = np.minimum(m["yhat_a"], m["yhat_b"])
        m["hi"] = np.maximum(m["yhat_a"], m["yhat_b"])
        v = m[m["partition"] == "val"]
        q = conformal_correction(v["y"], v["lo"], v["hi"], target)
        meta[spec["feature_set"]] = {"conformal_correction_kg": q, "calibration_rows": int(len(v)), **spec}
        parts = ["val"] + (["test"] if final else [])
        for part in parts:
            g = m[m["partition"] == part].join(ctx, on="row_id")
            for kind, lo, hi in [("raw", g["lo"], g["hi"]), ("conformal", g["lo"] - q, g["hi"] + q)]:
                base = {"feature_set": spec["feature_set"], "partition": part, "interval": kind, "target_coverage": target,
                        "correction_kg": q if kind == "conformal" else 0.0}
                rows.append({**base, "group_by": "all", "group": "all", **_summ(g["y"], lo, hi, g["lifter_key"])})
                for col in ["Sex", "bw_bin", "Equipment"]:
                    for val, sub in g.groupby(col, dropna=False):
                        rows.append({**base, "group_by": col, "group": "missing" if pd.isna(val) else str(val),
                                     **_summ(sub["y"], lo.loc[sub.index], hi.loc[sub.index], sub["lifter_key"])})
    out = pd.DataFrame(rows)
    tdir = artifacts_dir(cfg) / ("tables_final" if final else "tables_val")
    tdir.mkdir(parents=True, exist_ok=True)
    out.to_csv(tdir / "intervals.csv", index=False)
    write_json(tdir / "intervals.json", meta)
    return out
