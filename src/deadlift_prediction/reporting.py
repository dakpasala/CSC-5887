"""Markdown data audit, results tables, and figures."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402

from .config import artifacts_dir, read_json, reports_dir  # noqa: E402

SYNTH_BANNER = "> **SYNTHETIC FIXTURE.** These numbers come from generated data and are not research findings.\n\n"


def _md(df: pd.DataFrame, floatfmt: str = ".2f") -> str:
    if df.empty:
        return "_(none)_\n"
    df = df.copy()
    for c in df.columns:
        if pd.api.types.is_float_dtype(df[c]):
            df[c] = df[c].map(lambda v: "" if pd.isna(v) else format(v, floatfmt))
    cols = list(df.columns)
    lines = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    lines += ["| " + " | ".join(map(str, r)) + " |" for r in df.astype(str).to_numpy()]
    return "\n".join(lines) + "\n"


def write_data_audit(s: dict, bal_a: pd.DataFrame, bal_b: pd.DataFrame, path: Path) -> None:
    snap = s["snapshot"]
    out = ["# Data audit — " + s["config"] + "\n"]
    if s["synthetic"]:
        out.append(SYNTH_BANNER)
    out.append(f"- Source: {snap['source_url']}\n- Archive: `{snap['archive']}` (sha256 `{snap['sha256']}`)\n"
               f"- Retrieved: {snap.get('retrieved_at')}\n- Raw rows in snapshot: {snap['raw_rows']:,}\n"
               f"- Cleaned rows: {s['clean_rows']:,}; estimated unique lifters: {s['clean_lifters']:,}\n"
               f"- Date coverage: {s['date_min']} to {s['date_max']}\n- Split ID: `{s['split_id']}`\n\n")
    out.append("## Exclusions by step\n\n" + _md(pd.DataFrame(s["exclusions"]).drop(columns=["note"]).assign(
        note=[e["note"][:120] for e in s["exclusions"]])) + "\n")
    rl = s["audit"]["repeated_listings"]
    out.append(f"Repeated listings removed: {rl['removed']:,} ({rl['same_meet_other_division']:,} same meet in another division; "
               f"{rl['different_meet_key_same_day']:,} under a different meet key on the same day, e.g. cross-federation listings).\n\n")
    out.append("Values set to missing (rows kept): " + ", ".join(f"{k} = {v:,}" for k, v in s["audit"]["set_to_missing"].items()) + ".\n\n")
    out.append("Extreme values flagged but kept: " + ", ".join(f"{k} = {v:,}" for k, v in s["audit"]["flags_kept"].items()) + ".\n\n")
    out.append("## Missingness (cleaned rows)\n\n" + _md(pd.DataFrame([{"column": k, "share_missing": v} for k, v in s["missingness"].items()]), ".4f") + "\n")
    out.append("## Distributions\n\n**Sex**\n\n" + _md(pd.DataFrame(list(s["sex"].items()), columns=["Sex", "rows"])))
    out.append("\n**Equipment**\n\n" + _md(pd.DataFrame(list(s["equipment"].items()), columns=["Equipment", "rows"])))
    out.append(f"\n**Federation** (top 20 of {s['n_federations']})\n\n" + _md(pd.DataFrame(list(s["federation_top20"].items()), columns=["Federation", "rows"])))
    t = s["target_kg"]
    out.append(f"\nTarget Best3DeadliftKg: mean {t['mean']:.1f}, sd {t['std']:.1f}, min {t['min']:.1f}, median {t['50%']:.1f}, max {t['max']:.1f}.\n\n")
    out.append(f"## History eligibility\n\nRows with a strictly earlier eligible meet for the same lifter: {s['history_eligible_rows']:,} "
               f"({s['history_eligible_rows'] / s['clean_rows']:.1%}); lifters with at least one such row: {s['history_eligible_lifters']:,}.\n\n")
    idt = s["identity"]
    out.append("## Lifter identity\n\n" + "\n".join(f"- {k}: {v}" for k, v in idt.items() if k not in ("limitations", "rows_per_lifter")))
    out.append("\n- rows per lifter: " + ", ".join(f"{k} {v:.3g}" for k, v in idt["rows_per_lifter"].items()))
    out.append("\n\nLimitations:\n" + "\n".join(f"- {x}" for x in idt["limitations"]) + "\n\n")
    sp = s["splits"]
    out.append(f"## Splits\n\nProtocol A (unseen lifters): hashed-identity group split {sp['group_fractions']}, seed {sp['seed']}.\n\n"
               + _md(bal_a) + "\n")
    out.append(f"Protocol B (future meets): {sp['chrono_rule']}; boundaries {sp['chrono_boundaries']}. Lifters recur across periods.\n\n"
               + _md(bal_b) + "\n")
    out.append("Protocol C transfer groups (chosen by row counts only): "
               + "; ".join(f"{g['field']}={g['value']} ({g['rows']:,} rows)" for g in sp["transfer_groups"]) + "\n")
    path.write_text("".join(out))


# ------------------------------------------------------------------------- summary

def _fig_dir(cfg):
    d = reports_dir(cfg) / "figures"
    d.mkdir(parents=True, exist_ok=True)
    return d


def summarize_results(cfg: dict, final: bool = False) -> Path:
    root = artifacts_dir(cfg)
    tdir = root / ("tables_final" if final else "tables_val")
    m = pd.read_csv(tdir / "metrics.csv")
    pr = pd.read_csv(tdir / "paired.csv")
    sg = pd.read_csv(tdir / "subgroups.csv", dtype={"group": str}, keep_default_na=False, na_values={"mape": [""], "r2": [""]})
    figs = _fig_dir(cfg)
    rd = reports_dir(cfg)
    tag = "test" if final else "val"
    sns.set_theme(style="whitegrid", context="paper")

    keep = ["label", "model", "feature_set", "rows", "lifters", "mae", "mae_ci_low", "mae_ci_high", "lifter_avg_mae", "mape", "r2"]
    out = [f"# Results — {cfg['name']} ({'TEST, final' if final else 'VALIDATION only'})\n\n"]
    if cfg.get("synthetic"):
        out.append(SYNTH_BANNER)
    out.append("MAE in kg with 95% lifter-bootstrap CI. All rows within a comparison are identical across models.\n\n")
    for comp, g in m.groupby("comparison", sort=False):
        g = g.copy()
        g["label"] = g["run_id"].str.replace("__", " · ")
        out.append(f"## {comp} — partition `{g['partition'].iloc[0] if g['partition'].nunique() == 1 else ', '.join(g['partition'].unique())}`\n\n")
        for part, gp in g.groupby("partition", sort=False):
            if g["partition"].nunique() > 1:
                out.append(f"**{part}**\n\n")
            out.append(_md(gp[keep]) + "\n")
        p = pr[pr["comparison"] == comp]
        if len(p):
            p = p.assign(a=p["run_a"].str.replace("__", " · "), b=p["run_b"].str.replace("__", " · "))
            out.append("Paired MAE differences (a − b; negative = a better):\n\n"
                       + _md(p[["partition", "a", "b", "rows", "lifters", "mae_diff_a_minus_b", "ci_low", "ci_high"]]) + "\n")
    out.append("## Subgroups (protocol A, feature set D; protocol B LightGBM)\n\n")
    sg2 = sg[["run_id", "group_by", "group", "rows", "lifters", "mae", "mape", "r2", "sparse"]].copy()
    sg2["run_id"] = sg2["run_id"].str.replace("__", " · ")
    out.append(_md(sg2) + "\n")
    cov = tdir / "transfer_covariates.csv"
    if cov.exists():
        out.append("## Transfer covariate differences\n\n" + _md(pd.read_csv(cov)) + "\n")
    runs = pd.read_csv(tdir / "runs.csv")
    out.append("## Runs\n\n" + _md(runs.drop(columns=["selected"])) + "\n")
    path = rd / f"results_{tag}.md"
    path.write_text("".join(out))
    m.to_csv(rd / f"metrics_{tag}.csv", index=False)
    pr.to_csv(rd / f"paired_{tag}.csv", index=False)
    sg.to_csv(rd / f"subgroups_{tag}.csv", index=False)

    _plots(cfg, root, m, sg, figs, tag)
    print(f"wrote {path} and figures in {figs}")
    return path


def _plots(cfg, root, m, sg, figs, tag):
    title_sfx = " (SYNTHETIC)" if cfg.get("synthetic") else ""
    # model MAE comparison at feature set D
    d = m[m["comparison"] == "models_D"].copy()
    if len(d):
        d["name"] = d["model"] + np.where(d["model"] == "mlp", " s" + d["seed"].astype(str), "")
        fig, ax = plt.subplots(figsize=(6, 3.2))
        ax.barh(d["name"], d["mae"], xerr=[d["mae"] - d["mae_ci_low"], d["mae_ci_high"] - d["mae"]], color="#4C72B0")
        ax.set_xlabel("MAE (kg)"); ax.set_title(f"Protocol A, feature set D — {tag}{title_sfx}")
        fig.tight_layout(); fig.savefig(figs / f"model_mae_{tag}.png", dpi=200); plt.close(fig)
    # ablation
    a = m[(m["comparison"] == "ablation_core") & (m["model"] != "ratio")]
    if len(a):
        fig, ax = plt.subplots(figsize=(6, 3.4))
        for model, g in a.groupby("model"):
            ax.errorbar(g["feature_set"].str[0], g["mae"], yerr=[g["mae"] - g["mae_ci_low"], g["mae_ci_high"] - g["mae"]],
                        marker="o", capsize=3, label=model)
        r = m[(m["comparison"] == "ablation_core") & (m["model"] == "ratio")]
        if len(r):
            ax.axhline(r["mae"].iloc[0], ls="--", c="gray", label="ratio (squat×r_sex)")
        ax.set_xlabel("feature set (A squat · B +bench · C +BW/age/sex · D +equipment)"); ax.set_ylabel("MAE (kg)")
        ax.set_title(f"Feature ablation — {tag}{title_sfx}"); ax.legend(fontsize=7)
        fig.tight_layout(); fig.savefig(figs / f"ablation_{tag}.png", dpi=200); plt.close(fig)
    # subgroup errors
    s = sg[sg["run_id"].str.contains("ablation__A__D_plus_equipment__lightgbm")]
    if len(s):
        fig, axes = plt.subplots(1, 3, figsize=(10, 3.2), sharey=True)
        for ax, col in zip(axes, ["Sex", "bw_bin", "has_history"]):
            g = s[s["group_by"] == col]
            if col == "bw_bin":
                g = g.assign(_k=g["group"].map(lambda v: float(v.split("-")[0]) if v != "missing" else 1e9)).sort_values("_k")
            ax.bar(g["group"].astype(str), g["mae"], color=np.where(g["sparse"], "#DD8452", "#4C72B0"))
            ax.set_title(col); ax.tick_params(axis="x", rotation=45, labelsize=7)
        axes[0].set_ylabel("MAE (kg)")
        fig.suptitle(f"LightGBM (D) subgroup MAE — {tag}{title_sfx}; orange = sparse")
        fig.tight_layout(); fig.savefig(figs / f"subgroups_{tag}.png", dpi=200); plt.close(fig)
    # actual vs predicted and residuals for LightGBM D
    rid = "ablation__A__D_plus_equipment__lightgbm"
    pp = root / "runs" / rid / "predictions.parquet"
    if pp.exists():
        p = pd.read_parquet(pp)
        p = p[p["partition"] == ("test" if tag == "test" else "val")]
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        axes[0].hexbin(p["y"], p["yhat"], gridsize=80, bins="log", cmap="viridis", mincnt=1)
        lim = [0, max(p["y"].max(), p["yhat"].max())]
        axes[0].plot(lim, lim, c="red", lw=0.8); axes[0].set_xlabel("actual deadlift (kg)"); axes[0].set_ylabel("predicted (kg)")
        axes[1].hexbin(p["y"], p["y"] - p["yhat"], gridsize=80, bins="log", cmap="viridis", mincnt=1)
        axes[1].axhline(0, c="red", lw=0.8); axes[1].set_xlabel("actual deadlift (kg)"); axes[1].set_ylabel("residual: actual − predicted (kg)")
        fig.suptitle(f"LightGBM, protocol A, feature set D — {tag}{title_sfx}")
        fig.tight_layout(); fig.savefig(figs / f"actual_vs_pred_{tag}.png", dpi=200); plt.close(fig)
