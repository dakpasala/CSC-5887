# Draft: Experiments

Rough draft for paraphrasing. Unless stated otherwise, every number is **test-set** MAE in kg on protocol A (386,613
results from 118,000 unseen lifters). Rows are identical within each table. Brackets are 95% lifter-bootstrap
confidence intervals for paired differences. Source: `reports/REPORT.md` and `reports/full/`.

---

## VI. Experiments

### A. How accurate is same-meet prediction? (RQ1)

We first ask how well the deadlift can be predicted from same-meet information alone: squat, bench, bodyweight, age,
sex, and equipment. This setting uses no lifter history, so it applies equally to first-time and returning lifters.

| Model | MAE | MAPE | R² |
|---|---|---|---|
| Squat ratio (r × squat, by sex) | 21.91 | 12.3% | 0.77 |
| Ridge regression | 15.45 | 9.2% | 0.88 |
| MLP (1 seed) | 14.30 | 8.3% | 0.90 |
| **ResNet MLP (3 seeds), main model** | **14.28** | **8.3%** | **0.90** |
| LightGBM (tree baseline) | 14.08 | 8.3% | 0.90 |

**Accuracy.** The ResNet cuts the squat-ratio rule's error by about a third, a reduction of 7.6 kg [7.5, 7.8]. It beats
ridge regression by 1.17 kg [1.11, 1.22], so the relationships between the lifts are clearly nonlinear. Weighting each
lifter equally gives a near-identical MAE (14.22 kg), so prolific competitors are not driving the result.

**In practical terms.** The ResNet's median miss is 11.2 kg, and 75% of predictions fall within 20 kg of the recorded
deadlift, against a mean deadlift of 185 kg.

**Trees win on same-meet inputs alone.** With only these six inputs, LightGBM beats the ResNet by 0.20 kg
[0.18, 0.22]. The ResNet only slightly beats the plain MLP, by 0.02 kg [0.01, 0.03]. The three ResNet seeds agree
closely (14.31–14.34 kg), so this gap is not noise. It matches prior findings that tree ensembles are hard to beat on
small sets of tabular features [8]. The ordering reverses once lifter history is added (Section VI-D): the network's
advantage comes from combining many history features, not from the basic inputs.

**Where the errors are.** Absolute error grows with lift size:

- 10.4 kg for women vs 16.0 kg for men;
- 10.3 kg for lifters under 60 kg bodyweight vs 19.4 kg at 120 kg and above;
- 19.2 kg when bodyweight is missing.

Relative error stays at 8–9% (8.8% for women, 8.1% for men). Residuals show the usual regression toward the mean:
the strongest deadlifts are under-predicted and the weakest over-predicted. This reflects predicting a conditional
average. It is not evidence about any individual lifter.

### B. Which inputs help? (RQ2)

To measure each input group's contribution, we add groups one at a time and evaluate every stage on the same rows.
This keeps missing data from changing who is being evaluated.

| Inputs | Ridge | MLP | LightGBM | LightGBM change |
|---|---|---|---|---|
| Squat | 19.48 | 18.51 | 16.99 | — |
| + bench | 18.19 | 16.98 | 15.73 | −1.26 [−1.30, −1.21] |
| + bodyweight, age, sex | 16.79 | 15.30 | 14.66 | −1.07 [−1.13, −1.02] |
| + equipment | 15.45 | 14.30 | 14.08 | −0.58 [−0.62, −0.55] |
| + federation, age class, country, tested status, year | — | — | 13.71 | −0.37 [−0.40, −0.35] |
| + squat/bench attempt summaries | — | — | 13.68 | −0.03 |

**Every group helps, with shrinking returns.** All three models show the same pattern, and every step's confidence
interval excludes zero.

- **Squat:** LightGBM using squat alone already beats the fixed ratio rule by 5 kg. The squat–deadlift relationship
  depends on how strong the lifter is, not on a single multiplier.
- **Bench:** the bench is nearly as informative as the demographic group. It likely carries information about
  overall strength and body type that the squat alone misses.
- **Context:** the extra context group adds 0.37 kg. Most of it comes from federation, which is worth 0.25 kg
  [0.23, 0.27] on its own, and from filling missing ages from age classes (missing age falls from 42.6% to 30.1%).
- **Attempts:** squat and bench attempt details add almost nothing, partly because only 46% of results report
  attempts.

These are predictive contributions, not causal or biological effects.

### C. Does lifter history help? (RQ3)

Most results (69.5%) come from lifters who competed before. For these returning lifters we add history features,
built from strictly earlier meets, to the ResNet one group at a time. Every stage is evaluated on the same 268,289
results from 64,764 lifters, with three seeds averaged per stage.

