# Relasjonell universgraf v0.10e: fokusert band-validering under anbefalt ensemble-regime

## Hva dette steget gjør

Etter v0.10b–v0.10d hadde prosjektet en klar generatoranbefaling:
bruk `fast_balanced / deep` og hold kandidatsettet smalt. Det naturlige neste steget
var derfor ikke et nytt bredt atlas, men en **lokal robusthetstest rundt den daværende
referansekandidaten `band_best`**.

Denne runden gjør tre ting samtidig:

1. holder generatorregimet fast (`fast_balanced / deep`),
2. øker replikasjonen moderat (3 growth seeds og 3 run seeds per target),
3. tester et lite lokalt bånd rundt `band_best` i stedet for å spre arbeidet over hele parameterrommet.

## Kandidatsett

Det fokuserte kandidatbåndet i v0.10e er:

- `band_best = (r_birth=0.02, r_death=0.00, p_swap=0.02, p_triad=0.00, p_del=0.01)`
- `band_zero_del = (0.02, 0.00, 0.02, 0.00, 0.00)`
- `band_small_death = (0.02, 0.01, 0.02, 0.00, 0.01)`
- `band_small_triad = (0.02, 0.00, 0.02, 0.01, 0.01)`
- `macro_stable = (0.02, 0.05, 0.02, 0.00, 0.01)`

Dette er bevisst smalt:
vi undersøker om sentrum i kandidatbåndet fortsatt bør ligge på `band_best`,
eller om en nær nabo nå ser mer robust ut.

## Oppsett

- Growth-regime: `fast_balanced`
- Burn-in: `deep`
- Realiserte størrelsesnivåer: 48, 96, 192, 256
- Growth seeds per target: 3
- Run seeds per kandidat/target/growth: 3
- Bootstrap-replikater for usikkerhet og pairwise robusthet: 160

## Generatorfidelitet i denne runden

Det første viktige funnet er at **generatorproblemet ikke dominerer denne runden**.
Under `fast_balanced / deep` traff de realiserte startstørrelsene her i praksis eksakt
på de valgte nivåene:

| target | mean initial | q10 | q90 | separated from previous |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |
| 192 | 192.0 | 192.0 | 192.0 | 1 |
| 256 | 256.0 | 256.0 | 256.0 | 1 |

Dette betyr at v0.10e i langt større grad tester **dynamiske forskjeller mellom kandidater**,
og i mindre grad generatorartefakter.

## Kandidatsammendrag

Tabellen under viser både rå score, bootstrap-robusthet og de asymptotiske indikatorene som var viktigst i v0.10d.
`focused_score` er en lokal rangeringsstørrelse for denne runden, basert på:

- høy `ci_low_mean_composite`
- lav `alpha_large`
- lav `|alpha_jump|`
- høy `linear_margin`
- høy `quasi_large`

Den er altså ment som en **lokal beslutningshjelp i dette båndet**, ikke som en universell fysisk størrelse.

| candidate | focused score | mean composite | CI low composite | top prob (mean composite) | alpha_large | alpha_jump | linear_margin | quasi_large |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| band_small_triad | 0.693 | 0.587 | 0.484 | 0.325 | 0.221 | -0.097 | 0.228 | -0.012 |
| band_best | 0.555 | 0.495 | 0.421 | 0.006 | 0.209 | -0.013 | 0.113 | -0.045 |
| band_zero_del | 0.528 | 0.590 | 0.527 | 0.375 | 0.062 | -0.127 | 0.122 | -0.178 |
| band_small_death | 0.527 | 0.554 | 0.503 | 0.256 | 0.225 | -0.027 | 0.136 | -0.273 |
| macro_stable | 0.092 | 0.486 | 0.401 | 0.037 | 0.410 | 0.075 | 0.092 | -0.300 |


## Det viktigste nye resultatet

v0.10e gir et klart og viktig metodisk funn:

> **`band_best` holder seg ikke som lokal vinner når vi låser generatoren til det anbefalte regimet og undersøker et nærliggende kandidatbånd med moderat økt replikasjon.**

Mer presist:

- `band_zero_del` har høyest **rå mean composite** (0.590)
  og høyest **top probability på mean composite** (0.375).
- `band_small_triad` har høyest **focused score** (0.693),
  fordi den kombinerer sterk score med bedre `linear_margin` og en mindre negativ `quasi_large` enn flere av konkurrentene.
- `band_best` faller ned til en mellomposisjon i dette båndet, med svært lav `top_prob_mean_composite`
  på bare 0.006.

Det betyr ikke at `band_best` er "falsifisert". Men det betyr at prosjektets lokale sentrum
ikke lenger bør ligge ukritisk på den gamle referansekandidaten.

## Pairwise robusthet

Bootstrap-sannsynlighetene for rå mean composite er særlig opplysende.

Noen nøkkelpar:

- `band_zero_del > band_best`: 0.887
- `band_small_triad > band_best`: 0.800
- `band_small_death > band_best`: 0.819
- `band_zero_del > band_small_triad`: 0.581
- `band_small_triad > band_zero_del`: 0.419

Dette tegner et tydelig bilde:

- `band_best` er ikke den robuste lokale favoritten.
- Fronten i dette båndet er i stedet **todelt**:
  - `band_zero_del` ser sterkest ut på rå score og bootstrap-vinnersannsynlighet,
  - `band_small_triad` ser sterkest ut når vi legger mer vekt på skala-stabilitet og mindre negativ `quasi_large`.

## Tolkning av de lokale parameteraksene

