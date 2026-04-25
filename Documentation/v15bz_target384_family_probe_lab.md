# Relasjonell universgraf v0.15bz: target-384 family probe

## Formal

Denne runden tar samme family-observabler ett hakk videre i skala til target `384`.
Oppsettet er fortsatt smalt: samme growth_seed, samme placements, samme perturbasjoner.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 384 | 384.0 | 384.0 | 384.0 | 1 |

## Target-384 profiler

| profile | family | coarse | core | shell | rare | spectral rel | dim rel | support b2 | shell2/shell1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p0 | spectral_diffuse_rare_family | 0.928 | 0.291 | 0.454 | 0.255 | 0.016 | 0.066 | 67.000 | 1.000 |
| add_chord_p1 | spectral_diffuse_rare_family | 0.910 | 0.271 | 0.466 | 0.262 | 0.025 | 0.073 | 67.000 | 1.000 |
| add_chord_p2 | rare_diffuse_family | 0.765 | 0.284 | 0.432 | 0.284 | 0.060 | 0.038 | 72.000 | 1.654 |
| add_chord_p3 | spectral_core_family | 0.933 | 0.515 | 0.285 | 0.200 | 0.015 | 0.036 | 25.000 | 1.000 |
| local_swap_p0 | spectral_diffuse_rare_family | 0.941 | 0.342 | 0.389 | 0.269 | 0.026 | 0.053 | 67.000 | 1.000 |
| local_swap_p1 | mixed_family | 0.966 | 0.452 | 0.362 | 0.186 | 0.065 | 0.040 | 67.000 | 1.000 |
| local_swap_p2 | rare_diffuse_family | 0.879 | 0.247 | 0.459 | 0.294 | 0.041 | 0.066 | 72.000 | 1.654 |
| local_swap_p3 | spectral_diffuse_rare_family | 0.930 | 0.282 | 0.359 | 0.359 | 0.012 | 0.031 | 25.000 | 1.000 |

## Family summary

| family | n | profiles | mean coarse | mean core | mean rare | mean spectral rel |
| --- | --- | --- | --- | --- | --- | --- |
| spectral_diffuse_rare_family | 4 | add_chord_p0;add_chord_p1;local_swap_p0;local_swap_p3 | 0.927 | 0.297 | 0.286 | 0.020 |
| rare_diffuse_family | 2 | add_chord_p2;local_swap_p2 | 0.822 | 0.265 | 0.289 | 0.051 |
| mixed_family | 1 | local_swap_p1 | 0.966 | 0.452 | 0.186 | 0.065 |
| spectral_core_family | 1 | add_chord_p3 | 0.933 | 0.515 | 0.200 | 0.015 |

## Beste pairwise feature-avstander

| rank | profile A | profile B | family match | support dist | carrier dist | combined | symmetry label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | add_chord_p0 | add_chord_p1 | 1 | 0.000 | 0.103 | 0.051 | support_and_carrier_near_symmetry |
| 2 | add_chord_p0 | local_swap_p0 | 1 | 0.000 | 0.172 | 0.086 | support_and_carrier_near_symmetry |
| 3 | add_chord_p1 | local_swap_p0 | 1 | 0.000 | 0.209 | 0.104 | support_only_near_symmetry |
| 4 | add_chord_p2 | local_swap_p2 | 1 | 0.000 | 0.306 | 0.153 | support_only_near_symmetry |
| 5 | local_swap_p0 | local_swap_p1 | 0 | 0.000 | 0.343 | 0.172 | support_only_near_symmetry |
| 6 | add_chord_p3 | local_swap_p3 | 0 | 0.000 | 0.462 | 0.231 | support_only_near_symmetry |
| 7 | add_chord_p0 | local_swap_p1 | 0 | 0.000 | 0.485 | 0.242 | support_only_near_symmetry |
| 8 | add_chord_p1 | local_swap_p1 | 0 | 0.000 | 0.540 | 0.270 | support_only_near_symmetry |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon.
- `target384_family_probe`: `target384_family_plus_symmetry_candidate` fordi Target 384 har repeterte family-labels og 2 full near-symmetry-kandidater.
- `symmetry_scope`: `feature_level_only` fordi Near-symmetry betyr bare lav normalisert support/carrier-avstand, ikke automorfi eller fysisk symmetri.
- `next_step`: `holdout_target384_candidates` fordi Neste steg bor holde ut de konkrete target-384 kandidatene, ikke utvide søket.

## Tolkning

- Dette er et smalt skalahopp, ikke et bredt nytt search.
- Positivt signal her betyr bare at target 384 organiserer seg mer stabilt i samme feature-rom.
- Symmetri skal ikke leses sterkere enn feature-avstandene tillater.
