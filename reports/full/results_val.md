# Results — full (VALIDATION only)

MAE in kg with 95% lifter-bootstrap CI. All rows within a comparison are identical across models.

## ablation_core — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| ablation · A · A_squat · ratio | ratio | A_squat | 390871 | 118377 | 21.98 | 21.85 | 22.11 | 21.70 | 12.38 | 0.77 |
| ablation · A · A_squat · linear | linear | A_squat | 390871 | 118377 | 19.55 | 19.42 | 19.64 | 18.60 | 11.54 | 0.82 |
| ablation · A · B_squat_bench · linear | linear | B_squat_bench | 390871 | 118377 | 18.24 | 18.11 | 18.33 | 17.22 | 10.73 | 0.84 |
| ablation · A · C_plus_demographics · linear | linear | C_plus_demographics | 390871 | 118377 | 16.85 | 16.74 | 16.94 | 16.47 | 9.91 | 0.86 |
| ablation · A · D_plus_equipment · linear | linear | D_plus_equipment | 390871 | 118377 | 15.46 | 15.35 | 15.55 | 15.36 | 9.19 | 0.88 |
| ablation · A · A_squat · lightgbm | lightgbm | A_squat | 390871 | 118377 | 17.13 | 17.03 | 17.21 | 16.80 | 10.06 | 0.86 |
| ablation · A · B_squat_bench · lightgbm | lightgbm | B_squat_bench | 390871 | 118377 | 15.84 | 15.74 | 15.92 | 15.33 | 9.22 | 0.88 |
| ablation · A · C_plus_demographics · lightgbm | lightgbm | C_plus_demographics | 390871 | 118377 | 14.69 | 14.60 | 14.77 | 14.51 | 8.54 | 0.89 |
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 390871 | 118377 | 14.10 | 14.01 | 14.18 | 14.02 | 8.25 | 0.90 |
| ablation · A · A_squat · mlp · s42 | mlp | A_squat | 390871 | 118377 | 18.65 | 18.55 | 18.75 | 17.70 | 10.94 | 0.84 |
| ablation · A · B_squat_bench · mlp · s42 | mlp | B_squat_bench | 390871 | 118377 | 17.08 | 16.98 | 17.17 | 16.10 | 9.94 | 0.86 |
| ablation · A · C_plus_demographics · mlp · s42 | mlp | C_plus_demographics | 390871 | 118377 | 15.35 | 15.26 | 15.43 | 15.15 | 8.92 | 0.89 |
| ablation · A · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 390871 | 118377 | 14.32 | 14.22 | 14.40 | 14.24 | 8.32 | 0.90 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | ablation · A · B_squat_bench · linear | ablation · A · A_squat · linear | 390871 | 118377 | -1.31 | -1.36 | -1.27 |
| val | ablation · A · C_plus_demographics · linear | ablation · A · B_squat_bench · linear | 390871 | 118377 | -1.38 | -1.43 | -1.32 |
| val | ablation · A · D_plus_equipment · linear | ablation · A · C_plus_demographics · linear | 390871 | 118377 | -1.39 | -1.44 | -1.35 |
| val | ablation · A · D_plus_equipment · linear | ablation · A · A_squat · ratio | 390871 | 118377 | -6.52 | -6.63 | -6.41 |
| val | ablation · A · B_squat_bench · lightgbm | ablation · A · A_squat · lightgbm | 390871 | 118377 | -1.29 | -1.35 | -1.25 |
| val | ablation · A · C_plus_demographics · lightgbm | ablation · A · B_squat_bench · lightgbm | 390871 | 118377 | -1.15 | -1.20 | -1.10 |
| val | ablation · A · D_plus_equipment · lightgbm | ablation · A · C_plus_demographics · lightgbm | 390871 | 118377 | -0.59 | -0.62 | -0.56 |
| val | ablation · A · D_plus_equipment · lightgbm | ablation · A · A_squat · ratio | 390871 | 118377 | -7.88 | -7.99 | -7.76 |
| val | ablation · A · B_squat_bench · mlp · s42 | ablation · A · A_squat · mlp · s42 | 390871 | 118377 | -1.57 | -1.63 | -1.52 |
| val | ablation · A · C_plus_demographics · mlp · s42 | ablation · A · B_squat_bench · mlp · s42 | 390871 | 118377 | -1.73 | -1.80 | -1.67 |
| val | ablation · A · D_plus_equipment · mlp · s42 | ablation · A · C_plus_demographics · mlp · s42 | 390871 | 118377 | -1.03 | -1.07 | -0.99 |
| val | ablation · A · D_plus_equipment · mlp · s42 | ablation · A · A_squat · ratio | 390871 | 118377 | -7.66 | -7.77 | -7.54 |

## ablation_federation_extension — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| ablation · A · D_plus_equipment · linear | linear | D_plus_equipment | 390871 | 118377 | 15.46 | 15.35 | 15.55 | 15.36 | 9.19 | 0.88 |
| ablation · A · E_plus_federation · linear | linear | E_plus_federation | 390871 | 118377 | 14.92 | 14.83 | 15.00 | 14.81 | 8.87 | 0.89 |
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 390871 | 118377 | 14.10 | 14.01 | 14.18 | 14.02 | 8.25 | 0.90 |
| ablation · A · E_plus_federation · lightgbm | lightgbm | E_plus_federation | 390871 | 118377 | 13.87 | 13.79 | 13.94 | 13.74 | 8.12 | 0.90 |
| ablation · A · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 390871 | 118377 | 14.32 | 14.22 | 14.40 | 14.24 | 8.32 | 0.90 |
| ablation · A · E_plus_federation · mlp · s42 | mlp | E_plus_federation | 390871 | 118377 | 13.88 | 13.80 | 13.96 | 13.73 | 8.10 | 0.90 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | ablation · A · E_plus_federation · linear | ablation · A · D_plus_equipment · linear | 390871 | 118377 | -0.54 | -0.57 | -0.52 |
| val | ablation · A · E_plus_federation · lightgbm | ablation · A · D_plus_equipment · lightgbm | 390871 | 118377 | -0.24 | -0.25 | -0.21 |
| val | ablation · A · E_plus_federation · mlp · s42 | ablation · A · D_plus_equipment · mlp · s42 | 390871 | 118377 | -0.44 | -0.47 | -0.41 |

