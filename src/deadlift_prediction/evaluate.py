"""Metrics from saved predictions: per-run tables, paired comparisons on identical
rows with lifter-bootstrap CIs, and subgroup breakdowns.

By default only validation partitions are scored (development mode). `final=True`
scores test partitions; configurations must be frozen before that is used.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .config import artifacts_dir, read_json, write_json
from .features import CORE_ABLATION
from .metrics import bootstrap_mean_ci, summarize
from .prepare import load_prepared
from .train import RunSpec

MODELS = ["ratio", "linear", "lightgbm", "mlp"]


def _runs(root) -> dict[str, dict]:
    out = {}
    for d in sorted((root / "runs").glob("*")):
        if (d / "done.json").exists():
            out[d.name] = read_json(d / "meta.json")
    return out


class Evaluator:
    def __init__(self, cfg: dict, final: bool):
        self.cfg, self.final = cfg, final
        self.root = artifacts_dir(cfg)
        self.runs = _runs(self.root)
        df, self.splits = load_prepared(cfg)
        bins = cfg["features"]["bodyweight_bins"]
        df["bw_bin"] = pd.cut(df["BodyweightKg"], bins=bins, right=False).astype(object).map(
            lambda iv: f"{iv.left:g}-{iv.right:g}" if pd.notna(iv) else "missing")
        self.ctx = df.set_index("row_id")[["Sex", "Equipment", "Federation", "bw_bin", "has_history", "BodyweightKg",
                                          "Age", "Best3SquatKg", "Best3BenchKg"]]
        self.ev = cfg["evaluation"]
        self._pred_cache: dict[str, pd.DataFrame] = {}

    def pred(self, run_id: str) -> pd.DataFrame:
        if run_id not in self._pred_cache:
            self._pred_cache[run_id] = pd.read_parquet(self.root / "runs" / run_id / "predictions.parquet")
        return self._pred_cache[run_id]

    def test_part(self, base: str = "test") -> str:
        return base if self.final else "val"

    # ------------------------------------------------------------------ comparison
    def compare(self, name: str, run_ids: list[str], partition: str, row_filter=None,
                pairs: list[tuple[str, str]] | None = None, labels: dict | None = None) -> tuple[list[dict], list[dict]]:
        run_ids = [r for r in run_ids if r in self.runs]
        if not run_ids:
            return [], []
        frames = {}
        for r in run_ids:
            p = self.pred(r)
            p = p[p["partition"] == partition].set_index("row_id")
            if row_filter is not None:
                p = p[row_filter(self.ctx.loc[p.index])]
            frames[r] = p
        common = None
        for p in frames.values():
            common = p.index if common is None else common.intersection(p.index)
        reps, seed = self.ev["bootstrap_reps"], self.cfg["seed"]
        rows, paired = [], []
        for r in run_ids:
            p = frames[r].loc[common]
            s = summarize(p["y"], p["yhat"], p["lifter_key"], self.ev["sparse_rows"], self.ev["sparse_lifters"])
            lo, hi = bootstrap_mean_ci(np.abs(p["y"] - p["yhat"]), p["lifter_key"], reps, seed)
            meta = self.runs[r]
            rows.append({"comparison": name, "partition": partition, "run_id": r, "label": (labels or {}).get(r, r),
                         "protocol": meta["protocol"], "experiment": meta["experiment"], "feature_set": meta["feature_set"],
                         "model": meta["model"], "seed": meta["seed"], **s, "mae_ci_low": lo, "mae_ci_high": hi,
                         "rows_before_intersection": len(frames[r])})
        for a, b in pairs or []:
            if a not in frames or b not in frames:
                continue
            pa, pb = frames[a].loc[common], frames[b].loc[common]
            diff = np.abs(pa["y"] - pa["yhat"]).to_numpy() - np.abs(pb["y"] - pb["yhat"]).to_numpy()
            lo, hi = bootstrap_mean_ci(diff, pa["lifter_key"], reps, seed + 1)
            paired.append({"comparison": name, "partition": partition, "a": (labels or {}).get(a, a), "b": (labels or {}).get(b, b),
                           "run_a": a, "run_b": b, "rows": len(common), "lifters": int(pa["lifter_key"].nunique()),
                           "mae_a": float(np.abs(pa["y"] - pa["yhat"]).mean()), "mae_b": float(np.abs(pb["y"] - pb["yhat"]).mean()),
                           "mae_diff_a_minus_b": float(diff.mean()), "ci_low": lo, "ci_high": hi})
        return rows, paired

    def subgroups(self, run_ids: list[str], partition: str) -> list[dict]:
        out = []
        for r in run_ids:
            if r not in self.runs:
                continue
            p = self.pred(r)
            p = p[p["partition"] == partition].join(self.ctx, on="row_id")
            for col in ["Sex", "bw_bin", "has_history", "Equipment"]:
                for val, g in p.groupby(col, dropna=False):
                    s = summarize(g["y"], g["yhat"], g["lifter_key"], self.ev["sparse_rows"], self.ev["sparse_lifters"])
                    out.append({"run_id": r, "model": self.runs[r]["model"], "feature_set": self.runs[r]["feature_set"],
                                "partition": partition, "group_by": col, "group": "missing" if pd.isna(val) else str(val), **s})
        return out


def rid(exp, proto, fs, model, seed=None, hist=False, variant=None):
    return RunSpec(exp, proto, fs, model, seed=seed or 42, history_only=hist, variant=variant).run_id


def evaluate(cfg: dict, final: bool = False) -> dict:
    E = Evaluator(cfg, final)
    s0 = cfg["models"]["mlp"]["seeds"][0]
    seeds = cfg["models"]["mlp"]["seeds"]
    T = E.test_part()
    rows, paired, subs = [], [], []

    def add(res):
        rows.extend(res[0]); paired.extend(res[1])

    # 1. core ablation, each model, identical rows across stages
    ratio = rid("ablation", "A", "A_squat", "ratio")
    abl = [ratio]
    pairs = []
    for m in ["linear", "lightgbm", "mlp"]:
        ids = [rid("ablation", "A", fs, m, s0) for fs in CORE_ABLATION]
        abl += ids
        pairs += list(zip(ids[1:], ids[:-1]))
        pairs.append((ids[-1], ratio))
    add(E.compare("ablation_core", abl, T, pairs=pairs))
    # E extension vs D
    ext, pairs = [], []
    for m in ["linear", "lightgbm", "mlp"]:
        d, e = rid("ablation", "A", "D_plus_equipment", m, s0), rid("ablation", "A", "E_plus_federation", m, s0)
        ext += [d, e]; pairs.append((e, d))
    add(E.compare("ablation_federation_extension", ext, T, pairs=pairs))
    # model comparison at D, including MLP seeds
    dmods = [ratio, rid("ablation", "A", "D_plus_equipment", "linear"), rid("ablation", "A", "D_plus_equipment", "lightgbm")]
    dmods += [rid("ablation", "A", "D_plus_equipment", "mlp", s) for s in seeds]
    lg = dmods[2]
    add(E.compare("models_D", dmods, T, pairs=[(lg, dmods[1]), (lg, ratio)] + [(rid("ablation", "A", "D_plus_equipment", "mlp", s), lg) for s in seeds]))

    # 2. history, identical history-eligible rows
    has_h = lambda c: c["has_history"].to_numpy(bool)
    no_h = lambda c: ~c["has_history"].to_numpy(bool)
    last = rid("history", "A", "D_plus_equipment", "last_deadlift", hist=True)
    hist_ids = [last]
    pairs = []
    for m in ["linear", "lightgbm", "mlp"]:
        all_rows = rid("ablation", "A", "D_plus_equipment", m, s0)
        hrows = rid("history", "A", "D_plus_equipment", m, s0, hist=True)
        withh = rid("history", "A", "D_plus_equipment+history", m, s0, hist=True)
        hist_ids += [all_rows, hrows, withh]
        pairs += [(withh, all_rows), (withh, hrows), (withh, last)]
    add(E.compare("history_eligible", hist_ids, T, row_filter=has_h, pairs=pairs))
    add(E.compare("no_history_rows", [ratio] + [rid("ablation", "A", "D_plus_equipment", m, s0) for m in ["linear", "lightgbm", "mlp"]],
                  T, row_filter=no_h))

    # 3. chronological
    ch = [rid("chrono", "B", "A_squat", "ratio"), rid("chrono", "B", "D_plus_equipment", "linear"),
          rid("chrono", "B", "D_plus_equipment", "lightgbm"), rid("chrono", "B", "D_plus_equipment", "mlp", s0)]
    add(E.compare("chrono_all", ch, T, pairs=[(ch[2], ch[0]), (ch[2], ch[1]), (ch[3], ch[2])]))
    chh = [rid("chrono", "B", "D_plus_equipment", "last_deadlift", hist=True), rid("chrono", "B", "D_plus_equipment", "lightgbm"),
           rid("chrono", "B", "D_plus_equipment", "lightgbm", hist=True), rid("chrono", "B", "D_plus_equipment+history", "lightgbm", hist=True)]
    add(E.compare("chrono_history_eligible", chh, T, row_filter=has_h, pairs=[(chh[3], chh[2]), (chh[3], chh[0]), (chh[3], chh[1])]))

    # 4. transfer
    transfer_cov = []
    for g in E.splits["transfer_groups"]:
        proto = f"C:{g['field']}={g['value']}"
        wf, wo = (("D_plus_equipment", "C_plus_demographics") if g["field"] == "Equipment" else ("E_plus_federation", "D_plus_equipment"))
        ids = [rid("transfer", proto, "A_squat", "ratio")]
        ids += [rid("transfer", proto, fs, m) for fs in (wf, wo) for m in ["linear", "lightgbm"]]
        ids.append(rid("transfer", proto, wf, "mlp", s0))
        parts = ["test_transfer", "test_in_dist"] if final else ["val"]
        for part in parts:
            add(E.compare(f"transfer|{g['field']}={g['value']}", ids, part,
                          pairs=[(rid("transfer", proto, wf, "lightgbm"), rid("transfer", proto, wo, "lightgbm")),
                                 (rid("transfer", proto, wf, "lightgbm"), ids[0])]))
        if final and ids[0] in E.runs:
            p = E.pred(ids[0]).join(E.ctx, on="row_id")
            for part, sub in p.groupby("partition"):
                transfer_cov.append({"group": f"{g['field']}={g['value']}", "partition": part, "rows": len(sub),
                                     "lifters": sub["lifter_key"].nunique(), "share_female": (sub["Sex"] == "F").mean(),
                                     "share_raw": (sub["Equipment"] == "Raw").mean(), "mean_squat": sub["Best3SquatKg"].mean(),
                                     "mean_bench": sub["Best3BenchKg"].mean(), "mean_bodyweight": sub["BodyweightKg"].mean(),
                                     "age_missing": sub["Age"].isna().mean(), "mean_deadlift": sub["y"].mean()})

    # 5. capacity check: larger variants vs base models on identical rows
    variants = cfg.get("capacity", {}).get("variants", {})
    for fs, hist, base_exp, name in [("D_plus_equipment", False, "ablation", "capacity_D"),
                                     ("D_plus_equipment+history", True, "history", "capacity_D_history")]:
        ids, pairs = [], []
        for m in ["lightgbm", "mlp"]:
            base = rid(base_exp, "A", fs, m, s0, hist=hist)
            ids.append(base)
            for vname, v in variants.items():
                if v["model"] == m:
                    vid = rid("capacity", "A", fs, m, s0, hist=hist, variant=vname)
                    ids.append(vid)
                    pairs.append((vid, base))
        add(E.compare(name, ids, T, row_filter=has_h if hist else None, pairs=pairs))

    # 6. follow-up: career-summary history vs previous-meet history, identical rows
    last_a = rid("history", "A", "D_plus_equipment", "last_deadlift", hist=True)
    ha = {m: rid("history", "A", "D_plus_equipment+history", m, s0, hist=True) for m in ["lightgbm", "mlp"]}
    ra = {m: rid("history_rich", "A", "D_plus_equipment+history_rich", m, s0, hist=True) for m in ["lightgbm", "mlp"]}
    add(E.compare("history_rich_A", [last_a, ha["lightgbm"], ha["mlp"], ra["lightgbm"], ra["mlp"]], T, row_filter=has_h,
                  pairs=[(ra["lightgbm"], ha["lightgbm"]), (ra["mlp"], ha["mlp"]), (ra["lightgbm"], last_a), (ra["mlp"], ra["lightgbm"])]))
    last_b = rid("chrono", "B", "D_plus_equipment", "last_deadlift", hist=True)
    hb = rid("chrono", "B", "D_plus_equipment+history", "lightgbm", hist=True)
    rb = rid("history_rich", "B", "D_plus_equipment+history_rich", "lightgbm", hist=True)
    add(E.compare("history_rich_B", [last_b, hb, rb], T, row_filter=has_h, pairs=[(rb, hb), (rb, last_b)]))

    # subgroup breakdowns for the primary-protocol D models
    subs = E.subgroups(dmods[:4], T)
    subs += E.subgroups([ch[2]], T)

    out_dir = E.root / ("tables_final" if final else "tables_val")
    out_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out_dir / "metrics.csv", index=False)
    pd.DataFrame(paired).to_csv(out_dir / "paired.csv", index=False)
    pd.DataFrame(subs).to_csv(out_dir / "subgroups.csv", index=False)
    if transfer_cov:
        pd.DataFrame(transfer_cov).to_csv(out_dir / "transfer_covariates.csv", index=False)
    runs = pd.DataFrame([{k: m[k] for k in ["run_id", "experiment", "protocol", "feature_set", "model", "seed", "train_rows",
                                             "train_lifters", "val_rows", "fit_seconds"]} | {"val_mae": m["val_metrics"].get("mae"),
                                             "selected": {k: v for k, v in m["selected"].items() if k != "coef"}}
                         for m in E.runs.values()])
    runs.to_csv(out_dir / "runs.csv", index=False)
    write_json(out_dir / "evaluation.json", {"final": final, "scored_partition": T, "n_runs": len(E.runs),
                                             "bootstrap_reps": cfg["evaluation"]["bootstrap_reps"],
                                             "bootstrap_unit": "lifter", "split_id": E.splits["split_id"]})
    print(f"wrote {out_dir} ({len(rows)} metric rows, {len(paired)} paired comparisons)")
    return {"dir": str(out_dir)}