| Model (returning lifters) | MAE | Change |
|---|---|---|
| Repeat last deadlift | 13.44 | — |
| ResNet, no history | 14.41 | — |
| + previous meet | 8.62 | −5.79 [−5.87, −5.69] |
| + career summaries | 8.22 | −0.40 [−0.42, −0.39] |
| + any-event history and previous attempts (returning specialist) | **8.07** | −0.15 [−0.16, −0.14] |
| Best blend | 8.02 | |

**History is by far the largest gain.** The previous meet alone cuts the ResNet's error by 5.8 kg, more than all the
same-meet input groups combined. Career summaries add another 0.40 kg, and deadlift history from other event types
plus previous attempts add 0.15 kg. In total, history lowers the ResNet's error for returning lifters by
6.3 kg [6.2, 6.4].

**The network gets more out of history than the trees.** At each step the ResNet gains more than LightGBM does with
the same inputs:

- previous meet: −5.79 vs −5.48 kg;
- career summaries: −0.40 vs −0.32 kg.

Without history the ResNet trails LightGBM (Section VI-A). With full history it is ahead (8.07 vs 8.13 kg, Section
VI-D). This matches the idea that the network's strength is combining many related numeric features.

**The model adds more than repeating history.** Simply repeating the lifter's last deadlift gives 13.44 kg, already
better than the no-history model. The final ResNet beats that baseline by 5.4 kg [5.3, 5.5]. It combines the lifter's
past performance with how they are lifting at this meet, rather than assuming they repeat themselves.

**First-time lifters.** They have no full-power history and improve less: from 13.99 kg (same-meet inputs) to 13.04 kg
for the ResNet first-time specialist, which adds the extra context inputs. The exception is the 4,400 first-time
lifters (3.7%) with an earlier deadlift-only or bench-and-deadlift meet. Using that history cuts their error from
15.51 to 10.31 kg. Their earlier meets are not full power, which is why the original history features missed them.

### D. Model comparison

We compare our main model, the ResNet MLP, against gradient-boosted trees and other neural networks on the same
inputs and rows. Each model is used as two specialists, one for first-time lifters and one for returning lifters.
Neural networks and LightGBM are averaged over three seeds; CatBoost uses one.

| Model | All lifters | First-time | Returning |
|---|---|---|---|
| CatBoost (trees) | 9.66 | 13.07 | 8.16 |
| LightGBM (trees, 3 seeds) | 9.62 | 13.01 | 8.13 |
| Embedding MLP (3 seeds) | 9.62 | 13.00 | 8.12 |
| **ResNet MLP (3 seeds), main model** | **9.59** | 13.04 | **8.07** |
| Blend of the above + sequence models | **9.54** | **12.98** | **8.02** |

**Our network edges out strong tree baselines.** The ResNet is the best single model family overall and for returning
lifters. Paired against LightGBM it is −0.035 kg [−0.043, −0.026] overall and −0.064 kg [−0.074, −0.053] for
returning lifters. Against CatBoost the gaps are −0.07 and −0.09 kg. For first-time lifters it is slightly worse than
LightGBM (+0.03 kg [+0.02, +0.05]) and the embedding MLP (+0.04 kg). Its advantage comes from using history, and
returning lifters are 69% of results. The gaps are small: all families land within 0.07 kg of each other. Prior work finds that tree ensembles usually match or beat deep
networks on tabular data [8], so matching them is the realistic bar for a network here. Our ResNet does slightly
better. The validation-weighted blend adds 0.05 kg over the ResNet, and neural networks carry most of its weight
(Table V). CatBoost received zero blend weight because its errors are already covered by the other models.

**The specialist split matters more than the model.** A single model for all lifters loses about 0.5 kg against the
two specialists. For example, LightGBM gets 10.11 kg for everyone versus 9.64 kg split. That is about ten times the
ResNet's edge over the trees.

**Tuning, losses, and seeds.** Each of these gives small but consistent gains:

- **Hyperparameter search:** 0.03–0.07 kg per model.
- **Huber loss instead of squared error:** about 0.1 kg for LightGBM.
- **Averaging three seeds:** up to 0.09 kg for the networks, which vary more between seeds than the tree models do.

**Sequence models.** For returning lifters, a GRU reads the raw sequence of past meets, with no hand-built history
summaries, and reaches 8.23 kg. That is close to an untuned LightGBM with about 25 engineered history features
(8.21 kg). The network learns most of what those features capture. A Transformer over the last 16 meets did not
improve on the GRU (8.20 vs 8.16 kg for the tuned GRU).

**Bigger models don't help.** Networks with about 25× the parameters, larger tree ensembles, and 10× more training
data each changed the error by 0.2 kg or less. Together with the tight spread across model families, this suggests
the remaining error reflects information the inputs don't contain, such as deadlift-specific strength and day-to-day
variation, rather than limited model capacity.

### E. Generalization to later meets and unseen groups (RQ4)

