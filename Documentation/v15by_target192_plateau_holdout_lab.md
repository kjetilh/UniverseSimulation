# Relasjonell universgraf v0.15by: target-192 plateau holdout

## Formal

Denne runden tester om target-192 plateauet fra `v15bx` holder pa friske seeds.
Forventningen er seks `spectral_diffuse_rare_family`-profiler og to p2-profiler som `mixed_family`.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 192 | 192.0 | 192.0 | 192.0 | 1 |

## Holdout family map

| profile | expected | observed | match | coarse | core | shell | rare | spectral rel | plateau margin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p0 | spectral_diffuse_rare_family | spectral_diffuse_rare_family | 1 | 0.895 | 0.487 | 0.281 | 0.231 | 0.011 | -0.037 |
| add_chord_p1 | spectral_diffuse_rare_family | spectral_diffuse_rare_family | 1 | 0.819 | 0.298 | 0.378 | 0.324 | 0.017 | 0.144 |
| add_chord_p2 | mixed_family | spectral_diffuse_rare_family | 0 | 0.882 | 0.330 | 0.472 | 0.198 | 0.025 | 0.018 |
| add_chord_p3 | spectral_diffuse_rare_family | spectral_diffuse_rare_family | 1 | 0.857 | 0.313 | 0.474 | 0.213 | 0.035 | 0.033 |
| local_swap_p0 | spectral_diffuse_rare_family | spectral_diffuse_rare_family | 1 | 0.835 | 0.318 | 0.330 | 0.352 | 0.005 | 0.132 |
| local_swap_p1 | spectral_diffuse_rare_family | mixed_family | 0 | 0.840 | 0.372 | 0.451 | 0.177 | 0.020 | -0.003 |
| local_swap_p2 | mixed_family | spectral_diffuse_rare_family | 0 | 0.870 | 0.303 | 0.447 | 0.250 | 0.034 | 0.070 |
| local_swap_p3 | spectral_diffuse_rare_family | spectral_diffuse_rare_family | 1 | 0.827 | 0.325 | 0.435 | 0.240 | 0.037 | 0.060 |

## Holdout summary

| group | n | match rate | plateau retention | p2 retention | plateau margin | p2 rare margin | full near symmetries |
| --- | --- | --- | --- | --- | --- | --- | --- |
| all_profiles | 8 | 0.625 | 0.833 | 0.000 | 0.055 | -0.044 | 1 |
| expected_plateau | 6 | 0.833 | 0.833 | nan | 0.055 | nan | 1 |
| expected_p2_outliers | 2 | 0.000 | nan | 0.000 | nan | -0.044 | 1 |

## Beste pairwise feature-avstander

| rank | profile A | profile B | family match | support dist | carrier dist | combined | symmetry label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | add_chord_p3 | local_swap_p3 | 1 | 0.000 | 0.146 | 0.073 | support_and_carrier_near_symmetry |
| 2 | add_chord_p2 | local_swap_p2 | 1 | 0.000 | 0.211 | 0.106 | support_only_near_symmetry |
| 3 | add_chord_p1 | local_swap_p1 | 0 | 0.000 | 0.298 | 0.149 | support_only_near_symmetry |
| 4 | add_chord_p3 | local_swap_p1 | 0 | 0.077 | 0.237 | 0.157 | support_only_near_symmetry |
| 5 | local_swap_p1 | local_swap_p3 | 0 | 0.077 | 0.247 | 0.162 | support_only_near_symmetry |
| 6 | add_chord_p1 | local_swap_p3 | 1 | 0.077 | 0.279 | 0.178 | support_only_near_symmetry |
| 7 | add_chord_p3 | local_swap_p2 | 1 | 0.254 | 0.122 | 0.188 | carrier_only_near_symmetry |
| 8 | local_swap_p2 | local_swap_p3 | 1 | 0.254 | 0.149 | 0.202 | carrier_only_near_symmetry |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon.
- `target192_plateau_holdout`: `target192_plateau_weak_holdout` fordi Target-192 map holder delvis (0.625), men ikke rent nok til mekanismeforklaring.
- `observed_plateau_members`: `observed` fordi add_chord_p0;add_chord_p1;add_chord_p2;add_chord_p3;local_swap_p0;local_swap_p2;local_swap_p3
- `symmetry_holdout`: `full_near_symmetry_candidate` fordi 1 profilpar er full feature-level near-symmetry-kandidater.
- `next_step`: `target384_or_new_observable` fordi Neste steg bor enten hoppe til target 384 eller bytte observabel, ikke presse target 192 terskler.

## Tolkning

- Dette er en holdout av et scale-jump signal, ikke en ny search.
- Hvis plateauet holder, er neste sporsmal mekanisme: hvorfor spectral/diffuse/rare, og hvorfor p2-avviket?
- Ingen symmetry-lesning skal overstige feature-level evidensen.
