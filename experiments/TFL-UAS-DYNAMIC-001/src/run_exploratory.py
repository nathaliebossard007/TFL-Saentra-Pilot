"""TFL-UAS-DYNAMIC-001 v1.0 exploratory pipeline."""
from __future__ import annotations
import hashlib, json, shutil
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ALG = ROOT / "data" / "algorithm_visible"
EVAL = ROOT / "data" / "evaluator_only"
OUT = ROOT / "results" / "exploratory"
DIAG = ROOT / "diagnostics"
SEEDS = range(101, 121)
SCENARIOS = [
    "D1_common_translation", "D2_coordinated_rotation_maneuver",
    "D3_independent_motion", "D4_apparent_block_stable_geometry",
    "D5_organized_expansion_contraction", "D6_perturbation_recovery",
]
PAIRS = [(i, j) for i in range(4) for j in range(i + 1, 4)]
WINDOWS = (5, 15, 30)
LAGS = (1, 5, 15, 30)
T = np.arange(181, dtype=float)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, separators=(",", ":")), encoding="utf-8")


def track_id(seed: int, obj: int) -> str:
    return "trk_" + hashlib.sha256(f"dynamic001/{seed}/{obj}".encode()).hexdigest()[:12]


def centroid(seed: int) -> np.ndarray:
    phase = 0.004 * T + 0.02 * seed
    return np.stack([
        4200 + 18 * T + 180 * np.sin(phase),
        3600 + 12 * T + 150 * np.cos(phase),
        850 + 25 * np.sin(0.01 * T + 0.1 * seed),
    ], axis=1)


def rotate(points: np.ndarray, angle: np.ndarray) -> np.ndarray:
    c, s = np.cos(angle), np.sin(angle)
    return np.stack([c * points[:, 0] - s * points[:, 1],
                     s * points[:, 0] + c * points[:, 1], points[:, 2]], axis=1)


def positions(seed: int, scenario: str) -> np.ndarray:
    rng = np.random.default_rng(8100 + seed)
    center = centroid(seed)
    offsets = np.array([[-260, -170, 0], [260, -170, 0],
                        [-260, 170, 0], [260, 170, 0]], dtype=float)
    tracks = []
    for obj, offset in enumerate(offsets):
        if scenario == "D1_common_translation":
            angle = np.zeros_like(T)
            scale = np.ones_like(T)
            rel = rotate(np.repeat(offset[None, :], len(T), axis=0), angle) * scale[:, None]
        elif scenario == "D2_coordinated_rotation_maneuver":
            angle = 0.01 * T + 0.05 * np.sin(0.02 * T + 0.1 * seed)
            rel = rotate(np.repeat(offset[None, :], len(T), axis=0), angle)
        elif scenario == "D3_independent_motion":
            q = np.zeros((len(T), 3))
            q[0] = offset
            for k in range(1, len(T)):
                q[k] = 0.985 * q[k - 1] + rng.normal(0, [7, 7, 2], 3)
            rel = q
        elif scenario == "D4_apparent_block_stable_geometry":
            # Geometry is quiet within short blocks, while each track receives
            # a distinct longer-window velocity/motion evolution.
            rel = np.repeat(offset[None, :], len(T), axis=0).astype(float)
            for block in range(12):
                start, end = block * 15, min((block + 1) * 15, len(T))
                rel[start:end] += np.array([
                    16 * np.sin(block + obj), 12 * np.cos(0.7 * block + obj),
                    3 * np.sin(0.4 * block + obj)])
            rel += np.stack([2 * np.sin(0.11 * T + obj),
                             2 * np.cos(0.09 * T + obj),
                             np.zeros_like(T)], axis=1)
        elif scenario == "D5_organized_expansion_contraction":
            scale = 1.0 + 0.32 * np.sin(0.018 * T + 0.1 * seed)
            rel = np.repeat(offset[None, :], len(T), axis=0) * scale[:, None]
        elif scenario == "D6_perturbation_recovery":
            angle = 0.006 * T
            rel = rotate(np.repeat(offset[None, :], len(T), axis=0), angle)
            disturbance = (T >= 70) & (T <= 100)
            rel[disturbance] += rng.normal(0, [65, 65, 18], (disturbance.sum(), 3))
        else:
            raise ValueError(scenario)
        tracks.append(center + rel + rng.normal(0, [2, 2, 1], (len(T), 3)))
    return np.asarray(tracks)


