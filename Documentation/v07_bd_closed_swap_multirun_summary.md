# v0.7 multirun-sammenligning – v07_bd_closed_swap

## Formål

Sammenligne rank-baseline og lokal maksimal kobling over samme seeder og samme parameterregime.

## Aggregerte resultater

| mode | runs | meeting_fraction | mean_first_meeting_time|met | mean_final_radius | mean_unequal_time | mean_local_overlap | mean_same_descriptor_rate | mean_shared_token_frac_final | mean_shared_node_frac_final |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rank | 12 | 0 | NA | 2.91667 | 41.4679 | 0.0504299 | 0.0326923 | 0.0641548 | 0.798737 |
| maximal | 12 | 0 | NA | 2.33333 | 39.3436 | 0.0819646 | 0.0792709 | 0.215917 | 0.8136 |

## Survival/meeting

### Overlevelseskurve – rank

| time | P(not met by t) |
| --- | --- |
| 0 | 1 |
| 5.00775 | 1 |
| 12.5194 | 1 |
| 25.0388 | 1 |
| 37.5581 | 1 |
| 50.0775 | 1 |

### Overlevelseskurve – maximal

| time | P(not met by t) |
| --- | --- |
| 0 | 1 |
| 5.00775 | 1 |
| 12.5194 | 1 |
| 25.0388 | 1 |
| 37.5581 | 1 |
| 50.0775 | 1 |

## Tolkning

For v0.7 er nøkkelspørsmålet ikke bare om divergence sprer seg, men også om bedre lokal kobling øker sannsynligheten for repair og tidligere meeting.

_Per-seed CSV: `/mnt/data/v07_bd_closed_swap_multirun.csv`_
