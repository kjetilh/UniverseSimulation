# Relasjonell universgraf v0.8 – faseatlas, Paretofront og regimevalg

## Sammendrag

Dette dokumentet beskriver v0.8-steg i prosjektet: det første egentlige faseatlaset for den relasjonelle universgrafen etter at v0.7 etablerte lokal maksimal kobling som metodisk basis.

Målet i v0.8 er ikke å påstå at modellen allerede har skarpe faser i streng statistisk-mekanisk forstand. Målet er å gjøre noe mer beskjedent og mer nyttig: å kartlegge et eksplisitt kandidatrom og rangere regimer etter fire mål som prosjektet nå har identifisert som sentrale:

1. **repair / overlap** – hvor mye to nærliggende universgrener bevarer felles lokal struktur
2. **bounded causal spread** – hvor sterkt forskjellen holder seg innen en begrenset radius
3. **quasi-invariants** – hvor lite topologiske og charge-lignende makrovariabler divergerer
4. **geometry robustness** – hvor lite geometri-proksier som spektralradius, clustering og dimensjonsproxy divergerer

Det gir et reelt regimekart, men fortsatt et *heuristisk* et: grensene er operative og empiriske, ikke fundamentalteoretiske.

## Hva som er eksakt og hva som er heuristisk

- Eksakt: lokale rewrite-regler, familywise uniformization, maksimal lokal kobling og run-level observablene som skrives direkte fra simuleringen.
- Numerisk estimert: seed-aggregater, bootstrap-intervaller og relative scorer over gridet.
- Heuristisk: faseetiketter, composite-score og tolkningen av `geometry robustness` som en proxy snarere enn ekte geometri.

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

For hver run-aggregert størrelse beregnes det også bootstrap confidence intervals over seed-utvalget. Disse er nyttige som robusthetsindikatorer, men de gjør ikke fasegrensene skarpe.

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

- Beste coarse kandidat hadde `(r_birth, r_death, p_swap, p_triad)=(0.08, 0.02, 0.02, 0.00)`, composite ≈ 0.768, repair ≈ 0.766, causal ≈ 0.571.
- Paretofronten i coarse-scanet inneholdt 17 punkter. Det betyr at ingen enkelt regime dominerte alle fire mål samtidig.
- Høy repair og høy geometrirobusthet falt ikke helt sammen: beste repair-punkt og beste geom-punkt var ulike, noe som styrker bildet av et kompromiss mellom selvreparasjon og makrostabilitet.
- I den finere rerun-runden holdt topprankingen seg rundt samme region; beste refined kandidat hadde composite ≈ 0.912.

## Phase labels i coarse-scanet

| label | count |
| --- | --- |
| mixed | 32 |
| drift_dominant | 14 |
| macro_stable_weak_repair | 6 |
| repair_cone_candidate | 2 |

## Beste composite-regimer (coarse)

| r_birth | r_death | p_swap | p_triad | p_del | repair | causal | quasi | geom | composite | label | pareto |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.08 | 0.02 | 0.02 | 0 | 0 | 0.766 | 0.571 | 0.936 | 0.852 | 0.768 | mixed | 1 |
| 0.05 | 0 | 0.02 | 0.02 | 0 | 0.807 | 0.724 | 0.781 | 0.708 | 0.761 | repair_cone_candidate | 1 |
| 0.08 | 0 | 0.06 | 0 | 0 | 0.824 | 0.476 | 0.924 | 0.832 | 0.758 | mixed | 1 |
| 0.02 | 0.02 | 0.02 | 0 | 0 | 0.552 | 0.707 | 1.000 | 0.895 | 0.749 | macro_stable_weak_repair | 1 |
| 0.02 | 0 | 0.02 | 0 | 0 | 0.581 | 0.612 | 0.988 | 0.877 | 0.729 | macro_stable_weak_repair | 1 |
| 0.02 | 0.05 | 0.02 | 0 | 0 | 0.369 | 0.827 | 0.991 | 0.933 | 0.721 | macro_stable_weak_repair | 1 |
| 0.02 | 0 | 0.06 | 0 | 0 | 0.520 | 0.693 | 0.958 | 0.830 | 0.713 | mixed | 0 |
| 0.05 | 0 | 0.02 | 0 | 0 | 0.589 | 0.520 | 0.943 | 0.933 | 0.711 | macro_stable_weak_repair | 1 |

## Beste repair-regimer (coarse)

