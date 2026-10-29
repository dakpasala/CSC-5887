import numpy as np
import pandas as pd
import pytest

from deadlift_prediction.features import (FEATURE_SETS, FORBIDDEN, UNKNOWN, Preprocessor, check_allowed,
                                          feature_spec)


@pytest.mark.parametrize("col", ["Best3DeadliftKg", "TotalKg", "Dots", "Wilks", "Glossbrenner", "Goodlift", "Place",
                                 "Deadlift3Kg", "Best4DeadliftKg", "lifter_key", "Date", "Name", "WeightClassKg"])
def test_forbidden_columns_rejected(col):
    with pytest.raises(ValueError):
        check_allowed([col])
    with pytest.raises(ValueError):
        Preprocessor([col], []).fit(pd.DataFrame({col: [1.0, 2.0]}))


def test_all_named_feature_sets_are_allowlisted():
    for name in list(FEATURE_SETS) + ["D_plus_equipment+history"]:
        spec = feature_spec(name)
        cols = spec["numeric"] + spec["categorical"]
        assert not set(cols) & FORBIDDEN
    assert "Federation" not in feature_spec("D_plus_equipment")["categorical"]


def test_preprocessing_fitted_on_train_only():
    train = pd.DataFrame({"Age": [20.0, 30.0, np.nan], "Sex": ["M", "F", "M"]})
    test = pd.DataFrame({"Age": [1000.0, np.nan], "Sex": ["Mx", None]})
    p = Preprocessor(["Age"], ["Sex"]).fit(train)
    assert p.medians["Age"] == 25.0
    assert p.means["Age"] == pytest.approx(25.0)
    p.dense(test)
    assert p.medians["Age"] == 25.0  # transform does not refit
    assert p.fitted_rows == 3
    assert (p.codes(test)[:, 0] == UNKNOWN).all()  # unseen and missing -> unknown
    X = p.dense(test)
    assert X.shape == (2, 1 + 1 + 3) and np.isfinite(X).all()


def test_min_count_maps_rare_categories_to_unknown():
    train = pd.DataFrame({"Federation": ["A"] * 5 + ["B"]})
    p = Preprocessor([], ["Federation"], min_count=2).fit(train)
    assert p.vocab["Federation"] == {"A": 1}
    assert list(p.codes(pd.DataFrame({"Federation": ["A", "B", "Z"]}))[:, 0]) == [1, 0, 0]
