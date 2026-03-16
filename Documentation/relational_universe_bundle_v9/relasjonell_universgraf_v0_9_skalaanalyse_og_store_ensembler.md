# Relasjonell universgraf v0.9 – skalaanalyse, større naturlige ensembler og burn-in-sensitivitet

## Sammendrag

v0.9 tar det neste metodisk riktige steget etter v0.8b: i stedet for bare å spørre hvilke regimer som er robuste på naturlige ensembler, spør vi hvordan denne robustheten **skalerer** når de naturlige starttilstandene blir større og når de får forskjellig modenhet før perturbasjonen settes inn.

Dette steget gjør fire ting samtidig:

1. evaluerer et fokusert kandidatbånd fra v0.8b på større naturlige ensembler,
2. introduserer både lett og dyp burn-in ved hver skala,
3. bruker hendelsesbudsjetter som vokser med initial størrelse,
4. estimerer skalaindikatorer for radius/front, overlap/repair og quasi-invariant-bevaring.

## Metode

- kandidater testet: 5
- naturlige ensembler: 6
- growth seeds per ensemble: 2
- event-budsjett: steps = clamp(round(4.5 * N_init), 120, 300)
- bootstrap-replikater for kandidatoppsummeringer: 80

Naturlige starttilstander er fortsatt vokst frem av modellens egen dynamikk, ikke hånddesignet. Dermed blir v0.9 en strengere test av om kandidatbåndet overlever kontakt med større og mer moden intern geometri.

## Startensembler

| ensemble | burn-in | target | mean nodes | mean tokens | mean β1 | mean spectral radius | mean dim proxy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| natural24_light | light | 24 | 27.5 | 5.0 | 3.0 | 3.21 | 2.22 |
| natural24_deep | deep | 24 | 35.0 | 8.0 | 5.0 | 3.64 | 2.13 |
| natural48_light | light | 48 | 45.0 | 15.0 | 8.0 | 4.04 | 2.34 |
| natural48_deep | deep | 48 | 58.5 | 15.0 | 12.5 | 4.29 | 2.85 |
| natural96_light | light | 96 | 78.5 | 15.5 | 15.5 | 4.36 | 2.88 |
| natural96_deep | deep | 96 | 91.0 | 29.5 | 23.0 | 5.05 | 3.03 |

## Viktigste funn

- Høyest rangert kandidat i v0.9 ble `balanced_pdel` med mean composite ≈ 0.703 og bootstrap lower bound ≈ 0.622.
- Samme kandidat hadde radius-eksponent α ≈ 0.068 og burn-in-sensitivitet ≈ 0.020.
- Overlap-vs-logN-slope var ≈ 0.217, mens quasi-vs-logN-slope var ≈ -0.324.
- Neste kandidat lå nær med mean composite ≈ 0.694 og bootstrap lower bound ≈ 0.595.

Disse tallene betyr ikke at vi har etablert en fysisk teori. De betyr at kandidatrommet igjen blir **smalere** når testen blir strengere, og at vi nå kan begynne å skille mellom kandidater som bare er robuste på moderate naturlige ensembler og kandidater som også ser rimelige ut under skalaøkning.

## Toppkandidater

| candidate | r_birth | r_death | p_swap | p_triad | p_del | mean composite | CI low | radius α | overlap slope | quasi slope | burn-in sens |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| balanced_pdel | 0.02 | 0.02 | 0.02 | 0.00 | 0.01 | 0.703 | 0.622 | 0.068 | 0.217 | -0.324 | 0.020 |
| triad_runner | 0.02 | 0.02 | 0.02 | 0.02 | 0.00 | 0.694 | 0.595 | 0.189 | 0.096 | -0.002 | 0.099 |
| band_best | 0.02 | 0.00 | 0.02 | 0.00 | 0.01 | 0.653 | 0.589 | 0.368 | 0.151 | -0.136 | 0.068 |
| macro_stable | 0.02 | 0.05 | 0.02 | 0.00 | 0.01 | 0.655 | 0.580 | -0.135 | 0.238 | -0.182 | 0.045 |
| high_birth | 0.08 | 0.02 | 0.02 | 0.00 | 0.01 | 0.592 | 0.460 | -0.238 | 0.152 | -0.078 | 0.239 |

