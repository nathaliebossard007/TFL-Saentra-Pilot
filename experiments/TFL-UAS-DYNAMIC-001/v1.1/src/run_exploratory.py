"""DYNAMIC-001 v1.1 operator-only exploratory revision."""
from __future__ import annotations
import json, shutil
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
V10 = ROOT.parent
ALG = V10 / "data" / "algorithm_visible"
EVAL = V10 / "data" / "evaluator_only"
OUT = ROOT / "results" / "exploratory"
RAW = OUT / "raw_revised_dynamic_states"
DIAG = ROOT / "diagnostics"
WINDOWS, LAGS = (5, 15, 30), (1, 5, 15, 30)
PAIRS = [(i, j) for i in range(4) for j in range(i + 1, 4)]
SIM_MIN, MOTION_MIN = 0.8, 0.7


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, separators=(",", ":")), encoding="utf-8")


def arrays(record: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    p = np.asarray([[s["position_xyz"] for s in tr] for tr in record["track_states"]], float)
    v = np.asarray([[s["velocity_xyz"] for s in tr] for tr in record["track_states"]], float)
    a = np.asarray([[s["acceleration_xyz"] for s in tr] for tr in record["track_states"]], float)
    return p, v, a


def corr(a: np.ndarray, b: np.ndarray) -> float | None:
    if len(a) < 2 or np.std(a) < 1e-9 or np.std(b) < 1e-9:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def pair_series(record: dict) -> list[dict[str, np.ndarray]]:
    p, v, a = arrays(record)
    output = []
    for i, j in PAIRS:
        d = np.linalg.norm(p[i] - p[j], axis=1)
        dd = np.gradient(d)
        dv = v[i] - v[j]
        den = np.linalg.norm(v[i], axis=1) * np.linalg.norm(v[j], axis=1)
        direction = np.sum(v[i] * v[j], axis=1) / np.maximum(den, 1e-9)
        ai, aj = np.linalg.norm(a[i], axis=1), np.linalg.norm(a[j], axis=1)
        aden = np.linalg.norm(a[i], axis=1) * np.linalg.norm(a[j], axis=1)
        acc_dir = np.sum(a[i] * a[j], axis=1) / np.maximum(aden, 1e-9)
        output.append({"d": d, "dd": dd, "dv": dv, "speed_i": np.linalg.norm(v[i], axis=1),
                       "speed_j": np.linalg.norm(v[j], axis=1), "direction": direction,
                       "acc_i": ai, "acc_j": aj, "acc_direction": acc_dir})
    return output


def pair_vector(z: dict[str, np.ndarray], t: int, w: int) -> tuple[np.ndarray, dict]:
    start = max(0, t - w + 1)
    dscale = max(float(np.mean(z["d"][start:t + 1])), 1.0)
    speed_corr = corr(z["speed_i"][start:t + 1], z["speed_j"][start:t + 1])
    acc_corr = corr(z["acc_i"][start:t + 1], z["acc_j"][start:t + 1])
    vector = np.r_[z["d"][t] / dscale, z["dd"][t] / 12.0,
                   z["dv"][t] / 8.0, z["direction"][t],
                   speed_corr if speed_corr is not None else 0.0,
                   np.exp(-np.mean(np.std(z["dv"][start:t + 1], axis=0)) / 8.0),
                   acc_corr if acc_corr is not None else 0.0,
                   z["acc_direction"][t]]
    motion = float(np.mean([vector[5], vector[6], vector[7], vector[8]]))
    return vector.astype(float), {"speed_correlation": speed_corr, "acceleration_correlation": acc_corr,
                                  "motion_correlation": motion, "acceleration_defined": acc_corr is not None}


def similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.exp(-np.mean((a - b) ** 2) / 2.0))


def intervals(values: list[bool]) -> list[list[int]]:
    out, start = [], None
    for i, value in enumerate(values + [False]):
        if value and start is None:
            start = i
        elif not value and start is not None:
            out.append([start, i - 1, i - start]); start = None
    return out


def revised_state(record: dict) -> dict:
    pairs = pair_series(record)
    states = {str(w): [] for w in WINDOWS}
    pair_lifetimes, pair_lag = {}, {}
    spatial = []
    for t in range(181):
        spatial.append([float(z["d"][t]) for z in pairs])
    for w in WINDOWS:
        vectors = [[pair_vector(z, t, w) for z in pairs] for t in range(181)]
        for t in range(181):
            rows = []
            for q, (_, details) in enumerate(vectors[t]):
                rows.append({"pair_index": q, **details, "relation_vector": vectors[t][q][0].round(8).tolist()})
            states[str(w)].append(rows)
        for q in range(6):
            stable = [False] * 181
            for t in range(1, 181):
                sim = similarity(vectors[t][q][0], vectors[t - 1][q][0])
                stable[t] = sim >= SIM_MIN and vectors[t][q][1]["motion_correlation"] >= MOTION_MIN
            pair_lifetimes[f"w{w}_p{q}"] = intervals(stable)
            pair_lag[f"w{w}_p{q}"] = {}
            for lag in LAGS:
                values = []
                for t in range(lag, 181):
                    values.append(similarity(vectors[t][q][0], vectors[t - lag][q][0]) >= SIM_MIN)
                pair_lag[f"w{w}_p{q}"][str(lag)] = float(np.mean(values))
    return {"rigid_spatial_relational_state": spatial, "motion_relational_state": states,
            "pair_relation_lifetimes": pair_lifetimes, "pair_lagged_persistence": pair_lag,
            "operator_constants": {"similarity_min": SIM_MIN, "motion_correlation_min": MOTION_MIN,
                                    "windows_s": list(WINDOWS), "lags_s": list(LAGS)}}


