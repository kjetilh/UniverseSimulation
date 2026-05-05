# UniverseSimulation: rapport til Lasse

Dato: 2026-04-29

Denne rapporten er skrevet for en teknisk leser som kan matematikk og systemtenkning, men som ikke har fulgt prosjektet fra innsiden. Målet er ikke å overbevise deg om at prosjektet har funnet fysikk. Målet er å forklare hva vi faktisk tester, hvorfor det er interessant, hvilke metoder vi bruker, hva vi har funnet så langt, og hva som fortsatt mangler før man kan mene at dette virkelig peker mot noe dypt.

## Kortversjonen

UniverseSimulation er et eksperimentelt forskningsprosjekt der vi studerer dynamikk på relasjonelle grafer. Tanken er å starte med en struktur som ikke har innebygd rom, avstand eller partikler, og undersøke om noe som ligner geometri, stabile lokale forstyrrelser, quasi-invarianter eller propagasjon kan oppstå fra rene relasjonelle regler.

Det viktige er ikke at modellen "er universet". Det er den ikke. Det interessante spørsmålet er smalere:

Kan en enkel, diskret relasjonell dynamikk spontant produsere robuste struktursignaler som minner om noen av egenskapene vi vanligvis forbinder med geometri, lokalisering, defekter og nesten-bevarte størrelser?

Status nå er blandet, men ikke tom:

- Vi har en stabil arbeidsregime-kandidat, `band_zero_del`, valgt etter flere kontroller.
- Vi har ikke vist Lorentz-likhet eller spacetime-lignende geometri. Det sporet er fortsatt `not_yet`.
- Vi har sett lokale struktur- og quasi-invariant-signaler, særlig spektrale signaler, men de er lokale/familiespesifikke og ikke globale lover.
- Det mest interessante aktive signalet er defect-/collision-sporet: lokale forstyrrelser kan bli langlivede, interagere ikke-trivielt, og ved større skalaer ser vi family-/p2-horizon-struktur som er robust nok til videre smal testing.
- Det vi ikke har: en partikkel, en universell geometri, en fysisk lov, eller et bevis for at dette skalerer til noe univers-lignende.

## Hvorfor gjøre dette?

Prosjektet springer ut av et ganske grunnleggende spørsmål: hvor mye struktur kan oppstå uten at vi legger inn rom og fysikk på forhånd?

I vanlige simuleringer starter man ofte med et rom, et gitter, en metrikk, eller en differensialligning. Da er det vanskelig å vite om geometri og lokalitet er noe modellen forklarer, eller noe vi allerede har puttet inn. Her prøver vi en mer brutal disiplin: start med en graf, la noder og kanter oppdatere seg etter regler, og mål om dynamikken selv skaper noe som kan tolkes som:

- lokalitet,
- avstandslignende struktur,
- robuste forstyrrelser,
- familier av gjentatte mønstre,
- nesten-bevarte størrelser,
- eller propagasjon med noenlunde stabil front.

For en hardware-person er en nøktern analogi dette: tenk på et system uten ferdig romlig koordinatsystem, men med mange lokale koblinger og feil/perturbasjoner. Spørsmålet blir da om bestemte typer feil dør ut, sprer seg, låser seg i mønstre, eller danner robuste "defektmodi". Analogien skal ikke brukes som bevis, men den kan hjelpe med intuisjonen: vi leter etter robuste responsmønstre i et komplekst, lokalt koblet system.

## Hva modellen gjør, på et overordnet nivå

Modellen arbeider med grafer: noder, kanter og lokale oppdateringsregler. Man kan tenke på grafen som en ren relasjonsstruktur. Det finnes ikke et fysisk rom i startpunktet. Avstand, "shells", radius og geometri er målte størrelser vi prøver å utlede fra grafens koblingsstruktur og dynamikk.

Vi kjører mange starttilstander og mange regelvarianter. For hver runde måler vi hvordan grafen utvikler seg, hvilke strukturelle trekk som er stabile, og hvordan lokale perturbasjoner endrer utviklingen.

Noen viktige begreper:

