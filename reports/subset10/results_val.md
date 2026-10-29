# Results — subset10 (VALIDATION only)

MAE in kg with 95% lifter-bootstrap CI. All rows within a comparison are identical across models.

## ablation_core — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| ablation · A · A_squat · ratio | ratio | A_squat | 39386 | 12011 | 21.59 | 21.17 | 21.94 | 21.58 | 12.25 | 0.78 |
| ablation · A · A_squat · linear | linear | A_squat | 39386 | 12011 | 19.56 | 19.27 | 19.91 | 18.66 | 11.60 | 0.83 |
| ablation · A · B_squat_bench · linear | linear | B_squat_bench | 39386 | 12011 | 18.21 | 17.87 | 18.58 | 17.21 | 10.75 | 0.85 |
| ablation · A · C_plus_demographics · linear | linear | C_plus_demographics | 39386 | 12011 | 16.84 | 16.54 | 17.12 | 16.50 | 9.90 | 0.87 |
| ablation · A · D_plus_equipment · linear | linear | D_plus_equipment | 39386 | 12011 | 15.40 | 15.11 | 15.66 | 15.37 | 9.13 | 0.89 |
| ablation · A · A_squat · lightgbm | lightgbm | A_squat | 39386 | 12011 | 17.20 | 16.81 | 17.51 | 16.98 | 10.11 | 0.86 |
| ablation · A · B_squat_bench · lightgbm | lightgbm | B_squat_bench | 39386 | 12011 | 15.91 | 15.58 | 16.23 | 15.38 | 9.25 | 0.88 |
| ablation · A · C_plus_demographics · lightgbm | lightgbm | C_plus_demographics | 39386 | 12011 | 15.04 | 14.78 | 15.26 | 14.74 | 8.74 | 0.89 |
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 39386 | 12011 | 14.32 | 14.05 | 14.56 | 14.20 | 8.37 | 0.90 |
| ablation · A · A_squat · mlp · s42 | mlp | A_squat | 39386 | 12011 | 18.71 | 18.41 | 18.99 | 17.93 | 10.88 | 0.84 |
| ablation · A · B_squat_bench · mlp · s42 | mlp | B_squat_bench | 39386 | 12011 | 17.09 | 16.77 | 17.40 | 16.17 | 9.89 | 0.86 |
| ablation · A · C_plus_demographics · mlp · s42 | mlp | C_plus_demographics | 39386 | 12011 | 15.50 | 15.23 | 15.71 | 15.20 | 8.99 | 0.89 |
| ablation · A · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 39386 | 12011 | 14.44 | 14.18 | 14.64 | 14.37 | 8.41 | 0.90 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | ablation · A · B_squat_bench · linear | ablation · A · A_squat · linear | 39386 | 12011 | -1.35 | -1.53 | -1.19 |
| val | ablation · A · C_plus_demographics · linear | ablation · A · B_squat_bench · linear | 39386 | 12011 | -1.37 | -1.54 | -1.20 |
| val | ablation · A · D_plus_equipment · linear | ablation · A · C_plus_demographics · linear | 39386 | 12011 | -1.45 | -1.59 | -1.31 |
| val | ablation · A · D_plus_equipment · linear | ablation · A · A_squat · ratio | 39386 | 12011 | -6.19 | -6.52 | -5.83 |
| val | ablation · A · B_squat_bench · lightgbm | ablation · A · A_squat · lightgbm | 39386 | 12011 | -1.28 | -1.42 | -1.18 |
| val | ablation · A · C_plus_demographics · lightgbm | ablation · A · B_squat_bench · lightgbm | 39386 | 12011 | -0.87 | -1.06 | -0.69 |
| val | ablation · A · D_plus_equipment · lightgbm | ablation · A · C_plus_demographics · lightgbm | 39386 | 12011 | -0.72 | -0.84 | -0.61 |
| val | ablation · A · D_plus_equipment · lightgbm | ablation · A · A_squat · ratio | 39386 | 12011 | -7.26 | -7.63 | -6.91 |
| val | ablation · A · B_squat_bench · mlp · s42 | ablation · A · A_squat · mlp · s42 | 39386 | 12011 | -1.61 | -1.81 | -1.46 |
| val | ablation · A · C_plus_demographics · mlp · s42 | ablation · A · B_squat_bench · mlp · s42 | 39386 | 12011 | -1.59 | -1.74 | -1.40 |
| val | ablation · A · D_plus_equipment · mlp · s42 | ablation · A · C_plus_demographics · mlp · s42 | 39386 | 12011 | -1.06 | -1.19 | -0.95 |
| val | ablation · A · D_plus_equipment · mlp · s42 | ablation · A · A_squat · ratio | 39386 | 12011 | -7.15 | -7.50 | -6.77 |

## ablation_federation_extension — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| ablation · A · D_plus_equipment · linear | linear | D_plus_equipment | 39386 | 12011 | 15.40 | 15.11 | 15.66 | 15.37 | 9.13 | 0.89 |
| ablation · A · E_plus_federation · linear | linear | E_plus_federation | 39386 | 12011 | 14.85 | 14.55 | 15.11 | 14.91 | 8.82 | 0.89 |
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 39386 | 12011 | 14.32 | 14.05 | 14.56 | 14.20 | 8.37 | 0.90 |
| ablation · A · E_plus_federation · lightgbm | lightgbm | E_plus_federation | 39386 | 12011 | 14.11 | 13.86 | 14.32 | 14.00 | 8.26 | 0.90 |
| ablation · A · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 39386 | 12011 | 14.44 | 14.18 | 14.64 | 14.37 | 8.41 | 0.90 |
| ablation · A · E_plus_federation · mlp · s42 | mlp | E_plus_federation | 39386 | 12011 | 14.04 | 13.79 | 14.25 | 13.93 | 8.19 | 0.90 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | ablation · A · E_plus_federation · linear | ablation · A · D_plus_equipment · linear | 39386 | 12011 | -0.55 | -0.66 | -0.47 |
| val | ablation · A · E_plus_federation · lightgbm | ablation · A · D_plus_equipment · lightgbm | 39386 | 12011 | -0.21 | -0.27 | -0.13 |
| val | ablation · A · E_plus_federation · mlp · s42 | ablation · A · D_plus_equipment · mlp · s42 | 39386 | 12011 | -0.40 | -0.49 | -0.31 |

