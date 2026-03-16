# Relasjonell universgraf v0.8 – faseatlas, Paretofront og regimevalg

## Sammendrag

Dette dokumentet beskriver v0.8-steg i prosjektet: det første egentlige faseatlaset for den relasjonelle universgrafen etter at v0.7 etablerte lokal maksimal kobling som metodisk basis.

Målet i v0.8 er ikke å påstå at modellen allerede har skarpe faser i streng statistisk-mekanisk forstand. Målet er å gjøre noe mer beskjedent og mer nyttig: å kartlegge et eksplisitt kandidatrom og rangere regimer etter fire mål som prosjektet nå har identifisert som sentrale:

1. **repair / overlap** – hvor mye to nærliggende universgrener bevarer felles lokal struktur
2. **bounded causal spread** – hvor sterkt forskjellen holder seg innen en begrenset radius
3. **quasi-invariants** – hvor lite topologiske og charge-lignende makrovariabler divergerer
4. **geometry robustness** – hvor lite geometri-proksier som spektralradius, clustering og dimensjonsproxy divergerer

Det gir et reelt regimekart, men fortsatt et *heuristisk* et: grensene er operative og empiriske, ikke fundamentalteoretiske.

## Scan-design

- kandidat-slice: `p_del = 0`
- `r_birth ∈ {0.02, 0.05, 0.08}`
- `r_death ∈ {0.00, 0.02, 0.05}`
- `p_swap ∈ {0.02, 0.04, 0.06}`
- `p_triad ∈ {0.00, 0.02}`
- perturbasjon: `local_swap`
- kobling: `local_coupling = maximal`

Denne slicen er valgt bevisst. v0.7 pekte på et lovende område med lav `p_del`, lav til moderat `p_triad`, moderat `p_swap`, og moderat token-open dynamikk. v0.8 prøver derfor å kartlegge *nettopp* den delen av rommet mer disiplinert før vi utvider aksene igjen.

## De fire v0.8-scorefamiliene

For hvert gridpunkt ble det først aggregert over flere seeds. Deretter ble råmålene normalisert over hele coarse-scanet, og vi bygget fire samlescorer:

### 1. Repair-score

Bygget av høy `meeting`-rate, høy lokal overlap, høy same-descriptor-rate, høy delt token-/node-fraksjon og lav `unequal_time`.

### 2. Causal-score

Bygget av lav slutt-radius, lav estimert front-hastighet og lav slutt-edge-differanse.

### 3. Quasi-score

Bygget av liten absolutt divergens i `delta_beta1`, `delta_tokens`, `delta_nodes` og `delta_triangles`.

### 4. Geometry-score

Bygget av liten absolutt divergens i `delta_spectral_radius`, `delta_clustering` og `delta_dim_proxy`.

Til slutt ble det definert en vektet composite-score

```text
composite = 0.35 * repair + 0.25 * causal + 0.20 * quasi + 0.20 * geom
```

samt en Paretofront i det firedimensjonale score-rommet.

## Viktigste funn

- Beste coarse kandidat hadde `(r_birth, r_death, p_swap, p_triad)=(0.02, 0.02, 0.02, 0.00)`, composite ≈ 0.854, repair ≈ 0.910, causal ≈ 0.648.
- Paretofronten i coarse-scanet inneholdt 12 punkter. Det betyr at ingen enkelt regime dominerte alle fire mål samtidig.
- Høy repair og høy geometrirobusthet falt ikke helt sammen: beste repair-punkt og beste geom-punkt var ulike, noe som styrker bildet av et kompromiss mellom selvreparasjon og makrostabilitet.
- I den finere rerun-runden holdt topprankingen seg rundt samme region; beste refined kandidat hadde composite ≈ 0.932.

## Phase labels i coarse-scanet

| label | count |
| --- | --- |
| mixed | 33 |
| drift_dominant | 13 |
| macro_stable_weak_repair | 5 |
| repair_cone_candidate | 3 |