- `regime`: en bestemt generator-/oppdateringsinnstilling. Det nåværende arbeidsregimet er `band_zero_del`.
- `target`: nominell startstørrelse, for eksempel 48, 96, 192, 384 eller 768 noder.
- `perturbation`: en lokal forstyrrelse. Eksempler er `add_chord`, `local_swap` og `token_shift`.
- `placement`: hvor i grafen forstyrrelsen legges.
- `control`: en matchet kjøring uten eller med tilsvarende kontrollforstyrrelse, brukt for å skille reell dynamikk fra artefakter.
- `observable`: en målbar størrelse vi bruker for å beskrive dynamikken, for eksempel spektralradius, komponentstruktur, defektmasse, shell-occupancy eller genealogien til skadekomponenter.

## Metodisk disiplin

Prosjektet har blitt mer interessant etter hvert som metodene har blitt strengere. Tidlig var det lett å feiltolke signaler fordi generatoren ikke alltid traff de nominelle størrelsene. Derfor ble en viktig del av arbeidet å rydde opp i generator-/størrelsesartefakter.

De viktigste metodiske reglene nå er:

- Filer på disk er ground truth. Resultater skal komme fra faktiske `.csv`- og rapportfiler, ikke fra ønsketenkning.
- Vi skiller algebraiske fakta, generatorartefakter, scoringartefakter og dynamiske resultater.
- En heuristisk label er ikke en fysisk entitet. "Binding-like", "persistent split" eller "p2 horizon" er arbeidslabels, ikke partikkelnavn.
- Lokale positive signaler teller, men de får ikke oppgraderes til universelle lover uten holdout, kontroller og skala-testing.
- Hvis et eksperiment ikke er kjørt, skal det ikke finnes oppdiktede tall.

Metodene er i praksis en kombinasjon av:

- ensemblekjøringer over mange seeds,
- smale kandidatdueller i stedet for brede, løse scans,
- bootstrap-/pairwise-sammenligninger,
- matchede single- og pair-runs,
- AB/BA-ordrekontroller for kollisjoner,
- holdout-runder på friske seeds,
- skalahopp fra 48 til 96, 192, 384 og 768,
- og stadig mer mekanistiske observabler når terminale labels blir for grove.

Dette ligner mer på eksperimentell feilsøking enn på elegant teori. Det er bevisst. Prosjektet prøver å hindre at pene metaforer løper foran dataene.

## Hva vi har funnet

### 1. Arbeidsregimet `band_zero_del` er fortsatt beste anker

`v11e` avgjorde den siste smale frontier-duellen til fordel for `band_zero_del`. Det vant på rå score, CI-low, pairwise bootstrap og focused score. Dette betyr ikke at `band_zero_del` er "sann fysikk"; det betyr at det er den mest stabile operative plattformen for videre strukturtesting.

Praktisk konsekvens: vi har sluttet å bruke mesteparten av tiden på frontier-tuning. Det er viktig, fordi uendelig parameterjakt lett blir en måte å lure seg selv på.

### 2. Lorentz-/spacetime-sporet er ikke løst

Det finnes lokale struktur- og propagasjonssignaler, men Lorentz-likhet er fortsatt `not_yet`.

Grunnen er ikke bare at signalene er svake. Problemet er mer spesifikt: propagasjon og frontfart er mode-dependent og placement-sensitive. `v14`, `v14b` og `v14c` viste at kontroller og perturbasjonshygiene er bedre enn før, men lokal anisotropi er fortsatt en levende alternativ forklaring.

Dette er en viktig negativ konklusjon. Hvis man vil si at noe spacetime-aktig oppstår, må man vise at observerte fronter ikke bare skyldes hvor og hvordan man pirker i grafen. Der er vi ikke.

### 3. Quasi-invarianter finnes som lokale kandidater, ikke globale lover

Et quasi-invariant-signal er en størrelse som endrer seg lite under dynamikken, men ikke nødvendigvis er eksakt bevart.

Det mest interessante sporet har vært spektralt, særlig relativ drift i spektralradius-lignende mål. Det dukket opp som bedre enn mange trivielle alternativer og overlevde flere lokale tester. Men hver gang vi presset bredere, ble bildet mer blandet.

Den nåværende lesningen er derfor:

- Spektrale mål bærer reell strukturinformasjon.
- De blir mer interessante når vi condition-er på lokale familier/modi.
- De er ikke validert som globale bevaringslover.
- Eksakte null-drifter som dukket opp tidligere må leses forsiktig som regime-/koblingsartefakter, ikke dyp matematikk.

