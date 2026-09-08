# Vurdering: typede nodegrafer som søke- og kompileringssubstrat

Skrevet 8. september 2026 av Losen (Claude Opus 5) på oppdrag fra Kjetil.
Kode: `Tools/nodegraph/`. Formålsdefinisjon: `Tools/nodegraph/PURPOSE.md`.
Alle tall under er lest fra filer i `Tools/nodegraph/_cache/`, ikke fra
sammendrag.

**Ingen fysikkpåstand.** Ingen v-runde er åpnet, ingen gate berørt,
`attempt_ledger.csv` er urørt.

---

## 1. Kort svar

Ideen har verdi, men ikke jevnt fordelt over de fem delene den består av. Delt
opp:

| Del av forslaget | Vurdering |
|---|---|
| Typede noder som funksjonsdefinisjoner, komposittnoder, bibliotek | **Solid.** Bygget, testet, virker. Billig. |
| Kompilere en funnet graf til raskere form | **Solid, med én skarp betingelse.** Målt 265–289× — men bare når dataene allerede ligger på den kompilerte siden. Krysser du språkgrensen per kall er gevinsten ~3×. |
| AI-agent som justerer algoritmer uten å forstå matten | **Reell, men det er ikke her flaskehalsen ligger.** Et deterministisk søk uten tokens fant svaret. Grafrepresentasjonen er den lette femtedelen. |
| «Utfordringen ligger kanskje i å beskrive formålene» | **Det er ikke «kanskje». Det er hele problemet,** og det er det eneste stedet dette repoet har et dokumentert, dyrt sår. |
| Løse partielle differensiallikninger | **Overklaimet som formulert.** Én naboversjon er innen rekkevidde og gjør allerede nytte i litteraturen; åpne PDE-problemer er det ikke. |

Den versjonen som er verdt å bygge er smalere enn den foreslåtte og peker en
annen vei: ikke «en AI som oppfinner algoritmer», men **et billig, typet,
kompilerbart uttrykkssubstrat med en formålskontrakt som nekter å gate på en
størrelse den ikke har kalibrert** — og hvis første jobb er å finne
observablene v17 manglet, og å være kjøremotoren for Goals-som-uttrykk i HAVEN.

---

## 2. Hva forslaget er, i kjent terminologi

Dette er ikke kritikk. Det er posisjonering, og den er nødvendig fordi hver
enkelt del har et eksisterende bevis for at den lar seg gjøre — og fordi hver
del også har en kjent grunn til at den ofte ikke gir gevinst.

- **Typede noder med deklarert aritet, inn- og ut-typer** er *strongly typed
  genetic programming* (Montana, *Evolutionary Computation*, 1995). Typene
  fjerner det meste av et ellers meningsløst søkerom.
- **Graf-IR som kompileres til mange mål** er MLIR, XLA, ONNX, TVM, Halide.
  Modent felt. Det ikke-trivielle er ikke å generere kode, men å bevise at den
  genererte koden betyr det samme.
- **Å omskrive uttrykksgrafer til raskere ekvivalente former** er *equality
  saturation* (`egg`, POPL 2021). Dette er den etablerte måten «kompiler det
  til en mer effektiv form» faktisk gjøres på.
- **Språkmodell som forslagsoperator over et program­rom med billig, eksakt
  evaluator** er FunSearch (Romera-Paredes m.fl., *Nature*, 2024). Den fant
  nye konstruksjoner for cap set-problemet og bedre bin-packing-heuristikker.
  Det er det sterkeste eksisterende beviset for at brukerens kjerne-loop
  virker. Merk hva som bar den: en *billig, eksakt, total* scorefunksjon.
- **Søk etter raskere algoritmer helt ned i assembly** er AlphaDev (*Nature*,
  2023) og AlphaTensor (*Nature*, 2022). Gevinstene var reelle og små, og
  regnekostnaden enorm.
- **Å finne styrende likninger — inkludert PDE-er — fra data ved å søke over
  et bibliotek av kandidatledd** er SINDy (*PNAS*, 2016) og PDE-FIND (*Science
  Advances*, 2017). Dette er den nærmeste naboen til PDE-ideen, og den virker.
