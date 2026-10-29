import numpy as np
import pandas as pd

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