### 1. `p_del`: fra `band_best` til `band_zero_del`
Å sette `p_del` fra `0.01` til `0.00` ga i denne runden:

- høyere mean composite
- høyere CI low composite
- klart høyere vinnersannsynlighet på rå score
- lavere `alpha_large`

Dette er en konkret indikasjon på at den lille delete-komponenten i `band_best`
ikke nødvendigvis er nyttig i akkurat dette ensemble-regimet.

### 2. `p_triad`: fra `band_best` til `band_small_triad`
Å innføre en liten triad-komponent (`p_triad = 0.01`) ga:

- høyere mean composite
- betydelig bedre `linear_margin`
- den minst negative `quasi_large` i kandidatsettet
- best `focused_score`

Dette er viktig fordi tidligere atlasrunder ofte favoriserte svært lave triad-verdier.
v0.10e sier ikke at stor triad-rate er bra; det sier at **en svært liten, men ikke-null triad-rate**
kan være gunstig i denne lokale delen av parameterrommet.

### 3. `r_death`: fra `band_best` til `band_small_death`
En liten death-rate (`0.01`) forbedrer `band_best` på rå mean composite, men gir mer negativ `quasi_large`
og mer blandet asymptotisk profil enn `band_small_triad`. Resultatet er derfor interessant,
men ikke like sterkt som de to nye frontkandidatene.

## Størrelsesprofiler

| candidate | target | realized initial | mean radius | mean overlap | mean quasi | mean composite |
| --- | --- | --- | --- | --- | --- | --- |
| band_best | 48 | 48.0 | 5.33 | 0.607 | 0.698 | 0.614 |
| band_best | 96 | 96.0 | 6.11 | 0.618 | 0.438 | 0.516 |
| band_best | 192 | 192.0 | 9.33 | 0.632 | 0.409 | 0.381 |
| band_best | 256 | 256.0 | 7.11 | 0.664 | 0.393 | 0.469 |
| band_small_death | 48 | 48.0 | 5.22 | 0.531 | 0.828 | 0.616 |
| band_small_death | 96 | 96.0 | 6.22 | 0.731 | 0.704 | 0.673 |
| band_small_death | 192 | 192.0 | 9.78 | 0.646 | 0.365 | 0.340 |
| band_small_death | 256 | 256.0 | 7.33 | 0.698 | 0.484 | 0.589 |
| band_small_triad | 48 | 48.0 | 4.11 | 0.643 | 0.881 | 0.714 |
| band_small_triad | 96 | 96.0 | 5.89 | 0.624 | 0.428 | 0.554 |
| band_small_triad | 192 | 192.0 | 8.11 | 0.711 | 0.617 | 0.548 |
| band_small_triad | 256 | 256.0 | 7.22 | 0.714 | 0.353 | 0.531 |
| band_zero_del | 48 | 48.0 | 5.11 | 0.536 | 0.854 | 0.622 |
| band_zero_del | 96 | 96.0 | 7.11 | 0.516 | 0.758 | 0.542 |
| band_zero_del | 192 | 192.0 | 7.00 | 0.667 | 0.670 | 0.647 |
| band_zero_del | 256 | 256.0 | 7.78 | 0.626 | 0.573 | 0.548 |
| macro_stable | 48 | 48.0 | 4.89 | 0.625 | 0.763 | 0.719 |
| macro_stable | 96 | 96.0 | 5.56 | 0.636 | 0.504 | 0.522 |
| macro_stable | 192 | 192.0 | 9.56 | 0.606 | 0.398 | 0.424 |
| macro_stable | 256 | 256.0 | 8.22 | 0.456 | 0.177 | 0.277 |


Legg merke til at både `band_zero_del` og `band_small_triad` holder seg konkurransedyktige
på tvers av alle fire nivåer, men med litt ulike profiler:

- `band_zero_del` er mer "stabilt sterk" på rå score.
- `band_small_triad` ser bedre ut på de mer strukturelle asymptotiske indikatorene.

## Hva dette innebærer

### Metodisk
Dette er et godt forskningstegn. Når generatorproblemet først ble renset bort i v0.10b–v0.10d,
og vi deretter gjorde en lokal nabotest, endret den foretrukne kandidaten seg.
Det betyr at prosjektet nå er i en fase der **lokal kandidatseleksjon faktisk betyr noe**,
ikke bare generatorvalg.

### Dynamisk
Innen dette smale båndet peker resultatene mot at prosjektets mest lovende sentrum nå er
en **to-kandidat-front** snarere enn én referansekandidat:

- `band_zero_del`
- `band_small_triad`

`band_best` er fortsatt relevant som referanse, men ikke lenger som opplagt lokal standard.

### Ikke-konklusjoner
Dette er fortsatt ikke en bekreftet fysisk teori.
Det er heller ikke et fullstendig parameteratlas.
Det er en kontrollert, lokal robusthetstest i ett anbefalt ensemble-regime.

## Operativ anbefaling videre

Den mest nyttige neste runden er nå en **v0.10f / v0.11-frontier-test** med:

1. `fast_balanced / deep` beholdt som standard generator,
2. kandidatsett sentrert på `band_zero_del` og `band_small_triad`,
3. én eller to ekstra naboer langs `p_swap`-aksen og eventuelt en finere `p_triad`-akse,
4. flere growth seeds og flere run seeds enn i v0.10e,
5. samme eksplisitte rapportering av realiserte startstørrelser.

Kort sagt:
v0.10e flytter prosjektets operative sentrum **vekk fra `band_best` og over mot en todelt lokal front**.