## models_D — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| ablation · A · A_squat · ratio | ratio | A_squat | 390871 | 118377 | 21.98 | 21.85 | 22.11 | 21.70 | 12.38 | 0.77 |
| ablation · A · D_plus_equipment · linear | linear | D_plus_equipment | 390871 | 118377 | 15.46 | 15.35 | 15.55 | 15.36 | 9.19 | 0.88 |
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 390871 | 118377 | 14.10 | 14.01 | 14.18 | 14.02 | 8.25 | 0.90 |
| ablation · A · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 390871 | 118377 | 14.32 | 14.22 | 14.40 | 14.24 | 8.32 | 0.90 |
| ablation · A · D_plus_equipment · mlp · s43 | mlp | D_plus_equipment | 390871 | 118377 | 14.32 | 14.23 | 14.40 | 14.24 | 8.34 | 0.90 |
| ablation · A · D_plus_equipment · mlp · s44 | mlp | D_plus_equipment | 390871 | 118377 | 14.33 | 14.24 | 14.41 | 14.28 | 8.33 | 0.90 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | ablation · A · D_plus_equipment · lightgbm | ablation · A · D_plus_equipment · linear | 390871 | 118377 | -1.36 | -1.40 | -1.31 |
| val | ablation · A · D_plus_equipment · lightgbm | ablation · A · A_squat · ratio | 390871 | 118377 | -7.88 | -7.99 | -7.76 |
| val | ablation · A · D_plus_equipment · mlp · s42 | ablation · A · D_plus_equipment · lightgbm | 390871 | 118377 | 0.22 | 0.20 | 0.24 |
| val | ablation · A · D_plus_equipment · mlp · s43 | ablation · A · D_plus_equipment · lightgbm | 390871 | 118377 | 0.22 | 0.20 | 0.24 |
| val | ablation · A · D_plus_equipment · mlp · s44 | ablation · A · D_plus_equipment · lightgbm | 390871 | 118377 | 0.23 | 0.21 | 0.25 |

## history_eligible — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| history · A · D_plus_equipment · last_deadlift · histrows | last_deadlift | D_plus_equipment | 272140 | 64848 | 13.45 | 13.35 | 13.57 | 13.99 | 7.87 | 0.86 |
| ablation · A · D_plus_equipment · linear | linear | D_plus_equipment | 272140 | 64848 | 15.57 | 15.44 | 15.68 | 15.20 | 8.80 | 0.88 |
| history · A · D_plus_equipment · linear · histrows | linear | D_plus_equipment | 272140 | 64848 | 15.59 | 15.47 | 15.71 | 15.33 | 8.89 | 0.88 |
| history · A · D_plus_equipment-history · linear · histrows | linear | D_plus_equipment+history | 272140 | 64848 | 9.89 | 9.82 | 9.97 | 9.73 | 5.75 | 0.94 |
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 272140 | 64848 | 14.24 | 14.13 | 14.35 | 14.00 | 7.99 | 0.90 |
| history · A · D_plus_equipment · lightgbm · histrows | lightgbm | D_plus_equipment | 272140 | 64848 | 14.25 | 14.14 | 14.35 | 14.05 | 8.03 | 0.90 |
| history · A · D_plus_equipment-history · lightgbm · histrows | lightgbm | D_plus_equipment+history | 272140 | 64848 | 8.78 | 8.72 | 8.83 | 8.82 | 5.09 | 0.95 |
| ablation · A · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 272140 | 64848 | 14.45 | 14.34 | 14.56 | 14.18 | 8.07 | 0.90 |
| history · A · D_plus_equipment-history · mlp · histrows · s42 | mlp | D_plus_equipment+history | 272140 | 64848 | 8.77 | 8.72 | 8.83 | 8.81 | 5.10 | 0.95 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | history · A · D_plus_equipment-history · linear · histrows | ablation · A · D_plus_equipment · linear | 272140 | 64848 | -5.68 | -5.77 | -5.59 |
| val | history · A · D_plus_equipment-history · linear · histrows | history · A · D_plus_equipment · linear · histrows | 272140 | 64848 | -5.70 | -5.78 | -5.61 |
| val | history · A · D_plus_equipment-history · linear · histrows | history · A · D_plus_equipment · last_deadlift · histrows | 272140 | 64848 | -3.55 | -3.64 | -3.48 |
| val | history · A · D_plus_equipment-history · lightgbm · histrows | ablation · A · D_plus_equipment · lightgbm | 272140 | 64848 | -5.46 | -5.56 | -5.38 |
| val | history · A · D_plus_equipment-history · lightgbm · histrows | history · A · D_plus_equipment · lightgbm · histrows | 272140 | 64848 | -5.47 | -5.57 | -5.38 |
| val | history · A · D_plus_equipment-history · lightgbm · histrows | history · A · D_plus_equipment · last_deadlift · histrows | 272140 | 64848 | -4.67 | -4.76 | -4.58 |
| val | history · A · D_plus_equipment-history · mlp · histrows · s42 | ablation · A · D_plus_equipment · mlp · s42 | 272140 | 64848 | -5.68 | -5.78 | -5.60 |
| val | history · A · D_plus_equipment-history · mlp · histrows · s42 | history · A · D_plus_equipment · last_deadlift · histrows | 272140 | 64848 | -4.68 | -4.77 | -4.59 |

