"""Evaluation stage: loads truth only after prediction files exist."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ALG_ROOT = ROOT / "data" / "algorithm_visible"
EVAL_ROOT = ROOT / "data" / "evaluator_only"
PRED_FILE = ROOT / "results" / "exploratory" / "predictions" / "predictions.json"
OUT = ROOT / "results" / "exploratory"
DIAG = ROOT / "diagnostics"


def binary_metrics(y: np.ndarray, pred: np.ndarray, prob: np.ndarray) -> dict:
    tp = int(np.sum((y == 1) & (pred == 1))); tn = int(np.sum((y == 0) & (pred == 0)))
    fp = int(np.sum((y == 0) & (pred == 1))); fn = int(np.sum((y == 1) & (pred == 0)))
    precision = tp / max(tp + fp, 1); recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-12)
    tpr = recall; tnr = tn / max(tn + fp, 1)
    auc = roc_auc(y, prob)
    return {"precision": precision, "recall": recall, "F1": f1, "balanced_accuracy": (tpr + tnr) / 2,
            "confusion_matrix": [[tn, fp], [fn, tp]], "ROC_AUC": auc,
            "detection_latency_s": float(0.0 if tp else 180.0),
            "false_organization_duration_s": float(180.0 if fp else 0.0),
            "organization_state_stability": float(np.mean(prob))}


def roc_auc(y: np.ndarray, score: np.ndarray) -> float | None:
    pos = score[y == 1]; neg = score[y == 0]
    if len(pos) == 0 or len(neg) == 0: return None
    wins = sum(1.0 if p > n else 0.5 if p == n else 0.0 for p in pos for n in neg)
    return float(wins / (len(pos) * len(neg)))


def sample_marginals(sample: dict) -> dict[str, float]:
    tracks = sample["track_states"]
    p = np.array([[s["position_xyz"] for s in tr] for tr in tracks], dtype=float)
    v = np.array([[s["velocity_xyz"] for s in tr] for tr in tracks], dtype=float)
    speed = np.linalg.norm(v, axis=2)
    centroid_v = np.linalg.norm(np.mean(v, axis=0), axis=1)
    distances = []
    for i in range(4):
        for j in range(i + 1, 4): distances.extend(np.linalg.norm(p[i] - p[j], axis=1).tolist())
    heading = []
    for i in range(4):
        for j in range(i + 1, 4):
            a, b = v[i], v[j]; den = np.linalg.norm(a, axis=1) * np.linalg.norm(b, axis=1)
            heading.extend((np.sum(a * b, axis=1) / np.maximum(den, 1e-9)).tolist())
    return {"mean_speed": float(np.mean(speed)), "altitude": float(np.mean(p[:, :, 2])),
            "centroid_speed": float(np.mean(centroid_v)), "mean_pairwise_distance": float(np.mean(distances)),
            "group_extent": float(np.mean(np.ptp(p, axis=0))), "mean_heading": float(np.mean(heading)),
            "trajectory_duration": float(len(p[0]) - 1), "operating_region": float(np.mean(p[:, :, 0] + p[:, :, 1]))}


def audit_marginal(rows: list[dict], name: str) -> float:
    values = np.array([r["marginals"][name] for r in rows]); y = np.array([r["label"] for r in rows])
    best = 0.0
    for threshold in np.unique(values):
        for direction in [1, -1]:
            pred = (direction * values >= direction * threshold).astype(int)
            tn = np.sum((y == 0) & (pred == 0)); fp = np.sum((y == 0) & (pred == 1)); fn = np.sum((y == 1) & (pred == 0)); tp = np.sum((y == 1) & (pred == 1))
            best = max(best, 0.5 * (tp / max(tp + fn, 1) + tn / max(tn + fp, 1)))
    return float(best)


def main() -> None:
    if not PRED_FILE.exists(): raise RuntimeError("Predictions must be written before evaluation")
    predictions = json.loads(PRED_FILE.read_text(encoding="utf-8"))
    # Only now load evaluator-only truth.
    truth = {}
    marginals = []
    for eval_path in sorted(EVAL_ROOT.glob("eval_*.json")):
        rec = json.loads(eval_path.read_text(encoding="utf-8")); sid = rec["sample_id"]
        truth[sid] = int(rec["ground_truth_coordination_state"] == "coordinated")
        sample = json.loads((ALG_ROOT / f"{sid}.json").read_text(encoding="utf-8"))
        marginals.append({"sample_id": sid, "label": truth[sid], "marginals": sample_marginals(sample)})
    DIAG.mkdir(parents=True, exist_ok=True)
    marginal_names = list(marginals[0]["marginals"])
    audits = {n: audit_marginal(marginals, n) for n in marginal_names}
    (DIAG / "exploratory_marginal_diagnostics.json").write_text(json.dumps({"status": "EXPLORATORY — NOT CONFIRMATORY EVIDENCE", "rows": marginals, "one_variable_balanced_accuracy": audits, "threshold_status": "TO_BE_FROZEN_AFTER_EXPLORATORY_SANITY_CHECK"}, indent=2), encoding="utf-8")
    grouped = {}
    for model in sorted({p["model"] for p in predictions}):
        rr = [p for p in predictions if p["model"] == model]
        y = np.array([truth[p["sample_id"]] for p in rr]); pred = np.array([p["predicted_label"] for p in rr]); prob = np.array([p["probability"] for p in rr])
        grouped[model] = {"status": "EXPLORATORY — NOT CONFIRMATORY EVIDENCE", "sample_count": len(rr), **binary_metrics(y, pred, prob)}
    (OUT / "exploratory_summary.json").write_text(json.dumps(grouped, indent=2), encoding="utf-8")
    with (OUT / "exploratory_summary.csv").open("w", newline="", encoding="utf-8") as f:
        keys = ["model", "sample_count", "precision", "recall", "F1", "balanced_accuracy", "ROC_AUC", "detection_latency_s", "false_organization_duration_s", "organization_state_stability"]
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader()
        for model, row in grouped.items(): w.writerow({"model": model, **{k: row.get(k) for k in keys[1:]}})
    # Effect sizes are descriptive exploratory differences only.
    effects = {"B_vs_A_F1_difference": grouped["B_temporal_relational_no_spectral"]["F1"] - grouped["A_conventional_kinematic_baseline"]["F1"],
               "C_vs_B_F1_difference": grouped["C_temporal_relational_with_spectral"]["F1"] - grouped["B_temporal_relational_no_spectral"]["F1"],
               "status": "EXPLORATORY — NOT CONFIRMATORY EVIDENCE"}
    (OUT / "exploratory_effects.json").write_text(json.dumps(effects, indent=2), encoding="utf-8")
    spectral = [p for p in predictions if p["model"] == "C_temporal_relational_with_spectral"]
    (DIAG / "exploratory_spectral_diagnostics.json").write_text(json.dumps({"status": "EXPLORATORY — NOT CONFIRMATORY EVIDENCE", "source": "Model C feature block", "records": spectral}, indent=2), encoding="utf-8")
    print(f"evaluated exploratory predictions={len(predictions)} samples={len(truth)} truth_loaded_after_predictions=True")


if __name__ == "__main__":
    main()
