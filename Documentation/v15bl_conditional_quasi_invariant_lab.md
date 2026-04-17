# Relasjonell universgraf v0.15bl: conditional quasi-invariant lab

## Formal

Denne runden gar tilbake til quasi-invariant-sporet, men condition-er pa de lokale mesoskopiske familiene som faktisk har overlevd i defect-sporet, i stedet for a blande alle run sammen.

## Startstorrelser

| target | mean initial | q10 | q90 | separated | mean dim proxy |
| --- | --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 | 2.381 |
| 96 | 96.0 | 96.0 | 96.0 | 1 | 2.593 |

## Familie-pools

| family pool | n | spectral | dim | clustering | triangles | best non-trivial | spectral rank | dim-spectral | spectral<dim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_cycle_core_shell_band_pool | 18 | 0.100 | 0.139 | 0.540 | 0.667 | abs_delta_spectral_radius_rel | 1 | 0.039 | 0.611 |
| local_swap_growth202_mode_map_pool | 18 | 0.050 | 0.050 | 0.133 | 0.126 | abs_delta_spectral_radius_rel | 1 | 0.000 | 0.556 |

## Kondisjonerte delsignaler

| condition | family | n | exact return | coarse return | spectral | dim | best non-trivial | spectral rank | dim-spectral |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cycle_band_p0 | add_chord_cycle_core_shell_band | 6 | 0.859 | 0.934 | 0.075 | 0.134 | abs_delta_spectral_radius_rel | 1 | 0.059 |
| cycle_band_p1 | add_chord_cycle_core_shell_band | 6 | 0.846 | 0.946 | 0.150 | 0.146 | abs_delta_dim_proxy_rel | 2 | -0.004 |
| cycle_band_p2 | add_chord_cycle_core_shell_band | 6 | 0.752 | 0.944 | 0.075 | 0.137 | abs_delta_spectral_radius_rel | 1 | 0.062 |
| buffered_heavy_load | local_swap_growth202_mode_map | 6 | 0.000 | 0.697 | 0.054 | 0.032 | abs_delta_dim_proxy_rel | 2 | -0.022 |
| low_load_diffuse | local_swap_growth202_mode_map | 6 | 0.000 | 0.646 | 0.053 | 0.070 | abs_delta_spectral_radius_rel | 1 | 0.017 |
| rare_load_risk | local_swap_growth202_mode_map | 6 | 0.000 | 0.672 | 0.042 | 0.049 | abs_delta_spectral_radius_rel | 1 | 0.007 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsene er rent separert og alle reruns matcher onsket perturbasjon.
- `zero_sanity_metrics`: `do_not_read_as_laws` fordi Globalt holder nodes/beta1 fortsatt lavest drift (0.000 / 0.250), men de skal fortsatt behandles som sanity-metrikker, ikke nye lover.
- `add_chord_conditional_signal`: `conditioning_sharpens_spectral` fordi Innen add_chord-bandet blir spektral drift skarpere i `cycle_band_p2` enn i den blandede familie-poolen (0.062 vs 0.039 dim-minus-spectral).
- `local_swap_conditional_signal`: `conditioning_sharpens_spectral` fordi Innen local_swap-moduskartet blir spektral drift skarpere i `low_load_diffuse` enn i den pooled mode-familien (0.017 vs 0.000 dim-minus-spectral).
- `cross_family_reading`: `shared_family_level_spectral_candidate` fordi Bade add_chord (`cycle_band_p2`) og local_swap (`low_load_diffuse`) har nå minst ett kondisjonert delsignal der spektral drift er beste ikke-trivielle kandidat.
- `next_step`: `carrier_first_cross_family_validation` fordi Neste steg bor teste om denne spektrale kandidaten holder under en liten carrier-first sammenlikning pa tvers av perturbasjonstyper.

## Tolkning

- Dette er fortsatt en liten conditional lab, ikke en ny global invariant-scan.
- `nodes` og `beta1` rapporteres fortsatt bare som sanity-metrikker; de skal ikke oppgraderes til lover av denne runden.
- Et positivt signal her bor leses som familiespesifikk eller carrier-spesifikk sharpening, ikke som universell spacetime- eller Lorentz-likhet.
