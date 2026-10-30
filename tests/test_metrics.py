import numpy as np
import pytest

from deadlift_prediction.metrics import bootstrap_mean_ci, lifter_mae, mae, mape, r2, summarize


def test_hand_calculated():
    y, yhat = [100.0, 200.0, 300.0], [110.0, 190.0, 330.0]
    assert mae(y, yhat) == pytest.approx(50 / 3)
    assert mape(y, yhat)[0] == pytest.approx((10 + 5 + 10) / 3)
    # SS_res = 100+100+900 = 1100; SS_tot = 20000
    assert r2(y, yhat)[0] == pytest.approx(1 - 1100 / 20000)


def test_r2_negative_and_undefined():
    assert r2([1.0, 2.0, 3.0], [3.0, 3.0, 0.0])[0] < 0
    val, note = r2([5.0, 5.0], [5.0, 4.0])
    assert val is None and "constant" in note
    assert r2([1.0], [1.0])[0] is None
    assert mape([0.0, 1.0], [1.0, 1.0])[0] is None


def test_lifter_mae_weights_lifters_equally():
    y, yhat, g = [0, 0, 0, 0], [1, 1, 1, 9], ["a", "a", "a", "b"]
    assert mae(y, yhat) == 3.0
    assert lifter_mae(y, yhat, g) == 5.0
    s = summarize(y, yhat, g, sparse_rows=10, sparse_lifters=1)
    assert s["sparse"] and s["rows"] == 4 and s["lifters"] == 2


def test_bootstrap_by_lifter_brackets_mean():
    rng = np.random.default_rng(0)
    g = np.repeat(np.arange(200), 5)
    v = rng.exponential(10, size=len(g))
    lo, hi = bootstrap_mean_ci(v, g, reps=200, seed=1)
    assert lo < v.mean() < hi
    # constant within-lifter -> resampling lifters is the only source of variation
    lo2, hi2 = bootstrap_mean_ci(np.ones(10), np.repeat([0, 1], 5), reps=50, seed=1)
    assert lo2 == hi2 == 1.0


def test_pinball_hand_calculated():
    from deadlift_prediction.metrics import pinball

    # y - q = [10, -10]: alpha=0.9 -> (0.9*10 + 0.1*10)/2 = 5
    assert pinball([110.0, 90.0], [100.0, 100.0], 0.9) == pytest.approx(5.0)
    assert pinball([100.0], [100.0], 0.1) == 0.0


def test_conformal_correction_reaches_target_coverage():
    from deadlift_prediction.intervals import conformal_correction

    rng = np.random.default_rng(0)
    y = rng.normal(0, 10, 20000)
    lo, hi = np.full_like(y, -5.0), np.full_like(y, 5.0)  # too narrow (~38% coverage)
    q = conformal_correction(y, lo, hi, 0.8)
    y2 = rng.normal(0, 10, 20000)  # fresh data stands in for test
    cov = np.mean((y2 >= lo - q) & (y2 <= hi + q))
    assert q > 0 and abs(cov - 0.8) < 0.015
    # an over-wide range is narrowed (negative correction)
    assert conformal_correction(y, np.full_like(y, -50.0), np.full_like(y, 50.0), 0.8) < 0
