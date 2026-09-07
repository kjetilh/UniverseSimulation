# Finnes det en orden i simuleringen som bevarer geometri?

Skrevet 6. september 2026 av Claude, etter WP-G1. Grunnlag: koden i
`relational_universe_local_max_coupling_lab.py` (kernel og hendelser),
`relational_universe_v16a_disjoint_event_commutation_gate.py` (`action_access`),
v16b-loggene, v13/v14-rapportene og WP-G1-rapporten. Alle tall under er lest
fra disk i dag; ingen ny dynamikk er kjørt.

## Formål

Avgjøre om det i denne simuleringen finnes en orden på hendelsene, eller en
projeksjon av dem, som *dokumenterbart* bevarer geometri — slik at en
dimensjonsmåling i det hele tatt måler noe. «Dokumenterbart» betyr: hele
kjeden dynamikk → ordensuttrekk → estimator er kjørt på et underlag med kjent
geometri og på en null, og estimatoren skiller dem. WP-G1 viste at WP-F0
manglet nettopp dette leddet. Hvert kandidatsvar under måles mot det kravet.

Spørsmålet har to lesninger som må holdes fra hverandre, for de har ulike
svar:

- **Lesning L (Lorentz):** finnes en kausalmengde-lik orden — en orden med
  lyskjegler — som en Myrheim–Meyer- eller kjedelengde-estimator kan gi en
  romtidsdimensjon til? Det var WP-F0/WP-F1s premiss.
- **Lesning G (graf):** finnes en geometri i det hele tatt — en metrikk med
  stabil, null-separert dimensjon — uansett om hendelsesordenen er Lorentz-lik?

## 1. Hva konflikt-DAG-en faktisk er — lest fra koden, ikke fra tallene

WP-F0 kalte den «kjedebunt», WP-G1 viste at en kalibrert bunt med tilfeldige
tverrkanter bommer med faktor 3. Begge hadde rett, og grunnen står i
`action_access`:

- 92 % av hendelsene er `move` (11 340 av 12 288 per arm i v16b). Et `move`
  leser `token:t`, `node:v`, `node:u`, `edge:v:u` — og **skriver bare
  `token:t`**. Ingen hendelse skriver `node:*` unntatt `seed` (7 av 12 288).
- Følgelig: to tokens som står på samme node, eller går over samme kant rett
  etter hverandre, **konflikterer aldri**. Romlig sammenfall er usynlig for
  ordenen per definisjon, ikke per tetthet.
- Målt: 25 561 av 27 931 DAG-kanter (91,5 %) har bare `token:*` som vitne, og
  23 450 av dem binder to hendelser til *samme* token. Tverrbindinger mellom
  tokens kommer bare fra `birth` (leser vertstoken, skriver nytt token — en
  slektskapsgaffel) og fra de 1,3 % strukturelle hendelsene (`swap`) som
  skriver `edge`/`adj`.
- Tokens: 17–26 ved start, 127–175 ved slutt. h = 41–64 ≈ lengste
  token-verdenslinje; N/h = 32–50 ≈ antall tokens. Tallene i WP-F0 er altså
  ikke et *funn* om dynamikken; de er en *avlesning av ressursmodellen*.

Riktig beskrivelse: konflikt-DAG-en er et **slektstre av token-verdenslinjer**,
sydd sammen bare der grafen ble redigert. Derfor bommer en tilfeldig-tverrkant-
bunt (tverrkantene er ikke tilfeldige, de er gafler og redigeringer), og derfor
kan ingen økning i steg per node redde den: flere `move` gir flere ledd i
kjedene og null nye tverrbindinger.

**Dom, kandidat A (konflikt-DAG-en):** bevarer beviselig ikke geometri under
lesning L. Ikke fordi den er tynn, men fordi skrivesettet er valgt slik at
posisjon aldri skrives. WP-G1s d=2-moteksempel er et symptom på dette.

## 2. Hva dynamikken faktisk lar hendelser påvirke hverandre gjennom

For å finne en orden som *kan* bære geometri må man spørre hva som faktisk
overfører innflytelse. Fra kernelen:

- Tokens vekselvirker **ikke** med hverandre direkte. `local_token_kernel`
  for token t leser bare t-ets posisjon, naboene, naboenes naboer og grader.
  Andre tokens' posisjoner inngår ikke.
- Tokens vekselvirker med **grafen**: `delete`/`triad`/`swap` endrer kanter;
  `birth`/`death`-vekter leser graden der tokenet står. Grafen er det delte
  mediet.
- Den eneste kanalen mellom to tokens er derfor: A redigerer grafen ved v; B
  kommer senere til v og B-ets kernel *leser* den endrede naboskapen. Merk at
  `action_access` for `move` **ikke** registrerer det kernelen leste (naboer
  av v, naboer av u, grader) — bare den ene kanten som ble brukt. Statistisk
  avhengighet (B valgte annerledes fordi A la til en kant) er usynlig for
  konflikt-DAG-en selv der den finnes. Kommutasjonsauditen i v16a fanger
  ikke dette: den tester at *tilstanden* blir lik når to erklært disjunkte
  hendelser byttes, ikke at *sannsynlighetene* var upåvirket.

