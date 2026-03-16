# v0.10c growth-regime search

Dette dokumentet sammenligner noen få alternative growth-regimer etter at v0.10b viste at referansegeneratoren ikke skalerte troverdig til store nominelle størrelser.

## Viktig tolkning

- `fast_ref`, `fast_balanced` og `fast_push` er **generatorregimer**, ikke nye fysiske teorier.
- De er ment som praktiske ensemblebyggere for storskala tester.
- God størrelse-treff alene er ikke nok; vi må også se på frøvarians og en enkel naturalness-proxy.

## Regime-aggregater

| regime | mean_abs_rel_err | hit_rate | naturalness | sd_nodes_mean | composite |
| --- | --- | --- | --- | --- | --- |
| fast_ref | 0.000 | 1.00 | 0.485 | 0.00 | 0.871 |
| fast_push | 0.038 | 0.83 | 0.420 | 1.19 | 0.662 |
| fast_balanced | 0.043 | 0.79 | 0.509 | 1.40 | 0.654 |

## Per størrelse og burn-in-label

| regime | burnin | target | realized_mean | q10 | q90 | hit_rate | naturalness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| fast_balanced | deep | 96 | 96.0 | 96.0 | 96.0 | 1.00 | 0.574 |
| fast_balanced | deep | 192 | 192.0 | 192.0 | 192.0 | 1.00 | 0.492 |
| fast_balanced | deep | 256 | 256.0 | 256.0 | 256.0 | 1.00 | 0.475 |
| fast_balanced | light | 96 | 103.2 | 98.7 | 106.0 | 0.50 | 0.555 |
| fast_balanced | light | 192 | 210.0 | 208.0 | 212.0 | 0.50 | 0.485 |
| fast_balanced | light | 256 | 278.8 | 276.6 | 281.1 | 0.75 | 0.476 |
| fast_push | deep | 96 | 96.0 | 96.0 | 96.0 | 1.00 | 0.423 |
| fast_push | deep | 192 | 192.0 | 192.0 | 192.0 | 1.00 | 0.412 |
| fast_push | deep | 256 | 256.0 | 256.0 | 256.0 | 1.00 | 0.394 |
| fast_push | light | 96 | 105.8 | 105.3 | 106.0 | 0.25 | 0.457 |
| fast_push | light | 192 | 208.0 | 204.2 | 211.4 | 0.75 | 0.426 |
| fast_push | light | 256 | 267.0 | 264.0 | 270.8 | 1.00 | 0.405 |
| fast_ref | deep | 96 | 96.0 | 96.0 | 96.0 | 1.00 | 0.499 |
| fast_ref | deep | 192 | 192.0 | 192.0 | 192.0 | 1.00 | 0.491 |
| fast_ref | deep | 256 | 256.0 | 256.0 | 256.0 | 1.00 | 0.464 |
| fast_ref | light | 96 | 96.0 | 96.0 | 96.0 | 1.00 | 0.499 |
| fast_ref | light | 192 | 192.0 | 192.0 | 192.0 | 1.00 | 0.491 |
| fast_ref | light | 256 | 256.0 | 256.0 | 256.0 | 1.00 | 0.464 |

## Nivåseparasjon

| regime | burnin | A | B | gap_q90_to_q10 | overlap_fraction | separated |
| --- | --- | --- | --- | --- | --- | --- |
| fast_balanced | deep | 96 | 192 | 96.0 | 0.00 | 1 |
| fast_balanced | deep | 192 | 256 | 64.0 | 0.00 | 1 |
| fast_balanced | light | 96 | 192 | 102.0 | 0.00 | 1 |
| fast_balanced | light | 192 | 256 | 64.6 | 0.00 | 1 |
| fast_push | deep | 96 | 192 | 96.0 | 0.00 | 1 |
| fast_push | deep | 192 | 256 | 64.0 | 0.00 | 1 |
| fast_push | light | 96 | 192 | 98.2 | 0.00 | 1 |
| fast_push | light | 192 | 256 | 52.6 | 0.00 | 1 |
| fast_ref | deep | 96 | 192 | 96.0 | 0.00 | 1 |
| fast_ref | deep | 192 | 256 | 64.0 | 0.00 | 1 |
| fast_ref | light | 96 | 192 | 96.0 | 0.00 | 1 |
| fast_ref | light | 192 | 256 | 64.0 | 0.00 | 1 |

## Kort dom

Et regime er ikke automatisk bedre bare fordi det treffer målstørrelsen eksakt. Hvis dette oppnås ved å produsere for enkle eller for smale strukturer, må det sies eksplisitt.
I praksis bør prosjektet foretrekke et regime som både treffer størrelse og bevarer et rimelig forhold til de mindre, mer troverdige naturlige strukturene.

