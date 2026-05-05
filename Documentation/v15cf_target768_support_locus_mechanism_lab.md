# Relasjonell universgraf v0.15cf: target-768 support-locus mechanism lab

## Formal

Denne runden ser bare pa den stabile resten etter `v15ce`: placement `0` og `2` ved target `768`.
Sporsmalet er om target-768 ser bedre ut som en support-locus-splitt enn som en bred carrier family-map.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 768 | 768.0 | 768.0 | 768.0 | 1 |

## Profile summary

| profile | coarse | core | rare | support core | occ entropy | top3 | mean dist | shell4+ | rare mass | spectral rel |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p0 | 0.888 | 0.217 | 0.368 | 0.833 | 0.934 | 0.046 | 4.467 | 0.678 | 0.085 | 0.008 |
| add_chord_p2 | 0.882 | 0.214 | 0.385 | 0.833 | 0.918 | 0.116 | 7.060 | 0.693 | 0.088 | 0.017 |
| local_swap_p0 | 0.975 | 0.155 | 0.363 | 1.000 | 0.940 | 0.045 | 5.044 | 0.661 | 0.098 | 0.003 |
| local_swap_p2 | 0.965 | 0.121 | 0.471 | 1.000 | 0.919 | 0.057 | 6.963 | 0.711 | 0.125 | 0.007 |

## Locus summary

| placement | profiles | coarse | core | rare | support core | occ entropy | top3 | mean dist | shell4+ | rare mass | spectral rel |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | add_chord_p0;local_swap_p0 | 0.931 | 0.186 | 0.366 | 0.917 | 0.937 | 0.046 | 4.755 | 0.669 | 0.092 | 0.006 |
| 2 | add_chord_p2;local_swap_p2 | 0.923 | 0.167 | 0.428 | 0.917 | 0.918 | 0.087 | 7.012 | 0.702 | 0.106 | 0.012 |

## Comparison summary

| compare | rare gap | support-core gap | distance gap | shell4+ gap | rare-mass gap | entropy gap | top3 gap | coarse gap | spectral gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p2_minus_p0 | 0.017 | 0.000 | 2.593 | 0.015 | 0.003 | -0.016 | -0.070 | 0.006 | 0.009 |
| local_swap_p2_minus_p0 | 0.107 | 0.000 | 1.920 | 0.050 | 0.026 | -0.022 | -0.012 | 0.010 | 0.004 |
| pooled_p2_minus_p0 | 0.062 | 0.000 | 2.256 | 0.033 | 0.015 | -0.019 | -0.041 | 0.008 | 0.007 |

## Carrier gap

| compare | core gap | rare gap | support-core gap | distance gap | shell4+ gap | rare-mass gap | entropy gap | top3 gap | spectral gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| carrier_gap_at_p0 | 0.062 | 0.005 | 0.167 | 0.577 | 0.017 | 0.014 | 0.006 | 0.001 | 0.005 |
| carrier_gap_at_p2 | 0.093 | 0.085 | 0.167 | 0.097 | 0.018 | 0.037 | 0.000 | 0.059 | 0.010 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle target-768 support-locus-runs matcher onsket perturbasjon.
- `support_locus_mechanism`: `support_locus_split_not_yet` fordi Heller ikke denne smale p0/p2-observabelen skiller target-768-resten rent.
- `next_step`: `new_target768_observable` fordi Neste steg bor vaere en ny target-768-observabel, ikke mer av samme support-locus-lesning.

## Tolkning

- Dette er en smal target-768-runde rundt den stabile resten, ikke et nytt family-sok.
- Positivt signal her betyr at p0/p2-splittelsen leses bedre som locus-mekanisme enn som full carrier-fysikk.
- Near-symmetry skal fortsatt leses som feature-level naerhet, ikke sterkere.
