# Relasjonell universgraf v0.15bd: local_swap trigger-axis lab

## Formål

Denne runden tester et lite sett tolkbare kandidat-akser for a se om en av dem ordner de tre diffuse growth_seed-202-modiene som `p1 > p3 > p2`.

## Placement snapshot

| placement | label | coarse return | core share | shell+rare | tail density | core/shell | mean degree | ball3/ball1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | mixed_core_shell | 0.585 | 0.516 | 0.484 | 0.675 | 1.548 | 4.667 | 4.091 |
| 1 | diffuse_shell_recurrence | 0.846 | 0.342 | 0.658 | 0.520 | 0.893 | 6.667 | 2.722 |
| 2 | diffuse_shell_recurrence | 0.446 | 0.130 | 0.870 | 0.338 | 0.294 | 7.667 | 2.571 |
| 3 | diffuse_shell_recurrence | 0.631 | 0.222 | 0.778 | 0.442 | 0.500 | 5.333 | 2.786 |

## Candidate axes

| axis | family | p1 | p3 | p2 | p0 | ordered | margin |
| --- | --- | --- | --- | --- | --- | --- | --- |
| retention_core_axis | dynamic | 1.739 | 1.131 | 0.740 | 2.133 | 1 | 0.390 |
| retention_density_axis | dynamic | 1.366 | 1.073 | 0.784 | 1.259 | 1 | 0.289 |
| retention_minus_shell_axis | dynamic | 0.189 | -0.147 | -0.424 | 0.101 | 1 | 0.277 |
| core_to_shell | dynamic | 0.893 | 0.500 | 0.294 | 1.548 | 1 | 0.206 |
| core_minus_shell_axis | dynamic | -0.315 | -0.556 | -0.740 | 0.032 | 1 | 0.185 |
| coarse_return | dynamic | 0.846 | 0.631 | 0.446 | 0.585 | 1 | 0.185 |
| core_share | dynamic | 0.342 | 0.222 | 0.130 | 0.516 | 1 | 0.092 |
| tail_density | dynamic | 0.520 | 0.442 | 0.338 | 0.675 | 1 | 0.078 |
| support_compactness_axis | support | -2.722 | -2.786 | -2.571 | -4.091 | 0 | nan |
| support_density_axis | support | 6.667 | 5.333 | 7.667 | 4.667 | 0 | nan |

## Operativ lesning

- `trigger_axis_status`: `retention_core_axis_supported` fordi En enkel dynamisk akse, `coarse_return + core_to_shell`, ordner p1 > p3 > p2 renere enn de andre tolkbare kandidatene.
- `support_axis_status`: `support_weaker_than_dynamic` fordi Beste støtteakse er `support_compactness_axis`, men den holder ikke ren ordering.
- `next_step`: `explain_axis_from_components` fordi Neste steg bør forklare hva som faktisk driver denne aksen lokalt, ikke bare bruke den som score.

## Tolkning

- Dette er en ren akselab pa eksisterende data, ikke en ny simulering.
- Les dette som en liten triggerakse for den diffuse modussplittelsen, ikke som en ny global lov.
