# Relasjonell universgraf v0.15cd: target-768 family probe

## Formal

Denne runden tar samme family-observabler ett hakk videre i skala til target `768`.
Maalet er en ren skalaavgjorelse etter at `v15cc` ikke fant en overbevisende ny target-384-observabel.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 768 | 768.0 | 768.0 | 768.0 | 1 |

## Target-768 profiler

| profile | family | coarse | core | shell | rare | spectral rel | dim rel | support b2 | shell2/shell1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p0 | spectral_diffuse_rare_family | 0.897 | 0.234 | 0.449 | 0.317 | 0.008 | 0.032 | 24.000 | 1.625 |
| add_chord_p1 | rare_diffuse_family | 0.858 | 0.202 | 0.394 | 0.404 | 0.009 | 0.003 | 21.000 | 0.636 |
| add_chord_p2 | rare_diffuse_family | 0.910 | 0.149 | 0.395 | 0.456 | 0.011 | 0.003 | 22.000 | 0.900 |
| add_chord_p3 | rare_diffuse_family | 0.948 | 0.243 | 0.446 | 0.311 | 0.014 | 0.006 | 74.000 | 2.944 |
| local_swap_p0 | rare_diffuse_family | 0.917 | 0.215 | 0.432 | 0.353 | 0.016 | 0.012 | 24.000 | 1.625 |
| local_swap_p1 | rare_diffuse_family | 0.933 | 0.303 | 0.346 | 0.351 | 0.019 | 0.006 | 21.000 | 0.636 |
| local_swap_p2 | rare_diffuse_family | 0.930 | 0.111 | 0.450 | 0.439 | 0.009 | 0.000 | 22.000 | 0.900 |
| local_swap_p3 | rare_diffuse_family | 0.863 | 0.233 | 0.493 | 0.274 | 0.036 | 0.007 | 74.000 | 2.944 |

## Family summary

| family | n | profiles | mean coarse | mean core | mean rare | mean spectral rel |
| --- | --- | --- | --- | --- | --- | --- |
| rare_diffuse_family | 7 | add_chord_p1;add_chord_p2;add_chord_p3;local_swap_p0;local_swap_p1;local_swap_p2;local_swap_p3 | 0.908 | 0.208 | 0.370 | 0.016 |
| spectral_diffuse_rare_family | 1 | add_chord_p0 | 0.897 | 0.234 | 0.317 | 0.008 |

## Beste pairwise feature-avstander

| rank | profile A | profile B | family match | support dist | carrier dist | combined | symmetry label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | add_chord_p2 | local_swap_p2 | 1 | 0.000 | 0.159 | 0.079 | support_and_carrier_near_symmetry |
| 2 | add_chord_p0 | local_swap_p0 | 0 | 0.000 | 0.289 | 0.144 | support_only_near_symmetry |
| 3 | add_chord_p1 | add_chord_p2 | 1 | 0.112 | 0.182 | 0.147 | support_and_carrier_near_symmetry |
| 4 | add_chord_p3 | local_swap_p3 | 1 | 0.000 | 0.356 | 0.178 | support_only_near_symmetry |
| 5 | add_chord_p1 | local_swap_p2 | 1 | 0.112 | 0.291 | 0.201 | support_only_near_symmetry |
| 6 | add_chord_p1 | local_swap_p1 | 1 | 0.000 | 0.454 | 0.227 | support_only_near_symmetry |
| 7 | add_chord_p2 | local_swap_p0 | 1 | 0.204 | 0.272 | 0.238 | no_near_symmetry |
| 8 | local_swap_p0 | local_swap_p2 | 1 | 0.204 | 0.289 | 0.246 | no_near_symmetry |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon.
- `target768_family_probe`: `target768_family_plateau_supported` fordi Target 768 viser en dominerende familie med 7 av 8 profiler; 2 full near-symmetry-kandidater.
- `symmetry_scope`: `feature_level_only` fordi Near-symmetry betyr bare lav normalisert support/carrier-avstand, ikke automorfi eller fysisk symmetri.
- `next_step`: `holdout_target768_plateau` fordi Neste steg bor holde ut target-768 plateauet pa friske seeds.

## Tolkning

- Dette er et smalt skalahopp, ikke et bredt nytt search.
- Positivt signal her betyr bare at target 768 organiserer seg mer stabilt i samme feature-rom.
- Symmetri skal ikke leses sterkere enn feature-avstandene tillater.