- **Observasjonell ekvivalens i bottom-up syntese** er standardteknikken som
  gjør enumerering håndterbar, og er implementert i `search.py`.

Konklusjon på dette punktet: arkitekturen er godt fundert og ikke ny. Det er
ikke innvendingen — spørsmålet var om den har nytte her, ikke om den er
original.

---

## 3. Fire steder forslaget hevder mer enn det bærer

**(a) «La språkmodeller manipulere nodene uten å forstå matte selv.»**
Halvveis riktig, men den beskriver mekanismen feil vei. En modell brukt som
*blind* mutasjonsoperator er dårligere enn genetisk programmering, som er
billigere og har bedre støy­egenskaper. Det FunSearch faktisk utnytter er det
motsatte: modellens *sterke priorer over programformer*, med evaluatoren som
eneste sannhetskilde. Designkonsekvensen er konkret: grafen må kunne leses og
skrives som tekst, ikke bare som graf. `core.parse` / `Graph.to_expr` er den
døren, og typesjekken står i den.

**(b) «Så kan vi kompilere det inn i en mer effektiv form … til og med direkte
i assembly.»** Assembly er en felle på dette stadiet. AlphaDev-klassen gevinst
er noen få instruksjoner mot enorm søkekostnad. De riktige målene er, i
rekkefølge: en rask in-process form, **Swift** (fordi Goals skal evalueres i
CellProtocol), og C/Rust for hete løkker. Og «kompilere» er bare et meningsfylt
ord hvis semantikken er definert ett sted og backendene *bevises* like mot den.
Uten det får man den klassiske feilen der den raske versjonen er uenig med den
trege, og ingen oppdager det.

**(c) «Kanskje løse partielle differensiallikninger.»** Skill fire ting:
oppdage lukket form fra simuleringsdata (rekkevidde — det er SINDy/PDE-FIND, og
det er nyttig her); oppdage *observabler* (rekkevidde, og det er det v17
manglet); finne et numerisk skjema for en kjent PDE (rekkevidde, men et løst
felt); løse åpne PDE-problemer (nei). Formuleringen i forslaget lover det
fjerde og leverer det første.

**(d) «Utfordringen ligger kanskje i å beskrive formålene.»** Dette er den
viktigste setningen i hele forslaget, og «kanskje» er for svakt. Nodebiblioteket
er den lette femtedelen. Uten en formålskontrakt som er billig, eksakt, total
*og kalibrert*, gir et søkerammeverk deg bare en penere notasjon for å gjette —
og et søk over tusenvis av kandidater produserer garantert en vinner selv når
det ikke finnes noe å finne. Det er derfor `purpose.py` er den filen i dette
rammeverket som faktisk er verdt noe.

---

## 4. Det som ble bygget og målt

`Tools/nodegraph/`, 45 noder, alle med både Python- og C-implementasjon,
ingen tredjepartsavhengighet i kjernen.

### 4.1 Kjernen (D1–D3)

Noder deklarerer aritet og typer; feiltypet konstruksjon avvises med presis
melding. Grafen er hash-consed, så like deluttrykk blir samme node og
`key()` er strukturell identitet. Komposittnoder er førsteklasses: en lagret
delgraf registreres som node, brukes som node, og inlines til nøyaktig samme
graf som den innsatte formen.

**Konformans:** hver av de 45 nodene ble kompilert til C og sammenlignet mot
referansetolken på 250 tilfeldige input hver. **0 avvik.** For den utvalgte
grafen: 400 forsøk, største absolutte avvik **0,0**. En backend som ikke består
denne prøven sertifiseres ikke og deles ikke ut.

Testen fant også en reell divergens underveis: `(x - m) ** 2` kaster
`OverflowError` i Python der `(x-m)*(x-m)` gir `inf` som så flates til 0, mens
C-siden ikke har noen unntaksvei i det hele tatt. `std`, `corr`, `zscore` og
`skew` er skrevet om, og totalitetstesten holder det fast.

