# Relasjonell universgraf v0.15c: collision type lab

## Formål

Denne runden følger opp v0.15b og prøver å klassifisere hvilken type interaksjon de parvise `add_chord`-defectene faktisk ser ut til å ha.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |
| 192 | 192.0 | 192.0 | 192.0 | 1 |
| 256 | 256.0 | 256.0 | 256.0 | 1 |

## Collision classes

| class | n | mean union jaccard | final union jaccard | order jaccard | control consistency | pair damage | union damage | pair comps | union comps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| binding_like | 3 | 0.403 | 0.409 | 1.000 | 1.000 | 0.573 | 0.585 | 2.667 | 8.000 |
| mixed_collision | 9 | 0.357 | 0.410 | 1.000 | 1.000 | 0.470 | 0.531 | 11.556 | 12.000 |
| secondary_split_like | 4 | 0.406 | 0.472 | 1.000 | 1.000 | 0.456 | 0.677 | 7.500 | 3.750 |

## Run-level diagnostics

| target | pair | dist | mean union j | final union j | final order j | control | pair dmg | union dmg | pair comps | union comps | class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 48 | 2-3 | 4 | 0.426 | 0.366 | 1.000 | 1.000 | 0.583 | 0.583 | 3.000 | 4.000 | binding_like |
| 48 | 2-3 | 4 | 0.462 | 0.550 | 1.000 | 1.000 | 0.562 | 0.729 | 5.000 | 1.000 | secondary_split_like |
| 48 | 3-4 | 3 | 0.435 | 0.405 | 1.000 | 1.000 | 0.604 | 0.625 | 2.000 | 6.000 | binding_like |
| 48 | 3-4 | 3 | 0.398 | 0.371 | 1.000 | 1.000 | 0.375 | 0.625 | 6.000 | 2.000 | secondary_split_like |
| 96 | 0-5 | 5 | 0.455 | 0.538 | 1.000 | 1.000 | 0.573 | 0.677 | 5.000 | 5.000 | mixed_collision |
| 96 | 0-5 | 5 | 0.357 | 0.485 | 1.000 | 1.000 | 0.438 | 0.583 | 10.000 | 5.000 | secondary_split_like |
| 96 | 1-5 | 6 | 0.410 | 0.481 | 1.000 | 1.000 | 0.448 | 0.771 | 9.000 | 7.000 | secondary_split_like |
| 96 | 1-5 | 6 | 0.416 | 0.465 | 1.000 | 1.000 | 0.510 | 0.573 | 7.000 | 10.000 | mixed_collision |
| 192 | 3-4 | 7 | 0.323 | 0.469 | 1.000 | 1.000 | 0.526 | 0.568 | 10.000 | 12.000 | mixed_collision |
| 192 | 3-4 | 7 | 0.208 | 0.145 | 1.000 | 1.000 | 0.396 | 0.099 | 13.000 | 10.000 | mixed_collision |
| 192 | 1-2 | 7 | 0.357 | 0.474 | 1.000 | 1.000 | 0.500 | 0.667 | 12.000 | 7.000 | mixed_collision |
| 192 | 1-2 | 7 | 0.350 | 0.458 | 1.000 | 1.000 | 0.531 | 0.547 | 3.000 | 14.000 | binding_like |
| 256 | 1-5 | 7 | 0.385 | 0.492 | 1.000 | 1.000 | 0.504 | 0.656 | 15.000 | 11.000 | mixed_collision |
| 256 | 1-5 | 7 | 0.420 | 0.521 | 1.000 | 1.000 | 0.551 | 0.602 | 16.000 | 11.000 | mixed_collision |
| 256 | 0-2 | 6 | 0.360 | 0.282 | 1.000 | 1.000 | 0.375 | 0.406 | 14.000 | 23.000 | mixed_collision |
| 256 | 0-2 | 6 | 0.288 | 0.302 | 1.000 | 1.000 | 0.297 | 0.527 | 12.000 | 19.000 | mixed_collision |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er separert og matched control-grenene holder seg samkjørte på tvers av single/pair/AB/BA.
- `collision_type_signal`: `mixed_collision_family` fordi Kollisjonsklassene splitter seg fortsatt (`secondary_split_like` 0.250, `binding_like` 0.188, `annihilation_like` 0.000, `pass_through_like` 0.000).
- `next_step`: `tighten_interaction_type` fordi Neste steg bør være en enda smalere interaksjonstest med flere snapshots og eksplisitt komponentsporing rundt møtet.

## Heuristiske klasser

- `near_superposition`: pair-run ser nesten ut som unionen av single-runs også ved slutten.
- `annihilation_like`: pair-run ender betydelig svakere enn unionen av single-runs.
- `binding_like`: pair-run ender i færre og mer konsentrerte komponenter enn unionen.
- `secondary_split_like`: pair-run ender i flere og mer fragmenterte komponenter enn unionen.
- `pass_through_like`: pair-run avviker underveis, men ender nær separert sluttgeometri.
- `mixed_collision`: det er et kollisjonssignal, men ikke en ren type ennå.

Disse etikettene er diagnostiske arbeidsnavn, ikke bevis på fysiske partikkelklasser.
