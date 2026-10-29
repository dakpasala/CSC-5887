import pandas as pd
import pytest

from deadlift_prediction.config import PROJECT_ROOT, load_config


@pytest.fixture
def cfg():
    return load_config(PROJECT_ROOT / "configs" / "smoke.yaml")


def raw_rows(rows):
    """Build a raw-like string frame from partial dicts."""
    base = {"Name": "A", "Sex": "M", "Event": "SBD", "Equipment": "Raw", "Age": "30", "Division": "Open",
            "BodyweightKg": "90", "Best3SquatKg": "200", "Best3BenchKg": "130", "Best3DeadliftKg": "250",
            "Federation": "F1", "Date": "2020-01-01", "MeetCountry": "USA", "MeetName": "M1", "Place": "1", "TotalKg": "580"}
    return pd.DataFrame([{**base, **r} for r in rows]).astype(object)


def lifter_frame(rows):
    """Clean-shaped frame for history/split tests."""
    df = pd.DataFrame(rows)
    df["Date"] = pd.to_datetime(df["Date"])
    for c, v in {"Best3SquatKg": 200.0, "Best3BenchKg": 130.0, "Best3DeadliftKg": 250.0}.items():
        if c not in df:
            df[c] = v
    if "row_id" not in df:
        df["row_id"] = [f"r{i}" for i in range(len(df))]
    return df
