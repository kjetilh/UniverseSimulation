# Relasjonell universgraf v0.15ck: target-768 outer feeder flux lab

## Formal

Denne runden tester om ny outer-masse ved p2 mates gjennom fa, konsentrerte feeder-soner fra inner shell-3.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 768 | 768.0 | 768.0 | 768.0 | 1 |

## Aggregate feeder flux

| profile | concentrated | diffuse | self-prop | mixed | birth intensity | feeder cov | feeder top1 | feeder top3 | self-parent cov |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p0 | 0.000 | 0.000 | 0.750 | 0.250 | 1.160 | 0.386 | 0.897 | 0.999 | 0.672 |
| add_chord_p2 | 0.250 | 0.000 | 0.500 | 0.250 | 0.115 | 0.398 | 1.000 | 1.000 | 0.510 |
| local_swap_p0 | 0.000 | 0.000 | 1.000 | 0.000 | 2.656 | 0.306 | 0.816 | 0.997 | 0.811 |
| local_swap_p2 | 0.000 | 0.000 | 1.000 | 0.000 | 2.996 | 0.038 | 0.993 | 1.000 | 0.915 |

## P2 versus P0

| compare | concentrated gap | feeder cov gap | feeder top1 gap | feeder top3 gap | self-parent gap | birth intensity gap |
| --- | --- | --- | --- | --- | --- | --- |
| add_chord_p2_minus_p0 | 0.250 | 0.012 | 0.103 | 0.001 | -0.161 | -1.045 |
| local_swap_p2_minus_p0 | 0.000 | -0.268 | 0.176 | 0.003 | 0.104 | 0.340 |

## Cross-carrier P2 contrast

| compare | concentrated gap | feeder cov gap | feeder top1 gap | feeder top3 gap | self-parent gap | birth intensity gap |
| --- | --- | --- | --- | --- | --- | --- |
| local_swap_p2_minus_add_chord_p2 | -0.250 | -0.360 | -0.007 | 0.000 | 0.404 | 2.881 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon.
- `shared_p2_feeder_flux`: `feeder_flux_not_yet` fordi Feeder-fluxen skiller ikke p2 fra p0 rent i begge carrierne.
- `carrier_alignment`: `aligned` fordi Carrier-alignment her betyr bare at p2-vs-p0-feeder-gapen peker samme vei i begge carrierne.
- `next_step`: `different_mechanism_axis` fordi Neste steg bor vaere en annen mekanismeakse enn outer-flux.

## Tolkning

- Dette er en smal flux-observabel ved target 768, ikke et nytt skalahopp.
- Positivt signal her betyr bare at outer-halen mates gjennom fa indre feeder-soner ved p2.