Dette gir to ordener som er intrinsiske i en sterkere forstand enn
konflikt-DAG-en:

**Kandidat B — kernel-leseordenen.** Utvid lesesettet til alt kernelen
evaluerte (2-hopps naboskap og grader ved v), behold skrivesettene. Hendelse
B avhenger av A hvis A skrev noe B-ets kernel leste. Dette er den vanlige
måten å definere lyskjegler for lokale oppdateringsregler (Lieb–Robinson-
lesning). Den er billig: ett ekstra felt per hendelse i loggen. Men også
her skriver bare strukturelle hendelser noe andre leser; `move` skriver
fortsatt bare eget token. Tverrbindingene blir tettere enn i A, men de
bæres fortsatt av de 1,3 % redigeringene.

**Kandidat C — den kontrafaktiske skadeordenen.** B avhenger av A hvis
fjerning eller endring av A endrer B. Det er den egentlige innflytelses-
ordenen, og repoet har allerede instrumentet: koblede kjøringer i v7-laben
(`damage_snapshot`, `radius_from_support`, `estimate_front_speed`), brukt i
v14/v14c. B er en statisk tilnærming til C.

## 3. Hvorfor ingen av dem er Lorentz-like — og hva de er i stedet

Her ligger det avgjørende argumentet, og det er uavhengig av tetthet.

Innflytelse mellom to hendelser bæres av at et token *går* fra der A
redigerte til der B leser. Tokens går tilfeldig (kernelen velger nabo
uniformt, vektet av p_del/p_triad/p_swap). En tilfeldig vandrer på en graf
med endelig dimensjon sprer seg **diffusivt**: avstand ∝ √t. En kausalmengde
fra en Lorentz-romtid har lyskjegler: avstand ∝ t. Det er ikke en detalj.
Myrheim–Meyer, kjedelengde ∝ N^{1/d} og Alexandrov-intervallenes volumskalering
er alle avledet for Poisson-drysset i Minkowski-rom, altså for lineære kjegler.
På en diffusiv orden gir de tall, men tallene har ingen kjent tolkning.

v14 målte skadefronten direkte: effektiv fart 0,21–0,25 grafkanter per tidsenhet,
treffer r=2 etter ~9–14 og r=3 etter ~10–16 tidsenheter, og dommen var
«mode_dependent_not_yet» for Lorentz-likhet. Fronten ble bare fulgt til r=3 i
grafer med radius 7–12, så om den er ballistisk eller diffusiv er ikke
avgjort på disk. Men mekanismen — vandrende bærere — tilsier diffusiv, og
den forhåndsregistrerte forventningen bør være det.

**Konsekvens for lesning L:** en ballistisk (Lorentz-lik) orden finnes bare
hvis token-vandringen er ballistisk, og det er den ikke på en graf med
endelig dimensjon. Hvis grafen derimot er ekspander-lik (uendelig-dimensjonal),
er vandringen «rask», men da finnes ingen endelig dimensjon å måle. Begge
grener gir samme svar: **det finnes ingen orden i denne dynamikken som er
dokumenterbart Lorentz-lik, og det er ikke en målefeil — det følger av at
innflytelse bæres av tilfeldige vandrere.** v18 slik den var tenkt (WP-F1)
måler derfor feil ting uansett hvilken orden den får.

## 4. Det som faktisk kan måles — lesning G

At ordenen er diffusiv betyr ikke at den er tom for geometri. Den bærer
geometrien til *mediet*, tilstandsgrafen, gjennom to størrelser som begge har
kjente nuller:

1. **Fortidsvolumets vekst.** For hendelse e, la J⁻(e, τ) være hendelsene i
   e-ets fortid (under orden B eller C) innen tid τ bakover. På et d-dimensjonalt
   underlag dekker en vandrer ∼τ^{d/2} noder på tid τ, så |J⁻(e, τ)| ∝ τ^{1+d_s/2}
   der d_s er grafens spektral-/vandringsdimensjon. På en ekspander vokser
   det eksponentielt; på en ring som τ^{3/2}; på en 2D-flate som τ^2.
   Eksponenten er en dimensjonsmåling med null.
2. **Grafens egen metrikk.** v13 målte `dim_proxy` (kulevolum-eksponent,
   r ≤ 4) til 1,7–3,1 (median 2,4), spektralradius ~4, klynging ~0,12, og
   skaderadius 3–12. Det er en kandidat til «geometri» i lesning G. Den er
   aldri stilt mot nuller ved r > 4, og ved r ≤ 4 skiller kulevolum knapt et
   tre fra et gitter. Så også her mangler dokumentasjonen, men den er billig.

