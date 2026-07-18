# UniverseSimulation Argumentation Map

Last source review: 2026-07-18.

## Research question

The program asks whether a very small ontology and local stochastic graph rules
can produce sufficiently robust higher-level regularities to justify saying
that universe-like law structure is possible in this model family.

The project is not trying to match our universe by visual analogy. It requires
operational observables, controls, transfer tests, and explicit failure gates.

## Evidence levels

1. **Formal/algebraic**: definitions, exact identities, relabel covariance, and
   rule-level facts.
2. **Generator/instrumentation**: what the simulator constructs or logs and
   whether replay/integrity checks pass.
3. **Executed result**: values from completed, source-locked runs or analyses.
4. **Inference**: the narrow interpretation supported by those results.
5. **Open proposal**: a not-yet-executed next experiment.

Generator hygiene is not physics. A scoring artifact is not a dynamical result.

## Primitive program

- relational state represented by a dynamic graph
- local stochastic updates
- event-based causal dependency rather than assumed background spacetime
- emergent rather than presupposed geometry, particles, and conservation laws
- relabel covariance as a minimum representation-symmetry requirement

The implemented simulator is an experimental relative of the formal program,
not an exact realization of every DPO/CTMC statement in the research report.

## What has survived so far

- `band_zero_del` is the current operational frontier regime.
- Defect perturbations show persistent local damage and non-superposition under
  matched controls.
- Event-DAG construction, replay, relabel, and several coarse-map contracts have
  passed their declared integrity gates.
- Open causal-interval abundance is an exact finite-poset observable and shows a
  repeatable contrast beyond the v16i layer+indegree null.
- v16j shows that the contrast remains under exact direct in/out-degree, exact
  depth, scheduler-order, and global dyadic parent-age controls.
- v16s replicated a finite event-DAG full-spectrum contrast on fresh histories;
  v16u closed the known realized-effort confound in the local footprint-null
  procedure.
- v16v showed effect-blind that all six sources admit multiple complete global
  edge-slot reconstructions independent of the local switch path: `48/48`
  integrity passes and `8/8` distinct endpoints per source.
- v16w showed that finite endpoint diversity is not enough to qualify that
  global family. Structural integrity passed `288/288`, but candidate-column
  covariance was only `8/24` and objective sensitivity only `15/36`.
- v16x repaired representation dependence with canonical integer random costs:
  endpoint integrity passed `192/192` and replay/permutation/relabel covariance
  passed `24/24`. A residual-SCC audit also proved that the most concentrated
  edges lie on feasible alternating cycles and are not globally forced.
- v16y implemented a lazy degree-corrected 2x2 Metropolis law. Tested detailed
  balance passed `48/48`, representation passed `6/6`, and all `24/24` finite
  chains met the movement criterion.
- v16z gave exact pair-specific alternating-cycle decompositions for all six
  v16y start pairs: `2139` cycles total, full coverage, and whole-cycle
  forward/reverse replay `6/6`.
- v17a turned that direction into a target-independent finite proposal with an
  explicit reverse auxiliary and exact Metropolis ratio. Frozen-start replay
  and representation passed `12/12`; reverse support and pathwise detailed
  balance passed `84/84`; runtime passed `24/24`.
- v17b replaced the low-yield random walk with exact residual-cycle
  enumeration. Matched valid yield improved `24/24` with median ratio
  `2.898276`, and finite movement passed `24/24`, while exact reverse support
  and pathwise balance passed `36/36`.
- v17c preserved that exact proposal law and replayed all `24/24` v17b
  transition traces exactly using completion counting plus uniform rank
  sampling. Count/support parity passed `36/36`, movement and resource passed
  `24/24`, maximum runtime was `14.921836` seconds, and no source effect was
  computed.
- v17d extended that qualified kernel to 2048 steps with both starts and two
  fresh seeds. Traversal/resource passed `24/24`, residual-component centers
  `90/90`, and proposal-footprint overlap `18/18`. Endpoint centers passed only
  `85/108` and distance agreement `12/18`; all distance failures were the
  start-family contrast. Source effects remained closed.
- v17e matched the v17d random-stream prefix exactly at `192/192` checkpoints
  and doubled the budget to 4096 steps. Integrity, reversibility,
  representation and traversal/resource all passed, but material cross-start
  contraction passed `0/6`; scale/baseline ratios were
  `0.978973-1.005348`.
- The v17e post-run diagnosis found within-start dispersion expansion of
  `1.385802-1.470668` in all six sources while absolute cross-start distance
  stayed flat. This retires more scale growth for the length-2-to-4 move class;
  it does not prove global disconnection or reject other reversible moves.

The coarse global feasible set is nontrivial, but v16x rejected the random-cost
endpoint measure before testing whether the v16s effect survives. Only `2/6`
sources passed the frozen diversity gate; after combining both declared seed
families, `4/6` still exceeded the `0.95` top-edge inclusion bound. The result
does not distinguish structural probability concentration from bias induced by
the random-min-cost probability law.

V16y does not resolve that ambiguity. Its local kernel is reversible, but the
finite endpoints are strongly start-dependent: all `24` failed center rows are
start comparisons, cross-start distance is about `0.422`, and within-start
distance about `0.078`. The chain concentration profile is worse than the v16x
reference on all six sources. This supports a move-accessibility diagnosis, not
a claim that the move graph is disconnected.