| r_birth | r_death | p_swap | p_triad | p_del | repair | causal | quasi | geom | composite | label | pareto |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.08 | 0 | 0.04 | 0.02 | 0 | 0.860 | 0.429 | 0.607 | 0.495 | 0.629 | mixed | 1 |
| 0.08 | 0 | 0.06 | 0 | 0 | 0.824 | 0.476 | 0.924 | 0.832 | 0.758 | mixed | 1 |
| 0.08 | 0.02 | 0.04 | 0.02 | 0 | 0.821 | 0.555 | 0.647 | 0.570 | 0.670 | mixed | 1 |
| 0.05 | 0 | 0.02 | 0.02 | 0 | 0.807 | 0.724 | 0.781 | 0.708 | 0.761 | repair_cone_candidate | 1 |
| 0.08 | 0.02 | 0.02 | 0 | 0 | 0.766 | 0.571 | 0.936 | 0.852 | 0.768 | mixed | 1 |
| 0.05 | 0.02 | 0.02 | 0.02 | 0 | 0.737 | 0.439 | 0.752 | 0.626 | 0.643 | mixed | 0 |
| 0.08 | 0 | 0.02 | 0.02 | 0 | 0.707 | 0.704 | 0.627 | 0.580 | 0.665 | repair_cone_candidate | 0 |
| 0.08 | 0 | 0.06 | 0.02 | 0 | 0.672 | 0.434 | 0.692 | 0.745 | 0.631 | mixed | 0 |

## Beste geometry-regimer (coarse)

| r_birth | r_death | p_swap | p_triad | p_del | repair | causal | quasi | geom | composite | label | pareto |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | 0.02 | 0.02 | 0 | 0 | 0.557 | 0.451 | 0.955 | 0.948 | 0.688 | macro_stable_weak_repair | 1 |
| 0.05 | 0 | 0.02 | 0 | 0 | 0.589 | 0.520 | 0.943 | 0.933 | 0.711 | macro_stable_weak_repair | 1 |
| 0.02 | 0.05 | 0.02 | 0 | 0 | 0.369 | 0.827 | 0.991 | 0.933 | 0.721 | macro_stable_weak_repair | 1 |
| 0.05 | 0.05 | 0.04 | 0 | 0 | 0.331 | 0.638 | 0.878 | 0.920 | 0.635 | mixed | 0 |
| 0.08 | 0 | 0.02 | 0 | 0 | 0.666 | 0.428 | 0.935 | 0.905 | 0.708 | mixed | 1 |
| 0.05 | 0 | 0.04 | 0 | 0 | 0.517 | 0.478 | 0.906 | 0.899 | 0.661 | mixed | 0 |
| 0.08 | 0.05 | 0.02 | 0 | 0 | 0.535 | 0.499 | 0.915 | 0.895 | 0.674 | mixed | 0 |
| 0.02 | 0.02 | 0.02 | 0 | 0 | 0.552 | 0.707 | 1.000 | 0.895 | 0.749 | macro_stable_weak_repair | 1 |

## Paretofront (coarse)

| r_birth | r_death | p_swap | p_triad | p_del | repair | causal | quasi | geom | composite | label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.08 | 0.02 | 0.02 | 0 | 0 | 0.766 | 0.571 | 0.936 | 0.852 | 0.768 | mixed |
| 0.05 | 0 | 0.02 | 0.02 | 0 | 0.807 | 0.724 | 0.781 | 0.708 | 0.761 | repair_cone_candidate |
| 0.08 | 0 | 0.06 | 0 | 0 | 0.824 | 0.476 | 0.924 | 0.832 | 0.758 | mixed |
| 0.02 | 0.02 | 0.02 | 0 | 0 | 0.552 | 0.707 | 1.000 | 0.895 | 0.749 | macro_stable_weak_repair |
| 0.02 | 0 | 0.02 | 0 | 0 | 0.581 | 0.612 | 0.988 | 0.877 | 0.729 | macro_stable_weak_repair |
| 0.02 | 0.05 | 0.02 | 0 | 0 | 0.369 | 0.827 | 0.991 | 0.933 | 0.721 | macro_stable_weak_repair |
| 0.05 | 0 | 0.02 | 0 | 0 | 0.589 | 0.520 | 0.943 | 0.933 | 0.711 | macro_stable_weak_repair |
| 0.08 | 0 | 0.02 | 0 | 0 | 0.666 | 0.428 | 0.935 | 0.905 | 0.708 | mixed |
| 0.05 | 0.02 | 0.02 | 0 | 0 | 0.557 | 0.451 | 0.955 | 0.948 | 0.688 | macro_stable_weak_repair |
| 0.08 | 0.02 | 0.04 | 0.02 | 0 | 0.821 | 0.555 | 0.647 | 0.570 | 0.670 | mixed |
| 0.05 | 0 | 0.04 | 0.02 | 0 | 0.575 | 0.799 | 0.712 | 0.603 | 0.664 | mixed |
| 0.08 | 0.05 | 0.06 | 0.02 | 0 | 0.639 | 0.603 | 0.710 | 0.713 | 0.659 | mixed |
| 0.05 | 0.02 | 0.06 | 0.02 | 0 | 0.587 | 0.799 | 0.730 | 0.541 | 0.659 | mixed |
| 0.02 | 0.02 | 0.04 | 0.02 | 0 | 0.407 | 0.767 | 0.881 | 0.696 | 0.650 | mixed |
| 0.08 | 0 | 0.04 | 0.02 | 0 | 0.860 | 0.429 | 0.607 | 0.495 | 0.629 | mixed |
| 0.05 | 0.05 | 0.06 | 0.02 | 0 | 0.471 | 0.804 | 0.630 | 0.655 | 0.623 | mixed |
| 0.02 | 0 | 0.06 | 0.02 | 0 | 0.484 | 0.864 | 0.556 | 0.486 | 0.594 | mixed |

