# Relasjonell universgraf v0.9b – asymptotisk refinering og finite-size-artefakter

## Sammendrag

v0.9b tar det neste metodisk riktige steget etter v0.9: i stedet for bare å spørre hvilke kandidater som gjør det bra på større naturlige ensembler, spør vi om de fortsatt ser gode ut når vi leser resultatene **asymptotisk**.

Dette steget gjør fem ting samtidig:

1. holder fast ved det fokuserte kandidatbåndet fra v0.9,
2. utvider naturlige ensembler opp til 192-nivå,
3. bruker samme type naturlig vekst og light/deep burn-in som før,
4. estimerer asymptotiske indikatorer for radius/front, repair og quasi-invariants,
5. prøver å skille mellom reell sublineær frontvekst og **finite-size-artefakter**.

Den viktigste konklusjonen er at v0.9-vinneren **ikke** forblir best under denne strengere testen. Det er et godt tegn metodisk, fordi det betyr at rammeverket nå er sterkt nok til å avsløre når et regime bare ser pent ut på moderate størrelser.

## Metode

- kandidater testet: 4
- naturlige ensembler: 8
- størrelsesnivåer: 24, 48, 96, 192
- burn-in-regimer: light og deep på hvert nivå
- growth seeds i hovedscan: 2 (`101`, `202`)
- event-budsjett: `steps = clamp(round(4.5 * N_init), 120, 650)`
- bootstrap-replikater for asymptotiske kandidatintervaller: 80
- lokal refinering: 1 ekstra growth seed (`303`) for de to beste asymptotiske kandidatene

## Startensembler

| ensemble | target | burn-in | mean nodes | mean tokens | mean β1 | mean spectral radius | mean dim proxy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| natural24_light | 24 | light | 27.5 | 5.0 | 3.0 | 3.21 | 2.22 |
| natural24_deep | 24 | deep | 35.0 | 8.0 | 5.0 | 3.64 | 2.13 |
| natural48_light | 48 | light | 45.0 | 15.0 | 8.0 | 4.04 | 2.34 |
| natural48_deep | 48 | deep | 58.5 | 15.0 | 12.5 | 4.29 | 2.85 |
| natural96_light | 96 | light | 78.5 | 15.5 | 15.5 | 4.36 | 2.88 |
| natural96_deep | 96 | deep | 91.0 | 29.5 | 23.0 | 5.05 | 3.03 |
| natural192_light | 192 | light | 138.5 | 39.5 | 37.0 | 4.81 | 2.97 |
| natural192_deep | 192 | deep | 153.0 | 80.5 | 59.0 | 5.69 | 2.98 |

## Nye asymptotiske indikatorer

v0.9b introduserer fire indikatorer som er ment å fange opp finite-size-risiko mer direkte enn v0.9 gjorde.

### 1. `alpha_large`

Log-log-helningen for `(radius + 1)` mot `N`, men bare på de tre største størrelsene.

- Lav verdi er bra.
- Høy verdi betyr at perturbasjonsfronten vokser raskt på stor skala.
- Hvis `alpha_large` er mye større enn all-skalaestimatet, er det et advarselssignal.

### 2. `alpha_jump`

Definert som:

`alpha_jump = alpha_large - alpha_all`

- Hvis denne er nær null eller negativ, er det et tegn på at stor-skala oppførsel ikke blir verre enn all-skala oppførsel.
- Hvis den er klart positiv, kan lav all-skala-eksponent være en finite-size-illusjon.

### 3. `linear_margin`

Definert som:

`RMSE(linear-in-N fit) - best(RMSE(logN fit), RMSE(sqrtN fit))`

- Positiv verdi betyr at en enkel sublineær familie passer radius bedre enn lineær vekst.
- Negativ verdi betyr at lineær vekst faktisk beskriver dataene like godt eller bedre.

### 4. `quasi_large`

Stor-skala-helning for quasi-score mot `log N`.

- Mindre negativ er bedre.
- Kraftig negativ verdi betyr at quasi-invariant-bevaringen brytes raskt ned når størrelsen øker.

## Kandidatsammendrag

