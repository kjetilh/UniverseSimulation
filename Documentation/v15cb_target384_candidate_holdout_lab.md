# Relasjonell universgraf v0.15cb: target-384 candidate holdout

## Formal

Denne runden holder ut den konkrete target-384-kandidatmappen fra `v15bz`.
Det inkluderer bade family-labels og de to full feature-level near-symmetry-kandidatene.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 384 | 384.0 | 384.0 | 384.0 | 1 |

## Holdout family map

| profile | expected | observed | match | coarse | core | shell | rare | spectral rel |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p0 | spectral_diffuse_rare_family | spectral_diffuse_rare_family | 1 | 0.969 | 0.378 | 0.407 | 0.215 | 0.054 |
| add_chord_p1 | spectral_diffuse_rare_family | spectral_diffuse_rare_family | 1 | 0.953 | 0.379 | 0.379 | 0.243 | 0.036 |
| add_chord_p2 | rare_diffuse_family | spectral_diffuse_rare_family | 0 | 0.886 | 0.230 | 0.452 | 0.318 | 0.017 |
| add_chord_p3 | spectral_core_family | rare_diffuse_family | 0 | 0.853 | 0.322 | 0.376 | 0.302 | 0.033 |
| local_swap_p0 | spectral_diffuse_rare_family | rare_diffuse_family | 0 | 0.941 | 0.302 | 0.446 | 0.252 | 0.062 |
| local_swap_p1 | mixed_family | rare_diffuse_family | 0 | 0.946 | 0.296 | 0.428 | 0.275 | 0.046 |
| local_swap_p2 | rare_diffuse_family | rare_diffuse_family | 1 | 0.951 | 0.334 | 0.418 | 0.248 | 0.033 |
| local_swap_p3 | spectral_diffuse_rare_family | spectral_diffuse_rare_family | 1 | 0.922 | 0.323 | 0.427 | 0.250 | 0.030 |

## Holdout summary

| group | n | match rate | quartet retention | rare-pair retention | full near retention |
| --- | --- | --- | --- | --- | --- |
| all_profiles | 8 | 0.500 | 0.750 | 0.500 | 0.000 |
| spectral_diffuse_rare_quartet | 4 | 0.750 | 0.750 | nan | 0.000 |
| rare_diffuse_pair | 2 | 0.500 | nan | 0.500 | 0.000 |

## Expected full near-symmetry pairs

| pair | retained | support dist | carrier dist | combined | rank | observed label |
| --- | --- | --- | --- | --- | --- | --- |
| add_chord_p0 / add_chord_p1 | 0 | 0.000 | 0.337 | 0.169 | 1 | support_only_near_symmetry |
| add_chord_p0 / local_swap_p0 | 0 | 0.000 | 0.377 | 0.189 | 5 | support_only_near_symmetry |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon.
- `target384_holdout`: `target384_candidates_not_replicated` fordi Target-384-kandidatene replikerer ikke rent (0.500).
- `observed_quartet`: `observed` fordi add_chord_p0;add_chord_p1;add_chord_p2;local_swap_p3
- `retained_full_near_pairs`: `observed` fordi none
- `next_step`: `new_observable_or_scale_decision` fordi Neste steg bor bytte observabel eller ta en ny skalaavgjorelse.

## Tolkning

- Dette er en holdout av konkrete target-384 kandidater, ikke et nytt target-384 search.
- Positivt signal betyr at både cluster-strukturen og de beste near-symmetry-parene faktisk har noen ben å stå på.
