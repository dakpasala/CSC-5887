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


class EmbedMLPModel(BaseModel):
    """MLP with learned per-feature embeddings (deep-learning architecture follow-up).

    Numeric features (training-median imputed, standardized with training
    statistics) each get a periodic "PLR" embedding (Gorishniy et al., 2022):
    v = [sin(2*pi*c*x), cos(2*pi*c*x)] with k learnable frequencies c per feature
    (initialised N(0, frequency_scale)), then a per-feature Linear(2k -> d) + ReLU.
    Missing-value indicators are appended as plain inputs. Each categorical gets
    an nn.Embedding (code 0 = unknown/infrequent/missing). The concatenation feeds
    an MLP with ReLU and dropout. Training matches MLPModel: standardized target,
    L1 loss, Adam, early stopping on validation MAE (kg), best epoch restored."""

    kind = "embed_mlp"

    def _inputs(self, df):
        import torch

        num = self.prep.numeric_raw(df)
        mu = np.array([self.prep.means[c] for c in self.prep.numeric])
        sd = np.array([self.prep.stds[c] for c in self.prep.numeric])
        num = ((num - mu) / sd).astype("float32")
        ind = self.prep.indicators(df).astype("float32")
        codes = self.prep.codes(df).astype("int64")
        return torch.from_numpy(num), torch.from_numpy(ind), torch.from_numpy(codes)

    def _build(self):
        import torch
        from torch import nn

        p = self.params
        n_num, n_ind = len(self.prep.numeric), len(self.prep.indicator_cols)
        k, d, d_cat = p["n_frequencies"], p["d_embedding"], p["d_cat"]
        vocab = [len(self.prep.vocab[c]) + 1 for c in self.prep.categorical]

        class Net(nn.Module):
            def __init__(self):
                super().__init__()
                self.freq = nn.Parameter(torch.randn(n_num, k) * p["frequency_scale"])
                self.w = nn.Parameter(torch.randn(n_num, 2 * k, d) / np.sqrt(2 * k))
                self.b = nn.Parameter(torch.zeros(n_num, d))
                self.cats = nn.ModuleList([nn.Embedding(v, d_cat) for v in vocab])
                width = n_num * d + n_ind + len(vocab) * d_cat
                layers = []
                for h in p["hidden"]:
                    layers += [nn.Linear(width, h), nn.ReLU()]
                    if p.get("dropout"):
                        layers.append(nn.Dropout(p["dropout"]))
                    width = h
                layers.append(nn.Linear(width, 1))
                self.mlp = nn.Sequential(*layers)

            def forward(self, num, ind, codes):
                z = 2 * np.pi * num.unsqueeze(-1) * self.freq          # (B, F, k)
                z = torch.cat([torch.sin(z), torch.cos(z)], dim=-1)     # (B, F, 2k)
                e = torch.relu(torch.einsum("bfk,fkd->bfd", z, self.w) + self.b)
                parts = [e.flatten(1), ind] + [emb(codes[:, j]) for j, emb in enumerate(self.cats)]
                return self.mlp(torch.cat(parts, dim=1)).squeeze(1)

        return Net()

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
        tr = self._inputs(train)
        va = tuple(t.to(device) for t in self._inputs(val))
        self.y_mean, self.y_std = float(y_train.mean()), float(y_train.std() or 1.0)
        ytr = torch.from_numpy(((y_train - self.y_mean) / self.y_std).astype("float32"))
        net = self._build().to(device)
        opt = torch.optim.Adam(net.parameters(), lr=p["lr"])
        loss_fn = nn.L1Loss() if p.get("loss", "l1") == "l1" else nn.MSELoss()
        gen = torch.Generator().manual_seed(self.seed)
        best, bad = (np.inf, None, -1), 0
        for epoch in range(p["max_epochs"]):
            net.train()
            t0 = time.time()
            perm = torch.randperm(len(ytr), generator=gen)
            total = 0.0
            for i in range(0, len(perm), p["batch_size"]):
                idx = perm[i:i + p["batch_size"]]
                opt.zero_grad()
                loss = loss_fn(net(*(t[idx].to(device) for t in tr)), ytr[idx].to(device))
                loss.backward()
                opt.step()
                total += loss.item() * len(idx)
            score = mae(y_val, self._forward(net, va))
            self.tuning.append({"epoch": epoch, "train_loss": total / len(perm), "val_mae": score, "seconds": time.time() - t0})
            if score < best[0] - 1e-6:
                best, bad = (score, copy.deepcopy(net.state_dict()), epoch), 0
            else:
                bad += 1
                if bad >= p["patience"]:
                    break
        net.load_state_dict(best[1])
        self.net = net.cpu().eval()
        n_params = sum(t.numel() for t in self.net.parameters())
        self.selected = {k: p[k] for k in ["hidden", "dropout", "lr", "batch_size", "loss", "n_frequencies",
                                           "frequency_scale", "d_embedding", "d_cat"]}
        self.selected.update({"best_epoch": best[2], "epochs_run": len(self.tuning), "parameters": int(n_params),
                              "target_scaling": "standardized with training mean/std", "device": device,
                              "numeric_embedding": "periodic PLR (Gorishniy et al. 2022)"})
        return self

    def _forward(self, net, inputs):
        import torch

        net.eval()
        n = len(inputs[0])
        out = []
        with torch.no_grad():
            for i in range(0, n, 65536):
                out.append(net(*(t[i:i + 65536] for t in inputs)).cpu().numpy())
        return np.concatenate(out).astype("float64") * self.y_std + self.y_mean

    def predict(self, df):
        return self._forward(self.net, self._inputs(df))

    # The network class is built inside _build (torch is imported lazily so the
    # LightGBM process never loads it), so pickling stores weights as arrays and
    # rebuilds the network on load.
    def __getstate__(self):
        state = self.__dict__.copy()
        net = state.pop("net", None)
        if net is not None:
            state["_weights"] = {k: v.detach().cpu().numpy() for k, v in net.state_dict().items()}
        return state

    def __setstate__(self, state):
        weights = state.pop("_weights", None)
        self.__dict__.update(state)
        if weights is not None:
            import torch

            net = self._build()
            net.load_state_dict({k: torch.from_numpy(v) for k, v in weights.items()})
            self.net = net.eval()


