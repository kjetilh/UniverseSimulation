# Relasjonell universgraf v0.10f: frontier-runde rundt band_zero_del og band_small_triad

## 1. Formål

v0.10e endte med en todelt operativ front:

- `band_zero_del`, som vant på rå `mean_composite` og bootstrap-sannsynlighet.
- `band_small_triad`, som fortsatt lå nær nok til at det ikke var forsvarlig å låse prosjektet til én standardkandidat.

Neste riktige steg var derfor en ren frontier-runde med tre metodiske krav:

1. holde generatoren fast på `fast_balanced / deep`,
2. øke growth-seed-variasjonen i en smal lokal scan,
3. bruke ekstra run-seed-replikasjon på ankerparet og beste brede utfordrer.

Målet var å avgjøre om den gamle todelte fronten holder seg, om den smelter sammen til én vinner, eller om en tredje lokal nabo overtar.

## 2. Oppsett

### 2.1 Generator og ensembler

Generatorregimet ble holdt fast på `fast_balanced / deep`.
Det er viktig, fordi v0.10b–v0.10d viste at generatorartefakter ellers kunne dominere hele tolkningen.

Brukte mål-størrelser:

- 48
- 96
- 192
- 256

Med 4 growth seeds traff alle disse nivåene eksakt i denne runden:

| target | mean initial nodes | sd | q10 | q90 | separated_from_prev |
| --- | ---: | ---: | ---: | ---: | ---: |
| 48 | 48.0 | 0.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 0.0 | 96.0 | 96.0 | 1 |
| 192 | 192.0 | 0.0 | 192.0 | 192.0 | 1 |
| 256 | 256.0 | 0.0 | 256.0 | 256.0 | 1 |

Dette er metodisk viktig: v0.10f er i praksis en **dynamisk** frontier-test, ikke en generator-test.

### 2.2 Kandidater i bred frontier-scan

Den brede scanen brukte 7 kandidater:

- `band_zero_del` = `(p_swap, p_triad, p_del) = (0.02, 0.00, 0.00)`
- `frontier_diag_mid` = `(0.02, 0.005, 0.005)`
- `band_small_triad` = `(0.02, 0.010, 0.010)`
- `band_best` = `(0.02, 0.000, 0.010)` som historisk referanse
- `frontier_triad_only` = `(0.02, 0.010, 0.000)`
- `frontier_zero_del_swap025` = `(0.025, 0.000, 0.000)`
- `frontier_small_triad_swap015` = `(0.015, 0.010, 0.010)`

Alle med `r_birth = 0.02` og `r_death = 0.00`.

### 2.3 Replikasjon

Bred scan:

- 4 growth seeds
- 3 run seeds per growth seed

Dette ga 12 coupled-run-replikater per ensemble per kandidat.

Finalefelt:

- ankerparet `band_zero_del`, `band_small_triad`
- pluss beste brede utfordrer etter `focused_score`
- ekstra run-seed-replikasjon til totalt 4 run seeds per growth seed

## 3. Resultater fra bred frontier-scan

| candidate | focused score | mean composite | CI low composite | top prob | alpha_large | alpha_jump | linear_margin | quasi_large |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `frontier_diag_mid` | 0.672 | 0.578 | 0.517 | 0.017 | 0.055 | -0.057 | 0.091 | -0.094 |
| `frontier_zero_del_swap025` | 0.621 | 0.658 | 0.589 | 0.211 | 0.161 | -0.081 | 0.120 | -0.143 |
| `frontier_triad_only` | 0.598 | 0.582 | 0.522 | 0.011 | 0.162 | -0.060 | 0.008 | 0.088 |
| `band_zero_del` | 0.480 | 0.686 | 0.628 | 0.566 | 0.345 | 0.026 | -0.059 | -0.178 |
| `band_best` | 0.426 | 0.382 | 0.381 | 0.000 | 0.095 | -0.084 | 0.074 | -0.151 |
| `band_small_triad` | 0.400 | 0.421 | 0.390 | 0.000 | -0.031 | -0.064 | 0.021 | -0.358 |
| `frontier_small_triad_swap015` | 0.267 | 0.648 | 0.583 | 0.194 | 0.316 | 0.103 | 0.008 | -0.328 |

### 3.1 Første tolkning

Dette er den første virkelig viktige endringen i v0.10f:

- `band_small_triad` holder **ikke** posisjonen sin fra v0.10e.
- En ny lokal nabo, `frontier_diag_mid`, overtar som beste kandidat på `focused_score`.
- `band_zero_del` holder fortsatt klart best rå `mean_composite`.

Dermed får vi ikke lenger en ren todeling mellom de to gamle ankerne. Fronten **reorganiserer** seg til en ny spenning mellom:

- `band_zero_del` som **repair/composite-vinner**, og
- `frontier_diag_mid` som **asymptotic/focused-score-vinner**.

## 4. Finalefelt med ekstra run-seeds

Finalistene ble:

- `band_zero_del`
- `band_small_triad`
- `frontier_diag_mid`

Resultatene etter ekstra run-seeds:

| candidate | focused score | mean composite | CI low composite | top prob | alpha_large | alpha_jump | linear_margin | quasi_large |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `frontier_diag_mid` | 0.714 | 0.585 | 0.515 | 0.209 | 0.087 | -0.064 | 0.058 | -0.157 |
| `band_zero_del` | 0.666 | 0.637 | 0.575 | 0.791 | 0.251 | -0.021 | 0.049 | -0.132 |
| `band_small_triad` | 0.382 | 0.386 | 0.353 | 0.000 | 0.102 | 0.011 | 0.039 | -0.283 |