| candidate | r_birth | r_death | p_swap | p_triad | p_del | mean composite | CI low | alpha_large | alpha_jump | linear margin | asym score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| band_best | 0.02 | 0.00 | 0.02 | 0.00 | 0.01 | 0.623 | 0.568 | 0.303 | 0.025 | 0.059 | 0.810 |
| macro_stable | 0.02 | 0.05 | 0.02 | 0.00 | 0.01 | 0.608 | 0.598 | 0.237 | 0.263 | 0.007 | 0.689 |
| triad_runner | 0.02 | 0.02 | 0.02 | 0.02 | 0.00 | 0.520 | 0.541 | 0.898 | 0.373 | -0.092 | 0.446 |
| balanced_pdel | 0.02 | 0.02 | 0.02 | 0.00 | 0.01 | 0.644 | 0.614 | 1.266 | 0.742 | -0.103 | 0.333 |

## Hovedfunn

### 1. `band_best` blir asymptotisk vinner

`band_best` var ikke v0.9-vinneren på rå composite, men kommer ut som best i v0.9b når finite-size-risiko tas eksplisitt med.

Hovedtall i hovedscan:

- mean composite ≈ 0.623
- bootstrap lower bound ≈ 0.568
- `alpha_large` ≈ 0.303
- `alpha_jump` ≈ 0.025
- `linear_margin` ≈ 0.059
- asymptotic score ≈ 0.810

Det er spesielt viktig at:

- `alpha_jump` er svært liten
- `linear_margin` er positiv
- den lokale radiusveksten er jevn

Dette er akkurat den typen profil man ønsker hvis man prøver å identifisere et regime med ekte sublineær frontvekst.

### 2. `balanced_pdel` ser nå mer ut som en finite-size-vinner

I v0.9 så `balanced_pdel` sterk ut. I v0.9b får vi derimot:

- `alpha_large` ≈ 1.266
- `alpha_jump` ≈ 0.742
- `linear_margin` ≈ -0.103

Det betyr at stor-skala-fronten vokser langt raskere enn all-skalaestimatet antydet, og at lineær vekst faktisk beskriver radius minst like godt som de enkle sublineære familiene vi testet.

Dette er den skarpeste enkeltobservasjonen i v0.9b:
**noe av det som så best ut i v0.9 ser nå ut til å ha vært delvis et finite-size-fenomen.**

### 3. `macro_stable` holder seg som en seriøs kontrollkandidat

`macro_stable` har:

- `alpha_large` ≈ 0.237
- `alpha_jump` ≈ 0.263
- `linear_margin` ≈ 0.007

Den er ikke like ren som `band_best`, men heller ikke like problematisk som `balanced_pdel`. Den fungerer derfor godt som kontrollregime: et kandidatpunkt som fortsatt er interessant, men mindre asymptotisk overbevisende.

### 4. `triad_runner` faller tilbake

`triad_runner` får:

- `alpha_large` ≈ 0.898
- `alpha_jump` ≈ 0.373
- `linear_margin` ≈ -0.092

Det er dårligere enn `band_best` og `macro_stable` på de indikatorene som nettopp skulle fange opp finite-size-risiko.

## Størrelsesprofiler

### `band_best`

| target | mean initial N | mean radius | mean overlap | mean quasi | mean composite | |Δβ1| |
| --- | --- | --- | --- | --- | --- | --- |
| 24 | 31.2 | 3.25 | 0.560 | 0.719 | 0.605 | 0.000 |
| 48 | 51.8 | 3.75 | 0.840 | 0.750 | 0.807 | 0.250 |
| 96 | 84.8 | 4.50 | 0.649 | 0.531 | 0.494 | 0.500 |
| 192 | 145.8 | 5.50 | 0.842 | 0.562 | 0.585 | 0.750 |

### `balanced_pdel`

| target | mean initial N | mean radius | mean overlap | mean quasi | mean composite | |Δβ1| |
| --- | --- | --- | --- | --- | --- | --- |
| 24 | 31.2 | 3.25 | 0.568 | 0.714 | 0.609 | 0.000 |
| 48 | 51.8 | 1.00 | 0.916 | 0.938 | 0.894 | 0.000 |
| 96 | 84.8 | 4.25 | 0.735 | 0.543 | 0.546 | 1.000 |
| 192 | 145.8 | 6.50 | 0.842 | 0.405 | 0.528 | 1.000 |

Kontrasten mellom disse to profilene er instruktiv:

- `band_best` vokser jevnere i radius når skalaen øker.
- `balanced_pdel` får en langt skarpere stor-skala oppbremsing/oppblåsing i fittene, som slår ut i høy `alpha_large` og høy `alpha_jump`.

## Lokal refinering med ekstra growth seed

Etter hovedscanet kjørte vi en lokal refinering på de to mest interessante kandidatene med én ekstra growth seed.

