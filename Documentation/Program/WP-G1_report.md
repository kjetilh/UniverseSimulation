# WP-G1: adversariell replikasjon av WP-F0

Status: steg 1, 2, 3 og 5 fullført 6. september 2026. Arbeidsgrunnlag:
`8ae4dc8` (WP-A). Tersklene i WP-F0 er uendret. Ingen ny
UniverseSimulation-dynamikk er kjørt, og resultatet er ikke en fysikkpåstand.

## Brief audit, Formål og mål

Oppdraget, WP-F0-spesifikasjonen, v16b-kilden og alle målte CSV-kilder er
`retrieved` fra arbeidskopien. Blindfasen ble kjørt før
`Tools/causet_admissibility.py`, `WP-F0_report.md` eller WP-F0-resultatene ble
åpnet. `WP-G1_blind_manifest.json` bevarer kilde- og råresultathasher.
`WP-G1_adversarial_preregistration.json` frøs design, seed og utvalgsregler før
steg 2 ble målt. Briefen er premiss, ikke autoritet.

Brief-auditen fant én faktisk feil: den antyder at det ligger fine
hendelses-DAG-er med andre N enn 2048/3072 i de navngitte v16-filene. Et
fullstendig inventar fant 96 fine historier i ni kantfiler, men bare N=2048 og
N=3072; de andre størrelsene er grove kvotient-DAG-er. Dette utløste en
korreksjonsrunde før trenddommen: N-ekstrapolasjonen er merket som en
ubeskyttet topunktsbeskrivelse, og ingen tidligere dom var basert på det gale
premisset.

Formål: `purpose://prompt.unknown` (kandidat: uavhengig, adversariell
replikasjon av en programgate).

| mål | baseline | målbart mål | evidens | sluttstatus |
| --- | --- | --- | --- | --- |
| G1 | samme forfatter hadde skrevet gate og kode | 36/36 historier målt uavhengig og avvik avgjort | replika- og sammenlignings-CSV | tilfredsstilt |
| G2 | null-, konstruksjons-, N- og desimeringsangrep manglet | steg 2.1–2.4 med frosne generatorer og råtall | sju steg-2-CSV-er | tilfredsstilt |
| G3 | ingen uavhengig linjeaudit | alle angitte kodeflater testet; feil og korrekte deler skilt | 10 tester | tilfredsstilt |
| G4 | rotpåstanden stod i WP-F0 | støttet, motsagt eller åpent med grunn og eier | dom og claim-ledger under | tilfredsstilt: motsagt i bred form |

## Steg 1 — uavhengig replika

Replikaen bruker `frozenset`/`set` for forfedre og etterkommere, ikke
bitsett-heltall. Den leser eksplisitt N fra de respektive run-summary-filene,
slik at isolerte endehendelser ikke forsvinner. `causal_depth` i v16b er
lengste innkommende vei målt i kanter; `causal_depth = max(depth)+1` er dermed
lengste kjede i elementer. Gulvargumentet er gyldig.

Alle 12 deterministiske felter under var identiske for alle 36 historier:

| feltgruppe | største absolutt avvik | største relativt avvik |
| --- | ---: | ---: |
| rå kanter og kanter/hendelse | 0 | 0 |
| sammenlignbare par, r, r_floor og r/r_floor | 0 | 0 |
| h, lenker og lenker/hendelse | 0 | 0 |
| maks \|I\|, maks \|I\|/N og Θ | 0 | 0 |

Portdommen reproduseres derfor: G0.1 bestås av 1/36, G0.2 av 0/36, G0.3 av
19/36, G0.4 av 0/36, og hele Gate 0 av 0/36.

Desimeringen reproduserer ikke WP-F0s tall når spesifikasjonens «minst 20
trekk per p» brukes bokstavelig. Tabellen viser konvensjonell median over
historier:

| arm | N | replika s, 20 trekk ved alle p | WP-F0 s, ett trekk ved p=1 |
| --- | ---: | ---: | ---: |
| current_global | 2048 | 0,713 | 0,680 |
| exposure_matched_local | 2048 | 0,724 | 0,680 |
| current_global | 3072 | 0,722 | 0,682 |
| exposure_matched_local | 3072 | 0,725 | 0,687 |

