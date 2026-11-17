# Draft: Dataset, Problem Setup, and Method

Rough draft for paraphrasing into the team document. Section numbers continue from the introduction and related
work drafts (`paper/intro_related_work.md`). Every number comes from the saved pipeline outputs
(`data/processed/full/data_summary.json`, `reports/full/data_audit.md`, run metadata in `artifacts/full/runs/`)
or from `reports/REPORT.md`. Reference numbers [1], [6]–[14] match the intro draft's list.

---

## III. Dataset

**Source.** We use the OpenPowerlifting bulk CSV [1], snapshot 2026-10-24 (revision 0fc10dd9), downloaded once on
2026-10-29 and kept unchanged. The snapshot has 4,054,260 entries across 42 columns. Each entry is one lifter's result
in one division at one meet. It covers all event types (full power, bench-only, deadlift-only, and others) and dates
from 1964 to 2026.

**Cleaning.** Table I lists each step and how many rows it removes:

1. **Full-power entries only.** We keep entries where all three lifts were contested (Event = SBD): 2,927,873
   entries.
2. **Successful lifts only.** We require a finite, positive best squat, bench, and deadlift. This removes failed or
   missing lifts, which OpenPowerlifting records as negative or empty values. No lift is imputed.
3. **Exact duplicates.** We remove rows identical in every column.
4. **Repeated listings.** OpenPowerlifting lists a lifter once per division entered, so one performance can appear
   several times. When the lifter, date, equipment, and all three lifts match, we keep one row. Most of these
   (107,440) are the same meet in another division; 445 are the same performance listed under a different meet.

**Table I — Cleaning steps**

| Step | Rows removed | Rows remaining |
|---|---|---|
| Raw snapshot | — | 4,054,260 |
| Full-power (SBD) entries only | 1,126,387 | 2,927,873 |
| Squat missing or failed | 131,602 | 2,796,271 |
| Bench missing or failed | 61,403 | 2,734,868 |
| Deadlift missing or failed | 30,514 | 2,704,354 |
| Exact duplicate rows | 1,709 | 2,702,645 |
| Repeated listings (same lifter, date, equipment, lifts) | 107,885 | **2,594,760** |

The cleaned data have **2,594,760 results from 788,075 lifters** in 440 federations, from 1964-09-05 to 2026-10-18.

**Implausible and extreme values.** Implausible demographic values are set to missing; the row is kept:

- 3 ages outside 5–100 years;
- 23 bodyweights outside 20–300 kg.

Extreme but possibly real lifts are **flagged and kept**, never removed:

- 238 deadlifts over 400 kg;
- 3,120 deadlift-to-squat ratios above 3 or below 0.4.

**The target.** The target is the best successful deadlift in kilograms: mean 185.4 kg, SD 61.1, median 183.7, range
1–492.5.

**Composition.**

- **Sex:** 68.9% male, 31.1% female, and 159 entries in the Mx category.
- **Equipment:** Raw 41.5%, Single-ply 38.1%, Unlimited 10.4%, Wraps 8.1%, Multi-ply 1.9%.
- **Federations:** the largest are THSPA and THSWPA, the Texas high-school federations for boys and girls (461,726 and
  283,473 rows), then USAPL (289,194).
- **Missing data:** age is missing for 42.6% of rows, falling to 30.1% after filling from the reported age class.
  Bodyweight is missing for 0.5%.

**Lifter identity.** OpenPowerlifting separates different lifters who share a name with a "#n" suffix (for example,
"John Doe #2"). We use the full name, suffix included, as the lifter's identity, stored as a pseudonymous hash, and
never merge or split identities. The audit found:

- 31,260 suffixed identities;
- 1,312 identities recorded under more than one sex;
- 16,094 whose implied birth year varies by more than two years.

These may be data-entry errors or merged identities. We report them rather than correct them. The average lifter has
3.3 results (median 2, maximum 175). Lifters with 10 or more results contribute 31.5% of all rows.

**History coverage.**

- **Earlier full-power meet:** 1,804,454 results (69.5%), from 430,939 lifters. We call these *returning lifters*;
  the remaining 790,306 results are *first-time lifters*.
