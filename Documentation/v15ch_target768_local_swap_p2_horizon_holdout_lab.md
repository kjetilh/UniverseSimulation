# Relasjonell universgraf v0.15ch: target-768 local_swap p2 horizon holdout

## Formal

Denne runden holder bare ut den sterkeste resten fra `v15cg`: `local_swap_p2` ved target `768`.
Den bruker friske run-seeds og et lite nabolag av horisont-terskler for aa teste om signalet er mer enn ett enkelt cutoff-treff.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 768 | 768.0 | 768.0 | 768.0 | 1 |

## Profile x threshold summary

| config | profile | established | none | horizon | retention | last12 high | total high | far share | distance | spectral rel |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| loose | local_swap_p0 | 0.000 | 0.833 | 10.167 | 0.112 | 0.000 | 7.167 | 0.644 | 4.726 | 0.009 |
| loose | local_swap_p2 | 0.500 | 0.333 | 65.167 | 0.667 | 0.556 | 65.167 | 0.626 | 6.151 | 0.012 |
| loose | add_chord_p2 | 0.667 | 0.167 | 88.667 | 0.812 | 0.778 | 88.333 | 0.657 | 6.418 | 0.011 |
| baseline | local_swap_p0 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.644 | 4.726 | 0.009 |
| baseline | local_swap_p2 | 0.500 | 0.500 | 63.000 | 0.500 | 0.500 | 63.333 | 0.626 | 6.151 | 0.012 |
| baseline | add_chord_p2 | 0.667 | 0.167 | 87.833 | 0.833 | 0.764 | 87.833 | 0.657 | 6.418 | 0.011 |
| tight | local_swap_p0 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.644 | 4.726 | 0.009 |
| tight | local_swap_p2 | 0.500 | 0.500 | 62.667 | 0.500 | 0.500 | 62.667 | 0.626 | 6.151 | 0.012 |
| tight | add_chord_p2 | 0.667 | 0.167 | 85.167 | 0.833 | 0.708 | 85.167 | 0.657 | 6.418 | 0.011 |

## Candidate comparison

| config | compare | est gap | control none gap | retention gap | last12 gap | horizon gap | distance gap | support score | supported |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| loose | local_swap_p2_minus_local_swap_p0 | 0.500 | 0.500 | 0.555 | 0.556 | 55.000 | 1.425 | 6 | 1 |
| baseline | local_swap_p2_minus_local_swap_p0 | 0.500 | 0.500 | 0.500 | 0.500 | 63.000 | 1.425 | 6 | 1 |
| tight | local_swap_p2_minus_local_swap_p0 | 0.500 | 0.500 | 0.500 | 0.500 | 62.667 | 1.425 | 6 | 1 |

## Cross-carrier contrast

| config | compare | est gap | retention gap | last12 gap | horizon gap | far share gap | distance gap | candidate-specific |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| loose | local_swap_p2_minus_add_chord_p2 | -0.167 | -0.146 | -0.222 | -23.500 | -0.031 | -0.267 | 0 |
| baseline | local_swap_p2_minus_add_chord_p2 | -0.167 | -0.333 | -0.264 | -24.833 | -0.031 | -0.267 | 0 |
| tight | local_swap_p2_minus_add_chord_p2 | -0.167 | -0.333 | -0.208 | -22.500 | -0.031 | -0.267 | 0 |

## Robustness summary

| subject | supported configs | carrier-specific configs | cross-carrier configs | swap2 est min/max | add2 est min/max | support score min/max |
| --- | --- | --- | --- | --- | --- | --- |
| local_swap_p2_far_shell_horizon | loose;baseline;tight | none | loose;baseline;tight | 0.500/0.500 | 0.667/0.667 | 6/6 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon.
- `local_swap_p2_horizon_holdout`: `local_swap_p2_horizon_holdout_supported` fordi local_swap_p2 holder pa holdout ved baseline og 3 av 3 terskelkonfigurasjoner; baseline established-rate er 0.500 mot 0.000 for p0-kontrollen, og add_chord_p2 holder samtidig 0.667 ved baseline.
- `carrier_scope`: `shared_p2_candidate` fordi Begge carrierne viser minst noe p2-horisont i 3 terskelkonfigurasjoner; dette er fortsatt feature-level evidens, ikke en arts-paastand.
- `baseline_control`: `observed` fordi baseline p0 no-horizon=1.000; baseline local support score=6/6.
- `next_step`: `probe_shared_p2_horizon_mechanism` fordi Neste steg bor forklare hvorfor p2 bygger halehorisont pa tvers av carrier, ikke gjenapne bred target-768 family-tuning.

## Tolkning

- Dette er en holdout av en smal p2-lomme, ikke en ny bred target-768-runde.
- Positivt signal her betyr bare at local_swap_p2 ser mer robust ut som feature-level halehorisont under sma terskelendringer.
- Negativt signal her betyr at v15cg traff en svak lomme som ikke holder rent paa friske seeds eller nabo-cutoffs.