def diagnostics(state: dict) -> dict:
    out = {"pair_lagged_persistence": state["pair_lagged_persistence"], "pair_lifetime_summary": {}}
    for key, spans in state["pair_relation_lifetimes"].items():
        durations = [x[2] for x in spans]
        out["pair_lifetime_summary"][key] = {"interval_count": len(spans), "mean_s": float(np.mean(durations) if durations else 0.0), "max_s": int(max(durations) if durations else 0)}
    refs, window_dist = [], {str(w): [] for w in WINDOWS}
    for w in WINDOWS:
        rows = state["motion_relational_state"][str(w)]
        base = np.mean([[*r["relation_vector"]] for t in range(30, 61) for r in rows[t]], axis=0)
        for t in range(181):
            current = np.mean([[*r["relation_vector"]] for r in rows[t]], axis=0)
            refs.append(float(np.linalg.norm(current - base) / np.sqrt(base.size)))
            if t >= w:
                previous = np.mean([[*r["relation_vector"]] for r in rows[t - w]], axis=0)
                window_dist[str(w)].append(float(np.linalg.norm(current - previous) / np.sqrt(base.size)))
    spatial_change = float(np.mean(np.linalg.norm(np.diff(np.asarray(state["rigid_spatial_relational_state"]), axis=0), axis=1)))
    return {"reference_state_distance_series": refs, "reference_state_distance_mean": float(np.mean(refs)),
            "window_motion_state_distance_mean": {k: float(np.mean(v)) for k, v in window_dist.items()},
            "spatial_state_change_mean": spatial_change, "pair_lagged_persistence": out["pair_lagged_persistence"],
            "pair_lifetime_summary": out["pair_lifetime_summary"], "recovery_latency_s": None, "reformation_latency_s": None}


def main() -> None:
    if OUT.exists(): shutil.rmtree(OUT)
    if DIAG.exists(): shutil.rmtree(DIAG)
    RAW.mkdir(parents=True, exist_ok=True); DIAG.mkdir(parents=True, exist_ok=True)
    files = sorted(ALG.glob("sample_*.json"))
    if len(files) != 120: raise RuntimeError(f"expected 120 v1.0 exploratory inputs, got {len(files)}")
    raw = []
    for path in files:
        record = json.loads(path.read_text(encoding="utf-8"))
        if set(record) != {"track_states"}: raise RuntimeError("algorithm-visible schema contaminated")
        raw.append({"sample_id": path.stem, "states": revised_state(record)})
    for row in raw: write(RAW / f"{row['sample_id']}.json", row)
    write(OUT / "raw_state_manifest.json", {"sample_count": len(raw), "source": "DYNAMIC-001 v1.0 algorithm-visible exploratory data", "truth_loaded": False})
    if revised_state(json.loads(files[0].read_text(encoding="utf-8"))) != raw[0]["states"]: raise RuntimeError("determinism gate failed")
    # Evaluator-only phase begins after all raw revised states are serialized.
    truth = {json.loads(p.read_text(encoding="utf-8"))["sample_id"]: json.loads(p.read_text(encoding="utf-8")) for p in sorted(EVAL.glob("eval_*.json"))}
    records = []
    for row in raw:
        meta = truth[row["sample_id"]]; item = diagnostics(row["states"])
        item.update({"sample_id": row["sample_id"], "scenario_id": meta["scenario_id"], "seed": meta["seed"]})
        if meta["scenario_id"] == "D6_perturbation_recovery":
            series = np.asarray(item["reference_state_distance_series"]); base = float(np.mean(series[30:61])); post = np.where(series[101:] <= base * 1.2)[0]
            item["recovery_latency_s"] = float(post[0] + 1 if len(post) else 180.0)
            item["reformation_latency_s"] = float(180.0 if len(post) == 0 else post[0] + 1)
        records.append(item)
    write(DIAG / "exploratory_v1.1_diagnostics.json", {"status": "EXPLORATORY — REVIEW REQUIRED BEFORE EXTENSION", "truth_loaded_after_raw_states": True, "records": records})
    write(OUT / "exploratory_manifest.json", {"sample_count": len(raw), "windows_s": list(WINDOWS), "lags_s": list(LAGS), "simulator_changed": False, "classifier_used": False, "raw_written_before_truth": True})
    print(f"DYNAMIC-001 v1.1 exploratory raw states={len(raw)} records={len(records)} review_required=True")


if __name__ == "__main__": main()