## models_D — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| ablation · A · A_squat · ratio | ratio | A_squat | 39386 | 12011 | 21.59 | 21.17 | 21.94 | 21.58 | 12.25 | 0.78 |
| ablation · A · D_plus_equipment · linear | linear | D_plus_equipment | 39386 | 12011 | 15.40 | 15.11 | 15.66 | 15.37 | 9.13 | 0.89 |
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 39386 | 12011 | 14.32 | 14.05 | 14.56 | 14.20 | 8.37 | 0.90 |
| ablation · A · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 39386 | 12011 | 14.44 | 14.18 | 14.64 | 14.37 | 8.41 | 0.90 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | ablation · A · D_plus_equipment · lightgbm | ablation · A · D_plus_equipment · linear | 39386 | 12011 | -1.08 | -1.23 | -0.95 |
| val | ablation · A · D_plus_equipment · lightgbm | ablation · A · A_squat · ratio | 39386 | 12011 | -7.26 | -7.63 | -6.91 |
| val | ablation · A · D_plus_equipment · mlp · s42 | ablation · A · D_plus_equipment · lightgbm | 39386 | 12011 | 0.11 | 0.04 | 0.20 |

## history_eligible — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| history · A · D_plus_equipment · last_deadlift · histrows | last_deadlift | D_plus_equipment | 27343 | 6519 | 13.28 | 13.00 | 13.70 | 13.89 | 7.78 | 0.87 |
| ablation · A · D_plus_equipment · linear | linear | D_plus_equipment | 27343 | 6519 | 15.51 | 15.22 | 15.99 | 15.38 | 8.80 | 0.88 |
| history · A · D_plus_equipment · linear · histrows | linear | D_plus_equipment | 27343 | 6519 | 15.58 | 15.29 | 16.03 | 15.53 | 8.92 | 0.88 |
| history · A · D_plus_equipment-history · linear · histrows | linear | D_plus_equipment+history | 27343 | 6519 | 9.86 | 9.69 | 10.09 | 9.74 | 5.77 | 0.94 |
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 27343 | 6519 | 14.51 | 14.24 | 14.97 | 14.36 | 8.18 | 0.90 |
| history · A · D_plus_equipment · lightgbm · histrows | lightgbm | D_plus_equipment | 27343 | 6519 | 14.57 | 14.30 | 15.04 | 14.46 | 8.25 | 0.90 |
| history · A · D_plus_equipment-history · lightgbm · histrows | lightgbm | D_plus_equipment+history | 27343 | 6519 | 9.03 | 8.87 | 9.23 | 9.06 | 5.28 | 0.95 |
| ablation · A · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 27343 | 6519 | 14.59 | 14.31 | 15.06 | 14.50 | 8.21 | 0.90 |
| history · A · D_plus_equipment-history · mlp · histrows · s42 | mlp | D_plus_equipment+history | 27343 | 6519 | 8.99 | 8.84 | 9.19 | 9.03 | 5.32 | 0.95 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | history · A · D_plus_equipment-history · linear · histrows | ablation · A · D_plus_equipment · linear | 27343 | 6519 | -5.65 | -5.97 | -5.35 |
| val | history · A · D_plus_equipment-history · linear · histrows | history · A · D_plus_equipment · linear · histrows | 27343 | 6519 | -5.72 | -6.01 | -5.44 |
| val | history · A · D_plus_equipment-history · linear · histrows | history · A · D_plus_equipment · last_deadlift · histrows | 27343 | 6519 | -3.43 | -3.69 | -3.21 |
| val | history · A · D_plus_equipment-history · lightgbm · histrows | ablation · A · D_plus_equipment · lightgbm | 27343 | 6519 | -5.49 | -5.76 | -5.23 |
| val | history · A · D_plus_equipment-history · lightgbm · histrows | history · A · D_plus_equipment · lightgbm · histrows | 27343 | 6519 | -5.54 | -5.81 | -5.29 |
| val | history · A · D_plus_equipment-history · lightgbm · histrows | history · A · D_plus_equipment · last_deadlift · histrows | 27343 | 6519 | -4.25 | -4.52 | -4.02 |
| val | history · A · D_plus_equipment-history · mlp · histrows · s42 | ablation · A · D_plus_equipment · mlp · s42 | 27343 | 6519 | -5.61 | -5.87 | -5.35 |
| val | history · A · D_plus_equipment-history · mlp · histrows · s42 | history · A · D_plus_equipment · last_deadlift · histrows | 27343 | 6519 | -4.29 | -4.57 | -4.08 |

## no_history_rows — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| ablation · A · A_squat · ratio | ratio | A_squat | 12043 | 12011 | 21.31 | 21.04 | 21.55 | 21.31 | 12.96 | 0.77 |
| ablation · A · D_plus_equipment · linear | linear | D_plus_equipment | 12043 | 12011 | 15.14 | 14.96 | 15.39 | 15.13 | 9.85 | 0.88 |
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 12043 | 12011 | 13.89 | 13.72 | 14.08 | 13.87 | 8.80 | 0.90 |
| ablation · A · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 12043 | 12011 | 14.08 | 13.90 | 14.28 | 14.06 | 8.87 | 0.90 |

## chrono_all — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| chrono · B · A_squat · ratio | ratio | A_squat | 39588 | 18296 | 21.41 | 21.10 | 21.71 | 21.88 | 12.31 | 0.78 |
| chrono · B · D_plus_equipment · linear | linear | D_plus_equipment | 39588 | 18296 | 14.75 | 14.55 | 14.93 | 15.05 | 8.90 | 0.89 |
| chrono · B · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 39588 | 18296 | 13.89 | 13.69 | 14.05 | 14.28 | 8.28 | 0.90 |
| chrono · B · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 39588 | 18296 | 13.73 | 13.53 | 13.91 | 14.16 | 8.14 | 0.91 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | chrono · B · D_plus_equipment · lightgbm | chrono · B · A_squat · ratio | 39588 | 18296 | -7.53 | -7.84 | -7.25 |
| val | chrono · B · D_plus_equipment · lightgbm | chrono · B · D_plus_equipment · linear | 39588 | 18296 | -0.86 | -0.97 | -0.76 |
| val | chrono · B · D_plus_equipment · mlp · s42 | chrono · B · D_plus_equipment · lightgbm | 39588 | 18296 | -0.15 | -0.20 | -0.09 |

