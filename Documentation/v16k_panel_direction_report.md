# v16k advisory-panel direction report

Date: 2026-07-14

## Purposes and goals

Formaal P1 uses `purpose://knowledge`: determine whether the v16j finite event-DAG interval-spectrum contrast repeats on formally fresh histories.

Formaal P2 uses `purpose://validation`: keep source provenance, null limitations, effect existence, magnitude compatibility, and physics claims separated.

Terminal goals:

1. Compare a full fresh replication, a sequential replication, and an event/resource-aware null.
2. Adjudicate the root claims and their undercutters rather than vote on proposals.
3. Freeze a runnable next gate before generating its formal histories.
4. Produce a result that can be negative or inconclusive without being relabeled as success.

## Repo ground truth

v16j retained the v16i interval-spectrum observable and used a directed double-edge-swap perturbation preserving event count, scheduler order, exact direct in/out-degree, exact causal depth and depth profile, and the global dyadic parent-age-bin histogram.

All `384/384` v16h perturbations passed the declared preservation, minimum-change, and uniqueness checks. All `12/12` runs had an effect ratio above one and empirical `p=1/33`. The primary local arm had median ratio `7.975000`. The frozen composite still failed because the v16h/v16d magnitude ratio was `0.469661`, below the preregistered lower bound `0.5`.

The correct working status is therefore `strict_null_contrast_supported_magnitude_transfer_not_stable`, not a claim that the contrast vanished and not a geometry claim.

## Panel and fanout

Four remote advisers received the same repo-grounded state and competing proposals:

- `gpt-5.6-sol`: experimental engineering and implementation feasibility
- `gpt-5.5`: statistical skepticism and stopping/magnitude design
- `gpt-5.6-terra`: causal-order/null-model and claim audit
- `gpt-5.6-luna`: independent program adjudication

The panel is not a voting mechanism. Its outputs were used as support, rebuttals, and undercutters in a second cross-critique round.

All advisers preferred a full fresh-history replication before an event/resource-aware null. The main disagreements were whether to use 12 or 24 arm-specific runs and how to classify magnitude. The cross-critique resolved these as follows:

- Twelve arm-specific runs are the smallest complete replication because they reproduce the v16h balance and retain six primary-arm runs. Twenty-four would improve magnitude precision but is not required to test existence.
- No early-success stop is allowed. A sequential design with six primary runs would create weak and potentially biased magnitude inference.
- Magnitude is descriptive and separate from effect existence. It is classified against the two already frozen factor-two anchor bands.
- The current short swap sampler has perturbation-integrity evidence, not a convergence or uniform-sampling proof.
- A coarse event-family/resource-stratified null is the next mechanism gate only if the fresh contrast replicates.

## Contamination audit

One adviser ran an unregistered in-memory trial on growth seeds `5203` and `5389` and reported its result before the formal design was frozen. Those numbers are not evidence. The seed pair is quarantined, all derived runs are excluded, and no threshold was changed after seeing it.

The formal growth seeds are independently and deterministically derived:

```text
5000 + stable_seed("v16k", "fresh-growth", i) mod 4000
```

This gives `8036` and `6132`. Formal offsets are `96729`, `92980`, and `91663`. None were used in the transient trial.

## Primary-source audit

Glaser and Surya derive interval-abundance expectations for causal sets that faithfully embed into Alexandrov intervals in Minkowski spacetime and use those analytic expectations for locality and dimension diagnostics: <https://arxiv.org/abs/1309.3403>.

That work does not make any arbitrary finite DAG with a repeatable interval spectrum manifoldlike. UniverseSimulation has not compared v16k spectra to the analytic sprinkling family, fitted a dimension, or tested a continuum limit.

Fosdick et al. show that configuration-model choices and graph-space labeling can change scientific conclusions and that sampling design must be specified carefully: <https://doi.org/10.1137/16M1087175>.

Greenhill and Sfragara prove rapid mixing only for stated classes of directed degree sequences and irreducible switch chains: <https://arxiv.org/abs/1701.07101>.

Those results do not establish mixing for the additional depth/order/age-constrained DAG space used here. Therefore v16j/v16k must say `perturbation_integrity`, not proven stationary, representative, independent, or uniform null sampling.

## Claim adjudication before execution

| Claim | Support | Rebuttal or undercutter | Pre-run status |
|---|---|---|---|
| The v16j spectrum contrast exists on fresh histories. | Existing v16h contrast is consistent across 12 runs. | All are one prior history ensemble; null sampling is conditional on a short swap process. | open |
| Effect magnitude is stable. | Both v16d and v16h medians are large relative to their null self-variation. | Frozen v16h/v16d ratio failed at `0.469661`. | unsupported |
| The perturbation sampler is uniform over the constrained DAG space. | Preservation, minimum change, and uniqueness pass. | No convergence/stationarity proof for this constrained chain. | unsupported |
| Event-family/resource wiring is not the mechanism. | None. | The null does not preserve these strata. | unsupported |
| The result establishes geometry or dimension. | Causal-set literature motivates interval observables. | No sprinkling-family fit, continuum scaling, or Lorentz test exists here. | unsupported |

## Selected gate

`relational_universe_v16k_fresh_strict_null_replication.py` will:

1. Generate all 12 fresh arm-specific runs at target `1536` and `3072` events.
2. Reuse v16h history generation and replay/rate audits.
3. Reuse the unchanged v16j primary null with `32` perturbations per run.
4. Evaluate the unchanged v16j primary existence thresholds on six local-arm runs.
5. Run a preregistered `0.10` accepted-swaps-per-edge sensitivity diagnostic with `16` perturbations per run.
6. Classify magnitude as compatible with both prior anchors, v16h only, v16d only, or outside the factor-two compatibility envelope.

The magnitude class cannot change the existence gate. The longer-perturbation diagnostic can make existence inconclusive, because sensitivity to a modestly longer perturbation would undercut interpretation of the primary short-chain contrast.

## Decision branches

- Fresh existence fails: retire the interval-spectrum contrast as a current general candidate.
- Primary exists but longer sensitivity fails: report `inconclusive`; diagnose the null sampler before mechanism claims.
- Existence and longer sensitivity pass: proceed to a separately calibrated coarse event-family/resource-stratified null.
- No branch authorizes dimension, manifoldlikeness, Lorentz symmetry, spacetime, continuum, particles, entanglement, or universal-law claims.
