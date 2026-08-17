# TFL-UAS-001A Frozen Provenance

- Experiment ID: TFL-UAS-001A
- Experiment version: 0.1.0
- Archive filename: TFL-UAS-001A_frozen_v0.1.0.zip
- Original archive SHA-256: 00e61bd2aedaff30fa9c19422cdd38fa19bd0e86ca3fcc437607813206a1c9be
- Archive size: 428050 bytes
- Import date: 2026-08-17
- Repository base commit used for import: 3b178fd845b8bfa50d49663829dd2818c818a13a
- Source location: TFL-UAS/TFL-UAS-001A_frozen_v0.1.0.zip
- Imported path: experiments/TFL-UAS-001A/
- Extracted file count: 87 predecessor files
- Extracted structure: README.md; config/tfl_uas_001a_v1.json; src/run_experiment.py; results/ (20 observations, 20 evaluator maps, 20 baseline outputs, 20 RIC outputs, summary.csv, summary.json, aggregate.json); report/TFL-UAS-001A_result.md
- Configuration file SHA-256: 08773ac135820dbffb2948163dd25d36bd0a581a60d0ab838efe0597f98b4797
- Configuration integrity: VERIFIED (the expected hash matches the raw configuration file bytes)
- Runtime summary configuration hash: 7dd8ed915067b7abfe1a38e2c6e59f024f228882ae8397f019565174279f53b8; this is the source code's sorted-JSON serialization hash, not the raw-file hash.
- Deterministic seed range: 101–120
- Scientific status: Track Association — NO-GO
- Archive integrity: VERIFIED
- Scientific separation review: PASS. Observation records contain no ground-truth labels. The baseline and RIC functions receive observations only; evaluator mappings are used by metrics() after predictions are produced. No scenario label or seed is used as an algorithm feature.
- Known limitation: The evaluator mapping is created in the same simulation process and remains in main() scope, but it is not passed to either association function. This historical implementation is preserved unchanged.
- Known limitation: The source ZIP remains in the local, ignored TFL-UAS/ input directory and is not part of the frozen predecessor manifest.

TFL-UAS-001A is a frozen predecessor artifact. Its source, configuration, raw outputs, metrics and research conclusion must not be modified to improve later TFL-UAS results.
