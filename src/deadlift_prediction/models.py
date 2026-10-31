"""Models: squat-ratio baseline, last-deadlift baseline, (ridge) linear regression,
LightGBM, and a small PyTorch MLP. Each model owns its training-fitted
Preprocessor and serializes together with it."""

from __future__ import annotations

import copy
import os
import pickle
import time
from pathlib import Path

import numpy as np
import pandas as pd

from .features import Preprocessor, feature_spec
from .metrics import mae, pinball


class BaseModel:
    kind = "base"

    def __init__(self, feature_set: str, params: dict, seed: int = 42, min_count: int = 1):
        self.feature_set = feature_set
        self.params = params
        self.seed = seed
        self.min_count = min_count
        self.tuning: list[dict] = []
        self.selected: dict = {}

    def _prep(self, train: pd.DataFrame) -> None:
        spec = feature_spec(self.feature_set)
        self.prep = Preprocessor(spec["numeric"], spec["categorical"], min_count=self.min_count).fit(train)

    def fit(self, train: pd.DataFrame, y_train: np.ndarray, val: pd.DataFrame, y_val: np.ndarray) -> "BaseModel":
        raise NotImplementedError

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        raise NotImplementedError

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path: Path) -> "BaseModel":
        with open(path, "rb") as f:
            return pickle.load(f)


class RatioModel(BaseModel):
    """deadlift = r_sex * squat, r fitted by least squares through the origin
    (r = sum(s*d) / sum(s^2)) separately per Sex on training rows. Unseen or
    missing Sex falls back to the pooled training ratio. Uses squat and Sex only,
    regardless of the requested feature set."""

    kind = "ratio"

    def fit(self, train, y_train, val, y_val):
        s = train["Best3SquatKg"].to_numpy()
        self.pooled = float(np.sum(s * y_train) / np.sum(s * s))
        self.by_sex = {}
        for sex, idx in train.groupby("Sex").indices.items():
            self.by_sex[str(sex)] = float(np.sum(s[idx] * y_train[idx]) / np.sum(s[idx] ** 2))
        self.selected = {"objective": "least squares through origin", "pooled": self.pooled, "by_sex": self.by_sex}
        return self

    def predict(self, df):
        r = df["Sex"].astype("object").map(lambda v: self.by_sex.get(str(v), self.pooled) if pd.notna(v) else self.pooled)
        return df["Best3SquatKg"].to_numpy() * r.to_numpy(dtype="float64")


class LastDeadliftModel(BaseModel):
    """Predicts the lifter's previous eligible meet deadlift (history rows only)."""

    kind = "last_deadlift"

    def fit(self, train, y_train, val, y_val):
        self.selected = {"rule": "prediction = prev_deadlift"}
        return self

    def predict(self, df):
        return df["prev_deadlift"].to_numpy(dtype="float64")


class LinearModel(BaseModel):
    """Least squares on standardized numerics, missing indicators and one-hot
    categoricals. alpha=0 is ordinary least squares; alpha>0 is ridge. alpha is
    chosen by validation MAE from a small fixed grid."""

    kind = "linear"

    def fit(self, train, y_train, val, y_val):
        from sklearn.linear_model import LinearRegression, Ridge

        self._prep(train)
        Xtr, Xva = self.prep.dense(train), self.prep.dense(val)
        best = None
        for alpha in self.params.get("alphas", [0.0]):
            m = LinearRegression() if alpha == 0 else Ridge(alpha=alpha, random_state=self.seed)
            m.fit(Xtr, y_train)
            score = mae(y_val, m.predict(Xva))
            self.tuning.append({"alpha": alpha, "val_mae": score})
            if best is None or score < best[0]:
                best = (score, alpha, m)
        _, alpha, self.model = best
        self.selected = {"alpha": alpha, "coef": dict(zip(self.prep.dense_names(), map(float, self.model.coef_))),
                         "intercept": float(self.model.intercept_)}
        return self

    def predict(self, df):
        return self.model.predict(self.prep.dense(df))


