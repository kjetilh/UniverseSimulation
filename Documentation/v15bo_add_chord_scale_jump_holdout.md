# Relasjonell universgraf v0.15bo: add_chord scale-jump holdout

## Formal

Denne runden tester 48/p2 mot den svakeste men beste 96-kandidaten fra v15bn (p3), med 96/p1 som naermeste kontrollrival.

## Startstorrelser

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |

## Aggregate profiler

| profile | role | exact | coarse | core | shell | rare | spectral | dim | best metric | spectral rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| anchor_48_p2 | anchor | 0.901 | 0.930 | 0.925 | 0.072 | 0.003 | 0.146 | 0.138 | abs_delta_dim_proxy_rel | 2 |
| control_96_p1 | control | 0.127 | 0.889 | 0.657 | 0.297 | 0.047 | 0.066 | 0.066 | abs_delta_dim_proxy_rel | 2 |
| candidate_96_p3 | candidate | 0.196 | 0.818 | 0.583 | 0.309 | 0.108 | 0.066 | 0.077 | abs_delta_spectral_radius_rel | 1 |

## Holdout-sammenlikning mot anker

| other profile | role | combined | coarse | spectral gap | best metric | spectral rank | rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| control_96_p1 | control | 1.370 | 1.362 | 0.008 | abs_delta_dim_proxy_rel | 2 | 1 |
| candidate_96_p3 | candidate | 1.533 | 1.513 | 0.019 | abs_delta_spectral_radius_rel | 1 | 2 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsene er rent separert og alle holdout-runs matcher onsket add_chord-perturbasjon.
- `holdout_scale_pair`: `scale_jump_pair_not_yet` fordi 96/p3 holder ikke klart nok foran 96/p1 pa holdout til at vi kan lese dette som en ekte liten skalafamilie.
- `next_step`: `explain_scale_break` fordi Neste steg bor forklare hvor 48->96-likheten bryter, ikke late som scale-transfer allerede holder.

## Tolkning

- Dette er en ren holdout-tie-break for en liten add_chord-skalaovergang.
- Positivt signal her betyr bare at vi har et bedre grunnlag for a snakke om en smal familiespesifikk skalaovergang.
