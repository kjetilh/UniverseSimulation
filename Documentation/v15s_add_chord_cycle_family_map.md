# Relasjonell universgraf v0.15s: add_chord cycle-family map

## Formål

Denne runden kartlegger bare den lokale `add_chord`-familien rundt den ene profilen som holdt ekte `cyclic_return` i `v15r`.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Local family map

| placement | support | prefix | full | transition | prefix exact | full exact | full coarse |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 5,6,8 | morphology_return | cyclic_return | morphology_tips_to_cycle | 0.031 | 0.977 | 0.884 |
| 1 | 6,8,10 | morphology_return | cyclic_return | morphology_tips_to_cycle | 0.154 | 1.000 | 0.961 |
| 2 | 5,6,14 | cyclic_return | cyclic_return | sustained_cyclic_return | 0.723 | 0.969 | 0.961 |
| 3 | 5,6,19 | morphology_return | cyclic_return | morphology_tips_to_cycle | 0.031 | 0.659 | 0.953 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert og alle lokale add_chord-profiler matcher ønsket perturbasjonstype.
- `cycle_family_status`: `local_cycle_band` fordi Det overlevende cycle-signalet sprer seg til minst én umiddelbar naboprofil på samme base.
- `strongest_profile`: `p1` fordi Sterkeste full-horisontprofil er plassering 1 med full_exact_return_rate=1.000.
- `next_step`: `probe_cycle_band` fordi Neste steg bør være en enda smalere kartlegging bare rundt det lokale cycle-båndet.

## Tolkning

- Dette er en ren local family-map på samme base, ikke en ny sweep.
- Les dette som recurrence i ett smalt add_chord-område, ikke som generell cycle-lov.