### 4.2 Prøvearenaen (D4–D5)

Formålet søket ble pekt mot, valgt fordi det er nøyaktig det v17 manglet:

> Finn en skalar observabel av sluttgrafen hvis **parede** respons på en endring
> i omskrivingsregelen slår det samme søket oppnår på permuterte armetiketter,
> og som beholder responsen på startseeds den ikke ble valgt på.

Designet er paret: begge armnivåer deler starttilstand, så start-familie-variansen
— størrelsen som forklarte 99,8 % av v17s primærgate — kanselleres ved
konstruksjon i stedet for ved håp.

- **Svak arm** (søkemålet): `p_local_rewire` 0,03 mot 0,09, 24 parede
  treningsseeds + 24 holdout-seeds, 20 000 hendelser per kjøring.
- **Sterk arm** (positiv referanse): `p_triadic_closure` 0,02 mot 0,30, 8+8 par.
- **Statistikk:** winsorisert paret studentisert middel. Nullen er *målt*, ikke
  antatt: å permutere armetiketten i et par er nøyaktig å snu fortegnet på
  differansen, så nullfordelingen kommer fra de samme differansene gratis.

To nuller, fordi det tas to ulike beslutninger:
`null_search` (95-persentil av **maksimum** over hele kandidatmengden — den
kontrollerer multippel-testing-problemet et søk skaper) gater utvalget;
`null_single` gater holdout, der nøyaktig én vinner måles.

**Kontrakten er admissibel:** positiv referanse 50,0 mot søkenull 5,05,
separasjon **9,9**. Instrumentet responderer beviselig når effekten er til
stede. På den sterke armen er søkenullen 37,2 med bare 8 par — en direkte
måling av hvor mye et søk over 9 000 kandidater blåser opp maksimumsstatistikken.

**Resultat på svak arm** (9 000 distinkte kandidater, dybde 3):

| | score | gate | |
|---|---|---|---|
| utvalg (train) | 8,019 | 5,051 | PASS |
| holdout | 3,284 | 2,048 | PASS |
| beste håndplukkede på holdout (β₁) | 2,641 | | |

**Replikasjon på 24 helt ferske seeds** (`seed-base 500000`), der kun den
forhåndsregistrerte vinneren ble målt:

| observabel | replikasjon | perm. p |
|---|---|---|
| **vinner** `sq(sq(vmin(vshift(tokdeg, beta1))))` | **4,943** | < 0,0001 |
| β₁ | 4,262 | 0,0001 |
| middelgrad | 1,442 | 0,171 |
| n | 1,275 | 0,230 |
| middelklynging | 0,581 | 0,573 |
| ... alle ti håndplukkede | ≤ 4,262 | |

Vinneren slår alle ti håndplukkede observabler på seeds den aldri så under
utvelgelsen.

### 4.3 Hva vinneren faktisk er

Tre uavhengige søkeseeds ga tre uttrykk:

```
seed 20260908 : sq(sq(vmin(vshift(tokdeg, beta1))))     train 8,02  holdout 3,28
seed 111      : sq(sq(median(vshift(tokdeg, beta1))))   train 8,15  holdout 3,69
seed 222      : sq(sq(beta1))                           train 7,78  holdout 3,44
```

Alle tre er β₁ i fjerde potens. Spearman-korrelasjon mellom vinner og β₁ på
replikasjonssettet: **0,98**. Transformasjonsstigen, målt på alle tre splittene:

| | train | holdout | replikasjon |
|---|---|---|---|
| log(β₁) | 5,56 | 2,40 | 4,05 |
| √β₁ | 5,92 | 2,52 | 4,16 |
| β₁ | 6,27 | 2,64 | 4,26 |
| β₁² | 6,92 | 2,90 | 4,40 |
| β₁⁴ | 7,78 | 3,44 | 4,43 |
| β₁⁸ | 7,34 | 4,28 | 3,95 |

Konvekse transformasjoner øker statistikken, konkave senker den, konsistent over
alle tre splittene. Den nærliggende lesningen er at søket fant en bedre
parametrisering. **Den lesningen holder ikke, og det er verdt å se hvorfor.**

