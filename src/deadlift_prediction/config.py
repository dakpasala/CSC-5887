"""YAML config loading with single-level `base:` inheritance and run metadata helpers."""

from __future__ import annotations

import copy
import hashlib
import json
import platform
from importlib import metadata
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _deep_merge(base: dict, override: dict) -> dict:
    out = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = copy.deepcopy(value)
    return out


def load_config(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    with open(path) as f:
        cfg = yaml.safe_load(f) or {}
    base = cfg.pop("base", None)
    if base:
        cfg = _deep_merge(load_config(path.parent / base), cfg)
    cfg.setdefault("synthetic", False)
    cfg["_config_path"] = str(path)
    return cfg


def resolve(cfg: dict, key: str) -> Path:
    """Resolve a path-valued config entry relative to the project root."""
    node: Any = cfg
    for part in key.split("."):
        node = node[part]
    p = Path(node)
    return p if p.is_absolute() else PROJECT_ROOT / p


def processed_dir(cfg: dict) -> Path:
    """Processed data lives in a per-config folder so subsets never overwrite each other."""
    base = resolve(cfg, "data.processed_dir")
    return base if cfg.get("synthetic") else base / cfg["name"]


def artifacts_dir(cfg: dict) -> Path:
    base = resolve(cfg, "artifacts_dir")
    return base if cfg.get("synthetic") else base / cfg["name"]


def reports_dir(cfg: dict) -> Path:
    base = resolve(cfg, "reports_dir")
    return base if cfg.get("synthetic") else base / cfg["name"]


def config_hash(cfg: dict) -> str:
    clean = {k: v for k, v in cfg.items() if not k.startswith("_")}
    return hashlib.sha256(json.dumps(clean, sort_keys=True, default=str).encode()).hexdigest()[:12]


def package_versions() -> dict[str, str]:
    out = {"python": platform.python_version(), "platform": platform.platform()}
    for pkg in ["numpy", "pandas", "pyarrow", "scikit-learn", "lightgbm", "torch", "matplotlib", "seaborn"]:
        try:
            out[pkg] = metadata.version(pkg)
        except metadata.PackageNotFoundError:
            out[pkg] = "not installed"
    return out


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, default=str)


def read_json(path: Path) -> Any:
    with open(path) as f:
        return json.load(f)
