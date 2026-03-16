# v0.7 faseprobe

Dette er ikke et endelig fasekart. Det er en hurtig sonde for å finne lovende regimer før v0.8.

- coupling_mode: maximal
- perturbation: local_swap
- steps per run: 500
- seeds per grid point: 6
- antall gridpunkter: 16

## Beste lokal overlap

| r_birth | r_death | p_swap | p_triad | p_del | meeting_frac | mean_overlap | same_desc | unequal_time | shared_token_frac | final_radius |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | 0 | 0.04 | 0 | 0 | 0 | 0.199 | 0.198 | 29.7 | 0.436 | 2.33 |
| 0.05 | 0 | 0.04 | 0.03 | 0 | 0 | 0.185 | 0.186 | 22.8 | 0.493 | 1.5 |
| 0.05 | 0.05 | 0.04 | 0 | 0 | 0 | 0.181 | 0.195 | 31.6 | 0.373 | 2.17 |
| 0.05 | 0.05 | 0.08 | 0.03 | 0 | 0 | 0.164 | 0.169 | 29.8 | 0.439 | 1.5 |
| 0.05 | 0.05 | 0.04 | 0.03 | 0 | 0 | 0.16 | 0.153 | 25.1 | 0.313 | 1.5 |

## Beste repair (meeting/unequal/shared token)

| r_birth | r_death | p_swap | p_triad | p_del | meeting_frac | mean_overlap | same_desc | unequal_time | shared_token_frac | final_radius |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | 0 | 0.04 | 0.03 | 0 | 0 | 0.185 | 0.186 | 22.8 | 0.493 | 1.5 |
| 0.05 | 0.05 | 0.04 | 0.03 | 0 | 0 | 0.16 | 0.153 | 25.1 | 0.313 | 1.5 |
| 0.05 | 0.05 | 0.08 | 0 | 0 | 0 | 0.133 | 0.131 | 26.3 | 0.346 | 2.33 |
| 0.05 | 0 | 0.08 | 0.03 | 0 | 0 | 0.127 | 0.131 | 27.4 | 0.424 | 1.5 |
| 0.05 | 0 | 0.04 | 0 | 0 | 0 | 0.199 | 0.198 | 29.7 | 0.436 | 2.33 |

## Mest begrenset radius (lav radius + lav unequal time)

| r_birth | r_death | p_swap | p_triad | p_del | meeting_frac | mean_overlap | same_desc | unequal_time | shared_token_frac | final_radius |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.05 | 0.04 | 0 | 0 | 0 | 0.0958 | 0.0923 | 356 | 0.667 | 4.17 |
| 0 | 0.05 | 0.08 | 0 | 0 | 0 | 0.107 | 0.102 | 319 | 0.611 | 4 |
| 0 | 0 | 0.08 | 0 | 0 | 0 | 0.0896 | 0.0897 | 128 | 1 | 3.5 |
| 0 | 0 | 0.04 | 0 | 0 | 0 | 0.144 | 0.147 | 123 | 1 | 3.17 |
| 0.05 | 0 | 0.08 | 0 | 0 | 0 | 0.141 | 0.136 | 30 | 0.406 | 2.83 |

_CSV: `/mnt/data/v07_phase_probe_repr.csv`_
