"""Feature allowlists, training-only preprocessing, and past-only history features."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from .data import TARGET

# ---------------------------------------------------------------------------- allowlists
# Every model input must come from one of these named sets. Nothing outside
# ALLOWED_INPUTS may ever be used; `check_allowed` enforces it.

NUMERIC_SAME_MEET = {"Best3SquatKg", "Best3BenchKg", "BodyweightKg", "Age"}
CATEGORICAL_SAME_MEET = {"Sex", "Equipment", "Federation"}
HISTORY_FEATURES = {"prev_squat", "prev_bench", "prev_deadlift", "days_since_prev", "n_prev_meets"}
ALLOWED_INPUTS = NUMERIC_SAME_MEET | CATEGORICAL_SAME_MEET | HISTORY_FEATURES

FORBIDDEN = {
    TARGET, "Best4DeadliftKg", "Deadlift1Kg", "Deadlift2Kg", "Deadlift3Kg", "Deadlift4Kg",
    "TotalKg", "Dots", "Wilks", "Glossbrenner", "Goodlift", "Place", "WeightClassKg",
    "Name", "lifter_key", "row_id", "meet_key", "Date",
}

FEATURE_SETS: dict[str, dict[str, list[str]]] = {
    "A_squat": {"numeric": ["Best3SquatKg"], "categorical": []},
    "B_squat_bench": {"numeric": ["Best3SquatKg", "Best3BenchKg"], "categorical": []},
    "C_plus_demographics": {"numeric": ["Best3SquatKg", "Best3BenchKg", "BodyweightKg", "Age"], "categorical": ["Sex"]},
    "D_plus_equipment": {"numeric": ["Best3SquatKg", "Best3BenchKg", "BodyweightKg", "Age"], "categorical": ["Sex", "Equipment"]},
    # Named extension, reported separately from the core ablation.
    "E_plus_federation": {"numeric": ["Best3SquatKg", "Best3BenchKg", "BodyweightKg", "Age"], "categorical": ["Sex", "Equipment", "Federation"]},
}
HISTORY_NUMERIC = ["prev_squat", "prev_bench", "prev_deadlift", "days_since_prev", "n_prev_meets"]
CORE_ABLATION = ["A_squat", "B_squat_bench", "C_plus_demographics", "D_plus_equipment"]


def feature_spec(name: str) -> dict[str, list[str]]:
    """Resolve a feature-set name; a `+history` suffix appends the history block."""
    base, _, extra = name.partition("+")
    spec = {k: list(v) for k, v in FEATURE_SETS[base].items()}
    if extra == "history":
        spec["numeric"] += HISTORY_NUMERIC
    elif extra:
        raise KeyError(name)
    spec = {"numeric": spec["numeric"], "categorical": spec["categorical"]}
    check_allowed(spec["numeric"] + spec["categorical"])
    return spec


def check_allowed(cols: list[str]) -> None:
    bad = [c for c in cols if c not in ALLOWED_INPUTS or c in FORBIDDEN]
    if bad:
        raise ValueError(f"columns not on the feature allowlist: {bad}")


# ---------------------------------------------------------------------------- preprocessing

UNKNOWN = 0  # categorical code reserved for unseen / infrequent / missing categories


@dataclass
class Preprocessor:
    """Learned on the training partition only.

    numeric: median imputation + missing indicator (only for columns missing in
    train) + standardization. categorical: vocabulary of categories with at least
    `min_count` training rows; everything else (incl. unseen at test time and
    missing) maps to code 0 = unknown.
    """

    numeric: list[str]
    categorical: list[str]
    min_count: int = 1
    medians: dict = field(default_factory=dict)
    means: dict = field(default_factory=dict)
    stds: dict = field(default_factory=dict)
    indicator_cols: list = field(default_factory=list)
    vocab: dict = field(default_factory=dict)
    fitted_rows: int = 0

    def fit(self, df: pd.DataFrame) -> "Preprocessor":
        check_allowed(self.numeric + self.categorical)
        self.fitted_rows = len(df)
        for c in self.numeric:
            x = df[c].astype("float64")
            med = float(x.median()) if x.notna().any() else 0.0
            self.medians[c] = med
            filled = x.fillna(med)
            self.means[c] = float(filled.mean())
            sd = float(filled.std(ddof=0))
            self.stds[c] = sd if sd > 0 else 1.0
            if x.isna().any():
                self.indicator_cols.append(c)
        for c in self.categorical:
            counts = df[c].value_counts(dropna=True)
            keep = sorted(counts[counts >= self.min_count].index.astype(str))
            self.vocab[c] = {v: i + 1 for i, v in enumerate(keep)}
        return self

    # numeric block -----------------------------------------------------------
    def numeric_raw(self, df: pd.DataFrame) -> np.ndarray:
        cols = [df[c].astype("float64").fillna(self.medians[c]).to_numpy() for c in self.numeric]
        return np.column_stack(cols) if cols else np.empty((len(df), 0))

    def indicators(self, df: pd.DataFrame) -> np.ndarray:
        cols = [df[c].isna().to_numpy(dtype="float64") for c in self.indicator_cols]
        return np.column_stack(cols) if cols else np.empty((len(df), 0))

    def codes(self, df: pd.DataFrame) -> np.ndarray:
        cols = []
        for c in self.categorical:
            mapping = self.vocab[c]
            cols.append(df[c].astype("object").map(lambda v: mapping.get(str(v), UNKNOWN) if pd.notna(v) else UNKNOWN).to_numpy(dtype="int64"))
        return np.column_stack(cols) if cols else np.empty((len(df), 0), dtype="int64")

    def dense(self, df: pd.DataFrame) -> np.ndarray:
        """Standardized numerics + indicators + one-hot (unknown column included)."""
        num = self.numeric_raw(df)
        if num.shape[1]:
            mu = np.array([self.means[c] for c in self.numeric])
            sd = np.array([self.stds[c] for c in self.numeric])
            num = (num - mu) / sd
        blocks = [num, self.indicators(df)]
        codes = self.codes(df)
        for j, c in enumerate(self.categorical):
            k = len(self.vocab[c]) + 1
            onehot = np.zeros((len(df), k))
            onehot[np.arange(len(df)), codes[:, j]] = 1.0
            blocks.append(onehot)
        return np.hstack(blocks).astype("float32")

    def dense_names(self) -> list[str]:
        names = list(self.numeric) + [f"{c}__missing" for c in self.indicator_cols]
        for c in self.categorical:
            names += [f"{c}=__unknown__"] + [f"{c}={v}" for v in self.vocab[c]]
        return names

    def tree_frame(self, df: pd.DataFrame) -> pd.DataFrame:
        """Raw numerics (NaN kept, handled natively by LightGBM) + categorical codes."""
        out = pd.DataFrame({c: df[c].astype("float64").to_numpy() for c in self.numeric})
        codes = self.codes(df)
        for j, c in enumerate(self.categorical):
            out[c] = pd.Categorical(codes[:, j], categories=list(range(len(self.vocab[c]) + 1)))
        return out


# ---------------------------------------------------------------------------- history

def add_history(df: pd.DataFrame) -> pd.DataFrame:
    """Previous-meet features computed strictly from earlier dates.

    For each (lifter, date), the "meet" on that day is represented by its row
    with the largest squat+bench+deadlift (ties broken by row_id). The previous
    meet for a target row is the latest such representative with a date strictly
    before the target date. Rows on the same day never see each other, since
    their ordering within a day is unknown. n_prev_meets counts distinct earlier
    dates. Rows without an earlier date get NaN history and has_history=False.
    """
    need = ["lifter_key", "Date", "row_id", "Best3SquatKg", "Best3BenchKg", "Best3DeadliftKg"]
    rep = df[need].copy()
    rep["_sbd"] = rep["Best3SquatKg"] + rep["Best3BenchKg"] + rep["Best3DeadliftKg"]
    rep = rep.sort_values(["lifter_key", "Date", "_sbd", "row_id"], ascending=[True, True, False, True], kind="mergesort")
    rep = rep.drop_duplicates(["lifter_key", "Date"], keep="first")  # one row per lifter-day
    rep = rep.sort_values(["lifter_key", "Date"], kind="mergesort")
    g = rep.groupby("lifter_key", sort=False)
    hist = pd.DataFrame({
        "lifter_key": rep["lifter_key"].to_numpy(),
        "Date": rep["Date"].to_numpy(),
        "prev_date": g["Date"].shift(1).to_numpy(),
        "prev_squat": g["Best3SquatKg"].shift(1).to_numpy(),
        "prev_bench": g["Best3BenchKg"].shift(1).to_numpy(),
        "prev_deadlift": g["Best3DeadliftKg"].shift(1).to_numpy(),
        "n_prev_meets": g.cumcount().to_numpy().astype("float64"),
    })
    out = df.drop(columns=[c for c in [*HISTORY_NUMERIC, "has_history", "prev_date"] if c in df.columns])
    out = out.merge(hist, on=["lifter_key", "Date"], how="left", validate="many_to_one")
    out["days_since_prev"] = (out["Date"] - out["prev_date"]).dt.days.astype("float64")
    out["has_history"] = out["prev_date"].notna()
    assert (out.loc[out["has_history"], "prev_date"] < out.loc[out["has_history"], "Date"]).all()
    return out