Dette er kanskje det matematisk mest interessante sporet, men det er også det letteste å overselge. Spektral stabilitet kan være et ekte hint, men det kan også være en konsekvens av generator og oppdateringsregel.

### 4. Defect-sporet ga det første tydelige mesoskalasignalet

Defect-sporet startet med lokale perturbasjoner. Et viktig funn i `v15` var at `add_chord` ofte ga langlivede split-lignende skadeområder. I aggregatet ga `add_chord` `persistent_split` i omtrent `0.938` av runene, mens `local_swap` lå rundt `0.688`. `token_shift` ga også mye persistent split, men med mer ut-døing.

Dette er ikke en partikkel. Men det var første tydelige tegn på at lokale inngrep kan produsere repeterbare mesoskopiske utfall som ikke bare er tilfeldig diffus skade.

### 5. Kollisjoner var ikke bare superposisjon

`v15b` testet to lokale `add_chord`-defekter samtidig, med matchede single-runs som kontroll. Hvis to defekter bare superponerte, burde pair-runen ligne unionen av single-runene.

Det gjorde den ikke. `mean_pair_union_jaccard` lå omtrent mellom `0.208` og `0.462`, mens kontrollene holdt seg rene. Alle rader støttet ikke-triviell interaksjon.

Men neste runder viste også at interaksjonstypen var blandet. `v15c` fant omtrent:

- `binding_like`: `0.188`
- `secondary_split_like`: `0.250`
- `mixed_collision`: `0.562`
- `annihilation_like`: `0.000`
- `pass_through_like`: `0.000`

Altså: ekte interaksjonssignal, men ikke en ren kollisjonsfamilie.

### 6. Nyere arbeid peker mot familie-/skalasignaler, særlig ved target 768

Etter mange små runder ble det tydelig at mer budsjett på samme grove labels ikke ga nok. Prosjektet flyttet derfor mot bedre observabler, familiestruktur og skala.

Ved target `96` fant vi family-struktur, men den replikerte dårlig på holdout. Target `192` ga et mer ordnet plateau, men p2-splittelsen holdt ikke rent. Target `384` ga nye kandidater og near-symmetry-signaler, men holdout svekket dem.

Target `768` ble mer interessant. `v15cd` fant et sterkt første signal: sju av åtte profiler falt i `rare_diffuse_family`, med `add_chord_p0` som outlier og near-symmetry-kandidater som inkluderte `add_chord_p2` / `local_swap_p2`. `v15ce` holdt dette bare delvis på friske seeds, men nok til at target 768 fortsatt er den mest lovende skalaen i denne observabelstakken.

### 7. Den ferskeste aktive kandidaten er en p2-horisont ved target 768

`v15cg` testet om p2 ved target 768 holder en far-shell-horisont: altså om skade/aktivitet langt ute i grafens shell-struktur varer gjennom halen. Den fant et svakt, men ekte p2-signal: `local_swap_p2` var sterkest, `add_chord_p2` holdt delvis, og p0-kontrollene var rene.

`v15ch` gjorde så holdout med friske seeds og flere terskler. Dette holdt overraskende godt:

- `local_swap_p2` holdt ved baseline og i `3/3` terskelkonfigurasjoner mot p0-kontrollen.
- p0-kontrollen holdt seg ren.
- `add_chord_p2` holdt også i `3/3` terskelkonfigurasjoner og var litt sterkere ved baseline.

Dette er den mest interessante ferske retningen: ikke en local_swap-spesifikk anomalitet, men en delt feature-level p2-kandidat på tvers av `add_chord` og `local_swap`.

Samtidig har de siste mekanismeforsøkene vært negative eller svake:

- `v15ci`: outer-genealogi var for generisk; alle profiler ble `reseeded_outer_horizon`.
- `v15cj`: outer-occupancy ga bare et svakt og carrier-splittet konsentrasjonssignal.
- `v15ck`: outer-feeder-flux endte `feeder_flux_not_yet`.

Arbeidskonklusjonen nå er derfor ganske presis: p2-lommen ved target 768 er reell nok til videre arbeid, men de enkleste outer-tail-forklaringene holder ikke. Neste test bør flytte mekanismeaksen innover, mot trigger-, gate- eller boundary-observabler rundt shell2/shell3 eller supportnær lansering.

## Hva dette kan være verdt

