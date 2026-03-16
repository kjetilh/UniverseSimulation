# v0.7 representativ kjøring – v07_bd_closed_swap_seed109_max

## Hva som er nytt i v0.7

Dette steget beholder familywise uniformization fra v0.6, men bytter ut lokal rank/common-random-number coupling med eksplisitt maksimal kobling av de endelige lokale overgangskjernene.

Det betyr at når begge grener aksepterer samme event-familie, velger vi lokale overganger slik at sannsynligheten for nøyaktig samme lokale hendelse blir så stor som distribusjonene tillater.

## Parametre

- local_coupling: maximal
- steps: 1200
- seed: 109
- perturbation: local_swap
- r_seed: 0.04
- r_token: 1.0
- r_birth: 0.05
- r_death: 0.05
- p_triad: 0.0
- p_del: 0.0
- p_swap: 0.08

## Startperturbasjon

```json
{
  "delta_core": {
    "beta1": 0,
    "components": 0,
    "nodes": 0,
    "tokens": 0
  },
  "support": [
    2,
    3,
    4
  ],
  "type": "local_swap"
}
```

## Hovedmål

| metric | value |
| --- | --- |
| final_time | 33.10633863783979 |
| final_radius_control | 2 |
| final_radius_perturbed | 2 |
| final_edge_diff_count | 16 |
| final_delta_tokens | 14.0 |
| final_delta_nodes | 0.0 |
| avg_local_overlap_both_accept | 0.1268120478309263 |
| avg_same_descriptor_both_accept | 0.1301989150090416 |
| fit_speed_control | 0.02991161850443719 |
| fit_speed_perturbed | 0.051308318760753174 |
| first_meeting_step | -1 |
| first_meeting_time | -1.0 |
| meeting_count | 0 |
| total_unequal_time | 33.10633863783979 |
| state_equal_final | 0 |
| shared_token_fraction_final | 0.4125874125874126 |
| shared_node_fraction_final | 1.0 |

## Familywise og lokal koblingskvalitet

| family | potential | both_accept | one_sided | null | mean_overlap | same_descriptor_rate |
| --- | --- | --- | --- | --- | --- | --- |
| seed | 1 | 1 | 0 | 0 | 1 | 1 |
| token | 1063 | 985 | 78 | 0 | 0.0677016 | 0.0670051 |
| birth | 120 | 105 | 15 | 0 | 0.607228 | 0.638095 |
| death | 16 | 15 | 1 | 0 | 0.587274 | 0.666667 |

## Frontdiagnostikk

- kontrollgren: fit speed ≈ 0.0299116
- kontrollgren: max(r/t) ≈ 0.24137

| radius | first_hit_time_control |
| --- | --- |
| 0 | 0.179473 |
| 1 | 12.429 |
| 2 | 12.429 |
| 3 | 12.429 |
| 4 | NA |
| 5 | NA |
| 6 | NA |
| 7 | NA |
| 8 | NA |

## Tolkning

Hvis v0.7 virker som ønsket, skal vi se høyere lokal overlap og høyere rate av identiske lokale hendelser enn i rank-baseline, uten at vi ofrer korrekt marginal dynamikk.

Dersom meeting blir vanligere og total unequal time kortere, er det et tegn på at v0.6 faktisk undervurderte hvor mye lokal repair modellen tillater.

_Rå logg: `/mnt/data/v07_bd_closed_swap_seed109_max_log.csv`_

_Rå eventdata: `/mnt/data/v07_bd_closed_swap_seed109_max_events.csv`_
