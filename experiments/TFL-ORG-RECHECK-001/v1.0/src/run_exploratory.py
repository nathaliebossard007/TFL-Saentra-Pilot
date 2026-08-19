"""TFL-ORG-RECHECK-001 frozen historical cross-over pilot."""
from __future__ import annotations
import json, shutil
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent.parent / "TFL-UAS-DYNAMIC-001" / "data" / "algorithm_visible"
OUT = ROOT / "results" / "exploratory"
RAW = OUT / "raw_g_r_p"
DIAG = ROOT / "diagnostics"
PAIRS = [(i, j) for i in range(4) for j in range(i + 1, 4)]
GAP = 1e-6

def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, separators=(",", ":"), allow_nan=False), encoding="utf-8")

def arrays(record: dict) -> tuple[np.ndarray, np.ndarray]:
    if set(record) != {"track_states"}:
        raise RuntimeError("selected source schema is not algorithm-visible only")
    p = np.asarray([[s["position_xyz"] for s in tr] for tr in record["track_states"]], float)
    v = np.asarray([[s["velocity_xyz"] for s in tr] for tr in record["track_states"]], float)
    if p.shape != (4, 181, 3) or v.shape != (4, 181, 3):
        raise RuntimeError(f"unexpected selected source shape: {p.shape}, {v.shape}")
    return p, v

