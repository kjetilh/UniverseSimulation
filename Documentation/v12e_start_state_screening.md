# Relasjonell universgraf v0.12e: screening og sortering av starttilstander

## Formål

Denne runden tester om de enkle radius-basisene fra v12d kan brukes til billigere prediksjon eller sortering av starttilstander før vi kjører hele dynamikken.

## Metode

- Arbeidsregime: `band_zero_del`.
- Baseenheter: `32` starttilstander bygget fra `4` størrelser med `8` growth-seeds hver.
- Dynamiske etiketter: `192` simulasjonsruns aggregert til base-nivå (`mean_final_radius_control`).
- Validering: `40` stratified holdout-split med testandel `0.25` per størrelse.
- Sammenligningsoppgaven er bevisst praktisk: kan vi rangere eller screene baser bedre enn en naiv konstant baseline?

## Hvordan metricene leses

- `relative_skill`: hvor mye bedre RMSE modellen er enn en konstant baseline.
- `spearman_all`: hvor godt modellen bevarer global rangordning pa tvers av alle testbaser.
- `pairwise_within_target`: hvor ofte modellen rangerer to baser riktig innen samme størrelse. Dette er den viktigste screening-metrikken hvis vi vil unnga at størrelse alene dominerer.
- `top_quartile_lift_within_target`: hvor mye bedre de toppskorede basene faktisk er enn gjennomsnittet innen samme størrelse. Positiv verdi betyr nyttig screening-lift.

## Base-nivå per størrelse

| target | bases | mean_radius | sd_radius | mean_overlap | mean_fit_speed |
| --- | --- | --- | --- | --- | --- |
| 48 | 8 | 4.979 | 1.113 | 0.663 | 0.232 |
| 96 | 8 | 6.208 | 1.136 | 0.680 | 0.224 |
| 192 | 8 | 8.000 | 0.645 | 0.600 | 0.225 |
| 256 | 8 | 7.125 | 1.092 | 0.707 | 0.219 |

## Screening-sammendrag

| rank | basis | pairwise_within_target | top_quartile_lift_within_target | spearman_all | relative_skill |
| --- | --- | --- | --- | --- | --- |
| 1 | full_basis | 0.550 | 0.011 | 0.592 | 0.151 |
| 2 | spectral_plus_dim | 0.521 | -0.006 | 0.691 | 0.245 |
| 3 | spectral_plus_clustering | 0.473 | -0.000 | 0.578 | 0.214 |
| 4 | spectral_only | 0.427 | -0.015 | 0.549 | 0.224 |

## Operativ lesning

- Beste screening-basis i denne runden er `full_basis` med within-target pairwise `0.550` og within-target top-quartile lift `0.011`.
- Narmeste kontroll er `spectral_plus_dim`. Hvis den ligger naert, er det mer riktig a snakke om et lite arbeidsplateau enn en hard enkeltrangering.
- Beste kompakte basis er `spectral_plus_dim`. Den slar ikke `full_basis` pa within-target screening her, men den holder hoyere global korrelasjon og bedre enkelhet.
- Den viktige metodiske lesningen er derfor ikke at én basis vant alt, men at repoet nå støtter et benchmark-vs-kompakt-basis-skille.
- Denne runden ma leses som en nyttetest av en enkel surrogate, ikke som ny fysikk i seg selv.

