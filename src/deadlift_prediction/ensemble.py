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
    "routed__A__embed_specialists": ("ensemble__A__X_all-anyhist__bestobj_embed",
                                     "ensemble__A__X_all-history_rich-anyhist__bestobj_embed__histrows"),
    "routed__A__dlatt_specialists": ("ensemble__A__X_all-anyhist-dlatt__huber_embed",
                                     "ensemble__A__X_all-history_rich-anyhist-dlatt__huber_embed__histrows"),
    "routed__A__gru_specialists": ("ensemble__A__X_all-anyhist-dlatt__huber_embed", "ensemble__A__seq_gru_blend__histrows"),
    "routed__A__tuned_specialists": ("ensemble__A__tuned_all", "ensemble__A__tuned_ret__histrows"),
    "routed__A__seedavg_specialists": ("ensemble__A__seedavg_all", "ensemble__A__seedavg_ret__histrows"),
    "routed__A__final_specialists": ("ensemble__A__final_all", "ensemble__A__final_ret__histrows"),
    "routed__A__final2_specialists": ("ensemble__A__final2_all", "ensemble__A__final2_ret__histrows"),
    "routed__A__final3_specialists": ("ensemble__A__final3_all", "ensemble__A__final3_ret__histrows"),
}

CATBOOST_RUNS = {"all": "catboost__A__X_all-anyhist-dlatt__catboost",
                 "ret": "catboost__A__X_all-history_rich-anyhist-dlatt__catboost__histrows"}
FINAL3_BLENDS = [
    ("ensemble__A__final2_all", CATBOOST_RUNS["all"], "ensemble__A__final3_all"),
    ("ensemble__A__final2_ret__histrows", CATBOOST_RUNS["ret"], "ensemble__A__final3_ret__histrows"),
]

# Seed-averaged ResNets (seed 42 + extra seeds) and the sequence Transformer, blended on top
# of the seed-averaged tuned blends.
RESNET_AVG = {"resnet_all": ("X_all+anyhist+dlatt", False), "resnet_ret": ("X_all+history_rich+anyhist+dlatt", True)}
SEQTF_RUN = "seqtf__A__X_all__seq_transformer__histrows__s42"
FINAL2_BLENDS = [
    ("ensemble__A__seedavg_all", "seedavg__A__resnet_all", "ensemble__A__final2_all"),
    ("ensemble__A__seedavg_ret__histrows", "seedavg__A__resnet_ret", "ensemble__A__final2_ret_r__histrows"),
    ("ensemble__A__final2_ret_r__histrows", SEQTF_RUN, "ensemble__A__final2_ret__histrows"),
]


def seedavg_id(name: str) -> str:
    return f"seedavg__A__{name}"


# Seed-averaged tuned models, re-blended, then a tabular ResNet blended on top.
SEEDAVG_BLENDS = [
    (seedavg_id("lgbm_all"), seedavg_id("embed_all"), "ensemble__A__seedavg_all"),
    (seedavg_id("lgbm_ret"), seedavg_id("embed_ret"), "ensemble__A__seedavg_ret_le__histrows"),
    ("ensemble__A__seedavg_ret_le__histrows", seedavg_id("gru_ret"), "ensemble__A__seedavg_ret__histrows"),
    ("ensemble__A__seedavg_all", "resnet__A__X_all-anyhist-dlatt__resnet_mlp__s42", "ensemble__A__final_all"),
    ("ensemble__A__seedavg_ret__histrows", "resnet__A__X_all-history_rich-anyhist-dlatt__resnet_mlp__histrows__s42",
     "ensemble__A__final_ret__histrows"),
]