## Beste composite-regimer (coarse)

| r_birth | r_death | p_swap | p_triad | repair | causal | quasi | geom | composite | label | pareto |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.02 | 0.02 | 0.02 | 0 | 0.910 | 0.648 | 0.994 | 0.875 | 0.854 | mixed | 1 |
| 0.02 | 0.05 | 0.02 | 0 | 0.619 | 0.814 | 0.989 | 0.980 | 0.814 | macro_stable_weak_repair | 1 |
| 0.08 | 0.02 | 0.02 | 0 | 0.825 | 0.535 | 0.960 | 0.900 | 0.795 | mixed | 1 |
| 0.02 | 0 | 0.02 | 0 | 0.707 | 0.504 | 0.988 | 0.928 | 0.757 | mixed | 1 |
| 0.02 | 0.02 | 0.02 | 0.02 | 0.846 | 0.709 | 0.788 | 0.566 | 0.744 | repair_cone_candidate | 1 |
| 0.08 | 0 | 0.02 | 0.02 | 0.747 | 0.735 | 0.773 | 0.649 | 0.729 | repair_cone_candidate | 1 |
| 0.08 | 0 | 0.02 | 0 | 0.660 | 0.525 | 0.937 | 0.896 | 0.729 | mixed | 0 |
| 0.02 | 0.02 | 0.04 | 0.02 | 0.614 | 0.846 | 0.865 | 0.644 | 0.728 | mixed | 1 |

## Beste repair-regimer (coarse)

| r_birth | r_death | p_swap | p_triad | repair | causal | quasi | geom | composite | label | pareto |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.02 | 0.02 | 0.02 | 0 | 0.910 | 0.648 | 0.994 | 0.875 | 0.854 | mixed | 1 |
| 0.02 | 0.02 | 0.02 | 0.02 | 0.846 | 0.709 | 0.788 | 0.566 | 0.744 | repair_cone_candidate | 1 |
| 0.08 | 0.02 | 0.02 | 0 | 0.825 | 0.535 | 0.960 | 0.900 | 0.795 | mixed | 1 |
| 0.08 | 0 | 0.02 | 0.02 | 0.747 | 0.735 | 0.773 | 0.649 | 0.729 | repair_cone_candidate | 1 |
| 0.05 | 0.02 | 0.04 | 0 | 0.724 | 0.501 | 0.827 | 0.763 | 0.697 | mixed | 0 |
| 0.08 | 0 | 0.06 | 0.02 | 0.710 | 0.343 | 0.693 | 0.772 | 0.627 | mixed | 0 |
| 0.02 | 0 | 0.02 | 0 | 0.707 | 0.504 | 0.988 | 0.928 | 0.757 | mixed | 1 |
| 0.08 | 0.02 | 0.04 | 0 | 0.682 | 0.374 | 0.896 | 0.891 | 0.689 | mixed | 0 |

## Beste geometry-regimer (coarse)

| r_birth | r_death | p_swap | p_triad | repair | causal | quasi | geom | composite | label | pareto |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | 0 | 0.02 | 0 | 0.526 | 0.611 | 0.954 | 0.993 | 0.726 | macro_stable_weak_repair | 1 |
| 0.02 | 0.05 | 0.02 | 0 | 0.619 | 0.814 | 0.989 | 0.980 | 0.814 | macro_stable_weak_repair | 1 |
| 0.08 | 0.05 | 0.02 | 0 | 0.648 | 0.446 | 0.966 | 0.949 | 0.721 | mixed | 1 |
| 0.05 | 0 | 0.04 | 0 | 0.486 | 0.525 | 0.873 | 0.947 | 0.665 | mixed | 0 |
| 0.05 | 0.02 | 0.02 | 0 | 0.271 | 0.299 | 0.937 | 0.946 | 0.546 | macro_stable_weak_repair | 0 |
| 0.02 | 0 | 0.02 | 0 | 0.707 | 0.504 | 0.988 | 0.928 | 0.757 | mixed | 1 |
| 0.08 | 0.05 | 0.06 | 0 | 0.535 | 0.579 | 0.977 | 0.919 | 0.711 | macro_stable_weak_repair | 0 |
| 0.08 | 0.02 | 0.02 | 0 | 0.825 | 0.535 | 0.960 | 0.900 | 0.795 | mixed | 1 |

