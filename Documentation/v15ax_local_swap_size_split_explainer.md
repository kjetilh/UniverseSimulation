# Relasjonell universgraf v0.15ax: local_swap size split explainer

## Formål

Denne runden bruker bare v15aw-data for å avgjøre om forskjellen mellom target 48 og 96 i local_swap-sporet er sterk nok til å behandles som ny viten.

## Target summary

| target | n | core+shell | mixed | diffuse shell | mean core share | mean shell share | mean rare share | dominant |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 48 | 8 | 1.000 | 0.000 | 0.000 | 0.692 | 0.296 | 0.012 | stable_core_variable_shell |
| 96 | 8 | 0.125 | 0.250 | 0.625 | 0.340 | 0.408 | 0.252 | diffuse_shell_recurrence |

## Placement pockets

| target | placement | n | core+shell | diffuse shell | mean core share | mean shell share | dominant |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 48 | 0 | 2 | 1.000 | 0.000 | 0.711 | 0.280 | stable_core_variable_shell |
| 48 | 1 | 2 | 1.000 | 0.000 | 0.683 | 0.287 | stable_core_variable_shell |
| 48 | 2 | 2 | 1.000 | 0.000 | 0.712 | 0.278 | stable_core_variable_shell |
| 48 | 3 | 2 | 1.000 | 0.000 | 0.661 | 0.339 | stable_core_variable_shell |
| 96 | 0 | 2 | 0.000 | 0.500 | 0.434 | 0.388 | mixed_core_shell |
| 96 | 1 | 2 | 0.000 | 0.500 | 0.372 | 0.416 | mixed_core_shell |
| 96 | 2 | 2 | 0.000 | 1.000 | 0.161 | 0.461 | diffuse_shell_recurrence |
| 96 | 3 | 2 | 0.500 | 0.500 | 0.393 | 0.366 | stable_core_variable_shell |

## Operativ lesning

- `size_split_status`: `local_swap_size_split_supported` fordi 48-nivået holder rent som stable core+shell, mens 96-nivået går over i en mer diffus shell-regime med klart lavere kjerneandel og høyere randandel.
- `96_pocket_status`: `small_core_shell_pockets_present` fordi Det finnes 1 små 96-lommer som fortsatt holder stable core+shell lokalt.
- `next_step`: `explain_diffuse_96_pockets` fordi Neste steg bør forklare hvorfor noen få 96-run fortsatt nærmer seg core+shell, i stedet for å scanne bredere.

## Tolkning

- Dette er en ren forklaringsrunde på toppen av v15aw, ikke en ny simulering.
- Les dette som en strukturert size-splitt i local_swap-observabelen, ikke som en stor asymptotisk lov.
