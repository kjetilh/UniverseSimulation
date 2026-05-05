# Relasjonell universgraf v0.15cl: target-768 inner gate / global budget lab

## Formal

Denne runden tester om p2-horisonten ved target 768 er koblet til en indre shell2/3-gate og global budget-lignende redistribusjon.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 768 | 768.0 | 768.0 | 768.0 | 1 |

## Aggregate inner gate / budget

| profile | horizon | pre gate peak | gate release | outer gain | opposite motion | spectral drift | beta1 drift |
| --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p0 | 0.000 | 0.208 | 0.054 | 0.080 | 0.916 | 0.008 | 0.010 |
| add_chord_p2 | 0.250 | 0.161 | 0.053 | 0.058 | 0.479 | 0.002 | 0.010 |
| local_swap_p0 | 0.000 | 0.231 | 0.082 | 0.192 | 0.940 | 0.015 | 0.000 |
| local_swap_p2 | 0.750 | 0.126 | 0.041 | 0.077 | 0.753 | 0.004 | 0.000 |

## P2 versus P0

| compare | horizon gap | pre gate gap | release gap | outer gain gap | opposite motion gap | spectral drift gap | beta1 drift gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p2_minus_p0 | 0.250 | -0.047 | -0.001 | -0.022 | -0.437 | -0.006 | 0.000 |
| local_swap_p2_minus_p0 | 0.750 | -0.106 | -0.041 | -0.115 | -0.187 | -0.010 | 0.000 |

## Cross-carrier P2 contrast

| compare | horizon gap | pre gate gap | release gap | outer gain gap | opposite motion gap | spectral drift gap | beta1 drift gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| local_swap_p2_minus_add_chord_p2 | 0.500 | -0.035 | -0.012 | 0.019 | 0.274 | 0.002 | -0.010 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon.
- `shared_p2_inner_gate`: `inner_gate_not_yet` fordi Shell2/3-gate skiller ikke p2 fra p0 rent (scores add=1/5, swap=1/5).
- `global_budget_coupling`: `global_budget_coupling_not_yet` fordi Det finnes ikke nok evidens for at p2-horisonten er global-budget-koblet i denne observabelen (scores add=2/4, swap=2/4).
- `next_step`: `try_local_trigger_or_scale_holdout` fordi Neste steg bor ikke oppgradere globale invarianter; prov en ren lokal trigger eller hold p2-horisonten ut paa ny skala.

## Tolkning

- Dette er en smal mekanismeobservabel, ikke et bevis for globale invarianter.
- Positivt signal betyr bare at p2-horisonten kan vaere koblet til indre redistribusjon under relativt stabile globale budget-metrikker.
- Negativt signal betyr at globale invariant-spraak ikke bor oppgraderes her; da bor neste steg vaere ren lokal trigger eller ny skala.
