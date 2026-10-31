# Results — full (TEST, final)

MAE in kg with 95% lifter-bootstrap CI. All rows within a comparison are identical across models.

## ablation_core — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| ablation · A · A_squat · ratio | ratio | A_squat | 386613 | 118000 | 21.91 | 21.76 | 22.09 | 21.62 | 12.34 | 0.77 |
| ablation · A · A_squat · linear | linear | A_squat | 386613 | 118000 | 19.48 | 19.36 | 19.61 | 18.54 | 11.52 | 0.83 |
| ablation · A · B_squat_bench · linear | linear | B_squat_bench | 386613 | 118000 | 18.19 | 18.06 | 18.32 | 17.21 | 10.73 | 0.84 |
| ablation · A · C_plus_demographics · linear | linear | C_plus_demographics | 386613 | 118000 | 16.79 | 16.69 | 16.90 | 16.42 | 9.90 | 0.86 |
| ablation · A · D_plus_equipment · linear | linear | D_plus_equipment | 386613 | 118000 | 15.45 | 15.35 | 15.55 | 15.34 | 9.20 | 0.88 |
| ablation · A · A_squat · lightgbm | lightgbm | A_squat | 386613 | 118000 | 16.99 | 16.89 | 17.08 | 16.73 | 10.00 | 0.86 |
| ablation · A · B_squat_bench · lightgbm | lightgbm | B_squat_bench | 386613 | 118000 | 15.73 | 15.64 | 15.82 | 15.31 | 9.18 | 0.88 |
| ablation · A · C_plus_demographics · lightgbm | lightgbm | C_plus_demographics | 386613 | 118000 | 14.66 | 14.58 | 14.75 | 14.52 | 8.57 | 0.90 |
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 386613 | 118000 | 14.08 | 14.00 | 14.16 | 14.03 | 8.27 | 0.90 |
| ablation · A · A_squat · mlp · s42 | mlp | A_squat | 386613 | 118000 | 18.51 | 18.39 | 18.61 | 17.65 | 10.89 | 0.84 |
| ablation · A · B_squat_bench · mlp · s42 | mlp | B_squat_bench | 386613 | 118000 | 16.98 | 16.87 | 17.09 | 16.10 | 9.92 | 0.86 |
| ablation · A · C_plus_demographics · mlp · s42 | mlp | C_plus_demographics | 386613 | 118000 | 15.30 | 15.22 | 15.39 | 15.14 | 8.92 | 0.89 |
| ablation · A · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 386613 | 118000 | 14.30 | 14.22 | 14.38 | 14.23 | 8.34 | 0.90 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | ablation · A · B_squat_bench · linear | ablation · A · A_squat · linear | 386613 | 118000 | -1.29 | -1.34 | -1.24 |
| test | ablation · A · C_plus_demographics · linear | ablation · A · B_squat_bench · linear | 386613 | 118000 | -1.40 | -1.45 | -1.35 |
| test | ablation · A · D_plus_equipment · linear | ablation · A · C_plus_demographics · linear | 386613 | 118000 | -1.34 | -1.40 | -1.30 |
| test | ablation · A · D_plus_equipment · linear | ablation · A · A_squat · ratio | 386613 | 118000 | -6.46 | -6.61 | -6.36 |
| test | ablation · A · B_squat_bench · lightgbm | ablation · A · A_squat · lightgbm | 386613 | 118000 | -1.26 | -1.30 | -1.21 |
| test | ablation · A · C_plus_demographics · lightgbm | ablation · A · B_squat_bench · lightgbm | 386613 | 118000 | -1.07 | -1.13 | -1.02 |
| test | ablation · A · D_plus_equipment · lightgbm | ablation · A · C_plus_demographics · lightgbm | 386613 | 118000 | -0.58 | -0.62 | -0.55 |
| test | ablation · A · D_plus_equipment · lightgbm | ablation · A · A_squat · ratio | 386613 | 118000 | -7.83 | -7.99 | -7.71 |
| test | ablation · A · B_squat_bench · mlp · s42 | ablation · A · A_squat · mlp · s42 | 386613 | 118000 | -1.53 | -1.58 | -1.49 |
| test | ablation · A · C_plus_demographics · mlp · s42 | ablation · A · B_squat_bench · mlp · s42 | 386613 | 118000 | -1.68 | -1.74 | -1.63 |
| test | ablation · A · D_plus_equipment · mlp · s42 | ablation · A · C_plus_demographics · mlp · s42 | 386613 | 118000 | -1.00 | -1.04 | -0.96 |
| test | ablation · A · D_plus_equipment · mlp · s42 | ablation · A · A_squat · ratio | 386613 | 118000 | -7.61 | -7.76 | -7.50 |

## ablation_federation_extension — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| ablation · A · D_plus_equipment · linear | linear | D_plus_equipment | 386613 | 118000 | 15.45 | 15.35 | 15.55 | 15.34 | 9.20 | 0.88 |
| ablation · A · E_plus_federation · linear | linear | E_plus_federation | 386613 | 118000 | 14.86 | 14.78 | 14.96 | 14.77 | 8.86 | 0.89 |
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 386613 | 118000 | 14.08 | 14.00 | 14.16 | 14.03 | 8.27 | 0.90 |
| ablation · A · E_plus_federation · lightgbm | lightgbm | E_plus_federation | 386613 | 118000 | 13.83 | 13.76 | 13.91 | 13.74 | 8.12 | 0.91 |
| ablation · A · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 386613 | 118000 | 14.30 | 14.22 | 14.38 | 14.23 | 8.34 | 0.90 |
| ablation · A · E_plus_federation · mlp · s42 | mlp | E_plus_federation | 386613 | 118000 | 13.83 | 13.75 | 13.91 | 13.73 | 8.10 | 0.91 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | ablation · A · E_plus_federation · linear | ablation · A · D_plus_equipment · linear | 386613 | 118000 | -0.58 | -0.61 | -0.55 |
| test | ablation · A · E_plus_federation · lightgbm | ablation · A · D_plus_equipment · lightgbm | 386613 | 118000 | -0.25 | -0.27 | -0.23 |
| test | ablation · A · E_plus_federation · mlp · s42 | ablation · A · D_plus_equipment · mlp · s42 | 386613 | 118000 | -0.47 | -0.49 | -0.45 |

## models_D — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| ablation · A · A_squat · ratio | ratio | A_squat | 386613 | 118000 | 21.91 | 21.76 | 22.09 | 21.62 | 12.34 | 0.77 |
| ablation · A · D_plus_equipment · linear | linear | D_plus_equipment | 386613 | 118000 | 15.45 | 15.35 | 15.55 | 15.34 | 9.20 | 0.88 |
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 386613 | 118000 | 14.08 | 14.00 | 14.16 | 14.03 | 8.27 | 0.90 |
| ablation · A · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 386613 | 118000 | 14.30 | 14.22 | 14.38 | 14.23 | 8.34 | 0.90 |
| ablation · A · D_plus_equipment · mlp · s43 | mlp | D_plus_equipment | 386613 | 118000 | 14.30 | 14.22 | 14.38 | 14.23 | 8.36 | 0.90 |
| ablation · A · D_plus_equipment · mlp · s44 | mlp | D_plus_equipment | 386613 | 118000 | 14.31 | 14.23 | 14.39 | 14.26 | 8.35 | 0.90 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | ablation · A · D_plus_equipment · lightgbm | ablation · A · D_plus_equipment · linear | 386613 | 118000 | -1.37 | -1.41 | -1.31 |
| test | ablation · A · D_plus_equipment · lightgbm | ablation · A · A_squat · ratio | 386613 | 118000 | -7.83 | -7.99 | -7.71 |
| test | ablation · A · D_plus_equipment · mlp · s42 | ablation · A · D_plus_equipment · lightgbm | 386613 | 118000 | 0.22 | 0.20 | 0.24 |
| test | ablation · A · D_plus_equipment · mlp · s43 | ablation · A · D_plus_equipment · lightgbm | 386613 | 118000 | 0.22 | 0.20 | 0.24 |
| test | ablation · A · D_plus_equipment · mlp · s44 | ablation · A · D_plus_equipment · lightgbm | 386613 | 118000 | 0.23 | 0.21 | 0.25 |

## history_eligible — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| history · A · D_plus_equipment · last_deadlift · histrows | last_deadlift | D_plus_equipment | 268289 | 64764 | 13.44 | 13.33 | 13.56 | 14.08 | 7.95 | 0.86 |
| ablation · A · D_plus_equipment · linear | linear | D_plus_equipment | 268289 | 64764 | 15.57 | 15.45 | 15.72 | 15.18 | 8.87 | 0.88 |
| history · A · D_plus_equipment · linear · histrows | linear | D_plus_equipment | 268289 | 64764 | 15.59 | 15.48 | 15.73 | 15.30 | 8.95 | 0.88 |
| history · A · D_plus_equipment-history · linear · histrows | linear | D_plus_equipment+history | 268289 | 64764 | 9.86 | 9.80 | 9.94 | 9.75 | 5.80 | 0.94 |
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 268289 | 64764 | 14.20 | 14.10 | 14.32 | 13.99 | 8.05 | 0.90 |
| history · A · D_plus_equipment · lightgbm · histrows | lightgbm | D_plus_equipment | 268289 | 64764 | 14.23 | 14.13 | 14.34 | 14.05 | 8.09 | 0.90 |
| history · A · D_plus_equipment-history · lightgbm · histrows | lightgbm | D_plus_equipment+history | 268289 | 64764 | 8.73 | 8.69 | 8.79 | 8.80 | 5.13 | 0.95 |
| ablation · A · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 268289 | 64764 | 14.43 | 14.32 | 14.55 | 14.18 | 8.12 | 0.90 |
| history · A · D_plus_equipment-history · mlp · histrows · s42 | mlp | D_plus_equipment+history | 268289 | 64764 | 8.71 | 8.66 | 8.76 | 8.78 | 5.12 | 0.95 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | history · A · D_plus_equipment-history · linear · histrows | ablation · A · D_plus_equipment · linear | 268289 | 64764 | -5.71 | -5.82 | -5.62 |
| test | history · A · D_plus_equipment-history · linear · histrows | history · A · D_plus_equipment · linear · histrows | 268289 | 64764 | -5.73 | -5.84 | -5.64 |
| test | history · A · D_plus_equipment-history · linear · histrows | history · A · D_plus_equipment · last_deadlift · histrows | 268289 | 64764 | -3.58 | -3.65 | -3.50 |
| test | history · A · D_plus_equipment-history · lightgbm · histrows | ablation · A · D_plus_equipment · lightgbm | 268289 | 64764 | -5.48 | -5.58 | -5.39 |
| test | history · A · D_plus_equipment-history · lightgbm · histrows | history · A · D_plus_equipment · lightgbm · histrows | 268289 | 64764 | -5.50 | -5.60 | -5.41 |
| test | history · A · D_plus_equipment-history · lightgbm · histrows | history · A · D_plus_equipment · last_deadlift · histrows | 268289 | 64764 | -4.71 | -4.79 | -4.61 |
| test | history · A · D_plus_equipment-history · mlp · histrows · s42 | ablation · A · D_plus_equipment · mlp · s42 | 268289 | 64764 | -5.73 | -5.84 | -5.64 |
| test | history · A · D_plus_equipment-history · mlp · histrows · s42 | history · A · D_plus_equipment · last_deadlift · histrows | 268289 | 64764 | -4.73 | -4.81 | -4.64 |

## no_history_rows — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| ablation · A · A_squat · ratio | ratio | A_squat | 118324 | 118000 | 21.31 | 21.21 | 21.41 | 21.30 | 12.92 | 0.76 |
| ablation · A · D_plus_equipment · linear | linear | D_plus_equipment | 118324 | 118000 | 15.16 | 15.09 | 15.22 | 15.15 | 9.95 | 0.88 |
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 118324 | 118000 | 13.80 | 13.73 | 13.86 | 13.79 | 8.77 | 0.90 |
| ablation · A · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 118324 | 118000 | 14.00 | 13.94 | 14.06 | 13.99 | 8.84 | 0.89 |

## chrono_all — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| chrono · B · A_squat · ratio | ratio | A_squat | 402128 | 183630 | 21.25 | 21.14 | 21.35 | 21.60 | 12.44 | 0.79 |
| chrono · B · D_plus_equipment · linear | linear | D_plus_equipment | 402128 | 183630 | 15.13 | 15.07 | 15.20 | 15.39 | 9.42 | 0.89 |
| chrono · B · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 402128 | 183630 | 14.04 | 13.99 | 14.10 | 14.42 | 8.57 | 0.90 |
| chrono · B · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 402128 | 183630 | 14.00 | 13.95 | 14.06 | 14.38 | 8.55 | 0.90 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | chrono · B · D_plus_equipment · lightgbm | chrono · B · A_squat · ratio | 402128 | 183630 | -7.21 | -7.29 | -7.14 |
| test | chrono · B · D_plus_equipment · lightgbm | chrono · B · D_plus_equipment · linear | 402128 | 183630 | -1.09 | -1.12 | -1.05 |
| test | chrono · B · D_plus_equipment · mlp · s42 | chrono · B · D_plus_equipment · lightgbm | 402128 | 183630 | -0.04 | -0.05 | -0.03 |

