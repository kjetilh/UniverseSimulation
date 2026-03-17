# v0.10e verifikasjon og regresjon

- base-separasjon: ok
- toppkandidat på mean composite: band_zero_del
- pairwise-konsistens: ok
- focused_score-regenerering: ok

## Røde flagg

- hvis startnivåene ikke lenger er separerte, faller grunnlaget for v0.10e sammen metodisk
- hvis `band_best` plutselig er topprangert på `mean_composite`, er det et signal om at enten dataene eller fortolkningen har flyttet seg
- hvis pairwise-tabellen ikke summerer til omtrent 1 i begge retninger, er bootstrap-sammendraget ikke konsistent
- hvis `focused_score` ikke kan regenereres fra delscore-feltene, er kandidat-CSV-en ikke selvkonsistent
