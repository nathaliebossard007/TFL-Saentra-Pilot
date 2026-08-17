"""Prediction stage: reads algorithm-visible samples only and writes raw predictions."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from relational_features import extract, sigmoid

ROOT = Path(__file__).resolve().parents[1]
ALG_ROOT = ROOT / "data" / "algorithm_visible"
PRED_ROOT = ROOT / "results" / "exploratory" / "predictions"


def quality(value: float, name: str) -> float:
    n = name.lower()
    if "correlation" in n or "coherence" in n:
        return float(np.clip((value + 1.0) / 2.0, 0.0, 1.0))
    if any(k in n for k in ["variance", "change_rate", "std"]):
        return float(1.0 / (1.0 + abs(value)))
    if "distance" in n and "mean" in n:
        return 0.5  # proximity is deliberately non-discriminative in the fixed score
    if "edge_count" in n or "degree_mean" in n or "ratio" in n:
        return float(np.clip(value / 6.0, 0.0, 1.0))
    if "spectral_gap" in n:
        return float(np.clip(abs(value), 0.0, 1.0))
    if "connectivity" in n or "persistence" in n or "lifetime" in n or "stability" in n or "weight" in n or "clustering" in n:
        return float(np.clip(value, 0.0, 1.0))
    return float(1.0 / (1.0 + abs(value)))


def fixed_logistic(values: np.ndarray, names: list[str]) -> float:
    if len(values) == 0:
        return 0.5
    q = np.array([quality(float(v), n) for v, n in zip(values, names)])
    # Fixed, label-free logistic score. Coefficients are not fitted from evaluator truth.
    return sigmoid(5.0 * (float(np.mean(q)) - 0.5))


def select(features: dict, kind: str) -> tuple[np.ndarray, list[str]]:
    b, bn = features["baseline"], features["baseline_names"]
    r, rn = features["relational"], features["relational_names"]
    s, sn = features["spectral"], features["spectral_names"]
    if kind == "A_conventional_kinematic_baseline": return b, bn
    if kind == "B_temporal_relational_no_spectral": return r, rn
    if kind == "C_temporal_relational_with_spectral": return np.r_[r, s], rn + sn
    if kind == "geometry_only":
        keep = [i for i, n in enumerate(bn) if "distance" in n or "position" in n or "formation" in n]
        return b[keep], [bn[i] for i in keep]
    if kind == "instantaneous_kinematics_only":
        keep = [i for i, n in enumerate(bn) if "heading" in n or "velocity" in n or "acceleration" in n]
        return b[keep], [bn[i] for i in keep]
    if kind == "temporal_relation_only":
        keep = [i for i, n in enumerate(rn) if any(k in n for k in ["persistence", "lifetime", "change", "stability", "coherence"])]
        return r[keep], [rn[i] for i in keep]
    if kind == "spectral_only": return s, sn
    if kind == "relation_plus_temporal": return r, rn
    if kind == "relation_plus_temporal_plus_spectral": return np.r_[r, s], rn + sn
    raise ValueError(kind)


MODELS = ["A_conventional_kinematic_baseline", "B_temporal_relational_no_spectral", "C_temporal_relational_with_spectral"]
ABLATIONS = ["geometry_only", "instantaneous_kinematics_only", "temporal_relation_only", "spectral_only", "relation_plus_temporal", "relation_plus_temporal_plus_spectral"]


def main() -> None:
    PRED_ROOT.mkdir(parents=True, exist_ok=True)
    files = sorted(ALG_ROOT.glob("sample_*.json"))
    if not files or any("evaluator" in str(p).lower() for p in files):
        raise RuntimeError("Algorithm-visible input set is empty or contaminated")
    rows = []
    for path in files:
        sample = json.loads(path.read_text(encoding="utf-8"))
        feat = extract(sample)
        for model in MODELS + ABLATIONS:
            vals, names = select(feat, model)
            prob = fixed_logistic(vals, names)
            rows.append({"sample_id": path.stem, "model": model, "probability": prob,
                         "predicted_label": int(prob >= 0.5), "feature_count": len(vals),
                         "feature_names": names, "features": np.asarray(vals, dtype=float).round(8).tolist()})
    (PRED_ROOT / "predictions.json").write_text(json.dumps(rows, separators=(",", ":")), encoding="utf-8")
    (PRED_ROOT / "prediction_manifest.json").write_text(json.dumps({"sample_count": len(files), "prediction_count": len(rows), "models": MODELS, "ablations": ABLATIONS, "truth_loaded": False}, indent=2), encoding="utf-8")
    print(f"predictions written samples={len(files)} rows={len(rows)} truth_loaded=False")


if __name__ == "__main__":
    main()
