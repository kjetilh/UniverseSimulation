# Relasjonell universgraf v0.15bw: family-structure holdout

## Formal

Denne runden tester om family-map fra `v15bv` holder pa friske seeds for samme target/base.
Dette er en holdout, ikke et nytt placement-sok og ikke et skalahopp.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 96 | 96.0 | 96.0 | 96.0 | 1 |

## Holdout family map

| profile | expected | observed | match | coarse | core | shell | rare | spectral rel | geom margin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p0 | geometry_core_family | spectral_core_family | 0 | 0.786 | 0.453 | 0.367 | 0.179 | 0.022 | -0.047 |
| add_chord_p1 | expanded_shell_family | geometry_core_family | 0 | 0.835 | 0.613 | 0.332 | 0.055 | 0.070 | 0.095 |
| add_chord_p2 | geometry_core_family | geometry_core_family | 1 | 0.860 | 0.626 | 0.331 | 0.043 | 0.058 | 0.107 |
| add_chord_p3 | geometry_core_family | mixed_family | 0 | 0.802 | 0.478 | 0.362 | 0.160 | 0.056 | -0.022 |
| local_swap_p0 | geometry_core_family | spectral_core_family | 0 | 0.784 | 0.491 | 0.406 | 0.103 | 0.028 | -0.009 |
| local_swap_p1 | geometry_core_family | geometry_core_family | 1 | 0.846 | 0.633 | 0.312 | 0.054 | 0.055 | 0.096 |
| local_swap_p2 | geometry_core_family | geometry_core_family | 1 | 0.868 | 0.619 | 0.338 | 0.044 | 0.068 | 0.106 |
| local_swap_p3 | spectral_core_family | geometry_core_family | 0 | 0.802 | 0.553 | 0.340 | 0.107 | 0.039 | 0.043 |

## Holdout summary

| group | n | match rate | geometry retention | outlier retention | mean geom margin | full near symmetries |
| --- | --- | --- | --- | --- | --- | --- |
| all_profiles | 8 | 0.375 | 0.500 | 0.000 | 0.038 | 2 |
| expected_geometry_core | 6 | 0.500 | 0.500 | nan | 0.038 | 2 |
| expected_outliers | 2 | 0.000 | nan | 0.000 | nan | 2 |

## Beste pairwise feature-avstander

| rank | profile A | profile B | family match | support dist | carrier dist | combined | symmetry label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | add_chord_p2 | local_swap_p2 | 1 | 0.000 | 0.113 | 0.056 | support_and_carrier_near_symmetry |
| 2 | add_chord_p1 | local_swap_p1 | 1 | 0.000 | 0.172 | 0.086 | support_and_carrier_near_symmetry |
| 3 | add_chord_p3 | local_swap_p3 | 0 | 0.000 | 0.300 | 0.150 | support_only_near_symmetry |
| 4 | add_chord_p0 | local_swap_p0 | 1 | 0.000 | 0.337 | 0.168 | support_only_near_symmetry |
| 5 | add_chord_p1 | local_swap_p2 | 1 | 0.283 | 0.156 | 0.219 | carrier_only_near_symmetry |
| 6 | add_chord_p1 | add_chord_p2 | 1 | 0.283 | 0.204 | 0.243 | no_near_symmetry |
| 7 | local_swap_p1 | local_swap_p2 | 1 | 0.283 | 0.246 | 0.264 | no_near_symmetry |
| 8 | add_chord_p2 | local_swap_p1 | 1 | 0.283 | 0.246 | 0.264 | no_near_symmetry |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon.
- `family_holdout`: `family_structure_not_replicated` fordi Family-map replikerer ikke rent i holdout (0.375).
- `geometry_core_members`: `observed` fordi add_chord_p1;add_chord_p2;local_swap_p1;local_swap_p2;local_swap_p3
- `symmetry_holdout`: `full_near_symmetry_candidate` fordi 2 profilpar er full feature-level near-symmetry-kandidater i holdouten.
- `next_step`: `new_scale_jump` fordi Neste steg bor vaere nytt skalahopp heller enn mer family-threshold-tuning ved target 96.

## Tolkning

- Dette tester replikerbarhet av en heuristisk family-map, ikke eksakte arter.
- Hvis plateauet holder bedre enn outlier-rollene, skal bare plateauet brukes som kontroll i neste skalahopp.
- Full feature-level near-symmetry ville krevd lav avstand i bade support- og carrier-rom; support-only likhet er ikke nok.