## chrono_history_eligible — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| chrono · B · D_plus_equipment · last_deadlift · histrows | last_deadlift | D_plus_equipment | 28211 | 11721 | 12.47 | 12.27 | 12.75 | 13.86 | 7.49 | 0.88 |
| chrono · B · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 28211 | 11721 | 14.01 | 13.81 | 14.25 | 14.42 | 8.11 | 0.90 |
| chrono · B · D_plus_equipment · lightgbm · histrows | lightgbm | D_plus_equipment | 28211 | 11721 | 14.04 | 13.84 | 14.30 | 14.47 | 8.16 | 0.90 |
| chrono · B · D_plus_equipment-history · lightgbm · histrows | lightgbm | D_plus_equipment+history | 28211 | 11721 | 8.51 | 8.41 | 8.66 | 9.08 | 5.14 | 0.96 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | chrono · B · D_plus_equipment-history · lightgbm · histrows | chrono · B · D_plus_equipment · lightgbm · histrows | 28211 | 11721 | -5.53 | -5.84 | -5.33 |
| val | chrono · B · D_plus_equipment-history · lightgbm · histrows | chrono · B · D_plus_equipment · last_deadlift · histrows | 28211 | 11721 | -3.96 | -4.13 | -3.76 |
| val | chrono · B · D_plus_equipment-history · lightgbm · histrows | chrono · B · D_plus_equipment · lightgbm | 28211 | 11721 | -5.50 | -5.81 | -5.31 |

## transfer|Equipment=Single-ply — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Equipment-Single-ply · A_squat · ratio | ratio | A_squat | 24312 | 8435 | 21.30 | 20.88 | 21.68 | 20.84 | 12.13 | 0.79 |
| transfer · C-Equipment-Single-ply · D_plus_equipment · linear | linear | D_plus_equipment | 24312 | 8435 | 15.26 | 14.91 | 15.51 | 15.26 | 9.11 | 0.89 |
| transfer · C-Equipment-Single-ply · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 24312 | 8435 | 14.40 | 14.07 | 14.62 | 14.35 | 8.40 | 0.90 |
| transfer · C-Equipment-Single-ply · C_plus_demographics · linear | linear | C_plus_demographics | 24312 | 8435 | 16.69 | 16.32 | 16.96 | 16.33 | 9.86 | 0.87 |
| transfer · C-Equipment-Single-ply · C_plus_demographics · lightgbm | lightgbm | C_plus_demographics | 24312 | 8435 | 15.15 | 14.81 | 15.36 | 14.92 | 8.80 | 0.89 |
| transfer · C-Equipment-Single-ply · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 24312 | 8435 | 14.31 | 13.97 | 14.55 | 14.27 | 8.35 | 0.90 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | transfer · C-Equipment-Single-ply · D_plus_equipment · lightgbm | transfer · C-Equipment-Single-ply · C_plus_demographics · lightgbm | 24312 | 8435 | -0.76 | -0.86 | -0.65 |
| val | transfer · C-Equipment-Single-ply · D_plus_equipment · lightgbm | transfer · C-Equipment-Single-ply · A_squat · ratio | 24312 | 8435 | -6.91 | -7.24 | -6.47 |

## transfer|Equipment=Unlimited — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Equipment-Unlimited · A_squat · ratio | ratio | A_squat | 35401 | 11285 | 21.82 | 21.39 | 22.25 | 21.53 | 12.12 | 0.78 |
| transfer · C-Equipment-Unlimited · D_plus_equipment · linear | linear | D_plus_equipment | 35401 | 11285 | 15.65 | 15.34 | 15.91 | 15.50 | 9.08 | 0.88 |
| transfer · C-Equipment-Unlimited · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 35401 | 11285 | 14.64 | 14.34 | 14.91 | 14.37 | 8.37 | 0.89 |
| transfer · C-Equipment-Unlimited · C_plus_demographics · linear | linear | C_plus_demographics | 35401 | 11285 | 17.04 | 16.73 | 17.33 | 16.49 | 9.85 | 0.86 |
| transfer · C-Equipment-Unlimited · C_plus_demographics · lightgbm | lightgbm | C_plus_demographics | 35401 | 11285 | 15.33 | 15.04 | 15.60 | 14.83 | 8.72 | 0.88 |
| transfer · C-Equipment-Unlimited · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 35401 | 11285 | 14.78 | 14.49 | 15.02 | 14.55 | 8.46 | 0.89 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | transfer · C-Equipment-Unlimited · D_plus_equipment · lightgbm | transfer · C-Equipment-Unlimited · C_plus_demographics · lightgbm | 35401 | 11285 | -0.69 | -0.80 | -0.59 |
| val | transfer · C-Equipment-Unlimited · D_plus_equipment · lightgbm | transfer · C-Equipment-Unlimited · A_squat · ratio | 35401 | 11285 | -7.18 | -7.58 | -6.83 |

## transfer|Equipment=Wraps — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Equipment-Wraps · A_squat · ratio | ratio | A_squat | 36278 | 11167 | 21.48 | 20.95 | 21.86 | 21.60 | 12.26 | 0.78 |
| transfer · C-Equipment-Wraps · D_plus_equipment · linear | linear | D_plus_equipment | 36278 | 11167 | 15.29 | 14.94 | 15.62 | 15.33 | 9.12 | 0.89 |
| transfer · C-Equipment-Wraps · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 36278 | 11167 | 14.14 | 13.87 | 14.46 | 14.07 | 8.32 | 0.90 |
| transfer · C-Equipment-Wraps · C_plus_demographics · linear | linear | C_plus_demographics | 36278 | 11167 | 16.81 | 16.45 | 17.10 | 16.55 | 9.93 | 0.87 |
| transfer · C-Equipment-Wraps · C_plus_demographics · lightgbm | lightgbm | C_plus_demographics | 36278 | 11167 | 14.85 | 14.55 | 15.13 | 14.62 | 8.68 | 0.89 |
| transfer · C-Equipment-Wraps · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 36278 | 11167 | 14.28 | 13.99 | 14.59 | 14.26 | 8.37 | 0.90 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | transfer · C-Equipment-Wraps · D_plus_equipment · lightgbm | transfer · C-Equipment-Wraps · C_plus_demographics · lightgbm | 36278 | 11167 | -0.71 | -0.82 | -0.59 |
| val | transfer · C-Equipment-Wraps · D_plus_equipment · lightgbm | transfer · C-Equipment-Wraps · A_squat · ratio | 36278 | 11167 | -7.34 | -7.71 | -6.97 |