_SEQ_TABLES: dict[str, pd.DataFrame] = {}


def _seq_table(path: str) -> pd.DataFrame:
    if path not in _SEQ_TABLES:
        _SEQ_TABLES[path] = pd.read_parquet(path)
    return _SEQ_TABLES[path]


class GRUModel(BaseModel):
    """Sequence model over a lifter's earlier meets (deep-learning follow-up).

    Input 1: the last `seq_len` lifter-days of deadlift history from any event,
    strictly before the target date (features.build_sequences), read by a GRU.
    Input 2: the current meet's preprocessed static features (same dense matrix
    as MLPModel for the run's feature set). The GRU's final hidden state is
    concatenated with a projection of the static features and fed to an MLP.
    Training matches the other networks: standardized target, L1, Adam,
    validation early stopping on MAE (kg). Sequence features use fixed scalings,
    so nothing in them is fitted on non-training rows."""

    kind = "gru"
    SELECTED_KEYS = ["seq_len", "gru_hidden", "static_hidden", "hidden", "dropout", "lr", "batch_size"]

    def _inputs(self, df):
        import torch

        from .features import build_sequences

        seq = build_sequences(df, _seq_table(self.params["seq_table"]), self.params["seq_len"])
        return torch.from_numpy(seq), torch.from_numpy(self.prep.dense(df))

    def _build(self, n_static: int):
        import torch
        from torch import nn

        from .features import SEQ_STEP_FEATURES

        p = self.params

        class Net(nn.Module):
            def __init__(self):
                super().__init__()
                self.gru = nn.GRU(len(SEQ_STEP_FEATURES), p["gru_hidden"], num_layers=p.get("gru_layers", 1), batch_first=True)
                self.static = nn.Sequential(nn.Linear(n_static, p["static_hidden"]), nn.ReLU())
                layers, width = [], p["gru_hidden"] + p["static_hidden"]
                for h in p["hidden"]:
                    layers += [nn.Linear(width, h), nn.ReLU()]
                    if p.get("dropout"):
                        layers.append(nn.Dropout(p["dropout"]))
                    width = h
                layers.append(nn.Linear(width, 1))
                self.head = nn.Sequential(*layers)

            def forward(self, seq, static):
                _, h = self.gru(seq)
                return self.head(torch.cat([h[-1], self.static(static)], dim=1)).squeeze(1)

        return Net()

    def fit(self, train, y_train, val, y_val):
        import torch
        from torch import nn

        p = self.params
        torch.manual_seed(self.seed)
        np.random.seed(self.seed)
        torch.set_num_threads(os.cpu_count() or 1)
        self._prep(train)
        device = p.get("device", "auto")
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        tr = self._inputs(train)
        va = tuple(t.to(device) for t in self._inputs(val))
        self.n_static = tr[1].shape[1]
        self.y_mean, self.y_std = float(y_train.mean()), float(y_train.std() or 1.0)
        ytr = torch.from_numpy(((y_train - self.y_mean) / self.y_std).astype("float32"))
        net = self._build(self.n_static).to(device)
        opt = torch.optim.Adam(net.parameters(), lr=p["lr"])
        loss_fn = nn.L1Loss()
        gen = torch.Generator().manual_seed(self.seed)
        best, bad = (np.inf, None, -1), 0
        for epoch in range(p["max_epochs"]):
            net.train()
            t0 = time.time()
            perm = torch.randperm(len(ytr), generator=gen)
            total = 0.0
            for i in range(0, len(perm), p["batch_size"]):
                idx = perm[i:i + p["batch_size"]]
                opt.zero_grad()
                loss = loss_fn(net(tr[0][idx].to(device), tr[1][idx].to(device)), ytr[idx].to(device))
                loss.backward()
                opt.step()
                total += loss.item() * len(idx)
            score = mae(y_val, self._forward(net, va))
            self.tuning.append({"epoch": epoch, "train_loss": total / len(perm), "val_mae": score, "seconds": time.time() - t0})
            print(f"    {self.kind} epoch {epoch}: val MAE {score:.3f} ({time.time() - t0:.0f}s)", flush=True)
            if score < best[0] - 1e-6:
                best, bad = (score, copy.deepcopy(net.state_dict()), epoch), 0
            else:
                bad += 1
                if bad >= p["patience"]:
                    break
        net.load_state_dict(best[1])
        self.net = net.cpu().eval()
        self.selected = {k: p[k] for k in self.SELECTED_KEYS}
        self.selected.update({"best_epoch": best[2], "epochs_run": len(self.tuning), "loss": "l1",
                              "parameters": int(sum(t.numel() for t in self.net.parameters())), "device": device,
                              "sequence": "last seq_len lifter-days of any-event deadlift history, strictly earlier"})
        return self

    def _forward(self, net, inputs):
        import torch

        net.eval()
        out = []
        with torch.no_grad():
            for i in range(0, len(inputs[0]), 32768):
                out.append(net(inputs[0][i:i + 32768], inputs[1][i:i + 32768]).cpu().numpy())
        return np.concatenate(out).astype("float64") * self.y_std + self.y_mean

    def predict(self, df):
        return self._forward(self.net, self._inputs(df))

    def __getstate__(self):
        state = self.__dict__.copy()
        net = state.pop("net", None)
        if net is not None:
            state["_weights"] = {k: v.detach().cpu().numpy() for k, v in net.state_dict().items()}
        return state

    def __setstate__(self, state):
        weights = state.pop("_weights", None)
        self.__dict__.update(state)
        if weights is not None:
            import torch

            net = self._build(self.n_static)
            net.load_state_dict({k: torch.from_numpy(v) for k, v in weights.items()})
            self.net = net.eval()


