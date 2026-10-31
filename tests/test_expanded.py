"""Leakage and correctness checks for the expanded-input follow-up."""

import numpy as np
import pandas as pd
import pytest

from deadlift_prediction.features import (ANYHIST_FEATURES, ATTEMPT_FEATURES, FEATURE_SETS, FORBIDDEN,
                                          add_any_history, add_same_meet_extras, feature_spec)


def _row(**kw):
    base = {"Best3SquatKg": 200.0, "Best3BenchKg": 100.0, "Squat1Kg": 180.0, "Squat2Kg": 200.0, "Squat3Kg": -210.0,
            "Bench1Kg": 90.0, "Bench2Kg": -100.0, "Bench3Kg": 100.0, "Age": np.nan, "AgeClass": "40-44",
            "BirthYearClass": None, "Tested": None, "Date": pd.Timestamp("2020-05-01")}
    return {**base, **kw}


def test_no_deadlift_or_score_columns_in_any_expanded_set():
    for name in ["X_attempts", "X_context", "X_all", "X_all+anyhist", "X_all+history_rich+anyhist"]:
        spec = feature_spec(name)
        cols = spec["numeric"] + spec["categorical"]
        assert not set(cols) & FORBIDDEN
        assert not any(c.lower().startswith("deadlift") for c in cols)
    assert {"Squat4Kg", "Bench4Kg", "Deadlift1Kg", "TotalKg", "Place"} <= FORBIDDEN


def test_attempt_and_age_features_hand_calculated():
    df = add_same_meet_extras(pd.DataFrame([
        _row(),
        _row(Squat1Kg=np.nan, Squat2Kg=np.nan, Squat3Kg=np.nan, Age=30.0, AgeClass="80-999", Tested="Yes"),
        _row(Age=np.nan, AgeClass=None, BirthYearClass="70-999"),
    ]))
    r = df.iloc[0]
    assert r["squat_opener_ratio"] == pytest.approx(0.9)
    assert r["squat_third_ratio"] == pytest.approx(1.05)  # missed heavier third (negative = failed)
    assert r["squat_n_good"] == 2 and r["bench_n_good"] == 2
    assert r["age_filled"] == 42 and r["age_from_class"] == 1 and r["meet_year"] == 2020 and r["Tested"] == "No"
    r = df.iloc[1]
    assert np.isnan(r["squat_n_good"]) and np.isnan(r["squat_opener_ratio"])  # not reported -> missing, not zero
    assert r["age_filled"] == 30 and r["age_from_class"] == 0 and r["Tested"] == "Yes"
    assert df.iloc[2]["age_filled"] == 72


def test_any_event_history_strictly_earlier_and_cross_event():
    target = pd.DataFrame({"lifter_key": ["a", "a", "b"], "row_id": ["t1", "t2", "t3"],
                           "Date": pd.to_datetime(["2020-06-01", "2021-06-01", "2020-06-01"])})
    aux = pd.DataFrame({
        "lifter_key": ["a", "a", "a", "a", "b"],
        "Event": ["D", "BD", "SBD", "SBD", "D"],
        "Date": pd.to_datetime(["2019-01-01", "2020-06-01", "2020-06-01", "2021-06-01", "2020-06-01"]),
        "Best3DeadliftKg": [200.0, 230.0, 240.0, 999.0, 150.0],
    })
    h = add_any_history(target, aux).set_index("row_id")
    t1 = h.loc["t1"]  # SBD first-timer with an earlier deadlift-only meet; same-day BD/SBD never used
    assert t1["prev_any_deadlift"] == 200.0 and t1["n_prev_any_deadlift_meets"] == 1 and t1["prev_any_was_sbd"] == 0
    assert t1["days_since_prev_any_deadlift"] == (pd.Timestamp("2020-06-01") - pd.Timestamp("2019-01-01")).days
    t2 = h.loc["t2"]  # previous lifter-day represented by its largest deadlift (240 from SBD)
    assert t2["prev_any_deadlift"] == 240.0 and t2["best_prev_any_deadlift"] == 240.0
    assert t2["n_prev_any_deadlift_meets"] == 2 and t2["prev_any_was_sbd"] == 1
    assert not (h[ANYHIST_FEATURES] == 999.0).any().any()  # current deadlift never leaks in
    assert not h.loc["t3", "has_any_history"]  # only a same-day entry exists -> no history
    for c in ANYHIST_FEATURES:
        assert np.isnan(h.loc["t3", c])


def test_any_event_history_is_order_independent():
    rng = np.random.default_rng(0)
    target = pd.DataFrame({"lifter_key": rng.choice(list("abcde"), 200), "row_id": [f"r{i}" for i in range(200)],
                           "Date": pd.Timestamp("2015-01-01") + pd.to_timedelta(rng.integers(0, 3000, 200), unit="D")})
    aux = pd.DataFrame({"lifter_key": rng.choice(list("abcde"), 300), "Event": rng.choice(["D", "SBD", "BD"], 300),
                        "Date": pd.Timestamp("2014-01-01") + pd.to_timedelta(rng.integers(0, 3500, 300), unit="D"),
                        "Best3DeadliftKg": rng.uniform(100, 300, 300)})
    a = add_any_history(target, aux).sort_values("row_id").reset_index(drop=True)
    b = add_any_history(target.sample(frac=1, random_state=2), aux.sample(frac=1, random_state=3))
    b = b.sort_values("row_id").reset_index(drop=True)
    pd.testing.assert_frame_equal(a, b)
    # brute-force check of the most recent strictly-earlier deadlift
    for _, r in a.sample(40, random_state=1).iterrows():
        past = aux[(aux.lifter_key == r.lifter_key) & (aux.Date < r.Date)]
        if past.empty:
            assert np.isnan(r.prev_any_deadlift)
        else:
            last = past[past.Date == past.Date.max()]
            assert r.prev_any_deadlift == pytest.approx(last.Best3DeadliftKg.max())
            assert r.best_prev_any_deadlift == pytest.approx(past.Best3DeadliftKg.max())