## chrono_history_eligible — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| chrono · B · D_plus_equipment · last_deadlift · histrows | last_deadlift | D_plus_equipment | 301269 | 125023 | 12.54 | 12.46 | 12.63 | 13.87 | 7.67 | 0.88 |
| chrono · B · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 301269 | 125023 | 14.11 | 14.05 | 14.18 | 14.48 | 8.33 | 0.90 |
| chrono · B · D_plus_equipment · lightgbm · histrows | lightgbm | D_plus_equipment | 301269 | 125023 | 14.10 | 14.04 | 14.17 | 14.50 | 8.35 | 0.90 |
| chrono · B · D_plus_equipment-history · lightgbm · histrows | lightgbm | D_plus_equipment+history | 301269 | 125023 | 8.47 | 8.43 | 8.52 | 8.99 | 5.21 | 0.95 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | chrono · B · D_plus_equipment-history · lightgbm · histrows | chrono · B · D_plus_equipment · lightgbm · histrows | 301269 | 125023 | -5.62 | -5.68 | -5.57 |
| test | chrono · B · D_plus_equipment-history · lightgbm · histrows | chrono · B · D_plus_equipment · last_deadlift · histrows | 301269 | 125023 | -4.07 | -4.14 | -4.01 |
| test | chrono · B · D_plus_equipment-history · lightgbm · histrows | chrono · B · D_plus_equipment · lightgbm | 301269 | 125023 | -5.63 | -5.69 | -5.59 |

## transfer|Equipment=Single-ply — partition `test_transfer, test_in_dist`

**test_transfer**

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Equipment-Single-ply · A_squat · ratio | ratio | A_squat | 147373 | 44780 | 22.18 | 21.94 | 22.50 | 20.76 | 12.44 | 0.75 |
| transfer · C-Equipment-Single-ply · D_plus_equipment · linear | linear | D_plus_equipment | 147373 | 44780 | 15.86 | 15.70 | 16.03 | 15.71 | 9.45 | 0.88 |
| transfer · C-Equipment-Single-ply · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 147373 | 44780 | 16.00 | 15.83 | 16.17 | 15.58 | 9.44 | 0.87 |
| transfer · C-Equipment-Single-ply · C_plus_demographics · linear | linear | C_plus_demographics | 147373 | 44780 | 17.33 | 17.17 | 17.52 | 17.32 | 10.58 | 0.86 |
| transfer · C-Equipment-Single-ply · C_plus_demographics · lightgbm | lightgbm | C_plus_demographics | 147373 | 44780 | 15.31 | 15.17 | 15.46 | 15.50 | 9.05 | 0.88 |
| transfer · C-Equipment-Single-ply · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 147373 | 44780 | 24.09 | 23.90 | 24.32 | 22.72 | 14.30 | 0.75 |

**test_in_dist**

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Equipment-Single-ply · A_squat · ratio | ratio | A_squat | 239240 | 82600 | 21.68 | 21.47 | 21.87 | 20.96 | 12.22 | 0.77 |
| transfer · C-Equipment-Single-ply · D_plus_equipment · linear | linear | D_plus_equipment | 239240 | 82600 | 15.35 | 15.23 | 15.47 | 15.26 | 9.17 | 0.89 |
| transfer · C-Equipment-Single-ply · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 239240 | 82600 | 14.17 | 14.08 | 14.27 | 14.16 | 8.30 | 0.90 |
| transfer · C-Equipment-Single-ply · C_plus_demographics · linear | linear | C_plus_demographics | 239240 | 82600 | 16.74 | 16.61 | 16.87 | 16.32 | 9.88 | 0.86 |
| transfer · C-Equipment-Single-ply · C_plus_demographics · lightgbm | lightgbm | C_plus_demographics | 239240 | 82600 | 14.76 | 14.66 | 14.86 | 14.66 | 8.62 | 0.89 |
| transfer · C-Equipment-Single-ply · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 239240 | 82600 | 14.18 | 14.08 | 14.28 | 14.15 | 8.28 | 0.90 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test_transfer | transfer · C-Equipment-Single-ply · D_plus_equipment · lightgbm | transfer · C-Equipment-Single-ply · C_plus_demographics · lightgbm | 147373 | 44780 | 0.69 | 0.58 | 0.79 |
| test_transfer | transfer · C-Equipment-Single-ply · D_plus_equipment · lightgbm | transfer · C-Equipment-Single-ply · A_squat · ratio | 147373 | 44780 | -6.18 | -6.44 | -5.94 |
| test_in_dist | transfer · C-Equipment-Single-ply · D_plus_equipment · lightgbm | transfer · C-Equipment-Single-ply · C_plus_demographics · lightgbm | 239240 | 82600 | -0.59 | -0.63 | -0.56 |
| test_in_dist | transfer · C-Equipment-Single-ply · D_plus_equipment · lightgbm | transfer · C-Equipment-Single-ply · A_squat · ratio | 239240 | 82600 | -7.51 | -7.69 | -7.36 |

## transfer|Equipment=Unlimited — partition `test_transfer, test_in_dist`

**test_transfer**

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Equipment-Unlimited · A_squat · ratio | ratio | A_squat | 40208 | 9449 | 19.16 | 18.75 | 19.49 | 18.30 | 13.30 | 0.68 |
| transfer · C-Equipment-Unlimited · D_plus_equipment · linear | linear | D_plus_equipment | 40208 | 9449 | 62.82 | 62.45 | 63.18 | 62.83 | 48.30 | -0.93 |
| transfer · C-Equipment-Unlimited · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 40208 | 9449 | 15.06 | 14.78 | 15.28 | 15.28 | 11.19 | 0.82 |
| transfer · C-Equipment-Unlimited · C_plus_demographics · linear | linear | C_plus_demographics | 40208 | 9449 | 15.81 | 15.51 | 16.09 | 16.14 | 11.70 | 0.80 |
| transfer · C-Equipment-Unlimited · C_plus_demographics · lightgbm | lightgbm | C_plus_demographics | 40208 | 9449 | 13.14 | 12.90 | 13.34 | 13.40 | 9.82 | 0.87 |
| transfer · C-Equipment-Unlimited · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 40208 | 9449 | 31.38 | 30.97 | 31.87 | 30.45 | 22.20 | 0.38 |

**test_in_dist**

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Equipment-Unlimited · A_squat · ratio | ratio | A_squat | 346405 | 111120 | 22.13 | 21.97 | 22.28 | 21.57 | 12.18 | 0.76 |
| transfer · C-Equipment-Unlimited · D_plus_equipment · linear | linear | D_plus_equipment | 346405 | 111120 | 15.74 | 15.63 | 15.85 | 15.48 | 9.17 | 0.88 |
| transfer · C-Equipment-Unlimited · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 346405 | 111120 | 14.39 | 14.31 | 14.48 | 14.20 | 8.27 | 0.90 |
| transfer · C-Equipment-Unlimited · C_plus_demographics · linear | linear | C_plus_demographics | 346405 | 111120 | 17.01 | 16.91 | 17.11 | 16.41 | 9.85 | 0.86 |
| transfer · C-Equipment-Unlimited · C_plus_demographics · lightgbm | lightgbm | C_plus_demographics | 346405 | 111120 | 14.97 | 14.88 | 15.05 | 14.64 | 8.56 | 0.89 |
| transfer · C-Equipment-Unlimited · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 346405 | 111120 | 14.64 | 14.55 | 14.72 | 14.41 | 8.35 | 0.89 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test_transfer | transfer · C-Equipment-Unlimited · D_plus_equipment · lightgbm | transfer · C-Equipment-Unlimited · C_plus_demographics · lightgbm | 40208 | 9449 | 1.92 | 1.83 | 2.01 |
| test_transfer | transfer · C-Equipment-Unlimited · D_plus_equipment · lightgbm | transfer · C-Equipment-Unlimited · A_squat · ratio | 40208 | 9449 | -4.10 | -4.40 | -3.83 |
| test_in_dist | transfer · C-Equipment-Unlimited · D_plus_equipment · lightgbm | transfer · C-Equipment-Unlimited · C_plus_demographics · lightgbm | 346405 | 111120 | -0.57 | -0.61 | -0.54 |
| test_in_dist | transfer · C-Equipment-Unlimited · D_plus_equipment · lightgbm | transfer · C-Equipment-Unlimited · A_squat · ratio | 346405 | 111120 | -7.74 | -7.87 | -7.60 |

## transfer|Equipment=Wraps — partition `test_transfer, test_in_dist`

**test_transfer**

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Equipment-Wraps · A_squat · ratio | ratio | A_squat | 31414 | 15236 | 23.13 | 22.76 | 23.50 | 22.76 | 12.38 | 0.75 |
| transfer · C-Equipment-Wraps · D_plus_equipment · linear | linear | D_plus_equipment | 31414 | 15236 | 83.87 | 83.37 | 84.27 | 83.50 | 47.10 | -0.97 |
| transfer · C-Equipment-Wraps · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 31414 | 15236 | 22.22 | 21.83 | 22.64 | 21.14 | 11.05 | 0.78 |
| transfer · C-Equipment-Wraps · C_plus_demographics · linear | linear | C_plus_demographics | 31414 | 15236 | 17.44 | 17.18 | 17.73 | 17.34 | 9.67 | 0.85 |
| transfer · C-Equipment-Wraps · C_plus_demographics · lightgbm | lightgbm | C_plus_demographics | 31414 | 15236 | 17.00 | 16.69 | 17.28 | 16.70 | 9.36 | 0.86 |
| transfer · C-Equipment-Wraps · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 31414 | 15236 | 18.72 | 18.44 | 19.02 | 18.14 | 10.61 | 0.84 |

**test_in_dist**

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Equipment-Wraps · A_squat · ratio | ratio | A_squat | 355199 | 109462 | 21.83 | 21.68 | 21.98 | 21.69 | 12.36 | 0.77 |
| transfer · C-Equipment-Wraps · D_plus_equipment · linear | linear | D_plus_equipment | 355199 | 109462 | 15.35 | 15.25 | 15.45 | 15.32 | 9.18 | 0.88 |
| transfer · C-Equipment-Wraps · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 355199 | 109462 | 13.92 | 13.83 | 14.01 | 13.93 | 8.21 | 0.90 |
| transfer · C-Equipment-Wraps · C_plus_demographics · linear | linear | C_plus_demographics | 355199 | 109462 | 16.75 | 16.65 | 16.86 | 16.46 | 9.91 | 0.86 |
| transfer · C-Equipment-Wraps · C_plus_demographics · lightgbm | lightgbm | C_plus_demographics | 355199 | 109462 | 14.46 | 14.37 | 14.55 | 14.39 | 8.50 | 0.90 |
| transfer · C-Equipment-Wraps · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 355199 | 109462 | 14.17 | 14.08 | 14.26 | 14.18 | 8.33 | 0.90 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test_transfer | transfer · C-Equipment-Wraps · D_plus_equipment · lightgbm | transfer · C-Equipment-Wraps · C_plus_demographics · lightgbm | 31414 | 15236 | 5.23 | 4.92 | 5.51 |
| test_transfer | transfer · C-Equipment-Wraps · D_plus_equipment · lightgbm | transfer · C-Equipment-Wraps · A_squat · ratio | 31414 | 15236 | -0.90 | -1.31 | -0.47 |
| test_in_dist | transfer · C-Equipment-Wraps · D_plus_equipment · lightgbm | transfer · C-Equipment-Wraps · C_plus_demographics · lightgbm | 355199 | 109462 | -0.55 | -0.58 | -0.51 |
| test_in_dist | transfer · C-Equipment-Wraps · D_plus_equipment · lightgbm | transfer · C-Equipment-Wraps · A_squat · ratio | 355199 | 109462 | -7.91 | -8.06 | -7.77 |

## transfer|Equipment=Multi-ply — partition `test_transfer, test_in_dist`

**test_transfer**

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Equipment-Multi-ply · A_squat · ratio | ratio | A_squat | 7369 | 3006 | 51.62 | 49.16 | 54.45 | 40.85 | 22.29 | -0.22 |
| transfer · C-Equipment-Multi-ply · D_plus_equipment · linear | linear | D_plus_equipment | 7369 | 3006 | 116.70 | 114.78 | 118.46 | 108.07 | 54.90 | -2.80 |
| transfer · C-Equipment-Multi-ply · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 7369 | 3006 | 22.62 | 21.83 | 23.54 | 21.22 | 10.94 | 0.75 |
| transfer · C-Equipment-Multi-ply · C_plus_demographics · linear | linear | C_plus_demographics | 7369 | 3006 | 34.68 | 33.09 | 36.21 | 28.48 | 16.15 | 0.44 |
| transfer · C-Equipment-Multi-ply · C_plus_demographics · lightgbm | lightgbm | C_plus_demographics | 7369 | 3006 | 25.72 | 24.76 | 26.76 | 23.73 | 12.56 | 0.69 |
| transfer · C-Equipment-Multi-ply · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 7369 | 3006 | 38.60 | 37.27 | 39.97 | 33.56 | 18.16 | 0.41 |

