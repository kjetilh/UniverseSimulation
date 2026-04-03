# Relasjonell universgraf v0.15d: collision window lab

## Formål

Denne runden går smalere enn v0.15c og ser på selve interaksjonsvinduet der pair-runen avviker mest fra unionen av matched single-runs.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |

## Window classes

| class | n | min union j | final union j | window comp delta | final comp delta | window largest delta | final largest delta | min index frac |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| compress_then_split | 1 | 0.194 | 0.550 | -6.000 | 4.000 | 0.317 | -0.593 | 0.390 |
| mixed_window | 6 | 0.199 | 0.451 | -0.333 | 1.167 | -0.031 | -0.108 | 0.253 |
| persistent_binding_tendency | 1 | 0.161 | 0.405 | -5.000 | -4.000 | 0.528 | 0.198 | 0.610 |

## Run-level window diagnostics

| target | pair | dist | min union j | min step | min idx frac | window comp delta | final comp delta | window largest delta | final largest delta | class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 48 | 2-3 | 4 | 0.226 | 116 | 0.276 | -2.000 | -1.000 | -0.117 | 0.214 | mixed_window |
| 48 | 2-3 | 4 | 0.194 | 164 | 0.390 | -6.000 | 4.000 | 0.317 | -0.593 | compress_then_split |
| 48 | 3-4 | 3 | 0.161 | 256 | 0.610 | -5.000 | -4.000 | 0.528 | 0.198 | persistent_binding_tendency |
| 48 | 3-4 | 3 | 0.235 | 136 | 0.324 | 1.000 | 4.000 | -0.365 | -0.522 | mixed_window |
| 96 | 0-5 | 5 | 0.208 | 120 | 0.156 | 3.000 | 0.000 | 0.079 | -0.011 | mixed_window |
| 96 | 0-5 | 5 | 0.132 | 200 | 0.260 | 2.000 | 5.000 | -0.098 | -0.190 | mixed_window |
| 96 | 1-5 | 6 | 0.185 | 160 | 0.208 | 0.000 | 2.000 | 0.077 | -0.237 | mixed_window |
| 96 | 1-5 | 6 | 0.211 | 224 | 0.292 | -6.000 | -3.000 | 0.238 | 0.096 | mixed_window |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er separert og matched AB/BA-control holder seg samkjørt også i den tettere møtesporingen.
- `collision_window_signal`: `mixed_window_family` fordi Møtevinduet er fortsatt blandet (`persistent_fragmentation_tendency` 0.000, `persistent_binding_tendency` 0.125, `compress_then_split` 0.125, `mixed_window` 0.750).
- `next_step`: `narrow_pair_selection` fordi Neste steg bør være enda smalere pair-selection eller flere snapshots rundt møtet i én liten størrelseskorridor.

## Heuristiske møtevindusklasser

- `persistent_binding_tendency`: pair-run ligger under unionen i komponenttall både i møtevinduet og ved slutten.
- `persistent_fragmentation_tendency`: pair-run ligger over unionen i komponenttall både i møtevinduet og ved slutten.
- `compress_then_split`: pair-run komprimerer ved møtet, men ender senere mer fragmentert.
- `split_then_bind`: pair-run splitter først, men ender senere mer samlet.
- `mixed_window`: interaksjonsvinduet er reelt, men ikke skarpt nok til én type.
