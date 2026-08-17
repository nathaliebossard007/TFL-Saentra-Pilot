"""DYNAMIC-001 v1.2 frozen spatiotemporal occupancy operator."""
from __future__ import annotations
import json, shutil
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
V10 = ROOT.parent
ALG, EVAL = V10 / "data" / "algorithm_visible", V10 / "data" / "evaluator_only"
OUT, RAW, DIAG = ROOT / "results" / "exploratory", ROOT / "results" / "exploratory" / "raw_spatiotemporal_states", ROOT / "diagnostics"
WINDOWS = (5, 15, 30)
PAIRS = [(i, j) for i in range(4) for j in range(i + 1, 4)]
EPS, RANK, GAP = 1e-12, 2, 1e-6

def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, separators=(",", ":"), allow_nan=False), encoding="utf-8")

def arrays(record: dict) -> tuple[np.ndarray, np.ndarray]:
    p = np.asarray([[s["position_xyz"] for s in tr] for tr in record["track_states"]], float)
    v = np.asarray([[s["velocity_xyz"] for s in tr] for tr in record["track_states"]], float)
    if p.shape != (4, 181, 3) or v.shape != (4, 181, 3): raise RuntimeError("unexpected track schema")
    return p, v

def series(record: dict) -> list[dict[str, np.ndarray]]:
    p, v = arrays(record); out = []
    for i, j in PAIRS:
        rel = p[i] - p[j]; d = np.linalg.norm(rel, axis=1); dd = np.gradient(d)
        dv = v[i] - v[j]; den = np.linalg.norm(v[i], axis=1) * np.linalg.norm(v[j], axis=1)
        cos = np.sum(v[i] * v[j], axis=1) / np.maximum(den, 1e-12)
        out.append({"d": d, "dd": dd, "dv": dv, "cos": np.clip(cos, -1, 1)})
    return out

def projector(evecs: np.ndarray, vals: np.ndarray) -> tuple[list[list[float]] | None, int | None]:
    if len(vals) < RANK or float(vals[RANK] - vals[RANK - 1]) < GAP: return None, None
    p = evecs[:, :RANK] @ evecs[:, :RANK].T
    return p.tolist(), int(RANK)

def laplacian(w: np.ndarray) -> tuple[np.ndarray, dict]:
    deg = w.sum(axis=1); inv = np.zeros_like(deg); inv[deg >= EPS] = 1.0 / np.sqrt(deg[deg >= EPS])
    l = np.eye(len(w)) - inv[:, None] * w * inv[None, :]
    vals, vecs = np.linalg.eigh(l)
    proj, rank = projector(vecs, vals)
    return l, {"eigenvalues": vals.tolist(), "spectral_gap_r2": float(vals[RANK] - vals[RANK - 1]),
               "zero_degree_count": int(np.sum(deg < EPS)), "projector": proj, "projector_rank": rank}

def distance(a: np.ndarray, b: np.ndarray) -> float:
    delta = np.asarray(a) - np.asarray(b)
    return float(np.linalg.norm(delta, "fro" if delta.ndim == 2 else 2) / np.sqrt(delta.size))
def projector_distance(a: dict, b: dict) -> float | None:
    if a.get("projector") is None or b.get("projector") is None: return None
    pa, pb = np.asarray(a["projector"]), np.asarray(b["projector"])
    return float(np.linalg.norm(pa - pb, "fro") / np.sqrt(2 * RANK))

def state(record: dict) -> dict:
    zs = series(record); result = {"windows": {}}
    for w in WINDOWS:
        rows, operators = [], []
        for t in range(181):
            start = max(0, t - w + 1); dscale = max(float(np.mean([z["d"][start:t+1] for z in zs])), 1.0)
            shape_scale = max(float(np.median([z["d"][k] for z in zs for k in range(start, t+1)])), 1.0)
            rigid_w = np.zeros((4, 4)); shape_w = np.zeros((4, 4)); motion_w = np.zeros((4, 4))
            pair_rows = []
            for q, z in enumerate(zs):
                k = np.arange(start, t + 1); dnorm = z["d"] / dscale; sd = z["d"] / shape_scale
                qvec = np.column_stack([dnorm, np.abs(z["dd"]) / 12.0, np.linalg.norm(z["dv"], axis=1) / 8.0, (1 + z["cos"]) / 2])
                iw = np.exp(-np.mean(qvec[k] ** 2, axis=1) / 2.0)
                persistence = float(np.mean(np.exp(-((dnorm[k] - dnorm[t]) ** 2 + (z["dd"][k] / 12 - z["dd"][t] / 12) ** 2) / 2.0)) * np.mean((1 + z["cos"][k]) / 2))
                occ = float(np.mean(iw) * persistence)
                rigid_w[PAIRS[q]], shape_w[PAIRS[q]], motion_w[PAIRS[q]] = occ, float(np.mean(np.exp(-((sd[k] - sd[t]) ** 2) / 2.0)) * np.mean((1 + z["cos"][k]) / 2)), float(np.mean(iw))
                rigid_w[PAIRS[q][::-1]], shape_w[PAIRS[q][::-1]], motion_w[PAIRS[q][::-1]] = rigid_w[PAIRS[q]], shape_w[PAIRS[q]], motion_w[PAIRS[q]]
                pair_rows.append({"pair_index": q, "instantaneous_weight": float(iw[-1]), "occupancy_persistence": persistence, "occupancy_edge": occ, "shape_occupancy_edge": shape_w[PAIRS[q]], "motion_edge": motion_w[PAIRS[q]]})
            rigid_l, rigid_d = laplacian(rigid_w); shape_l, shape_d = laplacian(shape_w); motion_l, motion_d = laplacian(motion_w)
            _, occ_d = laplacian(rigid_w)
            operators.append({"rigid": rigid_l.tolist(), "shape": shape_l.tolist(), "motion": motion_l.tolist(), "occupancy": rigid_l.tolist(), "spectral": {"rigid": rigid_d, "shape": shape_d, "motion": motion_d, "occupancy": occ_d}, "pair_rows": pair_rows})
            rows.append(pair_rows)
        result["windows"][str(w)] = {"states": rows, "operators": operators}
    return result