**test_in_dist**

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Equipment-Multi-ply · A_squat · ratio | ratio | A_squat | 379244 | 116572 | 21.24 | 21.10 | 21.37 | 21.05 | 12.10 | 0.79 |
| transfer · C-Equipment-Multi-ply · D_plus_equipment · linear | linear | D_plus_equipment | 379244 | 116572 | 15.18 | 15.10 | 15.27 | 15.14 | 9.08 | 0.89 |
| transfer · C-Equipment-Multi-ply · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 379244 | 116572 | 13.95 | 13.88 | 14.04 | 13.96 | 8.23 | 0.90 |
| transfer · C-Equipment-Multi-ply · C_plus_demographics · linear | linear | C_plus_demographics | 379244 | 116572 | 16.39 | 16.30 | 16.50 | 16.13 | 9.71 | 0.87 |
| transfer · C-Equipment-Multi-ply · C_plus_demographics · lightgbm | lightgbm | C_plus_demographics | 379244 | 116572 | 14.46 | 14.38 | 14.55 | 14.40 | 8.49 | 0.90 |
| transfer · C-Equipment-Multi-ply · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 379244 | 116572 | 14.18 | 14.11 | 14.27 | 14.19 | 8.34 | 0.90 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test_transfer | transfer · C-Equipment-Multi-ply · D_plus_equipment · lightgbm | transfer · C-Equipment-Multi-ply · C_plus_demographics · lightgbm | 7369 | 3006 | -3.09 | -3.76 | -2.46 |
| test_transfer | transfer · C-Equipment-Multi-ply · D_plus_equipment · lightgbm | transfer · C-Equipment-Multi-ply · A_squat · ratio | 7369 | 3006 | -28.99 | -31.49 | -26.62 |
| test_in_dist | transfer · C-Equipment-Multi-ply · D_plus_equipment · lightgbm | transfer · C-Equipment-Multi-ply · C_plus_demographics · lightgbm | 379244 | 116572 | -0.50 | -0.53 | -0.47 |
| test_in_dist | transfer · C-Equipment-Multi-ply · D_plus_equipment · lightgbm | transfer · C-Equipment-Multi-ply · A_squat · ratio | 379244 | 116572 | -7.29 | -7.40 | -7.16 |

## transfer|Federation=THSPA — partition `test_transfer, test_in_dist`

**test_transfer**

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Federation-THSPA · A_squat · ratio | ratio | A_squat | 69477 | 16983 | 20.45 | 20.13 | 20.75 | 18.81 | 11.63 | 0.48 |
| transfer · C-Federation-THSPA · E_plus_federation · linear | linear | E_plus_federation | 69477 | 16983 | 18.64 | 18.42 | 18.86 | 18.53 | 11.64 | 0.63 |
| transfer · C-Federation-THSPA · E_plus_federation · lightgbm | lightgbm | E_plus_federation | 69477 | 16983 | 19.97 | 19.74 | 20.20 | 20.22 | 12.21 | 0.59 |
| transfer · C-Federation-THSPA · D_plus_equipment · linear | linear | D_plus_equipment | 69477 | 16983 | 17.87 | 17.67 | 18.10 | 17.76 | 11.12 | 0.66 |
| transfer · C-Federation-THSPA · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 69477 | 16983 | 18.42 | 18.20 | 18.62 | 18.65 | 11.24 | 0.64 |
| transfer · C-Federation-THSPA · E_plus_federation · mlp · s42 | mlp | E_plus_federation | 69477 | 16983 | 19.97 | 19.74 | 20.20 | 20.00 | 12.12 | 0.58 |

**test_in_dist**

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Federation-THSPA · A_squat · ratio | ratio | A_squat | 317136 | 102851 | 22.10 | 21.91 | 22.28 | 21.60 | 12.42 | 0.79 |
| transfer · C-Federation-THSPA · E_plus_federation · linear | linear | E_plus_federation | 317136 | 102851 | 15.07 | 14.95 | 15.17 | 14.93 | 8.97 | 0.90 |
| transfer · C-Federation-THSPA · E_plus_federation · lightgbm | lightgbm | E_plus_federation | 317136 | 102851 | 13.99 | 13.88 | 14.07 | 13.87 | 8.20 | 0.91 |
| transfer · C-Federation-THSPA · D_plus_equipment · linear | linear | D_plus_equipment | 317136 | 102851 | 15.39 | 15.27 | 15.49 | 15.23 | 9.19 | 0.90 |
| transfer · C-Federation-THSPA · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 317136 | 102851 | 14.21 | 14.12 | 14.32 | 14.13 | 8.34 | 0.91 |
| transfer · C-Federation-THSPA · E_plus_federation · mlp · s42 | mlp | E_plus_federation | 317136 | 102851 | 14.02 | 13.92 | 14.11 | 13.86 | 8.17 | 0.91 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test_transfer | transfer · C-Federation-THSPA · E_plus_federation · lightgbm | transfer · C-Federation-THSPA · D_plus_equipment · lightgbm | 69477 | 16983 | 1.55 | 1.48 | 1.60 |
| test_transfer | transfer · C-Federation-THSPA · E_plus_federation · lightgbm | transfer · C-Federation-THSPA · A_squat · ratio | 69477 | 16983 | -0.48 | -0.75 | -0.23 |
| test_in_dist | transfer · C-Federation-THSPA · E_plus_federation · lightgbm | transfer · C-Federation-THSPA · D_plus_equipment · lightgbm | 317136 | 102851 | -0.23 | -0.25 | -0.21 |
| test_in_dist | transfer · C-Federation-THSPA · E_plus_federation · lightgbm | transfer · C-Federation-THSPA · A_squat · ratio | 317136 | 102851 | -8.11 | -8.27 | -7.97 |

## transfer|Federation=USAPL — partition `test_transfer, test_in_dist`

**test_transfer**

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Federation-USAPL · A_squat · ratio | ratio | A_squat | 43006 | 17917 | 22.10 | 21.81 | 22.36 | 22.24 | 12.27 | 0.76 |
| transfer · C-Federation-USAPL · E_plus_federation · linear | linear | E_plus_federation | 43006 | 17917 | 15.36 | 15.15 | 15.55 | 15.17 | 9.16 | 0.88 |
| transfer · C-Federation-USAPL · E_plus_federation · lightgbm | lightgbm | E_plus_federation | 43006 | 17917 | 14.34 | 14.13 | 14.54 | 14.21 | 8.25 | 0.89 |
| transfer · C-Federation-USAPL · D_plus_equipment · linear | linear | D_plus_equipment | 43006 | 17917 | 15.43 | 15.22 | 15.61 | 15.30 | 9.20 | 0.88 |
| transfer · C-Federation-USAPL · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 43006 | 17917 | 14.38 | 14.17 | 14.57 | 14.26 | 8.24 | 0.89 |
| transfer · C-Federation-USAPL · E_plus_federation · mlp · s42 | mlp | E_plus_federation | 43006 | 17917 | 14.33 | 14.13 | 14.51 | 14.20 | 8.19 | 0.89 |

**test_in_dist**

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Federation-USAPL · A_squat · ratio | ratio | A_squat | 343607 | 105792 | 22.02 | 21.86 | 22.17 | 21.89 | 12.43 | 0.77 |
| transfer · C-Federation-USAPL · E_plus_federation · linear | linear | E_plus_federation | 343607 | 105792 | 14.82 | 14.72 | 14.92 | 14.78 | 8.85 | 0.89 |
| transfer · C-Federation-USAPL · E_plus_federation · lightgbm | lightgbm | E_plus_federation | 343607 | 105792 | 13.79 | 13.72 | 13.88 | 13.73 | 8.13 | 0.91 |
| transfer · C-Federation-USAPL · D_plus_equipment · linear | linear | D_plus_equipment | 343607 | 105792 | 15.46 | 15.36 | 15.57 | 15.41 | 9.22 | 0.88 |
| transfer · C-Federation-USAPL · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 343607 | 105792 | 14.06 | 13.98 | 14.14 | 14.04 | 8.29 | 0.90 |
| transfer · C-Federation-USAPL · E_plus_federation · mlp · s42 | mlp | E_plus_federation | 343607 | 105792 | 13.81 | 13.75 | 13.90 | 13.76 | 8.15 | 0.91 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test_transfer | transfer · C-Federation-USAPL · E_plus_federation · lightgbm | transfer · C-Federation-USAPL · D_plus_equipment · lightgbm | 43006 | 17917 | -0.04 | -0.08 | 0.01 |
| test_transfer | transfer · C-Federation-USAPL · E_plus_federation · lightgbm | transfer · C-Federation-USAPL · A_squat · ratio | 43006 | 17917 | -7.76 | -7.99 | -7.45 |
| test_in_dist | transfer · C-Federation-USAPL · E_plus_federation · lightgbm | transfer · C-Federation-USAPL · D_plus_equipment · lightgbm | 343607 | 105792 | -0.27 | -0.29 | -0.25 |
| test_in_dist | transfer · C-Federation-USAPL · E_plus_federation · lightgbm | transfer · C-Federation-USAPL · A_squat · ratio | 343607 | 105792 | -8.23 | -8.39 | -8.11 |

## transfer|Federation=THSWPA — partition `test_transfer, test_in_dist`

**test_transfer**

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Federation-THSWPA · A_squat · ratio | ratio | A_squat | 42326 | 8254 | 16.30 | 15.95 | 16.61 | 14.36 | 14.46 | 0.17 |
| transfer · C-Federation-THSWPA · E_plus_federation · linear | linear | E_plus_federation | 42326 | 8254 | 10.59 | 10.43 | 10.75 | 10.61 | 10.25 | 0.68 |
| transfer · C-Federation-THSWPA · E_plus_federation · lightgbm | lightgbm | E_plus_federation | 42326 | 8254 | 12.70 | 12.51 | 12.88 | 13.06 | 12.53 | 0.58 |
| transfer · C-Federation-THSWPA · D_plus_equipment · linear | linear | D_plus_equipment | 42326 | 8254 | 10.89 | 10.70 | 11.06 | 10.73 | 9.96 | 0.67 |
| transfer · C-Federation-THSWPA · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 42326 | 8254 | 12.28 | 12.09 | 12.45 | 12.62 | 12.08 | 0.60 |
| transfer · C-Federation-THSWPA · E_plus_federation · mlp · s42 | mlp | E_plus_federation | 42326 | 8254 | 14.43 | 14.23 | 14.63 | 14.64 | 14.22 | 0.48 |

**test_in_dist**

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Federation-THSWPA · A_squat · ratio | ratio | A_squat | 344287 | 110287 | 22.61 | 22.45 | 22.78 | 21.92 | 12.10 | 0.73 |
| transfer · C-Federation-THSWPA · E_plus_federation · linear | linear | E_plus_federation | 344287 | 110287 | 15.51 | 15.43 | 15.61 | 15.14 | 8.84 | 0.87 |
| transfer · C-Federation-THSWPA · E_plus_federation · lightgbm | lightgbm | E_plus_federation | 344287 | 110287 | 14.40 | 14.33 | 14.49 | 14.07 | 8.07 | 0.89 |
| transfer · C-Federation-THSWPA · D_plus_equipment · linear | linear | D_plus_equipment | 344287 | 110287 | 16.10 | 16.01 | 16.20 | 15.71 | 9.17 | 0.86 |
| transfer · C-Federation-THSWPA · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 344287 | 110287 | 14.67 | 14.59 | 14.75 | 14.37 | 8.22 | 0.88 |
| transfer · C-Federation-THSWPA · E_plus_federation · mlp · s42 | mlp | E_plus_federation | 344287 | 110287 | 14.41 | 14.34 | 14.49 | 14.08 | 8.06 | 0.89 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test_transfer | transfer · C-Federation-THSWPA · E_plus_federation · lightgbm | transfer · C-Federation-THSWPA · D_plus_equipment · lightgbm | 42326 | 8254 | 0.42 | 0.39 | 0.46 |
| test_transfer | transfer · C-Federation-THSWPA · E_plus_federation · lightgbm | transfer · C-Federation-THSWPA · A_squat · ratio | 42326 | 8254 | -3.59 | -3.91 | -3.33 |
| test_in_dist | transfer · C-Federation-THSWPA · E_plus_federation · lightgbm | transfer · C-Federation-THSWPA · D_plus_equipment · lightgbm | 344287 | 110287 | -0.27 | -0.29 | -0.25 |
| test_in_dist | transfer · C-Federation-THSWPA · E_plus_federation · lightgbm | transfer · C-Federation-THSWPA · A_squat · ratio | 344287 | 110287 | -8.21 | -8.34 | -8.07 |

## capacity_D — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 386613 | 118000 | 14.08 | 14.00 | 14.16 | 14.03 | 8.27 | 0.90 |
| capacity · A · D_plus_equipment · lightgbm · lgbm_big | lightgbm | D_plus_equipment | 386613 | 118000 | 14.08 | 14.01 | 14.16 | 14.02 | 8.27 | 0.90 |
| ablation · A · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 386613 | 118000 | 14.30 | 14.22 | 14.38 | 14.23 | 8.34 | 0.90 |
| capacity · A · D_plus_equipment · mlp · mlp_wide · s42 | mlp | D_plus_equipment | 386613 | 118000 | 14.32 | 14.24 | 14.40 | 14.27 | 8.36 | 0.90 |
| capacity · A · D_plus_equipment · mlp · mlp_deep · s42 | mlp | D_plus_equipment | 386613 | 118000 | 14.29 | 14.22 | 14.37 | 14.25 | 8.35 | 0.90 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | capacity · A · D_plus_equipment · lightgbm · lgbm_big | ablation · A · D_plus_equipment · lightgbm | 386613 | 118000 | 0.00 | -0.00 | 0.01 |
| test | capacity · A · D_plus_equipment · mlp · mlp_wide · s42 | ablation · A · D_plus_equipment · mlp · s42 | 386613 | 118000 | 0.02 | 0.01 | 0.03 |
| test | capacity · A · D_plus_equipment · mlp · mlp_deep · s42 | ablation · A · D_plus_equipment · mlp · s42 | 386613 | 118000 | -0.01 | -0.02 | 0.00 |

