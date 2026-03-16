# v0.7 – representativ enkeltsammenligning for seed 109

## Oppsett
Regime:
- `r_seed = 0.04`
- `r_token = 1.0`
- `r_birth = 0.05`
- `r_death = 0.05`
- `p_swap = 0.08`
- `p_triad = 0.0`
- `p_del = 0.0`
- perturbasjon: `local_swap`

Vi sammenligner samme seed under to lokale koblinger:
- `rank`
- `maximal`

## Rank
- avg_local_overlap_both_accept = 0.0335
- avg_same_descriptor_both_accept = 0.0179
- shared_token_fraction_final = 0.0272
- final_edge_diff_count = 10
- total_unequal_time = 34.044

## Maximal
- avg_local_overlap_both_accept = 0.1268
- avg_same_descriptor_both_accept = 0.1302
- shared_token_fraction_final = 0.4126
- final_edge_diff_count = 16
- total_unequal_time = 33.106

## Tolkning
Dette er et godt eksempel på hvorfor v0.7 er verdifull selv uten full meeting.

Maksimal lokal kobling:
- firedobler omtrent lokal overlap,
- gjør identiske lokale hendelser mye vanligere,
- og bevarer langt mer felles token-lineage.

Det betyr at modellen i dette tilfellet er mye mindre “lokalt irreversibel” enn rank-baseline fikk den til å se ut.