- **Wider deadlift history:** we also keep every successful deadlift from any event type as history only. That is
  2,859,715 lifter-meet entries, including 176,270 deadlift-only and 55,249 bench-and-deadlift entries.
  29,907 first-time full-power lifters have an earlier deadlift from another kind of meet.
- **Attempts:** reported for 45.6% of full-power rows (squat and bench) and for 47.6% of historical deadlift
  entries. The remaining federations publish only best lifts.

---

## IV. Problem Setup

**Task.** Given one full-power competition result, predict the lifter's best successful deadlift at that meet. Inputs
may use only information available before the deadlift: that meet's squat and bench, the lifter's recorded
characteristics, and the lifter's results at strictly earlier meets.

**What the model is never shown.** Model inputs come from an explicit allowlist, enforced in code and by tests. Never
allowed:

- the current meet's deadlift and deadlift attempts;
- the total;
- scoring formulas (Wilks, Dots, Glossbrenner, Goodlift);
- placing and weight class;
- names, identity keys, and dates.

The meet year is allowed only as a coarse context feature. History features use only meets on **strictly earlier
dates**. Same-day entries never see each other, because their order within a day is unknown.

**Evaluation protocols.** Table II summarizes the three protocols.

- **A — Unseen lifters (primary).** Lifters are split 70/15/15 into train, validation, and test by a hash of their
  identity (seed 42). Every result from a lifter lands in the same partition, and the code checks that the
  partitions share no lifters.
- **B — Later meets.** Train on meets before 2023-01-01, validate on 2023-01-01 to 2024-10-31, and test on meets from
  2024-11-01 onward. The boundaries are the 70% and 85% date quantiles, snapped to month starts. Lifters can appear
  in more than one period, so this measures performance on future meets rather than on unseen people.
- **C — Unseen groups (transfer).** One equipment category or federation is removed from training and validation.
  We evaluate on protocol-A test lifters inside that group (*transfer*) and outside it (*in-distribution*), using
  the same fitted model. Groups were chosen by row counts alone:
  - every equipment category with at least 20,000 rows except the largest (Raw): Single-ply, Unlimited, Wraps,
    Multi-ply;
  - the three largest federations: THSPA, USAPL, THSWPA.

**Table II — Partition sizes (rows / lifters)**

| Protocol | Train | Validation | Test |
|---|---|---|---|
| A — unseen lifters | 1,817,276 / 551,698 | 390,871 / 118,377 | 386,613 / 118,000 |
| B — later meets | 1,800,694 / 575,145 | 391,938 / 181,332 | 402,128 / 183,630 |
| C — unseen groups | Protocol-A train/validation minus the held-out group | | A-test rows inside / outside the group |

**Metrics.**

- **Primary metric:** mean absolute error (MAE) in kilograms.
- **Secondary metrics:** mean absolute percentage error, R², and lifter-averaged MAE. Prolific lifters contribute
  many rows, so the lifter-averaged MAE checks they don't dominate.
- **Comparisons:** every comparison is made on identical rows. Confidence intervals (95%) come from 200 bootstrap
  resamples of whole lifters, not individual rows, because one lifter's results are correlated. Model differences
  are reported as paired differences with their own lifter-bootstrap intervals.

**Model selection.**

- **Validation only.** All tuning, early stopping, blend weights, and interval calibration use validation data only.
  Each experiment's configuration is fixed before its test set is scored, and test is scored once.
- **Post-hoc follow-ups.** Later experiments were chosen after earlier test results were known. Protocol B was never
  used to choose any experiment, so it serves as an independent check (Section VI).

---

## V. Method

### A. Inputs

The inputs fall into four groups:

1. **Same-meet inputs.**
   - The meet's best squat and bench, bodyweight, age, sex, equipment, federation.
   - Age filled in from the reported age class when exact age is missing, plus a flag marking the fill.
   - Meet year, drug-tested status, home country, parent federation.
   - Summaries of that meet's squat and bench attempts: opener ÷ best, third attempt ÷ best, number of good
     attempts. Deadlift attempts are never used.
2. **Full-power history,** from the lifter's earlier full-power meets:
   - previous squat, bench, and deadlift; days since that meet; number of earlier meets;
   - career-best squat, bench, and deadlift; career-average deadlift ÷ squat and deadlift ÷ (squat + bench);
   - the deadlift from two meets ago; days since the first meet;
   - whether the previous meet used the same equipment.