## capacity_D_history — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| history · A · D_plus_equipment-history · lightgbm · histrows | lightgbm | D_plus_equipment+history | 268289 | 64764 | 8.73 | 8.69 | 8.79 | 8.80 | 5.13 | 0.95 |
| capacity · A · D_plus_equipment-history · lightgbm · histrows · lgbm_big | lightgbm | D_plus_equipment+history | 268289 | 64764 | 8.69 | 8.65 | 8.75 | 8.76 | 5.11 | 0.95 |
| history · A · D_plus_equipment-history · mlp · histrows · s42 | mlp | D_plus_equipment+history | 268289 | 64764 | 8.71 | 8.66 | 8.76 | 8.78 | 5.12 | 0.95 |
| capacity · A · D_plus_equipment-history · mlp · histrows · mlp_wide · s42 | mlp | D_plus_equipment+history | 268289 | 64764 | 8.69 | 8.64 | 8.74 | 8.76 | 5.11 | 0.95 |
| capacity · A · D_plus_equipment-history · mlp · histrows · mlp_deep · s42 | mlp | D_plus_equipment+history | 268289 | 64764 | 8.68 | 8.64 | 8.73 | 8.76 | 5.09 | 0.95 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | capacity · A · D_plus_equipment-history · lightgbm · histrows · lgbm_big | history · A · D_plus_equipment-history · lightgbm · histrows | 268289 | 64764 | -0.03 | -0.04 | -0.03 |
| test | capacity · A · D_plus_equipment-history · mlp · histrows · mlp_wide · s42 | history · A · D_plus_equipment-history · mlp · histrows · s42 | 268289 | 64764 | -0.02 | -0.03 | -0.02 |
| test | capacity · A · D_plus_equipment-history · mlp · histrows · mlp_deep · s42 | history · A · D_plus_equipment-history · mlp · histrows · s42 | 268289 | 64764 | -0.03 | -0.04 | -0.02 |

## history_rich_A — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| history · A · D_plus_equipment · last_deadlift · histrows | last_deadlift | D_plus_equipment | 268289 | 64764 | 13.44 | 13.33 | 13.56 | 14.08 | 7.95 | 0.86 |
| history · A · D_plus_equipment-history · lightgbm · histrows | lightgbm | D_plus_equipment+history | 268289 | 64764 | 8.73 | 8.69 | 8.79 | 8.80 | 5.13 | 0.95 |
| history · A · D_plus_equipment-history · mlp · histrows · s42 | mlp | D_plus_equipment+history | 268289 | 64764 | 8.71 | 8.66 | 8.76 | 8.78 | 5.12 | 0.95 |
| history_rich · A · D_plus_equipment-history_rich · lightgbm · histrows | lightgbm | D_plus_equipment+history_rich | 268289 | 64764 | 8.41 | 8.37 | 8.47 | 8.64 | 4.97 | 0.96 |
| history_rich · A · D_plus_equipment-history_rich · mlp · histrows · s42 | mlp | D_plus_equipment+history_rich | 268289 | 64764 | 8.38 | 8.34 | 8.44 | 8.63 | 4.95 | 0.96 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | history_rich · A · D_plus_equipment-history_rich · lightgbm · histrows | history · A · D_plus_equipment-history · lightgbm · histrows | 268289 | 64764 | -0.32 | -0.34 | -0.30 |
| test | history_rich · A · D_plus_equipment-history_rich · mlp · histrows · s42 | history · A · D_plus_equipment-history · mlp · histrows · s42 | 268289 | 64764 | -0.33 | -0.34 | -0.31 |
| test | history_rich · A · D_plus_equipment-history_rich · lightgbm · histrows | history · A · D_plus_equipment · last_deadlift · histrows | 268289 | 64764 | -5.03 | -5.11 | -4.94 |
| test | history_rich · A · D_plus_equipment-history_rich · mlp · histrows · s42 | history_rich · A · D_plus_equipment-history_rich · lightgbm · histrows | 268289 | 64764 | -0.03 | -0.04 | -0.01 |

## history_rich_B — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| chrono · B · D_plus_equipment · last_deadlift · histrows | last_deadlift | D_plus_equipment | 301269 | 125023 | 12.54 | 12.46 | 12.63 | 13.87 | 7.67 | 0.88 |
| chrono · B · D_plus_equipment-history · lightgbm · histrows | lightgbm | D_plus_equipment+history | 301269 | 125023 | 8.47 | 8.43 | 8.52 | 8.99 | 5.21 | 0.95 |
| history_rich · B · D_plus_equipment-history_rich · lightgbm · histrows | lightgbm | D_plus_equipment+history_rich | 301269 | 125023 | 8.17 | 8.12 | 8.21 | 8.75 | 5.05 | 0.96 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | history_rich · B · D_plus_equipment-history_rich · lightgbm · histrows | chrono · B · D_plus_equipment-history · lightgbm · histrows | 301269 | 125023 | -0.31 | -0.32 | -0.29 |
| test | history_rich · B · D_plus_equipment-history_rich · lightgbm · histrows | chrono · B · D_plus_equipment · last_deadlift · histrows | 301269 | 125023 | -4.38 | -4.44 | -4.32 |

## ensemble|A|D — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 386613 | 118000 | 14.08 | 14.00 | 14.16 | 14.03 | 8.27 | 0.90 |
| ablation · A · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 386613 | 118000 | 14.30 | 14.22 | 14.38 | 14.23 | 8.34 | 0.90 |
| ensemble · A · D_plus_equipment · lgbm_mlp | ensemble | D_plus_equipment | 386613 | 118000 | 14.08 | 14.01 | 14.16 | 14.02 | 8.26 | 0.90 |
| expanded · A · X_all-anyhist · lightgbm | lightgbm | X_all+anyhist | 386613 | 118000 | 10.29 | 10.24 | 10.34 | 11.71 | 6.21 | 0.94 |
| expanded · A · X_all-anyhist · mlp · s42 | mlp | X_all+anyhist | 386613 | 118000 | 10.29 | 10.24 | 10.34 | 11.75 | 6.25 | 0.94 |
| ensemble · A · X_all-anyhist · lgbm_mlp | ensemble | X_all+anyhist | 386613 | 118000 | 10.19 | 10.14 | 10.24 | 11.65 | 6.18 | 0.94 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | ensemble · A · D_plus_equipment · lgbm_mlp | ablation · A · D_plus_equipment · lightgbm | 386613 | 118000 | 0.00 | -0.00 | 0.01 |
| test | ensemble · A · D_plus_equipment · lgbm_mlp | ablation · A · D_plus_equipment · mlp · s42 | 386613 | 118000 | -0.22 | -0.23 | -0.20 |
| test | ensemble · A · X_all-anyhist · lgbm_mlp | expanded · A · X_all-anyhist · lightgbm | 386613 | 118000 | -0.09 | -0.10 | -0.09 |
| test | ensemble · A · X_all-anyhist · lgbm_mlp | expanded · A · X_all-anyhist · mlp · s42 | 386613 | 118000 | -0.10 | -0.10 | -0.09 |

## ensemble|A|history_rich — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| history_rich · A · D_plus_equipment-history_rich · lightgbm · histrows | lightgbm | D_plus_equipment+history_rich | 268289 | 64764 | 8.41 | 8.37 | 8.47 | 8.64 | 4.97 | 0.96 |
| history_rich · A · D_plus_equipment-history_rich · mlp · histrows · s42 | mlp | D_plus_equipment+history_rich | 268289 | 64764 | 8.38 | 8.34 | 8.44 | 8.63 | 4.95 | 0.96 |
| ensemble · A · D_plus_equipment-history_rich · lgbm_mlp · histrows | ensemble | D_plus_equipment+history_rich | 268289 | 64764 | 8.32 | 8.28 | 8.38 | 8.57 | 4.92 | 0.96 |
| expanded · A · X_all-history_rich-anyhist · lightgbm · histrows | lightgbm | X_all+history_rich+anyhist | 268289 | 64764 | 8.36 | 8.32 | 8.42 | 8.57 | 4.93 | 0.96 |
| expanded · A · X_all-history_rich-anyhist · mlp · histrows · s42 | mlp | X_all+history_rich+anyhist | 268289 | 64764 | 8.33 | 8.29 | 8.39 | 8.56 | 4.93 | 0.96 |
| ensemble · A · X_all-history_rich-anyhist · lgbm_mlp · histrows | ensemble | X_all+history_rich+anyhist | 268289 | 64764 | 8.25 | 8.21 | 8.30 | 8.47 | 4.88 | 0.96 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | ensemble · A · D_plus_equipment-history_rich · lgbm_mlp · histrows | history_rich · A · D_plus_equipment-history_rich · lightgbm · histrows | 268289 | 64764 | -0.09 | -0.10 | -0.08 |
| test | ensemble · A · D_plus_equipment-history_rich · lgbm_mlp · histrows | history_rich · A · D_plus_equipment-history_rich · mlp · histrows · s42 | 268289 | 64764 | -0.06 | -0.07 | -0.06 |
| test | ensemble · A · X_all-history_rich-anyhist · lgbm_mlp · histrows | expanded · A · X_all-history_rich-anyhist · lightgbm · histrows | 268289 | 64764 | -0.12 | -0.12 | -0.11 |
| test | ensemble · A · X_all-history_rich-anyhist · lgbm_mlp · histrows | expanded · A · X_all-history_rich-anyhist · mlp · histrows · s42 | 268289 | 64764 | -0.09 | -0.09 | -0.08 |

## ensemble|B|D — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| chrono · B · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 402128 | 183630 | 14.04 | 13.99 | 14.10 | 14.42 | 8.57 | 0.90 |
| chrono · B · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 402128 | 183630 | 14.00 | 13.95 | 14.06 | 14.38 | 8.55 | 0.90 |
| ensemble · B · D_plus_equipment · lgbm_mlp | ensemble | D_plus_equipment | 402128 | 183630 | 13.97 | 13.92 | 14.03 | 14.36 | 8.52 | 0.91 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | ensemble · B · D_plus_equipment · lgbm_mlp | chrono · B · D_plus_equipment · lightgbm | 402128 | 183630 | -0.07 | -0.08 | -0.07 |
| test | ensemble · B · D_plus_equipment · lgbm_mlp | chrono · B · D_plus_equipment · mlp · s42 | 402128 | 183630 | -0.03 | -0.04 | -0.02 |

## expanded_all_rows — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 386613 | 118000 | 14.08 | 14.00 | 14.16 | 14.03 | 8.27 | 0.90 |
| ablation · A · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 386613 | 118000 | 14.30 | 14.22 | 14.38 | 14.23 | 8.34 | 0.90 |
| expanded · A · X_attempts · lightgbm | lightgbm | X_attempts | 386613 | 118000 | 14.02 | 13.95 | 14.10 | 13.95 | 8.23 | 0.90 |
| expanded · A · X_attempts · mlp · s42 | mlp | X_attempts | 386613 | 118000 | 14.26 | 14.18 | 14.34 | 14.20 | 8.35 | 0.90 |
| expanded · A · X_context · lightgbm | lightgbm | X_context | 386613 | 118000 | 13.71 | 13.64 | 13.80 | 13.63 | 8.06 | 0.91 |
| expanded · A · X_context · mlp · s42 | mlp | X_context | 386613 | 118000 | 13.75 | 13.67 | 13.82 | 13.68 | 8.07 | 0.91 |
| expanded · A · X_all · lightgbm | lightgbm | X_all | 386613 | 118000 | 13.68 | 13.61 | 13.76 | 13.58 | 8.03 | 0.91 |
| expanded · A · X_all · mlp · s42 | mlp | X_all | 386613 | 118000 | 13.71 | 13.63 | 13.79 | 13.61 | 8.05 | 0.91 |
| expanded · A · X_all-anyhist · lightgbm | lightgbm | X_all+anyhist | 386613 | 118000 | 10.29 | 10.24 | 10.34 | 11.71 | 6.21 | 0.94 |
| expanded · A · X_all-anyhist · mlp · s42 | mlp | X_all+anyhist | 386613 | 118000 | 10.29 | 10.24 | 10.34 | 11.75 | 6.25 | 0.94 |
| ensemble · A · X_all-anyhist · lgbm_mlp | ensemble | X_all+anyhist | 386613 | 118000 | 10.19 | 10.14 | 10.24 | 11.65 | 6.18 | 0.94 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | expanded · A · X_attempts · lightgbm | ablation · A · D_plus_equipment · lightgbm | 386613 | 118000 | -0.06 | -0.07 | -0.05 |
| test | expanded · A · X_context · lightgbm | ablation · A · D_plus_equipment · lightgbm | 386613 | 118000 | -0.37 | -0.39 | -0.35 |
| test | expanded · A · X_all · lightgbm | ablation · A · D_plus_equipment · lightgbm | 386613 | 118000 | -0.40 | -0.43 | -0.38 |
| test | expanded · A · X_all-anyhist · lightgbm | ablation · A · D_plus_equipment · lightgbm | 386613 | 118000 | -3.79 | -3.86 | -3.73 |
| test | expanded · A · X_all-anyhist · lightgbm | expanded · A · X_all · lightgbm | 386613 | 118000 | -3.39 | -3.44 | -3.33 |
| test | ensemble · A · X_all-anyhist · lgbm_mlp | expanded · A · X_all-anyhist · lightgbm | 386613 | 118000 | -0.09 | -0.10 | -0.09 |