## transfer|Federation=THSPA — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Federation-THSPA · A_squat · ratio | ratio | A_squat | 32553 | 10480 | 21.68 | 21.21 | 22.02 | 21.48 | 12.30 | 0.80 |
| transfer · C-Federation-THSPA · E_plus_federation · linear | linear | E_plus_federation | 32553 | 10480 | 15.03 | 14.64 | 15.35 | 15.05 | 8.92 | 0.90 |
| transfer · C-Federation-THSPA · E_plus_federation · lightgbm | lightgbm | E_plus_federation | 32553 | 10480 | 14.30 | 14.00 | 14.60 | 14.10 | 8.35 | 0.91 |
| transfer · C-Federation-THSPA · D_plus_equipment · linear | linear | D_plus_equipment | 32553 | 10480 | 15.31 | 14.97 | 15.64 | 15.26 | 9.11 | 0.90 |
| transfer · C-Federation-THSPA · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 32553 | 10480 | 14.43 | 14.15 | 14.71 | 14.27 | 8.44 | 0.91 |
| transfer · C-Federation-THSPA · E_plus_federation · mlp · s42 | mlp | E_plus_federation | 32553 | 10480 | 14.19 | 13.90 | 14.49 | 14.06 | 8.25 | 0.91 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | transfer · C-Federation-THSPA · E_plus_federation · lightgbm | transfer · C-Federation-THSPA · D_plus_equipment · lightgbm | 32553 | 10480 | -0.13 | -0.22 | -0.06 |
| val | transfer · C-Federation-THSPA · E_plus_federation · lightgbm | transfer · C-Federation-THSPA · A_squat · ratio | 32553 | 10480 | -7.38 | -7.78 | -6.92 |

## transfer|Federation=USAPL — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Federation-USAPL · A_squat · ratio | ratio | A_squat | 35225 | 10786 | 21.61 | 21.14 | 22.04 | 21.80 | 12.26 | 0.78 |
| transfer · C-Federation-USAPL · E_plus_federation · linear | linear | E_plus_federation | 35225 | 10786 | 14.81 | 14.50 | 15.07 | 14.97 | 8.81 | 0.89 |
| transfer · C-Federation-USAPL · E_plus_federation · lightgbm | lightgbm | E_plus_federation | 35225 | 10786 | 14.12 | 13.82 | 14.36 | 14.05 | 8.26 | 0.90 |
| transfer · C-Federation-USAPL · D_plus_equipment · linear | linear | D_plus_equipment | 35225 | 10786 | 15.42 | 15.10 | 15.73 | 15.46 | 9.15 | 0.89 |
| transfer · C-Federation-USAPL · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 35225 | 10786 | 14.32 | 14.04 | 14.57 | 14.26 | 8.38 | 0.90 |
| transfer · C-Federation-USAPL · E_plus_federation · mlp · s42 | mlp | E_plus_federation | 35225 | 10786 | 14.02 | 13.72 | 14.28 | 14.06 | 8.24 | 0.90 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | transfer · C-Federation-USAPL · E_plus_federation · lightgbm | transfer · C-Federation-USAPL · D_plus_equipment · lightgbm | 35225 | 10786 | -0.21 | -0.30 | -0.12 |
| val | transfer · C-Federation-USAPL · E_plus_federation · lightgbm | transfer · C-Federation-USAPL · A_squat · ratio | 35225 | 10786 | -7.50 | -7.89 | -7.10 |

## transfer|Federation=THSWPA — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Federation-THSWPA · A_squat · ratio | ratio | A_squat | 35121 | 11231 | 22.36 | 21.98 | 22.80 | 21.91 | 12.06 | 0.74 |
| transfer · C-Federation-THSWPA · E_plus_federation · linear | linear | E_plus_federation | 35121 | 11231 | 15.55 | 15.29 | 15.87 | 15.32 | 8.83 | 0.87 |
| transfer · C-Federation-THSWPA · E_plus_federation · lightgbm | lightgbm | E_plus_federation | 35121 | 11231 | 14.77 | 14.52 | 15.09 | 14.38 | 8.23 | 0.88 |
| transfer · C-Federation-THSWPA · D_plus_equipment · linear | linear | D_plus_equipment | 35121 | 11231 | 16.08 | 15.80 | 16.40 | 15.75 | 9.11 | 0.86 |
| transfer · C-Federation-THSWPA · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 35121 | 11231 | 14.96 | 14.69 | 15.27 | 14.58 | 8.32 | 0.88 |
| transfer · C-Federation-THSWPA · E_plus_federation · mlp · s42 | mlp | E_plus_federation | 35121 | 11231 | 14.69 | 14.45 | 14.99 | 14.35 | 8.19 | 0.88 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | transfer · C-Federation-THSWPA · E_plus_federation · lightgbm | transfer · C-Federation-THSWPA · D_plus_equipment · lightgbm | 35121 | 11231 | -0.19 | -0.27 | -0.10 |
| val | transfer · C-Federation-THSWPA · E_plus_federation · lightgbm | transfer · C-Federation-THSWPA · A_squat · ratio | 35121 | 11231 | -7.59 | -7.94 | -7.28 |

## Subgroups (protocol A, feature set D; protocol B LightGBM)

