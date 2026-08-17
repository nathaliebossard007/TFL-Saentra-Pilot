"""Run only 001B exploratory seeds 101–120 in separated stages."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(name: str) -> None:
    subprocess.run([sys.executable, str(HERE / name)], check=True, cwd=HERE)


def main() -> None:
    run("generate_exploratory.py")
    # This test executes before prediction and before any evaluator truth is loaded.
    run("leakage_tests.py")
    run("predict_exploratory.py")
    if not (HERE.parent / "results" / "exploratory" / "predictions" / "prediction_manifest.json").exists():
        raise RuntimeError("prediction manifest missing after prediction stage")
    run("evaluate_exploratory.py")
    print("EXPLORATORY — NOT CONFIRMATORY EVIDENCE")
    print("confirmatory and held-out seeds were not executed")


if __name__ == "__main__":
    main()
