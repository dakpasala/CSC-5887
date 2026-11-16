# Draft: Introduction and Related Work

Rough draft for paraphrasing into the team document. Target length: about 1 page of a 5-page IEEE
paper for these two sections combined. All numbers below are test-set results from `reports/REPORT.md`.
The bracketed numbers [1]…[14] refer to the reference list at the end.

---

## I. Introduction

Powerlifting meets record three lifts per competitor: the squat, the bench press, and the deadlift. Because the
lifts are performed in that order at the same meet, a lifter's squat and bench are known before their deadlift. This
raises a practical question: **how well can a lifter's competition deadlift be predicted from their squat, bench, and
basic characteristics?** A good estimate gives athletes and coaches a reference point for comparing a recorded
deadlift with those of similar lifters. A common rule of thumb predicts the deadlift as a fixed multiple of the squat.

We study this question on OpenPowerlifting [1], a public archive of more than four million competition entries. After
cleaning, our snapshot contains 2.59 million full-power results from 788,075 lifters. We frame the task as same-meet
supervised regression: the target is the best successful deadlift, and the inputs are restricted to information
available before that deadlift. Totals, scoring formulas such as Wilks and Dots, placings, and the meet's own deadlift
attempts are excluded, because they reveal the answer. Predictions are intended as references for comparing recorded
performance. They are not forecasts of future strength, estimates of maximal capacity, or attempt recommendations.

This differs from prior work, which mostly forecasts future meet results or predicts whether an attempt succeeds
(Section II). We ask four questions:

1. How accurately can the deadlift be predicted from squat, bench, bodyweight, age, sex, and equipment?
2. Which groups of inputs improve accuracy over simple baselines?
3. Do a lifter's earlier competition results help, compared on identical lifters?
4. How does accuracy change for meets later than the training data, and for federations or equipment
   categories never seen in training?

Our main contributions are:

- **A leakage-controlled benchmark.** Splits are grouped by lifter, and inputs come from an explicit allowlist.
  History features use only strictly earlier meets. Each comparison is evaluated on identical rows, with
  lifter-level bootstrap confidence intervals.
- **A measured ablation of input groups and lifter history.** Squat-based ratios give 21.9 kg mean absolute error
  (MAE). A gradient-boosted model with same-meet inputs reaches 14.1 kg. Adding prior-meet history lowers the error
  for returning lifters to about 8 kg, roughly 5 kg better than simply repeating their last deadlift.
- **A comparison of tree ensembles with deep tabular and sequence models.** LightGBM, CatBoost, MLPs (plain,
  embedding-based, ResNet), a GRU, and a Transformer over meet histories all land within about 0.1 kg of each
  other once tuned. Blending them gives a final system with **9.54 kg MAE** on unseen lifters, 12.98 kg for
  first-time lifters, and 8.02 kg for returning lifters.
- **Generalization and uncertainty tests.** The final recipe reaches 9.11 kg on meets after the training period.
  Never-seen federations and equipment categories cost 0.15–1.7 kg. Calibrated 80% prediction ranges achieve 80.2%
  test coverage.

---

## II. Related Work

**Performance prediction in powerlifting.** Ferrari et al. [2] predict *future* classic-powerlifting performance with a
machine-learning linear regression, using sex, age, bodyweight, initial strength, and competition history (54,064
observations, 8,907 lifters). Medina-Romero et al. [3] apply data-mining and machine-learning techniques to predict
powerlifting results. A 2025 study from Dublin City University [4] models whether an individual raw-powerlifting
*attempt* succeeds, using nonlinear mixed logistic regression. Our task is different from all three: we predict the
deadlift recorded at the same meet from the lifts that precede it. We also study generalization to later meets and
unseen federations, which these works do not address.

**Normalizing strength across lifters.** Coefficient formulas such as Wilks and Dots rescale totals by bodyweight so
lifters of different sizes can be compared [5]. They summarize performance after the fact and use the deadlift, so they
cannot serve as predictors here. Our models instead learn the relationship between the lifts directly, conditioned on
bodyweight, age, sex, and equipment.

**Models for tabular data.** Gradient-boosted decision trees such as LightGBM [6] and CatBoost [7] are strong defaults
for tabular regression. A large benchmark found that tree ensembles still match or beat deep networks on typical
tabular data [8]. Deep tabular models have narrowed this gap through residual architectures [9] and learned
embeddings of numerical features [10]. We compare both families on the same rows. For lifters with earlier meets, we
also test sequence models that read the full meet history: a GRU [11] and a Transformer encoder [12].

