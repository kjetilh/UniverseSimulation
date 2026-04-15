# Relasjonell universgraf v0.15bf: local_swap gap asymmetry explainer

## Formål

Denne runden spør om `p1 > p3` og `p3 > p2` faktisk er to ulike typer lokale gap inne i den samme triggeraksen.

## Pair asymmetry

| pair | coarse gap | core/shell gap | tail density gap | core-share gap | shell burden gap | mode |
| --- | --- | --- | --- | --- | --- | --- |
| p1_vs_p3 | 0.215 | 0.393 | 0.078 | 0.120 | 0.120 | core_shape_separation |
| p3_vs_p2 | 0.185 | 0.206 | 0.104 | 0.092 | 0.092 | retention_plus_shell_drag |
| p1_vs_p2 | 0.400 | 0.599 | 0.182 | 0.213 | 0.213 | mixed_gap_family |

## Operativ lesning

- `gap_asymmetry_status`: `neighbor_gap_asymmetry_supported` fordi De to nabogapene er ikke samme type: øvre gap er mer ren kjerneform-separasjon, nedre gap er mer en blandet retention+shell-drag-overgang.
- `next_step`: `explain_shell_drag_side` fordi Neste steg bør gå på shell-drag-siden av den balanserte overgangen, ikke lete etter enda en ny totalakse.

## Tolkning

- Dette er fortsatt en forklaringsrunde på eksisterende data, ikke en ny simulering.
- Les dette som lokal struktur inne i growth_seed-202-splittelsen, ikke som en global local_swap-lov.