## Coarse slice by `p_swap`

### p_swap = 0.02

| r_birth/r_death \ p_triad | 0 | 0.02 |
| --- | --- | --- |
| 0.02/0 | 0.73 | 0.51 |
| 0.02/0.02 | 0.75 | 0.65 |
| 0.02/0.05 | 0.72 | 0.56 |
| 0.05/0 | 0.71 | 0.76 |
| 0.05/0.02 | 0.69 | 0.64 |
| 0.05/0.05 | 0.56 | 0.38 |
| 0.08/0 | 0.71 | 0.67 |
| 0.08/0.02 | 0.77 | 0.54 |
| 0.08/0.05 | 0.67 | 0.39 |

### p_swap = 0.04

| r_birth/r_death \ p_triad | 0 | 0.02 |
| --- | --- | --- |
| 0.02/0 | 0.66 | 0.59 |
| 0.02/0.02 | 0.68 | 0.65 |
| 0.02/0.05 | 0.62 | 0.42 |
| 0.05/0 | 0.66 | 0.66 |
| 0.05/0.02 | 0.65 | 0.55 |
| 0.05/0.05 | 0.63 | 0.56 |
| 0.08/0 | 0.65 | 0.63 |
| 0.08/0.02 | 0.63 | 0.67 |
| 0.08/0.05 | 0.65 | 0.58 |

### p_swap = 0.06

| r_birth/r_death \ p_triad | 0 | 0.02 |
| --- | --- | --- |
| 0.02/0 | 0.71 | 0.59 |
| 0.02/0.02 | 0.61 | 0.59 |
| 0.02/0.05 | 0.60 | 0.36 |
| 0.05/0 | 0.55 | 0.65 |
| 0.05/0.02 | 0.58 | 0.66 |
| 0.05/0.05 | 0.67 | 0.62 |
| 0.08/0 | 0.76 | 0.63 |
| 0.08/0.02 | 0.66 | 0.61 |
| 0.08/0.05 | 0.69 | 0.66 |

## Refined rerun

Et lite utvalg av coarse-vinnerne ble ikke bare rerunnet; de ble utvidet til lokale nabolag i parameterrommet. Denne refinement-runden åpner også en liten `p_del`-akse for å teste robusthet mot svak sletting.

## Beste composite-regimer (refined)

| r_birth | r_death | p_swap | p_triad | p_del | repair | causal | quasi | geom | composite | label | pareto |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.09 | 0.02 | 0.02 | 0 | 0.02 | 0.914 | 0.868 | 0.953 | 0.922 | 0.912 | spacetime_candidate | 1 |
| 0.07 | 0.01 | 0.02 | 0 | 0 | 0.892 | 0.689 | 0.991 | 0.923 | 0.867 | spacetime_candidate | 1 |
| 0.08 | 0.03 | 0.02 | 0 | 0 | 0.875 | 0.716 | 0.954 | 0.954 | 0.867 | spacetime_candidate | 1 |
| 0.09 | 0.03 | 0.02 | 0 | 0.02 | 0.914 | 0.731 | 0.895 | 0.894 | 0.860 | mixed | 0 |
| 0.09 | 0.02 | 0.02 | 0 | 0.01 | 0.774 | 0.891 | 0.836 | 0.959 | 0.853 | spacetime_candidate | 1 |
| 0.07 | 0.03 | 0.02 | 0 | 0 | 0.880 | 0.695 | 0.943 | 0.906 | 0.852 | mixed | 0 |


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
4. Confidence intervals i denne versjonen er bootstrap over seeds per gridpunkt. De er nyttige, men begrenset av lite antall runs og bør ikke forveksles med en full usikkerhetsanalyse over hele atlaset.

## Neste riktige steg etter v0.8

- utvide atlaset med en liten `p_del`-akse (`0, 0.01, 0.02`)
- legge på bootstrap/CI for topprankingen
- krysse atlaset mot energilaben, slik at `quasi` ikke bare betyr liten divergens mellom grener, men også liten drift i de beste makrovariablene innen hver gren
- og generere egentlige heatmaps/pareto-plott for rapportering

_Coarse aggregate CSV: `Documentation/v08_phase_atlas_coarse.csv`_

_Coarse run-level CSV: `Documentation/v08_phase_atlas_coarse_runs.csv`_

_Refined aggregate CSV: `Documentation/v08_phase_atlas_refined.csv`_

_Refined run-level CSV: `Documentation/v08_phase_atlas_refined_runs.csv`_

_Coarse Paretofront CSV: `Documentation/v08_phase_atlas_coarse_frontier.csv`_

_Refined Paretofront CSV: `Documentation/v08_phase_atlas_refined_frontier.csv`_