class ResNetMLPModel(BaseModel):
    """Tabular ResNet (Gorishniy et al., 2021), architecture follow-up.

    Input: the same dense preprocessed matrix as MLPModel. Linear(d_in -> d),
    then n_blocks residual blocks x + Dropout(Linear(Dropout(ReLU(Linear(BN(x)))))),
    then BN -> ReLU -> Linear(d -> 1). Training matches the other networks:
    standardized target, L1, Adam, validation early stopping on MAE (kg)."""

    kind = "resnet_mlp"

    def _build(self, d_in: int):
        import torch
        from torch import nn

        p = self.params

        class Block(nn.Module):
            def __init__(self):
                super().__init__()
                self.f = nn.Sequential(nn.BatchNorm1d(p["d"]), nn.Linear(p["d"], p["d_hidden"]), nn.ReLU(),
                                       nn.Dropout(p["dropout_hidden"]), nn.Linear(p["d_hidden"], p["d"]),
                                       nn.Dropout(p["dropout_residual"]))

            def forward(self, x):
                return x + self.f(x)

        class Net(nn.Module):
            def __init__(self):
                super().__init__()
                self.inp = nn.Linear(d_in, p["d"])
                self.blocks = nn.Sequential(*[Block() for _ in range(p["n_blocks"])])
                self.out = nn.Sequential(nn.BatchNorm1d(p["d"]), nn.ReLU(), nn.Linear(p["d"], 1))

            def forward(self, x):
                return self.out(self.blocks(self.inp(x))).squeeze(1)

        return Net()

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
        Xtr = torch.from_numpy(self.prep.dense(train))
        Xva = torch.from_numpy(self.prep.dense(val)).to(device)
        self.d_in = Xtr.shape[1]
        self.y_mean, self.y_std = float(y_train.mean()), float(y_train.std() or 1.0)
        ytr = torch.from_numpy(((y_train - self.y_mean) / self.y_std).astype("float32"))
        net = self._build(self.d_in).to(device)
        opt = torch.optim.Adam(net.parameters(), lr=p["lr"])
        loss_fn = nn.L1Loss()
        gen = torch.Generator().manual_seed(self.seed)
        best, bad = (np.inf, None, -1), 0
        for epoch in range(p["max_epochs"]):
            net.train()
            t0 = time.time()
            perm = torch.randperm(len(Xtr), generator=gen)
            total = 0.0
            for i in range(0, len(perm), p["batch_size"]):
                idx = perm[i:i + p["batch_size"]]
                if len(idx) < 2:
                    continue  # BatchNorm needs > 1 row
                opt.zero_grad()
                loss = loss_fn(net(Xtr[idx].to(device)), ytr[idx].to(device))
                loss.backward()
                opt.step()
                total += loss.item() * len(idx)
            score = mae(y_val, self._forward(net, Xva))
            self.tuning.append({"epoch": epoch, "train_loss": total / len(perm), "val_mae": score, "seconds": time.time() - t0})
            if score < best[0] - 1e-6:
                best, bad = (score, copy.deepcopy(net.state_dict()), epoch), 0
            else:
                bad += 1
                if bad >= p["patience"]:
                    break
        net.load_state_dict(best[1])
        self.net = net.cpu().eval()
        self.selected = {k: p[k] for k in ["d", "d_hidden", "n_blocks", "dropout_hidden", "dropout_residual", "lr", "batch_size"]}
        self.selected.update({"best_epoch": best[2], "epochs_run": len(self.tuning), "loss": "l1", "device": device,
                              "parameters": int(sum(t.numel() for t in self.net.parameters()))})
        return self

    def _forward(self, net, X):
        import torch

        net.eval()
        out = []
        with torch.no_grad():
            for i in range(0, len(X), 65536):
                out.append(net(X[i:i + 65536]).cpu().numpy())
        return np.concatenate(out).astype("float64") * self.y_std + self.y_mean

    def predict(self, df):
        import torch

        return self._forward(self.net, torch.from_numpy(self.prep.dense(df)))

    def __getstate__(self):
        state = self.__dict__.copy()
        net = state.pop("net", None)
        if net is not None:
            state["_weights"] = {k: v.detach().cpu().numpy() for k, v in net.state_dict().items()}
        return state

    def __setstate__(self, state):
        weights = state.pop("_weights", None)
        self.__dict__.update(state)
        if weights is not None:
            import torch

            net = self._build(self.d_in)
            net.load_state_dict({k: torch.from_numpy(v) for k, v in weights.items()})
            self.net = net.eval()


