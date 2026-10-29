# Data audit — subset10
- Source: https://openpowerlifting.gitlab.io/opl-csv/files/openpowerlifting-latest.zip
- Archive: `openpowerlifting-2026-10-24-0fc10dd9.zip` (sha256 `26be6b73f4b16ba5f4f8fb568f258d2c5ab165f379aed21e2489af9d0022afe7`)
- Retrieved: 2026-10-29T16:48:02.360389+00:00
- Raw rows in snapshot: 4,054,260
- Cleaned rows: 260,829; estimated unique lifters: 79,087
- Date coverage: 1964-09-05 to 2026-10-18
- Split ID: `4a6bc1eefdce`

## Exclusions by step

| step | rows_before | rows_removed | rows_after | note |
|---|---|---|---|---|
| raw_snapshot | 4054260 | 0 | 4054260 | event counts: {'B': 803516, 'S': 19962, 'D': 220108, 'BD': 76125, 'SBD': 2927873, 'SD': 2490, 'SB': 4186} |
| event_is_SBD | 2927873 | 0 | 2927873 |  |
| Best3SquatKg_finite_positive | 2927873 | 131602 | 2796271 | missing, zero, or negative (failed) best lift |
| Best3BenchKg_finite_positive | 2796271 | 61403 | 2734868 | missing, zero, or negative (failed) best lift |
| Best3DeadliftKg_finite_positive | 2734868 | 30514 | 2704354 | missing, zero, or negative (failed) best lift |
| valid_date | 2704354 | 0 | 2704354 |  |
| has_name | 2704354 | 0 | 2704354 |  |
| exact_duplicate_rows | 2704354 | 1709 | 2702645 | identical across every raw column |
| repeated_listing_same_lifter_date_equipment_lifts | 2702645 | 107885 | 2594760 | same Name+Date+Equipment+S/B/D (multi-division or cross-federation listing) |
| lifter_subsample | 2594760 | 2333931 | 260829 | kept lifters with hash < 0.1 (sampled by identity, not by row) |

Repeated listings removed: 107,885 (107,440 same meet in another division; 445 under a different meet key on the same day, e.g. cross-federation listings).

Values set to missing (rows kept): age_out_of_range = 3, bodyweight_out_of_range = 23, invalid_sex = 0, invalid_equipment = 0.

Extreme values flagged but kept: deadlift_over_400kg = 35, deadlift_to_squat_ratio_over_3 = 153, deadlift_to_squat_ratio_under_0.4 = 161.

## Missingness (cleaned rows)

| column | share_missing |
|---|---|
| Age | 0.4252 |
| BodyweightKg | 0.0050 |
| Sex | 0.0000 |
| Equipment | 0.0000 |
| Federation | 0.0000 |

## Distributions

**Sex**

| Sex | rows |
|---|---|
| M | 179888 |
| F | 80927 |
| Mx | 14 |

**Equipment**

| Equipment | rows |
|---|---|
| Raw | 108689 |
| Single-ply | 98599 |
| Unlimited | 27442 |
| Wraps | 21232 |
| Multi-ply | 4867 |

**Federation** (top 20 of 428)

| Federation | rows |
|---|---|
| THSPA | 46073 |
| USAPL | 29162 |
| THSWPA | 28710 |
| USPA | 14987 |
| FPR | 11326 |
| USPF | 10379 |
| CPU | 6515 |
| APF | 3777 |
| NSF | 3724 |
| EPA | 3609 |
| IPF | 3592 |
| RPS | 3512 |
| FFForce | 3056 |
| BVDK | 2695 |
| EPF | 2636 |
| SVNL | 2621 |
| WRPF | 2527 |
| UkrainePF | 2386 |
| CSST | 2174 |
| WPC | 2054 |

Target Best3DeadliftKg: mean 185.5, sd 61.3, min 10.0, median 183.7, max 487.5.

## History eligibility

Rows with a strictly earlier eligible meet for the same lifter: 181,527 (69.6%); lifters with at least one such row: 43,218.

## Lifter identity

- canonical_identity: OPL Name including '#n' disambiguation suffix; hashed to lifter_key
- unique_lifters: 79087
- lifters_with_hash_suffix: 3100
- base_names_disambiguated_by_suffix: 2459
- base_names_with_both_suffixed_and_unsuffixed_entries: 0
- lifters_with_multiple_sex_values: 121
- lifters_with_2plus_aged_records: 26273
- lifters_with_implied_birth_year_spread_over_2y: 1582
- lifter_days_with_multiple_meet_keys: 279
- rows per lifter: mean 3.3, median 2, p99 20, max 102, share_of_rows_from_lifters_with_10plus 0.313

Limitations:
- Names without a suffix are assumed to be one person; OPL may not yet have split some same-name athletes.
- Inconsistent implied birth years or multiple Sex values can indicate merged identities (or data-entry errors); they are reported, not corrected.
- One person entered under two spellings is treated as two lifters, which can place the same athlete in both train and test.

## Splits

Protocol A (unseen lifters): hashed-identity group split {'train': 0.7, 'val': 0.15, 'test': 0.15}, seed 42.

| partition | rows | lifters | share_female | share_raw | mean_squat | mean_bench | mean_deadlift | mean_bodyweight | age_missing | bodyweight_missing | has_history | date_min | date_max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| test | 39285 | 11781 | 0.30 | 0.41 | 171.85 | 108.10 | 186.24 | 82.45 | 0.43 | 0.00 | 0.70 | 1965-09-04 | 2026-10-18 |
| train | 182158 | 55295 | 0.31 | 0.42 | 171.12 | 107.13 | 185.34 | 82.52 | 0.42 | 0.00 | 0.70 | 1964-09-05 | 2026-10-18 |
| val | 39386 | 12011 | 0.31 | 0.42 | 170.90 | 107.43 | 185.73 | 82.11 | 0.43 | 0.01 | 0.69 | 1965-09-04 | 2026-10-18 |

Protocol B (future meets): train: Date < val_start; val: val_start <= Date < test_start; test: Date >= test_start; boundaries {'val_start': '2023-01-01', 'test_start': '2024-11-01'}. Lifters recur across periods.

| partition | rows | lifters | share_female | share_raw | mean_squat | mean_bench | mean_deadlift | mean_bodyweight | age_missing | bodyweight_missing | has_history | date_min | date_max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| test | 40199 | 18266 | 0.38 | 0.62 | 165.46 | 102.39 | 180.65 | 82.22 | 0.40 | 0.00 | 0.75 | 2024-11-01 | 2026-10-18 |
| train | 181042 | 57692 | 0.28 | 0.34 | 173.81 | 109.75 | 187.71 | 82.60 | 0.44 | 0.01 | 0.68 | 1964-09-05 | 2022-12-27 |
| val | 39588 | 18296 | 0.38 | 0.57 | 165.08 | 101.23 | 180.52 | 82.00 | 0.39 | 0.00 | 0.71 | 2023-01-01 | 2024-10-31 |

Protocol C transfer groups (chosen by row counts only): Equipment=Single-ply (98,599 rows); Equipment=Unlimited (27,442 rows); Equipment=Wraps (21,232 rows); Federation=THSPA (46,073 rows); Federation=USAPL (29,162 rows); Federation=THSWPA (28,710 rows)
