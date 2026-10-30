import numpy as np
import pandas as pd
import pytest

from deadlift_prediction.features import add_history
from conftest import lifter_frame


def test_history_strictly_earlier_and_ordered():
    df = lifter_frame([
        {"lifter_key": "a", "Date": "2020-03-01", "Best3DeadliftKg": 230.0},
        {"lifter_key": "a", "Date": "2019-01-01", "Best3DeadliftKg": 210.0},
        {"lifter_key": "a", "Date": "2021-06-01", "Best3DeadliftKg": 260.0},
        {"lifter_key": "b", "Date": "2020-03-01", "Best3DeadliftKg": 100.0},
    ])
    h = add_history(df).set_index("row_id")
    assert np.isnan(h.loc["r1", "prev_deadlift"]) and not h.loc["r1", "has_history"]
    assert h.loc["r0", "prev_deadlift"] == 210.0 and h.loc["r0", "n_prev_meets"] == 1
    assert h.loc["r2", "prev_deadlift"] == 230.0 and h.loc["r2", "n_prev_meets"] == 2
    assert h.loc["r0", "days_since_prev"] == (pd.Timestamp("2020-03-01") - pd.Timestamp("2019-01-01")).days
    assert not h.loc["r3", "has_history"]  # other lifters never leak in
    # current deadlift never appears as its own history
    assert (h["prev_deadlift"] != h["Best3DeadliftKg"]).all() or h["prev_deadlift"].isna().any()


def test_same_day_rows_never_see_each_other():
    df = lifter_frame([
        {"lifter_key": "a", "Date": "2020-01-01", "Best3DeadliftKg": 200.0},
        {"lifter_key": "a", "Date": "2020-05-01", "Best3DeadliftKg": 220.0, "Equipment": "Raw"},
        {"lifter_key": "a", "Date": "2020-05-01", "Best3DeadliftKg": 240.0, "Equipment": "Wraps"},
        {"lifter_key": "a", "Date": "2020-09-01", "Best3DeadliftKg": 250.0},
    ])
    h = add_history(df).set_index("row_id")
    # both same-day rows look back to Jan, not to each other
    assert h.loc["r1", "prev_deadlift"] == 200.0 and h.loc["r2", "prev_deadlift"] == 200.0
    assert h.loc["r1", "n_prev_meets"] == 1 and h.loc["r2", "n_prev_meets"] == 1
    # the later meet uses one deterministic same-day representative (largest SBD total)
    assert h.loc["r3", "prev_deadlift"] == 240.0 and h.loc["r3", "n_prev_meets"] == 2


def test_history_independent_of_input_order():
    rows = [{"lifter_key": k, "Date": d, "Best3DeadliftKg": float(v)}
            for k in "abc" for d, v in [("2018-01-01", 100), ("2019-01-01", 110), ("2019-01-01", 120), ("2020-01-01", 130)]]
    df = lifter_frame(rows)
    a = add_history(df).sort_values("row_id").reset_index(drop=True)
    b = add_history(df.sample(frac=1, random_state=1)).sort_values("row_id").reset_index(drop=True)
    pd.testing.assert_frame_equal(a, b)
    assert (a.loc[a["has_history"], "prev_date"] < a.loc[a["has_history"], "Date"]).all()


def test_rich_history_uses_only_strictly_earlier_meets():
    df = lifter_frame([
        {"lifter_key": "a", "Date": "2018-01-01", "Best3SquatKg": 200.0, "Best3BenchKg": 100.0, "Best3DeadliftKg": 240.0, "Equipment": "Raw"},
        {"lifter_key": "a", "Date": "2019-01-01", "Best3SquatKg": 250.0, "Best3BenchKg": 120.0, "Best3DeadliftKg": 250.0, "Equipment": "Single-ply"},
        {"lifter_key": "a", "Date": "2020-01-01", "Best3SquatKg": 210.0, "Best3BenchKg": 110.0, "Best3DeadliftKg": 300.0, "Equipment": "Raw"},  # same-day pair
        {"lifter_key": "a", "Date": "2020-01-01", "Best3SquatKg": 205.0, "Best3BenchKg": 105.0, "Best3DeadliftKg": 260.0, "Equipment": "Wraps"},
        {"lifter_key": "a", "Date": "2021-01-01", "Best3SquatKg": 220.0, "Best3BenchKg": 115.0, "Best3DeadliftKg": 999.0, "Equipment": "Raw"},
    ])
    h = add_history(df).set_index("row_id")
    first = h.loc["r0"]
    assert not first["has_history"]
    for c in ["best_prev_deadlift", "mean_prev_dl_sq_ratio", "prev2_deadlift", "days_since_first", "prev_same_equipment"]:
        assert np.isnan(first[c])
    r1 = h.loc["r1"]
    assert r1["best_prev_deadlift"] == 240.0 and np.isnan(r1["prev2_deadlift"])
    assert r1["mean_prev_dl_sq_ratio"] == pytest.approx(240 / 200) and r1["prev_same_equipment"] == 0.0
    # same-day rows: identical history from the two earlier meets only; never their own lifts
    for rid in ["r2", "r3"]:
        r = h.loc[rid]
        assert r["best_prev_deadlift"] == 250.0 and r["best_prev_squat"] == 250.0 and r["prev2_deadlift"] == 240.0
        assert r["mean_prev_dl_sq_ratio"] == pytest.approx((240 / 200 + 250 / 250) / 2)
        assert r["days_since_first"] == (pd.Timestamp("2020-01-01") - pd.Timestamp("2018-01-01")).days
    assert h.loc["r2", "prev_same_equipment"] == 0.0  # prev meet Single-ply vs Raw
    # later meet: same-day representative is the larger-total row (r2, 300 kg)
    r4 = h.loc["r4"]
    assert r4["best_prev_deadlift"] == 300.0 and r4["prev2_deadlift"] == 250.0 and r4["prev_same_equipment"] == 1.0
    assert r4["mean_prev_dl_sq_ratio"] == pytest.approx((240 / 200 + 250 / 250 + 300 / 210) / 3)
    # the current (999 kg) deadlift never appears in any history column
    assert not (h[["best_prev_deadlift", "prev_deadlift", "prev2_deadlift"]] == 999.0).any().any()


def test_rich_feature_set_is_allowlisted():
    from deadlift_prediction.features import FORBIDDEN, HISTORY_RICH, feature_spec

    spec = feature_spec("D_plus_equipment+history_rich")
    assert set(HISTORY_RICH) <= set(spec["numeric"]) and not set(spec["numeric"]) & FORBIDDEN