33/36 s-verdier avviker mer enn 1 %, og 14/36 ligger utenfor det opprinnelige
per-historie-KI-et. Årsaken er ikke bare ny RNG: WP-F0-linje 292 kjører ett
trekk ved p=1, mens linje 184–194 vekter hvert enkelt trekk som et
regresjonspunkt. Dermed får p=1 én tjuendedel av vekten til hvert annet nivå.
Gate 1 feiler fortsatt klart med den bokstavelige prosedyren.

`WP-G1_replica_per_history.csv` har nøyaktig samme kolonner som WP-F0-filen.
Rått blindresultat og de 6 912 første trekkene er bevart separat; den endelige
spesifikasjonstro filen inneholder 4 320 trekk (36 × 6 × 20).

## Steg 2 — angrep på premissene

### 2.1 Kalibrert kjedebunt med tverrkanter

Nullen hadde 32 kjeder × 64 elementer og nøyaktig 2 328 rå kanter, medianen
avrundet fra de 24 N=2048-historiene. 312 unike tverrkanter ble lagt mellom
ulike kjeder, alltid fremover i lag; 24 forhåndsregistrerte replikater ble
målt.

| størrelse | historier N=2048, median [min; maks] | kalibrert bunt, median [min; maks] |
| --- | --- | --- |
| rå kanter/hendelse | 1,136 [1,091; 1,215] | 1,137 [1,137; 1,137] |
| lenker/hendelse | 1,026 [1,009; 1,054] | 1,125 [1,121; 1,129] |
| r/r_floor (G0.1) | 1,262 [1,123; 1,700] | 3,980 [3,568; 4,564] |
| maks \|I\|/N (G0.3) | 0,051 [0,025; 0,084] | 0,135 [0,098; 0,174] |
| Θ (G0.4) | 1,212 [0,937; 1,658] | 3,980 [3,568; 4,564] |
| s, WP-F0-vektet | 0,680 [0,626; 0,726] | 0,685 [0,660; 0,718] |

Nullen treffer bare råkantkalibreringen og omtrent s; den bommer med faktor
3,2 på r/r_floor og Θ og 2,6 på største intervallfraksjon. «Kjedebunt med
tilfeldige tverrkanter» er derfor ikke en adekvat strukturell beskrivelse.
Tallene støtter den smalere betegnelsen *sparsom konflikt-DAG dominert av
lange, vedvarende ressurskjeder med langt mindre miksing enn tilfeldige
tverrkanter*.

### 2.2 En ekte d=2-sprinkling gjennom konflikt-DAG-konstruksjonen

Hver av 24 holdout-sprinklinger hadde N=2048 uniforme lyskjeglekoordinater.
Hver hendelse fikk 1–3 tilfeldige ressurser som både leses og skrives.
Ressurspoolen ble valgt på åtte separate kalibreringshistorier per kandidat,
utelukkende etter råkantavvik; valgt pool var 2048.

| størrelse | underliggende d=2-poset | konflikt-DAG-projeksjon |
| --- | ---: | ---: |
| r, median [min; maks] | 0,499 [0,487; 0,518] | 0,00590 [0,00520; 0,00681] |
| h, median [min; maks] | 85 [79; 92] | 13 [11; 15] |
| Θ, median [min; maks] | 12,08 [11,32; 13,11] | 1,012 [0,818; 1,152] |
| rå kanter/hendelse | — | 1,144 [1,114; 1,174] |
| lenker/hendelse | — | 1,143 [1,113; 1,170] |
| r/r_floor | — | 2,449 [2,246; 2,668] |
| maks \|I\|/N | — | 0,00757 [0,00635; 0,01074] |

Generatorens r≈0,5 og Θ≈12 verifiserer d=2-inputtet. Etter nøyaktig samme
frontierregel som `DependencyDAG.add` blir lenker≈1 og Θ≈1. Gate 0 avviser
dermed 24/24 kjente d=2-inputt etter konfliktprojeksjonen (G0.2, G0.3 og G0.4
feiler). Dette er det avgjørende moteksemplet: gaten tester om
ressurskonfliktprojeksjonen selv ser ut som en sprinkling, ikke om den
underliggende hendelsesordenen kan være geometrisk. Den etablerer ikke at
historiene er d=2; den viser at WP-F0s veto ikke følger av disse størrelsene.

