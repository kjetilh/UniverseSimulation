# Relasjonell universgraf v0.15bv: family-structure and feature-symmetry lab

## Formal

Denne runden leter etter familiestruktur etter at samme-locus-duellene mellom add_chord og local_swap ble blandet.
Oppsettet er smalt: target 96, growth seed 202, placements 0-3, perturbasjonene add_chord og local_swap, og fire nye holdout-seeds per profil.

Symmetri betyr her bare feature-level near-symmetry: lav normalisert avstand i support-geometri og carrier-observabler. Det er ikke en graph automorphism claim.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 96 | 96.0 | 96.0 | 96.0 | 1 |

## Aggregert profilkart

| profile | family | coarse | core | shell | rare | spectral rel | dim rel | support b2 | shell2/shell1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p0 | geometry_core_family | 0.771 | 0.623 | 0.298 | 0.079 | 0.063 | 0.098 | 25.000 | 1.750 |
| add_chord_p1 | expanded_shell_family | 0.773 | 0.465 | 0.415 | 0.120 | 0.028 | 0.040 | 37.000 | 1.267 |
| add_chord_p2 | geometry_core_family | 0.839 | 0.602 | 0.333 | 0.065 | 0.078 | 0.045 | 42.000 | 1.167 |
| add_chord_p3 | geometry_core_family | 0.828 | 0.594 | 0.327 | 0.079 | 0.044 | 0.087 | 26.000 | 1.091 |
| local_swap_p0 | geometry_core_family | 0.855 | 0.648 | 0.299 | 0.053 | 0.042 | 0.065 | 25.000 | 1.750 |
| local_swap_p1 | geometry_core_family | 0.955 | 0.724 | 0.251 | 0.025 | 0.040 | 0.172 | 37.000 | 1.267 |
| local_swap_p2 | geometry_core_family | 0.888 | 0.656 | 0.276 | 0.067 | 0.087 | 0.078 | 42.000 | 1.167 |
| local_swap_p3 | spectral_core_family | 0.818 | 0.476 | 0.433 | 0.091 | 0.045 | 0.078 | 26.000 | 1.091 |

## Family summary

| family | n | profiles | mean coarse | mean core | mean rare | mean spectral rel |
| --- | --- | --- | --- | --- | --- | --- |
| geometry_core_family | 6 | add_chord_p0;add_chord_p2;add_chord_p3;local_swap_p0;local_swap_p1;local_swap_p2 | 0.856 | 0.641 | 0.061 | 0.059 |
| expanded_shell_family | 1 | add_chord_p1 | 0.773 | 0.465 | 0.120 | 0.028 |
| spectral_core_family | 1 | local_swap_p3 | 0.818 | 0.476 | 0.091 | 0.045 |

## Beste feature-level near-symmetry-kandidater

| rank | profile A | profile B | family match | support dist | carrier dist | combined | symmetry label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | add_chord_p0 | local_swap_p0 | 1 | 0.000 | 0.228 | 0.114 | support_only_near_symmetry |
| 2 | add_chord_p2 | local_swap_p2 | 1 | 0.000 | 0.239 | 0.120 | support_only_near_symmetry |
| 3 | add_chord_p3 | local_swap_p3 | 0 | 0.000 | 0.251 | 0.126 | support_only_near_symmetry |
| 4 | add_chord_p3 | local_swap_p0 | 1 | 0.396 | 0.156 | 0.276 | carrier_only_near_symmetry |
| 5 | add_chord_p0 | add_chord_p3 | 1 | 0.396 | 0.176 | 0.286 | carrier_only_near_symmetry |
| 6 | add_chord_p1 | add_chord_p2 | 0 | 0.283 | 0.408 | 0.345 | no_near_symmetry |
| 7 | add_chord_p1 | local_swap_p3 | 0 | 0.485 | 0.236 | 0.361 | no_near_symmetry |
| 8 | local_swap_p0 | local_swap_p3 | 0 | 0.396 | 0.388 | 0.392 | no_near_symmetry |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon.
- `family_structure`: `family_structure_without_symmetry_supported` fordi 1 ikke-trivielle family-labels gjentas, men ingen profilpar er naere pa bade support og carrier.
- `symmetry_scope`: `feature_level_only` fordi Symmetri her betyr bare lav normalisert avstand i valgte support/carrier-features, ikke automorfier eller fysisk symmetri.
- `next_step`: `holdout_repeated_families` fordi Neste steg bor teste om de repeterte family-labelene holder under flere seeds for samme placements.

## Tolkning

- Dette er en familie-/symmetriobservabel, ikke en ny bred placement scan.
- Repeterte family-labels er heuristiske grupperinger av målte carrier-features; de skal ikke leses som partikkelarter.
- Near-symmetry-kandidater er nyttige hvis de gir konkrete holdout-kandidater; ellers er riktig reaksjon skalahopp, ikke mer terskelfiksing.