def build_seedavg(cfg: dict) -> list[dict]:
    """Average each tuned model's predictions over its available seeds (base seed +
    extra seeds). Deterministic LightGBM settings have one seed, so the average is
    the tuned model itself."""
    from .hpo import TARGETS
    from .train import RunSpec

    root = artifacts_dir(cfg) / "runs"
    base_seed = cfg["models"]["mlp"]["seeds"][0]
    extra = cfg.get("seedavg", {}).get("extra_seeds", [])
    metas = []
    for name, (kind, fs, hist) in TARGETS.items():
        ids = [RunSpec("tuned", "A", fs, kind, seed=base_seed, history_only=hist, variant="hpo").run_id]
        for sd in extra:
            v = f"hpo_s{sd}" if kind == "lightgbm" else "hpo"
            ids.append(RunSpec("tuned", "A", fs, kind, seed=sd, history_only=hist, variant=v).run_id)
        ids = [r for r in ids if (root / r / "done.json").exists()]
        if not ids:
            continue
        frames = [pd.read_parquet(root / r / "predictions.parquet").set_index(["row_id", "partition"]) for r in ids]
        out = frames[0].copy()
        out["yhat"] = np.mean([f.loc[out.index, "yhat"].to_numpy() for f in frames], axis=0)
        tmpl = read_json(root / ids[0] / "meta.json")
        meta = _write_pseudo_run(cfg, seedavg_id(name), out.reset_index(), tmpl,
                                 {"averaged_runs": ids, "n_seeds": len(ids)}, ids, "seedavg")
        print(f"{seedavg_id(name)}: {len(ids)} seed(s), val MAE {meta['val_metrics']['mae']:.3f}")
        metas.append(meta)
    for name, (fs, hist) in RESNET_AVG.items():
        ids = [RunSpec("resnet", "A", fs, "resnet_mlp", seed=sd, history_only=hist).run_id for sd in [base_seed, *extra]]
        ids = [r for r in ids if (root / r / "done.json").exists()]
        if len(ids) < 2:
            continue
        frames = [pd.read_parquet(root / r / "predictions.parquet").set_index(["row_id", "partition"]) for r in ids]
        out = frames[0].copy()
        out["yhat"] = np.mean([f.loc[out.index, "yhat"].to_numpy() for f in frames], axis=0)
        meta = _write_pseudo_run(cfg, seedavg_id(name), out.reset_index(), read_json(root / ids[0] / "meta.json"),
                                 {"averaged_runs": ids, "n_seeds": len(ids)}, ids, "seedavg")
        print(f"{seedavg_id(name)}: {len(ids)} seed(s), val MAE {meta['val_metrics']['mae']:.3f}")
        metas.append(meta)
    return metas

# Hyperparameter-search follow-up: blends of the refit tuned models (weights chosen on validation).
TUNED_BLENDS = [
    ("tuned__A__X_all-anyhist-dlatt__lightgbm__hpo", "tuned__A__X_all-anyhist-dlatt__embed_mlp__hpo__s42",
     "ensemble__A__tuned_all"),
    ("tuned__A__X_all-history_rich-anyhist-dlatt__lightgbm__histrows__hpo",
     "tuned__A__X_all-history_rich-anyhist-dlatt__embed_mlp__histrows__hpo__s42", "ensemble__A__tuned_ret_le__histrows"),
    ("ensemble__A__tuned_ret_le__histrows", "tuned__A__X_all__gru__histrows__hpo__s42", "ensemble__A__tuned_ret__histrows"),
]

# GRU follow-up: current best returning-lifter blend + hybrid GRU (weight chosen on validation).
SEQ_BLENDS = [
    ("ensemble__A__X_all-history_rich-anyhist-dlatt__huber_embed__histrows",
     "seq__A__X_all-history_rich-anyhist-dlatt__gru__histrows__s42", "ensemble__A__seq_gru_blend__histrows"),
]

# Fixed (LightGBM, embedding MLP, blend) triples for the past-deadlift-attempt follow-up.
DLATT_BLENDS = [
    ("dlatt__A__X_all-anyhist-dlatt__lightgbm", "dlatt__A__X_all-anyhist-dlatt__embed_mlp__s42",
     "ensemble__A__X_all-anyhist-dlatt__huber_embed"),
    ("dlatt__A__X_all-history_rich-anyhist-dlatt__lightgbm__histrows",
     "dlatt__A__X_all-history_rich-anyhist-dlatt__embed_mlp__histrows__s42",
     "ensemble__A__X_all-history_rich-anyhist-dlatt__huber_embed__histrows"),
]


def build_objective_ensembles(cfg: dict, has_history: pd.Series) -> list[dict]:
    """Best-objective LightGBM + MLP blends, then routed two-specialist systems.

    `has_history` is indexed by row_id. Routing uses only whether a strictly
    earlier full-power meet exists (known before the deadlift)."""
    root = artifacts_dir(cfg) / "runs"
    best = best_objective_runs(cfg)
    metas = build_seedavg(cfg)
    mlps = {"X_all+anyhist": [("expanded__A__X_all-anyhist__mlp__s42", "ensemble__A__X_all-anyhist__bestobj_mlp"),
                              ("dl_arch__A__X_all-anyhist__embed_mlp__s42", "ensemble__A__X_all-anyhist__bestobj_embed")],
            "X_all+history_rich+anyhist": [
                ("expanded__A__X_all-history_rich-anyhist__mlp__histrows__s42",
                 "ensemble__A__X_all-history_rich-anyhist__bestobj_mlp__histrows"),
                ("dl_arch__A__X_all-history_rich-anyhist__embed_mlp__histrows__s42",
                 "ensemble__A__X_all-history_rich-anyhist__bestobj_embed__histrows")]}
    jobs = [(fs, lgbm_id, mlp_id, run_id) for fs, lgbm_id in best.items() for mlp_id, run_id in mlps[fs]]
    # Later blends may consume earlier ones (SEQ_BLENDS uses a DLATT blend), so
    # existence is checked inside the loop, in order.
    jobs += [(None, lgbm_id, mlp_id, run_id) for lgbm_id, mlp_id, run_id in DLATT_BLENDS + SEQ_BLENDS + TUNED_BLENDS + SEEDAVG_BLENDS
                                                                         + FINAL2_BLENDS + FINAL3_BLENDS]
    for fs, lgbm_id, mlp_id, run_id in jobs:
        if not ((root / lgbm_id / "done.json").exists() and (root / mlp_id / "done.json").exists()):
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


