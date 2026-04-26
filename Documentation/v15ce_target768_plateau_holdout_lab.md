# Relasjonell universgraf v0.15ce: target-768 plateau holdout

## Formal

Denne runden tester om target-768 plateauet fra `v15cd` holder pa friske seeds.
Forventningen er sju `rare_diffuse_family`-profiler, `add_chord_p0` som spectral outlier, og to full near-symmetry-par.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 768 | 768.0 | 768.0 | 768.0 | 1 |

## Holdout family map

| profile | expected | observed | match | coarse | core | shell | rare | spectral rel |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p0 | spectral_diffuse_rare_family | spectral_diffuse_rare_family | 1 | 0.928 | 0.268 | 0.344 | 0.389 | 0.021 |
| add_chord_p1 | rare_diffuse_family | rare_diffuse_family | 1 | 0.814 | 0.121 | 0.328 | 0.550 | 0.003 |
| add_chord_p2 | rare_diffuse_family | rare_diffuse_family | 1 | 0.793 | 0.129 | 0.383 | 0.488 | 0.001 |
| add_chord_p3 | rare_diffuse_family | rare_diffuse_family | 1 | 0.775 | 0.170 | 0.409 | 0.420 | 0.023 |
| local_swap_p0 | rare_diffuse_family | spectral_diffuse_rare_family | 0 | 0.964 | 0.169 | 0.425 | 0.406 | 0.011 |
| local_swap_p1 | rare_diffuse_family | rare_diffuse_family | 1 | 0.907 | 0.268 | 0.425 | 0.307 | 0.014 |
| local_swap_p2 | rare_diffuse_family | rare_diffuse_family | 1 | 0.773 | 0.100 | 0.428 | 0.473 | 0.009 |
| local_swap_p3 | rare_diffuse_family | spectral_diffuse_rare_family | 0 | 0.879 | 0.282 | 0.422 | 0.296 | 0.008 |

## Holdout summary

| group | n | match rate | plateau retention | outlier retention | full near retention |
| --- | --- | --- | --- | --- | --- |
| all_profiles | 8 | 0.750 | 0.714 | 1.000 | 0.500 |
| expected_plateau | 7 | 0.714 | 0.714 | nan | 0.500 |
| expected_outlier | 1 | 1.000 | nan | 1.000 | 0.500 |

## Full near-symmetry holdout

| pair | retained full near | support dist | carrier dist | combined | rank | observed label |
| --- | --- | --- | --- | --- | --- | --- |
| add_chord_p1::add_chord_p2 | 0 | 0.112 | 0.251 | 0.181 | 2 | support_only_near_symmetry |
| add_chord_p2::local_swap_p2 | 1 | 0.000 | 0.187 | 0.094 | 1 | support_and_carrier_near_symmetry |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon.
- `target768_plateau_holdout`: `target768_plateau_weak_holdout` fordi Target-768 map holder delvis (0.750), men ikke rent nok til mekanismeforklaring.
- `observed_plateau_members`: `observed` fordi add_chord_p1;add_chord_p2;add_chord_p3;local_swap_p1;local_swap_p2
- `retained_full_near_pairs`: `observed` fordi add_chord_p2::local_swap_p2
- `next_step`: `target768_second_holdout_or_mechanism` fordi Neste steg bor vaere en enda smalere holdout eller en mekanismeobservabel, ikke mer family-label-tuning.

## Tolkning

- Dette er en holdout av et scale-jump signal, ikke en ny search.
- Positivt signal betyr at target-768 plateauet er mer enn en engangseffekt av seed-valg.
- Ingen symmetry-lesning skal overstige feature-level evidensen.
