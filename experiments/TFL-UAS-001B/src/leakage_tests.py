"""Fail-closed schema and lineage tests for the exploratory phase."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALG = ROOT / "data" / "algorithm_visible"
EVAL = ROOT / "data" / "evaluator_only"
ALLOWED = {"track_id", "timestamp", "position_xyz", "velocity_xyz", "acceleration_xyz", "state_uncertainty"}


def main() -> None:
    files = sorted(ALG.glob("sample_*.json"))
    if not files: raise AssertionError("no algorithm-visible samples")
    if any(re.search(r"101|102|103|104|105|106|107|108|109|110|111|112|113|114|115|116|117|118|119|120|apparent|coordinated|group|positive|negative", p.name, re.I) for p in files):
        raise AssertionError("algorithm-visible filename leaks seed or class")
    ids = set()
    for path in files:
        rec = json.loads(path.read_text(encoding="utf-8"))
        if set(rec) != {"track_states"}: raise AssertionError("algorithm record top-level schema mismatch")
        for track in rec["track_states"]:
            for state in track:
                if set(state) != ALLOWED: raise AssertionError(f"hidden field in {path.name}")
                ids.add(state["track_id"])
                if any(token in state["track_id"].lower() for token in ["seed", "apparent", "coordinated", "group"]): raise AssertionError("track ID leaks semantics")
    source = (Path(__file__).with_name("predict_exploratory.py")).read_text(encoding="utf-8").lower()
    if "evaluator_only" in source or "ground_truth" in source: raise AssertionError("prediction source references evaluator truth")
    if len(files) != 40 or len(ids) != 80: raise AssertionError("unexpected exploratory sample or track count")
    print("leakage/schema tests passed")


if __name__ == "__main__":
    main()