Pairwise bootstrap-sannsynligheter i finalefeltet:

| a | b | P(a > b) på mean composite |
| --- | --- | ---: |
| `band_zero_del` | `frontier_diag_mid` | 0.791 |
| `frontier_diag_mid` | `band_zero_del` | 0.209 |
| `band_zero_del` | `band_small_triad` | 1.000 |
| `frontier_diag_mid` | `band_small_triad` | 0.991 |

### 4.1 Hva dette betyr

Dette er kjernen i v0.10f:

1. **`band_small_triad` faller ut av den operative fronten.**
   Den er ikke lenger en plausibel medvinner i dette regimet.

2. **`band_zero_del` er fortsatt den beste kandidaten på rå ytelse.**
   Den har høyest `mean_composite`, høyest `CI low composite`, og vinner 79.1 % av bootstrap-sammenligningene mot `frontier_diag_mid`.

3. **`frontier_diag_mid` er nå beste kandidat på asymptotisk disiplin.**
   Den har klart lavere `alpha_large`, mer negativ og stabil `alpha_jump`, og høyest `focused_score`.

4. **Fronten er derfor ikke lenger “zero_del vs small_triad”.**
   Den er nå en **tension frontier** mellom:
   - en rå dynamisk vinner (`band_zero_del`), og
   - en mer asymptotisk/strukturert vinner (`frontier_diag_mid`).

## 5. Størrelsesprofiler

### 5.1 `band_zero_del`

- radius: 5.00, 6.50, 7.50, 8.75
- overlap faller fra 0.668 til 0.542
- quasi faller fra 1.000 til 0.695
- composite faller fra 0.869 til 0.430

Dette er fortsatt sterk rå ytelse, men skalaoppførselen er ikke spesielt “ren”.

### 5.2 `frontier_diag_mid`

- radius: 5.81, 7.25, 7.19, 8.19
- overlap holder seg relativt høyt
- quasi faller mindre dramatisk enn for `band_small_triad`
- composite er jevnere enn hos `band_small_triad`, men svakere enn `band_zero_del`

Dette er mer i tråd med hvorfor `focused_score` foretrekker den: ikke fordi den er best på alt, men fordi den ser mer disiplinert ut på stor skala.

### 5.3 `band_small_triad`

- radius og overlap er ustabile over nivåene
- quasi kollapser sterkt ved 192 og blir bare delvis bedre ved 256
- composite havner klart under de to andre finalistene

Det er derfor metodisk riktig å flytte `band_small_triad` ut av fronten og ned til kontroll-/referansestatus.

## 6. Metodisk dom

v0.10f er et godt forskningstegn av tre grunner.

### 6.1 Fronten ble ikke bevart av vane

Den gamle v0.10e-fronten overlevde ikke uendret. Det er bra. Det betyr at prosjektet ikke bare gjentar sine gamle vinnere når testene blir strengere.

### 6.2 Generatorproblemet er ikke lenger hovedforklaringen

De realiserte startstørrelsene traff 48, 96, 192 og 256 eksakt med null seed-spredning i denne runden. Resultatene er derfor primært dynamiske, ikke generatordrevne.

### 6.3 Vi har fått en skarpere type usikkerhet

Usikkerheten er nå ikke “er dette bare et artefakt?”.
Den er mer interessant:

> Hvilken type vinner ønsker prosjektet å optimalisere mot?
>
> - høyest rå repair/composite-ytelse,
> - eller mer disiplinert asymptotisk/geom-messig oppførsel?

Det er et bedre sted å være metodisk.

## 7. Operativ konklusjon

### 7.1 Hva som ikke lenger bør sies

- `band_small_triad` bør ikke lenger omtales som del av den operative fronten.
- `band_best` bør fortsatt bare brukes som historisk referanse.

### 7.2 Hva som bør sies nå

Den operative fronten i v0.10f er:

- `band_zero_del` som **raw winner**
- `frontier_diag_mid` som **asymptotic winner**

### 7.3 Hva som bør testes neste gang

v0.11 bør ikke være et bredt atlas. Det bør være en **frontier resolution round** mellom disse to kandidatfamiliene.

Det mest naturlige neste oppsettet er:

1. hold `fast_balanced / deep` fast,
2. bruk flere growth seeds og flere run seeds,
3. finprøv lokalt rundt punktene:
   - `(p_triad, p_del) = (0.000, 0.000)`
   - `(0.0025, 0.0025)`
   - `(0.0050, 0.0050)`
   - eventuelt blandede punkt som `(0.0025, 0.0000)` og `(0.0050, 0.0025)`
4. test også en liten `p_swap`-akse rundt 0.02 og 0.025 for zero-del-familien.

Det rette spørsmålet videre er ikke lenger “holder small_triad seg?”, men:

> Er `frontier_diag_mid` en genuin asymptotisk forbedring,
> eller er den bare en lokal kompromisskandidat som taper når replikasjonen blir enda høyere?

## 8. Kort dom

v0.10f gjorde akkurat det en moden forskningskodebase bør gjøre:

- den renset fronten videre,
- den tok ut en gammel kandidat,
- og den erstattet en enkel vinnerfortelling med en skarpere og mer nyttig spenning mellom to forskjellige typer styrke.

Det gjør prosjektet bedre, ikke svakere.