Utfordret annenadjudikasjon: G0.1 og G0.3 skiller fortsatt historiene fra den
tilfeldig ressursmerkede d=2-projeksjonen, så den smale dommen «den lagrede
konflikt-DAG-en er tynn og ikke selv sprinklinglik» står. Utfordringen velter
likevel den brede dommen «derfor er dimensjonsspørsmålet avvist og v18 skal
ikke kjøres», fordi projeksjonen ikke er vist å bevare den ordenen spørsmålet
gjelder. Dette er en intern adversariell dobbeltdom, ikke en uavhengig ny
panelist.

### 2.3 N-trenden

Inventaret omfatter 96 fine historier: v16b, v16c, v16d, v16e, v16h, v16k,
v16m, v16n-kalibrering og v16s. Det finnes **0** fine historier med
N≠2048/3072. En potensmodell kan derfor bare være en deskriptiv topunktslinje:

| utvalg/arm | Θ(2048) | Θ(3072) | eksponent b i Θ∝N^b, 95 % gruppebootstrap | naiv N ved Θ=5 |
| --- | ---: | ---: | ---: | ---: |
| WP-F0/current_global | 1,231 | 1,607 | 0,657 [0,227; 1,137] | 17 300 [7 100; 575 000] |
| WP-F0/local | 1,187 | 1,463 | 0,514 [−0,242; 1,056] | 33 500; positiv-b KI [7 900; 9,7×10⁹] |
| alle fine/current_global | 1,231 | 1,478 | 0,450 [0,133; 0,688] | 46 100 [16 500; 1,86×10⁷] |
| alle fine/local | 1,187 | 1,465 | 0,519 [0,185; 0,706] | 32 800 [16 300; 1,62×10⁶] |

Senere N=3072-kjøringer er ikke nødvendigvis utbyttbare med WP-F0, og to N
kan ikke teste en potenslov. Tallene viser en mulig positiv trend, men de kan
verken bære terskelkryssingen eller et fortsatt veto. Ny dynamikk ble ikke
kjørt.

### 2.4 Desimeringseksponenten for 32×64-bunten

For den rene bunten er eksakt
`L(p)=max(X₁,…,X₃₂)`, der `Xᵢ ~ Binomial(64,p)`. Den eksakte fordelingen gir:

| p | E[L] | P(L≥8) |
| ---: | ---: | ---: |
| 1 | 64,000 | 1,000 |
| 1/2 | 40,235 | 1,000 |
| 1/4 | 23,415 | 1,000 |
| 1/8 | 13,855 | ≈1,000 |
| 1/16 | 8,441 | 0,774 |
| 1/32 | 5,326 | 0,0267 |

200 000 replikater av nøyaktig WP-F0-fitprosedyre gir forventet s=0,7250,
95 % prosedyreintervall [0,6898; 0,7552]. Målt WP-F0-verdi 0,7189 treffer.
Med bokstavelig 20 trekk også ved p=1 blir forventningen 0,7219
[0,6988; 0,7418], og målingen treffer fortsatt. s<1 skyldes altså maksimumet
over 32 endelige kjeder og L≥8-seleksjonen, ikke i seg selv en feil fit.

## Steg 3 — linjeaudit av referansekoden

### Korrekte angrepsflater

- `link_count` (linje 106–114) er ekvivalent med dekkrelasjonen. Hvis en direkte
  kant p→v har en alternativ vei, slutter veien med en annen direkte
  forgjenger q→v og p er forfar til q; motsatt gir en slik q en alternativ
  vei. Både det eksplisitte fem-elements-posetet og alle 2¹⁰=1024 DAG-er i
  topologisk orden på fem elementer passerer mot brute-force-dekkene.
- `max_interval` (linje 116–127) er riktig: `desc[p] ∩ anc[q]` inneholder bare
  de strengt mellomliggende elementene; `+2` legger til p og q. Samme 1024-test
  passerer.
