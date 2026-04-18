# v0.15br operativ anbefaling

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle local_swap-holdout-runs matcher onsket perturbasjon.
- `local_swap_mode_spectral_holdout`: `mode_plus_spectral_pocket_supported` fordi Holdouten bevarer det lokale moduskartet, og p3 holder fortsatt spectral rank 1 som low_load_diffuse-lomme.
- `next_step`: `compare_carrier_geometries` fordi Neste steg bor sammenligne coarse carrier-geometri direkte mellom add_chord og local_swap, siden local_swap-lommen holder bedre lokalt.

- Les denne runden som en smal local_swap-holdout, ikke som en ny bred modescale.