class CatBoostModel(BaseModel):
    """CatBoost regression (follow-up). Numerics passed raw (NaN handled
    natively); categoricals passed as native CatBoost categorical features using
    the training-fitted codes (0 = unknown/infrequent/missing), so CatBoost's
    ordered target statistics see only training rows. Huber loss (as the best
    LightGBM), early stopping on validation MAE."""

    kind = "catboost"

    def _pool(self, df, y=None):
        from catboost import Pool

        X = self.prep.tree_frame(df)
        for c in self.prep.categorical:
            X[c] = X[c].astype("int64")
        return Pool(X, label=y, cat_features=list(self.prep.categorical) or None)

    def fit(self, train, y_train, val, y_val):
        from catboost import CatBoostRegressor

        self._prep(train)
        p = self.params
        loss = f"Huber:delta={p['huber_delta']}" if p.get("loss", "huber") == "huber" else "RMSE"
        self.model = CatBoostRegressor(
            loss_function=loss, eval_metric="MAE", iterations=p["iterations"], learning_rate=p["learning_rate"],
            depth=p["depth"], l2_leaf_reg=p["l2_leaf_reg"], border_count=p.get("border_count", 254),
            random_seed=self.seed, thread_count=os.cpu_count(), od_type="Iter", od_wait=p["od_wait"],
            use_best_model=True, verbose=0, allow_writing_files=False,
        )
        t0 = time.time()
        self.model.fit(self._pool(train, y_train), eval_set=self._pool(val, y_val))
        score = mae(y_val, self.model.predict(self._pool(val)))
        self.tuning.append({"val_mae": score, "best_iteration": int(self.model.get_best_iteration()), "seconds": time.time() - t0})
        self.selected = {"loss": loss, "learning_rate": p["learning_rate"], "depth": p["depth"], "l2_leaf_reg": p["l2_leaf_reg"],
                         "best_iteration": int(self.model.get_best_iteration()),
                         "categorical_representation": "native CatBoost categorical on training-fitted codes",
                         "early_stopping": f"validation MAE, patience {p['od_wait']}"}
        return self

    def predict(self, df):
        return self.model.predict(self._pool(df))