## expanded_sbd_first_timers — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| ablation · A · A_squat · ratio | ratio | A_squat | 118324 | 118000 | 21.31 | 21.21 | 21.41 | 21.30 | 12.92 | 0.76 |
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 118324 | 118000 | 13.80 | 13.73 | 13.86 | 13.79 | 8.77 | 0.90 |
| expanded · A · X_all · lightgbm | lightgbm | X_all | 118324 | 118000 | 13.35 | 13.28 | 13.41 | 13.34 | 8.48 | 0.90 |
| expanded · A · X_all-anyhist · lightgbm | lightgbm | X_all+anyhist | 118324 | 118000 | 13.07 | 13.01 | 13.14 | 13.07 | 8.24 | 0.91 |
| expanded · A · X_all-anyhist · mlp · s42 | mlp | X_all+anyhist | 118324 | 118000 | 13.13 | 13.07 | 13.20 | 13.13 | 8.29 | 0.90 |
| ensemble · A · X_all-anyhist · lgbm_mlp | ensemble | X_all+anyhist | 118324 | 118000 | 13.04 | 12.98 | 13.10 | 13.04 | 8.23 | 0.91 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | expanded · A · X_all · lightgbm | ablation · A · D_plus_equipment · lightgbm | 118324 | 118000 | -0.45 | -0.47 | -0.42 |
| test | expanded · A · X_all-anyhist · lightgbm | ablation · A · D_plus_equipment · lightgbm | 118324 | 118000 | -0.72 | -0.75 | -0.69 |
| test | ensemble · A · X_all-anyhist · lgbm_mlp | ablation · A · D_plus_equipment · lightgbm | 118324 | 118000 | -0.76 | -0.79 | -0.73 |

## expanded_first_timers_with_other_event_deadlift — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| ablation · A · A_squat · ratio | ratio | A_squat | 4400 | 4387 | 27.01 | 26.47 | 27.68 | 27.00 | 15.28 | 0.67 |
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 4400 | 4387 | 15.35 | 15.01 | 15.78 | 15.36 | 8.80 | 0.88 |
| expanded · A · X_all · lightgbm | lightgbm | X_all | 4400 | 4387 | 15.09 | 14.74 | 15.51 | 15.10 | 8.63 | 0.88 |
| expanded · A · X_all-anyhist · lightgbm | lightgbm | X_all+anyhist | 4400 | 4387 | 10.60 | 10.26 | 10.89 | 10.61 | 6.29 | 0.93 |
| expanded · A · X_all-anyhist · mlp · s42 | mlp | X_all+anyhist | 4400 | 4387 | 10.48 | 10.15 | 10.85 | 10.49 | 6.30 | 0.93 |
| ensemble · A · X_all-anyhist · lgbm_mlp | ensemble | X_all+anyhist | 4400 | 4387 | 10.39 | 10.05 | 10.71 | 10.39 | 6.20 | 0.94 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | expanded · A · X_all · lightgbm | ablation · A · D_plus_equipment · lightgbm | 4400 | 4387 | -0.26 | -0.43 | -0.12 |
| test | expanded · A · X_all-anyhist · lightgbm | ablation · A · D_plus_equipment · lightgbm | 4400 | 4387 | -4.75 | -5.06 | -4.44 |
| test | ensemble · A · X_all-anyhist · lgbm_mlp | ablation · A · D_plus_equipment · lightgbm | 4400 | 4387 | -4.97 | -5.29 | -4.64 |

## expanded_history_eligible — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| history · A · D_plus_equipment · last_deadlift · histrows | last_deadlift | D_plus_equipment | 268289 | 64764 | 13.44 | 13.33 | 13.56 | 14.08 | 7.95 | 0.86 |
| history_rich · A · D_plus_equipment-history_rich · lightgbm · histrows | lightgbm | D_plus_equipment+history_rich | 268289 | 64764 | 8.41 | 8.37 | 8.47 | 8.64 | 4.97 | 0.96 |
| history_rich · A · D_plus_equipment-history_rich · mlp · histrows · s42 | mlp | D_plus_equipment+history_rich | 268289 | 64764 | 8.38 | 8.34 | 8.44 | 8.63 | 4.95 | 0.96 |
| ensemble · A · D_plus_equipment-history_rich · lgbm_mlp · histrows | ensemble | D_plus_equipment+history_rich | 268289 | 64764 | 8.32 | 8.28 | 8.38 | 8.57 | 4.92 | 0.96 |
| expanded · A · X_all-history_rich-anyhist · lightgbm · histrows | lightgbm | X_all+history_rich+anyhist | 268289 | 64764 | 8.36 | 8.32 | 8.42 | 8.57 | 4.93 | 0.96 |
| expanded · A · X_all-history_rich-anyhist · mlp · histrows · s42 | mlp | X_all+history_rich+anyhist | 268289 | 64764 | 8.33 | 8.29 | 8.39 | 8.56 | 4.93 | 0.96 |
| ensemble · A · X_all-history_rich-anyhist · lgbm_mlp · histrows | ensemble | X_all+history_rich+anyhist | 268289 | 64764 | 8.25 | 8.21 | 8.30 | 8.47 | 4.88 | 0.96 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | expanded · A · X_all-history_rich-anyhist · lightgbm · histrows | history_rich · A · D_plus_equipment-history_rich · lightgbm · histrows | 268289 | 64764 | -0.04 | -0.06 | -0.03 |
| test | expanded · A · X_all-history_rich-anyhist · mlp · histrows · s42 | history_rich · A · D_plus_equipment-history_rich · mlp · histrows · s42 | 268289 | 64764 | -0.05 | -0.06 | -0.04 |
| test | ensemble · A · X_all-history_rich-anyhist · lgbm_mlp · histrows | ensemble · A · D_plus_equipment-history_rich · lgbm_mlp · histrows | 268289 | 64764 | -0.07 | -0.08 | -0.06 |
| test | ensemble · A · X_all-history_rich-anyhist · lgbm_mlp · histrows | history · A · D_plus_equipment · last_deadlift · histrows | 268289 | 64764 | -5.19 | -5.27 | -5.10 |

## expanded_chrono_all — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| chrono · B · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 402128 | 183630 | 14.04 | 13.99 | 14.10 | 14.42 | 8.57 | 0.90 |
| expanded · B · X_all-anyhist · lightgbm | lightgbm | X_all+anyhist | 402128 | 183630 | 9.89 | 9.85 | 9.93 | 11.13 | 6.23 | 0.94 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | expanded · B · X_all-anyhist · lightgbm | chrono · B · D_plus_equipment · lightgbm | 402128 | 183630 | -4.16 | -4.20 | -4.11 |

## expanded_chrono_history_eligible — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| chrono · B · D_plus_equipment · last_deadlift · histrows | last_deadlift | D_plus_equipment | 301269 | 125023 | 12.54 | 12.46 | 12.63 | 13.87 | 7.67 | 0.88 |
| history_rich · B · D_plus_equipment-history_rich · lightgbm · histrows | lightgbm | D_plus_equipment+history_rich | 301269 | 125023 | 8.17 | 8.12 | 8.21 | 8.75 | 5.05 | 0.96 |
| expanded · B · X_all-history_rich-anyhist · lightgbm · histrows | lightgbm | X_all+history_rich+anyhist | 301269 | 125023 | 8.11 | 8.07 | 8.15 | 8.68 | 5.00 | 0.96 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | expanded · B · X_all-history_rich-anyhist · lightgbm · histrows | history_rich · B · D_plus_equipment-history_rich · lightgbm · histrows | 301269 | 125023 | -0.06 | -0.07 | -0.05 |
| test | expanded · B · X_all-history_rich-anyhist · lightgbm · histrows | chrono · B · D_plus_equipment · last_deadlift · histrows | 301269 | 125023 | -4.43 | -4.50 | -4.37 |

## objective|X_all+anyhist — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| expanded · A · X_all-anyhist · lightgbm | lightgbm | X_all+anyhist | 386613 | 118000 | 10.29 | 10.24 | 10.34 | 11.71 | 6.21 | 0.94 |
| objective · A · X_all-anyhist · lightgbm · l1_kg | lightgbm | X_all+anyhist | 386613 | 118000 | 10.24 | 10.20 | 10.30 | 11.69 | 6.18 | 0.94 |
| objective · A · X_all-anyhist · lightgbm · huber_kg | lightgbm | X_all+anyhist | 386613 | 118000 | 10.20 | 10.15 | 10.25 | 11.65 | 6.16 | 0.94 |
| objective · A · X_all-anyhist · lightgbm · l2_ratio | lightgbm | X_all+anyhist | 386613 | 118000 | 10.31 | 10.26 | 10.36 | 11.71 | 6.22 | 0.94 |
| objective · A · X_all-anyhist · lightgbm · l1_ratio | lightgbm | X_all+anyhist | 386613 | 118000 | 10.28 | 10.24 | 10.34 | 11.71 | 6.18 | 0.94 |
| ensemble · A · X_all-anyhist · lgbm_mlp | ensemble | X_all+anyhist | 386613 | 118000 | 10.19 | 10.14 | 10.24 | 11.65 | 6.18 | 0.94 |
| ensemble · A · X_all-anyhist · bestobj_mlp | ensemble | X_all+anyhist | 386613 | 118000 | 10.16 | 10.11 | 10.21 | 11.62 | 6.15 | 0.94 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | objective · A · X_all-anyhist · lightgbm · l1_kg | expanded · A · X_all-anyhist · lightgbm | 386613 | 118000 | -0.04 | -0.05 | -0.03 |
| test | objective · A · X_all-anyhist · lightgbm · huber_kg | expanded · A · X_all-anyhist · lightgbm | 386613 | 118000 | -0.09 | -0.10 | -0.08 |
| test | objective · A · X_all-anyhist · lightgbm · l2_ratio | expanded · A · X_all-anyhist · lightgbm | 386613 | 118000 | 0.02 | 0.01 | 0.03 |
| test | objective · A · X_all-anyhist · lightgbm · l1_ratio | expanded · A · X_all-anyhist · lightgbm | 386613 | 118000 | -0.00 | -0.02 | 0.01 |
| test | ensemble · A · X_all-anyhist · bestobj_mlp | ensemble · A · X_all-anyhist · lgbm_mlp | 386613 | 118000 | -0.03 | -0.04 | -0.02 |

## objective|X_all+history_rich+anyhist — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| expanded · A · X_all-history_rich-anyhist · lightgbm · histrows | lightgbm | X_all+history_rich+anyhist | 268289 | 64764 | 8.36 | 8.32 | 8.42 | 8.57 | 4.93 | 0.96 |
| objective · A · X_all-history_rich-anyhist · lightgbm · histrows · l1_kg | lightgbm | X_all+history_rich+anyhist | 268289 | 64764 | 8.32 | 8.28 | 8.37 | 8.55 | 4.92 | 0.96 |
| objective · A · X_all-history_rich-anyhist · lightgbm · histrows · huber_kg | lightgbm | X_all+history_rich+anyhist | 268289 | 64764 | 8.25 | 8.21 | 8.30 | 8.49 | 4.88 | 0.96 |
| objective · A · X_all-history_rich-anyhist · lightgbm · histrows · l2_ratio | lightgbm | X_all+history_rich+anyhist | 268289 | 64764 | 8.47 | 8.42 | 8.52 | 8.65 | 4.99 | 0.96 |
| objective · A · X_all-history_rich-anyhist · lightgbm · histrows · l1_ratio | lightgbm | X_all+history_rich+anyhist | 268289 | 64764 | 8.40 | 8.36 | 8.46 | 8.62 | 4.93 | 0.96 |
| ensemble · A · X_all-history_rich-anyhist · lgbm_mlp · histrows | ensemble | X_all+history_rich+anyhist | 268289 | 64764 | 8.25 | 8.21 | 8.30 | 8.47 | 4.88 | 0.96 |
| ensemble · A · X_all-history_rich-anyhist · bestobj_mlp · histrows | ensemble | X_all+history_rich+anyhist | 268289 | 64764 | 8.21 | 8.17 | 8.26 | 8.45 | 4.86 | 0.96 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | objective · A · X_all-history_rich-anyhist · lightgbm · histrows · l1_kg | expanded · A · X_all-history_rich-anyhist · lightgbm · histrows | 268289 | 64764 | -0.04 | -0.06 | -0.03 |
| test | objective · A · X_all-history_rich-anyhist · lightgbm · histrows · huber_kg | expanded · A · X_all-history_rich-anyhist · lightgbm · histrows | 268289 | 64764 | -0.11 | -0.12 | -0.10 |
| test | objective · A · X_all-history_rich-anyhist · lightgbm · histrows · l2_ratio | expanded · A · X_all-history_rich-anyhist · lightgbm · histrows | 268289 | 64764 | 0.10 | 0.09 | 0.12 |
| test | objective · A · X_all-history_rich-anyhist · lightgbm · histrows · l1_ratio | expanded · A · X_all-history_rich-anyhist · lightgbm · histrows | 268289 | 64764 | 0.04 | 0.02 | 0.06 |
| test | ensemble · A · X_all-history_rich-anyhist · bestobj_mlp · histrows | ensemble · A · X_all-history_rich-anyhist · lgbm_mlp · histrows | 268289 | 64764 | -0.04 | -0.04 | -0.03 |

## routed_all_lifters — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| routed · A · original_specialists | routed | routed | 386613 | 118000 | 10.00 | 9.95 | 10.04 | 11.92 | 6.10 | 0.94 |
| routed · A · expanded_specialists | routed | routed | 386613 | 118000 | 9.71 | 9.67 | 9.76 | 11.40 | 5.90 | 0.94 |
| routed · A · objective_specialists | routed | routed | 386613 | 118000 | 9.68 | 9.64 | 9.73 | 11.38 | 5.88 | 0.94 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | routed · A · expanded_specialists | routed · A · original_specialists | 386613 | 118000 | -0.28 | -0.29 | -0.27 |
| test | routed · A · objective_specialists | routed · A · expanded_specialists | 386613 | 118000 | -0.03 | -0.04 | -0.03 |
| test | routed · A · objective_specialists | routed · A · original_specialists | 386613 | 118000 | -0.31 | -0.32 | -0.30 |