def diagnostics(state_value: dict, meta: dict) -> dict:
    out = {"sample_id": meta["sample_id"], "scenario_id": meta["scenario_id"], "seed": meta["seed"], "windows": {}}
    for w in WINDOWS:
        ops = state_value["windows"][str(w)]["operators"]; mats = [np.asarray(x["occupancy"]) for x in ops]
        base = np.mean(mats[30:61], axis=0); base_l, base_d = laplacian(base)
        refs = [distance(m, base) for m in mats]; spec = [distance(np.asarray(x["spectral"]["occupancy"]["eigenvalues"]), np.asarray(base_d["eigenvalues"])) for x in ops]
        proj = [projector_distance(x["spectral"]["occupancy"], base_d) for x in ops]
        out["windows"][str(w)] = {"reference_operator_distance": refs, "window_operator_distance": [None] + [distance(mats[t], mats[t-w]) for t in range(1,181)], "reference_spectrum_distance": spec, "reference_projector_distance": proj, "baseline_reference_mean": float(np.mean(refs[30:61])), "zero_degree_count": [x["spectral"]["occupancy"]["zero_degree_count"] for x in ops]}
    if meta["scenario_id"] == "D6_perturbation_recovery":
        d = out["windows"]["15"]; threshold = d["baseline_reference_mean"] * 1.2; good = np.asarray(d["reference_operator_distance"]) <= threshold; run = next((i for i in range(101, 167) if np.all(good[i:i+15])), None); out["recovery_latency_s"] = float(run - 100 if run is not None else 180.0)
        edges = np.asarray([[r["occupancy_edge"] for r in row] for row in state_value["windows"]["15"]["states"]]); edge_good = np.sum(edges > 0.0, axis=1) >= 5; run = next((i for i in range(101, 167) if np.all(edge_good[i:i+15])), None); out["reformation_latency_s"] = float(run - 100 if run is not None else 180.0)
    return out

def main() -> None:
    if OUT.exists(): shutil.rmtree(OUT)
    if DIAG.exists(): shutil.rmtree(DIAG)
    RAW.mkdir(parents=True, exist_ok=True); DIAG.mkdir(parents=True, exist_ok=True)
    files = sorted(ALG.glob("sample_*.json")); assert len(files) == 120
    raw = []
    for path in files:
        record = json.loads(path.read_text(encoding="utf-8")); assert set(record) == {"track_states"}
        raw.append({"sample_id": path.stem, "states": state(record)})
    for row in raw: write(RAW / f"{row['sample_id']}.json", row)
    write(OUT / "raw_state_manifest.json", {"sample_count": len(raw), "source": "DYNAMIC-001 v1.0 algorithm-visible exploratory data", "truth_loaded": False, "protocol_version": "1.2"})
    if raw[0]["states"] != state(json.loads(files[0].read_text(encoding="utf-8"))): raise RuntimeError("determinism gate failed")
    truth = {json.loads(p.read_text(encoding="utf-8"))["sample_id"]: json.loads(p.read_text(encoding="utf-8")) for p in sorted(EVAL.glob("eval_*.json"))}
    records = [diagnostics(row["states"], truth[row["sample_id"]]) for row in raw]
    write(DIAG / "exploratory_v1.2_diagnostics.json", {"status": "EXPLORATORY — REVIEW REQUIRED BEFORE EXTENSION", "truth_loaded_after_raw_states": True, "records": records})
    write(OUT / "exploratory_manifest.json", {"sample_count": 120, "windows_s": list(WINDOWS), "simulator_changed": False, "classifier_used": False, "raw_written_before_truth": True, "review_required": True})
    print("DYNAMIC-001 v1.2 exploratory raw states=120 records=120 review_required=True")

if __name__ == "__main__": main()
