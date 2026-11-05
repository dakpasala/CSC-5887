"""Bounded random hyperparameter search (follow-up). Validation only.

Each target is a (model, feature set, history_only) specialist. Trials train on
a fixed sample of protocol-A *training lifters* (sampled by hashed identity,
never by row) and are scored on the full validation partition. The best trial's
settings are later refit on the full training partition by the "tuned" runs in
train.plan. Test rows are never touched here. Trials are written to disk as they
finish, so an interrupted search resumes where it stopped.
"""

from __future__ import annotations

import time

import numpy as np

from .config import artifacts_dir, read_json, write_json
from .data import TARGET, hash_unit
from .models import build_model

TARGETS = {
    # name: (model, feature set, history_only)
    "lgbm_all": ("lightgbm", "X_all+anyhist+dlatt", False),
    "lgbm_ret": ("lightgbm", "X_all+history_rich+anyhist+dlatt", True),
    "embed_all": ("embed_mlp", "X_all+anyhist+dlatt", False),
    "embed_ret": ("embed_mlp", "X_all+history_rich+anyhist+dlatt", True),
    "gru_ret": ("gru", "X_all", True),
}

SPACES = {
    "lightgbm": {
        "num_leaves": [63, 127, 255, 511], "min_child_samples": [20, 50, 100, 200, 500],
        "learning_rate": [0.03, 0.05, 0.1], "colsample_bytree": [0.6, 0.8, 1.0], "subsample": [0.7, 0.9, 1.0],
        "reg_lambda": [0.0, 1.0, 10.0], "huber_delta": [5.0, 10.0, 20.0],
    },
    "embed_mlp": {
        "hidden": [[256, 128], [512, 256], [256, 256, 128]], "dropout": [0.0, 0.1, 0.2], "lr": [3e-4, 1e-3, 2e-3],
        "n_frequencies": [8, 16, 32], "frequency_scale": [0.1, 0.5, 1.0, 2.0], "d_embedding": [8, 16, 32],
        "batch_size": [2048, 4096],
    },
    "gru": {
        "gru_hidden": [32, 64, 128], "seq_len": [8, 12, 16], "hidden": [[128, 64], [256, 128]],
        "lr": [5e-4, 1e-3, 2e-3], "dropout": [0.0, 0.1],
    },
}


def sample(kind: str, rng: np.random.Generator) -> dict:
    return {k: v[rng.integers(len(v))] for k, v in SPACES[kind].items()}


def to_overrides(kind: str, params: dict) -> dict:
    """Map a sampled point to build_model overrides."""
    if kind != "lightgbm":
        return dict(params)
    tree = {k: params[k] for k in ["num_leaves", "min_child_samples", "colsample_bytree", "subsample", "reg_lambda"]}
    tree["subsample_freq"] = 1 if params["subsample"] < 1.0 else 0
    return {"objective": "huber", "huber_delta": params["huber_delta"], "learning_rate": params["learning_rate"],
            "n_estimators": 10000, "early_stopping_rounds": 100, "fixed_grid": [tree]}


def hpo_path(cfg: dict, name: str):
    return artifacts_dir(cfg) / "hpo" / f"{name}.json"


def best_overrides(cfg: dict, name: str) -> dict | None:
    p = hpo_path(cfg, name)
    if not p.exists():
        return None
    res = read_json(p)
    done = [t for t in res["trials"] if t.get("val_mae") is not None]
    if len(done) < res["n_trials"]:
        return None  # only use a finished search
    return min(done, key=lambda t: t["val_mae"])["overrides"]


def search(cfg: dict, names: list[str]) -> None:
    from .prepare import load_prepared

    h = cfg["hpo"]
    df, _ = load_prepared(cfg)
    part = df["split_A"].to_numpy()
    in_sample = hash_unit(df["lifter_key"], f"hpo{cfg['seed']}") < h["train_fraction"]
    for name in names:
        kind, fs, hist = TARGETS[name]
        mask = df["has_history"].to_numpy() if hist else np.ones(len(df), bool)
        tr, va = (part == "train") & mask & in_sample, (part == "val") & mask
        train_df, val_df = df[tr], df[va]
        y_tr, y_va = train_df[TARGET].to_numpy(float), val_df[TARGET].to_numpy(float)
        n = h["trials"][kind]
        path = hpo_path(cfg, name)
        res = read_json(path) if path.exists() else {"target": name, "model": kind, "feature_set": fs, "history_only": hist,
                                                     "n_trials": n, "train_fraction": h["train_fraction"],
                                                     "train_rows": int(tr.sum()), "val_rows": int(va.sum()), "trials": []}
        rng = np.random.default_rng([h["seed"], sum(map(ord, name))])
        points = [sample(kind, rng) for _ in range(n)]  # same sequence on resume
        for i, point in enumerate(points):
            if i < len(res["trials"]):
                continue
            t0 = time.time()
            ov = to_overrides(kind, point)
            model = build_model(kind, fs, cfg, cfg["seed"], ov).fit(train_df, y_tr, val_df, y_va)
            from .metrics import mae

            score = mae(y_va, model.predict(val_df))
            res["trials"].append({"trial": i, "params": point, "overrides": ov, "val_mae": score,
                                  "selected": {k: v for k, v in model.selected.items() if k != "coef"},
                                  "seconds": time.time() - t0})
            write_json(path, res)
            best = min(t["val_mae"] for t in res["trials"])
            print(f"  hpo {name} trial {i + 1}/{n}: val MAE {score:.3f} (best {best:.3f}, {time.time() - t0:.0f}s)", flush=True)


def run_search(cfg: dict, only: list[str] | None = None) -> None:
    """Tree targets and torch targets run in separate spawned processes (OpenMP conflict)."""
    from .models import TORCH_MODELS
    from .train import run_isolated

    names = [n for n in TARGETS if not only or n in only]
    for group in ([n for n in names if TARGETS[n][0] not in TORCH_MODELS], [n for n in names if TARGETS[n][0] in TORCH_MODELS]):
        if group:
            run_isolated(search, cfg, group)
