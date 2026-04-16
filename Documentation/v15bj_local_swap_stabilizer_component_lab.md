# Relasjonell universgraf v0.15bj: local_swap stabilizer component lab

## Formål

Denne runden åpner `full_stabilizer` fra `v15bi` for å se hva `p2` faktisk mangler relativt til `p1`.

## Component decomposition

| component | gap | share of total |
| --- | --- | --- |
| coarse_return | 0.400 | 0.561 |
| core_share | 0.213 | 0.298 |
| shell2_over_shell1 | 0.100 | 0.140 |
| full_stabilizer_gap | 0.713 | 1.000 |

## Operativ lesning

- `stabilizer_component_status`: `retention_led_stabilizer_deficit_supported` fordi p2 mangler ikke stabilisering pa alle fronter like mye. Underskuddet er retention-led, med core-share som tydelig sekundarkomponent og shell-lagdeling som liten tredjekomponent.
- `component_shares`: `retention_core_shell_shares` fordi Retention 0.561, core 0.298, shell-lagdeling 0.140 av total stabiliseringsgap.
- `next_step`: `compare_missing_retention_vs_missing_core` fordi Neste steg bør forklare hvorfor retention-led underskudd og høy last møtes akkurat i p2.

## Tolkning

- Dette er fortsatt en forklaringsrunde på eksisterende data, ikke en ny simulering.
- Les dette som en lokal p1-vs-p2-komponentdeling, ikke som en global local_swap-lov.