## no_history_rows — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| ablation · A · A_squat · ratio | ratio | A_squat | 118731 | 118377 | 21.43 | 21.32 | 21.53 | 21.43 | 13.05 | 0.76 |
| ablation · A · D_plus_equipment · linear | linear | D_plus_equipment | 118731 | 118377 | 15.21 | 15.14 | 15.30 | 15.20 | 10.08 | 0.88 |
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 118731 | 118377 | 13.79 | 13.72 | 13.86 | 13.78 | 8.83 | 0.90 |
| ablation · A · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 118731 | 118377 | 14.02 | 13.95 | 14.09 | 14.01 | 8.90 | 0.89 |

## chrono_all — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| chrono · B · A_squat · ratio | ratio | A_squat | 391938 | 181332 | 21.25 | 21.16 | 21.35 | 21.81 | 12.28 | 0.78 |
| chrono · B · D_plus_equipment · linear | linear | D_plus_equipment | 391938 | 181332 | 14.60 | 14.53 | 14.67 | 14.94 | 8.87 | 0.89 |
| chrono · B · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 391938 | 181332 | 13.61 | 13.55 | 13.66 | 14.04 | 8.17 | 0.91 |
| chrono · B · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 391938 | 181332 | 13.60 | 13.54 | 13.65 | 14.03 | 8.16 | 0.91 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | chrono · B · D_plus_equipment · lightgbm | chrono · B · A_squat · ratio | 391938 | 181332 | -7.65 | -7.72 | -7.57 |
| val | chrono · B · D_plus_equipment · lightgbm | chrono · B · D_plus_equipment · linear | 391938 | 181332 | -0.99 | -1.03 | -0.95 |
| val | chrono · B · D_plus_equipment · mlp · s42 | chrono · B · D_plus_equipment · lightgbm | 391938 | 181332 | -0.01 | -0.02 | 0.00 |

## chrono_history_eligible — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| chrono · B · D_plus_equipment · last_deadlift · histrows | last_deadlift | D_plus_equipment | 279563 | 116639 | 12.60 | 12.51 | 12.69 | 13.90 | 7.60 | 0.87 |
| chrono · B · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 279563 | 116639 | 13.67 | 13.59 | 13.74 | 14.12 | 7.96 | 0.91 |
| chrono · B · D_plus_equipment · lightgbm · histrows | lightgbm | D_plus_equipment | 279563 | 116639 | 13.65 | 13.57 | 13.72 | 14.13 | 7.97 | 0.91 |
| chrono · B · D_plus_equipment-history · lightgbm · histrows | lightgbm | D_plus_equipment+history | 279563 | 116639 | 8.29 | 8.25 | 8.33 | 8.81 | 5.01 | 0.96 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | chrono · B · D_plus_equipment-history · lightgbm · histrows | chrono · B · D_plus_equipment · lightgbm · histrows | 279563 | 116639 | -5.36 | -5.42 | -5.30 |
| val | chrono · B · D_plus_equipment-history · lightgbm · histrows | chrono · B · D_plus_equipment · last_deadlift · histrows | 279563 | 116639 | -4.31 | -4.37 | -4.25 |
| val | chrono · B · D_plus_equipment-history · lightgbm · histrows | chrono · B · D_plus_equipment · lightgbm | 279563 | 116639 | -5.38 | -5.44 | -5.32 |

## transfer|Equipment=Single-ply — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Equipment-Single-ply · A_squat · ratio | ratio | A_squat | 241225 | 83034 | 21.73 | 21.56 | 21.92 | 20.97 | 12.23 | 0.77 |
| transfer · C-Equipment-Single-ply · D_plus_equipment · linear | linear | D_plus_equipment | 241225 | 83034 | 15.40 | 15.29 | 15.51 | 15.28 | 9.18 | 0.89 |
| transfer · C-Equipment-Single-ply · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 241225 | 83034 | 14.22 | 14.13 | 14.33 | 14.14 | 8.29 | 0.90 |
| transfer · C-Equipment-Single-ply · C_plus_demographics · linear | linear | C_plus_demographics | 241225 | 83034 | 16.82 | 16.70 | 16.94 | 16.36 | 9.92 | 0.86 |
| transfer · C-Equipment-Single-ply · C_plus_demographics · lightgbm | lightgbm | C_plus_demographics | 241225 | 83034 | 14.81 | 14.71 | 14.91 | 14.64 | 8.59 | 0.89 |
| transfer · C-Equipment-Single-ply · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 241225 | 83034 | 14.23 | 14.13 | 14.33 | 14.14 | 8.26 | 0.90 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | transfer · C-Equipment-Single-ply · D_plus_equipment · lightgbm | transfer · C-Equipment-Single-ply · C_plus_demographics · lightgbm | 241225 | 83034 | -0.59 | -0.63 | -0.55 |
| val | transfer · C-Equipment-Single-ply · D_plus_equipment · lightgbm | transfer · C-Equipment-Single-ply · A_squat · ratio | 241225 | 83034 | -7.51 | -7.69 | -7.37 |

## transfer|Equipment=Unlimited — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Equipment-Unlimited · A_squat · ratio | ratio | A_squat | 350255 | 111372 | 22.21 | 22.06 | 22.38 | 21.66 | 12.21 | 0.76 |
| transfer · C-Equipment-Unlimited · D_plus_equipment · linear | linear | D_plus_equipment | 350255 | 111372 | 15.75 | 15.65 | 15.85 | 15.51 | 9.15 | 0.88 |
| transfer · C-Equipment-Unlimited · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 350255 | 111372 | 14.43 | 14.34 | 14.52 | 14.20 | 8.24 | 0.90 |
| transfer · C-Equipment-Unlimited · C_plus_demographics · linear | linear | C_plus_demographics | 350255 | 111372 | 17.08 | 16.97 | 17.19 | 16.47 | 9.85 | 0.86 |
| transfer · C-Equipment-Unlimited · C_plus_demographics · lightgbm | lightgbm | C_plus_demographics | 350255 | 111372 | 15.01 | 14.93 | 15.11 | 14.65 | 8.53 | 0.89 |
| transfer · C-Equipment-Unlimited · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 350255 | 111372 | 14.66 | 14.57 | 14.76 | 14.44 | 8.32 | 0.89 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | transfer · C-Equipment-Unlimited · D_plus_equipment · lightgbm | transfer · C-Equipment-Unlimited · C_plus_demographics · lightgbm | 350255 | 111372 | -0.58 | -0.62 | -0.55 |
| val | transfer · C-Equipment-Unlimited · D_plus_equipment · lightgbm | transfer · C-Equipment-Unlimited · A_squat · ratio | 350255 | 111372 | -7.78 | -7.91 | -7.63 |