Disse to henger sammen: (1) er (2) sett gjennom dynamikken. Hvis de gir samme
d, har universet en stabil geometri som dynamikken respekterer. Hvis (1) gir
en annen eksponent enn (2), er det interessant på egne ben: da endrer
redigeringene metrikken raskere enn tokens rekker å utforske den.

## 5. Hva «dokumenterbart bevarer geometri» krever — kravet WP-F0 manglet

Kravet, formulert så det kan feiles:

> Ordensuttrekket (B eller C) kjøres på tre underlag med *samme* token- og
> redigeringsregel: (a) et fast 2D-gitter, (b) en tilfeldig regulær graf
> (ekspander), (c) en ring. Estimatoren (fortidsvolum-eksponent) må gi
> ≈2 på (a), ≈1 på (c) og divergere på (b), med spredning smalere enn
> avstanden mellom dem. Først da er ordenen dokumentert geometribevarende,
> og først da kjøres den på det relasjonelle universet.

Praktisk hindring: redigeringsregelen endrer underlaget, så (a) drifter bort
fra gitteret. To løsninger, begge legitime kontroller: enten frys metrikken
(erstatt strukturelle skrivinger med «maling» på noder som kernelen leser,
så bærerne fortsatt overfører innflytelse men geometrien står), eller velg
p_swap/p_triad/p_del så lave at driften over kjøringen er målbart under
oppløsningen. Begge er timer, ikke dager, fordi alt kjører på eksisterende
kode: v7-laben har koblede kjøringer, v16b har ordensuttrekket, WP-F0/WP-G1
har estimatorene.

## 6. Argumentanalyse — hvor dette kan være feil

- *Premiss: tokens vekselvirker ikke direkte.* Lest fra `local_token_kernel`
  i v7-laben. v16b bruker `adapter.family_kernel` (v16ac); sjekket i dag:
  adapteren delegerer uendret til `v7.family_kernel` (linje 113–114), så
  premisset holder for begge armer. Den lokale adapteren endrer bare *ratene*
  (`family_rates`), ikke hva et token kan se.
- *Premiss: vandringen er diffusiv.* Sann for tilfeldig nabovalg på grafer
  med endelig dimensjon. Kan feile hvis kernelen har retningshukommelse (den
  har ikke) eller hvis grafen er ekspander-lik (da finnes ingen dimensjon å
  tape). Testes av fortidsvolum-eksponenten selv: ballistisk gir τ^{1+d}.
- *Motargument: «Θ vokser med N (1,24 → 1,66)».* Med N/h ≈ antall tokens og
  tokens som vokser gjennom kjøringen er Θ-veksten en avlesning av
  fødselsraten, ikke av geometri. WP-G1 2.3 lot dette stå åpent; del 1 her
  forklarer det.
- *Motargument: «høyere p_swap gir tettere tverrbindinger og kanskje en annen
  orden».* Riktig at ordenen blir tettere; galt at den blir Lorentz-lik, for
  bærerne vandrer fortsatt. Det endrer eksponenten i (1), ikke dens natur.
- *Sterkeste innvending:* at lesning L er den eneste som teller for
  prosjektets tese («bakgrunnsløst univers → emergent romtid»). Da er svaret
  i del 3 et negativt resultat om tesen, ikke om målingen — og det bør
  skrives rett ut, ikke gjemmes i en dimensjonsrunde som ikke kan finne det.

## 7. Svar

**Lesning L:** Nei. Ingen orden i denne simuleringen kan dokumenteres
Lorentz-lik, fordi innflytelse bæres av tilfeldige vandrere og derfor sprer
seg diffusivt. Konflikt-DAG-en (A) er i tillegg konstruert slik at romlig
sammenfall aldri registreres. Kausalmengde-estimatorene har ikke noe objekt
her. Det er programmets svar på spørsmålet slik WP-F1 stilte det, og det står
sterkere nå enn etter WP-F0, fordi det følger av mekanismen og ikke av
terskler.

**Lesning G:** Ja, betinget. Kernel-leseordenen (B) og skadeordenen (C) bærer
mediets geometri gjennom fortidsvolumets vekst-eksponent, og tilstandsgrafens
egen metrikk er en uavhengig avlesning av det samme. Ingen av dem er
dokumentert ennå; kravet i del 5 er hva det koster, og det er timer.

**Anbefalt neste beslutning:** Ikke v18. I stedet én kalibreringspakke
(«WP-F2: geometribevaring av innflytelsesordenen») med tre underlag og
forhåndsregistrerte eksponenter, og én billig pakke for tilstandsgrafens
dimensjon mot nuller ved r ≤ 10. Består F2, er det relasjonelle universet
neste — med fortidsvolum-eksponent som primærobservabel, ikke Myrheim–Meyer.
Består den ikke, er svaret at heller ikke mediet har stabil geometri, og da
er det programmets sluttresultat.