V16z narrows the accessibility question without resolving it globally. The
target-directed 2x2 search reduced each pair mismatch by more than `98%` but
found `0/6` complete paths under the frozen bounds. Exact pair-specific
whole-cycle paths exist, yet they do not define a state-independent proposal
law. The formal representation status remains failed because it compared raw
relabel-dependent slot keys; a post-run edge-move audit passed `6/6` and is a
diagnosis, not a retroactive preregistered pass.

V17a qualifies the tested proposal algebra but rejects its finite execution.
Movement passed `0/24`: all chains reached `16-40` unique states, yet none met
all preregistered proposal-count, accepted-cycle, long-cycle and five-percent
displacement floors. The post-run diagnosis points to low valid-cycle yield and
small finite displacement, not representation, reversibility, detailed-balance
or runtime failure. This neither proves disconnected components nor weakens the
earlier finite spectrum contrast; the effect was not computed.

V17b repairs that finite-movement failure but does not yet provide a usable
sampler. Resource passed only `12/24`, with chain runtime from `27.479260` to
`270.449001` seconds. The result supports the residual constructor's finite
yield and movement on the six reused spaces, not convergence, mixing, global
support or the v16s effect. A post-run runtime diagnosis is explicitly
exploratory and identifies implementation costs without changing the frozen
v17b status.

V17c isolates that resource failure as an implementation cost on the tested
finite spaces. It retained the exact ordered support, proposal probabilities,
reverse auxiliary, starts, seeds and transition paths while reducing the median
runtime ratio to `0.161356` and passing the frozen resource bound `24/24`. This
qualifies the implementation for a finite stability test. It does not establish
irreducibility, convergence, mixing, a unique endpoint law or survival of the
v16s spectrum contrast.

V17d shows that runtime qualification was not enough to remove finite start
memory. Seed and early/late distance comparisons passed `12/12`, while all six
start-family distance comparisons failed with cross/within ratios
`2.656766-2.906643`. Source-edge/conflict gaps contracted in `12/12` postrun
cells, but direct cross-start endpoint distance was effectively flat. Exact
residual-SCC profiles were identical across both starts, both seeds and both
windows within each source. This supports one bounded scale-response test, not
global connectivity, convergence, mixing or source-effect survival.

V17e executed that bounded test with an exact matched v17d prefix. All
`192/192` checkpoint endpoints replayed before continuation to 4096 steps, and
all probability, representation, traversal and resource checks passed. The
material absolute cross-start contraction nevertheless passed `0/6`, with
scale/baseline ratios `0.978973-1.005348`. Within-start dispersion expanded
`1.385802-1.470668`, so the lower cross/within ratios are diffusion within the
start clouds rather than center convergence. This retires more scale growth of
the tested length-2-to-4 kernel and motivates a broader reversible move class;
it does not establish disconnected components or reject the model family.

## What has been explained away or remains negative

- Lorentz-like propagation remains `not_yet` because placement and mode effects
  remain live and local isotropy is not established.
- A spectral quasi-invariant candidate was local and did not become a broad law.
- Clock/depth alignment is reproducible, but v16h attributes it to the
  scheduler's pre-event total-rate profile rather than independent geometry.
- Defect labels, persistence, recurrence, and genealogy are useful observables,
  but do not establish particle species.
- Correlation or shared response is not quantum entanglement.
- Bell's theorem, a chosen Bell inequality and observed finite Bell-test data
  are separate evidential layers. UniverseSimulation currently has no local
  setting/outcome trial protocol, causal separation audit or Bell statistic.
- Tokens and local rewrite events provide repo-grounded ingredients for an
  action-density or change-intensity hypothesis. The older weighted energy
  functional was chosen instrumentation, not emergent energy. No temperature
  exists until a local balance law and reproducible intensive fluctuation
  parameter are demonstrated.

## Threshold for stronger claims

To claim that robust universe-like law structure is possible in this model,
one isolated positive observable is insufficient. At minimum, the program needs
several jointly surviving properties:

- representation/relabel robustness
- locality and causal propagation not reducible to scheduler bookkeeping
- a stable invariant or quasi-invariant with cross-seed and cross-scale transfer
- nontrivial persistent excitations and interactions under matched controls
- predictive coarse-graining or a robust continuum/geometry proxy
- fresh preregistered replication and explicit adversarial nulls

To claim Lorentz-like spacetime specifically requires substantially more:
isotropy, dispersion/propagation tests, observer- or placement-robust behavior,
and a geometry estimator that survives mechanism controls and scale transfer.

## Current argument conclusion

The project has demonstrated that local graph rules can generate nontrivial,
repeatable finite relational structure worth continued study. It has not shown
that a universe, spacetime, Lorentz symmetry, particles, entanglement, or a
continuum emerges.

The best current next test is one effect-blind move-class expansion on the same
coarse feasible matching space. Retain v16x-v17e as controls. Preserve an
explicit stationary target and exact reverse accounting, but add a genuinely
broader transition such as an exact longer alternating cycle or reversible
compound-cycle proposal. Compare start-memory response under matched realized
work before source-spectrum inspection. Concrete conflict remains a required
diagnostic because exact preservation collapsed the available finite freedom.
The units-of-action
energy/cooling question remains a promising later mechanism gate, but must not
bypass null qualification or use uniform clock-rate scaling as a temperature
intervention.