| candidate | refine seeds | mean composite | CI low | alpha_large | alpha_jump | linear_margin | burn-in sens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| band_best | 101,202,303 | 0.591 | 0.558 | 0.141 | -0.082 | 0.111 | 0.155 |
| macro_stable | 101,202,303 | 0.604 | 0.576 | 0.406 | 0.287 | -0.038 | 0.222 |

Dette er kanskje det mest interessante sekundærfunnet i v0.9b:

- `band_best` blir **enda mer** asymptotisk konsistent under lokal refinering:
  - `alpha_large` faller til ≈ 0.141
  - `alpha_jump` blir negativ, ≈ -0.082
  - `linear_margin` øker til ≈ 0.111

- `macro_stable` holder seg brukbar, men ser svakere ut enn `band_best`:
  - `alpha_large` ≈ 0.406
  - `alpha_jump` ≈ 0.287
  - `linear_margin` ≈ -0.038

Så den lokale refineringen styrker ikke bare `band_best`; den styrker også tolkningen av at det faktisk er **den** kandidaten som best overlever asymptotikk-testen i denne runden.

## Tolkning

v0.9b viser tre ting som er viktige for prosjektet som helhet.

### A. Prosjektet går fortsatt i riktig retning

Når testen ble strengere, kollapset ikke hele kandidatrommet. I stedet:

- noen kandidater falt tilbake,
- noen holdt seg middels interessante,
- ett regime ble tydeligere.

Det er et sunt tegn i tidlig modellutvikling.

### B. Vi har nå et bedre skille mellom “vakre småsystemer” og mer robuste regimer

Det er lett å få pen oppførsel på små eller moderate ensembler. Det er langt vanskeligere å få noe som fortsatt ser kontrollert ut når man:

- øker naturlig størrelse,
- varierer burn-in,
- og leser av stor-skala eksponenter.

v0.9b er første steg der prosjektet virkelig begynner å gjøre dette skillet eksplisitt.

### C. Asymptotisk robusthet er nå et eget seleksjonskriterium

Før v0.9b kunne et regime vinne på composite-score alene. Etter v0.9b må en kandidat også overleve:

- `alpha_large`
- `alpha_jump`
- `linear_margin`
- stor-skala quasi-driftsignal

Det gjør utvelgelsen mer fysisk interessant, selv om vi fortsatt bare er i en tidlig, eksplorativ fase.

## Hvor vi er nå

Prosjektet står nå omtrent her:

1. Vi har etablert at modellen kan produsere naturlig voksende ensembler.
2. Vi har identifisert et smalt kandidatbånd som ser bedre ut enn resten.
3. Vi har nå vist at dette båndet **ikke er homogent**:
   - noen kandidater ser ut til å være finite-size-vinnere,
   - andre ser mer asymptotisk troverdige ut.
4. Per nå er `band_best` den mest interessante kandidaten.

Det betyr ikke at vi har en fysisk teori.
Det betyr at vi nå har et langt bedre definert **arbeidsregime**.

## Neste riktige steg

Det naturlige neste steget etter v0.9b er v0.10:

1. større naturlige ensembler (for eksempel 256 og 384),
2. flere growth seeds på toppkandidatene,
3. eksplisitt forsøk på enkel data collapse / skaleringskollaps,
4. bedre skille mellom ekte asymptotisk sublinearitet og “pre-asymptotisk” transient struktur.

## Metodereferanser

Dette steget er inspirert av klassisk finite-size scaling og bootstrap-logikk, selv om systemet her ikke er et standard gittersystem:

- M. E. Fisher og M. N. Barber, *Scaling Theory for Finite-Size Effects in the Critical Region*, Phys. Rev. Lett. 28, 1516 (1972). DOI: 10.1103/PhysRevLett.28.1516
- M. Suzuki, *Static and Dynamic Finite-Size Scaling Theory Based on the Renormalization Group Approach*, Prog. Theor. Phys. 58(4), 1142–1150 (1977). DOI: 10.1143/PTP.58.1142
- B. Efron, *Bootstrap Methods: Another Look at the Jackknife*, Ann. Statist. 7(1), 1–26 (1979). DOI: 10.1214/aos/1176344552

## Filer

- `v09b_asymptotic_run_rows.csv`
- `v09b_asymptotic_group_rows.csv`
- `v09b_asymptotic_candidate_summary.csv`
- `v09b_asymptotic_size_profiles.csv`
- `v09b_ensemble_summary.csv`
- `v09b_refined_candidate_summary.csv`