## transfer|Equipment=Wraps — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Equipment-Wraps · A_squat · ratio | ratio | A_squat | 359626 | 109844 | 21.92 | 21.78 | 22.07 | 21.76 | 12.43 | 0.77 |
| transfer · C-Equipment-Wraps · D_plus_equipment · linear | linear | D_plus_equipment | 359626 | 109844 | 15.36 | 15.29 | 15.46 | 15.33 | 9.19 | 0.88 |
| transfer · C-Equipment-Wraps · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 359626 | 109844 | 13.95 | 13.87 | 14.04 | 13.92 | 8.22 | 0.90 |
| transfer · C-Equipment-Wraps · C_plus_demographics · linear | linear | C_plus_demographics | 359626 | 109844 | 16.81 | 16.71 | 16.92 | 16.51 | 9.94 | 0.86 |
| transfer · C-Equipment-Wraps · C_plus_demographics · lightgbm | lightgbm | C_plus_demographics | 359626 | 109844 | 14.51 | 14.43 | 14.61 | 14.39 | 8.50 | 0.90 |
| transfer · C-Equipment-Wraps · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 359626 | 109844 | 14.19 | 14.11 | 14.28 | 14.19 | 8.33 | 0.90 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | transfer · C-Equipment-Wraps · D_plus_equipment · lightgbm | transfer · C-Equipment-Wraps · C_plus_demographics · lightgbm | 359626 | 109844 | -0.56 | -0.59 | -0.53 |
| val | transfer · C-Equipment-Wraps · D_plus_equipment · lightgbm | transfer · C-Equipment-Wraps · A_squat · ratio | 359626 | 109844 | -7.98 | -8.10 | -7.85 |

## transfer|Equipment=Multi-ply — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Equipment-Multi-ply · A_squat · ratio | ratio | A_squat | 383325 | 116932 | 21.35 | 21.21 | 21.49 | 21.14 | 12.15 | 0.78 |
| transfer · C-Equipment-Multi-ply · D_plus_equipment · linear | linear | D_plus_equipment | 383325 | 116932 | 15.23 | 15.13 | 15.32 | 15.17 | 9.08 | 0.89 |
| transfer · C-Equipment-Multi-ply · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 383325 | 116932 | 14.00 | 13.91 | 14.09 | 13.96 | 8.21 | 0.90 |
| transfer · C-Equipment-Multi-ply · C_plus_demographics · linear | linear | C_plus_demographics | 383325 | 116932 | 16.48 | 16.38 | 16.60 | 16.19 | 9.73 | 0.87 |
| transfer · C-Equipment-Multi-ply · C_plus_demographics · lightgbm | lightgbm | C_plus_demographics | 383325 | 116932 | 14.51 | 14.42 | 14.60 | 14.41 | 8.48 | 0.90 |
| transfer · C-Equipment-Multi-ply · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 383325 | 116932 | 14.22 | 14.14 | 14.32 | 14.21 | 8.32 | 0.90 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | transfer · C-Equipment-Multi-ply · D_plus_equipment · lightgbm | transfer · C-Equipment-Multi-ply · C_plus_demographics · lightgbm | 383325 | 116932 | -0.51 | -0.54 | -0.48 |
| val | transfer · C-Equipment-Multi-ply · D_plus_equipment · lightgbm | transfer · C-Equipment-Multi-ply · A_squat · ratio | 383325 | 116932 | -7.36 | -7.46 | -7.25 |

## transfer|Federation=THSPA — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Federation-THSPA · A_squat · ratio | ratio | A_squat | 321327 | 103194 | 22.16 | 21.98 | 22.31 | 21.66 | 12.46 | 0.79 |
| transfer · C-Federation-THSPA · E_plus_federation · linear | linear | E_plus_federation | 321327 | 103194 | 15.12 | 15.01 | 15.22 | 14.98 | 8.98 | 0.90 |
| transfer · C-Federation-THSPA · E_plus_federation · lightgbm | lightgbm | E_plus_federation | 321327 | 103194 | 14.01 | 13.92 | 14.11 | 13.86 | 8.18 | 0.91 |
| transfer · C-Federation-THSPA · D_plus_equipment · linear | linear | D_plus_equipment | 321327 | 103194 | 15.44 | 15.32 | 15.54 | 15.29 | 9.20 | 0.89 |
| transfer · C-Federation-THSPA · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 321327 | 103194 | 14.23 | 14.13 | 14.32 | 14.12 | 8.31 | 0.91 |
| transfer · C-Federation-THSPA · E_plus_federation · mlp · s42 | mlp | E_plus_federation | 321327 | 103194 | 14.04 | 13.95 | 14.15 | 13.86 | 8.15 | 0.91 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | transfer · C-Federation-THSPA · E_plus_federation · lightgbm | transfer · C-Federation-THSPA · D_plus_equipment · lightgbm | 321327 | 103194 | -0.21 | -0.23 | -0.19 |
| val | transfer · C-Federation-THSPA · E_plus_federation · lightgbm | transfer · C-Federation-THSPA · A_squat · ratio | 321327 | 103194 | -8.14 | -8.27 | -7.99 |