# ---------------------------------------------------------------------------- final recipe on protocols B and C

FINAL_SYSTEM = "routed__A__final3_specialists"  # current best protocol-A system (CatBoost weight 0 => same as final2)


def _final_id(proto: str, name: str) -> str:
    from .hpo import TARGETS
    from .train import RunSpec

    if name.startswith("resnet"):
        fs, hist = RESNET_AVG[name]
        return RunSpec("final_B", proto, fs, "resnet_mlp", seed=42, history_only=hist).run_id
    kind, fs, hist = TARGETS[name]
    exp = "final_B" if proto == "B" else "final_C"
    return RunSpec(exp, proto, fs, kind, seed=42, history_only=hist, variant="hpo").run_id


def route(cfg: dict, name: str, first_id: str, hist_id: str, has_history: pd.Series) -> dict | None:
    """Routed system over every partition of the first-timer run: returning-lifter
    predictions replace first-timer ones wherever a strictly earlier full-power
    meet exists (known before the deadlift)."""
    root = artifacts_dir(cfg) / "runs"
    if not all((root / r / "done.json").exists() for r in (first_id, hist_id)):
        return None
    f = pd.read_parquet(root / first_id / "predictions.parquet").set_index(["row_id", "partition"])
    h = pd.read_parquet(root / hist_id / "predictions.parquet").set_index(["row_id", "partition"])
    use_h = has_history.reindex(f.index.get_level_values("row_id")).to_numpy(bool)
    out = f.copy()
    hk = f.index[use_h]
    out.loc[hk, "yhat"] = h.loc[hk, "yhat"].to_numpy()
    tmpl = {**read_json(root / first_id / "meta.json"), "feature_set": "routed", "history_only": False}
    meta = _write_pseudo_run(cfg, name, out.reset_index(), tmpl,
                             {"first_timers": first_id, "returning_lifters": hist_id,
                              "rule": "returning-lifter model when a strictly earlier full-power meet exists"},
                             [first_id, hist_id], "routed")
    print(f"{name}: val MAE {meta['val_metrics'].get('mae', float('nan')):.3f}")
    return meta


def final_b_blends() -> list[tuple[str, str, str]]:
    i = lambda n: _final_id("B", n)
    return [
        (i("lgbm_all"), i("embed_all"), "ensemble__B__final_all_le"),
        ("ensemble__B__final_all_le", i("resnet_all"), "ensemble__B__final_all"),
        (i("lgbm_ret"), i("embed_ret"), "ensemble__B__final_ret_le__histrows"),
        ("ensemble__B__final_ret_le__histrows", i("gru_ret"), "ensemble__B__final_ret_leg__histrows"),
        ("ensemble__B__final_ret_leg__histrows", i("resnet_ret"), "ensemble__B__final_ret__histrows"),
    ]


B_ROUTED = {
    "routed__B__original_specialists": ("chrono__B__D_plus_equipment__lightgbm",
                                        "history_rich__B__D_plus_equipment-history_rich__lightgbm__histrows"),
    "routed__B__expanded_specialists": ("expanded__B__X_all-anyhist__lightgbm",
                                        "expanded__B__X_all-history_rich-anyhist__lightgbm__histrows"),
    "routed__B__final_recipe": ("ensemble__B__final_all", "ensemble__B__final_ret__histrows"),
}


def c_routed_name(field: str, value: str) -> str:
    return f"routed__C-{field}-{value}__final_lgbm"


