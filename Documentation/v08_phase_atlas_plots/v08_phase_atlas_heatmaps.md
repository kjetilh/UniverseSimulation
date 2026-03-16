# v0.8 atlas heatmaps

## Observasjon

- Hver figur viser én score om gangen, uten subplots.
- Kolonnene er `(r_birth, r_death)`-kombinasjoner, og radene er `(p_swap, p_triad, p_del)`-kombinasjoner.
- Hvite markeringer er Paretofront-punkter.

## Tolkning

- Dette er ikke et fullstendig fasekart over hele parameterrommet. Det er en visualisering av det valgte coarse/refined-slicet.
- `p_del = 0` ble brukt i coarse-atlaset fordi v0.8 startet fra den delen av rommet som så mest lovende ut uten sletting; refined-runden åpner denne aksen svakt igjen.
- Paretofront er nyttig fordi repair, causalitet, quasi-stabilitet og geometri-proxy konkurrerer. Et punkt kan være svært godt på én akse uten å være globalt best.

## Spekulasjon som fortsatt må holdes nede

- Et varmt område i `composite_score` er ikke i seg selv en fase.
- Et Pareto-punkt er ikke nødvendigvis fysisk interessant; det kan også være et kompromisspunkt uten sterk spacetime-lesning.

## Filer

- `coarse_composite_score_heatmap.png`
- `coarse_repair_score_heatmap.png`
- `coarse_causal_score_heatmap.png`
- `coarse_quasi_score_heatmap.png`
- `coarse_geom_score_heatmap.png`
- `refined_composite_score_heatmap.png`
- `refined_repair_score_heatmap.png`
- `refined_causal_score_heatmap.png`
- `refined_quasi_score_heatmap.png`
- `refined_geom_score_heatmap.png`

_Coarse rows: 54_

_Refined rows: 324_