def make_track_record(seed: int, scenario: str) -> dict:
    p = positions(seed, scenario)
    v = np.gradient(p, axis=1)
    a = np.gradient(v, axis=1)
    tracks = []
    for obj in range(4):
        tracks.append([{
            "track_id": track_id(seed, obj), "timestamp": float(k),
            "position_xyz": p[obj, k].round(6).tolist(),
            "velocity_xyz": v[obj, k].round(6).tolist(),
            "acceleration_xyz": a[obj, k].round(6).tolist(),
            "state_uncertainty": [16, 16, 4],
        } for k in range(len(T))])
    return {"track_states": tracks}


def arrays(record: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    p = np.asarray([[x["position_xyz"] for x in tr] for tr in record["track_states"]], float)
    v = np.asarray([[x["velocity_xyz"] for x in tr] for tr in record["track_states"]], float)
    a = np.asarray([[x["acceleration_xyz"] for x in tr] for tr in record["track_states"]], float)
    return p, v, a


def corr(a: np.ndarray, b: np.ndarray) -> float:
    if np.std(a) < 1e-9 or np.std(b) < 1e-9:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def dynamic_state(record: dict) -> dict:
    p, v, a = arrays(record)
    pair = []
    for i, j in PAIRS:
        d = np.linalg.norm(p[i] - p[j], axis=1)
        dd = np.gradient(d)
        dv = v[i] - v[j]
        dv_norm = np.linalg.norm(dv, axis=1)
        speed_i, speed_j = np.linalg.norm(v[i], axis=1), np.linalg.norm(v[j], axis=1)
        den = np.linalg.norm(v[i], axis=1) * np.linalg.norm(v[j], axis=1)
        direction = np.sum(v[i] * v[j], axis=1) / np.maximum(den, 1e-9)
        acc_i, acc_j = np.linalg.norm(a[i], axis=1), np.linalg.norm(a[j], axis=1)
        pair.append({"distance": d, "normalized_distance": d / np.maximum(np.mean(d), 1e-6),
                     "distance_derivative": dd, "relative_velocity": dv,
                     "relative_velocity_norm": dv_norm, "direction_cosine": direction,
                     "speed_i": speed_i, "speed_j": speed_j,
                     "acc_i": acc_i, "acc_j": acc_j})

    motion = {str(w): [] for w in WINDOWS}
    spatial = []
    for k in range(len(T)):
        spatial.append([float(pair[q]["distance"][k]) for q in range(6)])
    for w in WINDOWS:
        for k in range(len(T)):
            start = max(0, k - w + 1)
            rows = []
            for q in range(6):
                z = pair[q]
                rows.append({
                    "distance_m": float(z["distance"][k]),
                    "normalized_distance": float(z["normalized_distance"][k]),
                    "distance_derivative_mps": float(z["distance_derivative"][k]),
                    "relative_velocity_xyz": z["relative_velocity"][k].round(6).tolist(),
                    "velocity_direction_cosine": float(z["direction_cosine"][k]),
                    "speed_correlation": corr(z["speed_i"][start:k + 1], z["speed_j"][start:k + 1]),
                    "relative_velocity_stability": float(np.exp(-np.mean(np.std(z["relative_velocity"][start:k + 1], axis=0)) / 8.0)),
                    "acceleration_coherence": corr(z["acc_i"][start:k + 1], z["acc_j"][start:k + 1]),
                })
            motion[str(w)].append(rows)
    return {"rigid_spatial_relational_state": spatial,
            "motion_relational_state": motion,
            "dynamic_organizational_state": {"registered_windows_s": list(WINDOWS), "registered_lags_s": list(LAGS)}}


def feature_vector(state: dict, time_index: int, window: int) -> np.ndarray:
    rows = state["motion_relational_state"][str(window)][time_index]
    vals = []
    for r in rows:
        vals.extend([r["normalized_distance"], r["distance_derivative_mps"] / 12.0,
                     *np.asarray(r["relative_velocity_xyz"], float) / 8.0,
                     r["velocity_direction_cosine"], r["speed_correlation"],
                     r["relative_velocity_stability"], r["acceleration_coherence"]])
    return np.asarray(vals, float)


def state_diagnostics(state: dict) -> dict:
    spatial = np.asarray(state["rigid_spatial_relational_state"], float)
    lagged, window_dist = {}, {}
    for lag in LAGS:
        vals = []
        for k in range(lag, len(T)):
            now, old = feature_vector(state, k, 15), feature_vector(state, k - lag, 15)
            vals.append(float(np.mean(np.abs(now - old) < 1.0)))
        lagged[str(lag)] = float(np.mean(vals))
    for w in WINDOWS:
        vals = []
        for k in range(w, len(T)):
            vals.append(float(np.linalg.norm(feature_vector(state, k, w) - feature_vector(state, k - w, w)) / np.sqrt(6 * 10)))
        window_dist[str(w)] = float(np.mean(vals))
    base = np.mean([feature_vector(state, k, 15) for k in range(30, 61)], axis=0)
    reference = [float(np.linalg.norm(feature_vector(state, k, 15) - base) / np.sqrt(base.size)) for k in range(len(T))]
    stable = np.asarray([lagged["1"] > 0.8] * len(T), bool)
    lifetimes = []
    run = 0
    for value in stable:
        run = run + 1 if value else 0
        if run and (not value or run == len(stable)):
            lifetimes.append(run)
    spatial_change = np.linalg.norm(np.diff(spatial, axis=0), axis=1).mean()
    motion_change = np.mean([np.linalg.norm(feature_vector(state, k, 15) - feature_vector(state, k - 1, 15)) for k in range(1, len(T))])
    return {"lagged_motion_persistence": lagged, "window_relational_state_distance": window_dist,
            "reference_state_distance_mean": float(np.mean(reference)),
            "reference_state_distance_max": float(np.max(reference)),
            "relation_lifetime_mean_s": float(np.mean(lifetimes) if lifetimes else 0.0),
            "relation_lifetime_max_s": int(max(lifetimes) if lifetimes else 0),
            "spatial_state_change_mean": float(spatial_change),
            "motion_state_change_mean": float(motion_change),
            "reference_state_distance_series": reference,
            "recovery_latency_s": None,
            "reformation_latency_s": None}


def main() -> None:
    for directory in (ALG, EVAL, OUT, DIAG):
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True, exist_ok=True)
    samples = []
    number = 1
    for seed in SEEDS:
        for scenario in SCENARIOS:
            sid = f"sample_{number:04d}"; number += 1
            record = make_track_record(seed, scenario)
            write_json(ALG / f"{sid}.json", record)
            write_json(EVAL / f"eval_{number - 1:04d}.json", {"sample_id": sid, "scenario_id": scenario, "seed": seed,
                "perturbation_start_s": 70 if scenario == "D6_perturbation_recovery" else None,
                "perturbation_end_s": 100 if scenario == "D6_perturbation_recovery" else None})
            samples.append((sid, record))

    raw_states = []
    for sid, record in samples:
        if set(record) != {"track_states"}:
            raise RuntimeError("algorithm-visible schema contains evaluator metadata")
        raw_states.append({"sample_id": sid, "states": dynamic_state(record)})
    raw_dir = OUT / "raw_dynamic_relational_states"
    raw_dir.mkdir(parents=True, exist_ok=True)
    for row in raw_states:
        write_json(raw_dir / f"{row['sample_id']}.json", row)

    if dynamic_state(make_track_record(101, SCENARIOS[0])) != raw_states[0]["states"]:
        raise RuntimeError("determinism gate failed")
    if any("scenario_id" in row["states"] or "seed" in row["states"] for row in raw_states):
        raise RuntimeError("state-output leakage detected")

    # Evaluator-only phase begins after raw dynamic states exist on disk.
    truth = {}
    for path in sorted(EVAL.glob("eval_*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        truth[record["sample_id"]] = record
    diagnostics = []
    for row in raw_states:
        item = state_diagnostics(row["states"])
        meta = truth[row["sample_id"]]
        item.update({"sample_id": row["sample_id"], "scenario_id": meta["scenario_id"], "seed": meta["seed"]})
        if meta["scenario_id"] == "D6_perturbation_recovery":
            series = np.asarray(item["reference_state_distance_series"])
            baseline = float(np.mean(series[30:61]))
            post = np.where(series[101:] <= baseline * 1.2)[0]
            item["recovery_latency_s"] = float(post[0] + 1 if len(post) else 180.0)
            item["reformation_latency_s"] = item["recovery_latency_s"]
        diagnostics.append(item)
    write_json(DIAG / "exploratory_dynamic_diagnostics.json", {
        "status": "EXPLORATORY — REVIEW REQUIRED BEFORE EXTENSION",
        "truth_loaded_after_raw_states": True, "records": diagnostics,
    })
    write_json(OUT / "exploratory_manifest.json", {"sample_count": len(raw_states), "seed_range": [101, 120],
        "scenario_count": 6, "windows_s": list(WINDOWS), "lags_s": list(LAGS),
        "raw_written_before_truth": True, "classifier_used": False})
    print(f"DYNAMIC-001 exploratory raw states={len(raw_states)} metrics={len(diagnostics)} review_required=True")


if __name__ == "__main__":
    main()
