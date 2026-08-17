"""Label-free feature extraction for the frozen 001B exploratory protocol."""
from __future__ import annotations

import itertools
import math
from typing import Any

import numpy as np

PARAMS = {
    "distance_gate_m": 2500.0,
    "velocity_gate_mps": 80.0,
    "edge_weight_min": 0.35,
    "sigma_distance": 50.0,
    "sigma_velocity": 10.0,
    "sigma_acceleration": 1.0,
    "sigma_uncertainty": 50.0,
    "minimum_valid_history": 10,
    "logistic_regression_regularization": 1.0,
}
WINDOWS = (5, 15, 30)
PAIRS = tuple(itertools.combinations(range(4), 2))


def arrays(sample: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    tracks = sample["track_states"]
    p = np.array([[s["position_xyz"] for s in tr] for tr in tracks], dtype=float)
    v = np.array([[s["velocity_xyz"] for s in tr] for tr in tracks], dtype=float)
    a = np.array([[s["acceleration_xyz"] for s in tr] for tr in tracks], dtype=float)
    u = np.array([[s["state_uncertainty"] for s in tr] for tr in tracks], dtype=float)
    return p, v, a, u


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    den = float(np.linalg.norm(a) * np.linalg.norm(b))
    return float(np.dot(a, b) / den) if den > 1e-12 else 0.0


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, x))))


def pair_series(p: np.ndarray, v: np.ndarray, a: np.ndarray, i: int, j: int) -> dict[str, np.ndarray]:
    rp, rv, ra = p[i] - p[j], v[i] - v[j], a[i] - a[j]
    d = np.linalg.norm(rp, axis=1)
    headings = np.array([cosine(v[i, k], v[j, k]) for k in range(len(v[i]))])
    vel_norm = np.linalg.norm(rv, axis=1)
    acc_norm = np.linalg.norm(ra, axis=1)
    return {"distance": d, "relative_velocity": rv, "relative_speed": vel_norm,
            "relative_acceleration": ra, "acceleration_norm": acc_norm, "heading": headings}


def baseline_window(p: np.ndarray, v: np.ndarray, a: np.ndarray, w: int) -> tuple[np.ndarray, list[str]]:
    values = []
    for i, j in PAIRS:
        s = pair_series(p, v, a, i, j)
        values.append([float(np.mean(s["distance"][-w:])), float(np.var(s["distance"][-w:])),
                       float(np.var((p[i, -w:] - p[j, -w:]), axis=0).mean()),
                       float(np.mean(s["heading"][-w:])),
                       float(np.mean(np.exp(-s["relative_speed"][-w:] / 10.0))),
                       float(np.mean(np.exp(-s["acceleration_norm"][-w:] / 1.0))),
                       0.0, 0.0])
    x = np.array(values)
    centroid_v = np.linalg.norm(np.mean(v[:, -w:], axis=0))
    speed_spread = np.std(np.linalg.norm(v[:, -w:], axis=2))
    x[:, 6] = np.clip(1.0 - speed_spread / 8.0, 0.0, 1.0)
    all_d = np.array([pair_series(p, v, a, i, j)["distance"][-w:] for i, j in PAIRS])
    x[:, 7] = np.mean(np.abs(np.diff(all_d, axis=1)) < 35.0)
    names = ["mean_pairwise_distance", "variance_pairwise_distance", "relative_position_variance",
             "heading_correlation", "velocity_correlation", "acceleration_correlation",
             "centroid_coherence", "formation_persistence"]
    return x.mean(axis=0), [f"{n}_w{w}" for n in names]


def edge_score(series: dict[str, np.ndarray], uncertainty: float, w: int) -> float:
    d = series["distance"][-w:]
    rv = series["relative_velocity"][-w:]
    ra = series["relative_acceleration"][-w:]
    q_distance = math.exp(-float(np.var(d)) / PARAMS["sigma_distance"] ** 2)
    med = np.median(rv, axis=0)
    q_velocity = math.exp(-float(np.mean(np.sum((rv - med) ** 2, axis=1))) / PARAMS["sigma_velocity"] ** 2)
    q_heading = float(np.mean((1.0 + series["heading"][-w:]) / 2.0))
    q_acc = math.exp(-float(np.mean(np.sum(ra ** 2, axis=1))) / PARAMS["sigma_acceleration"] ** 2)
    q_geometry = float(np.mean(np.abs(np.diff(d)) < 35.0)) if len(d) > 1 else 0.0
    q_unc = math.exp(-uncertainty / PARAMS["sigma_uncertainty"])
    return float(np.mean([q_distance, q_velocity, q_heading, q_acc, q_geometry, q_unc]))


