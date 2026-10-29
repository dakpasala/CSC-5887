import subprocess
import sys

import numpy as np
import pandas as pd
import pytest

from deadlift_prediction.models import BaseModel, build_model


def _data(n=600, seed=0):
    rng = np.random.default_rng(seed)
    sex = rng.choice(["M", "F"], n)
    squat = rng.uniform(80, 300, n)
    df = pd.DataFrame({"Best3SquatKg": squat, "Best3BenchKg": squat * 0.65, "BodyweightKg": rng.uniform(50, 130, n),
                       "Age": np.where(rng.random(n) < 0.3, np.nan, rng.uniform(16, 70, n)), "Sex": sex,
                       "Equipment": rng.choice(["Raw", "Wraps"], n), "Federation": rng.choice(["F1", "F2"], n)})
    y = squat * np.where(sex == "M", 1.2, 1.1) + rng.normal(0, 5, n)
    return df, y


def test_ratio_least_squares_through_origin_by_sex(cfg):
    df = pd.DataFrame({"Best3SquatKg": [100.0, 200.0, 100.0], "Sex": ["M", "M", "F"]})
    y = np.array([120.0, 250.0, 90.0])
    m = build_model("ratio", "A_squat", cfg, 42).fit(df, y, df, y)
    assert m.by_sex["M"] == pytest.approx((100 * 120 + 200 * 250) / (100**2 + 200**2))
    assert m.by_sex["F"] == pytest.approx(0.9)
    assert m.pooled == pytest.approx((12000 + 50000 + 9000) / 60000)
    unseen = pd.DataFrame({"Best3SquatKg": [100.0, 100.0], "Sex": ["Mx", None]})
    assert np.allclose(m.predict(unseen), 100 * m.pooled)


@pytest.mark.parametrize("kind", ["linear", "lightgbm"])
def test_roundtrip_and_unseen_categories(kind, cfg, tmp_path):
    df, y = _data()
    m = build_model(kind, "E_plus_federation", cfg, 42).fit(df[:400], y[:400], df[400:500], y[400:500])
    unseen = df[500:].copy()
    unseen.loc[unseen.index[:20], "Equipment"] = "Multi-ply"
    unseen.loc[unseen.index[20:40], "Federation"] = "NEWFED"
    unseen.loc[unseen.index[40:50], "Sex"] = None
    p1 = m.predict(unseen)
    assert np.isfinite(p1).all()
    m.save(tmp_path / "m.pkl")
    p2 = BaseModel.load(tmp_path / "m.pkl").predict(unseen)
    np.testing.assert_allclose(p1, p2)
    assert m.prep.fitted_rows == 400


MLP_CHECK = r"""
import numpy as np, sys, tempfile, pathlib
sys.path.insert(0, sys.argv[1])
from test_models import _data
from deadlift_prediction.config import load_config, PROJECT_ROOT
from deadlift_prediction.models import build_model, BaseModel
cfg = load_config(PROJECT_ROOT / "configs" / "smoke.yaml")
df, y = _data()
m = build_model("mlp", "D_plus_equipment", cfg, 42).fit(df[:400], y[:400], df[400:500], y[400:500])
t = df[500:].copy(); t.loc[t.index[:10], "Equipment"] = "Multi-ply"
p1 = m.predict(t)
path = pathlib.Path(tempfile.mkdtemp()) / "m.pkl"; m.save(path)
p2 = BaseModel.load(path).predict(t)
assert np.isfinite(p1).all() and np.allclose(p1, p2), "mlp roundtrip mismatch"
assert abs(np.mean(p1) - np.mean(y)) < 200  # predictions are back in kg
print("MLP_OK")
"""


def test_mlp_roundtrip_in_isolated_process():
    # PyTorch and LightGBM bundle conflicting OpenMP runtimes on macOS, so the MLP
    # check runs in its own interpreter (mirroring how training isolates them).
    import pathlib
    here = str(pathlib.Path(__file__).parent)
    r = subprocess.run([sys.executable, "-c", MLP_CHECK, here], capture_output=True, text=True, timeout=300)
    assert "MLP_OK" in r.stdout, r.stderr[-2000:]
