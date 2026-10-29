"""Evaluation protocols.

A  unseen lifters: deterministic group split by hashed canonical identity.
B  future meets: non-overlapping date intervals (lifters may recur).
C  transfer: a federation or equipment category held out of train/val, built on
   top of protocol A so held-out test lifters never appear in fitting.
"""

from __future__ import annotations

import hashlib

import numpy as np
import pandas as pd

from .data import hash_unit

PARTS = ("train", "val", "test")


def group_split(df: pd.DataFrame, fractions: dict, seed: int) -> pd.Series:
    u = hash_unit(df["lifter_key"], f"split{seed}")
    t, v = fractions["train"], fractions["train"] + fractions["val"]
    part = np.where(u < t, "train", np.where(u < v, "val", "test"))
    return pd.Series(part, index=df.index, name="split_A")


def chrono_boundaries(dates: pd.Series, quantiles: dict) -> dict:
    """Boundaries from row-date coverage only, snapped to month starts."""
    out = {}
    for key in ("val_start", "test_start"):
        q = dates.quantile(quantiles[key])
        out[key] = pd.Timestamp(year=q.year, month=q.month, day=1)
    if not out["val_start"] < out["test_start"]:
        raise ValueError(f"degenerate chronological boundaries: {out}")
    return out


def chrono_split(df: pd.DataFrame, bounds: dict) -> pd.Series:
    d = df["Date"]
    part = np.where(d < bounds["val_start"], "train", np.where(d < bounds["test_start"], "val", "test"))
    return pd.Series(part, index=df.index, name="split_B")


def select_transfer_groups(df: pd.DataFrame, rules: dict) -> list[dict]:
    """Pick held-out categories using cleaned row counts only (never outcomes)."""
    groups = []
    eq = df["Equipment"].value_counts()
    cands = eq[eq >= rules["equipment"]["min_rows"]]
    if rules["equipment"].get("exclude_largest", True) and len(cands):
        cands = cands.iloc[1:]
    groups += [{"field": "Equipment", "value": v, "rows": int(n)} for v, n in cands.items()]
    fed = df["Federation"].value_counts().head(rules["federation"]["top_k"])
    groups += [{"field": "Federation", "value": v, "rows": int(n)} for v, n in fed.items()]
    return groups


def transfer_split(df: pd.DataFrame, split_a: pd.Series, field: str, value: str) -> pd.Series:
    """train/val: protocol-A train/val rows outside the group. test_transfer: A-test rows
    inside the group. test_in_dist: A-test rows outside it (same fitted model)."""
    inside = (df[field] == value).to_numpy()
    a = split_a.to_numpy()
    part = np.full(len(df), "excluded", dtype=object)
    part[(a == "train") & ~inside] = "train"
    part[(a == "val") & ~inside] = "val"
    part[(a == "test") & inside] = "test_transfer"
    part[(a == "test") & ~inside] = "test_in_dist"
    return pd.Series(part, index=df.index, name="split_C")


def assert_disjoint(df: pd.DataFrame, split: pd.Series, by_lifter: bool = True) -> None:
    """Row IDs (and, for grouped protocols, lifters) must be pairwise disjoint across partitions."""
    labels = [p for p in split.unique() if p != "excluded"]
    rows = {p: set(df.loc[split == p, "row_id"]) for p in labels}
    lifters = {p: set(df.loc[split == p, "lifter_key"]) for p in labels}
    for i, p in enumerate(labels):
        for q in labels[i + 1:]:
            assert not rows[p] & rows[q], f"row overlap between {p} and {q}"
            fit = {"train", "val"}
            if by_lifter and ({p, q} & fit):
                assert not lifters[p] & lifters[q], f"lifter overlap between {p} and {q}"


def manifest_id(manifest: pd.DataFrame) -> str:
    cols = sorted(manifest.columns)
    h = hashlib.sha256()
    for c in cols:
        h.update(c.encode())
        h.update(pd.util.hash_pandas_object(manifest[c].astype(str), index=False).to_numpy().tobytes())
    return h.hexdigest()[:12]


def balance_table(df: pd.DataFrame, split: pd.Series) -> pd.DataFrame:
    """Covariate summary per partition (no model outputs) for disclosure."""
    rows = []
    for p in sorted(split.unique()):
        sub = df[split.to_numpy() == p]
        rows.append({
            "partition": p,
            "rows": len(sub),
            "lifters": sub["lifter_key"].nunique(),
            "share_female": float((sub["Sex"] == "F").mean()),
            "share_raw": float((sub["Equipment"] == "Raw").mean()),
            "mean_squat": float(sub["Best3SquatKg"].mean()),
            "mean_bench": float(sub["Best3BenchKg"].mean()),
            "mean_deadlift": float(sub["Best3DeadliftKg"].mean()),
            "mean_bodyweight": float(sub["BodyweightKg"].mean()),
            "age_missing": float(sub["Age"].isna().mean()),
            "bodyweight_missing": float(sub["BodyweightKg"].isna().mean()),
            "has_history": float(sub["has_history"].mean()) if "has_history" in sub else np.nan,
            "date_min": sub["Date"].min(),
            "date_max": sub["Date"].max(),
        })
    return pd.DataFrame(rows)