## transfer|Federation=USAPL — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Federation-USAPL · A_squat · ratio | ratio | A_squat | 347247 | 106099 | 22.06 | 21.91 | 22.23 | 21.97 | 12.44 | 0.77 |
| transfer · C-Federation-USAPL · E_plus_federation · linear | linear | E_plus_federation | 347247 | 106099 | 14.87 | 14.79 | 14.96 | 14.84 | 8.86 | 0.89 |
| transfer · C-Federation-USAPL · E_plus_federation · lightgbm | lightgbm | E_plus_federation | 347247 | 106099 | 13.83 | 13.74 | 13.91 | 13.75 | 8.11 | 0.91 |
| transfer · C-Federation-USAPL · D_plus_equipment · linear | linear | D_plus_equipment | 347247 | 106099 | 15.48 | 15.39 | 15.58 | 15.45 | 9.20 | 0.88 |
| transfer · C-Federation-USAPL · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 347247 | 106099 | 14.08 | 13.99 | 14.16 | 14.05 | 8.25 | 0.90 |
| transfer · C-Federation-USAPL · E_plus_federation · mlp · s42 | mlp | E_plus_federation | 347247 | 106099 | 13.84 | 13.76 | 13.92 | 13.78 | 8.13 | 0.91 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | transfer · C-Federation-USAPL · E_plus_federation · lightgbm | transfer · C-Federation-USAPL · D_plus_equipment · lightgbm | 347247 | 106099 | -0.25 | -0.27 | -0.22 |
| val | transfer · C-Federation-USAPL · E_plus_federation · lightgbm | transfer · C-Federation-USAPL · A_squat · ratio | 347247 | 106099 | -8.23 | -8.35 | -8.10 |

## transfer|Federation=THSWPA — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| transfer · C-Federation-THSWPA · A_squat · ratio | ratio | A_squat | 347919 | 110504 | 22.69 | 22.53 | 22.84 | 22.01 | 12.13 | 0.73 |
| transfer · C-Federation-THSWPA · E_plus_federation · linear | linear | E_plus_federation | 347919 | 110504 | 15.58 | 15.47 | 15.68 | 15.20 | 8.85 | 0.87 |
| transfer · C-Federation-THSWPA · E_plus_federation · lightgbm | lightgbm | E_plus_federation | 347919 | 110504 | 14.47 | 14.39 | 14.56 | 14.09 | 8.06 | 0.89 |
| transfer · C-Federation-THSWPA · D_plus_equipment · linear | linear | D_plus_equipment | 347919 | 110504 | 16.13 | 16.02 | 16.23 | 15.74 | 9.16 | 0.86 |
| transfer · C-Federation-THSWPA · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 347919 | 110504 | 14.71 | 14.63 | 14.81 | 14.37 | 8.19 | 0.88 |
| transfer · C-Federation-THSWPA · E_plus_federation · mlp · s42 | mlp | E_plus_federation | 347919 | 110504 | 14.47 | 14.39 | 14.56 | 14.09 | 8.06 | 0.89 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | transfer · C-Federation-THSWPA · E_plus_federation · lightgbm | transfer · C-Federation-THSWPA · D_plus_equipment · lightgbm | 347919 | 110504 | -0.24 | -0.27 | -0.23 |
| val | transfer · C-Federation-THSWPA · E_plus_federation · lightgbm | transfer · C-Federation-THSWPA · A_squat · ratio | 347919 | 110504 | -8.22 | -8.36 | -8.10 |

## capacity_D — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| ablation · A · D_plus_equipment · lightgbm | lightgbm | D_plus_equipment | 390871 | 118377 | 14.10 | 14.01 | 14.18 | 14.02 | 8.25 | 0.90 |
| capacity · A · D_plus_equipment · lightgbm · lgbm_big | lightgbm | D_plus_equipment | 390871 | 118377 | 14.10 | 14.01 | 14.18 | 14.02 | 8.24 | 0.90 |
| ablation · A · D_plus_equipment · mlp · s42 | mlp | D_plus_equipment | 390871 | 118377 | 14.32 | 14.22 | 14.40 | 14.24 | 8.32 | 0.90 |
| capacity · A · D_plus_equipment · mlp · mlp_wide · s42 | mlp | D_plus_equipment | 390871 | 118377 | 14.34 | 14.25 | 14.42 | 14.28 | 8.34 | 0.90 |
| capacity · A · D_plus_equipment · mlp · mlp_deep · s42 | mlp | D_plus_equipment | 390871 | 118377 | 14.31 | 14.22 | 14.39 | 14.26 | 8.33 | 0.90 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | capacity · A · D_plus_equipment · lightgbm · lgbm_big | ablation · A · D_plus_equipment · lightgbm | 390871 | 118377 | -0.00 | -0.01 | 0.00 |
| val | capacity · A · D_plus_equipment · mlp · mlp_wide · s42 | ablation · A · D_plus_equipment · mlp · s42 | 390871 | 118377 | 0.02 | 0.01 | 0.03 |
| val | capacity · A · D_plus_equipment · mlp · mlp_deep · s42 | ablation · A · D_plus_equipment · mlp · s42 | 390871 | 118377 | -0.01 | -0.02 | 0.00 |

## capacity_D_history — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| history · A · D_plus_equipment-history · lightgbm · histrows | lightgbm | D_plus_equipment+history | 272140 | 64848 | 8.78 | 8.72 | 8.83 | 8.82 | 5.09 | 0.95 |
| capacity · A · D_plus_equipment-history · lightgbm · histrows · lgbm_big | lightgbm | D_plus_equipment+history | 272140 | 64848 | 8.75 | 8.70 | 8.81 | 8.80 | 5.08 | 0.95 |
| history · A · D_plus_equipment-history · mlp · histrows · s42 | mlp | D_plus_equipment+history | 272140 | 64848 | 8.77 | 8.72 | 8.83 | 8.81 | 5.10 | 0.95 |
| capacity · A · D_plus_equipment-history · mlp · histrows · mlp_wide · s42 | mlp | D_plus_equipment+history | 272140 | 64848 | 8.74 | 8.68 | 8.79 | 8.77 | 5.09 | 0.95 |
| capacity · A · D_plus_equipment-history · mlp · histrows · mlp_deep · s42 | mlp | D_plus_equipment+history | 272140 | 64848 | 8.74 | 8.69 | 8.80 | 8.78 | 5.07 | 0.95 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | capacity · A · D_plus_equipment-history · lightgbm · histrows · lgbm_big | history · A · D_plus_equipment-history · lightgbm · histrows | 272140 | 64848 | -0.02 | -0.03 | -0.02 |
| val | capacity · A · D_plus_equipment-history · mlp · histrows · mlp_wide · s42 | history · A · D_plus_equipment-history · mlp · histrows · s42 | 272140 | 64848 | -0.03 | -0.04 | -0.03 |
| val | capacity · A · D_plus_equipment-history · mlp · histrows · mlp_deep · s42 | history · A · D_plus_equipment-history · mlp · histrows · s42 | 272140 | 64848 | -0.03 | -0.04 | -0.02 |

