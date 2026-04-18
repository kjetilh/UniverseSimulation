# Relasjonell universgraf v0.15bq: add_chord alternative coarse geometry lab

## Formal

Denne runden tester om shell-dynamikk og shell-topologi gir en bedre liten scale-transfer-lesning for add_chord enn de enkle core/shell/rare-share-maalene.

## Startstorrelser

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |

## Aggregate profiler

| profile | role | exact | coarse | refresh | burst | shell cover | connected | fragmented | loop | attach frac |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| anchor_48_p2 | anchor | 0.901 | 0.930 | 0.066 | 0.070 | 0.658 | 0.265 | 0.735 | 0.000 | 0.912 |
| control_96_p1 | control | 0.127 | 0.889 | 0.093 | 0.000 | 0.541 | 0.000 | 1.000 | 0.000 | 0.882 |
| candidate_96_p3 | candidate | 0.196 | 0.818 | 0.097 | 0.001 | 0.524 | 0.000 | 1.000 | 0.000 | 0.858 |

## Anker-sammenlikning

| other profile | role | alt coarse distance | share distance | shell refresh | connected | fragmented | attach frac | alt rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| control_96_p1 | control | 1.242 | 0.537 | 0.093 | 0.000 | 1.000 | 0.882 | 1 |
| candidate_96_p3 | candidate | 1.342 | 0.685 | 0.097 | 0.000 | 1.000 | 0.858 | 2 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsene er rent separert og alle add_chord-runs matcher onsket perturbasjon.
- `alt_coarse_bridge`: `alt_coarse_bridge_not_yet` fordi 96/p3 er ikke naermere 48/p2 enn 96/p1 pa shell-dynamikk/topologi; alt-gapet er -0.100.
- `next_step`: `pivot_observable_or_carrier` fordi Neste steg bor ga til en ny observabel eller et annet carrier-spor, ikke presse videre pa samme add_chord-skalaovergang.

## Tolkning

- Dette er en alternativ coarse-geometri-test av samme smale add_chord-skalahypotese.
- Positivt signal her betyr bare at shell-dynamikk/topologi er en bedre coarse observabel enn share-pakken, ikke at scale-transfer er generelt lost.
