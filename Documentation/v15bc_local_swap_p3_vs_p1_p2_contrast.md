# Relasjonell universgraf v0.15bc: local_swap p3-vs-p1-p2 contrast

## Formål

Denne runden forklarer hva som faktisk skiller `p3` fra de to mest informative nabomodusene i `growth_seed 202`: `p1` og `p2`.

## Placement snapshot

| placement | label | coarse return | shell+rare | core/shell | tail density | tail union |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | diffuse_shell_recurrence | 0.846 | 0.658 | 0.893 | 0.520 | 73.0 |
| 2 | diffuse_shell_recurrence | 0.446 | 0.870 | 0.294 | 0.338 | 77.0 |
| 3 | diffuse_shell_recurrence | 0.631 | 0.778 | 0.500 | 0.442 | 36.0 |

## Pairwise contrasts

| pair | contrast | coarse gap | shell+rare gap | core/shell gap | tail density gap | tail union gap | rare gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| p3_vs_p1 | compressed_vs_wide_retention | -0.215 | 0.120 | -0.393 | -0.078 | -37.0 | 0.059 |
| p3_vs_p2 | retained_vs_dissipative_shell | 0.185 | -0.092 | 0.206 | 0.104 | -41.0 | -0.095 |

## Operativ lesning

- `p3_boundary_contrast`: `p3_boundary_contrast_supported` fordi P3 skiller seg fra p1 og p2 langs to forskjellige akser: kompresjon mot bred retention, og retention mot dissipativ rare-shell.
- `next_step`: `look_for_shared_trigger_axis` fordi Neste steg bør lete etter én liten triggerakse som avgjør om samme diffuse regime blir bred retention, komprimert shell-retur eller dissipativ rare-shell.

## Tolkning

- Dette er en ren kontrastanalyse inne i `growth_seed 202`, ikke en ny simulering.
- Les dette som en forklaring av p3-grensen mot to naere modi, ikke som en bred ny local_swap-lov.