## routed_first_timers — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| routed · A · original_specialists | routed | routed | 118324 | 118000 | 13.80 | 13.73 | 13.86 | 13.79 | 8.77 | 0.90 |
| routed · A · expanded_specialists | routed | routed | 118324 | 118000 | 13.04 | 12.98 | 13.10 | 13.04 | 8.23 | 0.91 |
| routed · A · objective_specialists | routed | routed | 118324 | 118000 | 13.03 | 12.96 | 13.09 | 13.02 | 8.20 | 0.91 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | routed · A · objective_specialists | routed · A · original_specialists | 118324 | 118000 | -0.77 | -0.80 | -0.74 |

## routed_returning — partition `test`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| routed · A · original_specialists | routed | routed | 268289 | 64764 | 8.32 | 8.28 | 8.38 | 8.57 | 4.92 | 0.96 |
| routed · A · expanded_specialists | routed | routed | 268289 | 64764 | 8.25 | 8.21 | 8.30 | 8.47 | 4.88 | 0.96 |
| routed · A · objective_specialists | routed | routed | 268289 | 64764 | 8.21 | 8.17 | 8.26 | 8.45 | 4.86 | 0.96 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| test | routed · A · objective_specialists | routed · A · original_specialists | 268289 | 64764 | -0.11 | -0.12 | -0.10 |

## Subgroups (protocol A, feature set D; protocol B LightGBM)

| run_id | group_by | group | rows | lifters | mae | mape | r2 | sparse |
|---|---|---|---|---|---|---|---|---|
| ablation · A · A_squat · ratio | Sex | F | 119451 | 34376 | 16.30 | 13.25 | 0.55 | False |
| ablation · A · A_squat · ratio | Sex | M | 267148 | 83814 | 24.42 | 11.94 | 0.62 | False |
| ablation · A · A_squat · ratio | Sex | Mx | 14 | 11 | 21.25 | 13.50 | 0.57 | True |
| ablation · A · A_squat · ratio | bw_bin | 0-60 | 64134 | 20857 | 15.43 | 12.94 | 0.66 | False |
| ablation · A · A_squat · ratio | bw_bin | 105-120 | 34447 | 13919 | 26.96 | 12.57 | 0.58 | False |
| ablation · A · A_squat · ratio | bw_bin | 120-1000 | 25559 | 8480 | 34.54 | 15.34 | 0.38 | False |
| ablation · A · A_squat · ratio | bw_bin | 60-75 | 97685 | 37810 | 19.22 | 12.09 | 0.70 | False |
| ablation · A · A_squat · ratio | bw_bin | 75-90 | 94517 | 38349 | 22.01 | 11.84 | 0.69 | False |
| ablation · A · A_squat · ratio | bw_bin | 90-105 | 68288 | 27598 | 24.15 | 11.54 | 0.64 | False |
| ablation · A · A_squat · ratio | bw_bin | missing | 1983 | 1247 | 31.69 | 14.73 | 0.59 | False |
| ablation · A · A_squat · ratio | has_history | False | 118324 | 118000 | 21.31 | 12.92 | 0.76 | False |
| ablation · A · A_squat · ratio | has_history | True | 268289 | 64764 | 22.18 | 12.09 | 0.76 | False |
| ablation · A · A_squat · ratio | Equipment | Multi-ply | 7369 | 3006 | 50.10 | 21.70 | -0.16 | False |
| ablation · A · A_squat · ratio | Equipment | Raw | 160249 | 62892 | 22.59 | 12.48 | 0.77 | False |
| ablation · A · A_squat · ratio | Equipment | Single-ply | 147373 | 44780 | 20.46 | 11.60 | 0.79 | False |
| ablation · A · A_squat · ratio | Equipment | Unlimited | 40208 | 9449 | 18.46 | 12.79 | 0.70 | False |
| ablation · A · A_squat · ratio | Equipment | Wraps | 31414 | 15236 | 23.09 | 12.35 | 0.75 | False |
| ablation · A · D_plus_equipment · linear | Sex | F | 119451 | 34376 | 11.32 | 9.71 | 0.78 | False |
| ablation · A · D_plus_equipment · linear | Sex | M | 267148 | 83814 | 17.29 | 8.97 | 0.80 | False |
| ablation · A · D_plus_equipment · linear | Sex | Mx | 14 | 11 | 18.68 | 14.02 | 0.73 | True |
| ablation · A · D_plus_equipment · linear | bw_bin | 0-60 | 64134 | 20857 | 12.09 | 11.16 | 0.79 | False |
| ablation · A · D_plus_equipment · linear | bw_bin | 105-120 | 34447 | 13919 | 18.72 | 8.92 | 0.80 | False |
| ablation · A · D_plus_equipment · linear | bw_bin | 120-1000 | 25559 | 8480 | 22.36 | 10.43 | 0.74 | False |
| ablation · A · D_plus_equipment · linear | bw_bin | 60-75 | 97685 | 37810 | 13.20 | 8.74 | 0.85 | False |
| ablation · A · D_plus_equipment · linear | bw_bin | 75-90 | 94517 | 38349 | 15.36 | 8.52 | 0.84 | False |
| ablation · A · D_plus_equipment · linear | bw_bin | 90-105 | 68288 | 27598 | 17.51 | 8.56 | 0.81 | False |
| ablation · A · D_plus_equipment · linear | bw_bin | missing | 1983 | 1247 | 21.63 | 11.43 | 0.82 | False |
| ablation · A · D_plus_equipment · linear | has_history | False | 118324 | 118000 | 15.16 | 9.95 | 0.88 | False |
| ablation · A · D_plus_equipment · linear | has_history | True | 268289 | 64764 | 15.57 | 8.87 | 0.88 | False |
| ablation · A · D_plus_equipment · linear | Equipment | Multi-ply | 7369 | 3006 | 27.51 | 12.88 | 0.63 | False |
| ablation · A · D_plus_equipment · linear | Equipment | Raw | 160249 | 62892 | 15.32 | 9.13 | 0.88 | False |
| ablation · A · D_plus_equipment · linear | Equipment | Single-ply | 147373 | 44780 | 15.50 | 9.11 | 0.88 | False |
| ablation · A · D_plus_equipment · linear | Equipment | Unlimited | 40208 | 9449 | 12.66 | 9.00 | 0.87 | False |
| ablation · A · D_plus_equipment · linear | Equipment | Wraps | 31414 | 15236 | 16.57 | 9.36 | 0.87 | False |
| ablation · A · D_plus_equipment · lightgbm | Sex | F | 119451 | 34376 | 10.38 | 8.79 | 0.82 | False |
| ablation · A · D_plus_equipment · lightgbm | Sex | M | 267148 | 83814 | 15.73 | 8.03 | 0.84 | False |
| ablation · A · D_plus_equipment · lightgbm | Sex | Mx | 14 | 11 | 15.83 | 11.73 | 0.79 | True |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | 0-60 | 64134 | 20857 | 10.19 | 8.87 | 0.85 | False |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | 105-120 | 34447 | 13919 | 17.06 | 8.18 | 0.83 | False |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | 120-1000 | 25559 | 8480 | 19.07 | 8.91 | 0.81 | False |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | 60-75 | 97685 | 37810 | 12.36 | 8.06 | 0.87 | False |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | 75-90 | 94517 | 38349 | 14.39 | 8.06 | 0.86 | False |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | 90-105 | 68288 | 27598 | 16.23 | 8.06 | 0.83 | False |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | missing | 1983 | 1247 | 19.46 | 9.74 | 0.85 | False |
| ablation · A · D_plus_equipment · lightgbm | has_history | False | 118324 | 118000 | 13.80 | 8.77 | 0.90 | False |
| ablation · A · D_plus_equipment · lightgbm | has_history | True | 268289 | 64764 | 14.20 | 8.05 | 0.90 | False |
| ablation · A · D_plus_equipment · lightgbm | Equipment | Multi-ply | 7369 | 3006 | 20.43 | 9.94 | 0.79 | False |
| ablation · A · D_plus_equipment · lightgbm | Equipment | Raw | 160249 | 62892 | 14.25 | 8.12 | 0.90 | False |
| ablation · A · D_plus_equipment · lightgbm | Equipment | Single-ply | 147373 | 44780 | 13.93 | 8.21 | 0.90 | False |
| ablation · A · D_plus_equipment · lightgbm | Equipment | Unlimited | 40208 | 9449 | 11.36 | 8.28 | 0.90 | False |
| ablation · A · D_plus_equipment · lightgbm | Equipment | Wraps | 31414 | 15236 | 15.88 | 8.88 | 0.88 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Sex | F | 119451 | 34376 | 10.46 | 8.84 | 0.81 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Sex | M | 267148 | 83814 | 16.02 | 8.12 | 0.83 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Sex | Mx | 14 | 11 | 18.55 | 13.03 | 0.72 | True |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | 0-60 | 64134 | 20857 | 10.32 | 8.97 | 0.84 | False |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | 105-120 | 34447 | 13919 | 17.40 | 8.27 | 0.82 | False |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | 120-1000 | 25559 | 8480 | 19.43 | 8.99 | 0.81 | False |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | 60-75 | 97685 | 37810 | 12.52 | 8.13 | 0.87 | False |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | 75-90 | 94517 | 38349 | 14.61 | 8.13 | 0.85 | False |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | 90-105 | 68288 | 27598 | 16.52 | 8.11 | 0.83 | False |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | missing | 1983 | 1247 | 19.21 | 9.60 | 0.85 | False |
| ablation · A · D_plus_equipment · mlp · s42 | has_history | False | 118324 | 118000 | 14.00 | 8.84 | 0.89 | False |
| ablation · A · D_plus_equipment · mlp · s42 | has_history | True | 268289 | 64764 | 14.43 | 8.12 | 0.90 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Equipment | Multi-ply | 7369 | 3006 | 20.51 | 9.94 | 0.78 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Equipment | Raw | 160249 | 62892 | 14.27 | 8.10 | 0.90 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Equipment | Single-ply | 147373 | 44780 | 14.50 | 8.45 | 0.89 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Equipment | Unlimited | 40208 | 9449 | 11.36 | 8.26 | 0.90 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Equipment | Wraps | 31414 | 15236 | 15.82 | 8.80 | 0.88 | False |
| chrono · B · D_plus_equipment · lightgbm | Sex | F | 153262 | 62699 | 10.48 | 8.81 | 0.83 | False |
| chrono · B · D_plus_equipment · lightgbm | Sex | M | 248786 | 120888 | 16.24 | 8.41 | 0.83 | False |
| chrono · B · D_plus_equipment · lightgbm | Sex | Mx | 80 | 57 | 12.57 | 8.97 | 0.78 | True |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | 0-60 | 67024 | 27418 | 10.08 | 8.95 | 0.86 | False |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | 105-120 | 34213 | 18544 | 17.34 | 8.78 | 0.85 | False |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | 120-1000 | 24968 | 11812 | 18.88 | 9.41 | 0.82 | False |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | 60-75 | 107545 | 54595 | 12.47 | 8.34 | 0.88 | False |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | 75-90 | 99287 | 53775 | 14.56 | 8.44 | 0.87 | False |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | 90-105 | 68960 | 37945 | 16.22 | 8.29 | 0.86 | False |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | missing | 131 | 124 | 15.09 | 17.64 | 0.93 | False |
| chrono · B · D_plus_equipment · lightgbm | has_history | False | 100859 | 100696 | 13.85 | 9.28 | 0.89 | False |
| chrono · B · D_plus_equipment · lightgbm | has_history | True | 301269 | 125023 | 14.11 | 8.33 | 0.90 | False |
| chrono · B · D_plus_equipment · lightgbm | Equipment | Multi-ply | 1229 | 747 | 22.94 | 10.96 | 0.73 | False |
| chrono · B · D_plus_equipment · lightgbm | Equipment | Raw | 251065 | 136852 | 14.55 | 8.32 | 0.90 | False |
| chrono · B · D_plus_equipment · lightgbm | Equipment | Single-ply | 13674 | 8396 | 16.66 | 9.43 | 0.85 | False |
| chrono · B · D_plus_equipment · lightgbm | Equipment | Unlimited | 115589 | 34671 | 12.21 | 8.86 | 0.88 | False |
| chrono · B · D_plus_equipment · lightgbm | Equipment | Wraps | 20571 | 13523 | 15.88 | 9.18 | 0.88 | False |

## Transfer covariate differences

