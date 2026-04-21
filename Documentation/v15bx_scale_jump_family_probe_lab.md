# Relasjonell universgraf v0.15bx: scale-jump family probe

## Formal

Denne runden tar skalahoppet som `v15bw` gjorde metodisk riktig: samme observabler, men target `192` i stedet for mer target-96-terskelfiksing.
Family-labels brukes som sonder og kontroller, ikke som etablert familiestruktur.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 192 | 192.0 | 192.0 | 192.0 | 1 |

## Target-192 profiler

| profile | family | coarse | core | shell | rare | spectral rel | dim rel | support b2 | shell2/shell1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p0 | spectral_diffuse_rare_family | 0.789 | 0.241 | 0.493 | 0.267 | 0.011 | 0.026 | 13.000 | 2.333 |
| add_chord_p1 | spectral_diffuse_rare_family | 0.812 | 0.337 | 0.417 | 0.246 | 0.029 | 0.040 | 30.000 | 0.929 |
| add_chord_p2 | mixed_family | 0.886 | 0.379 | 0.461 | 0.160 | 0.013 | 0.068 | 36.000 | 1.062 |
| add_chord_p3 | spectral_diffuse_rare_family | 0.849 | 0.384 | 0.408 | 0.208 | 0.016 | 0.024 | 30.000 | 1.250 |
| local_swap_p0 | spectral_diffuse_rare_family | 0.837 | 0.270 | 0.450 | 0.280 | 0.030 | 0.036 | 13.000 | 2.333 |
| local_swap_p1 | spectral_diffuse_rare_family | 0.822 | 0.331 | 0.473 | 0.196 | 0.026 | 0.047 | 30.000 | 0.929 |
| local_swap_p2 | mixed_family | 0.915 | 0.411 | 0.440 | 0.149 | 0.045 | 0.039 | 36.000 | 1.062 |
| local_swap_p3 | spectral_diffuse_rare_family | 0.884 | 0.339 | 0.439 | 0.222 | 0.020 | 0.043 | 30.000 | 1.250 |

## Family summary

| family | n | profiles | mean coarse | mean core | mean rare | mean spectral rel |
| --- | --- | --- | --- | --- | --- | --- |
| spectral_diffuse_rare_family | 6 | add_chord_p0;add_chord_p1;add_chord_p3;local_swap_p0;local_swap_p1;local_swap_p3 | 0.832 | 0.317 | 0.236 | 0.022 |
| mixed_family | 2 | add_chord_p2;local_swap_p2 | 0.900 | 0.395 | 0.154 | 0.029 |

## Beste pairwise feature-avstander

| rank | profile A | profile B | family match | support dist | carrier dist | combined | symmetry label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | add_chord_p1 | local_swap_p1 | 1 | 0.000 | 0.237 | 0.119 | support_only_near_symmetry |
| 2 | add_chord_p3 | local_swap_p3 | 1 | 0.000 | 0.276 | 0.138 | support_only_near_symmetry |
| 3 | add_chord_p1 | local_swap_p3 | 1 | 0.077 | 0.204 | 0.140 | support_only_near_symmetry |
| 4 | local_swap_p1 | local_swap_p3 | 1 | 0.077 | 0.250 | 0.163 | support_only_near_symmetry |
| 5 | add_chord_p2 | local_swap_p2 | 1 | 0.000 | 0.349 | 0.175 | support_only_near_symmetry |
| 6 | add_chord_p1 | add_chord_p3 | 1 | 0.077 | 0.281 | 0.179 | support_only_near_symmetry |
| 7 | add_chord_p3 | local_swap_p1 | 1 | 0.077 | 0.322 | 0.199 | support_only_near_symmetry |
| 8 | add_chord_p0 | local_swap_p0 | 1 | 0.000 | 0.424 | 0.212 | support_only_near_symmetry |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon.
- `scale_jump_family_probe`: `scale_jump_family_plateau_supported` fordi Target 192 viser en dominerende familie med 6 av 8 profiler; 0 full near-symmetry-kandidater.
- `symmetry_scope`: `feature_level_only` fordi Near-symmetry betyr bare lav normalisert support/carrier-avstand, ikke automorfi eller fysisk symmetri.
- `next_step`: `holdout_target192_family_plateau` fordi Neste steg bor validere target-192 plateauet pa friske seeds for a se om skalahoppet faktisk stabiliserte familiestrukturen.

## Tolkning

- Dette er et smalt skalahopp etter en negativ holdout, ikke en bred ny scan.
- Positivt signal her betyr bare at target 192 kan ha et mer stabilt feature-plateau enn target 96.
- Symmetrikandidater ma holdes pa friske seeds for de kan brukes som mer enn navigasjon.
