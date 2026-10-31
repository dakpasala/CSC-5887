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
# Follow-up experiment (added after the main test results were reported; tuned on
# validation only): career summaries over all strictly earlier meets.
HISTORY_RICH_FEATURES = {"best_prev_squat", "best_prev_bench", "best_prev_deadlift", "mean_prev_dl_sq_ratio",
                         "mean_prev_dl_sb_ratio", "prev2_deadlift", "days_since_first", "prev_same_equipment"}
HISTORY_FEATURES = HISTORY_FEATURES | HISTORY_RICH_FEATURES
# Expanded-input follow-up (team-approved widening of the allowlist). Same-meet
# squat/bench attempt summaries (never deadlift attempts), filled age, context
# categoricals, and deadlift history from earlier meets of any event type.
ATTEMPT_FEATURES = ["squat_opener_ratio", "squat_third_ratio", "squat_n_good",
                    "bench_opener_ratio", "bench_third_ratio", "bench_n_good"]
CONTEXT_NUMERIC = ["age_filled", "age_from_class", "meet_year"]
CONTEXT_CATEGORICAL = ["Tested", "Country", "ParentFederation"]
ANYHIST_FEATURES = ["prev_any_deadlift", "best_prev_any_deadlift", "n_prev_any_deadlift_meets",
                    "days_since_prev_any_deadlift", "prev_any_was_sbd"]
NUMERIC_SAME_MEET = NUMERIC_SAME_MEET | set(ATTEMPT_FEATURES) | set(CONTEXT_NUMERIC)
CATEGORICAL_SAME_MEET = CATEGORICAL_SAME_MEET | set(CONTEXT_CATEGORICAL)
HISTORY_FEATURES = HISTORY_FEATURES | set(ANYHIST_FEATURES)
ALLOWED_INPUTS = NUMERIC_SAME_MEET | CATEGORICAL_SAME_MEET | HISTORY_FEATURES

FORBIDDEN = {
    TARGET, "Best4DeadliftKg", "Deadlift1Kg", "Deadlift2Kg", "Deadlift3Kg", "Deadlift4Kg",
    "TotalKg", "Dots", "Wilks", "Glossbrenner", "Goodlift", "Place", "WeightClassKg",
    "Name", "lifter_key", "row_id", "meet_key", "Date", "Squat4Kg", "Bench4Kg", "Division",
}

FEATURE_SETS: dict[str, dict[str, list[str]]] = {
    "A_squat": {"numeric": ["Best3SquatKg"], "categorical": []},
    "B_squat_bench": {"numeric": ["Best3SquatKg", "Best3BenchKg"], "categorical": []},
    "C_plus_demographics": {"numeric": ["Best3SquatKg", "Best3BenchKg", "BodyweightKg", "Age"], "categorical": ["Sex"]},
    "D_plus_equipment": {"numeric": ["Best3SquatKg", "Best3BenchKg", "BodyweightKg", "Age"], "categorical": ["Sex", "Equipment"]},
    # Named extension, reported separately from the core ablation.
    "E_plus_federation": {"numeric": ["Best3SquatKg", "Best3BenchKg", "BodyweightKg", "Age"], "categorical": ["Sex", "Equipment", "Federation"]},
    # Expanded-input follow-up.
    "X_attempts": {"numeric": ["Best3SquatKg", "Best3BenchKg", "BodyweightKg", "Age", *ATTEMPT_FEATURES],
                   "categorical": ["Sex", "Equipment"]},
    "X_context": {"numeric": ["Best3SquatKg", "Best3BenchKg", "BodyweightKg", "Age", *CONTEXT_NUMERIC],
                  "categorical": ["Sex", "Equipment", "Federation", *CONTEXT_CATEGORICAL]},
    "X_all": {"numeric": ["Best3SquatKg", "Best3BenchKg", "BodyweightKg", "Age", *ATTEMPT_FEATURES, *CONTEXT_NUMERIC],
              "categorical": ["Sex", "Equipment", "Federation", *CONTEXT_CATEGORICAL]},
}
HISTORY_NUMERIC = ["prev_squat", "prev_bench", "prev_deadlift", "days_since_prev", "n_prev_meets"]
HISTORY_RICH = ["best_prev_squat", "best_prev_bench", "best_prev_deadlift", "mean_prev_dl_sq_ratio",
                "mean_prev_dl_sb_ratio", "prev2_deadlift", "days_since_first", "prev_same_equipment"]
CORE_ABLATION = ["A_squat", "B_squat_bench", "C_plus_demographics", "D_plus_equipment"]


