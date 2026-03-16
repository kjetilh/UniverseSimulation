# v0.8b verifikasjon og regresjon

## Hva som ble sjekket

- at de naturlige ensemblefamiliene faktisk ble større enn `toy_cycle8`,
- at bootstrap-intervallene omslutter de tilhørende punktestimatene,
- at rangeringen etter `ci_low_mean_composite_natural` ikke hopper rundt når bootstrap-seed endres litt,
- og at CSV-strukturen fortsatt inneholder de viktigste bakoverkompatible kolonnene.

## Resultat

- Kolonnesjekk run CSV: pass
- Kolonnesjekk ensemble CSV: pass
- Kolonnesjekk overall CSV: pass
- Naturlige ensembler større enn `toy_cycle8`: pass
- Bootstrap-konsistens: pass
- Ranking-stabilitet: pass

## Detaljer

- `toy_cycle8` mean initial nodes: 8.000
- `natural24` mean initial nodes: 33.200
- `natural48` mean initial nodes: 53.000
- `natural_jitter` mean initial nodes: 40.800
- Ranking-kriteriet her er pragmatisk: baseline-topkandidaten skal holde seg innen topp-2 over små bootstrap-seed-endringer.
- Topkandidaten fra baseline-bootstrap holdt posisjonene [1, 1, 2, 1, 1] over seed-varianten.
- Felles kandidater i top-3 over alle bootstrap-seeds: 2
