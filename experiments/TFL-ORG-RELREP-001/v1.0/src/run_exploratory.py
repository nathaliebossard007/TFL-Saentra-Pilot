"""TFL-ORG-RELREP-001 frozen parallel-representation pilot."""
from __future__ import annotations
import itertools, json, shutil
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent.parent / "TFL-UAS-DYNAMIC-001" / "data" / "algorithm_visible"
OUT, RAW, DIAG = ROOT / "results" / "exploratory", ROOT / "results" / "exploratory" / "raw_parallel_representations", ROOT / "diagnostics"
PAIRS = [(i, j) for i in range(4) for j in range(i + 1, 4)]
PERMS, WINDOWS, TOL, GAP = list(itertools.permutations(range(4))), (5, 15, 30), 1e-9, 1e-6

def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, separators=(",", ":"), allow_nan=False), encoding="utf-8")

def arrays(record: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if set(record) != {"track_states"}: raise RuntimeError("algorithm-visible schema contaminated")
    p = np.asarray([[s["position_xyz"] for s in tr] for tr in record["track_states"]], float)
    v = np.asarray([[s["velocity_xyz"] for s in tr] for tr in record["track_states"]], float)
    ids = np.asarray([[s["track_id"] for s in tr] for tr in record["track_states"]], object)
    if p.shape != (4, 181, 3) or v.shape != (4, 181, 3) or not np.all(ids == ids[:, :1]): raise RuntimeError("selected source track schema changed")
    return p, v, ids[:, 0]

def geometry(p: np.ndarray, v: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    d = np.asarray([np.linalg.norm(p[i] - p[j], axis=1) for i, j in PAIRS])
    speed = np.asarray([np.linalg.norm(v[i] - v[j], axis=1) for i, j in PAIRS])
    cos = []
    for i, j in PAIRS:
        den = np.linalg.norm(v[i], axis=1) * np.linalg.norm(v[j], axis=1)
        cos.append(np.sum(v[i] * v[j], axis=1) / np.maximum(den, 1e-12))
    return d, speed, np.clip(np.asarray(cos), -1, 1)

def relation(d: np.ndarray, cos: np.ndarray, t: int) -> tuple[np.ndarray, np.ndarray]:
    scale = max(float(np.median(d[:, t])), 1.0)
    weights = np.exp(-((d[:, t] / scale) ** 2 + ((1 + cos[:, t]) / 2) ** 2) / 2.0)
    incident = [[] for _ in range(4)]
    for q, (i, j) in enumerate(PAIRS):
        incident[i].append((weights[q], q)); incident[j].append((weights[q], q))
    edges = set()
    for node in range(4):
        for _, q in sorted(incident[node], key=lambda x: (-x[0], x[1]))[:2]: edges.add(q)
    matrix = np.zeros((4, 4))
    for q in range(6):
        i, j = PAIRS[q]; matrix[i, j] = matrix[j, i] = float(weights[q])
    return np.asarray(sorted(edges), int), matrix

def canonical_edges(edges: np.ndarray) -> tuple[int, ...]:
    src = set(int(x) for x in edges); encodings = []
    for perm in PERMS:
        bits = []
        for i, j in PAIRS:
            old = tuple(sorted((perm[i], perm[j])))
            bits.append(int(PAIRS.index(old) in src))
        encodings.append(tuple(bits))
    return min(encodings)

def canonical_matrix(matrix: np.ndarray) -> tuple[float, ...]:
    out = []
    for perm in PERMS:
        out.append(tuple(np.asarray(matrix)[np.ix_(perm, perm)].round(12).ravel().tolist()))
    return min(out)

def laplacian(matrix: np.ndarray) -> dict:
    deg = matrix.sum(axis=1); inv = np.zeros(4); inv[deg > 1e-12] = 1 / np.sqrt(deg[deg > 1e-12])
    l = np.eye(4) - inv[:, None] * matrix * inv[None, :]
    vals, vecs = np.linalg.eigh(l); proj = None
    if vals[2] - vals[1] >= GAP: proj = (vecs[:, :2] @ vecs[:, :2].T).tolist()
    return {"eigenvalues": vals.tolist(), "lambda2": float(vals[1]), "zero_degree_count": int(np.sum(deg <= 1e-12)), "projector": proj, "projector_rank": 2 if proj is not None else None}

def switch(edges: np.ndarray) -> tuple[np.ndarray | None, dict]:
    e = {PAIRS[int(q)] for q in edges}
    for a, b in sorted(e):
        for c, d in sorted(e):
            if len({a, b, c, d}) != 4: continue
            for replacement in [((a, c), (b, d)), ((a, d), (b, c))]:
                r = {tuple(sorted(x)) for x in replacement}
                if r & e: continue
                new = (e - {(a, b), (c, d)}) | r
                return np.asarray([PAIRS.index(x) for x in sorted(new)], int), {"available": True, "source_edges": sorted([list(x) for x in e]), "target_edges": sorted([list(x) for x in new])}
    return None, {"available": False, "source_edges": sorted([list(x) for x in e]), "target_edges": None}

def p_distance(a: dict, b: dict) -> float | None:
    if a["projector"] is None or b["projector"] is None: return None
    return float(np.linalg.norm(np.asarray(a["projector"]) - np.asarray(b["projector"]), "fro") / 2.0)

def build_view(p: np.ndarray, v: np.ndarray, ids: np.ndarray) -> dict:
    d, speed, cos = geometry(p, v); A = np.array([[np.cos(np.deg2rad(37)), -np.sin(np.deg2rad(37)), 0], [np.sin(np.deg2rad(37)), np.cos(np.deg2rad(37)), 0], [0, 0, 1]])
    center = p.mean(axis=0); p2 = (p - center) @ A.T * 1.8 + center; v2 = v @ A.T * 1.8
    d2, speed2, cos2 = geometry(p2, v2)
    states = {"source": [], "A": [], "B": []}; switches = []
    for t in range(181):
        e, wt = relation(d, cos, t); ea, wta = relation(d2, cos2, t); eb, info = switch(e); switches.append(info)
        wb = np.zeros((4, 4))
        if eb is not None:
            for q in eb:
                i, j = PAIRS[int(q)]; wb[i, j] = wb[j, i] = wt[i, j]
        states["source"].append({"R_id": list(canonical_edges(e)), "R_wt": wt.tolist(), "P": laplacian(wt), "G": {"pair_distance": d[:, t].tolist(), "relative_speed": speed[:, t].tolist()}})
        states["A"].append({"R_id": list(canonical_edges(ea)), "R_wt": wta.tolist(), "P": laplacian(wta), "G": {"pair_distance": d2[:, t].tolist(), "relative_speed": speed2[:, t].tolist()}})
        states["B"].append({"R_id": list(canonical_edges(eb)) if eb is not None else None, "R_wt": wb.tolist() if eb is not None else None, "P": laplacian(wb) if eb is not None else None, "G": {"pair_distance": d[:, t].tolist(), "relative_speed": speed[:, t].tolist()}, "switch": info})
    for label in states:
        for w in WINDOWS:
            transitions = []
            for t in range(181):
                transitions.append(None if t < w else {"edge_equal_to_previous_window": states[label][t]["R_id"] == states[label][t-w]["R_id"], "weighted_distance": None if states[label][t]["R_wt"] is None or states[label][t-w]["R_wt"] is None else float(np.linalg.norm(np.asarray(states[label][t]["R_wt"]) - np.asarray(states[label][t-w]["R_wt"])))})
            states[label].append({"R_t_window_s": w, "transitions": transitions})
    return {"canonical_node_ids": ids.tolist(), "states": states, "switches": switches, "operator_constants": {"windows_s": list(WINDOWS), "weight_tolerance": TOL, "projector_gap_min": GAP}}

def main() -> None:
    if OUT.exists(): shutil.rmtree(OUT)
    if DIAG.exists(): shutil.rmtree(DIAG)
    RAW.mkdir(parents=True, exist_ok=True); DIAG.mkdir(parents=True, exist_ok=True)
    files = sorted(SOURCE.glob("sample_*.json"));
    if len(files) != 120: raise RuntimeError("selected source count changed")
    raw = []
    for path in files:
        p, v, ids = arrays(json.loads(path.read_text(encoding="utf-8"))); raw.append({"sample_id": path.stem, "representations": build_view(p, v, ids)})
    for row in raw: write(RAW / f"{row['sample_id']}.json", row)
    write(OUT / "raw_state_manifest.json", {"sample_count": 120, "source": str(SOURCE), "truth_loaded": False, "representations": ["G", "R_id", "R_wt", "R_t", "P"], "raw_written_before_evaluator": True})
    p, v, ids = arrays(json.loads(files[0].read_text(encoding="utf-8")))
    if raw[0]["representations"] != build_view(p, v, ids): raise RuntimeError("determinism gate failed")
    write(DIAG / "exploratory_diagnostics.json", {"status": "EXPLORATORY — REVIEW REQUIRED BEFORE INTERPRETATION", "evaluator_metadata_loaded": False, "records": [{"sample_id": x["sample_id"], "timestamps": 181, "b_available": sum(s["switch"]["available"] for s in x["representations"]["states"]["B"][:181]), "projector_defined_source": sum(s["P"]["projector"] is not None for s in x["representations"]["states"]["source"][:181])} for x in raw]})
    write(OUT / "exploratory_manifest.json", {"sample_count": 120, "selected_source": "DYNAMIC-001 algorithm-visible tracks", "evaluator_metadata_loaded": False, "classifier_used": False, "review_required": True})
    print("TFL-ORG-RELREP-001 exploratory raw parallel representations=120 review_required=True")

if __name__ == "__main__": main()
