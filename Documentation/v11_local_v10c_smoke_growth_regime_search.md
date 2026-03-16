# v0.10c growth-regime search

Dette dokumentet sammenligner noen få alternative growth-regimer etter at v0.10b viste at referansegeneratoren ikke skalerte troverdig til store nominelle størrelser.

## Viktig tolkning

- `fast_ref`, `fast_balanced` og `fast_push` er **generatorregimer**, ikke nye fysiske teorier.
- De er ment som praktiske ensemblebyggere for storskala tester.
- God størrelse-treff alene er ikke nok; vi må også se på frøvarians og en enkel naturalness-proxy.

## Regime-aggregater

| regime | mean_abs_rel_err | hit_rate | naturalness | sd_nodes_mean | composite |
| --- | --- | --- | --- | --- | --- |
| fast_ref | 0.000 | 1.00 | 0.316 | 0.00 | 0.829 |
| fast_push | 0.037 | 0.92 | 0.278 | 0.83 | 0.655 |
| fast_balanced | 0.040 | 0.67 | 0.340 | 1.50 | 0.584 |

## Per størrelse og burn-in-label

| regime | burnin | target | realized_mean | q10 | q90 | hit_rate | naturalness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| fast_balanced | deep | 96 | 96.0 | 96.0 | 96.0 | 1.00 | 0.383 |
| fast_balanced | deep | 192 | 192.0 | 192.0 | 192.0 | 1.00 | 0.324 |
| fast_balanced | deep | 256 | 256.0 | 256.0 | 256.0 | 1.00 | 0.303 |
| fast_balanced | light | 96 | 101.0 | 97.0 | 105.0 | 0.50 | 0.383 |
| fast_balanced | light | 192 | 212.0 | 212.0 | 212.0 | 0.00 | 0.320 |
| fast_balanced | light | 256 | 278.0 | 274.8 | 281.2 | 0.50 | 0.325 |
| fast_push | deep | 96 | 96.0 | 96.0 | 96.0 | 1.00 | 0.279 |
| fast_push | deep | 192 | 192.0 | 192.0 | 192.0 | 1.00 | 0.282 |
| fast_push | deep | 256 | 256.0 | 256.0 | 256.0 | 1.00 | 0.261 |
| fast_push | light | 96 | 105.5 | 105.1 | 105.9 | 0.50 | 0.303 |
| fast_push | light | 192 | 205.5 | 203.5 | 207.5 | 1.00 | 0.280 |
| fast_push | light | 256 | 270.0 | 268.4 | 271.6 | 1.00 | 0.264 |
| fast_ref | deep | 96 | 96.0 | 96.0 | 96.0 | 1.00 | 0.317 |
| fast_ref | deep | 192 | 192.0 | 192.0 | 192.0 | 1.00 | 0.336 |
| fast_ref | deep | 256 | 256.0 | 256.0 | 256.0 | 1.00 | 0.295 |
| fast_ref | light | 96 | 96.0 | 96.0 | 96.0 | 1.00 | 0.317 |
| fast_ref | light | 192 | 192.0 | 192.0 | 192.0 | 1.00 | 0.336 |
| fast_ref | light | 256 | 256.0 | 256.0 | 256.0 | 1.00 | 0.295 |

## Nivåseparasjon

| regime | burnin | A | B | gap_q90_to_q10 | overlap_fraction | separated |
| --- | --- | --- | --- | --- | --- | --- |
| fast_balanced | deep | 96 | 192 | 96.0 | 0.00 | 1 |
| fast_balanced | deep | 192 | 256 | 64.0 | 0.00 | 1 |
| fast_balanced | light | 96 | 192 | 107.0 | 0.00 | 1 |
| fast_balanced | light | 192 | 256 | 62.8 | 0.00 | 1 |
| fast_push | deep | 96 | 192 | 96.0 | 0.00 | 1 |
| fast_push | deep | 192 | 256 | 64.0 | 0.00 | 1 |
| fast_push | light | 96 | 192 | 97.6 | 0.00 | 1 |
| fast_push | light | 192 | 256 | 60.9 | 0.00 | 1 |
| fast_ref | deep | 96 | 192 | 96.0 | 0.00 | 1 |
| fast_ref | deep | 192 | 256 | 64.0 | 0.00 | 1 |
| fast_ref | light | 96 | 192 | 96.0 | 0.00 | 1 |
| fast_ref | light | 192 | 256 | 64.0 | 0.00 | 1 |

## Kort dom

Et regime er ikke automatisk bedre bare fordi det treffer målstørrelsen eksakt. Hvis dette oppnås ved å produsere for enkle eller for smale strukturer, må det sies eksplisitt.
I praksis bør prosjektet foretrekke et regime som både treffer størrelse og bevarer et rimelig forhold til de mindre, mer troverdige naturlige strukturene.

