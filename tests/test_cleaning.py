import numpy as np

from deadlift_prediction.data import CLEAN_COLUMNS, clean
from conftest import raw_rows


def test_nonpositive_missing_invalid_lifts_excluded(cfg):
    raw = raw_rows([
        {"Name": "ok"},
        {"Name": "neg", "Best3DeadliftKg": "-250"},
        {"Name": "zero", "Best3SquatKg": "0"},
        {"Name": "missing", "Best3BenchKg": None},
        {"Name": "text", "Best3DeadliftKg": "abc"},
        {"Name": "bench_only", "Event": "B"},
    ])
    df, log, _ = clean(raw, cfg)
    assert len(df) == 1
    assert (df[["Best3SquatKg", "Best3BenchKg", "Best3DeadliftKg"]] > 0).all().all()
    removed = {e["step"]: e["rows_removed"] for e in log}
    assert removed["event_is_SBD"] == 1
    assert removed["Best3DeadliftKg_finite_positive"] == 2


def test_missing_and_invalid_age_kept_as_nan(cfg):
    raw = raw_rows([{"Name": "a", "Age": None}, {"Name": "b", "Age": "250"}, {"Name": "c", "Age": "23.5"},
                    {"Name": "d", "BodyweightKg": "5"}])
    df, _, audit = clean(raw, cfg)
    assert len(df) == 4
    assert df["Age"].isna().sum() == 2
    assert df["BodyweightKg"].isna().sum() == 1
    assert audit["set_to_missing"]["age_out_of_range"] == 1


def test_exact_and_repeated_listings_removed_but_distinct_lifters_kept(cfg):
    raw = raw_rows([
        {"Name": "X"},
        {"Name": "X"},                                   # exact duplicate
        {"Name": "X", "Division": "Juniors"},            # same performance, other division
        {"Name": "X", "Federation": "F2"},               # cross-listed under another federation
        {"Name": "X #2"},                                # different lifter, identical lifts
        {"Name": "Y"},                                   # different lifter, identical lifts
        {"Name": "X", "Equipment": "Wraps"},             # distinct entry (other equipment)
    ])
    df, log, audit = clean(raw, cfg)
    assert len(df) == 4
    assert df["lifter_key"].nunique() == 3
    assert audit["repeated_listings"]["removed"] == 2


def test_post_outcome_columns_dropped(cfg):
    df, _, _ = clean(raw_rows([{"Name": "a"}]), cfg)
    assert list(df.columns) == CLEAN_COLUMNS
    for c in ["TotalKg", "Place", "Dots", "Wilks", "Name"]:
        assert c not in df.columns


def test_lifter_subsample_is_by_identity(cfg):
    cfg = {**cfg, "data": {**cfg["data"], "lifter_fraction": 0.5}}
    raw = raw_rows([{"Name": f"L{i}", "Date": f"20{10 + j}-01-01"} for i in range(200) for j in range(3)])
    df, _, _ = clean(raw, cfg)
    per = df.groupby("lifter_key").size()
    assert (per == 3).all()  # whole lifters kept or dropped
    assert 50 < len(per) < 150
