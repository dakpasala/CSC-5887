# Draft: Experiments

Rough draft for paraphrasing. All numbers are **test-set** MAE in kg on protocol A (386,613 results, 118,000 unseen
lifters) unless stated. Rows are identical within each table. Brackets are 95% lifter-bootstrap confidence intervals
for paired differences. Source: `reports/REPORT.md` and `reports/full/`.

---

## VI. Experiments

### A. How accurate is same-meet prediction? (RQ1)

Models here see only same-meet inputs: squat, bench, bodyweight, age, sex, and equipment.

| Model | MAE | MAPE | R² |
|---|---|---|---|
| Squat ratio (r × squat, by sex) | 21.91 | 12.3% | 0.77 |
| Ridge regression | 15.45 | 9.2% | 0.88 |
| MLP (3 seeds) | 14.30 | 8.3% | 0.90 |
| **LightGBM** | **14.08** | **8.3%** | **0.90** |

LightGBM cuts the ratio rule's error by a third. Its median miss is 11 kg, and 76% of predictions fall within 20 kg of
the recorded deadlift. Absolute error grows with lift size (10.4 kg for women vs 15.7 kg for men), but relative error
stays similar at 8–9%.

### B. Which inputs help? (RQ2)

LightGBM, adding one input group at a time:

| Inputs | MAE | Change |
|---|---|---|
| Squat | 16.99 | — |
| + bench | 15.73 | −1.26 [−1.30, −1.21] |
| + bodyweight, age, sex | 14.66 | −1.07 [−1.13, −1.02] |
| + equipment | 14.08 | −0.58 [−0.62, −0.55] |
| + federation, age class, country, tested status, year | 13.71 | −0.37 [−0.40, −0.35] |
| + squat/bench attempt summaries | 13.68 | −0.03 |

Every group helps, with shrinking returns, and ridge regression and the MLP follow the same pattern. Even squat
alone beats the fixed ratio by 5 kg, so the deadlift–squat relationship isn't a single ratio. Attempt details add
almost nothing, partly because only 46% of results report attempts. These are predictive contributions, not causal
effects.

### C. Does lifter history help? (RQ3)

Returning lifters only (268,289 results, 64,764 lifters):

| Model | MAE |
|---|---|
| Repeat last deadlift | 13.44 |
| LightGBM, no history | 14.20 |
| + previous meet | 8.73 |
| + career summaries | 8.41 |
| + any-event history and previous attempts (returning specialist) | 8.15 |
| Best blend | **8.02** |

History is the largest single gain: −5.5 kg [−5.6, −5.4] from the previous meet alone. The final model also beats
simply repeating the last deadlift by 5.4 kg. First-time lifters have no history, so they improve less: 13.80 →
12.98 kg. For the 3.7% of first-timers with an earlier deadlift-only or push-pull meet, that history cuts their error
from 15.36 to 10.39 kg.

### D. Model comparison

The table below compares model families on the same inputs, each routed into first-time and returning specialists.
Single-model numbers are averaged over 3 seeds where marked.

| Model | All lifters | First-time | Returning |
|---|---|---|---|
| CatBoost | 9.66 | 13.07 | 8.16 |
| **LightGBM (main model)** | **9.64** | 13.02 | 8.15 |
| Embedding MLP (3 seeds) | 9.62 | 13.00 | 8.12 |
| ResNet MLP (3 seeds) | 9.59 | 13.04 | 8.07 |
| Blend of the above + sequence models | **9.54** | **12.98** | **8.02** |

- **Model family barely matters.** All families land within 0.12 kg of each other, and the blend adds only 0.10 kg
  over LightGBM.
- **The specialist split matters more.** One LightGBM for everyone gets 10.11 kg, about 0.5 kg worse than the
  specialists.
- **Sequence models learn history on their own.** For returning lifters, a GRU reading raw past meets, with no
  hand-built history features, reaches 8.23 kg, close to LightGBM with about 25 engineered history features
  (8.21 kg, untuned). Averaged over seeds, the GRU reaches 8.12 kg. A Transformer over 16 meets did not beat it
  (8.20 kg).
- **Bigger models don't help.** Larger networks (about 25× the parameters), larger trees, and 10× more training data
  each changed the error by 0.2 kg or less. The remaining error reflects information the inputs don't contain, not
  model capacity.

### E. Generalization to later meets and unseen groups (RQ4)

**Later meets (protocol B, 402,128 results from 2024-11 onward).** The full recipe was retrained on the date split.

| Specialist set | All | First-time | Returning |
|---|---|---|---|
| Original (same-meet + previous meet) | 9.59 | 13.85 | 8.17 |
| + expanded inputs | 9.35 | 13.05 | 8.11 |
| Final recipe | **9.11** | **13.00** | **7.81** |

Protocol B was never used to choose experiments. On it, the later follow-ups improve accuracy by 0.24 kg, against
0.18 kg on protocol A. So the gains are not an artifact of reusing the protocol-A test set.

**Unseen federations and equipment (protocol C).** The cost of never seeing a group: on the same test rows,
LightGBM specialists trained without the group, minus the best system trained with it.

| Held out | Results | Extra error |
|---|---|---|
| USAPL | 43,006 | +0.15 |
| Unlimited equipment | 40,208 | +0.23 |
| Single-ply | 147,373 | +0.46 |
| Multi-ply | 7,369 | +0.74 |
| THSWPA (HS girls) | 42,326 | +0.84 |
| Wraps | 31,414 | +1.39 |
| THSPA (HS boys) | 69,477 | +1.68 |

Groups that resemble the training data transfer well. The Texas high-school federations and Wraps meets, which have
distinct populations, cost the most. Earlier no-history models lost 2–9 kg on these groups, so history also makes
transfer more robust. These gaps reflect population differences, not causal effects of equipment or federation.

### F. Prediction ranges

| Group | Coverage (target 80%) | Median width |
|---|---|---|
| All lifters | **80.2%** | 27 kg (±14) |
| First-time | 80.4% | 42 kg (±21) |
| Returning | 80.2% | 23 kg (±12) |

The calibration was fitted on validation only, and test coverage matches the 80% target. Misses are balanced, about
10% below the range and 9% above it. Coverage stays within 1.5 points across sex, bodyweight, and equipment. The
exceptions are Multi-ply (78%) and the 14-result Mx group.

---

## Notes for the team

- **If space runs out:** cut the protocol-B table to one sentence, then fold Section F's table into the text.
- **Figures:** the best two would be the ablation chart (Section B) and an MAE-progression bar chart
  (14.1 → 9.6 → 9.5). Existing figures are in `reports/full/figures/`. The progression chart doesn't exist yet;
  ask and I'll generate it.
- **Section D's untuned 8.21 kg:** this is the untuned LightGBM, used so the GRU comparison is like-for-like (both
  untuned). The tuned LightGBM returning number is 8.15.