## history_rich_A — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| history · A · D_plus_equipment · last_deadlift · histrows | last_deadlift | D_plus_equipment | 272140 | 64848 | 13.45 | 13.35 | 13.57 | 13.99 | 7.87 | 0.86 |
| history · A · D_plus_equipment-history · lightgbm · histrows | lightgbm | D_plus_equipment+history | 272140 | 64848 | 8.78 | 8.72 | 8.83 | 8.82 | 5.09 | 0.95 |
| history · A · D_plus_equipment-history · mlp · histrows · s42 | mlp | D_plus_equipment+history | 272140 | 64848 | 8.77 | 8.72 | 8.83 | 8.81 | 5.10 | 0.95 |
| history_rich · A · D_plus_equipment-history_rich · lightgbm · histrows | lightgbm | D_plus_equipment+history_rich | 272140 | 64848 | 8.46 | 8.42 | 8.52 | 8.65 | 4.94 | 0.96 |
| history_rich · A · D_plus_equipment-history_rich · mlp · histrows · s42 | mlp | D_plus_equipment+history_rich | 272140 | 64848 | 8.42 | 8.37 | 8.48 | 8.64 | 4.92 | 0.95 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | history_rich · A · D_plus_equipment-history_rich · lightgbm · histrows | history · A · D_plus_equipment-history · lightgbm · histrows | 272140 | 64848 | -0.31 | -0.33 | -0.30 |
| val | history_rich · A · D_plus_equipment-history_rich · mlp · histrows · s42 | history · A · D_plus_equipment-history · mlp · histrows · s42 | 272140 | 64848 | -0.35 | -0.36 | -0.33 |
| val | history_rich · A · D_plus_equipment-history_rich · lightgbm · histrows | history · A · D_plus_equipment · last_deadlift · histrows | 272140 | 64848 | -4.98 | -5.07 | -4.90 |
| val | history_rich · A · D_plus_equipment-history_rich · mlp · histrows · s42 | history_rich · A · D_plus_equipment-history_rich · lightgbm · histrows | 272140 | 64848 | -0.04 | -0.05 | -0.02 |

## history_rich_B — partition `val`

| label | model | feature_set | rows | lifters | mae | mae_ci_low | mae_ci_high | lifter_avg_mae | mape | r2 |
|---|---|---|---|---|---|---|---|---|---|---|
| chrono · B · D_plus_equipment · last_deadlift · histrows | last_deadlift | D_plus_equipment | 279563 | 116639 | 12.60 | 12.51 | 12.69 | 13.90 | 7.60 | 0.87 |
| chrono · B · D_plus_equipment-history · lightgbm · histrows | lightgbm | D_plus_equipment+history | 279563 | 116639 | 8.29 | 8.25 | 8.33 | 8.81 | 5.01 | 0.96 |
| history_rich · B · D_plus_equipment-history_rich · lightgbm · histrows | lightgbm | D_plus_equipment+history_rich | 279563 | 116639 | 8.00 | 7.96 | 8.04 | 8.58 | 4.87 | 0.96 |

Paired MAE differences (a − b; negative = a better):

| partition | a | b | rows | lifters | mae_diff_a_minus_b | ci_low | ci_high |
|---|---|---|---|---|---|---|---|
| val | history_rich · B · D_plus_equipment-history_rich · lightgbm · histrows | chrono · B · D_plus_equipment-history · lightgbm · histrows | 279563 | 116639 | -0.29 | -0.30 | -0.28 |
| val | history_rich · B · D_plus_equipment-history_rich · lightgbm · histrows | chrono · B · D_plus_equipment · last_deadlift · histrows | 279563 | 116639 | -4.60 | -4.66 | -4.54 |

## Subgroups (protocol A, feature set D; protocol B LightGBM)

