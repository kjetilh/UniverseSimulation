# Relasjonell universgraf v0.15be: local_swap trigger-axis component lab

## Formål

Denne runden åpner `retention_core_axis = coarse_return + core_to_shell` fra `v15bd` for å se hvilke komponenter som faktisk driver `p1 > p3 > p2`.

## Pair decomposition

| pair | axis gap | coarse gap | core/shell gap | tail density gap | coarse share | core share | family |
| --- | --- | --- | --- | --- | --- | --- | --- |
| p1_vs_p3 | 0.608 | 0.215 | 0.393 | 0.078 | 0.354 | 0.646 | core_amplification_dominant |
| p3_vs_p2 | 0.390 | 0.185 | 0.206 | 0.104 | 0.473 | 0.527 | balanced_two_component_gap |
| p1_vs_p2 | 0.999 | 0.400 | 0.599 | 0.182 | 0.401 | 0.599 | balanced_two_component_gap |

## Operativ lesning

- `axis_component_status`: `two_component_axis_supported` fordi Aksen ser ikke monolittisk ut: p1 > p3 drives mest av core/shell, mens p3 > p2 drives av en mer balansert blanding av return og core/shell.
- `component_balance`: `core_component_stronger` fordi Mean core-share av aksedelta er 0.591 mot coarse-share 0.409.
- `next_step`: `explain_balanced_vs_core_cases` fordi Neste steg bør forklare hvorfor ett gap blir core-dominert mens det andre blir mer balansert.

## Tolkning

- Dette er fortsatt en ren forklaringsrunde på eksisterende data, ikke en ny simulering.
- Les dette som en lokal komponentforklaring for `growth_seed 202`, ikke som en global lov for `local_swap`.