def graph_at(p: np.ndarray, v: np.ndarray, a: np.ndarray, u: np.ndarray, t: int, w: int) -> tuple[np.ndarray, dict[str, float], dict[str, float]]:
    n = 4
    A = np.zeros((n, n), dtype=float)
    edge_weights = []
    for i, j in PAIRS:
        s = pair_series(p, v, a, i, j)
        d_now = float(s["distance"][t])
        rel_speed = float(s["relative_speed"][t])
        unc = float(np.mean(np.sqrt(np.sum(u[[i, j], max(0, t - w + 1):t + 1] ** 2, axis=2))))
        score = edge_score({k: v0[:t + 1] for k, v0 in s.items()}, unc, min(w, t + 1)) if t + 1 >= PARAMS["minimum_valid_history"] else 0.0
        if d_now <= PARAMS["distance_gate_m"] and rel_speed <= PARAMS["velocity_gate_mps"] and score >= PARAMS["edge_weight_min"]:
            A[i, j] = A[j, i] = score
            edge_weights.append(score)
    deg = A.sum(axis=1)
    diag = np.diag(deg)
    inv = np.diag(1.0 / np.sqrt(np.maximum(deg, 1e-12)))
    L = np.eye(n) - inv @ A @ inv
    eig = np.linalg.eigvalsh(L) if edge_weights else np.zeros(n)
    spectral = {"spectral_gap": float(eig[1] - eig[0]) if len(eig) > 1 else 0.0,
                "spectral_q25": float(np.quantile(eig, .25)), "spectral_q50": float(np.quantile(eig, .50)),
                "spectral_q75": float(np.quantile(eig, .75)), "laplacian_std": float(np.std(eig)),
                "connectivity": float(np.count_nonzero(deg) / n),
                "clustering": float(np.mean([A[i, j] * A[j, k] * A[k, i] for i, j, k in [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)] ])),
                "temporal_spectral_change": 0.0}
    relational = {"edge_count": float(len(edge_weights)), "edge_node_ratio": float(len(edge_weights) / n),
                  "mean_edge_weight": float(np.mean(edge_weights)) if edge_weights else 0.0,
                  "degree_mean": float(np.mean(deg)), "connected_structure": float(np.count_nonzero(deg) >= 2),
                  "edge_persistence": 0.0, "edge_weight_variance": float(np.var(edge_weights)) if edge_weights else 0.0,
                  "relation_lifetime": 0.0, "topology_change_rate": 0.0, "relative_geometry_stability": 0.0}
    return A, relational, spectral


def relational_window(p: np.ndarray, v: np.ndarray, a: np.ndarray, u: np.ndarray, w: int) -> tuple[np.ndarray, list[str], np.ndarray, np.ndarray]:
    rel_rows, spec_rows, matrices = [], [], []
    # Five-second evaluation stride keeps the exploratory run tractable while
    # retaining the frozen 5/15/30 s temporal windows and transitions.
    indices = list(range(PARAMS["minimum_valid_history"] - 1, len(p[0]), 5))
    if indices[-1] != len(p[0]) - 1:
        indices.append(len(p[0]) - 1)
    for t in indices:
        A, rel, spec = graph_at(p, v, a, u, t, w)
        matrices.append(A)
        rel_rows.append(list(rel.values()))
        spec_rows.append(list(spec.values()))
    rel_arr, spec_arr = np.array(rel_rows), np.array(spec_rows)
    if len(matrices) > 1:
        changes = [np.count_nonzero(matrices[k] != matrices[k - 1]) / 2.0 for k in range(1, len(matrices))]
        rel_arr[:, 5] = np.mean(changes)
        rel_arr[:, 8] = np.mean(changes)
        rel_arr[:, 6] = np.mean([np.mean(m > 0) for m in matrices], axis=0) if False else rel_arr[:, 6]
        spec_arr[:, -1] = np.mean([np.linalg.norm(matrices[k] - matrices[k - 1]) for k in range(1, len(matrices))])
    names_rel = ["edge_count", "edge_node_ratio", "mean_edge_weight", "degree_mean", "connected_structure",
                 "edge_persistence", "edge_weight_variance", "relation_lifetime", "topology_change_rate", "relative_geometry_stability"]
    names_spec = ["spectral_gap", "spectral_q25", "spectral_q50", "spectral_q75", "laplacian_std", "connectivity", "clustering", "temporal_spectral_change"]
    return np.concatenate([np.mean(rel_arr, axis=0), np.std(rel_arr, axis=0)]), [f"{n}_w{w}" for n in names_rel] * 2, np.concatenate([np.mean(spec_arr, axis=0), np.std(spec_arr, axis=0)]), [f"{n}_w{w}" for n in names_spec] * 2


def extract(sample: dict[str, Any]) -> dict[str, Any]:
    p, v, a, u = arrays(sample)
    baseline, bnames = [], []
    rel, rnames, spec, snames = [], [], [], []
    for w in WINDOWS:
        x, n = baseline_window(p, v, a, w); baseline.extend(x); bnames.extend(n)
        x, n, z, zn = relational_window(p, v, a, u, w); rel.extend(x); rnames.extend(n); spec.extend(z); snames.extend(zn)
    return {"baseline": np.array(baseline), "baseline_names": bnames,
            "relational": np.array(rel), "relational_names": rnames,
            "spectral": np.array(spec), "spectral_names": snames}
