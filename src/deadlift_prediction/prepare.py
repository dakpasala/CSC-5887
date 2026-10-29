"""`prepare` stage: clean, audit identities, compute past-only history, freeze splits."""

from __future__ import annotations

import time

import pandas as pd

from . import synthetic
from .config import config_hash, processed_dir, reports_dir, write_json
from .data import clean, load_raw_sbd
from .features import add_history
from .identity import identity_audit
from .splits import (assert_disjoint, balance_table, chrono_boundaries, chrono_split, group_split,
                     manifest_id, select_transfer_groups)


def _dist(s: pd.Series, top: int | None = None) -> dict:
    vc = s.fillna("<missing>").value_counts()
    if top:
        vc = vc.head(top)
    return {str(k): int(v) for k, v in vc.items()}


def prepare(cfg: dict) -> dict:
    t0 = time.time()
    out_dir = processed_dir(cfg)
    out_dir.mkdir(parents=True, exist_ok=True)

    if cfg.get("synthetic"):
        raw = synthetic.make_raw(seed=cfg["seed"])
        meta = {"source_url": "SYNTHETIC FIXTURE (not OpenPowerlifting)", "sha256": "synthetic", "raw_rows": len(raw),
                "event_counts": raw["Event"].value_counts().to_dict(), "archive": None}
    else:
        raw, meta = load_raw_sbd(cfg)
    print(f"loaded {len(raw):,} SBD rows (raw snapshot rows: {meta['raw_rows']:,})")

    df, log, audit = clean(raw, cfg)
    del raw
    log.insert(0, {"step": "raw_snapshot", "rows_before": meta["raw_rows"], "rows_removed": 0, "rows_after": meta["raw_rows"],
                   "note": f"event counts: {meta.get('event_counts')}"})
    ident = identity_audit(audit.pop("_identity_frame"))
    print(f"cleaned: {len(df):,} rows, {df['lifter_key'].nunique():,} lifters")

    df = add_history(df)

    df["split_A"] = group_split(df, cfg["splits"]["group"], cfg["seed"]).to_numpy()
    assert_disjoint(df, df["split_A"], by_lifter=True)
    bounds = chrono_boundaries(df["Date"], cfg["splits"]["chrono_quantiles"])
    df["split_B"] = chrono_split(df, bounds).to_numpy()
    assert_disjoint(df, df["split_B"], by_lifter=False)
    groups = select_transfer_groups(df, cfg["transfer"])

    manifest = df[["row_id", "lifter_key", "split_A", "split_B"]]
    split_id = manifest_id(manifest)
    df.to_parquet(out_dir / "clean.parquet", index=False)
    manifest.to_parquet(out_dir / "manifest.parquet", index=False)

    splits_info = {
        "split_id": split_id, "seed": cfg["seed"], "group_fractions": cfg["splits"]["group"],
        "chrono_boundaries": {k: v.strftime("%Y-%m-%d") for k, v in bounds.items()},
        "chrono_rule": "train: Date < val_start; val: val_start <= Date < test_start; test: Date >= test_start",
        "transfer_groups": groups, "transfer_rules": cfg["transfer"],
    }
    write_json(out_dir / "splits.json", splits_info)

    bal_a = balance_table(df, df["split_A"])
    bal_b = balance_table(df, df["split_B"])
    rd = reports_dir(cfg)
    rd.mkdir(parents=True, exist_ok=True)
    bal_a.to_csv(rd / "balance_protocol_A.csv", index=False)
    bal_b.to_csv(rd / "balance_protocol_B.csv", index=False)

    hist = df[df["has_history"]]
    summary = {
        "config": cfg["name"], "config_hash": config_hash(cfg), "synthetic": bool(cfg.get("synthetic")),
        "snapshot": {k: meta.get(k) for k in ["source_url", "archive", "retrieved_at", "sha256", "raw_rows"]},
        "exclusions": log, "audit": audit, "identity": ident,
        "clean_rows": len(df), "clean_lifters": int(df["lifter_key"].nunique()),
        "date_min": df["Date"].min().strftime("%Y-%m-%d"), "date_max": df["Date"].max().strftime("%Y-%m-%d"),
        "rows_by_year": {str(k): int(v) for k, v in df["Date"].dt.year.value_counts().sort_index().items()},
        "missingness": {c: float(df[c].isna().mean()) for c in ["Age", "BodyweightKg", "Sex", "Equipment", "Federation"]},
        "sex": _dist(df["Sex"]), "equipment": _dist(df["Equipment"]), "federation_top20": _dist(df["Federation"], 20),
        "n_federations": int(df["Federation"].nunique()),
        "history_eligible_rows": int(len(hist)), "history_eligible_lifters": int(hist["lifter_key"].nunique()),
        "target_kg": {k: float(v) for k, v in df["Best3DeadliftKg"].describe().items()},
        "split_id": split_id, "splits": splits_info,
        "partition_sizes": {
            "A": df.groupby("split_A").agg(rows=("row_id", "size"), lifters=("lifter_key", "nunique")).to_dict("index"),
            "B": df.groupby("split_B").agg(rows=("row_id", "size"), lifters=("lifter_key", "nunique")).to_dict("index"),
        },
        "seconds": time.time() - t0,
    }
    write_json(out_dir / "data_summary.json", summary)
    from .reporting import write_data_audit

    write_data_audit(summary, bal_a, bal_b, rd / "data_audit.md")
    print(f"prepared {cfg['name']}: split_id {split_id}; wrote {out_dir}")
    return summary


def load_prepared(cfg: dict) -> tuple[pd.DataFrame, dict]:
    from .config import read_json

    d = processed_dir(cfg)
    return pd.read_parquet(d / "clean.parquet"), read_json(d / "splits.json")