**Later meets (protocol B).** We retrained the main model and the full recipe on the date split (training before
2023, testing on 402,128 results from November 2024 onward). They are compared with earlier LightGBM specialist sets
on the same rows.

| System | All | First-time | Returning |
|---|---|---|---|
| LightGBM, original inputs (same-meet + previous meet) | 9.59 | 13.85 | 8.17 |
| LightGBM, expanded inputs | 9.35 | 13.05 | 8.11 |
| **ResNet MLP, final inputs (main model, 3 seeds)** | **9.10** | **13.01** | **7.79** |
| Blend, final recipe (1 seed per component) | 9.11 | 13.00 | 7.81 |

**The main model holds up about two years past the training period.** It beats the expanded-input trees by
0.26 kg [0.24, 0.27] overall, and by 0.33 kg [0.31, 0.34] for returning lifters. It even edges out the full blend,
by 0.013 kg [0.007, 0.019]; the blend here uses one seed per component, while the ResNet averages three. Absolute
error is somewhat lower than on protocol A, partly because recent meets have more Raw lifting and more lifters with
history.

This table also checks our own process. Most later improvements (career and attempt history, tuning, new
architectures, blending) were chosen while looking at protocol-A results, so their protocol-A gains could be slightly
optimistic. Protocol B was never used for any choice. Measured against the expanded-input trees, the main model
improves by 0.26 kg on protocol B versus 0.12 kg on protocol A. The improvements carry over to data never used for
any decision.

**Unseen federations and equipment (protocol C).** For each held-out group, we compare LightGBM specialists trained
without the group against the best system trained with it, on the same test rows. The difference is the cost of
never seeing that group.

| Held out | Results | Seen in training | Held out | Extra error |
|---|---|---|---|---|
| USAPL | 43,006 | 10.06 | 10.21 | +0.15 |
| Unlimited equipment | 40,208 | 7.26 | 7.50 | +0.23 |
| Single-ply | 147,373 | 9.33 | 9.79 | +0.46 |
| Multi-ply | 7,369 | 13.79 | 14.52 | +0.74 |
| THSWPA (HS girls) | 42,326 | 5.87 | 6.71 | +0.84 |
| Wraps | 31,414 | 11.11 | 12.50 | +1.39 |
| THSPA (HS boys) | 69,477 | 8.69 | 10.37 | +1.68 |

**Transfer cost depends on how unusual the group is.** Groups that resemble the training data cost less than 0.5 kg.
The Texas high-school federations (young lifters, with ages mostly unreported) and Wraps meets cost the most. Part of
each cost is a model difference, LightGBM alone versus the full blend, worth about 0.1 kg.

**History makes transfer far more robust.** Earlier models without history lost 2–9 kg on the same groups. Linear
models that saw an equipment category they had never trained on failed badly, with 63–117 kg MAE. With the final
inputs, no held-out group is more than 1.7 kg worse than when it was seen in training. These gaps reflect population
differences, not causal effects of equipment or federation.

### F. Prediction ranges

Each prediction comes with an 80% range: the prediction ± Q × spread. The spread comes from quantile LightGBM models,
and the scale Q is fitted on validation only (Section V-D). Test results:

| Group | Coverage (target 80%) | Median width |
|---|---|---|
| All lifters | **80.2%** | 27 kg (±14) |
| First-time | 80.4% | 42 kg (±21) |
| Returning | 80.2% | 23 kg (±12) |

**Calibrated.** Test coverage matches the 80% target. Misses are balanced (10.3% below the range, 9.4% above), and the
prediction always lies inside its own range.

**Adaptive.** Ranges are much tighter for returning lifters than for first-time lifters, and for women (median
19.5 kg) than for men (30.9 kg). Coverage stays within about 1.5 points of 80% across sex, bodyweight bins, and
equipment. The weakest groups are Multi-ply (78%) and the very small Mx group (14 results).

**Usefulness.** Calibrated ranges are the right way to present these predictions as reference values. A typical
returning lifter's recorded deadlift falls within about ±12 kg of the prediction eight times out of ten.

---

## Notes for the team

- **If space runs out:** first cut the Ridge/MLP columns from Section B's table, then fold the protocol-B table
  into one sentence, then shorten Section F to its first paragraph.
- **Figures:** the best two would be the ablation chart (Section B) and an MAE-progression bar chart
  (14.1 → 9.6 → 9.5). The ablation chart is in `reports/full/figures/`. The progression chart doesn't exist yet;
  ask and I'll generate it.
- **Section C's LightGBM comparison numbers** (−5.48 and −0.32 kg) are the same-row LightGBM history steps from
  the earlier LightGBM-based experiments (`reports/REPORT.md`, RQ3 and its career-history follow-up).
- **Section D's 8.21 kg** is the untuned LightGBM, used so the GRU comparison is like-for-like (both untuned). The
  tuned LightGBM returning-lifter number is 8.15 kg.