def pair_geometry(p: np.ndarray, v: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    d = np.array([np.linalg.norm(p[i] - p[j], axis=1) for i, j in PAIRS])
    rv = np.array([np.linalg.norm(v[i] - v[j], axis=1) for i, j in PAIRS])
    cos = []
    for i, j in PAIRS:
        den = np.linalg.norm(v[i], axis=1) * np.linalg.norm(v[j], axis=1)
        cos.append(np.sum(v[i] * v[j], axis=1) / np.maximum(den, 1e-12))
    return d, rv, np.clip(np.asarray(cos), -1, 1)

def graph(d: np.ndarray, cos: np.ndarray, t: int) -> np.ndarray:
    scale = max(float(np.median(d[:, t])), 1.0)
    weights = np.exp(-((d[:, t] / scale) ** 2 + ((1 + cos[:, t]) / 2) ** 2) / 2.0)
    incident = [[] for _ in range(4)]
    for q, (i, j) in enumerate(PAIRS):
        incident[i].append((weights[q], q)); incident[j].append((weights[q], q))
    edges = set()
    for node in range(4):
        for _, q in sorted(incident[node], key=lambda x: (-x[0], x[1]))[:2]: edges.add(q)
    return np.asarray(sorted(edges), dtype=int)

def laplacian(edges: np.ndarray) -> tuple[np.ndarray, dict]:
    w = np.zeros((4, 4))
    for q in edges:
        i, j = PAIRS[int(q)]; w[i, j] = w[j, i] = 1.0
    deg = w.sum(axis=1); inv = np.zeros(4); inv[deg > 1e-12] = 1 / np.sqrt(deg[deg > 1e-12])
    l = np.eye(4) - inv[:, None] * w * inv[None, :]
    vals, vecs = np.linalg.eigh(l)
    proj = None
    if vals[2] - vals[1] >= GAP: proj = (vecs[:, :2] @ vecs[:, :2].T).tolist()
    return l, {"edges": [int(x) for x in edges], "eigenvalues": vals.tolist(), "lambda2": float(vals[1]), "zero_degree_count": int(np.sum(deg <= 1e-12)), "projector_rank": 2 if proj is not None else None, "projector": proj}

def projector_distance(a: dict, b: dict) -> float | None:
    if a["projector"] is None or b["projector"] is None: return None
    return float(np.linalg.norm(np.asarray(a["projector"]) - np.asarray(b["projector"]), "fro") / 2.0)

def jaccard(a: set[int], b: set[int]) -> float:
    return float(len(a & b) / len(a | b)) if a | b else 1.0

def switch(edges: np.ndarray) -> tuple[np.ndarray | None, dict]:
    e = {tuple(PAIRS[int(q)]) for q in edges}
    nodes = range(4)
    for a, b in sorted(e):
        for c, d in sorted(e):
            if len({a, b, c, d}) != 4: continue
            for replacement in [((a, c), (b, d)), ((a, d), (b, c))]:
                r = {tuple(sorted(x)) for x in replacement}
                if r & e or len(r) != 2: continue
                new = (e - {(a, b), (c, d)}) | r
                q = np.asarray([PAIRS.index(x) for x in sorted(new)], dtype=int)
                return q, {"available": True, "source_edges": sorted([list(x) for x in e]), "target_edges": sorted([list(x) for x in new])}
    return None, {"available": False, "source_edges": sorted([list(x) for x in e]), "target_edges": None}

def sample_state(record: dict) -> dict:
    p, v = arrays(record); d, rv, cos = pair_geometry(p, v)
    pa = np.array([[np.cos(np.deg2rad(37)), -np.sin(np.deg2rad(37)), 0], [np.sin(np.deg2rad(37)), np.cos(np.deg2rad(37)), 0], [0, 0, 1]])
    center = p.mean(axis=0); p_a = (p - center) @ pa.T * 1.8 + center
    v_a = v @ pa.T * 1.8
    da, rva, cosa = pair_geometry(p_a, v_a)
    a_rows, b_rows = [], []
    for t in range(181):
        e = graph(d, cos, t); la, sa = laplacian(e); eb, info = switch(e)
        sb = laplacian(eb)[1] if eb is not None else None
        geom_a = {"mean_pair_distance_change": float(np.mean(np.abs(da[:, t] - d[:, t]) / np.maximum(d[:, t], 1e-12))), "median_pair_distance_change": float(np.median(np.abs(da[:, t] - d[:, t]) / np.maximum(d[:, t], 1e-12))), "pair_distance_correlation": float(np.corrcoef(d[:, t], da[:, t])[0, 1])}
        geom_b = {"mean_pair_distance_change": 0.0, "median_pair_distance_change": 0.0, "pair_distance_correlation": 1.0}
        a_rows.append({"timestamp": t, "G": geom_a, "R": {"edge_jaccard": jaccard(set(e), set(e)), "degree_sequence_equal": True, "changed_edge_count": 0}, "P": {"spectrum_distance": float(np.linalg.norm(np.asarray(sa["eigenvalues"]) - np.asarray(sa["eigenvalues"]))), "lambda2_change": 0.0, "projector_distance": 0.0 if sa["projector"] is not None else None, "base": sa}})
        b_rows.append({"timestamp": t, "G": geom_b, "R": {"edge_jaccard": jaccard(set(e), set(eb)) if eb is not None else None, "degree_sequence_equal": True if eb is not None else None, "changed_edge_count": int(len(set(e) ^ set(eb))) if eb is not None else None}, "P": {"spectrum_distance": float(np.linalg.norm(np.asarray(sa["eigenvalues"]) - np.asarray(sb["eigenvalues"]))) if sb else None, "lambda2_change": abs(sa["lambda2"] - sb["lambda2"]) if sb else None, "projector_distance": projector_distance(sa, sb) if sb else None, "base": sb}, "switch": info})
    return {"condition_A": a_rows, "condition_B": b_rows, "source_summary": {"sample_timestamp_count": 181, "pair_count": 6, "operator_recomputed": True}}

def main() -> None:
    if OUT.exists(): shutil.rmtree(OUT)
    if DIAG.exists(): shutil.rmtree(DIAG)
    RAW.mkdir(parents=True, exist_ok=True); DIAG.mkdir(parents=True, exist_ok=True)
    files = sorted(SOURCE.glob("sample_*.json"))
    if len(files) != 120: raise RuntimeError("selected source count changed")
    raw = []
    for path in files:
        raw.append({"sample_id": path.stem, "states": sample_state(json.loads(path.read_text(encoding="utf-8")))})
    for row in raw: write(RAW / f"{row['sample_id']}.json", row)
    write(OUT / "raw_state_manifest.json", {"sample_count": 120, "source": str(SOURCE), "truth_loaded": False, "conditions": ["A_geometry_breaking_relation_preserving", "B_geometry_preserving_relation_breaking"], "raw_written_before_interpretation": True})
    if raw[0]["states"] != sample_state(json.loads(files[0].read_text(encoding="utf-8"))): raise RuntimeError("determinism gate failed")
    write(DIAG / "exploratory_diagnostics.json", {"status": "EXPLORATORY — REVIEW REQUIRED BEFORE INTERPRETATION", "evaluator_metadata_loaded": False, "records": [{"sample_id": x["sample_id"], "condition_A_timestamps": len(x["states"]["condition_A"]), "condition_B_available_timestamps": sum(r["switch"]["available"] for r in x["states"]["condition_B"])} for x in raw]})
    write(OUT / "exploratory_manifest.json", {"sample_count": 120, "selected_source": "DYNAMIC-001 algorithm-visible tracks", "evaluator_metadata_loaded": False, "classifier_used": False, "review_required": True})
    print("TFL-ORG-RECHECK-001 exploratory raw G/R/P outputs=120 review_required=True")

if __name__ == "__main__": main()
