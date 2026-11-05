"""GRU follow-up: meet sequences must contain only strictly earlier meets of the same lifter."""

import numpy as np
import pandas as pd
import pytest

from deadlift_prediction.features import SEQ_STEP_FEATURES, build_sequence_table, build_sequences

F = {n: i for i, n in enumerate(SEQ_STEP_FEATURES)}


def _aux(rows):
    df = pd.DataFrame(rows)
    df["Date"] = pd.to_datetime(df["Date"])
    for c in ["Deadlift1Kg", "Deadlift2Kg", "Deadlift3Kg", "Best3SquatKg", "Best3BenchKg"]:
        if c not in df:
            df[c] = np.nan
    df["Equipment"] = df["Equipment"].fillna("Raw") if "Equipment" in df else "Raw"
    return df


def test_sequence_strictly_earlier_ordered_padded_and_isolated():
    aux = _aux([
        {"lifter_key": "a", "Event": "D", "Date": "2018-01-01", "Best3DeadliftKg": 200.0},
        {"lifter_key": "a", "Event": "SBD", "Date": "2019-01-01", "Best3DeadliftKg": 220.0, "Best3SquatKg": 180.0, "Best3BenchKg": 110.0,
         "Deadlift1Kg": 200.0, "Deadlift2Kg": 220.0, "Deadlift3Kg": -231.0, "Equipment": "Wraps"},
        {"lifter_key": "a", "Event": "SBD", "Date": "2020-01-01", "Best3DeadliftKg": 999.0},  # target day: never included
        {"lifter_key": "b", "Event": "D", "Date": "2017-01-01", "Best3DeadliftKg": 555.0},
    ])
    table = build_sequence_table(aux)
    target = pd.DataFrame({"lifter_key": ["a", "b"], "Date": pd.to_datetime(["2020-01-01", "2017-01-01"]),
                           "Equipment": ["Raw", "Raw"]})
    seq = build_sequences(target, table, seq_len=4)
    a, b = seq[0], seq[1]
    assert a.shape == (4, len(SEQ_STEP_FEATURES))
    assert list(a[:, F["is_real"]]) == [0, 0, 1, 1]                   # right-aligned, left-padded
    assert a[2, F["dl"]] == pytest.approx(2.0) and a[3, F["dl"]] == pytest.approx(2.2)  # oldest -> newest
    assert a[3, F["sq"]] == pytest.approx(1.8) and a[3, F["has_sq"]] == 1 and a[2, F["has_sq"]] == 0
    assert a[3, F["is_sbd"]] == 1 and a[2, F["is_d"]] == 1
    assert a[3, F["eq_same"]] == 0 and a[2, F["eq_same"]] == 1           # Wraps vs target Raw
    assert a[3, F["att_ratio"]] == pytest.approx(231 / 220 - 1) and a[3, F["has_att"]] == 1
    assert a[3, F["log_days_before"]] == pytest.approx(np.log1p(365 / 30))
    assert not np.isclose(seq[..., F["dl"]], 9.99).any()                  # same-day target never included
    assert not np.isclose(a[..., F["dl"]], 5.55).any()                    # other lifter never included
    assert (b == 0).all()                                                  # only a same-day entry exists for b


def test_sequence_matches_brute_force_and_truncates_to_most_recent():
    rng = np.random.default_rng(0)
    aux = _aux([{"lifter_key": rng.choice(list("abc")), "Event": rng.choice(["SBD", "D"]),
                 "Date": (pd.Timestamp("2010-01-01") + pd.Timedelta(days=int(d))).strftime("%Y-%m-%d"),
                 "Best3DeadliftKg": float(rng.uniform(100, 300))} for d in rng.integers(0, 4000, 150)])
    table = build_sequence_table(aux)
    target = pd.DataFrame({"lifter_key": rng.choice(list("abc"), 60),
                           "Date": pd.Timestamp("2011-01-01") + pd.to_timedelta(rng.integers(0, 3500, 60), unit="D"),
                           "Equipment": "Raw"})
    L = 5
    seq = build_sequences(target, table, seq_len=L)
    for i, r in target.iterrows():
        past = table[(table.lifter_key == r.lifter_key) & (table.Date < r.Date)].sort_values("Date").tail(L)
        real = seq[i][seq[i][:, F["is_real"]] == 1]
        assert len(real) == len(past)
        np.testing.assert_allclose(real[:, F["dl"]], past["dl"].to_numpy(), rtol=1e-6)
