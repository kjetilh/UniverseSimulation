# Relasjonell universgraf v0.15ai: early-lock band lab

## Formal

Denne runden tester en ny observabel inne i den robuste `early_fragment_lock`-familien: om hale-fragmenteringen er bedre beskrevet av coarse `low/mid/high` fragment-load-band enn av ett eksakt shell-komponenttall.

## Oppsett

- behold samme lokale `t48_g202` add_chord-band
- behold bare run som faktisk ligger i hovedfamilien `early_fragment_lock`
- bruk ankerrun fra `v15ae-v15af` og holdout-run fra `v15ah` som falt tilbake til hovedfamilien
- bruk coarse band `low = 1..3`, `mid = 4..6`, `high = 7+`

## Startstorrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Kildegrupper

| group | n | structured | band lock | low | mid | high | band drift | band share | exact share | uplift |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| anchor_main_family | 12 | 1.000 | 0.833 | 0.250 | 0.500 | 0.083 | 0.000 | 0.673 | 0.347 | 0.326 |
| holdout_revert | 10 | 0.900 | 0.600 | 0.300 | 0.200 | 0.100 | 0.100 | 0.704 | 0.387 | 0.317 |
| combined | 22 | 0.955 | 0.727 | 0.273 | 0.364 | 0.091 | 0.045 | 0.687 | 0.365 | 0.322 |

## Per placement

| placement | n | mode | low | mid | high | band share | exact share | band drift |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 7 | mid | 0.286 | 0.571 | 0.000 | 0.668 | 0.379 | 0.000 |
| 1 | 7 | mid | 0.286 | 0.429 | 0.000 | 0.681 | 0.372 | 0.000 |
| 2 | 8 | high | 0.250 | 0.125 | 0.250 | 0.709 | 0.347 | 0.125 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er rent separert og alle run i denne runden matcher onsket add_chord-perturbasjon.
- `coarse_band_status`: `early_lock_has_structured_band_ladder` fordi Hovedfamilien er mye bedre lest som coarse low/mid/high-band med litt naboband-drift enn som ett eksakt shell-komponenttall, og dette holder ogsa pa holdout-run som falt tilbake til hovedfamilien.
- `band_mode_note`: `descriptive` fordi Ankerrun domineres mest av `mid`, mens holdout-revert-rundene domineres mest av `low`.
- `next_step`: `probe_band_onset_and_switching` fordi Neste steg bor forklare nar run larser seg inn i low, mid eller high band, og hvilke run som bare driver mellom to naboband.

## Tolkning

- Dette er fortsatt ikke en ny defect-art eller en lov; det er en smal observabeltest inne i den robuste hovedfamilien.
- Hvis coarse band slar eksakt telling, betyr det at hovedfamilien er bedre lest som fragment-load-band enn som ett skarpt shell-komponenttall.
- Hvis coarse band fortsatt er diffust, betyr det at neste steg bor bytte observabel igjen, ikke presse samme aksen hardere.
