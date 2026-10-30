"""Command line: download, prepare, train, evaluate, summarize, smoke."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import PROJECT_ROOT, load_config


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="deadlift", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add(name, help_):
        p = sub.add_parser(name, help=help_)
        p.add_argument("--config", default=str(PROJECT_ROOT / "configs" / "default.yaml"))
        return p

    p = add("download", "fetch and register the bulk CSV snapshot (once)")
    p.add_argument("--force", action="store_true", help="replace the registered snapshot")
    p.add_argument("--existing", type=Path, help="register an already-downloaded zip instead of fetching")
    add("prepare", "clean, audit, compute history, freeze splits")
    p = add("train", "fit all planned runs (skips finished runs)")
    p.add_argument("--experiment", action="append", choices=["ablation", "history", "chrono", "transfer", "capacity"])
    p.add_argument("--only", help="substring filter on run IDs")
    p.add_argument("--force", action="store_true")
    for name in ("evaluate", "summarize"):
        p = add(name, f"{name} saved predictions")
        p.add_argument("--final", action="store_true", help="score TEST partitions (only after configs are frozen)")
    sub.add_parser("smoke", help="full pipeline on the deterministic synthetic fixture")

    args = ap.parse_args(argv)
    if args.cmd == "smoke":
        smoke()
        return
    cfg = load_config(args.config)
    if args.cmd == "download":
        from .data import download
        download(cfg, force=args.force, existing=args.existing)
    elif args.cmd == "prepare":
        from .prepare import prepare
        prepare(cfg)
    elif args.cmd == "train":
        from .train import train
        train(cfg, experiments=args.experiment, force=args.force, only=args.only)
    elif args.cmd == "evaluate":
        from .evaluate import evaluate
        evaluate(cfg, final=args.final)
    elif args.cmd == "summarize":
        from .reporting import summarize_results
        summarize_results(cfg, final=args.final)


def smoke(config: str | Path | None = None) -> dict:
    """Synthetic end-to-end run. Its scores are NOT research findings."""
    from .evaluate import evaluate
    from .prepare import prepare
    from .reporting import summarize_results
    from .train import train

    cfg = load_config(config or PROJECT_ROOT / "configs" / "smoke.yaml")
    assert cfg["synthetic"], "smoke must use a synthetic config"
    summary = prepare(cfg)
    metas = train(cfg, force=True)
    for final in (False, True):
        evaluate(cfg, final=final)
        summarize_results(cfg, final=final)
    print(f"SMOKE OK (synthetic): {len(metas)} runs")
    return {"summary": summary, "runs": metas, "cfg": cfg}


if __name__ == "__main__":
    main()