| run_id | group_by | group | rows | lifters | mae | mape | r2 | sparse |
|---|---|---|---|---|---|---|---|---|
| ablation · A · A_squat · ratio | Sex | F | 12305 | 3528 | 16.34 | 13.22 | 0.55 | False |
| ablation · A · A_squat · ratio | Sex | M | 27078 | 8500 | 23.97 | 11.81 | 0.64 | False |
| ablation · A · A_squat · ratio | Sex | Mx | 3 | 2 | 21.51 | 12.80 | -3.02 | True |
| ablation · A · A_squat · ratio | bw_bin | 0-60 | 6706 | 2126 | 15.53 | 12.87 | 0.72 | False |
| ablation · A · A_squat · ratio | bw_bin | 105-120 | 3458 | 1424 | 26.77 | 12.98 | 0.61 | False |
| ablation · A · A_squat · ratio | bw_bin | 120-1000 | 2310 | 824 | 29.30 | 13.20 | 0.54 | False |
| ablation · A · A_squat · ratio | bw_bin | 60-75 | 10061 | 3793 | 19.42 | 12.21 | 0.70 | False |
| ablation · A · A_squat · ratio | bw_bin | 75-90 | 9442 | 3865 | 22.51 | 11.77 | 0.68 | False |
| ablation · A · A_squat · ratio | bw_bin | 90-105 | 7188 | 2814 | 23.81 | 11.51 | 0.68 | False |
| ablation · A · A_squat · ratio | bw_bin | missing | 221 | 150 | 30.45 | 18.14 | 0.53 | False |
| ablation · A · A_squat · ratio | has_history | False | 12043 | 12011 | 21.31 | 12.96 | 0.77 | False |
| ablation · A · A_squat · ratio | has_history | True | 27343 | 6519 | 21.71 | 11.94 | 0.78 | False |
| ablation · A · A_squat · ratio | Equipment | Multi-ply | 771 | 308 | 40.50 | 19.31 | 0.27 | False |
| ablation · A · A_squat · ratio | Equipment | Raw | 16448 | 6445 | 22.69 | 12.58 | 0.77 | False |
| ablation · A · A_squat · ratio | Equipment | Single-ply | 15074 | 4485 | 20.13 | 11.49 | 0.80 | False |
| ablation · A · A_squat · ratio | Equipment | Unlimited | 3985 | 968 | 17.85 | 12.45 | 0.72 | False |
| ablation · A · A_squat · ratio | Equipment | Wraps | 3108 | 1506 | 22.87 | 12.19 | 0.78 | False |
| ablation · A · D_plus_equipment · linear | Sex | F | 12305 | 3528 | 11.28 | 9.66 | 0.79 | False |
| ablation · A · D_plus_equipment · linear | Sex | M | 27078 | 8500 | 17.27 | 8.88 | 0.81 | False |
| ablation · A · D_plus_equipment · linear | Sex | Mx | 3 | 2 | 19.75 | 11.70 | -5.31 | True |
| ablation · A · D_plus_equipment · linear | bw_bin | 0-60 | 6706 | 2126 | 11.80 | 10.78 | 0.83 | False |
| ablation · A · D_plus_equipment · linear | bw_bin | 105-120 | 3458 | 1424 | 18.52 | 9.21 | 0.81 | False |
| ablation · A · D_plus_equipment · linear | bw_bin | 120-1000 | 2310 | 824 | 21.30 | 9.78 | 0.77 | False |
| ablation · A · D_plus_equipment · linear | bw_bin | 60-75 | 10061 | 3793 | 13.44 | 8.81 | 0.85 | False |
| ablation · A · D_plus_equipment · linear | bw_bin | 75-90 | 9442 | 3865 | 15.68 | 8.41 | 0.83 | False |
| ablation · A · D_plus_equipment · linear | bw_bin | 90-105 | 7188 | 2814 | 17.51 | 8.52 | 0.82 | False |
| ablation · A · D_plus_equipment · linear | bw_bin | missing | 221 | 150 | 22.51 | 15.76 | 0.76 | False |
| ablation · A · D_plus_equipment · linear | has_history | False | 12043 | 12011 | 15.14 | 9.85 | 0.88 | False |
| ablation · A · D_plus_equipment · linear | has_history | True | 27343 | 6519 | 15.51 | 8.80 | 0.88 | False |
| ablation · A · D_plus_equipment · linear | Equipment | Multi-ply | 771 | 308 | 23.90 | 12.14 | 0.74 | False |
| ablation · A · D_plus_equipment · linear | Equipment | Raw | 16448 | 6445 | 15.36 | 9.11 | 0.88 | False |
| ablation · A · D_plus_equipment · linear | Equipment | Single-ply | 15074 | 4485 | 15.51 | 9.04 | 0.88 | False |
| ablation · A · D_plus_equipment · linear | Equipment | Unlimited | 3985 | 968 | 12.52 | 8.92 | 0.87 | False |
| ablation · A · D_plus_equipment · linear | Equipment | Wraps | 3108 | 1506 | 16.66 | 9.17 | 0.87 | False |
| ablation · A · D_plus_equipment · lightgbm | Sex | F | 12305 | 3528 | 10.49 | 8.84 | 0.81 | False |
| ablation · A · D_plus_equipment · lightgbm | Sex | M | 27078 | 8500 | 16.06 | 8.16 | 0.83 | False |
| ablation · A · D_plus_equipment · lightgbm | Sex | Mx | 3 | 2 | 18.02 | 10.61 | -4.62 | True |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | 0-60 | 6706 | 2126 | 10.02 | 8.69 | 0.88 | False |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | 105-120 | 3458 | 1424 | 17.60 | 8.77 | 0.83 | False |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | 120-1000 | 2310 | 824 | 20.26 | 9.19 | 0.78 | False |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | 60-75 | 10061 | 3793 | 12.71 | 8.24 | 0.87 | False |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | 75-90 | 9442 | 3865 | 14.82 | 8.04 | 0.85 | False |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | 90-105 | 7188 | 2814 | 16.23 | 8.03 | 0.84 | False |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | missing | 221 | 150 | 21.31 | 14.19 | 0.77 | False |
| ablation · A · D_plus_equipment · lightgbm | has_history | False | 12043 | 12011 | 13.89 | 8.80 | 0.90 | False |
| ablation · A · D_plus_equipment · lightgbm | has_history | True | 27343 | 6519 | 14.51 | 8.18 | 0.90 | False |
| ablation · A · D_plus_equipment · lightgbm | Equipment | Multi-ply | 771 | 308 | 21.06 | 10.78 | 0.79 | False |
| ablation · A · D_plus_equipment · lightgbm | Equipment | Raw | 16448 | 6445 | 14.34 | 8.15 | 0.89 | False |
| ablation · A · D_plus_equipment · lightgbm | Equipment | Single-ply | 15074 | 4485 | 14.26 | 8.37 | 0.90 | False |
| ablation · A · D_plus_equipment · lightgbm | Equipment | Unlimited | 3985 | 968 | 11.49 | 8.33 | 0.90 | False |
| ablation · A · D_plus_equipment · lightgbm | Equipment | Wraps | 3108 | 1506 | 16.49 | 8.95 | 0.87 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Sex | F | 12305 | 3528 | 10.45 | 8.82 | 0.82 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Sex | M | 27078 | 8500 | 16.25 | 8.23 | 0.83 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Sex | Mx | 3 | 2 | 16.29 | 9.54 | -2.49 | True |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | 0-60 | 6706 | 2126 | 10.00 | 8.70 | 0.88 | False |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | 105-120 | 3458 | 1424 | 17.61 | 8.75 | 0.83 | False |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | 120-1000 | 2310 | 824 | 20.31 | 9.18 | 0.79 | False |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | 60-75 | 10061 | 3793 | 12.78 | 8.28 | 0.87 | False |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | 75-90 | 9442 | 3865 | 14.96 | 8.09 | 0.85 | False |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | 90-105 | 7188 | 2814 | 16.60 | 8.17 | 0.84 | False |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | missing | 221 | 150 | 20.59 | 13.76 | 0.79 | False |
| ablation · A · D_plus_equipment · mlp · s42 | has_history | False | 12043 | 12011 | 14.08 | 8.87 | 0.90 | False |
| ablation · A · D_plus_equipment · mlp · s42 | has_history | True | 27343 | 6519 | 14.59 | 8.21 | 0.90 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Equipment | Multi-ply | 771 | 308 | 20.55 | 10.55 | 0.79 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Equipment | Raw | 16448 | 6445 | 14.29 | 8.13 | 0.90 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Equipment | Single-ply | 15074 | 4485 | 14.67 | 8.54 | 0.89 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Equipment | Unlimited | 3985 | 968 | 11.44 | 8.29 | 0.90 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Equipment | Wraps | 3108 | 1506 | 16.41 | 8.87 | 0.87 | False |
| chrono · B · D_plus_equipment · lightgbm | Sex | F | 15035 | 6183 | 10.16 | 8.42 | 0.83 | False |
| chrono · B · D_plus_equipment · lightgbm | Sex | M | 24548 | 12109 | 16.17 | 8.19 | 0.82 | False |
| chrono · B · D_plus_equipment · lightgbm | Sex | Mx | 5 | 4 | 13.63 | 8.71 | 0.81 | True |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | 0-60 | 6808 | 2730 | 9.75 | 8.60 | 0.86 | False |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | 105-120 | 3368 | 1849 | 16.81 | 8.22 | 0.84 | False |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | 120-1000 | 2474 | 1124 | 19.64 | 9.60 | 0.78 | False |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | 60-75 | 10617 | 5505 | 12.34 | 8.20 | 0.87 | False |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | 75-90 | 9900 | 5482 | 14.31 | 7.82 | 0.87 | False |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | 90-105 | 6411 | 3649 | 16.44 | 8.30 | 0.85 | False |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | missing | 10 | 9 | 17.22 | 11.53 | 0.79 | True |
| chrono · B · D_plus_equipment · lightgbm | has_history | False | 11377 | 11364 | 13.59 | 8.69 | 0.89 | False |
| chrono · B · D_plus_equipment · lightgbm | has_history | True | 28211 | 11721 | 14.01 | 8.11 | 0.90 | False |
| chrono · B · D_plus_equipment · lightgbm | Equipment | Multi-ply | 141 | 79 | 21.05 | 10.14 | 0.77 | False |
| chrono · B · D_plus_equipment · lightgbm | Equipment | Raw | 22701 | 13066 | 14.58 | 8.00 | 0.89 | False |
| chrono · B · D_plus_equipment · lightgbm | Equipment | Single-ply | 1303 | 809 | 17.00 | 9.49 | 0.85 | False |
| chrono · B · D_plus_equipment · lightgbm | Equipment | Unlimited | 12994 | 3558 | 11.92 | 8.58 | 0.89 | False |
| chrono · B · D_plus_equipment · lightgbm | Equipment | Wraps | 2449 | 1656 | 15.86 | 8.43 | 0.87 | False |

