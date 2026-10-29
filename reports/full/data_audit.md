# Data audit — full
- Source: https://openpowerlifting.gitlab.io/opl-csv/files/openpowerlifting-latest.zip
- Archive: `openpowerlifting-2026-10-24-0fc10dd9.zip` (sha256 `26be6b73f4b16ba5f4f8fb568f258d2c5ab165f379aed21e2489af9d0022afe7`)
- Retrieved: 2026-10-29T16:48:02.360389+00:00
- Raw rows in snapshot: 4,054,260
- Cleaned rows: 2,594,760; estimated unique lifters: 788,075
- Date coverage: 1964-09-05 to 2026-10-18
- Split ID: `9eacfcc77688`

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

Repeated listings removed: 107,885 (107,440 same meet in another division; 445 under a different meet key on the same day, e.g. cross-federation listings).

Values set to missing (rows kept): age_out_of_range = 3, bodyweight_out_of_range = 23, invalid_sex = 0, invalid_equipment = 0.

Extreme values flagged but kept: deadlift_over_400kg = 238, deadlift_to_squat_ratio_over_3 = 1,597, deadlift_to_squat_ratio_under_0.4 = 1,523.

## Missingness (cleaned rows)

| column | share_missing |
|---|---|
| Age | 0.4259 |
| BodyweightKg | 0.0051 |
| Sex | 0.0000 |
| Equipment | 0.0000 |
| Federation | 0.0000 |

## Distributions

**Sex**

| Sex | rows |
|---|---|
| M | 1788839 |
| F | 805762 |
| Mx | 159 |

**Equipment**

| Equipment | rows |
|---|---|
| Raw | 1075662 |
| Single-ply | 988837 |
| Unlimited | 270556 |
| Wraps | 210883 |
| Multi-ply | 48821 |
| Straps | 1 |

**Federation** (top 20 of 440)

| Federation | rows |
|---|---|
| THSPA | 461726 |
| USAPL | 289194 |
| THSWPA | 283473 |
| USPA | 147206 |
| FPR | 117102 |
| USPF | 106554 |
| CPU | 60064 |
| APF | 37495 |
| IPF | 35985 |
| NSF | 35916 |
| EPA | 35842 |
| RPS | 34023 |
| FFForce | 30195 |
| BVDK | 28705 |
| EPF | 26920 |
| WRPF | 24876 |
| UkrainePF | 24449 |
| SVNL | 23820 |
| CSST | 20928 |
| WPC | 20682 |

Target Best3DeadliftKg: mean 185.4, sd 61.1, min 1.0, median 183.7, max 492.5.

## History eligibility

Rows with a strictly earlier eligible meet for the same lifter: 1,804,454 (69.5%); lifters with at least one such row: 430,939.

## Lifter identity

- canonical_identity: OPL Name including '#n' disambiguation suffix; hashed to lifter_key
- unique_lifters: 788075
- lifters_with_hash_suffix: 31260
- base_names_disambiguated_by_suffix: 9362
- base_names_with_both_suffixed_and_unsuffixed_entries: 0
- lifters_with_multiple_sex_values: 1312
- lifters_with_2plus_aged_records: 261886
- lifters_with_implied_birth_year_spread_over_2y: 16094
- lifter_days_with_multiple_meet_keys: 3129
- rows per lifter: mean 3.29, median 2, p99 21, max 175, share_of_rows_from_lifters_with_10plus 0.315

Limitations:
- Names without a suffix are assumed to be one person; OPL may not yet have split some same-name athletes.
- Inconsistent implied birth years or multiple Sex values can indicate merged identities (or data-entry errors); they are reported, not corrected.
- One person entered under two spellings is treated as two lifters, which can place the same athlete in both train and test.

## Splits

Protocol A (unseen lifters): hashed-identity group split {'train': 0.7, 'val': 0.15, 'test': 0.15}, seed 42.

| partition | rows | lifters | share_female | share_raw | mean_squat | mean_bench | mean_deadlift | mean_bodyweight | age_missing | bodyweight_missing | has_history | date_min | date_max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| test | 386613 | 118000 | 0.31 | 0.41 | 171.27 | 107.56 | 185.44 | 82.63 | 0.43 | 0.01 | 0.69 | 1964-09-05 | 2026-10-18 |
| train | 1817276 | 551698 | 0.31 | 0.41 | 171.16 | 107.37 | 185.36 | 82.46 | 0.42 | 0.01 | 0.70 | 1964-09-05 | 2026-10-18 |
| val | 390871 | 118377 | 0.31 | 0.41 | 171.19 | 107.49 | 185.48 | 82.48 | 0.43 | 0.01 | 0.70 | 1964-09-05 | 2026-10-18 |

Protocol B (future meets): train: Date < val_start; val: val_start <= Date < test_start; test: Date >= test_start; boundaries {'val_start': '2023-01-01', 'test_start': '2024-11-01'}. Lifters recur across periods.

| partition | rows | lifters | share_female | share_raw | mean_squat | mean_bench | mean_deadlift | mean_bodyweight | age_missing | bodyweight_missing | has_history | date_min | date_max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| test | 402128 | 183630 | 0.38 | 0.62 | 165.46 | 102.43 | 180.79 | 82.27 | 0.39 | 0.00 | 0.75 | 2024-11-01 | 2026-10-18 |
| train | 1800694 | 575145 | 0.28 | 0.33 | 173.88 | 109.95 | 187.54 | 82.65 | 0.44 | 0.01 | 0.68 | 1964-09-05 | 2022-12-27 |
| val | 391938 | 181332 | 0.38 | 0.57 | 164.68 | 100.91 | 180.24 | 82.00 | 0.38 | 0.00 | 0.71 | 2023-01-01 | 2024-10-31 |

Protocol C transfer groups (chosen by row counts only): Equipment=Single-ply (988,837 rows); Equipment=Unlimited (270,556 rows); Equipment=Wraps (210,883 rows); Equipment=Multi-ply (48,821 rows); Federation=THSPA (461,726 rows); Federation=USAPL (289,194 rows); Federation=THSWPA (283,473 rows)
