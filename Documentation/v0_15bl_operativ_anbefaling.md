# v0.15bl operativ anbefaling

- `artifact_control`: `clean` fordi Startstorrelsene er rent separert og alle reruns matcher onsket perturbasjon.
- `zero_sanity_metrics`: `do_not_read_as_laws` fordi Globalt holder nodes/beta1 fortsatt lavest drift (0.000 / 0.250), men de skal fortsatt behandles som sanity-metrikker, ikke nye lover.
- `add_chord_conditional_signal`: `conditioning_sharpens_spectral` fordi Innen add_chord-bandet blir spektral drift skarpere i `cycle_band_p2` enn i den blandede familie-poolen (0.062 vs 0.039 dim-minus-spectral).
- `local_swap_conditional_signal`: `conditioning_sharpens_spectral` fordi Innen local_swap-moduskartet blir spektral drift skarpere i `low_load_diffuse` enn i den pooled mode-familien (0.017 vs 0.000 dim-minus-spectral).
- `cross_family_reading`: `shared_family_level_spectral_candidate` fordi Bade add_chord (`cycle_band_p2`) og local_swap (`low_load_diffuse`) har nå minst ett kondisjonert delsignal der spektral drift er beste ikke-trivielle kandidat.
- `next_step`: `carrier_first_cross_family_validation` fordi Neste steg bor teste om denne spektrale kandidaten holder under en liten carrier-first sammenlikning pa tvers av perturbasjonstyper.

- Les denne runden som en conditional quasi-invariant test pa lokale carrier-familier, ikke som en ny global lovtest.