## Paretofront (coarse)

| r_birth | r_death | p_swap | p_triad | repair | causal | quasi | geom | composite | label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.02 | 0.02 | 0.02 | 0 | 0.910 | 0.648 | 0.994 | 0.875 | 0.854 | mixed |
| 0.02 | 0.05 | 0.02 | 0 | 0.619 | 0.814 | 0.989 | 0.980 | 0.814 | macro_stable_weak_repair |
| 0.08 | 0.02 | 0.02 | 0 | 0.825 | 0.535 | 0.960 | 0.900 | 0.795 | mixed |
| 0.02 | 0 | 0.02 | 0 | 0.707 | 0.504 | 0.988 | 0.928 | 0.757 | mixed |
| 0.02 | 0.02 | 0.02 | 0.02 | 0.846 | 0.709 | 0.788 | 0.566 | 0.744 | repair_cone_candidate |
| 0.08 | 0 | 0.02 | 0.02 | 0.747 | 0.735 | 0.773 | 0.649 | 0.729 | repair_cone_candidate |
| 0.02 | 0.02 | 0.04 | 0.02 | 0.614 | 0.846 | 0.865 | 0.644 | 0.728 | mixed |
| 0.05 | 0 | 0.02 | 0 | 0.526 | 0.611 | 0.954 | 0.993 | 0.726 | macro_stable_weak_repair |
| 0.08 | 0.05 | 0.02 | 0 | 0.648 | 0.446 | 0.966 | 0.949 | 0.721 | mixed |
| 0.02 | 0.02 | 0.06 | 0.02 | 0.645 | 0.744 | 0.770 | 0.693 | 0.704 | repair_cone_candidate |
| 0.05 | 0 | 0.06 | 0.02 | 0.659 | 0.680 | 0.744 | 0.730 | 0.695 | mixed |
| 0.05 | 0.02 | 0.06 | 0.02 | 0.621 | 0.780 | 0.777 | 0.637 | 0.695 | mixed |

## Coarse slice by `p_swap`

### p_swap = 0.02

| r_birth/r_death \ p_triad | 0 | 0.02 |
| --- | --- | --- |
| 0.02/0 | 0.76 | 0.55 |
| 0.02/0.02 | 0.85 | 0.74 |
| 0.02/0.05 | 0.81 | 0.57 |
| 0.05/0 | 0.73 | 0.68 |
| 0.05/0.02 | 0.55 | 0.49 |
| 0.05/0.05 | 0.56 | 0.48 |
| 0.08/0 | 0.73 | 0.73 |
| 0.08/0.02 | 0.79 | 0.66 |
| 0.08/0.05 | 0.72 | 0.45 |

### p_swap = 0.04

| r_birth/r_death \ p_triad | 0 | 0.02 |
| --- | --- | --- |
| 0.02/0 | 0.69 | 0.61 |
| 0.02/0.02 | 0.69 | 0.73 |
| 0.02/0.05 | 0.67 | 0.51 |
| 0.05/0 | 0.67 | 0.60 |
| 0.05/0.02 | 0.70 | 0.54 |
| 0.05/0.05 | 0.63 | 0.51 |
| 0.08/0 | 0.70 | 0.54 |
| 0.08/0.02 | 0.69 | 0.48 |
| 0.08/0.05 | 0.67 | 0.57 |

### p_swap = 0.06