def feature_spec(name: str) -> dict[str, list[str]]:
    """Resolve a feature-set name. Suffixes (combinable, joined by `+`):
    `history` (previous meet), `history_rich` (previous meet + career summaries),
    `anyhist` (deadlift history from earlier meets of any event type)."""
    base, *extras = name.split("+")
    spec = {k: list(v) for k, v in FEATURE_SETS[base].items()}
    for extra in extras:
        if extra == "history":
            spec["numeric"] += HISTORY_NUMERIC
        elif extra == "history_rich":
            spec["numeric"] += HISTORY_NUMERIC + HISTORY_RICH
        elif extra == "anyhist":
            spec["numeric"] += ANYHIST_FEATURES
        else:
            raise KeyError(name)
    spec = {"numeric": list(dict.fromkeys(spec["numeric"])), "categorical": spec["categorical"]}
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
    """Past-only history features computed strictly from earlier dates.

    For each (lifter, date), the "meet" on that day is represented by its row
    with the largest squat+bench+deadlift (ties broken by row_id). The previous
    meet for a target row is the latest such representative with a date strictly
    before the target date. Rows on the same day never see each other, since
    their ordering within a day is unknown. n_prev_meets counts distinct earlier
    dates. Rows without an earlier date get NaN history and has_history=False.

    Career summaries (best_prev_*, mean_prev_* ratios, prev2_deadlift,
    days_since_first) aggregate over all strictly earlier representatives.
    prev_same_equipment compares the previous meet's equipment with the target
    row's own equipment.
    """
    need = ["lifter_key", "Date", "row_id", "Best3SquatKg", "Best3BenchKg", "Best3DeadliftKg"]
    has_eq = "Equipment" in df.columns
    rep = df[need + (["Equipment"] if has_eq else [])].copy()
    rep["_sbd"] = rep["Best3SquatKg"] + rep["Best3BenchKg"] + rep["Best3DeadliftKg"]
    rep = rep.sort_values(["lifter_key", "Date", "_sbd", "row_id"], ascending=[True, True, False, True], kind="mergesort")
    rep = rep.drop_duplicates(["lifter_key", "Date"], keep="first")  # one row per lifter-day
    rep = rep.sort_values(["lifter_key", "Date"], kind="mergesort").reset_index(drop=True)
    rep["_r_sq"] = rep["Best3DeadliftKg"] / rep["Best3SquatKg"]
    rep["_r_sb"] = rep["Best3DeadliftKg"] / (rep["Best3SquatKg"] + rep["Best3BenchKg"])
    g = rep.groupby("lifter_key", sort=False)
    n_prev = g.cumcount().to_numpy().astype("float64")
    with np.errstate(invalid="ignore", divide="ignore"):
        mean_sq = (g["_r_sq"].cumsum() - rep["_r_sq"]).to_numpy() / n_prev
        mean_sb = (g["_r_sb"].cumsum() - rep["_r_sb"]).to_numpy() / n_prev
    hist = pd.DataFrame({
        "lifter_key": rep["lifter_key"].to_numpy(),
        "Date": rep["Date"].to_numpy(),
        "prev_date": g["Date"].shift(1).to_numpy(),
        "prev_squat": g["Best3SquatKg"].shift(1).to_numpy(),
        "prev_bench": g["Best3BenchKg"].shift(1).to_numpy(),
        "prev_deadlift": g["Best3DeadliftKg"].shift(1).to_numpy(),
        "n_prev_meets": n_prev,
        "prev2_deadlift": g["Best3DeadliftKg"].shift(2).to_numpy(),
        "first_date": g["Date"].transform("first").to_numpy(),
        "mean_prev_dl_sq_ratio": np.where(n_prev > 0, mean_sq, np.nan),
        "mean_prev_dl_sb_ratio": np.where(n_prev > 0, mean_sb, np.nan),
    })
    for lift, name in [("Best3SquatKg", "best_prev_squat"), ("Best3BenchKg", "best_prev_bench"),
                       ("Best3DeadliftKg", "best_prev_deadlift")]:
        hist[name] = g[lift].cummax().groupby(rep["lifter_key"], sort=False).shift(1).to_numpy()
    if has_eq:
        hist["_prev_eq"] = g["Equipment"].shift(1).to_numpy()

    drop = [*HISTORY_NUMERIC, *HISTORY_RICH, "has_history", "prev_date"]
    out = df.drop(columns=[c for c in drop if c in df.columns])
    out = out.merge(hist, on=["lifter_key", "Date"], how="left", validate="many_to_one")
    out["has_history"] = out["prev_date"].notna()
    out["days_since_prev"] = (out["Date"] - out["prev_date"]).dt.days.astype("float64")
    out["days_since_first"] = np.where(out["has_history"], (out["Date"] - out["first_date"]).dt.days, np.nan)
    if has_eq:
        same = (out["_prev_eq"] == out["Equipment"]).astype("float64")
        out["prev_same_equipment"] = same.where(out["has_history"])
        out = out.drop(columns="_prev_eq")
    else:
        out["prev_same_equipment"] = np.nan
    out = out.drop(columns="first_date")
    assert (out.loc[out["has_history"], "prev_date"] < out.loc[out["has_history"], "Date"]).all()
    return out


