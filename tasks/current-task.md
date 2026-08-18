# Current Task

## AUTHORIZED — TFL-RELSTATE-001 protocol freeze only

Open a new exploratory experiment:

**TFL-RELSTATE-001 — Relational Organizational State Equivalence**

This is a new branch of inquiry motivated by review of SPATIAL-001 and DYNAMIC-001. Do not modify or reinterpret frozen predecessor protocols or outputs.

## Primary question

Can a collective system preserve the same organizational state while its absolute geometry, individual trajectories, and local motion vectors change substantially?

The test must distinguish **geometric/kinematic state** from **relational organizational state**.

## Core hypothesis

Organization is not identical to instantaneous geometry or individual predictability. A collective organizational state may persist when:

- absolute positions change;
- formation geometry changes;
- individual trajectories fluctuate;
- local memberships or positions are exchanged;

provided a registered set of relational roles, dependencies, constraints, and slow collective modes remains equivalent under the state evolution.

Use the hierarchy:

`geometry -> pair relations -> local relational structure -> role/dependency structure -> collective organizational state -> state evolution`

Do not collapse these levels into one learned score.

## Required conceptual separation

Freeze explicit observables for at least these layers:

1. **Coordinate / trajectory layer**
   - absolute position, velocity and acceleration only as observables;
   - this layer must not define organization by itself.

2. **Pairwise relational layer**
   - pair distance / normalized distance;
   - relative velocity and distance derivative;
   - local neighbor persistence and exchange.

3. **Collective structural layer**
   - graph/Laplacian representation of relational structure;
   - spectrum plus eigenspace/projector representation where mathematically well-defined;
   - explicit treatment of sign, degeneracy and permutation invariance.

4. **Role/dependency layer**
   - roles must be defined as relational properties or constraints, not absolute coordinates;
   - examples may include interior/exterior role, protected/protecting relation, bridge/core/periphery relation, or equivalent synthetic neutral roles;
   - individual node identity must not be necessary for organizational equivalence unless explicitly registered.

5. **Organizational equivalence layer**
   - define an equivalence relation `~_org` before implementation;
   - geometrically distinct states may be equivalent if the registered relational-role/dependency invariants are preserved;
   - distinguish `state change`, `rule change`, and `organizational breakdown`.

6. **Evolution layer**
   - compare the evolution of registered relational/operator states rather than adjacent geometric similarity alone;
   - define candidate slow/invariant collective subspaces and fast/local variation separately;
   - no quantum-mechanical physical claim is permitted. Hilbert-space/operator language may be used only as a mathematical analogy or finite-dimensional state-space construction.

## Required test families

The protocol must preregister synthetic neutral scenarios that can distinguish the hypothesis without using hostile/attack semantics. At minimum include:

- **R1 Geometric transformation / organizational preservation:** large translation/rotation/shape change with preserved relational-role constraints.
- **R2 Local exchange / organizational preservation:** individuals exchange local positions or roles are reassigned while collective dependency structure remains equivalent.
- **R3 Micro-variability / macro-coherence:** high individual trajectory variability while collective relational structure remains stable.
- **R4 Rigid coordination:** low individual variability and high macro-coherence, as a contrast to R3.
- **R5 Dependency violation:** geometry may remain visually plausible while one or more registered role/dependency constraints are broken.
- **R6 Reorganization:** old organizational equivalence class is left and a new stable equivalence class emerges.
- **R7 Disorganization:** no sustained registered relational-role/dependency structure after perturbation.

R3 vs R4 is a key diagnostic: the operator should not confuse low micro-variance with collective organization.

R1 vs R5 is also key: geometric similarity must not be sufficient for organizational equivalence.

## Primary measurements to preregister

Do not use a classifier as the primary test. Freeze deterministic measurements including:

- micro trajectory variability;
- macro relational/operator stability;
- pair/local-cluster persistence;
- role/dependency constraint preservation;
- graph/Laplacian spectrum distance;
- projector/subspace distance for selected collective modes;
- organizational-equivalence distance or Boolean equivalence rule defined from preregistered invariants;
- transition time when a system leaves one organizational equivalence class;
- if a new stable class emerges, reorganization latency;
- separation of fast local variation from slow collective-state variation.

A simple exploratory ratio such as macro stability versus micro predictability may be recorded descriptively, but it must not be tuned into a decision score during this experiment.

## Critical falsification conditions

The hypothesis is weakened if any of the following occur under the frozen protocol:

- geometrically transformed but organizationally preserved scenarios are consistently judged different;
- visually/geometrically similar dependency-violation scenarios remain indistinguishable from preserved organization;
- the supposed macro state is explainable almost entirely by one trivial geometric marginal;
- R3 high-micro-variability coherent cases collapse while only rigid R4 cases appear organized;
- subspace/operator results add no information beyond raw geometry/kinematics;
- organizational equivalence depends on evaluator labels rather than algorithm-visible relations.

Negative/null outcomes are valid results.

## Protocol-freeze task only

For this task:

1. Create a versioned `experiments/TFL-RELSTATE-001/v1.0/` directory.
2. Write `TFL-RELSTATE-001_PROTOCOL_v1.0.md` and a machine-readable companion config.
3. Define all scenarios, state layers, equivalence rules, invariances, thresholds (if any), windows, subspace selection rules and evaluation metrics before implementation.
4. Explicitly document which quantities are algorithm-visible and which are evaluator-only.
5. Freeze protocol/config hashes in `PROTOCOL_FREEZE.md`.
6. Add guards so frozen predecessors and RELSTATE-001 protocol/config cannot be silently changed.
7. Update `STATUS.md`, `docs/decisions.md`, and `tasks/backlog.md`.
8. Do **not** implement or execute RELSTATE-001 in the same task.

After the freeze, set the next task to:

**Implement TFL-RELSTATE-001 v1.0 exactly as frozen for exploratory seeds only, write raw label-free state/operator outputs before evaluator metadata, then stop at REVIEW_REQUIRED.**

## Scientific gates

- Preserve TFL-UAS-001A, 001B, SPATIAL-001 and DYNAMIC-001 v1.0/v1.1/v1.2/v1.2.1 unchanged.
- No retroactive reinterpretation of predecessor negative or limited results.
- No classifier, neural model, learned representation, learned edge weight or post-hoc threshold fitting in v1.0.
- No confirmatory or held-out execution.
- No physical quantum claim; operator/Hilbert terminology is mathematical state-space language only.
- Raw algorithm-visible outputs must be serialized before evaluator scenario metadata is loaded.
- Stop at REVIEW_REQUIRED after later exploratory execution.
- No GO/PARTIAL GO/NO-GO/INCONCLUSIVE decision during protocol freeze or automatic execution.
