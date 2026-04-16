# Relasjonell universgraf v0.15bg: local_swap shell-drag decomposition

## Formål

Denne runden åpner `retention_plus_shell_drag` fra `v15bf` for å se om shell-draget faktisk bæres av ordinær shell-bredde eller av rare-last.

## Relevant placements

| placement | label | coarse return | shell share | rare share | shell+rare | tail union | tail density |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | diffuse_shell_recurrence | 0.446 | 0.442 | 0.429 | 0.870 | 77 | 0.338 |
| 3 | diffuse_shell_recurrence | 0.631 | 0.444 | 0.333 | 0.778 | 36 | 0.442 |

## Shell-drag decomposition

| pair | shell gap | rare gap | shell-burden gap | rare fraction | shell fraction | tail-union gap | density gap | mode |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| p3_vs_p2 | -0.003 | 0.095 | 0.092 | 1.031 | -0.031 | 41 | 0.104 | rare_loaded_shell_drag |

## Operativ lesning

- `shell_drag_status`: `rare_loaded_shell_drag_supported` fordi Den balanserte p3 > p2-overgangen ser ikke ut som bredere shell i seg selv; taperen bærer nesten hele shell-draget som oppblåst rare-last.
- `next_step`: `explain_rare_load_trigger` fordi Neste steg bør forklare hva som avgjør om rare-last blåses opp i den dissipative p2-retningen.

## Tolkning

- Dette er fortsatt en ren forklaringsrunde på eksisterende data, ikke en ny simulering.
- Les dette som en lokal dekomponering av `p3 > p2`-overgangen, ikke som en generell lov for alle local_swap-tilfeller.
