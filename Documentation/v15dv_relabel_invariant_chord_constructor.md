# Relasjonell universgraf v0.15dv: relabel-invariant chord-constructor

## Formal

Dette er instrumenteringssteget som v15du krevde. Ingen ny defect-dynamikk kjoeres.
Legacy `add_chord` endres ikke; tidligere resultater forblir reproducerbare. Den nye helperen definerer en uniform sannsynlighetsfordeling over alle gyldige token-rooted lokale chords.

Symmetrien som kreves er distributional covariance:

`P(phi(c) | phi(G), p) = P(c | G, p)`

for enhver node-ommerking `phi`, candidate chord `c` og placement `p`. Samme RNG-tall trenger ikke gi pathwise transport etter at list order endres.

## Scope

- target: `1024`
- growth seeds: `202;303;404;505;606;707;808;909;1001;1103;1201;1301;1409;1511;1601;1709`
- placements: `p0;p1;p2`
- relabel trials: `192`
- primary gate: exact transported candidate-set equality and probability max error <= `1e-12`

## Candidate landscape

| placement | n_growth_seeds | selected_token_root_fraction | min_candidate_count | median_candidate_count | max_candidate_count | legacy_candidate_coverage | median_candidate_entropy_bits |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 16 | 1.000 | 1 | 12.500 | 44 | 1.000 | 3.633 |
| 1 | 16 | 1.000 | 3 | 15.500 | 56 | 1.000 | 3.947 |
| 2 | 16 | 1.000 | 1 | 10.500 | 36 | 1.000 | 3.391 |

Candidate-count og entropy viser hvor mye skjult constructor-valg legacy first-sorted policy kollapset til ett punkt. Dette er generatorhygiene, ikke fysikk.

## Evaluation

| key | value | evidence |
| --- | --- | --- |
| distributional_relabel_equivariance | 1.000 | candidate probability tolerance=1.0e-12 |
| transported_candidate_set_equality | 1.000 | all transported valid chords must equal the relabelled valid-chord set |
| selected_token_root_coverage | 1.000 | fallback is reported, not hidden |
| legacy_candidate_coverage | 1.000 | legacy first-sorted candidate is contained in the uniform candidate distribution |
| diagnosis | distributionally_relabel_invariant_constructor_ready | instrumentation readiness only; no dynamic effect has been measured |
| next_step | small_constructor_by_coupling_factorial_holdout | factor constructor policy and stochastic coupling before interpreting damage observables |

## Beslutning

- diagnosis: `distributionally_relabel_invariant_constructor_ready`
- next_step: `small_constructor_by_coupling_factorial_holdout`
- claim ceiling: `distributionally relabel-invariant perturbation instrumentation`

Den neste dynamiske testen boer vaere en liten `constructor x coupling`-faktorial:

- constructor: legacy first-sorted vs uniform relabel-invariant
- coupling: maximal vs rank
- primary products: marginal branch-observables og continuous horizon, ikke bare coarse active labels
- stopp hvis constructor eller coupling endrer majority outcome systematisk

Selv full stabilitet i en slik faktorial oppgraderer bare det lokale response-signalet. Lorentz, global invariant, universality og en universe-builder claim krever senere, separate gater.