## Gruppeprofil for beste kandidat: `balanced_pdel`

| ensemble | target | burn-in | composite | repair | causal | quasi | geom | radius | overlap | |Δβ1| | init nodes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| natural24_deep | 24 | deep | 0.663 | 0.467 | 0.753 | 0.802 | 0.751 | 2.50 | 0.645 | 0.00 | 35.0 |
| natural24_light | 24 | light | 0.680 | 0.536 | 0.651 | 0.979 | 0.670 | 4.00 | 0.491 | 0.00 | 27.5 |
| natural48_deep | 48 | deep | 0.879 | 0.889 | 0.882 | 0.938 | 0.798 | 1.00 | 0.924 | 0.00 | 58.5 |
| natural48_light | 48 | light | 0.846 | 0.880 | 0.856 | 0.938 | 0.681 | 1.00 | 0.908 | 0.00 | 45.0 |
| natural96_deep | 96 | deep | 0.572 | 0.639 | 0.486 | 0.562 | 0.569 | 3.50 | 0.802 | 1.00 | 91.0 |
| natural96_light | 96 | light | 0.582 | 0.619 | 0.439 | 0.562 | 0.715 | 4.00 | 0.751 | 1.00 | 78.5 |

## Hvordan skalaindikatorene skal leses

- **radius α**: log-log-helning for `(radius + 1)` mot `N`. Lavere verdi betyr at fronten vokser mer sublineært med størrelse.
- **overlap slope**: helning for local-overlap mot `log N`. Mindre negativ eller positiv helning er bedre.
- **quasi slope**: helning for quasi-score mot `log N`. Høyere verdi betyr at quasi-invariant-bevaring ikke kollapser raskt med skala.
- **burn-in sensitivity**: gjennomsnittlig differanse i composite mellom lett og dyp burn-in ved samme målskala. Lavere er bedre.

## Tolkning

Det mest interessante i v0.9 er ikke bare hvem som vant, men at analysen nå skiller mellom tre typer robusthet samtidig:

1. **ensemble-robusthet**: kandidaten må gjøre det bra på flere naturlige startfamilier,
2. **burn-in-robusthet**: kandidaten må ikke være sterkt avhengig av én spesifikk modenhetsgrad,
3. **skala-robusthet**: radius og drift bør ikke eksplodere ukontrollert når initial størrelse øker.

Hvis et kandidatbånd fortsatt ser bra ut under alle tre testene, er det metodisk langt mer interessant enn et regime som bare er pent på små hånddesignede startgrafer.

## Referanser til metodefamilier

Denne typen v0.9-analyse er inspirert av klassisk finite-size scaling og bootstrap-tradisjonen: man forsøker å lese av hvordan observerbare størrelser endrer seg med systemstørrelse og å sette intervaller på estimerte størrelser ved resampling. I vår setting er dette ikke et vanlig gittersystem, men metodologien er beslektet.

- M. E. Fisher og M. N. Barber, *Scaling Theory for Finite-Size Effects in the Critical Region*, Phys. Rev. Lett. 28, 1516 (1972). DOI: 10.1103/PhysRevLett.28.1516
- B. Efron, *Bootstrap Methods: Another Look at the Jackknife*, Ann. Statist. 7(1), 1–26 (1979). DOI: 10.1214/aos/1176344552

## Filer

- run-level data: `v09_scale_run_rows.csv`
- group-level data: `v09_scale_group_rows.csv`
- candidate summary data: `v09_scale_candidate_summary.csv`
- ensemble summary data: `v09_scale_ensemble_summary.csv`
