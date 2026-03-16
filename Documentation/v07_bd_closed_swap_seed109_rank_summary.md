# v0.7 representativ kjøring – v07_bd_closed_swap_seed109_rank

## Hva som er nytt i v0.7

Dette steget beholder familywise uniformization fra v0.6, men bytter ut lokal rank/common-random-number coupling med eksplisitt maksimal kobling av de endelige lokale overgangskjernene.

Det betyr at når begge grener aksepterer samme event-familie, velger vi lokale overganger slik at sannsynligheten for nøyaktig samme lokale hendelse blir så stor som distribusjonene tillater.

## Parametre

- local_coupling: rank
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
| final_time | 34.04391961323962 |
| final_radius_control | 2 |
| final_radius_perturbed | 2 |
| final_edge_diff_count | 10 |
| final_delta_tokens | 15.0 |
| final_delta_nodes | 0.0 |
| avg_local_overlap_both_accept | 0.03348510101747188 |
| avg_same_descriptor_both_accept | 0.017877094972067038 |
| fit_speed_control | 0.00021223833789989213 |
| fit_speed_perturbed | -0.006036140179648195 |
| first_meeting_step | -1 |
| first_meeting_time | -1.0 |
| meeting_count | 0 |
| total_unequal_time | 34.04391961323962 |
| state_equal_final | 0 |
| shared_token_fraction_final | 0.027210884353741496 |
| shared_node_fraction_final | 1.0 |

## Familywise og lokal koblingskvalitet

| family | potential | both_accept | one_sided | null | mean_overlap | same_descriptor_rate |
| --- | --- | --- | --- | --- | --- | --- |
| seed | 0 | 0 | 0 | 0 | NA | NA |
| token | 1079 | 811 | 268 | 0 | 0.0212651 | 0.0123305 |
| birth | 100 | 74 | 26 | 0 | 0.149733 | 0.0810811 |
| death | 21 | 10 | 11 | 0 | 0.164295 | 0 |

## Frontdiagnostikk

- kontrollgren: fit speed ≈ 0.000212238
- kontrollgren: max(r/t) ≈ 5.57187

| radius | first_hit_time_control |
| --- | --- |
| 0 | 0.179473 |
| 1 | 0.179473 |
| 2 | 9.39126 |
| 3 | 9.39126 |
| 4 | NA |
| 5 | NA |
| 6 | NA |
| 7 | NA |
| 8 | NA |

## Tolkning

Hvis v0.7 virker som ønsket, skal vi se høyere lokal overlap og høyere rate av identiske lokale hendelser enn i rank-baseline, uten at vi ofrer korrekt marginal dynamikk.

Dersom meeting blir vanligere og total unequal time kortere, er det et tegn på at v0.6 faktisk undervurderte hvor mye lokal repair modellen tillater.

_Rå logg: `/mnt/data/v07_bd_closed_swap_seed109_rank_log.csv`_

_Rå eventdata: `/mnt/data/v07_bd_closed_swap_seed109_rank_events.csv`_