| group | partition | rows | lifters | share_female | share_raw | mean_squat | mean_bench | mean_bodyweight | age_missing | mean_deadlift |
|---|---|---|---|---|---|---|---|---|---|---|
| Equipment=Single-ply | test_in_dist | 239240 | 82600 | 0.35 | 0.67 | 168.02 | 106.54 | 83.36 | 0.29 | 187.32 |
| Equipment=Single-ply | test_transfer | 147373 | 44780 | 0.25 | 0.00 | 176.56 | 109.21 | 81.43 | 0.66 | 182.38 |
| Equipment=Single-ply | val | 241225 | 83034 | 0.35 | 0.67 | 167.71 | 106.27 | 83.17 | 0.29 | 187.29 |
| Equipment=Unlimited | test_in_dist | 346405 | 111120 | 0.28 | 0.46 | 174.38 | 109.97 | 83.13 | 0.37 | 190.22 |
| Equipment=Unlimited | test_transfer | 40208 | 9449 | 0.52 | 0.00 | 144.48 | 86.80 | 78.36 | 0.94 | 144.23 |
| Equipment=Unlimited | val | 350255 | 111372 | 0.29 | 0.46 | 174.26 | 109.89 | 82.92 | 0.37 | 190.23 |
| Equipment=Wraps | test_in_dist | 355199 | 109462 | 0.31 | 0.45 | 169.44 | 106.34 | 82.02 | 0.45 | 183.32 |
| Equipment=Wraps | test_transfer | 31414 | 15236 | 0.25 | 0.00 | 192.02 | 121.28 | 89.56 | 0.17 | 209.43 |
| Equipment=Wraps | val | 359626 | 109844 | 0.31 | 0.45 | 169.59 | 106.41 | 81.88 | 0.45 | 183.55 |
| Equipment=Multi-ply | test_in_dist | 379244 | 116572 | 0.31 | 0.42 | 169.54 | 106.33 | 82.39 | 0.43 | 184.48 |
| Equipment=Multi-ply | test_transfer | 7369 | 3006 | 0.13 | 0.00 | 260.53 | 170.72 | 95.31 | 0.27 | 234.74 |
| Equipment=Multi-ply | val | 383325 | 116932 | 0.31 | 0.42 | 169.51 | 106.32 | 82.27 | 0.43 | 184.56 |
| Federation=THSPA | test_in_dist | 317136 | 102851 | 0.38 | 0.50 | 170.88 | 107.96 | 81.93 | 0.32 | 187.75 |
| Federation=THSPA | test_transfer | 69477 | 16983 | 0.00 | 0.01 | 173.08 | 105.72 | 85.79 | 0.94 | 174.92 |
| Federation=THSPA | val | 321327 | 103194 | 0.38 | 0.50 | 170.71 | 107.86 | 81.74 | 0.32 | 187.66 |
| Federation=USAPL | test_in_dist | 343607 | 105792 | 0.31 | 0.37 | 171.72 | 107.69 | 82.65 | 0.47 | 184.90 |
| Federation=USAPL | test_transfer | 43006 | 17917 | 0.34 | 0.80 | 167.72 | 106.45 | 82.47 | 0.07 | 189.78 |
| Federation=USAPL | val | 347247 | 106099 | 0.31 | 0.37 | 171.77 | 107.69 | 82.52 | 0.47 | 185.05 |
| Federation=THSWPA | test_in_dist | 344287 | 110287 | 0.22 | 0.46 | 179.03 | 113.92 | 84.25 | 0.37 | 194.57 |
| Federation=THSWPA | test_transfer | 42326 | 8254 | 1.00 | 0.02 | 108.22 | 55.80 | 69.52 | 0.94 | 111.14 |
| Federation=THSWPA | val | 347919 | 110504 | 0.23 | 0.46 | 178.95 | 113.85 | 84.04 | 0.37 | 194.67 |

## Runs

