"""Generate only exploratory TFL-UAS-001B established-track samples."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ALG_ROOT = ROOT / "data" / "algorithm_visible"
EVAL_ROOT = ROOT / "data" / "evaluator_only"
SEEDS = range(101, 121)
AREA = 10000.0
DURATION = 180
DT = 1.0


def opaque_track_id(seed: int, object_index: int) -> str:
    token = hashlib.sha256(f"track/{seed}/{object_index}".encode()).hexdigest()[:12]
    return f"trk_{token}"


def formation_offsets() -> np.ndarray:
    return np.array([[-240.0, -160.0, 0.0], [240.0, -160.0, 0.0],
                     [-240.0, 160.0, 0.0], [240.0, 160.0, 0.0]])


def rotate_xy(v: np.ndarray, angle: float) -> np.ndarray:
    c, s = math.cos(angle), math.sin(angle)
    return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1], v[2]])


def base_centroid(t: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Shared operating region and broad marginal scale for both classes."""
    phase = 0.006 * t
    p = np.array([4100.0 + 22.0 * t + 260.0 * math.sin(phase),
                  3700.0 + 15.0 * t + 180.0 * math.cos(phase),
                  900.0 + 35.0 * math.sin(0.012 * t)])
    v = np.array([22.0 + 1.56 * math.cos(phase),
                  15.0 - 1.08 * math.sin(phase),
                  0.42 * math.cos(0.012 * t)])
    a = np.array([-0.00936 * math.sin(phase), -0.00648 * math.cos(phase),
                  -0.00504 * math.sin(0.012 * t)])
    return p, v, a


def state_for(seed: int, cls: str, obj: int, t: float, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    p0, v0, a0 = base_centroid(t)
    off = formation_offsets()[obj]
    if cls == "coordinated_group":
        # Shared, perturbed turn and acceleration; bounded independent noise.
        turn = 0.13 * math.sin(0.045 * t + 0.13 * seed)
        scale = 1.0 + 0.06 * math.sin(0.031 * t + obj)
        po = rotate_xy(off * np.array([scale, scale, 1.0]), turn)
        vo = rotate_xy(np.array([0.0, 0.0, 0.0]), turn)
        ao = np.array([0.05 * math.sin(0.045 * t + 0.2 * obj),
                       0.04 * math.cos(0.045 * t + 0.15 * obj), 0.01 * math.sin(obj + t / 22)])
        p = p0 + po + np.array([18.0 * math.sin(0.027 * t + obj), 14.0 * math.cos(0.023 * t + obj), 8.0 * math.sin(t / 31 + obj)])
        v = v0 + vo + np.array([0.5 * math.cos(0.027 * t + obj), -0.4 * math.sin(0.023 * t + obj), 0.05 * math.cos(t / 31 + obj)])
        a = a0 + ao
    else:
        # Similar short-term geometry, but independent phase, drift, and maneuvers.
        phase = 0.021 * t + 0.17 * obj + 0.003 * seed
        drift = np.array([85.0 * math.sin(phase), 70.0 * math.cos(phase * 0.83),
                          18.0 * math.sin(phase * 0.61 + obj)])
        correction = np.array([0.9 * math.sin(0.049 * t + obj),
                               0.8 * math.cos(0.041 * t + 0.4 * obj),
                               0.08 * math.sin(t / 17 + obj)])
        p = p0 + off + drift + 20.0 * np.array([math.sin(0.03 * t + obj), math.cos(0.027 * t + obj), 0.0])
        v = v0 + np.array([1.8 * math.cos(phase), -1.5 * math.sin(phase * 0.83), 0.25 * math.cos(phase * 0.61 + obj)])
        a = a0 + correction
    # Deterministic state uncertainty is visible; noise is not class-labelled.
    return p, v, a


def make_sample(seed: int, cls: str, sample_id: str, variant: str) -> tuple[dict, dict]:
    rng = np.random.default_rng(seed * 1009 + (0 if cls == "apparent_group" else 1))
    tracks = []
    for obj in range(4):
        tid = opaque_track_id(seed, obj)
        states = []
        for k in range(DURATION + 1):
            t = float(k * DT)
            p, v, a = state_for(seed, cls, obj, t, rng)
            # The supplied tracks are established but noisy, with the same uncertainty model.
            noise = rng.normal(0.0, [8.0, 8.0, 4.0])
            states.append({"track_id": tid, "timestamp": t,
                          "position_xyz": (p + noise).round(6).tolist(),
                          "velocity_xyz": v.round(6).tolist(),
                          "acceleration_xyz": a.round(6).tolist(),
                          "state_uncertainty": [64.0, 64.0, 16.0]})
        tracks.append(states)
    algorithm_record = {"track_states": tracks}
    evaluator_record = {
        "sample_id": sample_id,
        "ground_truth_object_id": [opaque_track_id(seed, i) for i in range(4)],
        "ground_truth_group_id": "group_0",
        "ground_truth_coordination_state": "coordinated" if cls == "coordinated_group" else "independent",
        "scenario_class": cls,
        "scenario_variant": variant,
        "coordination_start_time": 0.0 if cls == "coordinated_group" else None,
        "coordination_end_time": float(DURATION) if cls == "coordinated_group" else None,
        "seed": seed,
        "simulator_control_variables": {"area_m": [AREA, AREA], "duration_s": DURATION, "dt_s": DT, "object_count": 4}
    }
    return algorithm_record, evaluator_record


def main() -> None:
    ALG_ROOT.mkdir(parents=True, exist_ok=True)
    EVAL_ROOT.mkdir(parents=True, exist_ok=True)
    # The exploratory directory is regenerated only by this explicit exploratory command.
    sample_number = 1
    for seed in SEEDS:
        for cls, variant in [("apparent_group", "development_apparent"), ("coordinated_group", "development_positive")]:
            sample_id = f"sample_{sample_number:04d}"
            alg, truth = make_sample(seed, cls, sample_id, variant)
            (ALG_ROOT / f"{sample_id}.json").write_text(json.dumps(alg, separators=(",", ":")), encoding="utf-8")
            (EVAL_ROOT / f"eval_{sample_number:04d}.json").write_text(json.dumps(truth, separators=(",", ":")), encoding="utf-8")
            sample_number += 1
    print(f"generated exploratory samples={sample_number - 1} seeds=101-120 classes=2")


if __name__ == "__main__":
    main()
