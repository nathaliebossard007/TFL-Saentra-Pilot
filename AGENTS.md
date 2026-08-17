# Agent Instructions

Before modifying scientific code, every Codex run must read:

1. README.md
2. STATUS.md
3. docs/pilot-brief.md
4. docs/research-baseline.md
5. docs/falsification-rules.md
6. tasks/current-task.md
7. tasks/backlog.md

Additional rules:

- Never modify a frozen predecessor experiment.
- Never expose evaluator-only ground truth to algorithms.
- Never tune confirmatory runs after inspecting confirmatory labels.
- Always write raw outputs before interpretation.
- Every new scientific decision must be appended to docs/decisions.md.
- Update STATUS.md, tasks/current-task.md, and tasks/backlog.md after completing a task.
- Record configuration hashes and deterministic random seeds.
- Fail closed if data leakage is detected.
- If an experiment returns NO-GO, preserve that result.
- Do not add complexity simply to rescue a hypothesis.