def build_final_protocols(cfg: dict, has_history: pd.Series, transfer_groups: list[dict]) -> list[dict]:
    """Blend + route the final recipe on protocol B, and route the tuned LightGBM
    specialists for each protocol-C transfer group. Blend weights use each
    protocol's own validation partition."""
    root = artifacts_dir(cfg) / "runs"
    metas = []
    for a, b, run_id in final_b_blends():
        if not ((root / a / "done.json").exists() and (root / b / "done.json").exists()):
            continue
        m, w, tuning = _blend(root, a, b)
        meta = _write_pseudo_run(cfg, run_id, m, read_json(root / a / "meta.json"),
                                 {"w_first": w, "weight_tuning": tuning}, [a, b], "ensemble")
        print(f"{run_id}: w={w}, val MAE {meta['val_metrics']['mae']:.3f}")
        metas.append(meta)
    for name, (f, h) in B_ROUTED.items():
        if (meta := route(cfg, name, f, h, has_history)) is not None:
            metas.append(meta)
    for g in transfer_groups:
        proto = f"C:{g['field']}={g['value']}"
        meta = route(cfg, c_routed_name(g["field"], g["value"]), _final_id(proto, "lgbm_all"), _final_id(proto, "lgbm_ret"), has_history)
        if meta is not None:
            metas.append(meta)
    return metas


# ---------------------------------------------------------------------------- ResNet main model

RESNET_SEEDS = [42, 43, 44]
RESNET_A_SETS = {  # name -> (feature set, history_only)
    "A_squat": ("A_squat", False), "B_squat_bench": ("B_squat_bench", False),
    "C_plus_demographics": ("C_plus_demographics", False), "D_plus_equipment": ("D_plus_equipment", False),
    "X_context": ("X_context", False), "X_all": ("X_all", False),
    "D_plus_equipment+history": ("D_plus_equipment+history", True),
    "D_plus_equipment+history_rich": ("D_plus_equipment+history_rich", True),
}


def resnetavg_id(proto: str, name: str) -> str:
    return f"resnetavg__{proto}__{name.replace('+', '-')}" + ("__histrows" if "history" in name or name == "ret" else "")


def average_runs(cfg: dict, name: str, ids: list[str]) -> dict | None:
    """Mean prediction over seed runs; only built when every seed has finished."""
    root = artifacts_dir(cfg) / "runs"
    if not all((root / r / "done.json").exists() for r in ids):
        return None
    frames = [pd.read_parquet(root / r / "predictions.parquet").set_index(["row_id", "partition"]) for r in ids]
    out = frames[0].copy()
    out["yhat"] = np.mean([f.loc[out.index, "yhat"].to_numpy() for f in frames], axis=0)
    return _write_pseudo_run(cfg, name, out.reset_index(), read_json(root / ids[0] / "meta.json"),
                             {"averaged_runs": ids, "n_seeds": len(ids)}, ids, "seedavg")


def build_resnet_main(cfg: dict, has_history: pd.Series, transfer_groups: list[dict]) -> list[dict]:
    """Seed averages and routed systems for the ResNet main model on protocols A, B, C."""
    from .train import RunSpec

    metas = []
    for name, (fs, hist) in RESNET_A_SETS.items():
        ids = [RunSpec("resnet_main", "A", fs, "resnet_mlp", seed=s, history_only=hist).run_id for s in RESNET_SEEDS]
        if (m := average_runs(cfg, resnetavg_id("A", name), ids)) is not None:
            metas.append(m)
    for key, fs, hist in [("all", "X_all+anyhist+dlatt", False), ("ret", "X_all+history_rich+anyhist+dlatt", True)]:
        ids = [RunSpec("final_B", "B", fs, "resnet_mlp", seed=s, history_only=hist).run_id for s in RESNET_SEEDS]
        if (m := average_runs(cfg, resnetavg_id("B", key), ids)) is not None:
            metas.append(m)
    pairs = {
        "routed__A__resnet_main": (seedavg_id("resnet_all"), seedavg_id("resnet_ret")),
        "routed__A__resnet_s42": ("resnet__A__X_all-anyhist-dlatt__resnet_mlp__s42",
                                  "resnet__A__X_all-history_rich-anyhist-dlatt__resnet_mlp__histrows__s42"),
        "routed__B__resnet_main": (resnetavg_id("B", "all"), resnetavg_id("B", "ret")),
        "routed__A__lgbm_tuned": ("tuned__A__X_all-anyhist-dlatt__lightgbm__hpo",
                                  "tuned__A__X_all-history_rich-anyhist-dlatt__lightgbm__histrows__hpo"),
    }
    for g in transfer_groups:
        proto = f"C:{g['field']}={g['value']}"
        pairs[f"routed__C-{g['field']}-{g['value']}__resnet"] = (
            RunSpec("resnet_C", proto, "X_all+anyhist+dlatt", "resnet_mlp", seed=42).run_id,
            RunSpec("resnet_C", proto, "X_all+history_rich+anyhist+dlatt", "resnet_mlp", seed=42, history_only=True).run_id)
    for name, (f, h) in pairs.items():
        if (m := route(cfg, name, f, h, has_history)) is not None:
            metas.append(m)
    return metas
