"""DYNAMIC-001 v1.2.1 diagnostic-only correction."""
from __future__ import annotations
import json, shutil
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
V12 = ROOT.parent / "v1.2"
EVAL = ROOT.parent / "data" / "evaluator_only"
OUT = ROOT / "results" / "exploratory"
RAW = OUT / "raw_corrected_diagnostics"
DIAG = ROOT / "diagnostics"
WINDOWS = (5, 15, 30)

def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, separators=(",", ":"), allow_nan=False), encoding="utf-8")

def norm_distance(a: np.ndarray, b: np.ndarray) -> float:
    d = a - b
    return float(np.linalg.norm(d, "fro") / np.sqrt(d.size))

def projector_distance(a: dict, b: dict) -> float | None:
    if a.get("projector") is None or b.get("projector") is None:
        return None
    d = np.asarray(a["projector"]) - np.asarray(b["projector"])
    return float(np.linalg.norm(d, "fro") / np.sqrt(4.0))

def corrected_state(source: dict) -> dict:
    windows = {}
    for w in WINDOWS:
        old = source["states"]["windows"][str(w)]
        ops = old["operators"]
        corrected = {"window_operator_distance": [], "window_spectrum_distance": [], "window_projector_distance": [], "valid_times": list(range(w, 181))}
        for t in range(181):
            if t < w:
                corrected["window_operator_distance"].append(None)
                corrected["window_spectrum_distance"].append(None)
                corrected["window_projector_distance"].append(None)
                continue
            current, previous = ops[t], ops[t - w]
            corrected["window_operator_distance"].append(norm_distance(np.asarray(current["occupancy"]), np.asarray(previous["occupancy"])))
            cur_spec = np.asarray(current["spectral"]["occupancy"]["eigenvalues"])
            prev_spec = np.asarray(previous["spectral"]["occupancy"]["eigenvalues"])
            corrected["window_spectrum_distance"].append(float(np.linalg.norm(cur_spec - prev_spec) / np.sqrt(cur_spec.size)))
            corrected["window_projector_distance"].append(projector_distance(current["spectral"]["occupancy"], previous["spectral"]["occupancy"]))
        windows[str(w)] = corrected
    rows = source["states"]["windows"]["15"]["states"]
    refs = np.mean([[r["occupancy_edge"] for r in rows[t]] for t in range(30, 61)], axis=0)
    restored = []
    for t in range(181):
        scores = [float(np.clip(1.0 - abs(rows[t][q]["occupancy_edge"] - refs[q]) / max(refs[q], 1e-12), 0.0, 1.0)) for q in range(6)]
        restored.append({"pair_similarity": scores, "restored_pair_count": int(sum(s >= 0.8 for s in scores)), "reference_edges": refs.tolist()})
    return {"sample_id": source["sample_id"], "windows": windows, "d6_pair_reformation": restored, "correction_constants": {"windows_s": list(WINDOWS), "d6_similarity_threshold": 0.8, "d6_minimum_pairs": 5, "d6_duration_s": 15, "d6_reference_interval_s": [30, 60]}}

def diagnostics(corrected: dict, meta: dict) -> dict:
    out = {"sample_id": meta["sample_id"], "scenario_id": meta["scenario_id"], "seed": meta["seed"], "windows": corrected["windows"]}
    if meta["scenario_id"] == "D6_perturbation_recovery":
        series = np.asarray(corrected["windows"]["15"]["window_operator_distance"], dtype=object)
        valid = np.asarray([x is not None for x in series])
        vals = np.asarray([x for x in series[30:61] if x is not None], float)
        threshold = float(np.mean(vals) * 1.2)
        good = np.asarray([x is not None and x <= threshold for x in series], bool)
        run = next((t for t in range(101, 167) if np.all(good[t:t + 15])), None)
        pair_good = np.asarray([x["restored_pair_count"] >= 5 for x in corrected["d6_pair_reformation"]], bool)
        reform = next((t for t in range(101, 167) if np.all(pair_good[t:t + 15])), None)
        out["d6_recovery"] = {"baseline_reference_mean": float(np.mean(vals)), "threshold": threshold, "recovery_latency_s": float(run - 100 if run is not None else 180.0), "reformation_latency_s": float(reform - 100 if reform is not None else 180.0), "valid_post_event_samples": int(np.sum(valid[101:]))}
    return out

def main() -> None:
    if OUT.exists(): shutil.rmtree(OUT)
    if DIAG.exists(): shutil.rmtree(DIAG)
    RAW.mkdir(parents=True, exist_ok=True); DIAG.mkdir(parents=True, exist_ok=True)
    files = sorted((V12 / "results" / "exploratory" / "raw_spatiotemporal_states").glob("sample_*.json"))
    if len(files) != 120: raise RuntimeError(f"expected 120 frozen v1.2 raw states, got {len(files)}")
    corrected = []
    for path in files:
        source = json.loads(path.read_text(encoding="utf-8"))
        if set(source) != {"sample_id", "states"}: raise RuntimeError("frozen v1.2 raw schema changed")
        corrected.append(corrected_state(source))
    for row in corrected: write(RAW / f"{row['sample_id']}.json", row)
    write(OUT / "raw_state_manifest.json", {"sample_count": 120, "source": "frozen DYNAMIC-001 v1.2 raw operator states", "truth_loaded": False, "protocol_version": "1.2.1", "operator_recomputed": False})
    if corrected[0] != corrected_state(json.loads(files[0].read_text(encoding="utf-8"))): raise RuntimeError("determinism gate failed")
    truth = {json.loads(p.read_text(encoding="utf-8"))["sample_id"]: json.loads(p.read_text(encoding="utf-8")) for p in sorted(EVAL.glob("eval_*.json"))}
    records = [diagnostics(row, truth[row["sample_id"]]) for row in corrected]
    write(DIAG / "exploratory_v1.2.1_diagnostics.json", {"status": "EXPLORATORY — REVIEW REQUIRED BEFORE EXTENSION", "truth_loaded_after_raw_states": True, "records": records})
    write(OUT / "exploratory_manifest.json", {"sample_count": 120, "windows_s": list(WINDOWS), "source_operator": "frozen v1.2", "operator_recomputed": False, "classifier_used": False, "raw_written_before_truth": True, "review_required": True})
    print("DYNAMIC-001 v1.2.1 exploratory correction raw states=120 records=120 review_required=True")

if __name__ == "__main__": main()