| run_id | experiment | protocol | feature_set | model | seed | train_rows | train_lifters | val_rows | fit_seconds | val_mae |
|---|---|---|---|---|---|---|---|---|---|---|
| ablation__A__A_squat__lightgbm | ablation | A | A_squat | lightgbm | 42 | 1817276 | 551698 | 390871 | 63.32 | 17.13 |
| ablation__A__A_squat__linear | ablation | A | A_squat | linear | 42 | 1817276 | 551698 | 390871 | 1.67 | 19.55 |
| ablation__A__A_squat__mlp__s42 | ablation | A | A_squat | mlp | 42 | 1817276 | 551698 | 390871 | 22.80 | 18.65 |
| ablation__A__A_squat__ratio | ablation | A | A_squat | ratio | 42 | 1817276 | 551698 | 390871 | 0.73 | 21.98 |
| ablation__A__B_squat_bench__lightgbm | ablation | A | B_squat_bench | lightgbm | 42 | 1817276 | 551698 | 390871 | 55.13 | 15.84 |
| ablation__A__B_squat_bench__linear | ablation | A | B_squat_bench | linear | 42 | 1817276 | 551698 | 390871 | 0.79 | 18.24 |
| ablation__A__B_squat_bench__mlp__s42 | ablation | A | B_squat_bench | mlp | 42 | 1817276 | 551698 | 390871 | 29.58 | 17.08 |
| ablation__A__C_plus_demographics__lightgbm | ablation | A | C_plus_demographics | lightgbm | 42 | 1817276 | 551698 | 390871 | 101.70 | 14.69 |
| ablation__A__C_plus_demographics__linear | ablation | A | C_plus_demographics | linear | 42 | 1817276 | 551698 | 390871 | 1.94 | 16.85 |
| ablation__A__C_plus_demographics__mlp__s42 | ablation | A | C_plus_demographics | mlp | 42 | 1817276 | 551698 | 390871 | 36.72 | 15.35 |
| ablation__A__D_plus_equipment__lightgbm | ablation | A | D_plus_equipment | lightgbm | 42 | 1817276 | 551698 | 390871 | 56.17 | 14.10 |
| ablation__A__D_plus_equipment__linear | ablation | A | D_plus_equipment | linear | 42 | 1817276 | 551698 | 390871 | 3.75 | 15.46 |
| ablation__A__D_plus_equipment__mlp__s42 | ablation | A | D_plus_equipment | mlp | 42 | 1817276 | 551698 | 390871 | 42.10 | 14.32 |
| ablation__A__D_plus_equipment__mlp__s43 | ablation | A | D_plus_equipment | mlp | 43 | 1817276 | 551698 | 390871 | 34.10 | 14.32 |
| ablation__A__D_plus_equipment__mlp__s44 | ablation | A | D_plus_equipment | mlp | 44 | 1817276 | 551698 | 390871 | 36.07 | 14.33 |
| ablation__A__E_plus_federation__lightgbm | ablation | A | E_plus_federation | lightgbm | 42 | 1817276 | 551698 | 390871 | 39.69 | 13.87 |
| ablation__A__E_plus_federation__linear | ablation | A | E_plus_federation | linear | 42 | 1817276 | 551698 | 390871 | 217.67 | 14.92 |
| ablation__A__E_plus_federation__mlp__s42 | ablation | A | E_plus_federation | mlp | 42 | 1817276 | 551698 | 390871 | 58.08 | 13.88 |
| capacity__A__D_plus_equipment-history__lightgbm__histrows__lgbm_big | capacity | A | D_plus_equipment+history | lightgbm | 42 | 1264025 | 301327 | 272140 | 66.90 | 8.75 |
| capacity__A__D_plus_equipment-history__mlp__histrows__mlp_deep__s42 | capacity | A | D_plus_equipment+history | mlp | 42 | 1264025 | 301327 | 272140 | 269.57 | 8.74 |
| capacity__A__D_plus_equipment-history__mlp__histrows__mlp_wide__s42 | capacity | A | D_plus_equipment+history | mlp | 42 | 1264025 | 301327 | 272140 | 68.22 | 8.74 |
| capacity__A__D_plus_equipment__lightgbm__lgbm_big | capacity | A | D_plus_equipment | lightgbm | 42 | 1817276 | 551698 | 390871 | 58.63 | 14.10 |
| capacity__A__D_plus_equipment__mlp__mlp_deep__s42 | capacity | A | D_plus_equipment | mlp | 42 | 1817276 | 551698 | 390871 | 147.81 | 14.31 |
| capacity__A__D_plus_equipment__mlp__mlp_wide__s42 | capacity | A | D_plus_equipment | mlp | 42 | 1817276 | 551698 | 390871 | 45.35 | 14.34 |
| chrono__B__A_squat__ratio | chrono | B | A_squat | ratio | 42 | 1800694 | 575145 | 391938 | 0.37 | 21.25 |
| chrono__B__D_plus_equipment-history__lightgbm__histrows | chrono | B | D_plus_equipment+history | lightgbm | 42 | 1223622 | 301072 | 279563 | 70.74 | 8.29 |
| chrono__B__D_plus_equipment__last_deadlift__histrows | chrono | B | D_plus_equipment | last_deadlift | 42 | 1223622 | 301072 | 279563 | 0.25 | 12.60 |
| chrono__B__D_plus_equipment__lightgbm | chrono | B | D_plus_equipment | lightgbm | 42 | 1800694 | 575145 | 391938 | 16.05 | 13.61 |
| chrono__B__D_plus_equipment__lightgbm__histrows | chrono | B | D_plus_equipment | lightgbm | 42 | 1223622 | 301072 | 279563 | 10.70 | 13.65 |
| chrono__B__D_plus_equipment__linear | chrono | B | D_plus_equipment | linear | 42 | 1800694 | 575145 | 391938 | 3.46 | 14.60 |
| chrono__B__D_plus_equipment__mlp__s42 | chrono | B | D_plus_equipment | mlp | 42 | 1800694 | 575145 | 391938 | 17.43 | 13.60 |
| ensemble__A__D_plus_equipment-history_rich__lgbm_mlp__histrows | ensemble | A | D_plus_equipment+history_rich | ensemble | 42 | 1264025 | 301327 | 272140 | 0.95 | 8.37 |
| ensemble__A__D_plus_equipment__lgbm_mlp | ensemble | A | D_plus_equipment | ensemble | 42 | 1817276 | 551698 | 390871 | 1.56 | 14.10 |
| ensemble__A__X_all-anyhist__bestobj_mlp | ensemble | A | X_all+anyhist | ensemble | 42 | 1817276 | 551698 | 390871 | 0.00 | 10.20 |
| ensemble__A__X_all-anyhist__lgbm_mlp | ensemble | A | X_all+anyhist | ensemble | 42 | 1817276 | 551698 | 390871 | 1.39 | 10.23 |
| ensemble__A__X_all-history_rich-anyhist__bestobj_mlp__histrows | ensemble | A | X_all+history_rich+anyhist | ensemble | 42 | 1264025 | 301327 | 272140 | 0.00 | 8.26 |
| ensemble__A__X_all-history_rich-anyhist__lgbm_mlp__histrows | ensemble | A | X_all+history_rich+anyhist | ensemble | 42 | 1264025 | 301327 | 272140 | 0.87 | 8.30 |
| ensemble__B__D_plus_equipment__lgbm_mlp | ensemble | B | D_plus_equipment | ensemble | 42 | 1800694 | 575145 | 391938 | 1.30 | 13.55 |
| expanded__A__X_all-anyhist__lightgbm | expanded | A | X_all+anyhist | lightgbm | 42 | 1817276 | 551698 | 390871 | 162.87 | 10.32 |
| expanded__A__X_all-anyhist__mlp__s42 | expanded | A | X_all+anyhist | mlp | 42 | 1817276 | 551698 | 390871 | 150.84 | 10.33 |
| expanded__A__X_all-history_rich-anyhist__lightgbm__histrows | expanded | A | X_all+history_rich+anyhist | lightgbm | 42 | 1264025 | 301327 | 272140 | 122.41 | 8.41 |
| expanded__A__X_all-history_rich-anyhist__mlp__histrows__s42 | expanded | A | X_all+history_rich+anyhist | mlp | 42 | 1264025 | 301327 | 272140 | 82.43 | 8.38 |
| expanded__A__X_all__lightgbm | expanded | A | X_all | lightgbm | 42 | 1817276 | 551698 | 390871 | 79.74 | 13.70 |
| expanded__A__X_all__mlp__s42 | expanded | A | X_all | mlp | 42 | 1817276 | 551698 | 390871 | 107.78 | 13.75 |
| expanded__A__X_attempts__lightgbm | expanded | A | X_attempts | lightgbm | 42 | 1817276 | 551698 | 390871 | 76.35 | 14.05 |
| expanded__A__X_attempts__mlp__s42 | expanded | A | X_attempts | mlp | 42 | 1817276 | 551698 | 390871 | 47.23 | 14.26 |
| expanded__A__X_context__lightgbm | expanded | A | X_context | lightgbm | 42 | 1817276 | 551698 | 390871 | 59.58 | 13.75 |
| expanded__A__X_context__mlp__s42 | expanded | A | X_context | mlp | 42 | 1817276 | 551698 | 390871 | 83.85 | 13.78 |
| expanded__B__X_all-anyhist__lightgbm | expanded | B | X_all+anyhist | lightgbm | 42 | 1800694 | 575145 | 391938 | 176.47 | 9.81 |
| expanded__B__X_all-history_rich-anyhist__lightgbm__histrows | expanded | B | X_all+history_rich+anyhist | lightgbm | 42 | 1223622 | 301072 | 279563 | 139.28 | 7.96 |
| history__A__D_plus_equipment-history__lightgbm__histrows | history | A | D_plus_equipment+history | lightgbm | 42 | 1264025 | 301327 | 272140 | 77.12 | 8.78 |
| history__A__D_plus_equipment-history__linear__histrows | history | A | D_plus_equipment+history | linear | 42 | 1264025 | 301327 | 272140 | 1.72 | 9.89 |
| history__A__D_plus_equipment-history__mlp__histrows__s42 | history | A | D_plus_equipment+history | mlp | 42 | 1264025 | 301327 | 272140 | 46.73 | 8.77 |
| history__A__D_plus_equipment__last_deadlift__histrows | history | A | D_plus_equipment | last_deadlift | 42 | 1264025 | 301327 | 272140 | 0.29 | 13.45 |
| history__A__D_plus_equipment__lightgbm__histrows | history | A | D_plus_equipment | lightgbm | 42 | 1264025 | 301327 | 272140 | 36.27 | 14.25 |
| history__A__D_plus_equipment__linear__histrows | history | A | D_plus_equipment | linear | 42 | 1264025 | 301327 | 272140 | 1.74 | 15.59 |
| history_rich__A__D_plus_equipment-history_rich__lightgbm__histrows | history_rich | A | D_plus_equipment+history_rich | lightgbm | 42 | 1264025 | 301327 | 272140 | 99.36 | 8.46 |
| history_rich__A__D_plus_equipment-history_rich__mlp__histrows__s42 | history_rich | A | D_plus_equipment+history_rich | mlp | 42 | 1264025 | 301327 | 272140 | 64.21 | 8.42 |
| history_rich__B__D_plus_equipment-history_rich__lightgbm__histrows | history_rich | B | D_plus_equipment+history_rich | lightgbm | 42 | 1223622 | 301072 | 279563 | 120.81 | 8.00 |
| objective__A__X_all-anyhist__lightgbm__huber_kg | objective | A | X_all+anyhist | lightgbm | 42 | 1817276 | 551698 | 390871 | 103.69 | 10.24 |
| objective__A__X_all-anyhist__lightgbm__l1_kg | objective | A | X_all+anyhist | lightgbm | 42 | 1817276 | 551698 | 390871 | 82.74 | 10.28 |
| objective__A__X_all-anyhist__lightgbm__l1_ratio | objective | A | X_all+anyhist | lightgbm | 42 | 1817276 | 551698 | 390871 | 388.17 | 10.32 |
| objective__A__X_all-anyhist__lightgbm__l2_ratio | objective | A | X_all+anyhist | lightgbm | 42 | 1817276 | 551698 | 390871 | 41.13 | 10.34 |
| objective__A__X_all-history_rich-anyhist__lightgbm__histrows__huber_kg | objective | A | X_all+history_rich+anyhist | lightgbm | 42 | 1264025 | 301327 | 272140 | 81.24 | 8.31 |
| objective__A__X_all-history_rich-anyhist__lightgbm__histrows__l1_kg | objective | A | X_all+history_rich+anyhist | lightgbm | 42 | 1264025 | 301327 | 272140 | 84.92 | 8.37 |
| objective__A__X_all-history_rich-anyhist__lightgbm__histrows__l1_ratio | objective | A | X_all+history_rich+anyhist | lightgbm | 42 | 1264025 | 301327 | 272140 | 512.77 | 8.46 |
| objective__A__X_all-history_rich-anyhist__lightgbm__histrows__l2_ratio | objective | A | X_all+history_rich+anyhist | lightgbm | 42 | 1264025 | 301327 | 272140 | 42.48 | 8.51 |
| quantile__A__D_plus_equipment-history_rich__lightgbm__histrows__q10 | quantile | A | D_plus_equipment+history_rich | lightgbm | 42 | 1264025 | 301327 | 272140 | 35.77 | 14.32 |
| quantile__A__D_plus_equipment-history_rich__lightgbm__histrows__q90 | quantile | A | D_plus_equipment+history_rich | lightgbm | 42 | 1264025 | 301327 | 272140 | 28.59 | 13.79 |
| quantile__A__D_plus_equipment__lightgbm__q10 | quantile | A | D_plus_equipment | lightgbm | 42 | 1817276 | 551698 | 390871 | 27.48 | 23.74 |
| quantile__A__D_plus_equipment__lightgbm__q90 | quantile | A | D_plus_equipment | lightgbm | 42 | 1817276 | 551698 | 390871 | 22.81 | 24.32 |
| routed__A__expanded_specialists | routed | A | routed | routed | 42 | 1817276 | 551698 | 390871 | 0.00 | 9.74 |
| routed__A__objective_specialists | routed | A | routed | routed | 42 | 1817276 | 551698 | 390871 | 0.00 | 9.71 |
| routed__A__original_specialists | routed | A | routed | routed | 42 | 1817276 | 551698 | 390871 | 0.00 | 10.02 |
| transfer__C-Equipment-Multi-ply__A_squat__ratio | transfer | C:Equipment=Multi-ply | A_squat | ratio | 42 | 1783370 | 545204 | 383325 | 3.69 | 21.35 |
| transfer__C-Equipment-Multi-ply__C_plus_demographics__lightgbm | transfer | C:Equipment=Multi-ply | C_plus_demographics | lightgbm | 42 | 1783370 | 545204 | 383325 | 33.23 | 14.51 |
| transfer__C-Equipment-Multi-ply__C_plus_demographics__linear | transfer | C:Equipment=Multi-ply | C_plus_demographics | linear | 42 | 1783370 | 545204 | 383325 | 4.51 | 16.48 |
| transfer__C-Equipment-Multi-ply__D_plus_equipment__lightgbm | transfer | C:Equipment=Multi-ply | D_plus_equipment | lightgbm | 42 | 1783370 | 545204 | 383325 | 18.28 | 14.00 |
| transfer__C-Equipment-Multi-ply__D_plus_equipment__linear | transfer | C:Equipment=Multi-ply | D_plus_equipment | linear | 42 | 1783370 | 545204 | 383325 | 6.22 | 15.23 |
| transfer__C-Equipment-Multi-ply__D_plus_equipment__mlp__s42 | transfer | C:Equipment=Multi-ply | D_plus_equipment | mlp | 42 | 1783370 | 545204 | 383325 | 32.11 | 14.22 |
| transfer__C-Equipment-Single-ply__A_squat__ratio | transfer | C:Equipment=Single-ply | A_squat | ratio | 42 | 1125458 | 387275 | 241225 | 2.86 | 21.73 |
| transfer__C-Equipment-Single-ply__C_plus_demographics__lightgbm | transfer | C:Equipment=Single-ply | C_plus_demographics | lightgbm | 42 | 1125458 | 387275 | 241225 | 13.88 | 14.81 |
| transfer__C-Equipment-Single-ply__C_plus_demographics__linear | transfer | C:Equipment=Single-ply | C_plus_demographics | linear | 42 | 1125458 | 387275 | 241225 | 3.65 | 16.82 |
| transfer__C-Equipment-Single-ply__D_plus_equipment__lightgbm | transfer | C:Equipment=Single-ply | D_plus_equipment | lightgbm | 42 | 1125458 | 387275 | 241225 | 9.63 | 14.22 |
| transfer__C-Equipment-Single-ply__D_plus_equipment__linear | transfer | C:Equipment=Single-ply | D_plus_equipment | linear | 42 | 1125458 | 387275 | 241225 | 4.56 | 15.40 |
| transfer__C-Equipment-Single-ply__D_plus_equipment__mlp__s42 | transfer | C:Equipment=Single-ply | D_plus_equipment | mlp | 42 | 1125458 | 387275 | 241225 | 22.53 | 14.23 |
| transfer__C-Equipment-Unlimited__A_squat__ratio | transfer | C:Equipment=Unlimited | A_squat | ratio | 42 | 1627544 | 519210 | 350255 | 3.36 | 22.21 |
| transfer__C-Equipment-Unlimited__C_plus_demographics__lightgbm | transfer | C:Equipment=Unlimited | C_plus_demographics | lightgbm | 42 | 1627544 | 519210 | 350255 | 23.92 | 15.01 |
| transfer__C-Equipment-Unlimited__C_plus_demographics__linear | transfer | C:Equipment=Unlimited | C_plus_demographics | linear | 42 | 1627544 | 519210 | 350255 | 4.70 | 17.08 |
| transfer__C-Equipment-Unlimited__D_plus_equipment__lightgbm | transfer | C:Equipment=Unlimited | D_plus_equipment | lightgbm | 42 | 1627544 | 519210 | 350255 | 17.23 | 14.43 |
| transfer__C-Equipment-Unlimited__D_plus_equipment__linear | transfer | C:Equipment=Unlimited | D_plus_equipment | linear | 42 | 1627544 | 519210 | 350255 | 5.97 | 15.75 |
| transfer__C-Equipment-Unlimited__D_plus_equipment__mlp__s42 | transfer | C:Equipment=Unlimited | D_plus_equipment | mlp | 42 | 1627544 | 519210 | 350255 | 41.10 | 14.66 |
| transfer__C-Equipment-Wraps__A_squat__ratio | transfer | C:Equipment=Wraps | A_squat | ratio | 42 | 1669052 | 511754 | 359626 | 3.43 | 21.92 |
| transfer__C-Equipment-Wraps__C_plus_demographics__lightgbm | transfer | C:Equipment=Wraps | C_plus_demographics | lightgbm | 42 | 1669052 | 511754 | 359626 | 27.32 | 14.51 |
| transfer__C-Equipment-Wraps__C_plus_demographics__linear | transfer | C:Equipment=Wraps | C_plus_demographics | linear | 42 | 1669052 | 511754 | 359626 | 4.39 | 16.81 |
| transfer__C-Equipment-Wraps__D_plus_equipment__lightgbm | transfer | C:Equipment=Wraps | D_plus_equipment | lightgbm | 42 | 1669052 | 511754 | 359626 | 20.69 | 13.95 |
| transfer__C-Equipment-Wraps__D_plus_equipment__linear | transfer | C:Equipment=Wraps | D_plus_equipment | linear | 42 | 1669052 | 511754 | 359626 | 5.86 | 15.36 |
| transfer__C-Equipment-Wraps__D_plus_equipment__mlp__s42 | transfer | C:Equipment=Wraps | D_plus_equipment | mlp | 42 | 1669052 | 511754 | 359626 | 35.78 | 14.19 |
| transfer__C-Federation-THSPA__A_squat__ratio | transfer | C:Federation=THSPA | A_squat | ratio | 42 | 1494571 | 482222 | 321327 | 3.21 | 22.16 |
| transfer__C-Federation-THSPA__D_plus_equipment__lightgbm | transfer | C:Federation=THSPA | D_plus_equipment | lightgbm | 42 | 1494571 | 482222 | 321327 | 13.30 | 14.23 |
| transfer__C-Federation-THSPA__D_plus_equipment__linear | transfer | C:Federation=THSPA | D_plus_equipment | linear | 42 | 1494571 | 482222 | 321327 | 6.02 | 15.44 |
| transfer__C-Federation-THSPA__E_plus_federation__lightgbm | transfer | C:Federation=THSPA | E_plus_federation | lightgbm | 42 | 1494571 | 482222 | 321327 | 12.79 | 14.01 |
| transfer__C-Federation-THSPA__E_plus_federation__linear | transfer | C:Federation=THSPA | E_plus_federation | linear | 42 | 1494571 | 482222 | 321327 | 60.76 | 15.12 |
| transfer__C-Federation-THSPA__E_plus_federation__mlp__s42 | transfer | C:Federation=THSPA | E_plus_federation | mlp | 42 | 1494571 | 482222 | 321327 | 41.32 | 14.04 |
| transfer__C-Federation-THSWPA__A_squat__ratio | transfer | C:Federation=THSWPA | A_squat | ratio | 42 | 1619081 | 515155 | 347919 | 3.36 | 22.69 |
| transfer__C-Federation-THSWPA__D_plus_equipment__lightgbm | transfer | C:Federation=THSWPA | D_plus_equipment | lightgbm | 42 | 1619081 | 515155 | 347919 | 17.29 | 14.71 |
| transfer__C-Federation-THSWPA__D_plus_equipment__linear | transfer | C:Federation=THSWPA | D_plus_equipment | linear | 42 | 1619081 | 515155 | 347919 | 6.06 | 16.13 |
| transfer__C-Federation-THSWPA__E_plus_federation__lightgbm | transfer | C:Federation=THSWPA | E_plus_federation | lightgbm | 42 | 1619081 | 515155 | 347919 | 13.93 | 14.47 |
| transfer__C-Federation-THSWPA__E_plus_federation__linear | transfer | C:Federation=THSWPA | E_plus_federation | linear | 42 | 1619081 | 515155 | 347919 | 103.25 | 15.58 |
| transfer__C-Federation-THSWPA__E_plus_federation__mlp__s42 | transfer | C:Federation=THSWPA | E_plus_federation | mlp | 42 | 1619081 | 515155 | 347919 | 61.68 | 14.47 |
| transfer__C-Federation-USAPL__A_squat__ratio | transfer | C:Federation=USAPL | A_squat | ratio | 42 | 1614712 | 494177 | 347247 | 3.37 | 22.06 |
| transfer__C-Federation-USAPL__D_plus_equipment__lightgbm | transfer | C:Federation=USAPL | D_plus_equipment | lightgbm | 42 | 1614712 | 494177 | 347247 | 18.15 | 14.08 |
| transfer__C-Federation-USAPL__D_plus_equipment__linear | transfer | C:Federation=USAPL | D_plus_equipment | linear | 42 | 1614712 | 494177 | 347247 | 5.84 | 15.48 |
| transfer__C-Federation-USAPL__E_plus_federation__lightgbm | transfer | C:Federation=USAPL | E_plus_federation | lightgbm | 42 | 1614712 | 494177 | 347247 | 13.68 | 13.83 |
| transfer__C-Federation-USAPL__E_plus_federation__linear | transfer | C:Federation=USAPL | E_plus_federation | linear | 42 | 1614712 | 494177 | 347247 | 98.52 | 14.87 |
| transfer__C-Federation-USAPL__E_plus_federation__mlp__s42 | transfer | C:Federation=USAPL | E_plus_federation | mlp | 42 | 1614712 | 494177 | 347247 | 30.46 | 13.84 |