3. **Deadlift history from any event type:** the most recent earlier deadlift, the best earlier deadlift, the number
   of earlier deadlift meets, days since the last one, and whether that meet was full power.
4. **Previous deadlift attempts,** from the most recent earlier deadlift meet: heaviest attempted weight (misses
   included), its ratio to the made lift, opener ratio, number of good attempts, career-maximum attempted weight,
   and the change in best deadlift per year between the last two deadlift meets.

**How history is built.** When a lifter has several entries on one day, the entry with the largest total represents
that day. Every history feature is computed from earlier days only. When no earlier meet exists, history features are
missing rather than filled with made-up values.

**Preprocessing.** All preprocessing is learned from the training partition only:

- **Numbers, for the networks:** missing values are filled with the training median, and a missing-value indicator is
  added for every input that has missing values in training. Values are then standardized with training means and
  standard deviations.
- **Numbers, for the tree models:** passed as-is, with missing values handled natively.
- **Categories:** a category gets its own code if it has at least 500 training rows. Rarer categories, unseen
  categories, and missing values share an *unknown* code. This leaves 186 federation codes in training (of 440
  federations) and 72 country codes. Networks receive these codes one-hot encoded, with a dedicated *unknown* column.

### B. Main model: ResNet MLP specialists

Our main model is a tabular residual network (ResNet MLP), following the architecture of Gorishniy et al. [9]. We
implemented it in PyTorch and use it as **two specialists**:

- **First-time-lifter specialist.** Trained on all training rows. Inputs: same-meet inputs, any-event deadlift history,
  and previous-attempt features. That is 24 numeric inputs and 20 missing-value indicators, plus 6 one-hot
  categoricals: **332 input features**.
- **Returning-lifter specialist.** Trained only on training rows that have an earlier full-power meet. Inputs: all four
  groups, 37 numeric inputs and 15 indicators plus the same 6 categoricals: **283 input features**.

**Routing.** At prediction time a result goes to the returning-lifter specialist if the lifter has a strictly earlier
full-power meet, and to the first-time specialist otherwise. That information is known before the meet.

**Architecture.** Each specialist has the same structure:

1. A linear layer maps the input features to width *d* = 256.
2. Three residual blocks follow. Each computes *x* + Dropout(Linear₂(Dropout(ReLU(Linear₁(BatchNorm(*x*)))))), where
   Linear₁ expands 256 → 512 and Linear₂ projects back to 256. Hidden dropout is 0.1; residual dropout is 0.
3. The output head is BatchNorm → ReLU → Linear(256 → 1), giving one value: the predicted deadlift.

The specialists have 876,289 and 863,745 parameters; the difference comes only from the input layer.

**Training.**

- **Target:** standardized with the training mean and standard deviation; predictions are converted back to kg.
- **Loss:** L1 (absolute error), matching the MAE metric.
- **Optimizer:** Adam, learning rate 10⁻³, batch size 4,096.
- **Stopping:** up to 40 epochs, with early stopping on validation MAE (patience 5). The weights from the best epoch
  are restored.
- **Seeds:** each specialist is trained with three seeds (42, 43, 44), and the three predictions are averaged. Seed
  averaging reduces the run-to-run variation seen in single networks.

The ResNet settings are the fixed defaults above and were **not tuned**. Section VI compares it with tuned tree models.

**Table III — ResNet MLP specialists**

| | First-time specialist | Returning specialist |
|---|---|---|
| Input features | 332 | 283 |
| Parameters | 876,289 | 863,745 |
| Training rows / lifters | 1,817,276 / 551,698 | 1,264,025 / 301,327 |
| Best epoch (seeds 42 / 43 / 44) | 26 / 17 / 5 | 15 / 16 / 15 |
| Fit time per seed (8-core laptop CPU) | 5–15 min | 6–7 min |

### C. Compared models and the blend

On the same inputs and rows, we compare the ResNet specialists against simple baselines, tree ensembles, and other
neural networks. Every model is used with the same two-specialist routing.

**Baselines.**

- **Squat ratio:** deadlift = r × squat, with r fitted by least squares through the origin, separately for each sex.
- **Repeat last deadlift:** returning lifters only.
- **Ridge regression:** on standardized numeric inputs and one-hot categories.

