# Relasjonell universgraf v0.15bn: add_chord scale-jump family map

## Formal

Denne runden tester om den sterkeste add_chord-lommen fra 48/p2 har en liten gjenkjennelig motpart ved target 96 pa samme coarse-geometri- og spectral-akse.

## Startstorrelser

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |

## Aggregate per target/placement

| target | placement | exact | coarse | core | shell | rare | spectral | dim | best non-trivial | spectral rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 48 | 0 | 0.859 | 0.934 | 0.879 | 0.108 | 0.013 | 0.075 | 0.134 | abs_delta_spectral_radius_rel | 1 |
| 48 | 1 | 0.846 | 0.946 | 0.892 | 0.108 | 0.000 | 0.150 | 0.146 | abs_delta_dim_proxy_rel | 2 |
| 48 | 2 | 0.752 | 0.944 | 0.855 | 0.145 | 0.000 | 0.075 | 0.137 | abs_delta_spectral_radius_rel | 1 |
| 48 | 3 | 0.836 | 0.937 | 0.890 | 0.104 | 0.006 | 0.088 | 0.099 | abs_delta_spectral_radius_rel | 1 |
| 96 | 0 | 0.027 | 0.773 | 0.414 | 0.440 | 0.146 | 0.042 | 0.059 | abs_delta_spectral_radius_rel | 1 |
| 96 | 1 | 0.093 | 0.871 | 0.610 | 0.337 | 0.053 | 0.068 | 0.056 | abs_delta_dim_proxy_rel | 2 |
| 96 | 2 | 0.111 | 0.848 | 0.576 | 0.342 | 0.082 | 0.056 | 0.032 | abs_delta_dim_proxy_rel | 2 |
| 96 | 3 | 0.125 | 0.797 | 0.601 | 0.349 | 0.050 | 0.019 | 0.081 | abs_delta_spectral_radius_rel | 1 |

## 48/p2 mot 96-kandidater

| 96 placement | combined distance | coarse distance | spectral gap | best metric | spectral rank | match rank |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 1.285 | 1.285 | 0.000 | abs_delta_spectral_radius_rel | 1 | 1 |
| 1 | 1.304 | 1.230 | 0.074 | abs_delta_dim_proxy_rel | 2 | 2 |
| 2 | 1.399 | 1.312 | 0.087 | abs_delta_dim_proxy_rel | 2 | 3 |
| 0 | 1.842 | 1.798 | 0.045 | abs_delta_spectral_radius_rel | 1 | 4 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsene er rent separert og alle add_chord-runs matcher onsket perturbasjon.
- `anchor_profile`: `cycle_band_p2` fordi Ankeret er target 48, placement 2, siden det var den sterkeste spektrale lommen i v15bl innen add_chord-bandet.
- `scale_jump_match`: `small_scale_jump_match_weak` fordi Beste 96-match er p3, men combined distance-gapet til neste kandidat er bare 0.019.
- `next_step`: `holdout_with_one_control` fordi Neste steg bor teste ankerparet mot en enkel 96-kontroll for a se om dette er ekte eller bare svak lokal konkurranse.

## Tolkning

- Dette er en liten add_chord-skalaovergang, ikke en bred ny scan.
- Positivt signal her betyr bare at vi har en kandidat til samme familie over ett lite skalahopp.
