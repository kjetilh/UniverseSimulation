# Relasjonell universgraf v0.15ba: local_swap compressed-shell explainer

## Formål

Denne runden sjekker om `202/p3` best leses som en komprimert shell-retur, i stedet for bare som en svak eller mislykket pocket.

## Case rows

| role | growth_seed | placement | label | coarse return | core share | shell share | rare share | shell+rare | core/shell | tail density |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| background_control | 101 | 0 | diffuse_shell_recurrence | 0.677 | 0.352 | 0.443 | 0.205 | 0.648 | 0.795 | 0.548 |
| background_control | 101 | 1 | mixed_core_shell | 0.615 | 0.402 | 0.448 | 0.149 | 0.598 | 0.897 | 0.618 |
| background_control | 101 | 2 | diffuse_shell_recurrence | 0.446 | 0.192 | 0.479 | 0.329 | 0.808 | 0.400 | 0.416 |
| pocket_anchor | 101 | 3 | stable_core_variable_shell | 0.785 | 0.563 | 0.287 | 0.149 | 0.437 | 1.960 | 0.698 |
| high_amplification_nonpocket | 202 | 0 | mixed_core_shell | 0.585 | 0.516 | 0.333 | 0.151 | 0.484 | 1.548 | 0.675 |
| high_coarse_diffuse_control | 202 | 1 | diffuse_shell_recurrence | 0.846 | 0.342 | 0.384 | 0.274 | 0.658 | 0.893 | 0.520 |
| background_control | 202 | 2 | diffuse_shell_recurrence | 0.446 | 0.130 | 0.442 | 0.429 | 0.870 | 0.294 | 0.338 |
| compressed_flip_candidate | 202 | 3 | diffuse_shell_recurrence | 0.631 | 0.222 | 0.444 | 0.333 | 0.778 | 0.500 | 0.442 |

## Role summary

| role | n | stable core+shell | diffuse shell | coarse return | shell+rare | core/shell | tail density | tail union nodes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| compressed_flip_candidate | 1 | 0.000 | 1.000 | 0.631 | 0.778 | 0.500 | 0.442 | 36.0 |
| pocket_anchor | 1 | 1.000 | 0.000 | 0.785 | 0.437 | 1.960 | 0.698 | 87.0 |
| high_coarse_diffuse_control | 1 | 0.000 | 1.000 | 0.846 | 0.658 | 0.893 | 0.520 | 73.0 |
| high_amplification_nonpocket | 1 | 0.000 | 0.000 | 0.585 | 0.484 | 1.548 | 0.675 | 93.0 |
| background_control | 4 | 0.000 | 0.750 | 0.546 | 0.731 | 0.597 | 0.480 | 81.2 |

## Operativ lesning

- `compressed_shell_status`: `compressed_shell_return_supported` fordi `202/p3` ser ikke best ut som svak pocket. Den holder fortsatt recurrence, men i en komprimert shell-dominert modus med hoy shell+rare-andel og lav tail-density.
- `relative_scope`: `shell_heavier_than_pocket` fordi `202/p3` er mer shell-dominert enn pocket-caset og samtidig mer komprimert i tailen.
- `next_step`: `explain_shell_retention_inside_growth202` fordi Neste steg bør sammenligne `202/p3` mot andre `growth_seed 202`-caser for a forklare hvorfor akkurat denne plasseringen holder pa shell-retur.

## Tolkning

- Dette er en ren forklaringsrunde pa toppen av v15aw-v15az, ikke en ny simulering.
- Les dette som en liten modusforklaring for `202/p3`, ikke som en ny generell local_swap-lov.