## Runs

| run_id | experiment | protocol | feature_set | model | seed | train_rows | train_lifters | val_rows | fit_seconds | val_mae |
|---|---|---|---|---|---|---|---|---|---|---|
| ablation__A__A_squat__lightgbm | ablation | A | A_squat | lightgbm | 42 | 182158 | 55295 | 39386 | 19.49 | 17.20 |
| ablation__A__A_squat__linear | ablation | A | A_squat | linear | 42 | 182158 | 55295 | 39386 | 1.06 | 19.56 |
| ablation__A__A_squat__mlp__s42 | ablation | A | A_squat | mlp | 42 | 182158 | 55295 | 39386 | 4.00 | 18.71 |
| ablation__A__A_squat__ratio | ablation | A | A_squat | ratio | 42 | 182158 | 55295 | 39386 | 0.04 | 21.59 |
| ablation__A__B_squat_bench__lightgbm | ablation | A | B_squat_bench | lightgbm | 42 | 182158 | 55295 | 39386 | 14.50 | 15.91 |
| ablation__A__B_squat_bench__linear | ablation | A | B_squat_bench | linear | 42 | 182158 | 55295 | 39386 | 0.07 | 18.21 |
| ablation__A__B_squat_bench__mlp__s42 | ablation | A | B_squat_bench | mlp | 42 | 182158 | 55295 | 39386 | 2.23 | 17.09 |
| ablation__A__C_plus_demographics__lightgbm | ablation | A | C_plus_demographics | lightgbm | 42 | 182158 | 55295 | 39386 | 17.17 | 15.04 |
| ablation__A__C_plus_demographics__linear | ablation | A | C_plus_demographics | linear | 42 | 182158 | 55295 | 39386 | 0.19 | 16.84 |
| ablation__A__C_plus_demographics__mlp__s42 | ablation | A | C_plus_demographics | mlp | 42 | 182158 | 55295 | 39386 | 3.67 | 15.50 |
| ablation__A__D_plus_equipment__lightgbm | ablation | A | D_plus_equipment | lightgbm | 42 | 182158 | 55295 | 39386 | 12.81 | 14.32 |
| ablation__A__D_plus_equipment__linear | ablation | A | D_plus_equipment | linear | 42 | 182158 | 55295 | 39386 | 0.35 | 15.40 |
| ablation__A__D_plus_equipment__mlp__s42 | ablation | A | D_plus_equipment | mlp | 42 | 182158 | 55295 | 39386 | 3.87 | 14.44 |
| ablation__A__E_plus_federation__lightgbm | ablation | A | E_plus_federation | lightgbm | 42 | 182158 | 55295 | 39386 | 12.51 | 14.11 |
| ablation__A__E_plus_federation__linear | ablation | A | E_plus_federation | linear | 42 | 182158 | 55295 | 39386 | 0.91 | 14.85 |
| ablation__A__E_plus_federation__mlp__s42 | ablation | A | E_plus_federation | mlp | 42 | 182158 | 55295 | 39386 | 6.06 | 14.04 |
| chrono__B__A_squat__ratio | chrono | B | A_squat | ratio | 42 | 181042 | 57692 | 39588 | 0.04 | 21.41 |
| chrono__B__D_plus_equipment-history__lightgbm__histrows | chrono | B | D_plus_equipment+history | lightgbm | 42 | 123171 | 30103 | 28211 | 17.25 | 8.51 |
| chrono__B__D_plus_equipment__last_deadlift__histrows | chrono | B | D_plus_equipment | last_deadlift | 42 | 123171 | 30103 | 28211 | 0.03 | 12.47 |
| chrono__B__D_plus_equipment__lightgbm | chrono | B | D_plus_equipment | lightgbm | 42 | 181042 | 57692 | 39588 | 4.27 | 13.89 |
| chrono__B__D_plus_equipment__lightgbm__histrows | chrono | B | D_plus_equipment | lightgbm | 42 | 123171 | 30103 | 28211 | 3.21 | 14.04 |
| chrono__B__D_plus_equipment__linear | chrono | B | D_plus_equipment | linear | 42 | 181042 | 57692 | 39588 | 0.25 | 14.75 |
| chrono__B__D_plus_equipment__mlp__s42 | chrono | B | D_plus_equipment | mlp | 42 | 181042 | 57692 | 39588 | 4.10 | 13.73 |
| history__A__D_plus_equipment-history__lightgbm__histrows | history | A | D_plus_equipment+history | lightgbm | 42 | 126714 | 30167 | 27343 | 15.34 | 9.03 |
| history__A__D_plus_equipment-history__linear__histrows | history | A | D_plus_equipment+history | linear | 42 | 126714 | 30167 | 27343 | 0.17 | 9.86 |
| history__A__D_plus_equipment-history__mlp__histrows__s42 | history | A | D_plus_equipment+history | mlp | 42 | 126714 | 30167 | 27343 | 6.40 | 8.99 |
| history__A__D_plus_equipment__last_deadlift__histrows | history | A | D_plus_equipment | last_deadlift | 42 | 126714 | 30167 | 27343 | 0.03 | 13.28 |
| history__A__D_plus_equipment__lightgbm__histrows | history | A | D_plus_equipment | lightgbm | 42 | 126714 | 30167 | 27343 | 12.70 | 14.57 |
| history__A__D_plus_equipment__linear__histrows | history | A | D_plus_equipment | linear | 42 | 126714 | 30167 | 27343 | 0.23 | 15.58 |
| transfer__C-Equipment-Single-ply__A_squat__ratio | transfer | C:Equipment=Single-ply | A_squat | ratio | 42 | 113509 | 38812 | 24312 | 0.26 | 21.30 |
| transfer__C-Equipment-Single-ply__C_plus_demographics__lightgbm | transfer | C:Equipment=Single-ply | C_plus_demographics | lightgbm | 42 | 113509 | 38812 | 24312 | 4.38 | 15.15 |
| transfer__C-Equipment-Single-ply__C_plus_demographics__linear | transfer | C:Equipment=Single-ply | C_plus_demographics | linear | 42 | 113509 | 38812 | 24312 | 0.33 | 16.69 |
| transfer__C-Equipment-Single-ply__D_plus_equipment__lightgbm | transfer | C:Equipment=Single-ply | D_plus_equipment | lightgbm | 42 | 113509 | 38812 | 24312 | 2.91 | 14.40 |
| transfer__C-Equipment-Single-ply__D_plus_equipment__linear | transfer | C:Equipment=Single-ply | D_plus_equipment | linear | 42 | 113509 | 38812 | 24312 | 0.38 | 15.26 |
| transfer__C-Equipment-Single-ply__D_plus_equipment__mlp__s42 | transfer | C:Equipment=Single-ply | D_plus_equipment | mlp | 42 | 113509 | 38812 | 24312 | 2.87 | 14.31 |
| transfer__C-Equipment-Unlimited__A_squat__ratio | transfer | C:Equipment=Unlimited | A_squat | ratio | 42 | 162967 | 51985 | 35401 | 0.34 | 21.82 |
| transfer__C-Equipment-Unlimited__C_plus_demographics__lightgbm | transfer | C:Equipment=Unlimited | C_plus_demographics | lightgbm | 42 | 162967 | 51985 | 35401 | 4.59 | 15.33 |
| transfer__C-Equipment-Unlimited__C_plus_demographics__linear | transfer | C:Equipment=Unlimited | C_plus_demographics | linear | 42 | 162967 | 51985 | 35401 | 0.45 | 17.04 |
| transfer__C-Equipment-Unlimited__D_plus_equipment__lightgbm | transfer | C:Equipment=Unlimited | D_plus_equipment | lightgbm | 42 | 162967 | 51985 | 35401 | 3.67 | 14.64 |
| transfer__C-Equipment-Unlimited__D_plus_equipment__linear | transfer | C:Equipment=Unlimited | D_plus_equipment | linear | 42 | 162967 | 51985 | 35401 | 0.57 | 15.65 |
| transfer__C-Equipment-Unlimited__D_plus_equipment__mlp__s42 | transfer | C:Equipment=Unlimited | D_plus_equipment | mlp | 42 | 162967 | 51985 | 35401 | 4.25 | 14.78 |
| transfer__C-Equipment-Wraps__A_squat__ratio | transfer | C:Equipment=Wraps | A_squat | ratio | 42 | 167267 | 51293 | 36278 | 0.33 | 21.48 |
| transfer__C-Equipment-Wraps__C_plus_demographics__lightgbm | transfer | C:Equipment=Wraps | C_plus_demographics | lightgbm | 42 | 167267 | 51293 | 36278 | 5.00 | 14.85 |
| transfer__C-Equipment-Wraps__C_plus_demographics__linear | transfer | C:Equipment=Wraps | C_plus_demographics | linear | 42 | 167267 | 51293 | 36278 | 0.42 | 16.81 |
| transfer__C-Equipment-Wraps__D_plus_equipment__lightgbm | transfer | C:Equipment=Wraps | D_plus_equipment | lightgbm | 42 | 167267 | 51293 | 36278 | 3.50 | 14.14 |
| transfer__C-Equipment-Wraps__D_plus_equipment__linear | transfer | C:Equipment=Wraps | D_plus_equipment | linear | 42 | 167267 | 51293 | 36278 | 0.54 | 15.29 |
| transfer__C-Equipment-Wraps__D_plus_equipment__mlp__s42 | transfer | C:Equipment=Wraps | D_plus_equipment | mlp | 42 | 167267 | 51293 | 36278 | 4.13 | 14.28 |
| transfer__C-Federation-THSPA__A_squat__ratio | transfer | C:Federation=THSPA | A_squat | ratio | 42 | 149980 | 48342 | 32553 | 0.31 | 21.68 |
| transfer__C-Federation-THSPA__D_plus_equipment__lightgbm | transfer | C:Federation=THSPA | D_plus_equipment | lightgbm | 42 | 149980 | 48342 | 32553 | 3.24 | 14.43 |
| transfer__C-Federation-THSPA__D_plus_equipment__linear | transfer | C:Federation=THSPA | D_plus_equipment | linear | 42 | 149980 | 48342 | 32553 | 0.48 | 15.31 |
| transfer__C-Federation-THSPA__E_plus_federation__lightgbm | transfer | C:Federation=THSPA | E_plus_federation | lightgbm | 42 | 149980 | 48342 | 32553 | 3.38 | 14.30 |
| transfer__C-Federation-THSPA__E_plus_federation__linear | transfer | C:Federation=THSPA | E_plus_federation | linear | 42 | 149980 | 48342 | 32553 | 1.01 | 15.03 |
| transfer__C-Federation-THSPA__E_plus_federation__mlp__s42 | transfer | C:Federation=THSPA | E_plus_federation | mlp | 42 | 149980 | 48342 | 32553 | 4.70 | 14.19 |
| transfer__C-Federation-THSWPA__A_squat__ratio | transfer | C:Federation=THSWPA | A_squat | ratio | 42 | 161954 | 51585 | 35121 | 0.33 | 22.36 |
| transfer__C-Federation-THSWPA__D_plus_equipment__lightgbm | transfer | C:Federation=THSWPA | D_plus_equipment | lightgbm | 42 | 161954 | 51585 | 35121 | 3.74 | 14.96 |
| transfer__C-Federation-THSWPA__D_plus_equipment__linear | transfer | C:Federation=THSWPA | D_plus_equipment | linear | 42 | 161954 | 51585 | 35121 | 0.57 | 16.08 |
| transfer__C-Federation-THSWPA__E_plus_federation__lightgbm | transfer | C:Federation=THSWPA | E_plus_federation | lightgbm | 42 | 161954 | 51585 | 35121 | 3.76 | 14.77 |
| transfer__C-Federation-THSWPA__E_plus_federation__linear | transfer | C:Federation=THSWPA | E_plus_federation | linear | 42 | 161954 | 51585 | 35121 | 0.69 | 15.55 |
| transfer__C-Federation-THSWPA__E_plus_federation__mlp__s42 | transfer | C:Federation=THSWPA | E_plus_federation | mlp | 42 | 161954 | 51585 | 35121 | 4.53 | 14.69 |
| transfer__C-Federation-USAPL__A_squat__ratio | transfer | C:Federation=USAPL | A_squat | ratio | 42 | 161436 | 49455 | 35225 | 0.35 | 21.61 |
| transfer__C-Federation-USAPL__D_plus_equipment__lightgbm | transfer | C:Federation=USAPL | D_plus_equipment | lightgbm | 42 | 161436 | 49455 | 35225 | 3.70 | 14.32 |
| transfer__C-Federation-USAPL__D_plus_equipment__linear | transfer | C:Federation=USAPL | D_plus_equipment | linear | 42 | 161436 | 49455 | 35225 | 0.54 | 15.42 |
| transfer__C-Federation-USAPL__E_plus_federation__lightgbm | transfer | C:Federation=USAPL | E_plus_federation | lightgbm | 42 | 161436 | 49455 | 35225 | 3.45 | 14.12 |
| transfer__C-Federation-USAPL__E_plus_federation__linear | transfer | C:Federation=USAPL | E_plus_federation | linear | 42 | 161436 | 49455 | 35225 | 0.95 | 14.81 |
| transfer__C-Federation-USAPL__E_plus_federation__mlp__s42 | transfer | C:Federation=USAPL | E_plus_federation | mlp | 42 | 161436 | 49455 | 35225 | 3.85 | 14.02 |