**Prediction uncertainty.** Conformal prediction gives distribution-free prediction intervals. Conformalized quantile
regression [13] and locally weighted (normalized) conformal methods [14] adapt the interval width to each input. We use
a normalized split-conformal correction, calibrated only on validation lifters, around the final system's predictions.

---

## References

Items marked **[verify]** have not been checked against the source yet. Confirm authors, venue, year, and pages
before submission.

1. OpenPowerlifting Project, "OpenPowerlifting bulk CSV data," https://openpowerlifting.gitlab.io/opl-csv/
   (snapshot 2026-10-24, revision 0fc10dd9). *Verified: download page and bundled README.*
2. L. Ferrari, G. Bochicchio, A. Bottari, F. Lucertini, and S. Pogliaghi, "Predicting future performance in
   powerlifting: A machine learning approach," *Sports Medicine – Open*, vol. 11, art. 112, 2025,
   doi:10.1186/s40798-025-00903-z. *Verified via Crossref, including the abstract summary above.*
3. J. Medina-Romero, A. M. Mora, J. F. Valenzuela-Valdés, and P. Á. Castillo, "Applying data mining and machine
   learning techniques to predict powerlifting results," *Engineering Proceedings*, vol. 39, no. 1, art. 20
   (ITISE 2023), doi:10.3390/engproc2023039020. *Metadata verified via Crossref; paper contents not yet read, so keep
   the description general.*
4. "Predicting a successful attempt in raw powerlifting: A nonlinear mixed logistic regression analysis," Dublin City
   University, 2025, https://doras.dcu.ie/31743/. *Title verified from the PDF; **authors and venue [verify]**
   (repository file name suggests "Darragh et al.").*
5. Wilks / Dots coefficient source. **[verify, choose a citation]**: e.g. the OpenPowerlifting coefficient
   documentation, or a published validation of the Wilks formula.
6. G. Ke et al., "LightGBM: A highly efficient gradient boosting decision tree," in *Proc. NeurIPS*, 2017.
   **[verify pages]**
7. L. Prokhorenkova, G. Gusev, A. Vorobev, A. V. Dorogush, and A. Gulin, "CatBoost: Unbiased boosting with categorical
   features," in *Proc. NeurIPS*, 2018. **[verify]**
8. L. Grinsztajn, E. Oyallon, and G. Varoquaux, "Why do tree-based models still outperform deep learning on typical
   tabular data?" in *Proc. NeurIPS (Datasets and Benchmarks)*, 2022. **[verify]**
9. Y. Gorishniy, I. Rubachev, V. Khrulkov, and A. Babenko, "Revisiting deep learning models for tabular data," in
   *Proc. NeurIPS*, 2021. **[verify]**
10. Y. Gorishniy, I. Rubachev, and A. Babenko, "On embeddings for numerical features in tabular deep learning," in
    *Proc. NeurIPS*, 2022. **[verify]**
11. K. Cho et al., "Learning phrase representations using RNN encoder–decoder for statistical machine translation," in
    *Proc. EMNLP*, 2014. **[verify]**
12. A. Vaswani et al., "Attention is all you need," in *Proc. NeurIPS*, 2017. **[verify]**
13. Y. Romano, E. Patterson, and E. Candès, "Conformalized quantile regression," in *Proc. NeurIPS*, 2019. **[verify]**
14. J. Lei, M. G'Sell, A. Rinaldo, R. J. Tibshirani, and L. Wasserman, "Distribution-free predictive inference for
    regression," *J. Amer. Statist. Assoc.*, vol. 113, no. 523, 2018. **[verify]**

---

## Notes for the team

- **Numbers:** every figure above comes from the test tables in `reports/full/` and the summary in
  `reports/REPORT.md`. If any number changes, update it here too.
- **Claims to keep modest:** don't claim novelty beyond the combination we tested (same-meet cross-lift prediction,
  controlled ablations, past-only history, generalization tests). We haven't done a full literature search.
- **Wording to avoid:** "predict how much someone can lift", "detect undertraining", or anything causal about
  equipment or federation. The paper's framing is a reference comparison, not a diagnosis.
- **Fitting the page budget:** for a 5-page limit, drop the "Normalizing strength" paragraph first, then shorten the
  contributions list to three items.