#### Dekomponeringen som avgjør det

β₁ er alltid positiv, og x⁴ er strengt voksende på positive tall. Da er
`sign(hi⁴ − lo⁴) = sign(hi − lo)` for hvert eneste par. **Hele β₁-stigen har
identisk fortegnsvektor.** En transformasjons­invariant test kan derfor ikke
skille dem i det hele tatt — og gjør det heller ikke:

| | fortegn (train) | p | fortegn (holdout) | p | fortegn (repl.) | p |
|---|---|---|---|---|---|---|
| log(β₁) | 23/24 | <10⁻⁵ | 20/24 | 0,0015 | 20/24 | 0,0015 |
| β₁ | 23/24 | <10⁻⁵ | 20/24 | 0,0015 | 20/24 | 0,0015 |
| β₁⁴ | 23/24 | <10⁻⁵ | 20/24 | 0,0015 | 20/24 | 0,0015 |
| β₁⁸ | 23/24 | <10⁻⁵ | 20/24 | 0,0015 | 20/24 | 0,0015 |
| **vinner** | 23/24 | <10⁻⁵ | **20/24** | 0,0015 | **21/24** | **0,00028** |

Hele forskjellen mellom 2,64 og 3,44 på holdout — og mellom 4,26 og 4,43 på
replikasjon — er **omvekting av par**, ikke ny retningsinformasjon. Statistikken
er ikke invariant under monotone transformasjoner, og en potens flytter massen
mot de parene der β₁ er stor. Om den omvektingen er en reell styrkegevinst
(parene med stor β₁ er mer pålitelige) eller en artefakt av at winsorisering ved
90-persentilen presser flere par opp mot taket med samme fortegn, kan ikke
avgjøres av tallene i tabellen over.

Det som **er** avgjort: vinneren er ikke en monoton omskrivning av β₁. Den er
(β₁ − min(tokdeg))⁴, og fortegnsvektoren dens skiller seg fra β₁ sin på både
holdout og replikasjon. På replikasjonssettet får den ett par til riktig vei:
21/24 mot 20/24, sign-test p 0,00028 mot 0,0015.

#### Resultatet, slik det står

> Søket bestod begge forhåndsregistrerte gater og replikerte på ferske seeds.
> Dekomponert med en transformasjonsinvariant test er den reelle gevinsten
> **ett par av 24**. Resten av det som så ut som en gevinst er statistikken som
> belønner en omparametrisering.

Det er et ærlig, lite, positivt resultat — og funnet av det er mindre verdt enn
måten det ble avslørt på. Se punkt 7 i del 5.

### 4.4 Kompilering (D6)

Den utvalgte grafen, gjort til komposittnode, inlinet, senket til C, sertifisert
mot referansen, og målt på 20 000 kall med `|tokdeg| = 3200`:

| | µs/kall | mot tolk |
|---|---|---|
| referansetolk | 899–1019 | 1,00× |
| Python-kodegenerering | ~samme | **0,86–0,99×** |
| C, marshalling hvert kall | 299–312 | 3,0–3,3× |
| C, input allerede residente | 3,4–3,5 | **265–289×** |

Spennet er fire kjøringer på en maskin som samtidig kjørte Codex-køen; en enkelt
kjøring under last ga 1,46× for marshalling-raden. Bruk ikke ett av tallene som
en presis måling. Poenget er avstanden mellom de to nederste radene, og den er
to størrelsesordener uansett hvilken kjøring du leser.

---

## 5. Det som dokumenterbart ikke virket

Ført opp her så det ikke gjøres om igjen.

1. **Kodegenerering til Python ga null gevinst (0,86–0,99× over fire kjøringer).** Dispatch var aldri
   flaskehalsen; op-kroppene er det. Gevinsten kommer av å *forlate* Python,
   ikke av å generere den penere.
2. **Å krysse språkgrensen per kall spiser nesten hele kompilerings­gevinsten:
   ~3× mot ~275×.** Dette er den viktigste enkeltmålingen i hele arbeidet, og
   den har direkte konsekvens for HAVEN: et kompilert Goal-uttrykk må evalueres
   *der dataene ligger*, inne i cellen, ikke kalles ett og ett utenfra.