**Tree ensembles.**

- **LightGBM [6]:** tuned, with Huber loss and early stopping on validation MAE.
- **CatBoost [7]:** native categorical handling, MAE loss.

LightGBM's settings come from a bounded random search: 16 trials per specialist, trained on a fixed 30% sample of
training lifters, scored on full validation, with the winner refit on all training data. Table IV lists the result.

**Table IV — Tuned LightGBM settings (tree baseline)**

| Setting | First-time specialist | Returning specialist |
|---|---|---|
| Leaves | 511 | 255 |
| Minimum rows per leaf | 100 | 50 |
| Learning rate | 0.03 | 0.05 |
| Features / rows per tree | 60% / 90% | 60% / 100% |
| Huber δ | 20 kg | 10 kg |
| Trees (early-stopped) | 1,184 | 1,859 |
| Fit time | 4.5 min | 3.2 min |

**Other neural networks.** All use L1 loss, a standardized target, Adam, and validation early stopping.

- **Plain MLP:** [128, 64] hidden units.
- **Embedding MLP [10]:** learned periodic embeddings for each numeric input and learned embeddings for each category;
  [256, 128] hidden units after tuning.

**Sequence models (returning lifters only).** These read the lifter's past meets directly instead of the history
summaries.

- **GRU [11]:** hidden size 128, reading the last 12 meets.
- **Transformer encoder [12]:** 2 layers, 4 heads, reading the last 16 meets.

**Blend.** Our best overall result blends these models, with weights chosen on validation. Neural models and the
stochastic LightGBM settings are first averaged over three seeds. The resulting shares are shown in Table V.

**Table V — Blend shares in the best system (chosen on validation)**

| Component | First-time lifters | Returning lifters |
|---|---|---|
| ResNet MLP | 25% | 38% |
| Embedding MLP | 56% | 9% |
| LightGBM | 19% | 9% |
| GRU | — | 19% |
| Transformer | — | 25% |

Neural networks carry 81% of the first-time blend and 91% of the returning-lifter blend. CatBoost received zero
weight.

### D. Prediction ranges

Each prediction from the best (blended) system comes with an 80% range: the prediction ± Q × spread.

- **Spread:** half the gap between two quantile LightGBM models (10th and 90th percentile), built with each
  specialist's tuned settings and floored at 1 kg. Harder cases therefore get wider ranges.
- **Q = 1.03:** a single scale factor fitted on validation lifters (normalized split-conformal prediction [13], [14]),
  so that 80% of validation results fall inside.
- The prediction always lies inside its own range. Test coverage is the independent check.

### E. Implementation

- **Software:** Python with pandas/PyArrow, LightGBM 4.7, CatBoost 1.2, and PyTorch 2.15 (CPU), on an 8-core laptop.
- **Our implementations:** all neural networks (MLP, embedding MLP, ResNet, GRU and Transformer models), their training
  loops, the history features, routing, blending, and interval calibration. The networks use PyTorch's standard
  layers; the tree models use the LightGBM and CatBoost libraries.
- **Experiment records:** every experiment saves its configuration, dataset checksum, split ID, seed, package versions,
  fitted preprocessing, and per-row predictions.
- **Tests:** a 61-test suite checks for leakage (for example, no same-day or future history), split separation, metric
  correctness, and model save/reload.
- **Code:** all in the project repository.

---

## Notes for the team

- **Table I's first row:** "1,126,387 removed" is the non-SBD entries (4,054,260 − 2,927,873). The other rows come
  straight from the cleaning log.
- **Table V:** the blend shares are the product of the pairwise validation weights. If space is tight, it can become
  one sentence: "neural networks carry most of the blend weight."
- **Table III's ResNet numbers:** parameter counts are exact (input layer + 3 blocks + head). Best epochs and fit
  times come from the saved run metadata.
- **Diagram:** a small one would help in Method — inputs → *has an earlier meet?* → first-time or returning ResNet
  specialist → prediction ± range.
- **What to keep out of Method:** the experiments that didn't change the final model, such as loss variants, the
  capacity check, and seed-averaging details. They belong in Experiments, in one or two sentences each.