| r_birth/r_death \ p_triad | 0 | 0.02 |
| --- | --- | --- |
| 0.02/0 | 0.71 | 0.61 |
| 0.02/0.02 | 0.63 | 0.70 |
| 0.02/0.05 | 0.63 | 0.43 |
| 0.05/0 | 0.58 | 0.70 |
| 0.05/0.02 | 0.57 | 0.70 |
| 0.05/0.05 | 0.70 | 0.67 |
| 0.08/0 | 0.68 | 0.63 |
| 0.08/0.02 | 0.73 | 0.66 |
| 0.08/0.05 | 0.71 | 0.68 |

## Refined rerun

Et lite utvalg av coarse-vinnerne ble rerunnet med flere seeds og lengre horisont. Hensikten var ikke full statistisk konvergens, men å sjekke om coarse-rangeringen var helt skjør.

## Beste composite-regimer (refined)

| r_birth | r_death | p_swap | p_triad | repair | causal | quasi | geom | composite | label | pareto |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.08 | 0.02 | 0.02 | 0 | 1.000 | 0.790 | 0.967 | 0.956 | 0.932 | repair_cone_candidate | 1 |
| 0.02 | 0.05 | 0.02 | 0 | 0.191 | 0.730 | 0.993 | 0.800 | 0.608 | mixed | 1 |
| 0.02 | 0 | 0.02 | 0 | 0.226 | 0.552 | 0.985 | 0.933 | 0.601 | mixed | 1 |
| 0.02 | 0.02 | 0.02 | 0 | 0.173 | 0.447 | 1.000 | 0.964 | 0.565 | macro_stable_weak_repair | 1 |
| 0.02 | 0.02 | 0.02 | 0.02 | 0.062 | 0.619 | 0.542 | 0.577 | 0.401 | drift_dominant | 0 |
| 0.08 | 0 | 0.02 | 0.02 | 0.278 | 0.388 | 0.000 | 0.000 | 0.194 | drift_dominant | 0 |


## Tolkning

v0.8 peker foreløpig mot et smalt bånd av **svakt til moderat åpne** regimer som de mest lovende kandidatene for videre arbeid. Disse regimene er verken helt lukkede eller sterkt åpne. De ser ut til å balansere fire ting samtidig:

- tilstrekkelig lokal repair til at to nærliggende grener ikke bare eksploderer fra hverandre
- tilstrekkelig bounded spread til at en causal-cone-lesning fortsatt gir mening
- tilstrekkelig quasi-invariant oppførsel til at makrovariabler ikke driver ukontrollert
- og tilstrekkelig geometrirobusthet til at dimensjonsproxy og relaterte observabler ikke er rent kaos

Dette er ikke et bevis på emergent spacetime. Det er derimot den hittil beste numeriske indikasjonen i prosjektet på *hvor* et slikt regime eventuelt må letes etter.

## Begrensninger

1. Dette er fortsatt et lite og lavdimensjonalt slice, ikke hele parameterrommet.
2. `p_del` ble holdt på 0 i v0.8 for å fokusere på den delen av rommet som v0.7 allerede antydet som lovende.
3. Faseetikettene er heuristiske og bør ikke forveksles med termodynamiske faser i streng forstand.
4. Confidence intervals og bootstrap over gridpunkter er ikke på plass ennå.

## Neste riktige steg etter v0.8

- utvide atlaset med en liten `p_del`-akse (`0, 0.01, 0.02`)
- legge på bootstrap/CI for topprankingen
- krysse atlaset mot energilaben, slik at `quasi` ikke bare betyr liten divergens mellom grener, men også liten drift i de beste makrovariablene innen hver gren
- og generere egentlige heatmaps/pareto-plott for rapportering

_Coarse aggregate CSV: `/mnt/data/v08_phase_atlas_coarse.csv`_

_Coarse run-level CSV: `/mnt/data/v08_phase_atlas_coarse_runs.csv`_

_Refined aggregate CSV: `/mnt/data/v08_phase_atlas_refined.csv`_

_Refined run-level CSV: `/mnt/data/v08_phase_atlas_refined_runs.csv`_
