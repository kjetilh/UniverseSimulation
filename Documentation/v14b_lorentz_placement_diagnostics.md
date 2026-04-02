# Relasjonell universgraf v0.14b: placement-aware Lorentz-diagnostikk

## Formål

Denne runden tester om forskjellen mellom `local_swap` og `add_chord` i v0.14 hovedsakelig var en ekte modusforskjell, eller om samme type inngrep varierer nesten like mye bare fordi vi treffer ulike lokale plasseringer.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |
| 192 | 192.0 | 192.0 | 192.0 | 1 |
| 256 | 256.0 | 256.0 | 256.0 | 1 |

## Placement-sammendrag

| regime | perturbation | placement | strict_match | unique_supports | mean fit_speed | mean hit t(r=2) |
| --- | --- | --- | --- | --- | --- | --- |
| band_pdel_0005 | add_chord | 0 | 1.000 | 7 | 0.225 | 11.546 |
| band_pdel_0005 | add_chord | 1 | 1.000 | 7 | 0.226 | 12.986 |
| band_pdel_0005 | add_chord | 2 | 1.000 | 8 | 0.240 | 13.555 |
| band_pdel_0005 | add_chord | 3 | 1.000 | 8 | 0.228 | 14.560 |
| band_pdel_0005 | local_swap | 0 | 1.000 | 7 | 0.252 | 11.074 |
| band_pdel_0005 | local_swap | 1 | 1.000 | 7 | 0.263 | 10.257 |
| band_pdel_0005 | local_swap | 2 | 1.000 | 8 | 0.285 | 10.406 |
| band_pdel_0005 | local_swap | 3 | 1.000 | 8 | 0.273 | 11.314 |
| band_zero_del | add_chord | 0 | 1.000 | 7 | 0.207 | 13.649 |
| band_zero_del | add_chord | 1 | 1.000 | 7 | 0.260 | 13.335 |
| band_zero_del | add_chord | 2 | 1.000 | 8 | 0.209 | 14.105 |
| band_zero_del | add_chord | 3 | 1.000 | 8 | 0.201 | 12.263 |
| band_zero_del | local_swap | 0 | 1.000 | 7 | 0.250 | 9.332 |
| band_zero_del | local_swap | 1 | 1.000 | 7 | 0.232 | 10.694 |
| band_zero_del | local_swap | 2 | 1.000 | 8 | 0.252 | 8.966 |
| band_zero_del | local_swap | 3 | 1.000 | 8 | 0.234 | 10.619 |

## Variasjon innen samme modus over plasseringer

| regime | perturbation | rel speed gap | rel hit gap r2 | same support rate |
| --- | --- | --- | --- | --- |
| band_pdel_0005 | add_chord | 0.626 | 0.330 | 0.000 |
| band_pdel_0005 | local_swap | 0.427 | 0.419 | 0.000 |
| band_zero_del | add_chord | 0.796 | 0.347 | 0.000 |
| band_zero_del | local_swap | 0.501 | 0.364 | 0.000 |

## Variasjon mellom modus ved samme plassering

| regime | rel speed gap | rel hit gap r2 | support gap |
| --- | --- | --- | --- |
| band_pdel_0005 | 0.510 | 0.364 | 0.0 |
| band_zero_del | 0.658 | 0.313 | 0.0 |

## Diagnose: modus vs plassering

| regime | within rel speed | mode rel speed | speed ratio | diagnosis |
| --- | --- | --- | --- | --- |
| band_pdel_0005 | 0.526 | 0.510 | 0.969 | placement_noise_competes |
| band_zero_del | 0.648 | 0.658 | 1.014 | placement_noise_competes |

## Operativ lesning

- `generator_and_placement_artifacts`: `clean` fordi Startstørrelsene er separert og alle placement-rader bruker ønsket perturbasjonstype.
- `mode_vs_placement`: `anisotropy_not_ruled_out` fordi Plasseringsover variasjon i ankerregimet er naer nok mellom-modus-gapet til at Lorentz-sporet fortsatt er uklart.
- `next_step`: `keep_narrow_same_family` fordi Neste steg bor fortsatt vaere smalt i samme familie; ikke oppskaler til stort valideringssett ennå.

## Tolkning

- Hvis mellom-modus-gapet er storre enn typisk within-modus-gap, styrker det at v14 faktisk sa en reell modusavhengighet.
- Hvis within-modus-gapet er nesten like stort, er lokal anisotropi fortsatt en sterk alternativ forklaring.
- Ingen av delene er i seg selv Lorentz-likhet; dette er fortsatt bare en smal diagnostikk.