- `decimate` (linje 129–156) induserer fra transitiv lukning. Kjeden 0→1→2
  desimert til {0,2} får L=2, som krevd.
- `mm_dimension` er monotont avtakende i r på det testede domenet. Den returnerer
  `inf` for r=0 og 1,0001 for r=1. Sistnevnte er en liten randtilnærming, ikke
  den eksakte verdien d=1; positive r som svarer til d>40 kollapses også til
  `inf`. Ingen av delene påvirker de målte historiene.

### Feil og kontraktsbrudd

1. **Historielasteren mister eller blander hendelser** (linje 261–275). N settes
   til største kantendepunkt + 1, så isolerte hendelser etter siste kant
   forsvinner og en kantløs historie droppes helt. `run_seed` er ikke del av
   grupperingsnøkkelen, så to ellers like kjøringer kan flettes. Tre målrettede
   tester demonstrerer dette. De 36 WP-F0-historiene er ikke rammet: run-summary
   gir samme N som største endepunkt, og alle deterministiske tall matcher.
2. **p=1 bryter den frosne trekkregelen og gir skjev nivåvekt** (linje 291–297,
   sammen med 184–194). Ett p=1-punkt mot 20 på hvert annet nivå endrer s
   systematisk; den bokstavelige replikaen avviker >1 % i 33/36 historier.
3. **Bootstrap-enheten er ikke historien** (linje 197–209 og 373–377). WP-F0
   resampler L-trekk innen hvert p-nivå. Det er et KI for Monte Carlo-feil gitt
   et fast historiesett, ikke for overføring til nye historier. Direkte
   historie-cluster-bootstrap gir KI-bredder:

   | arm/N | WP-F0-enhet | historie-enhet |
   | --- | ---: | ---: |
   | current_global/2048 | 0,0320 | 0,0222 |
   | current_global/3072 | 0,0344 | 0,0233 |
   | local/2048 | 0,0310 | 0,0302 |
   | local/3072 | 0,0363 | 0,0439 |

   Forskjellen har ikke én retning; de to bootstrapene estimerer ulike
   usikkerheter. «95 % KI per arm» er derfor ufullstendig merket, men Gate 1
   endres ikke.
4. **Aggregatets «median» er øvre midtpunkt** (linje 378–384), ikke medianen for
   partall n. Største synlige utslag er local/N=3072: rapportert r=0,03101 mot
   konvensjonell median 0,02771, Θ=1,5117 mot 1,4627 og d_MM=5,643 mot 5,505.
   Portutfallet endres ikke.

Testfil: `tests/test_wp_g1_adversarial_replication.py`. Resultat: 10/10 bestått.

## Steg 5 — claim-ledger, dom og neste beslutning

| claim | dom | evidens / grense |
| --- | --- | --- |
| C1: deterministisk WP-F0-måling reproduseres | støttet | 36/36, null avvik |
| C2: kalibrert kjedebunt er adekvat null | motsagt | r/r_floor, Θ og intervall bommer stort |
| C3: Gate 0 tester underliggende geometri | motsagt | 24/24 kjente d=2-inputt avvises etter konfliktprojeksjon |
| C4: Θ følger en etablert N-lov | åpen, eier Kjetil/programmet | bare to fine N; ingen ny dynamikk tillatt |
| C5: buntens s≈0,72 følger prosedyren | støttet | eksakt maks-binomfordeling + 200 000 fits |
| C6a: lenke/intervall/desimeringskjerne er korrekt | støttet | bevis + uttømmende fem-node-test |
| C6b: historielasteren bevarer alle runs/N | motsagt | tre konstruktive tester |
| C6c: s-implementasjonen følger trekkkravet | motsagt | ett mot påkrevd minst 20 ved p=1 |
| C6d: aggregatmediane og arm-KI er korrekt merket | motsagt | øvre midtpunkt og feil estimand |

**Én setning:** Konklusjonen «DAG-en er en kjedebunt, kjør ikke v18» faller på steg 2.2: en verifisert d=2-sprinkling får også lenker≈1 og Θ≈1 gjennom konflikt-DAG-konstruksjonen, mens den kalibrerte kjedebuntnullen bommer, så riktig svar er at den lagrede konflikt-DAG-en er tynn, men denne gaten kan ikke avgjøre underliggende dimensjon eller vetoere v18.