class SeqTransformerModel(GRUModel):
    """Transformer encoder over the same past-meet sequences as GRUModel
    (sequence follow-up). Each step is projected to d_model and given a learned
    position embedding; padded steps are masked out of attention and out of the
    masked-mean pooling. Static features, head, training, and serialization are
    inherited from GRUModel."""

    kind = "seq_transformer"
    SELECTED_KEYS = ["seq_len", "d_model", "n_heads", "n_layers", "d_ff", "static_hidden", "hidden", "dropout", "lr", "batch_size"]

    def _build(self, n_static: int):
        import torch
        from torch import nn

        from .features import SEQ_STEP_FEATURES

        p = self.params
        real = SEQ_STEP_FEATURES.index("is_real")

        class Net(nn.Module):
            def __init__(self):
                super().__init__()
                self.proj = nn.Linear(len(SEQ_STEP_FEATURES), p["d_model"])
                self.pos = nn.Parameter(torch.zeros(p["seq_len"], p["d_model"]))
                layer = nn.TransformerEncoderLayer(p["d_model"], p["n_heads"], p["d_ff"], p["dropout"], batch_first=True)
                self.enc = nn.TransformerEncoder(layer, p["n_layers"], enable_nested_tensor=False)
                self.static = nn.Sequential(nn.Linear(n_static, p["static_hidden"]), nn.ReLU())
                layers, width = [], p["d_model"] + p["static_hidden"]
                for h in p["hidden"]:
                    layers += [nn.Linear(width, h), nn.ReLU()]
                    if p.get("dropout"):
                        layers.append(nn.Dropout(p["dropout"]))
                    width = h
                layers.append(nn.Linear(width, 1))
                self.head = nn.Sequential(*layers)

            def forward(self, seq, static):
                valid = seq[..., real] > 0.5                        # (B, L)
                valid[:, -1] |= ~valid.any(dim=1)                   # never fully masked (avoids NaN attention)
                z = self.enc(self.proj(seq) + self.pos, src_key_padding_mask=~valid)
                w = valid.unsqueeze(-1).float()
                pooled = (z * w).sum(1) / w.sum(1).clamp(min=1.0)
                return self.head(torch.cat([pooled, self.static(static)], dim=1)).squeeze(1)

        return Net()


MODEL_CLASSES = {c.kind: c for c in [RatioModel, LastDeadliftModel, LinearModel, LightGBMModel, MLPModel, EmbedMLPModel,
                                     GRUModel, ResNetMLPModel, SeqTransformerModel, CatBoostModel]}
TORCH_MODELS = {"mlp", "embed_mlp", "gru", "resnet_mlp", "seq_transformer"}


def build_model(kind: str, feature_set: str, cfg: dict, seed: int, overrides: dict | None = None) -> BaseModel:
    params = dict(cfg["models"].get(kind, {}))
    params.update(overrides or {})
    if kind in ("gru", "seq_transformer"):
        from .config import processed_dir

        params.setdefault("seq_table", str(processed_dir(cfg) / "seq_table.parquet"))
    min_count = cfg["features"]["federation_min_count"]
    return MODEL_CLASSES[kind](feature_set, params, seed=seed, min_count=min_count)