# ---------------------------------------------------------------------------- expanded inputs

def _class_mid(s: pd.Series) -> pd.Series:
    """'40-44' -> 42; open-ended '80-999' -> 82; anything else -> NaN."""
    parts = s.astype("string").str.extract(r"^(\d+)-(\d+)$")
    lo = pd.to_numeric(parts[0], errors="coerce").astype("float64").to_numpy()
    hi = pd.to_numeric(parts[1], errors="coerce").astype("float64").to_numpy()
    with np.errstate(invalid="ignore"):
        mid = np.where(hi >= 200, lo + 2, (lo + hi) / 2)
    return pd.Series(mid, index=s.index, dtype="float64")


def add_same_meet_extras(df: pd.DataFrame) -> pd.DataFrame:
    """Row-wise derived inputs (nothing learned, no target used).

    Attempts: negative values are failed attempts (OPL convention), so the
    attempted weight is |value|. opener_ratio = |attempt 1| / best;
    third_ratio = |attempt 3| / best (> 1 when a heavier third was missed);
    n_good = successful attempts among 1-3. Missing when the federation does not
    report attempts. Age: recorded Age, else the AgeClass midpoint, else the
    BirthYearClass midpoint; age_from_class flags the fill.
    """
    out = df.copy()
    for lift, best in [("Squat", "Best3SquatKg"), ("Bench", "Best3BenchKg")]:
        att = out[[f"{lift}{i}Kg" for i in (1, 2, 3)]].astype("float64")
        reported = att.notna().any(axis=1)
        key = lift.lower()
        out[f"{key}_opener_ratio"] = att[f"{lift}1Kg"].abs() / out[best]
        out[f"{key}_third_ratio"] = att[f"{lift}3Kg"].abs() / out[best]
        out[f"{key}_n_good"] = (att > 0).sum(axis=1).astype("float64").where(reported)
    cls = _class_mid(out["AgeClass"]).fillna(_class_mid(out["BirthYearClass"]))
    out["age_filled"] = out["Age"].fillna(cls)
    out["age_from_class"] = (out["Age"].isna() & cls.notna()).astype("float64")
    out["meet_year"] = out["Date"].dt.year.astype("float64")
    out["Tested"] = np.where(out["Tested"].astype("string").fillna("") == "Yes", "Yes", "No")
    return out


def add_any_history(df: pd.DataFrame, aux: pd.DataFrame) -> pd.DataFrame:
    """Deadlift history from strictly earlier meets of any event type.

    `aux` has lifter_key, Event, Date, Best3DeadliftKg (successful deadlifts
    from SBD, D, BD and SD entries). Per lifter-day the largest deadlift
    represents that day. For each target row, the latest representative with a
    date strictly before the target date supplies the features; same-day
    entries are never used. Missing when no earlier deadlift exists.
    """
    rep = aux.sort_values(["lifter_key", "Date", "Best3DeadliftKg"], ascending=[True, True, False], kind="mergesort")
    rep = rep.drop_duplicates(["lifter_key", "Date"], keep="first").reset_index(drop=True)
    g = rep.groupby("lifter_key", sort=False)
    rep = pd.DataFrame({
        "lifter_key": rep["lifter_key"], "_aux_date": rep["Date"],
        "prev_any_deadlift": rep["Best3DeadliftKg"],
        "best_prev_any_deadlift": g["Best3DeadliftKg"].cummax(),
        "n_prev_any_deadlift_meets": (g.cumcount() + 1).astype("float64"),
        "prev_any_was_sbd": (rep["Event"] == "SBD").astype("float64"),
    }).sort_values("_aux_date", kind="mergesort")
    out = df.drop(columns=[c for c in [*ANYHIST_FEATURES, "_aux_date"] if c in df.columns])
    order = out["Date"].argsort(kind="mergesort")
    tgt = out.iloc[order][["lifter_key", "Date"]].reset_index()
    m = pd.merge_asof(tgt, rep, left_on="Date", right_on="_aux_date", by="lifter_key",
                      allow_exact_matches=False, direction="backward")
    m = m.set_index("index").reindex(out.index)
    for c in ["prev_any_deadlift", "best_prev_any_deadlift", "n_prev_any_deadlift_meets", "prev_any_was_sbd"]:
        out[c] = m[c].to_numpy()
    out["days_since_prev_any_deadlift"] = (out["Date"] - m["_aux_date"]).dt.days.astype("float64").to_numpy()
    has = out["prev_any_deadlift"].notna()
    assert (out.loc[has, "days_since_prev_any_deadlift"] > 0).all(), "any-event history must be strictly earlier"
    out["has_any_history"] = has
    return out
