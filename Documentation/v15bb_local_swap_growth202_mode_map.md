# Relasjonell universgraf v0.15bb: local_swap growth202 mode map

## Formål

Denne runden sjekker om de fire plasseringene inne i `target 96`, `growth_seed 202` faktisk fyller forskjellige lokale modi, i stedet for bare ulike grader av samme diffuse restkategori.

## Placement map

| placement | support | core-shell label | coarse return | shell+rare | core/shell | tail density | tail union | mode |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 8,10,64 | mixed_core_shell | 0.585 | 0.484 | 1.548 | 0.675 | 93.0 | high_core_mixed_mode |
| 1 | 6,7,18 | diffuse_shell_recurrence | 0.846 | 0.658 | 0.893 | 0.520 | 73.0 | wide_diffuse_retention_mode |
| 2 | 6,7,8 | diffuse_shell_recurrence | 0.446 | 0.870 | 0.294 | 0.338 | 77.0 | dissipative_rare_shell_mode |
| 3 | 0,13,39 | diffuse_shell_recurrence | 0.631 | 0.778 | 0.500 | 0.442 | 36.0 | compressed_shell_return_mode |

## Operativ lesning

- `growth202_mode_status`: `growth202_mode_map_supported` fordi De fire growth_seed-202-plasseringene fyller fire ulike lokale modi i stedet for a kollapse til én diffus restkategori.
- `next_step`: `compare_p3_to_other_202_modes` fordi Neste steg bør forklare hvorfor p3 velger komprimert shell-retur mens p1 og p2 velger andre diffuse modi.

## Tolkning

- Dette er en ren forklaringsrunde inne i growth_seed 202, ikke en ny simulering.
- Les dette som et lite moduskart for én lokal familie, ikke som en bred lov for local_swap.
