"""Regression metrics and lifter-level bootstrap."""

from __future__ import annotations

import numpy as np
import pandas as pd


def mae(y, yhat) -> float:
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    return float(np.mean(np.abs(y - yhat))) if len(y) else float("nan")


def pinball(y, q, alpha: float) -> float:
    """Mean pinball (quantile) loss of predicted quantile q at level alpha."""
    d = np.asarray(y, float) - np.asarray(q, float)
    return float(np.mean(np.maximum(alpha * d, (alpha - 1) * d))) if len(d) else float("nan")


def mape(y, yhat) -> tuple[float | None, str | None]:
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    if len(y) == 0:
        return None, "no rows"
    if np.any(y <= 0):
        return None, "MAPE requires strictly positive targets"
    return float(np.mean(np.abs(y - yhat) / y) * 100), None


def r2(y, yhat) -> tuple[float | None, str | None]:
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    if len(y) < 2:
        return None, "fewer than 2 rows"
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    if ss_tot == 0:
        return None, "constant target; R-squared undefined"
    return float(1 - np.sum((y - yhat) ** 2) / ss_tot), None


def lifter_mae(y, yhat, groups) -> float:
    """Each lifter's MAE averaged with equal weight per lifter."""
    err = pd.Series(np.abs(np.asarray(y, float) - np.asarray(yhat, float)))
    return float(err.groupby(np.asarray(groups)).mean().mean()) if len(err) else float("nan")


def summarize(y, yhat, groups, sparse_rows: int = 100, sparse_lifters: int = 30) -> dict:
    m, m_note = mape(y, yhat)
    r, r_note = r2(y, yhat)
    n_lifters = int(pd.Series(groups).nunique())
    out = {
        "rows": int(len(y)), "lifters": n_lifters, "mae": mae(y, yhat), "mape": m, "r2": r,
        "lifter_avg_mae": lifter_mae(y, yhat, groups),
        "sparse": bool(len(y) < sparse_rows or n_lifters < sparse_lifters),
    }
    notes = [n for n in (m_note, r_note) if n]
    if notes:
        out["notes"] = "; ".join(notes)
    return out


def _group_sums(values: np.ndarray, groups) -> tuple[np.ndarray, np.ndarray]:
    codes, _ = pd.factorize(np.asarray(groups))
    sums = np.bincount(codes, weights=values)
    counts = np.bincount(codes).astype(float)
    return sums, counts


def bootstrap_mean_ci(values, groups, reps: int, seed: int, alpha: float = 0.05) -> tuple[float, float]:
    """CI for a row-weighted mean, resampling whole lifters with replacement.

    Used for MAE (values = |error|) and paired MAE differences
    (values = |e_a| - |e_b| on identical rows)."""
    values = np.asarray(values, float)
    if len(values) == 0 or reps <= 0:
        return float("nan"), float("nan")
    sums, counts = _group_sums(values, groups)
    g = len(sums)
    rng = np.random.default_rng(seed)
    stats = np.empty(reps)
    chunk = max(1, int(2e7 // max(g, 1)))
    done = 0
    while done < reps:
        k = min(chunk, reps - done)
        idx = rng.integers(0, g, size=(k, g))
        stats[done:done + k] = sums[idx].sum(axis=1) / counts[idx].sum(axis=1)
        done += k
    return float(np.quantile(stats, alpha / 2)), float(np.quantile(stats, 1 - alpha / 2))
