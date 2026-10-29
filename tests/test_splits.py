import numpy as np
import pandas as pd
import pytest

from deadlift_prediction.splits import (assert_disjoint, chrono_boundaries, chrono_split, group_split,
                                        select_transfer_groups, transfer_split)


def _df(n_lifters=300, per=4, seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n_lifters):
        eq = ["Raw", "Wraps", "Single-ply"][i % 3]
        fed = ["F1", "F2", "F3", "F4"][rng.integers(0, 4)]
        for j in range(per):
            rows.append({"lifter_key": f"L{i}", "row_id": f"L{i}_{j}", "Equipment": eq if j < 3 else "Raw",
                         "Federation": fed, "Date": pd.Timestamp("2010-01-01") + pd.Timedelta(days=int(rng.integers(0, 4000)))})
    return pd.DataFrame(rows)


def test_group_split_disjoint_and_deterministic():
    df = _df()
    s1 = group_split(df, {"train": 0.7, "val": 0.15, "test": 0.15}, 42)
    s2 = group_split(df.sample(frac=1, random_state=3), {"train": 0.7, "val": 0.15, "test": 0.15}, 42)
    assert (s1 == s2.reindex(s1.index)).all()
    assert_disjoint(df, s1)
    for p in ["train", "val", "test"]:
        others = set(df.loc[s1 != p, "lifter_key"])
        assert not set(df.loc[s1 == p, "lifter_key"]) & others
    assert 0.6 < (s1 == "train").mean() < 0.8


def test_assert_disjoint_catches_lifter_overlap():
    df = pd.DataFrame({"lifter_key": ["a", "a"], "row_id": ["1", "2"]})
    with pytest.raises(AssertionError):
        assert_disjoint(df, pd.Series(["train", "test"]))


def test_chrono_intervals_ordered_and_non_overlapping():
    df = _df()
    b = chrono_boundaries(df["Date"], {"val_start": 0.7, "test_start": 0.85})
    s = chrono_split(df, b)
    tr, va, te = (df.loc[s == p, "Date"] for p in ["train", "val", "test"])
    assert tr.max() < b["val_start"] <= va.min()
    assert va.max() < b["test_start"] <= te.min()
    assert b["val_start"].day == 1 and b["test_start"].day == 1


def test_transfer_holdout_never_in_fit_and_test_lifters_removed():
    df = _df()
    a = group_split(df, {"train": 0.7, "val": 0.15, "test": 0.15}, 42)
    for field, value in [("Equipment", "Wraps"), ("Federation", "F2")]:
        c = transfer_split(df, a, field, value)
        fit = c.isin(["train", "val"])
        assert not (df.loc[fit, field] == value).any()
        assert (df.loc[c == "test_transfer", field] == value).all()
        test_lifters = set(df.loc[a == "test", "lifter_key"])
        assert not set(df.loc[fit, "lifter_key"]) & test_lifters
        assert_disjoint(df, c)


def test_transfer_selection_uses_counts_only():
    df = _df()
    rules = {"equipment": {"min_rows": 100, "exclude_largest": True}, "federation": {"top_k": 2}}
    g = select_transfer_groups(df, rules)
    eq = [x["value"] for x in g if x["field"] == "Equipment"]
    assert "Raw" not in eq and set(eq) == {"Wraps", "Single-ply"}
    assert len([x for x in g if x["field"] == "Federation"]) == 2
