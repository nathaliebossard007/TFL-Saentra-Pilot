"""TFL-ORG-SYM-001 frozen organizational-symmetry pilot."""
from __future__ import annotations
import itertools, json, shutil
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent.parent / "TFL-UAS-DYNAMIC-001" / "data" / "algorithm_visible"
OUT, RAW, DIAG = ROOT / "results" / "exploratory", ROOT / "results" / "exploratory" / "raw_symmetry_states", ROOT / "diagnostics"
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
    if p.shape != (4, 181, 3) or v.shape != (4, 181, 3) or not np.all(ids == ids[:, :1]): raise RuntimeError("stable track identity check failed")
    return p, v, ids[:, 0]

def features(p: np.ndarray, v: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    d = np.asarray([np.linalg.norm(p[i] - p[j], axis=1) for i, j in PAIRS])
    rv = np.asarray([np.linalg.norm(v[i] - v[j], axis=1) for i, j in PAIRS])
    cos = []
    for i, j in PAIRS:
        den = np.linalg.norm(v[i], axis=1) * np.linalg.norm(v[j], axis=1)
        cos.append(np.sum(v[i] * v[j], axis=1) / np.maximum(den, 1e-12))
    return d, rv, np.clip(np.asarray(cos), -1, 1)

def relation(d: np.ndarray, cos: np.ndarray, t: int) -> tuple[np.ndarray, np.ndarray]:
    scale = max(float(np.median(d[:, t])), 1.0)
    weights = np.exp(-((d[:, t] / scale) ** 2 + ((1 + cos[:, t]) / 2) ** 2) / 2.0)
    incident = [[] for _ in range(4)]
    for q, (i, j) in enumerate(PAIRS): incident[i].append((weights[q], q)); incident[j].append((weights[q], q))
    edges = set()
    for node in range(4):
        for _, q in sorted(incident[node], key=lambda x: (-x[0], x[1]))[:2]: edges.add(q)
    matrix = np.zeros((4, 4))
    for q, (i, j) in enumerate(PAIRS): matrix[i, j] = matrix[j, i] = float(weights[q])
    return np.asarray(sorted(edges), int), matrix

def laplacian(matrix: np.ndarray) -> dict:
    deg = matrix.sum(axis=1); inv = np.zeros(4); inv[deg > 1e-12] = 1 / np.sqrt(deg[deg > 1e-12])
    l = np.eye(4) - inv[:, None] * matrix * inv[None, :]
    vals, vecs = np.linalg.eigh(l); proj = None
    if vals[2] - vals[1] >= GAP: proj = (vecs[:, :2] @ vecs[:, :2].T).tolist()
    return {"eigenvalues": vals.tolist(), "lambda2": float(vals[1]), "zero_degree_count": int(np.sum(deg <= 1e-12)), "projector": proj, "projector_rank": 2 if proj is not None else None}

def permute_matrix(matrix: np.ndarray, perm: tuple[int, ...]) -> np.ndarray: return matrix[np.ix_(perm, perm)]
def encode_edges(edges: np.ndarray) -> tuple[int, ...]: return tuple(int(q in set(int(x) for x in edges)) for q in range(6))
def compose_permutations(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]: return tuple(a[b[i]] for i in range(4))

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

def build(record: dict) -> dict:
    p, v, ids = arrays(record); d, rv, cos = features(p, v)
    frames, switches = [], []
    for t in range(181):
        edges, matrix = relation(d, cos, t); base_p = laplacian(matrix); eb, info = switch(edges); switches.append(info)
        target = np.zeros((4, 4))
        if eb is not None:
            for q in eb:
                i, j = PAIRS[int(q)]; target[i, j] = target[j, i] = matrix[i, j]
        candidates = []
        for perm in PERMS:
            valid = all(np.max(np.abs(permute_matrix(matrix, perm) - matrix)) <= TOL for _ in [0])
            candidates.append({"permutation": list(perm), "candidate_stabilizer": bool(valid), "relation_matrix_max_error": float(np.max(np.abs(permute_matrix(matrix, perm) - matrix)))})
        allowed = [tuple(x["permutation"]) for x in candidates if x["candidate_stabilizer"]]
        closure = all(compose_permutations(a, b) in allowed for a in allowed for b in allowed) if allowed else False
        frames.append({"timestamp": t, "R_labeled": {"track_ids": ids.tolist(), "edges": encode_edges(edges), "matrix": matrix.tolist()}, "R_struct": {"G_allow_candidates": candidates, "G_allow_state": [list(x) for x in allowed], "closure_observed": closure}, "endpoint_reassignment": {"edges": encode_edges(eb) if eb is not None else None, "matrix": target.tolist() if eb is not None else None, "P_labeled": base_p, "P_struct": laplacian(target) if eb is not None else None}, "G": {"pair_distance": d[:, t].tolist(), "relative_speed": rv[:, t].tolist()}})
    for w in WINDOWS:
        for t in range(181):
            frames[t].setdefault("temporal", {})[str(w)] = None if t < w else {"edge_transition_equal": frames[t]["R_labeled"]["edges"] == frames[t-w]["R_labeled"]["edges"], "matrix_frobenius_distance": float(np.linalg.norm(np.asarray(frames[t]["R_labeled"]["matrix"]) - np.asarray(frames[t-w]["R_labeled"]["matrix"]))) }
    return {"frames": frames, "switches": switches, "role_layer": {"supported": False, "reason": "no independent algorithm-visible role partition"}, "operator_constants": {"windows_s": list(WINDOWS), "tolerance": TOL, "projector_gap_min": GAP}}

def main() -> None:
    if OUT.exists(): shutil.rmtree(OUT)
    if DIAG.exists(): shutil.rmtree(DIAG)
    RAW.mkdir(parents=True, exist_ok=True); DIAG.mkdir(parents=True, exist_ok=True)
    files = sorted(SOURCE.glob("sample_*.json"));
    if len(files) != 120: raise RuntimeError("selected source count changed")
    raw = [{"sample_id": path.stem, "symmetry": build(json.loads(path.read_text(encoding="utf-8")))} for path in files]
    for row in raw: write(RAW / f"{row['sample_id']}.json", row)
    write(OUT / "raw_state_manifest.json", {"sample_count": 120, "source": str(SOURCE), "truth_loaded": False, "raw_written_before_interpretation": True, "role_layer_supported": False})
    if raw[0]["symmetry"] != build(json.loads(files[0].read_text(encoding="utf-8"))): raise RuntimeError("determinism gate failed")
    write(DIAG / "exploratory_diagnostics.json", {"status": "EXPLORATORY — REVIEW REQUIRED BEFORE INTERPRETATION", "evaluator_metadata_loaded": False, "records": [{"sample_id": x["sample_id"], "timestamps": 181, "non_identity_stabilizer_candidates": sum(1 for f in x["symmetry"]["frames"] for q in f["R_struct"]["G_allow_state"] if tuple(q) != (0, 1, 2, 3)), "endpoint_switch_available": sum(s["available"] for s in x["symmetry"]["switches"]), "role_layer_supported": False} for x in raw]})
    write(OUT / "exploratory_manifest.json", {"sample_count": 120, "selected_source": "DYNAMIC-001 algorithm-visible tracks", "evaluator_metadata_loaded": False, "classifier_used": False, "review_required": True})
    print("TFL-ORG-SYM-001 exploratory raw symmetry outputs=120 review_required=True")

if __name__ == "__main__": main()
