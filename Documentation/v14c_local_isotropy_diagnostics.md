# Relasjonell universgraf v0.14c: lokal isotropi-diagnostikk

## Formål

Denne runden fryser ett regime og én perturbasjonstype (`band_zero_del` + `local_swap`) og tester om lokal støttegeometri kan forklare plasseringsover variasjon i frontmålingene.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |
| 192 | 192.0 | 192.0 | 192.0 | 1 |
| 256 | 256.0 | 256.0 | 256.0 | 1 |

## Placement-sammendrag

| placement | strict_match | unique_supports | mean fit_speed | mean hit t(r=2) | mean ball2 | mean degree |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1.000 | 11 | 0.232 | 9.010 | 28.6 | 4.944 |
| 1 | 1.000 | 10 | 0.224 | 10.471 | 34.8 | 6.000 |
| 2 | 1.000 | 12 | 0.241 | 8.583 | 25.4 | 5.111 |
| 3 | 1.000 | 11 | 0.260 | 10.220 | 27.6 | 4.917 |
| 4 | 1.000 | 11 | 0.234 | 11.003 | 27.8 | 5.111 |
| 5 | 1.000 | 12 | 0.215 | 9.776 | 30.2 | 5.583 |

## Geometrisignal

| feature | spearman vs speed | spearman vs -hit(r2) | q10 | q90 |
| --- | --- | --- | --- | --- |
| support_ball_2 | -0.064 | -0.296 | 15.000 | 43.000 |
| support_ball_3 | -0.098 | -0.324 | 24.000 | 74.000 |
| support_shell_2 | -0.091 | -0.283 | 7.000 | 26.000 |
| mean_support_degree | 0.029 | -0.257 | 3.000 | 7.000 |

## Within-base alignment

| feature | align speed | align hit | mean feature gap | mean speed gap | mean hit gap |
| --- | --- | --- | --- | --- | --- |
| support_ball_2 | 0.083 | 0.167 | 22.083 | 0.226 | 8.491 |
| support_ball_3 | 0.042 | 0.167 | 31.333 | 0.226 | 8.491 |
| support_shell_2 | 0.083 | 0.167 | 14.250 | 0.226 | 8.491 |
| mean_support_degree | 0.083 | 0.125 | 3.139 | 0.226 | 8.491 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er separert og alle local_swap-placement-rader bruker ønsket perturbasjon.
- `local_isotropy_probe`: `weak` fordi Ingen av de testede støttegeometriene, inkludert `support_ball_3`, forklarer hastighetsvariasjonen særlig godt.
- `next_step`: `pause_lorentz_expansion` fordi Ikke utvid Lorentz-sporet bredt ennå; bruk heller dette til å vurdere om videre isotropitesting er verdt kostnaden.

## Tolkning

- Hvis støttegeometri predikerer hvilken plassering som får raskest spredning, styrker det at lokal anisotropi / mikroframe er en reell forklaring.
- Hvis signalet er svakt selv her, er placement-støy fortsatt der, men ikke godt forklart av disse enkle lokale geometrifeaturene.
- Ingen av delene gir Lorentz-likhet; dette er bare en diagnose av lokal retning-/støttefølsomhet.