class LightGBMModel(BaseModel):
    """LightGBM regression. Numerics are passed raw (NaN handled natively);
    categoricals as integer codes declared categorical, code 0 = unknown.
    Small grid; each candidate uses validation early stopping on L1. With
    objective="quantile" (follow-up #6) the model predicts the `alpha` quantile;
    early stopping and selection then use validation pinball loss.

    Objective follow-up: objective may be "regression_l1" or "huber"
    (`huber_delta` in kg). With target="ratio" the model fits deadlift / squat
    and predictions are multiplied back by squat. Rows are weighted by squat
    (L1/Huber) or squat^2 (L2) so the loss stays the kg-scale loss; selection
    always uses validation MAE in kg."""

    kind = "lightgbm"

    def fit(self, train, y_train, val, y_val):
        import lightgbm as lgb

        self._prep(train)
        Xtr, Xva = self.prep.tree_frame(train), self.prep.tree_frame(val)
        p = self.params
        grid = p.get("fixed_grid") or p["grid"]
        quantile = p["objective"] == "quantile"
        extra = {"alpha": p["alpha"]} if quantile else {}
        if p["objective"] == "huber":
            extra = {"alpha": p.get("huber_delta", 10.0)}
        metric = "quantile" if quantile else "l1"
        self.target = p.get("target", "kg")
        s_tr, s_va = train["Best3SquatKg"].to_numpy(float), val["Best3SquatKg"].to_numpy(float)
        if self.target == "ratio":
            power = 2 if p["objective"] == "regression" else 1
            fit_y, fit_yv = y_train / s_tr, y_val / s_va
            w_tr, w_va = s_tr ** power, s_va ** power
            if p["objective"] == "huber":
                extra = {"alpha": p.get("huber_delta", 10.0) / float(np.median(s_tr))}  # delta on ratio scale
        else:
            fit_y, fit_yv, w_tr, w_va = y_train, y_val, None, None
        best = None
        for cand in grid:
            m = lgb.LGBMRegressor(
                objective=p["objective"], learning_rate=p["learning_rate"], n_estimators=p["n_estimators"],
                random_state=self.seed, n_jobs=os.cpu_count(), verbose=-1, **extra, **cand,
            )
            t0 = time.time()
            m.fit(Xtr, fit_y, sample_weight=w_tr, eval_X=(Xva,), eval_y=(fit_yv,),
                  eval_sample_weight=None if w_va is None else [w_va], eval_metric=metric,
                  callbacks=[lgb.early_stopping(p["early_stopping_rounds"], verbose=False)])
            pred = m.predict(Xva, num_iteration=m.best_iteration_)
            if self.target == "ratio":
                pred = pred * s_va
            score = pinball(y_val, pred, p["alpha"]) if quantile else mae(y_val, pred)
            self.tuning.append({**cand, "best_iteration": int(m.best_iteration_ or p["n_estimators"]),
                                ("val_pinball" if quantile else "val_mae"): score, "seconds": time.time() - t0})
            if best is None or score < best[0]:
                best = (score, cand, m)
        _, cand, self.model = best
        self.selected = {"objective": p["objective"], **extra, "target": self.target, "learning_rate": p["learning_rate"], **cand,
                         "best_iteration": int(self.model.best_iteration_ or p["n_estimators"]),
                         "categorical_representation": "integer codes as LightGBM categorical; 0 = unknown/infrequent/missing",
                         "early_stopping": f"validation {metric}, patience {p['early_stopping_rounds']}"}
        return self

    def predict(self, df):
        pred = self.model.predict(self.prep.tree_frame(df), num_iteration=self.model.best_iteration_)
        if getattr(self, "target", "kg") == "ratio":
            pred = pred * df["Best3SquatKg"].to_numpy(float)
        return pred


