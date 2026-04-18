# Relasjonell universgraf v0.15br: local_swap mode spectral holdout

## Formal

Denne runden tester om local_swap sin `low_load_diffuse`-lomme holder pa friske seeds som bade modus og spectral lomme.

## Startstorrelser

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 96 | 96.0 | 96.0 | 96.0 | 1 |

## Holdout mode map

| placement | mode | exact | coarse | core | shell | rare | ball2 load | stabilizer | spectral | dim | spectral rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | buffered_heavy_load | 0.000 | 0.664 | 0.442 | 0.395 | 0.162 | 37.000 | 2.373 | 0.030 | 0.080 | 1 |
| 2 | rare_load_risk | 0.000 | 0.677 | 0.378 | 0.443 | 0.179 | 42.000 | 2.221 | 0.035 | 0.039 | 1 |
| 3 | low_load_diffuse | 0.105 | 0.656 | 0.370 | 0.382 | 0.247 | 26.000 | 2.117 | 0.029 | 0.064 | 1 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle local_swap-holdout-runs matcher onsket perturbasjon.
- `local_swap_mode_spectral_holdout`: `mode_plus_spectral_pocket_supported` fordi Holdouten bevarer det lokale moduskartet, og p3 holder fortsatt spectral rank 1 som low_load_diffuse-lomme.
- `next_step`: `compare_carrier_geometries` fordi Neste steg bor sammenligne coarse carrier-geometri direkte mellom add_chord og local_swap, siden local_swap-lommen holder bedre lokalt.

## Tolkning

- Dette er en smal holdout av local_swap-lommen, ikke en bred ny modescan.
- Positivt signal her betyr bare at local_swap er et bedre neste carrier-spor for geometri/quasi-invariant-arbeid enn add_chord akkurat na.