3. **Blind nivå-for-nivå enumerering var uframkommelig.** Dybde 1 ga alene 260
   skalarer og 281 vektorer; produktet med hver binære op er millioner av
   nesten-ekvivalente uttrykk, og kjøringen ble drept etter 170 s uten å nå
   dybde 2. Måtte skrives om til trinnvis søk (vektorrørledninger →
   reduksjoner → skalar­algebra → prediktater) med eksplisitt budsjett per trinn.
4. **Første statistikkvalg (median/MAD) var degenerert ved n = 8.** Med
   tilnærmet konstante differanser blir MAD null under fortegns-permutasjon, og
   nullreferansen traff taket. Byttet til winsorisert paret studentisert middel.
   Merk at feilen ble *oppdaget av at nullen ble målt* — hadde nullen vært
   antatt, ville den passert ubemerket. Det er samme feilklasse som v17s.
5. **Effektstørrelse uten √n har nesten ingen styrke** mot en liten, men helt
   konsistent respons — som er nettopp det alternativet som betyr noe her.
6. **Søket fant ingen ny størrelse.** Det gjenfant β₁ i tre uavhengige kjøringer.
   Det er et ærlig delvis negativt resultat, ikke en suksess som skal rundes opp.
7. **«Sertifisert» var for sterkt ord, og konformansharnessen var for svak til
   å bære det.** C-backenden ga et stille galt svar — 11,6 % relativ feil — for
   en graf med seks vektor-mellomresultater på 400 000 elementer, samtidig som
   den bestod konformansprøven. Årsaken: arenaen mettet ved å returnere sin egen
   basepeker, så rørledningen aliaset sitt eget input; og prøven trakk aldri
   vektorer lengre enn 128, så den kunne ikke se det. Første rettelse var verre
   enn feilen: å flagge overflow men fortsatt gi ut basepekeren lot kallerne
   skrive utenfor bufferet, altså minnekorrupsjon i stedet for et galt tall —
   det ga segfault i testsuiten. Riktig rettelse er at allokering **feiler**:
   NULL, hver kaller sjekker, en mislykket vektor har lengde 0 så ingen løkke
   skriver noe, og inngangspunktet gjør flagget om til NaN som Python-siden
   reiser som `ArenaTooSmall`. Arenaen dimensjoneres nå fra grafens antall
   vektor-mellomresultater og inputlengden. Verifisert: korrekt på 2 000 000
   elementer, og 810 kall over alle 45 noder med utsultet arena uten krasj.
   **Lærdommen er ikke om arenaer.** Den er at en konformansprøve bare beviser
   noe innenfor fordelingen den trekker fra, og at et ord som «sertifisert»
   inviterer til å glemme det. Prøven trekker nå også 4 096 og 20 000.
8. **Formålskontrakten har en systematisk skjevhet jeg ikke forutså, og som er
   det viktigste funnet i hele arbeidet.** Statistikken er ikke invariant under
   monotone transformasjoner. Uttrykksrommet er full av slike transformasjoner.
   Et søk vil derfor *systematisk* klatre i transformasjonsretningen framfor i
   mekanismeretningen, fordi det er den billigste veien til en høyere score — og
   en score som stiger fra 2,64 til 3,44 ser ut som framgang selv når
   fortegnsvektoren, og dermed all retningsinformasjon, er bit-for-bit uendret.
   Dette er samme feilklasse som v17s: en gate som beveger seg av noe annet enn
   det den skulle måle. Den ble her fanget fordi kontrakten tvang fram en
   dekomponering, ikke fordi jeg mistenkte den. Rettelsen står som port 4, og den er gjennomført.

---

## 6. Hva som gjør dette verdt noe for HAVEN spesielt

Dette er argumentet som ikke avhenger av at søkedelen imponerer.

