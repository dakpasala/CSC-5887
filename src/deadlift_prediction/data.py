"""Snapshot download/metadata, raw reading, validation, and cleaning.

The raw zip is saved unchanged under data/raw/ with a `snapshot.json` sidecar
(source URL, retrieval time, sha256, schema, raw row count). Cleaning is a pure
function of the raw table so it can be unit tested on fixtures.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import io
import shutil
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.csv as pacsv

from .config import read_json, resolve, write_json

TARGET = "Best3DeadliftKg"
LIFTS = ["Best3SquatKg", "Best3BenchKg", "Best3DeadliftKg"]
VALID_SEX = {"M", "F", "Mx"}
VALID_EQUIPMENT = {"Raw", "Wraps", "Single-ply", "Multi-ply", "Unlimited", "Straps"}

# Columns carried into the cleaned table. Post-outcome fields (Place, TotalKg,
# Dots, Wilks, Glossbrenner, Goodlift, attempts) are deliberately dropped here so
# they cannot reach any downstream feature code.
# Expanded-input follow-up: squat/bench attempts (deadlift attempts are never
# kept), age classes, and home country. 4th attempts are excluded.
ATTEMPT_COLUMNS = ["Squat1Kg", "Squat2Kg", "Squat3Kg", "Bench1Kg", "Bench2Kg", "Bench3Kg"]
EXTRA_COLUMNS = [*ATTEMPT_COLUMNS, "AgeClass", "BirthYearClass", "Country"]

CLEAN_COLUMNS = [
    "row_id", "lifter_key", "meet_key", "Sex", "Equipment", "Age", "BodyweightKg",
    "Best3SquatKg", "Best3BenchKg", "Best3DeadliftKg", "Federation", "ParentFederation",
    "Tested", "MeetCountry", "Date", *EXTRA_COLUMNS,
]
AUX_COLUMNS = ["Name", "Event", "Equipment", "Date", "Best3DeadliftKg"]


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


def short_hash(text: str, n: int = 16) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:n]


# --------------------------------------------------------------------------- download

def snapshot_meta_path(cfg: dict) -> Path:
    return resolve(cfg, "data.raw_dir") / "snapshot.json"


def _csv_member(zf: zipfile.ZipFile) -> str:
    members = [m for m in zf.namelist() if m.endswith(".csv")]
    if len(members) != 1:
        raise ValueError(f"expected exactly one CSV in archive, found {members}")
    return members[0]


def download(cfg: dict, force: bool = False, existing: Path | None = None) -> dict:
    """Fetch the bulk zip once and record its metadata.

    If a snapshot is already registered, it is reused (the nightly file changes,
    so experiments must not re-download). `existing` registers an already
    downloaded zip instead of fetching.
    """
    raw_dir = resolve(cfg, "data.raw_dir")
    raw_dir.mkdir(parents=True, exist_ok=True)
    meta_path = snapshot_meta_path(cfg)
    if meta_path.exists() and not force:
        meta = read_json(meta_path)
        print(f"snapshot already registered: {meta['archive']} (sha256 {meta['sha256'][:12]}…); use --force to replace")
        return meta

    url = cfg["data"]["source_url"]
    tmp = raw_dir / "download.tmp"
    if existing is not None:
        existing = Path(existing)
        retrieved_at = dt.datetime.fromtimestamp(existing.stat().st_mtime, dt.timezone.utc)
        shutil.move(existing, tmp)
    else:
        print(f"downloading {url}")
        with urllib.request.urlopen(url) as resp, open(tmp, "wb") as out:
            shutil.copyfileobj(resp, out)
        retrieved_at = dt.datetime.now(dt.timezone.utc)

    with zipfile.ZipFile(tmp) as zf:
        member = _csv_member(zf)
        listing = [{"name": i.filename, "size": i.file_size} for i in zf.infolist()]
    archive = raw_dir / (Path(member).stem + ".zip")
    tmp.replace(archive)

    with zipfile.ZipFile(archive) as zf:
        with zf.open(member) as f:
            header = f.readline().decode("utf-8").strip().split(",")
    table = read_raw_table(archive, columns=["Event"])
    meta = {
        "source_url": url,
        "archive": archive.name,
        "csv_member": member,
        "retrieved_at": retrieved_at.isoformat(),
        "sha256": sha256_file(archive),
        "archive_bytes": archive.stat().st_size,
        "zip_listing": listing,
        "schema": header,
        "raw_rows": table.num_rows,
    }
    write_json(meta_path, meta)
    print(f"registered {archive.name}: {meta['raw_rows']:,} raw rows, sha256 {meta['sha256'][:12]}…")
    return meta


# --------------------------------------------------------------------------- reading

def read_raw_table(archive: Path, columns: list[str] | None = None) -> pa.Table:
    """Read the CSV inside the zip with every column as a string (explicit parsing later)."""
    with zipfile.ZipFile(archive) as zf:
        member = _csv_member(zf)
        with zf.open(member) as f:
            header = f.readline().decode("utf-8").strip().split(",")
        with zf.open(member) as f:
            buf = io.BytesIO(f.read())
    convert = pacsv.ConvertOptions(
        column_types={c: pa.string() for c in header},
        include_columns=columns,
        strings_can_be_null=True,
        null_values=[""],
    )
    return pacsv.read_csv(buf, convert_options=convert)


def load_raw_sbd(cfg: dict) -> tuple[pd.DataFrame, dict, pd.DataFrame]:
    """Return SBD rows (all columns as strings), snapshot metadata, and the raw
    deadlift rows of *every* event (for cross-event history)."""
    meta = read_json(snapshot_meta_path(cfg))
    archive = resolve(cfg, "data.raw_dir") / meta["archive"]
    table = read_raw_table(archive)
    if table.num_rows != meta["raw_rows"]:
        raise ValueError("raw row count does not match registered snapshot")
    event_counts = table.column("Event").value_counts().to_pylist()
    meta = dict(meta, event_counts={d["values"]: d["counts"] for d in event_counts})
    aux = table.select(AUX_COLUMNS).to_pandas()
    sbd = table.filter(pc.equal(table.column("Event"), "SBD"))
    del table
    return sbd.to_pandas(), meta, aux


# --------------------------------------------------------------------------- cleaning

def _to_float(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce").astype("float64")


def _hash_unique(values: pd.Series, prefix: str, n: int = 16) -> pd.Series:
    """sha256-based hash of each value, computed once per distinct value."""
    codes, uniques = pd.factorize(values.astype("string"))
    hashed = np.array([short_hash(prefix + str(u), n) for u in uniques], dtype=object)
    return pd.Series(hashed[codes], index=values.index)


def lifter_key(names: pd.Series) -> pd.Series:
    """Pseudonymous canonical identity: hash of the full OPL Name including any `#n` suffix."""
    return _hash_unique(names, "lifter|")


def hash_unit(keys: pd.Series, salt: str) -> np.ndarray:
    """Deterministic uniform [0,1) value per key (used for lifter sampling and group splits)."""
    codes, uniques = pd.factorize(pd.Series(keys).astype("string"))
    u = np.array([int(hashlib.sha256(f"{salt}|{k}".encode()).hexdigest()[:13], 16) / 16**13 for k in uniques])
    return u[codes]


def clean(raw: pd.DataFrame, cfg: dict) -> tuple[pd.DataFrame, list[dict], dict]:
    """Clean raw rows. Returns (clean_df, exclusion_log, audit_info).

    `raw` holds string columns straight from the CSV. Event filtering may already
    have happened; it is re-applied here so the function is safe on any input.
    """
    log: list[dict] = []
    audit: dict = {}

    def step(name: str, before: int, after: int, note: str = "") -> None:
        log.append({"step": name, "rows_before": before, "rows_removed": before - after, "rows_after": after, "note": note})

    df = raw.copy()
    raw_cols = list(raw.columns)
    for c in ["ParentFederation", "Tested", "MeetCountry", "MeetName", "Division", "Federation"]:
        if c not in df:
            df[c] = None
    n = len(df)
    df = df[df["Event"] == "SBD"]
    step("event_is_SBD", n, len(df))

    # One string per raw row (all raw columns), used for exact-duplicate detection
    # and stable row IDs. Unused raw columns are dropped right after to save memory.
    rowstr = df[raw_cols[0]].astype("string").fillna("")
    for c in raw_cols[1:]:
        rowstr = rowstr + "|" + df[c].astype("string").fillna("")
    for c in EXTRA_COLUMNS:
        if c not in df:
            df[c] = None
    keep_cols = ["Name", "Sex", "Equipment", "Age", "BodyweightKg", *LIFTS, "Federation", "ParentFederation", "Tested",
                 "MeetCountry", "MeetName", "Division", "Date", *EXTRA_COLUMNS]
    df = df[keep_cols].assign(_rowstr=rowstr.to_numpy())
    del rowstr

    for lift in LIFTS:
        df[lift] = _to_float(df[lift])
    for lift in LIFTS:
        n = len(df)
        ok = np.isfinite(df[lift]) & (df[lift] > 0)
        df = df[ok]
        step(f"{lift}_finite_positive", n, len(df), "missing, zero, or negative (failed) best lift")

    n = len(df)
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d", errors="coerce")
    df = df[df["Date"].notna()]
    step("valid_date", n, len(df))

    n = len(df)
    df = df[df["Name"].notna()]
    step("has_name", n, len(df))

    n = len(df)
    dup = df.duplicated(subset=["_rowstr"], keep="first")
    df = df[~dup]
    step("exact_duplicate_rows", n, len(df), "identical across every raw column")

    # Repeated listings: the same lifter (same canonical Name), same date and
    # equipment, identical three lifts. OPL lists lifters once per division they
    # entered, and cross-sanctioned meets can appear under several federations.
    # These are one performance; keep one deterministic representative.
    df["meet_key"] = _hash_unique(df["Federation"].fillna("") + "|" + df["Date"].dt.strftime("%Y-%m-%d") + "|"
                                  + df["MeetCountry"].fillna("") + "|" + df["MeetName"].fillna(""), "")
    df["_n_missing_demo"] = df[["Age", "BodyweightKg"]].isna().sum(axis=1)
    df = df.sort_values(["_n_missing_demo", "Federation", "MeetName", "Division"], na_position="last", kind="mergesort")
    listing_key = ["Name", "Date", "Equipment", *LIFTS]
    rep = df.duplicated(subset=listing_key, keep="first")
    dropped = df[rep]
    kept_meet = df[~rep].set_index(listing_key)["meet_key"]
    same_meet = dropped.set_index(listing_key)["meet_key"].eq(kept_meet.reindex(dropped.set_index(listing_key).index)).to_numpy()
    audit["repeated_listings"] = {
        "removed": int(rep.sum()),
        "same_meet_other_division": int(same_meet.sum()),
        "different_meet_key_same_day": int((~same_meet).sum()),
    }
    n = len(df)
    df = df[~rep]
    step("repeated_listing_same_lifter_date_equipment_lifts", n, len(df),
         "same Name+Date+Equipment+S/B/D (multi-division or cross-federation listing)")

    # Demographics: parse explicitly; implausible values become missing, rows kept.
    lo, hi = cfg["data"]["age_range"]
    df["Age"] = _to_float(df["Age"])
    bad_age = df["Age"].notna() & ~df["Age"].between(lo, hi)
    df.loc[bad_age, "Age"] = np.nan
    lo, hi = cfg["data"]["bodyweight_range"]
    df["BodyweightKg"] = _to_float(df["BodyweightKg"])
    bad_bw = df["BodyweightKg"].notna() & ~df["BodyweightKg"].between(lo, hi)
    df.loc[bad_bw, "BodyweightKg"] = np.nan
    bad_sex = ~df["Sex"].isin(VALID_SEX)
    df.loc[bad_sex, "Sex"] = np.nan
    bad_eq = ~df["Equipment"].isin(VALID_EQUIPMENT)
    df.loc[bad_eq, "Equipment"] = np.nan
    audit["set_to_missing"] = {
        "age_out_of_range": int(bad_age.sum()),
        "bodyweight_out_of_range": int(bad_bw.sum()),
        "invalid_sex": int(bad_sex.sum()),
        "invalid_equipment": int(bad_eq.sum()),
    }

    for c in ATTEMPT_COLUMNS:
        df[c] = _to_float(df[c])
    df["row_id"] = _hash_unique(df["_rowstr"], "")
    df = df.drop(columns="_rowstr")
    if df["row_id"].duplicated().any():
        raise ValueError("row_id collision; increase hash length")
    df["lifter_key"] = lifter_key(df["Name"])

    frac = cfg["data"].get("lifter_fraction", 1.0)
    if frac < 1.0:
        n = len(df)
        keep = hash_unit(df["lifter_key"], f"sample{cfg['seed']}") < frac
        df = df[keep]
        step("lifter_subsample", n, len(df), f"kept lifters with hash < {frac} (sampled by identity, not by row)")

    # Extreme but possibly real values are flagged, never removed.
    ratio = df["Best3DeadliftKg"] / df["Best3SquatKg"]
    audit["flags_kept"] = {
        "deadlift_over_400kg": int((df["Best3DeadliftKg"] > 400).sum()),
        "deadlift_to_squat_ratio_over_3": int((ratio > 3).sum()),
        "deadlift_to_squat_ratio_under_0.4": int((ratio < 0.4).sum()),
    }

    identity_frame = df[["lifter_key", "Name", "Sex", "Date", "Age", "meet_key"]].copy()
    df = df.sort_values(["Date", "row_id"]).reset_index(drop=True)
    return df[CLEAN_COLUMNS].copy(), log, {**audit, "_identity_frame": identity_frame}


def clean_aux(aux: pd.DataFrame, cfg: dict) -> tuple[pd.DataFrame, dict]:
    """Successful deadlifts from any event (SBD, D, BD, SD, including SBD entries
    that failed squat or bench), used only as strictly-earlier history context.

    Same identity key and lifter sampling as the main table. One row per
    lifter, date, equipment, and deadlift value (removes multi-division
    listings). Deadlift-only exhibition entries are kept, as in the source.
    """
    a = aux.copy()
    n0 = len(a)
    a["Best3DeadliftKg"] = _to_float(a["Best3DeadliftKg"])
    a["Date"] = pd.to_datetime(a["Date"], format="%Y-%m-%d", errors="coerce")
    a = a[np.isfinite(a["Best3DeadliftKg"]) & (a["Best3DeadliftKg"] > 0) & a["Date"].notna() & a["Name"].notna()]
    n1 = len(a)
    a = a.drop_duplicates(["Name", "Date", "Equipment", "Best3DeadliftKg"])
    a["lifter_key"] = lifter_key(a["Name"])
    frac = cfg["data"].get("lifter_fraction", 1.0)
    if frac < 1.0:
        a = a[hash_unit(a["lifter_key"], f"sample{cfg['seed']}") < frac]
    info = {"raw_rows": int(n0), "valid_deadlift_rows": int(n1), "after_dedup_and_sampling": int(len(a)),
            "by_event": {str(k): int(v) for k, v in a["Event"].value_counts().items()}}
    return a[["lifter_key", "Event", "Equipment", "Date", "Best3DeadliftKg"]].reset_index(drop=True), info
