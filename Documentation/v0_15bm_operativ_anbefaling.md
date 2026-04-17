# v0.15bm operativ anbefaling

- `artifact_control`: `clean` fordi Startstorrelsene er rent separert og alle holdout-runs matcher onsket perturbasjon.
- `add_chord_holdout_status`: `mixed` fordi `cycle_band_p2` har spectral rank 1, mens `cycle_band_p1` har 1.
- `local_swap_holdout_status`: `mixed` fordi `low_load_diffuse` har spectral rank 1, mens `buffered_heavy_load` har 1.
- `carrier_first_pool`: `pool_mixed` fordi Spectral-kandidat-poolen har dim-minus-spectral 0.030, mot 0.073 i kontroll-poolen.
- `carrier_first_reading`: `carrier_first_holdout_not_yet` fordi Holdouten bekrefter ikke en ren carrier-first spektral splittelse pa disse friske seedene.
- `next_step`: `keep_family_specific` fordi Neste steg bor holde seg innen den sterkeste familien i stedet for a presse en delt cross-family-lesning.

- Les denne runden som en liten carrier-first holdout, ikke som en ny global invariant-lovtest.