Hvis man vurderer prosjektet strengt, er verdien foreløpig ikke at det har funnet "universets kode". Det har det ikke.

Verdien ligger mer i at det har etablert en disiplinert eksperimentell maskin for å stille slike spørsmål uten å lure seg selv for lett. Vi har:

- funnet og korrigert generatorproblemer,
- etablert en stabil operativ regimekandidat,
- avvist for sterke Lorentz-tolkninger,
- funnet lokale quasi-invariant-signaler uten å gjøre dem til lover,
- funnet robuste lokale defect-/interaksjonssignaler,
- og identifisert en nyere target-768 p2-lomme som fortjener mekanistisk oppfølging.

For en hardware-/strålingsperson kan det interessante være metodikken rundt lokale feil og robust respons: hvordan lokale perturbasjoner sprer seg, låser seg, dør ut, eller danner langlivede skadeområder i et relasjonelt nettverk. Det er ikke direkte anvendt hardwarefysikk, men intuisjonen rundt fault propagation, shielding/stabilization, rare-load og retention kan være gjenkjennelig.

## Hva som ville gjort prosjektet mye mer overbevisende

Jeg ville ikke latt meg overbevise av flere pene labels. Det som må til er hardere.

Sterkere evidens ville være:

- At p2-horisonten ved target 768 får en klar mekanismeforklaring som holder på holdout.
- At samme mekanisme dukker opp ved større target, ikke bare samme størrelse.
- At observablene predikerer nye run før vi ser dem, ikke bare beskriver gamle.
- At en quasi-invariant kan defineres presist og holde på tvers av flere relevante regimefamilier.
- At Lorentz-lignende propagasjon kan skilles fra placement-sensitiv lokal anisotropi.
- At labels kan erstattes med målbare event chains, komponentgenealogi eller eksplisitte strukturelle kriterier.

Hvis de testene feiler, er det også nyttig. Da har prosjektet vist at de lokale mønstrene er ekte, men for heterogene eller modellspesifikke til å bære en stor tolkning.

## Min nøkterne vurdering

Prosjektet har noe for seg dersom man vurderer det som eksperimentell matematisk modellbygging: en systematisk jakt på hvilke typer emergent struktur som kan oppstå i relasjonelle grafer.

Prosjektet har ikke noe for seg dersom man forventer en kort vei til fysikk, partikler eller spacetime. Da er evidensen altfor svak.

Den mest forsvarlige posisjonen akkurat nå er:

Det finnes repeterbare, ikke-trivielle dynamiske signaler i modellen. Noen av dem er strukturelt interessante. De peker mot at lokalitet, defekter, familiestruktur og spektrale quasi-invarianter kan være fruktbare observabler i relasjonelle systemer. Men prosjektet er fortsatt på hypotesegenererende stadium, ikke teoribekreftende stadium.

For å gjøre seg opp en mening bør Lasse særlig se etter én ting: om neste runder klarer å gå fra "vi ser et mønster" til "vi kan forklare og predikere mønsteret med en mekanisme som holder på nye seeds og større skala". Hvis ja, blir prosjektet mye mer interessant. Hvis nei, er det fortsatt en god leksjon i hvor lett komplekse systemer lager lokalt overbevisende, men globalt skjøre mønstre.

## Filer som underbygger denne rapporten

De viktigste lokale ankerfilene i repoet er:

- `PROJECT_CONTEXT_LIVE.md`
- `PROJECT_HISTORY_INDEX.md`
- `Documentation/v11e_band_vs_bridge0075.md`
- `Documentation/v14_lorentz_diagnostics.md`
- `Documentation/v14b_lorentz_placement_diagnostics.md`
- `Documentation/v14c_local_isotropy_diagnostics.md`
- `Documentation/v15_defect_lifetime_lab.md`
- `Documentation/v15b_add_chord_collision_lab.md`
- `Documentation/v15c_collision_type_lab.md`
- `Documentation/v15g_collision_genealogy_lab.md`
- `Documentation/v15ch_target768_local_swap_p2_horizon_holdout_lab.md`
- `Documentation/v15ci_target768_p2_horizon_genealogy_mechanism_lab.md`
- `Documentation/v15cj_target768_outer_occupancy_concentration_lab.md`
- `Documentation/v15ck_target768_outer_feeder_flux_lab.md`