class MLPModel(BaseModel):
    """Feed-forward net on the dense preprocessed matrix. Targets are standardized
    with training mean/std and predictions converted back to kg. Loss is L1 so the
    training objective matches the primary metric (MAE). Early stopping on
    validation MAE (kg); the best epoch's weights are restored."""

    kind = "mlp"

    def fit(self, train, y_train, val, y_val):
        import torch
        from torch import nn

        p = self.params
        torch.manual_seed(self.seed)
        np.random.seed(self.seed)
        self._prep(train)
        device = p.get("device", "auto")
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        Xtr = torch.from_numpy(self.prep.dense(train))
        Xva = torch.from_numpy(self.prep.dense(val)).to(device)
        self.y_mean, self.y_std = float(y_train.mean()), float(y_train.std() or 1.0)
        ytr = torch.from_numpy(((y_train - self.y_mean) / self.y_std).astype("float32"))

        layers, width = [], Xtr.shape[1]
        for h in p["hidden"]:
            layers += [nn.Linear(width, h), nn.ReLU()]
            if p.get("dropout"):
                layers.append(nn.Dropout(p["dropout"]))
            width = h
        layers.append(nn.Linear(width, 1))
        net = nn.Sequential(*layers).to(device)
        opt = torch.optim.Adam(net.parameters(), lr=p["lr"])
        loss_fn = nn.L1Loss() if p.get("loss", "l1") == "l1" else nn.MSELoss()
        gen = torch.Generator().manual_seed(self.seed)

        best, bad = (np.inf, None, -1), 0
        for epoch in range(p["max_epochs"]):
            net.train()
            t0 = time.time()
            perm = torch.randperm(len(Xtr), generator=gen)
            total = 0.0
            for i in range(0, len(perm), p["batch_size"]):
                idx = perm[i:i + p["batch_size"]]
                xb, yb = Xtr[idx].to(device), ytr[idx].to(device)
                opt.zero_grad()
                loss = loss_fn(net(xb).squeeze(1), yb)
                loss.backward()
                opt.step()
                total += loss.item() * len(idx)
            pred = self._forward(net, Xva)
            score = mae(y_val, pred)
            self.tuning.append({"epoch": epoch, "train_loss": total / len(perm), "val_mae": score, "seconds": time.time() - t0})
            if score < best[0] - 1e-6:
                best, bad = (score, copy.deepcopy(net.state_dict()), epoch), 0
            else:
                bad += 1
                if bad >= p["patience"]:
                    break
        net.load_state_dict(best[1])
        self.state = {k: v.cpu() for k, v in net.state_dict().items()}
        self.net = net.cpu().eval()
        self.selected = {"hidden": p["hidden"], "dropout": p.get("dropout", 0), "lr": p["lr"], "batch_size": p["batch_size"],
                         "loss": p.get("loss", "l1"), "best_epoch": best[2], "epochs_run": len(self.tuning),
                         "target_scaling": "standardized with training mean/std", "device": device}
        return self

    def _forward(self, net, X):
        import torch

        net.eval()
        out = []
        with torch.no_grad():
            for i in range(0, len(X), 65536):
                out.append(net(X[i:i + 65536]).squeeze(1).cpu().numpy())
        return np.concatenate(out).astype("float64") * self.y_std + self.y_mean

    def predict(self, df):
        import torch

        return self._forward(self.net, torch.from_numpy(self.prep.dense(df)))


MODEL_CLASSES = {c.kind: c for c in [RatioModel, LastDeadliftModel, LinearModel, LightGBMModel, MLPModel]}


def build_model(kind: str, feature_set: str, cfg: dict, seed: int, overrides: dict | None = None) -> BaseModel:
    params = dict(cfg["models"].get(kind, {}))
    params.update(overrides or {})
    min_count = cfg["features"]["federation_min_count"]
    return MODEL_CLASSES[kind](feature_set, params, seed=seed, min_count=min_count)