| run_id | group_by | group | rows | lifters | mae | mape | r2 | sparse |
|---|---|---|---|---|---|---|---|---|
| ablation · A · A_squat · ratio | Sex | F | 121389 | 34677 | 16.56 | 13.31 | 0.54 | False |
| ablation · A · A_squat · ratio | Sex | M | 269445 | 83885 | 24.43 | 11.97 | 0.62 | False |
| ablation · A · A_squat · ratio | Sex | Mx | 37 | 19 | 13.08 | 9.02 | 0.79 | True |
| ablation · A · A_squat · ratio | bw_bin | 0-60 | 65239 | 21139 | 15.48 | 12.92 | 0.68 | False |
| ablation · A · A_squat · ratio | bw_bin | 105-120 | 34725 | 13870 | 26.79 | 12.54 | 0.61 | False |
| ablation · A · A_squat · ratio | bw_bin | 120-1000 | 25370 | 8511 | 33.46 | 15.17 | 0.40 | False |
| ablation · A · A_squat · ratio | bw_bin | 60-75 | 99847 | 38036 | 19.68 | 12.39 | 0.69 | False |
| ablation · A · A_squat · ratio | bw_bin | 75-90 | 95716 | 38733 | 22.32 | 11.73 | 0.67 | False |
| ablation · A · A_squat · ratio | bw_bin | 90-105 | 67882 | 27331 | 24.16 | 11.56 | 0.65 | False |
| ablation · A · A_squat · ratio | bw_bin | missing | 2092 | 1280 | 30.35 | 15.61 | 0.64 | False |
| ablation · A · A_squat · ratio | has_history | False | 118731 | 118377 | 21.43 | 13.05 | 0.76 | False |
| ablation · A · A_squat · ratio | has_history | True | 272140 | 64848 | 22.23 | 12.09 | 0.76 | False |
| ablation · A · A_squat · ratio | Equipment | Multi-ply | 7546 | 3005 | 47.57 | 21.07 | -0.02 | False |
| ablation · A · A_squat · ratio | Equipment | Raw | 161818 | 63150 | 22.81 | 12.57 | 0.76 | False |
| ablation · A · A_squat · ratio | Equipment | Single-ply | 149646 | 44851 | 20.53 | 11.67 | 0.78 | False |
| ablation · A · A_squat · ratio | Equipment | Unlimited | 40616 | 9590 | 18.59 | 12.93 | 0.70 | False |
| ablation · A · A_squat · ratio | Equipment | Wraps | 31245 | 15145 | 22.91 | 12.01 | 0.76 | False |
| ablation · A · D_plus_equipment · linear | Sex | F | 121389 | 34677 | 11.37 | 9.64 | 0.79 | False |
| ablation · A · D_plus_equipment · linear | Sex | M | 269445 | 83885 | 17.30 | 8.98 | 0.80 | False |
| ablation · A · D_plus_equipment · linear | Sex | Mx | 37 | 19 | 11.04 | 8.50 | 0.88 | True |
| ablation · A · D_plus_equipment · linear | bw_bin | 0-60 | 65239 | 21139 | 12.11 | 11.20 | 0.80 | False |
| ablation · A · D_plus_equipment · linear | bw_bin | 105-120 | 34725 | 13870 | 18.64 | 8.95 | 0.81 | False |
| ablation · A · D_plus_equipment · linear | bw_bin | 120-1000 | 25370 | 8511 | 21.78 | 10.29 | 0.75 | False |
| ablation · A · D_plus_equipment · linear | bw_bin | 60-75 | 99847 | 38036 | 13.41 | 8.89 | 0.85 | False |
| ablation · A · D_plus_equipment · linear | bw_bin | 75-90 | 95716 | 38733 | 15.47 | 8.32 | 0.83 | False |
| ablation · A · D_plus_equipment · linear | bw_bin | 90-105 | 67882 | 27331 | 17.53 | 8.53 | 0.81 | False |
| ablation · A · D_plus_equipment · linear | bw_bin | missing | 2092 | 1280 | 21.06 | 12.25 | 0.83 | False |
| ablation · A · D_plus_equipment · linear | has_history | False | 118731 | 118377 | 15.21 | 10.08 | 0.88 | False |
| ablation · A · D_plus_equipment · linear | has_history | True | 272140 | 64848 | 15.57 | 8.80 | 0.88 | False |
| ablation · A · D_plus_equipment · linear | Equipment | Multi-ply | 7546 | 3005 | 25.65 | 12.29 | 0.69 | False |
| ablation · A · D_plus_equipment · linear | Equipment | Raw | 161818 | 63150 | 15.49 | 9.21 | 0.88 | False |
| ablation · A · D_plus_equipment · linear | Equipment | Single-ply | 149646 | 44851 | 15.45 | 9.05 | 0.88 | False |
| ablation · A · D_plus_equipment · linear | Equipment | Unlimited | 40616 | 9590 | 12.62 | 9.08 | 0.87 | False |
| ablation · A · D_plus_equipment · linear | Equipment | Wraps | 31245 | 15145 | 16.60 | 9.11 | 0.87 | False |
| ablation · A · D_plus_equipment · lightgbm | Sex | F | 121389 | 34677 | 10.40 | 8.68 | 0.82 | False |
| ablation · A · D_plus_equipment · lightgbm | Sex | M | 269445 | 83885 | 15.77 | 8.05 | 0.84 | False |
| ablation · A · D_plus_equipment · lightgbm | Sex | Mx | 37 | 19 | 9.62 | 6.98 | 0.90 | True |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | 0-60 | 65239 | 21139 | 10.19 | 8.84 | 0.85 | False |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | 105-120 | 34725 | 13870 | 17.25 | 8.31 | 0.84 | False |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | 120-1000 | 25370 | 8511 | 18.92 | 8.93 | 0.81 | False |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | 60-75 | 99847 | 38036 | 12.52 | 8.19 | 0.87 | False |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | 75-90 | 95716 | 38733 | 14.48 | 7.86 | 0.85 | False |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | 90-105 | 67882 | 27331 | 16.11 | 7.95 | 0.84 | False |
| ablation · A · D_plus_equipment · lightgbm | bw_bin | missing | 2092 | 1280 | 18.92 | 10.20 | 0.86 | False |
| ablation · A · D_plus_equipment · lightgbm | has_history | False | 118731 | 118377 | 13.79 | 8.83 | 0.90 | False |
| ablation · A · D_plus_equipment · lightgbm | has_history | True | 272140 | 64848 | 14.24 | 7.99 | 0.90 | False |
| ablation · A · D_plus_equipment · lightgbm | Equipment | Multi-ply | 7546 | 3005 | 19.37 | 9.81 | 0.81 | False |
| ablation · A · D_plus_equipment · lightgbm | Equipment | Raw | 161818 | 63150 | 14.38 | 8.14 | 0.89 | False |
| ablation · A · D_plus_equipment · lightgbm | Equipment | Single-ply | 149646 | 44851 | 13.92 | 8.20 | 0.90 | False |
| ablation · A · D_plus_equipment · lightgbm | Equipment | Unlimited | 40616 | 9590 | 11.34 | 8.33 | 0.90 | False |
| ablation · A · D_plus_equipment · lightgbm | Equipment | Wraps | 31245 | 15145 | 15.86 | 8.53 | 0.88 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Sex | F | 121389 | 34677 | 10.48 | 8.73 | 0.82 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Sex | M | 269445 | 83885 | 16.05 | 8.14 | 0.83 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Sex | Mx | 37 | 19 | 9.60 | 6.77 | 0.89 | True |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | 0-60 | 65239 | 21139 | 10.25 | 8.89 | 0.85 | False |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | 105-120 | 34725 | 13870 | 17.50 | 8.35 | 0.83 | False |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | 120-1000 | 25370 | 8511 | 19.25 | 8.98 | 0.80 | False |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | 60-75 | 99847 | 38036 | 12.70 | 8.28 | 0.86 | False |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | 75-90 | 95716 | 38733 | 14.73 | 7.95 | 0.85 | False |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | 90-105 | 67882 | 27331 | 16.44 | 8.04 | 0.83 | False |
| ablation · A · D_plus_equipment · mlp · s42 | bw_bin | missing | 2092 | 1280 | 18.65 | 10.17 | 0.86 | False |
| ablation · A · D_plus_equipment · mlp · s42 | has_history | False | 118731 | 118377 | 14.02 | 8.90 | 0.89 | False |
| ablation · A · D_plus_equipment · mlp · s42 | has_history | True | 272140 | 64848 | 14.45 | 8.07 | 0.90 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Equipment | Multi-ply | 7546 | 3005 | 19.34 | 9.72 | 0.80 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Equipment | Raw | 161818 | 63150 | 14.41 | 8.13 | 0.89 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Equipment | Single-ply | 149646 | 44851 | 14.47 | 8.43 | 0.89 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Equipment | Unlimited | 40616 | 9590 | 11.33 | 8.30 | 0.90 | False |
| ablation · A · D_plus_equipment · mlp · s42 | Equipment | Wraps | 31245 | 15145 | 15.85 | 8.50 | 0.88 | False |
| chrono · B · D_plus_equipment · lightgbm | Sex | F | 148836 | 61324 | 10.22 | 8.40 | 0.82 | False |
| chrono · B · D_plus_equipment · lightgbm | Sex | M | 243068 | 119987 | 15.68 | 8.03 | 0.83 | False |
| chrono · B · D_plus_equipment · lightgbm | Sex | Mx | 34 | 23 | 13.80 | 10.74 | 0.83 | True |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | 0-60 | 66465 | 27064 | 9.86 | 8.61 | 0.85 | False |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | 105-120 | 32223 | 17766 | 16.54 | 8.34 | 0.85 | False |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | 120-1000 | 24332 | 11562 | 18.19 | 8.96 | 0.83 | False |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | 60-75 | 106451 | 54835 | 12.20 | 8.02 | 0.87 | False |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | 75-90 | 97656 | 53957 | 14.15 | 7.92 | 0.87 | False |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | 90-105 | 64719 | 36217 | 15.77 | 7.95 | 0.86 | False |
| chrono · B · D_plus_equipment · lightgbm | bw_bin | missing | 92 | 72 | 11.94 | 11.81 | 0.95 | True |
| chrono · B · D_plus_equipment · lightgbm | has_history | False | 112375 | 112234 | 13.45 | 8.70 | 0.90 | False |
| chrono · B · D_plus_equipment · lightgbm | has_history | True | 279563 | 116639 | 13.67 | 7.96 | 0.91 | False |
| chrono · B · D_plus_equipment · lightgbm | Equipment | Multi-ply | 1505 | 938 | 22.03 | 11.45 | 0.74 | False |
| chrono · B · D_plus_equipment · lightgbm | Equipment | Raw | 223032 | 129042 | 14.32 | 7.97 | 0.89 | False |
| chrono · B · D_plus_equipment · lightgbm | Equipment | Single-ply | 12776 | 7895 | 16.14 | 9.20 | 0.86 | False |
| chrono · B · D_plus_equipment · lightgbm | Equipment | Unlimited | 128819 | 35304 | 11.62 | 8.36 | 0.89 | False |
| chrono · B · D_plus_equipment · lightgbm | Equipment | Wraps | 25806 | 16956 | 15.58 | 8.26 | 0.88 | False |

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
| history__A__D_plus_equipment-history__lightgbm__histrows | history | A | D_plus_equipment+history | lightgbm | 42 | 1264025 | 301327 | 272140 | 77.12 | 8.78 |
| history__A__D_plus_equipment-history__linear__histrows | history | A | D_plus_equipment+history | linear | 42 | 1264025 | 301327 | 272140 | 1.72 | 9.89 |
| history__A__D_plus_equipment-history__mlp__histrows__s42 | history | A | D_plus_equipment+history | mlp | 42 | 1264025 | 301327 | 272140 | 46.73 | 8.77 |
| history__A__D_plus_equipment__last_deadlift__histrows | history | A | D_plus_equipment | last_deadlift | 42 | 1264025 | 301327 | 272140 | 0.29 | 13.45 |
| history__A__D_plus_equipment__lightgbm__histrows | history | A | D_plus_equipment | lightgbm | 42 | 1264025 | 301327 | 272140 | 36.27 | 14.25 |
| history__A__D_plus_equipment__linear__histrows | history | A | D_plus_equipment | linear | 42 | 1264025 | 301327 | 272140 | 1.74 | 15.59 |
| history_rich__A__D_plus_equipment-history_rich__lightgbm__histrows | history_rich | A | D_plus_equipment+history_rich | lightgbm | 42 | 1264025 | 301327 | 272140 | 99.36 | 8.46 |
| history_rich__A__D_plus_equipment-history_rich__mlp__histrows__s42 | history_rich | A | D_plus_equipment+history_rich | mlp | 42 | 1264025 | 301327 | 272140 | 64.21 | 8.42 |
| history_rich__B__D_plus_equipment-history_rich__lightgbm__histrows | history_rich | B | D_plus_equipment+history_rich | lightgbm | 42 | 1223622 | 301072 | 279563 | 120.81 | 8.00 |
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

