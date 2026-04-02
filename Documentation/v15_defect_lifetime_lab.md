# Relasjonell universgraf v0.15: defect lifetime lab

## Formål

Denne runden ser ikke etter Lorentz-likhet. Den tester om lokale perturbasjoner i `band_zero_del` skaper gjentagbare mesoskalafenomener som dør ut, forblir lokalisert, splitter seg eller blir vedvarende diffuse.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |
| 192 | 192.0 | 192.0 | 192.0 | 1 |
| 256 | 256.0 | 256.0 | 256.0 | 1 |

## Perturbasjonssammendrag

| perturbation | alive | mean radius | mean components | localized | split | diffuse | dies out | dominant |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord | 1.000 | 4.957 | 5.133 | 0.000 | 0.938 | 0.062 | 0.000 | persistent_split |
| local_swap | 1.000 | 5.436 | 5.850 | 0.062 | 0.688 | 0.250 | 0.000 | persistent_split |
| token_shift | 0.823 | 5.283 | 4.941 | 0.000 | 0.750 | 0.062 | 0.188 | persistent_split |

## Outcome etter størrelse

| perturbation | target | alive | radius | localized | split | diffuse | dies out |
| --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord | 48 | 1.000 | 3.150 | 0.000 | 0.750 | 0.250 | 0.000 |
| add_chord | 96 | 1.000 | 4.980 | 0.000 | 1.000 | 0.000 | 0.000 |
| add_chord | 192 | 1.000 | 6.940 | 0.000 | 1.000 | 0.000 | 0.000 |
| add_chord | 256 | 1.000 | 4.760 | 0.000 | 1.000 | 0.000 | 0.000 |
| local_swap | 48 | 1.000 | 3.610 | 0.000 | 0.250 | 0.750 | 0.000 |
| local_swap | 96 | 1.000 | 5.330 | 0.000 | 0.750 | 0.250 | 0.000 |
| local_swap | 192 | 1.000 | 5.920 | 0.250 | 0.750 | 0.000 | 0.000 |
| local_swap | 256 | 1.000 | 6.885 | 0.000 | 1.000 | 0.000 | 0.000 |
| token_shift | 48 | 0.770 | 3.600 | 0.000 | 0.750 | 0.000 | 0.250 |
| token_shift | 96 | 0.760 | 4.550 | 0.000 | 0.500 | 0.250 | 0.250 |
| token_shift | 192 | 0.760 | 5.780 | 0.000 | 0.750 | 0.000 | 0.250 |
| token_shift | 256 | 1.000 | 7.202 | 0.000 | 1.000 | 0.000 | 0.000 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er separert og alle testede perturbasjoner holder ønsket lokale type i denne runden.
- `defect_lifetime_signal`: `interesting_mesoscale_signal` fordi `add_chord` viser `persistent_split` oftere enn rent tilfeldig transientstøy (0.938).
- `next_step`: `follow_objects` fordi Neste steg bør være å følge den mest lovende utfallstypen mer direkte, for eksempel med kollisjoner eller lengre levetidsrunder.

## Heuristisk klassifisering

- `dies_out`: skaden kollapser tidlig og holder seg ikke aktiv lenge.
- `persistent_localized`: skaden holder seg i live, men forblir liten og relativt sammenhengende.
- `persistent_split`: skaden holder seg i live og viser fler-komponentmønster.
- `persistent_diffuse`: skaden holder seg i live og sprer seg bredt.
- `mixed_transient`: ingen ren type dominerer klart.

Disse klassene er heuristiske arbeidskategorier, ikke nye fysiske partikkeltyper.
