"""Lifter identity: canonical key definition and identity-quality audit.

OpenPowerlifting's documented disambiguation is the `Name` field itself: lifters
sharing a name are distinguished by a `#n` suffix (e.g. `John Doe #1`). We use
the full Name string (suffix included) as the canonical identity and never merge
or split identities automatically. The audit only *reports* signals of possible
identity errors; it changes nothing.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

SUFFIX_RE = r"\s#\d+$"


def identity_audit(frame: pd.DataFrame) -> dict:
    """`frame` has columns lifter_key, Name, Sex, Date, Age, meet_key (one row per cleaned record)."""
    names = frame.drop_duplicates("lifter_key")[["lifter_key", "Name"]]
    has_suffix = names["Name"].str.contains(SUFFIX_RE, regex=True)
    base = names["Name"].str.replace(SUFFIX_RE, "", regex=True)
    suffixed_bases = set(base[has_suffix])
    unsuffixed_bases = set(base[~has_suffix])

    sex_per = frame.dropna(subset=["Sex"]).groupby("lifter_key")["Sex"].nunique()

    # Age consistency: Age - (years elapsed) should be roughly constant per lifter.
    aged = frame.dropna(subset=["Age"])
    years = (aged["Date"] - pd.Timestamp("1900-01-01")).dt.days / 365.25
    implied_birth = years - aged["Age"]
    spread = implied_birth.groupby(aged["lifter_key"]).agg(lambda s: s.max() - s.min())
    multi_aged = aged.groupby("lifter_key").size()
    spread = spread[multi_aged[multi_aged >= 2].index]

    same_day = frame.groupby(["lifter_key", "Date"])["meet_key"].nunique()
    rows_per = frame.groupby("lifter_key").size()

    return {
        "canonical_identity": "OPL Name including '#n' disambiguation suffix; hashed to lifter_key",
        "unique_lifters": int(len(names)),
        "lifters_with_hash_suffix": int(has_suffix.sum()),
        "base_names_disambiguated_by_suffix": int(len(suffixed_bases)),
        "base_names_with_both_suffixed_and_unsuffixed_entries": int(len(suffixed_bases & unsuffixed_bases)),
        "lifters_with_multiple_sex_values": int((sex_per > 1).sum()),
        "lifters_with_2plus_aged_records": int(len(spread)),
        "lifters_with_implied_birth_year_spread_over_2y": int((spread > 2.0).sum()),
        "lifter_days_with_multiple_meet_keys": int((same_day > 1).sum()),
        "rows_per_lifter": {
            "mean": float(rows_per.mean()),
            "median": float(rows_per.median()),
            "p99": float(np.percentile(rows_per, 99)),
            "max": int(rows_per.max()),
            "share_of_rows_from_lifters_with_10plus": float(rows_per[rows_per >= 10].sum() / rows_per.sum()),
        },
        "limitations": [
            "Names without a suffix are assumed to be one person; OPL may not yet have split some same-name athletes.",
            "Inconsistent implied birth years or multiple Sex values can indicate merged identities (or data-entry errors); they are reported, not corrected.",
            "One person entered under two spellings is treated as two lifters, which can place the same athlete in both train and test.",
        ],
    }