Neste beslutning til Kjetil er derfor ikke automatisk «kjør hele v18», men å
erstatte vetoet med en orden eller projeksjon som er dokumentert
geometribevarende, og deretter avgjøre om v18 fortsatt er riktig eksperiment.

## Rapportkvalitet Q1–Q10

| metrikk | resultat | observerbar begrunnelse |
| --- | --- | --- |
| Q1 posisjonsendring | 1/1 sporet | C2/C3-dom følger 2.1/2.2-råtall |
| Q2 blandet ledger | 2/6 mot oppdragets «velt»-retning | C1 og C5 står; C2/C3 faller; C4 åpen; C6 delt |
| Q3 audit-status | 9/9 load-bearing claims har hentet fil/evidens | ingen hukommelseskilde teller |
| Q4 narrativ uavhengighet | 2/2 hovedfunn | både smal stående dom og bredt motfunn er eksplisitte |
| Q5 falsifiserbarhet | 0 umerkede selvforseglende claims | generator- og nullutfall kunne gått motsatt vei |
| Q6 naturlig eksperiment | 1/1 | d=2 ble faktisk kjørt gjennom projeksjonen før dom |
| Q7 revealed preference | ikke relevant | ingen aktørmotiv påstås |
| Q8 terminal adjudikasjon | 9/9 | C4 er eksplisitt åpen med eier |
| Q9 steelman-kilde | 1/1 | WP-F0-rapportens smale dom er bevart der data bærer den |
| Q10 uankrede innrømmelser | 0 | alle står ved tall eller test |

Metrikkene er diagnostikk, ikke karakter eller optimaliseringsmål.

## Verifikasjon og hasher

- Frossen WP-F0-spec: `004ceb53482e2f0bae0b5c4cf31b2051bea2537656d4373695e3ea2d1fe5f73c`.
- v16b-kilden lest før blind implementasjon: `fba9a56af938ffc90c9878d799498da0d1868e2491044147ae5df0ca9e2f7709`.
- Blindmanifest: `20f6c2d8e310a3f327f7897d5a83d65150f21aa266f033aa6ad4d454278bc520`;
  alle ikke-scriptartefakter i manifestet er reverifisert. Manifestet bevarer
  blindversjonens script-hash; sluttverktøyets hash er
  `bc4bcb77cef1cb383e8bb455b29e9674d316a694fec43b2d8ca46071607d1ce7`.
- Steg-2-preregistrering: `a45635b653c44c8f9aafb3de1e2010384e04387d77842b48d3e659f90daf77e2`.
- Replikasammenligning: `f68be6b7126750e57ccd264ca697b22e29e0c8c25a2db8a221ce4cd528147090`;
  d=2-holdout: `f1c71e27aa2fd406436e3d6e85bd44536bee0a7fd7b95a66305e887b0a7658b0`;
  fin-DAG-inventar: `1c120e4a614e7bc5994066388836c583dcd441b66ded500dd74aa59ef4051881`.
- `py_compile`, CSV-radtall/headerkontroll, blindmanifestkontroll,
  `git diff --check` og 10/10 enhetstester bestod.

## Commit-hasher og blokkert

- WP-A: `8ae4dc8`.
- WP-G1: ikke opprettet. `git add` ble forsøkt 6. september 2026, men sandboxen
  nekter skriving av `.git/index.lock` med `Operation not permitted`; både
  `.git` og `.git/index` er bekreftet ikke-skrivbare. Ingen filer ble staged.
- Blokkert evidens: ingen fine N utover 2048/3072 finnes på disk, så C4 kan ikke
  lukkes uten ny dynamikk eller nye eksterne historier.
- Blokkert levering: den påkrevde WP-G1-committen kan ikke opprettes i dette
  miljøet. Steg 1, 2, 3 og dommen er ellers fullført.
- Push, offentlig deploy og RAG-synk er ikke kjørt: WP-F0-spesifikasjonen sier
  uttrykkelig at closure-policyen ikke gjelder analysepakken, og WP-G1 sier
  «ikke push».
