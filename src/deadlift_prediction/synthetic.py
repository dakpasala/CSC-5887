"""Deterministic synthetic fixture shaped like the OpenPowerlifting CSV.

Used only by the smoke pipeline and tests. Scores computed on it are NOT
research findings.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

RAW_COLUMNS = [
    "Name", "Sex", "Event", "Equipment", "Age", "AgeClass", "BirthYearClass", "Division", "BodyweightKg",
    "WeightClassKg", "Squat1Kg", "Squat2Kg", "Squat3Kg", "Squat4Kg", "Best3SquatKg", "Bench1Kg", "Bench2Kg",
    "Bench3Kg", "Bench4Kg", "Best3BenchKg", "Deadlift1Kg", "Deadlift2Kg", "Deadlift3Kg", "Deadlift4Kg",
    "Best3DeadliftKg", "TotalKg", "Place", "Dots", "Wilks", "Glossbrenner", "Goodlift", "Tested", "Country",
    "State", "Federation", "ParentFederation", "Date", "MeetCountry", "MeetState", "MeetTown", "MeetName", "Sanctioned",
]


def dead_base(bw: float, strength: float, sex: str) -> float:
    return (1.6 if sex == "M" else 1.1) * bw * strength * 1.15


def make_raw(n_lifters: int = 600, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    feds = ["FEDA", "FEDB", "FEDC", "FEDD"]
    equips = ["Raw", "Raw", "Raw", "Wraps", "Single-ply"]
    rows = []
    for i in range(n_lifters):
        sex = "F" if rng.random() < 0.35 else "M"
        name = f"Synthetic Lifter {i}" + (" #2" if i % 50 == 0 else "")
        bw = rng.normal(70 if sex == "F" else 90, 12)
        strength = rng.normal(1.0, 0.15)
        birth = 1960 + rng.integers(0, 45)
        n_meets = int(rng.integers(1, 6))
        start = pd.Timestamp("2012-01-01") + pd.Timedelta(days=int(rng.integers(0, 3000)))
        eq = equips[rng.integers(0, len(equips))]
        fed = feds[rng.integers(0, len(feds))]
        for m in range(n_meets):
            date = start + pd.Timedelta(days=int(120 * m + rng.integers(0, 60)))
            gain = 1 + 0.03 * m
            base = (1.6 if sex == "M" else 1.1) * bw * strength * gain
            squat = round(base * rng.normal(1.0, 0.05) * (1.1 if eq == "Single-ply" else 1.0), 1)
            bench = round(base * 0.65 * rng.normal(1.0, 0.05), 1)
            dead = round(base * 1.15 * rng.normal(1.0, 0.05), 1)
            age = date.year - birth
            if m == 0 and i % 4 == 0:  # an earlier deadlift-only meet for some lifters
                rows.append({"Name": name, "Sex": sex, "Event": "D", "Equipment": eq, "Division": "Open",
                             "Best3DeadliftKg": str(round(dead_base(bw, strength, sex) * 0.97, 1)), "Place": "1",
                             "Federation": fed, "Date": (date - pd.Timedelta(days=90)).strftime("%Y-%m-%d"),
                             "MeetCountry": "USA", "MeetName": f"DL {fed} {date:%Y%m}"})
            rows.append({
                "Name": name, "Sex": sex, "Event": "SBD", "Equipment": eq,
                "Age": "" if rng.random() < 0.3 else str(age), "Division": "Open",
                "AgeClass": f"{(age // 5) * 5}-{(age // 5) * 5 + 4}",
                "Squat1Kg": str(round(squat * 0.9, 1)), "Squat2Kg": str(round(squat, 1)),
                "Squat3Kg": str(-round(squat * 1.04, 1)) if rng.random() < 0.4 else None,
                "Bench1Kg": str(round(bench * 0.92, 1)), "Bench2Kg": str(round(bench, 1)), "Bench3Kg": None,
                "BodyweightKg": "" if rng.random() < 0.05 else f"{bw:.1f}",
                "Best3SquatKg": str(squat), "Best3BenchKg": str(bench), "Best3DeadliftKg": str(dead),
                "TotalKg": f"{squat + bench + dead:.1f}", "Place": "1", "Federation": fed,
                "Date": date.strftime("%Y-%m-%d"), "MeetCountry": "USA", "MeetName": f"Meet {fed} {date:%Y%m}",
            })
    df = pd.DataFrame(rows)
    # Edge cases the cleaner must handle.
    extra = df.iloc[:5].copy()
    extra.loc[:, "Best3DeadliftKg"] = ["-200", "0", "", "abc", "180"]  # failed/zero/missing/invalid/valid
    extra.loc[extra.index[4], "Name"] = "Edge Valid"
    bench_only = df.iloc[5:8].copy()
    bench_only["Event"] = "B"
    dup_exact = df.iloc[10:13].copy()
    dup_division = df.iloc[20:23].copy()
    dup_division["Division"] = "Juniors"
    df = pd.concat([df, extra, bench_only, dup_exact, dup_division], ignore_index=True)
    for c in RAW_COLUMNS:
        if c not in df:
            df[c] = None
    df = df[RAW_COLUMNS].replace({"": None})
    return df.astype("object")
