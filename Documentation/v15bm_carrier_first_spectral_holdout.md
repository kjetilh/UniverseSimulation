# Relasjonell universgraf v0.15bm: carrier-first spectral holdout

## Formal

Denne runden tester om de to beste spektrale lommene fra v15bl holder mot naerliggende kontrollcarrier-pa friske holdout-seeds.

## Startstorrelser

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |

## Holdout-conditions

| condition | perturbation | role | spectral | dim | best non-trivial | spectral rank | dim-spectral |
| --- | --- | --- | --- | --- | --- | --- | --- |
| buffered_heavy_load | local_swap | dim_control | 0.032 | 0.085 | abs_delta_spectral_radius_rel | 1 | 0.053 |
| cycle_band_p1 | add_chord | dim_control | 0.119 | 0.213 | abs_delta_spectral_radius_rel | 1 | 0.093 |
| cycle_band_p2 | add_chord | spectral_candidate | 0.072 | 0.117 | abs_delta_spectral_radius_rel | 1 | 0.046 |
| low_load_diffuse | local_swap | spectral_candidate | 0.030 | 0.044 | abs_delta_spectral_radius_rel | 1 | 0.014 |

## Role-pools

| pool | n | spectral | dim | best non-trivial | spectral rank | dim-spectral |
| --- | --- | --- | --- | --- | --- | --- |
| dim_control_pool | 8 | 0.076 | 0.149 | abs_delta_spectral_radius_rel | 1 | 0.073 |
| spectral_candidate_pool | 8 | 0.051 | 0.081 | abs_delta_spectral_radius_rel | 1 | 0.030 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsene er rent separert og alle holdout-runs matcher onsket perturbasjon.
- `add_chord_holdout_status`: `mixed` fordi `cycle_band_p2` har spectral rank 1, mens `cycle_band_p1` har 1.
- `local_swap_holdout_status`: `mixed` fordi `low_load_diffuse` har spectral rank 1, mens `buffered_heavy_load` har 1.
- `carrier_first_pool`: `pool_mixed` fordi Spectral-kandidat-poolen har dim-minus-spectral 0.030, mot 0.073 i kontroll-poolen.
- `carrier_first_reading`: `carrier_first_holdout_not_yet` fordi Holdouten bekrefter ikke en ren carrier-first spektral splittelse pa disse friske seedene.
- `next_step`: `keep_family_specific` fordi Neste steg bor holde seg innen den sterkeste familien i stedet for a presse en delt cross-family-lesning.

## Tolkning

- Dette er en liten carrier-first holdout, ikke en ny global invariant-test.
- Positivt signal her betyr at spektral lomme holder mot en naer kontrollcarrier, ikke at Lorentz-likhet eller spacetime er etablert.
