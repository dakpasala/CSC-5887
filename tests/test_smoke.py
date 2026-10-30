import pandas as pd

from deadlift_prediction.cli import smoke
from deadlift_prediction.config import artifacts_dir, reports_dir


def test_synthetic_pipeline_end_to_end():
    out = smoke()
    cfg = out["cfg"]
    assert out["summary"]["synthetic"] is True
    root = artifacts_dir(cfg)
    m = pd.read_csv(root / "tables_final" / "metrics.csv")
    assert {"ablation_core", "history_eligible", "chrono_all", "models_D"} <= set(m["comparison"])
    assert m["mae"].notna().all()
    # every comparison scores identical rows across its runs
    for (comp, part), g in m.groupby(["comparison", "partition"]):
        assert g["rows"].nunique() == 1, comp
    runs = list((root / "runs").glob("*/predictions.parquet"))
    assert len(runs) == len(out["runs"]) + len(out["ensembles"])
    assert len(out["ensembles"]) == 3
    assert any(c.startswith("ensemble|") for c in m["comparison"])
    iv = pd.read_csv(root / "tables_final" / "intervals.csv")
    assert {"raw", "conformal"} <= set(iv["interval"]) and {"val", "test"} <= set(iv["partition"])
    assert iv["coverage"].between(0, 1).all()
    p = pd.read_parquet(runs[0])
    assert {"row_id", "lifter_key", "partition", "y", "yhat"} <= set(p.columns)
    assert "SYNTHETIC" in (reports_dir(cfg) / "results_test.md").read_text()
