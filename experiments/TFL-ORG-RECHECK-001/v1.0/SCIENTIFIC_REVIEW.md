# Scientific Review — TFL-ORG-RECHECK-001 v1.0

Date: 2026-08-19

## Authorized outcome

`NO_GO_TOY_MODEL_ONLY`

This outcome applies to the preregistered v1.0 cross-over criterion only. It does **not** falsify the broader hypothesis that relational organization can remain stable under large geometric change or that organization-breaking rewiring can be detected by richer relational/operator representations.

## Integrity

The exploratory run processed the frozen historical DYNAMIC-001 algorithm-visible source only. 120 samples × 181 timestamps were handled; raw G/R/P outputs were serialized before evaluator interpretation. No classifier, learned representation, confirmatory, held-out, or source modification was used. Repository guards passed.

## Condition A — geometry-breaking / organization-preserving

Condition A behaves exactly as preregistered. The frozen transform rotates and scales centered geometry by 1.80 while preserving the registered normalized relation construction. In inspected raw output, mean/median pair-distance change is approximately 0.80, pair-distance correlation is approximately 1, relational edge Jaccard is 1.0, and spectrum/lambda2 changes are zero to numerical precision.

This confirms the intended invariance construction but is largely guaranteed by the registered transform. It is therefore a consistency check, not independent evidence for a discovered organizational invariant.

## Condition B — geometry-preserving / organization-breaking

Condition B successfully creates relational rewiring while preserving raw geometry. In inspected raw output, mean/median distance change is 0, pair-distance correlation is 1.0, edge Jaccard is 1/3, four edges change, and the degree sequence is preserved.

However, the registered P layer does not respond: normalized-Laplacian spectrum distance is only numerical noise (~1e-15), lambda2 change is 0, and the rank-2 projector is unavailable because the relevant eigengap is degenerate. Thus the frozen B cross-over criterion requiring either spectrum distance >= 0.10 or lambda2 change >= 0.05 is not met.

## Structural interpretation

The failure is informative. The B perturbation is a degree-preserving 2-switch on an unweighted graph with only four nodes. The inspected source/target graphs can be relationally different while remaining spectrally equivalent under the registered normalized-Laplacian observables. Because the low-mode rank is degenerate, projector evidence is also unavailable. The P representation is therefore too coarse for this perturbation at this graph size.

The pilot demonstrates:

- G can change strongly while the registered R/P construction is invariant under a transform designed to preserve it.
- R can change strongly while G remains exactly unchanged.
- The specific four-node unweighted spectral layer used in v1.0 is **not sufficient** to detect the registered organization-breaking degree-preserving rewiring.

Accordingly the full preregistered G/R/P cross-over was not reproduced on historical data.

## Scientific consequence

Do not authorize systematic TFL/RDL re-analysis from this v1.0 result. Preserve `TFL-ORG-SNAPSHOT-001` as hypothesis-generating only.

A future follow-up, if explicitly authorized, should test whether the limitation is specifically caused by the four-node unweighted P construction. Any revision must be preregistered before execution and should avoid tuning to these outcomes. Candidate directions include richer weighted relational operators, larger historical graphs if genuinely available, or basis-/label-invariant subspace observables that remain defined under the observed degeneracies.

No follow-up is authorized by this review itself.