**Goals som uttrykk har ikke hatt kjøremotor.** Beslutningen om at Goals skal
kunne være både prompts og matematiske uttrykk / event-predikater — fordi
uttrykk er langt billigere enn tokens — forutsetter et substrat som er typet,
komponerbart, billig å evaluere og trygt å kompilere. Det er nøyaktig det som
ligger i `core.py` + `library.py`. `bool`-typen med `gt`/`lt`/`and`/`or`/`ifelse`
*er* event-predikatene. Målingen i 5.2 sier hvor den må kjøre.

**Metoden blir data, ikke prosa.** Kravet om at HAVENs dekomponering og analyse
ikke skal lekke ut i tekst, men ligge i celler som utfører operasjonen, er
vanskelig å oppfylle med instruksjoner til en modell og lett å oppfylle med en
graf: en nodegraf *er* en metode representert som data, med deklarerte grenser,
uten en eneste linje forklarende prosa som må følge med.

**Formålskontrakten er PDD-akseptansen, mekanisert.** Arbeidsflyten krever at
tester utledes av formålene og at G3 måles mot en forventningskontrakt.
`PurposeContract` er den kontrakten i kjørbar form, med den ene tilleggsregelen
v17 kjøpte dyrt: uten målt null *og* målt positiv referanse gates det ikke i det
hele tatt.

**Og for UniverseSimulation:** v17 brukte elleve runder på en primærstørrelse
som var 0,1 % følsom for det den skulle teste. Å søke observabelrommet under en
målt null er ikke en omvei rundt det problemet. Det er verktøyet for det.

---

## 7. Hva jeg ville krevd før mer investering

Fem porter. Hver har et tall, ikke en vurdering.

1. **Swift-backend med samme konformanskontrakt.** Uten den kjører Goals ikke
   der de skal. Port: alle 45 noder, 250 tilfeldige input, 0 avvik — samme
   prøve som C bestod.
2. **Ett funn som ikke er en omskrivning av noe biblioteket allerede hadde.**
   Port: Spearman mot enhver enkelt kanal < 0,9 på et replikasjonssett, med
   permutasjons-p < 0,01. Dagens kjøring er på 0,98 og består ikke.
3. **Språkmodell-forslagsstiller målt mot enumeratoren på samme kontrakt.**
   Port: bedre holdout-score per brukt krone enn det deterministiske søket.
   Grensesnittet (`search.Proposer`) er ferdig; målingen er ikke gjort, og
   påstanden om at modellen hjelper er derfor ubelagt.
4. **Transformasjonsinvarians i kontrakten.** En kandidat skal ikke kunne slå
   en annen på score alene når de to har identisk fortegnsvektor. Port: kontrakten
   må rapportere både den vektede statistikken og en transformasjonsinvariant
   test, og et funn teller bare som funn når *begge* forbedres. Dette er en
   endring i `purpose.py`, ikke en anbefaling. **Den er gjort** — kontrakten
   rapporterer nå fortegnstesten ved siden av den vektede statistikken, og
   `PurposeContract.evaluate` merker et funn som `transform_only` når
   fortegnsvektoren ikke er bedre enn referansens.
5. **Én formålskontrakt skrevet for noe utenfor denne arenaen** — en Palazzo-
   eller Kallimachos-Goal — som består sin egen admissibilitetsprøve. Det er
   den prøven som avgjør om «å beskrive formålene» er løsbart i praksis eller
   bare i denne ene sandkassen.

Faller port 2 og 3 begge, står fortsatt kjernen, kompilatoren og
formålskontrakten igjen som nyttige for HAVEN. Da er det dét dette er, og det
bør sies rett ut i stedet for å holdes åpent.

---

## 8. Kjøre det

```bash
cd Tools/nodegraph
python3 tests/test_nodegraph.py                    # 19 tester
python3 arena/build_substrate.py --arm weak        # ~80 s
python3 arena/build_substrate.py --arm strong --train-seeds 8 --holdout-seeds 8
python3 run_experiment.py --depth 3 --only strong  # positiv referanse
python3 run_experiment.py --depth 3 --only weak    # søket
python3 replicate.py                               # ferske seeds
python3 demo_compile.py                            # konformans + speedup
```
