# WP-F3 — designoppdrag til Astra: hva kan faktisk måles på universet?

Til: Astra (gpt-6-astra).
Fra: Losen (Claude), spesifikasjonsforfatter. Sendt 14. september 2026.
Fingeravtrykk: `universe-influence-order-form-test-design`.
Alle stier er relative til `UniverseSimulation/`.

Dette er del C av `Documentation/Program/WP-F2_M_and_WP-F3_design.md`. Del A og B er
utført og committet; del C ble ikke levert da Codex avsluttet, og sendes nå alene.

**Leveransen er et spesifikasjonsutkast, ikke en kjøring.** G1 gjelder: du foreslår,
Claude og Kjetil gater. Ingen ny dynamikk skal kjøres på univershistorier i dette
oppdraget.

---

## Les først

1. `Documentation/Geometribevarende_orden_2026-09-06.md` — mekanismeargumentet som
   avgjorde at ingen orden i denne dynamikken kan være Lorentz-lik, og hvorfor
   spørsmålet ble flyttet til «lesning G» (finnes en geometri med stabil,
   null-separert dimensjon).
2. `Documentation/Program/WP-F2_amendment_2.md` — kalibreringens resultat.
3. `Documentation/Program/WP-H_report.md` — særlig avsnittet om frakoblede nuller.
4. `Tools/nodegraph/INSTRUKSJONER.md` — de tre nektelsene, som er standarden.
5. `Documentation/Program/UC1_report.md`, `UC2_report.md`, `UC3_report.md` — se §3.

## 1. Hva som er målt, og som du kan bygge på

Innflytelsesordenen (kernel-lesesettet, ikke v16as konflikt-DAG) er kalibrert på fire
underlag med kjent dimensjon. Fortidsvolumets eksponent α i |J⁻(e,τ)| ∝ τ^α:

| underlag | kjent d | α modus R | α modus M | forhåndssagt 1 + d_s/2 |
|---|---|---|---|---|
| ring | 1 | 1,621 | 1,668 | 1,50 |
| lat2 | 2 | 2,054 | 2,226 | 2,00 |
| lat3 | 3 | 2,756 | 2,868 | 2,50 |
| rrg (ekspander) | ∞ | 1,757 | 1,939 | — |

Rekkefølgen holder for de tre endelige underlagene med disjunkte KI, og prediksjonen
1 + d_s/2 ble skrevet ned før måling. Modus M (frosset metrikk) reproduserer modus R
(metrikken drifter 10–20 %), så driften er ikke det som lagde signalet.

Ekspanderen har ingen eksponent: fortidsvolumet vokser eksponentielt. Tilpasser man
begge former over fit-vinduet, skiller R² dem **16/16 i modus R og 14/16 i modus M**.
Den gamle v16a-ordenen gir `nan` på de samme historiene — den kan ikke måle dette.

γ-leddet feiler (spenn 0,129 mot kravet 0,10) og er ikke lempet på.

## 2. Problemet du skal løse

Kalibreringen har fire underlag med **kjent** dimensjon. Universet har ingen. Derfor
kan ordningskriteriet — «α skal ordne seg riktig» — ikke overføres i det hele tatt:
det finnes ingen fasit å sjekke rekkefølgen mot. Uten en erstatning er kalibreringen
et instrument uten et spørsmål.

Det som *kan* overføres er formskillet, fordi det er en **binær egenskap med målt
referanse på begge sider**. Spørsmålet «foretrekker universets fortidsvolum en
potenslov eller en eksponentiell?» har allerede målt null og målt positiv referanse.

**Dette er Losens forslag, og det er ufullstendig.** Det svarer på om universet har
*en* dimensjon, ikke *hvilken*, og det er ikke opplagt at et R²-sammenligningskriterium
tåler å flyttes til et underlag som ikke ligner noen av de fire. Angrip det, og kom
fram til noe bedre — eller vis at det er det beste som finnes.

## 3. Det som har endret seg, og som du må ta stilling til

Etter at kalibreringen ble gjort gikk prosjektet tilbake til grunnspørsmålet i UC1–UC3
(9.–11. september). Der ble selve universmodellen revidert: en kontrollert flytelov for
endringsenheter (UC2), så en lokal regel for fødsel, kollaps og kutt (UC3). UC3-utfallet
var at alle 16 kjøringer fikk flere noder, men **endte med samtlige endringsenheter
isolert**.

Det gjør ett spørsmål uunngåelig, og det er ditt første:

> **Hvilke historier skal WP-F3 måle på?** De gamle v16b/v16c/v16d-historiene
> instrumentet ble kalibrert mot, eller UC-seriens? Er det i det hele tatt meningsfylt
> å måle fortidsvolum på en historie der endringsenhetene ender isolert — eller er
> isolasjonen i seg selv svaret på lesning G for den regelen?

Svar på det før du designer testen. Er svaret at ingen av dem egner seg, er det et
gyldig og nyttig utfall.

## 4. Konkrete spørsmål

- Hva er nullen for universets α, når ingen kjent dimensjon finnes? Er gradbevarende
  omkobling av sluttgrafen riktig null her, kjørt gjennom samme dynamikk?
- WP-H brukte en gradbevarende null der **alle 96 nullgrafer ble frakoblede** mens alle
  12 universgrafer var sammenhengende, og aggregeringsvalget snudde fortegnet
  (rot-median: universet under nullen 96/96; middelkurve: over 96/96). Hva er riktig
  sammenhengsbetinget null, og hvilken aggregering skal forhåndsregistreres?
- Hvis universet foretrekker eksponentiell: ekspander-likt, eller endelig-størrelse?
  Kalibreringen har bare ett ekspander-punkt.
- Hvis det foretrekker potenslov: hva er α, og hvilket utsagn er da tillatt? Skriv
  begge formuleringene **på forhånd**, for begge utfall, så de ikke skrives etter at
  tallet er sett.
- Hvor mange historier og hvor lange kjøringer kreves for at α-KI-et blir smalere enn
  avstanden mellom kalibreringens nabodimensjoner (≈0,7)?

## 5. Fire påstander du skal rive ned

Du har rollen som pålagt motrådgiver. Svar ordrett på hver, i utkastet:

1. **At α = 1 + d_s/2 er bekreftet.** Tre underlag, ett bommer med 0,26, og
   ring/lat2-separasjonen er 0,014. Tre punkter er lite.
2. **At formskillet er en dimensjonsdiagnose.** Alternativ forklaring: rrg har diameter
   ~10 mot lat3s 15, så vandreren når en større *andel* av grafen og kurven bøyer av.
   Det ville også gi «eksponentiell foretrekkes» uten at dimensjon er årsaken. Kan det
   skilles med data som allerede ligger i `Documentation/Program/WP-F2_*_curves.csv`?
3. **At modus M måler det samme som R.** Mark-koblingen ε = 0,25 ble frosset av Losen
   uten begrunnelse. Er ε stor nok til å bære innflytelse, og hvordan ser vi forskjell
   på «M bekrefter R» og «M har for svak kobling til å måle noe»?
4. **At γ-bruddet (0,129) er ringens skyld.** Den forklaringen er foreslått av Losen og
   ikke målt.

## 6. Standarden forslaget ditt skal bestå

`Tools/nodegraph/purpose.py` sine tre nektelser, anvendt på ditt eget forslag: målt
null; målt positiv referanse; og at statistikken kan skille sine egne to referanser.
Består det ikke, skal du ikke levere et forslag — lever «her er grunnen til at dette
ikke lar seg måle». Det er et fullgodt utfall.

Merk at nettopp den tredje nektelsen felte WP-F2-gaten: den krevde en eksponentordning
av et underlag som ikke har en eksponent. Fem spec-feil er registrert i denne pakken,
alle samme klasse — antatt at referansene deler en egenskap uten at det ble målt. Din
egen gjennomgang 8. september fant to av dem. Se etter den feilen i ditt eget forslag.

## 7. Leveranse

`Documentation/Program/WP-F3_design_draft.md`, med:

1. Svaret på §3 — hvilke historier, og hvorfor.
2. Forslaget: observabel, null, positiv referanse, forhåndsregistrert terskel, og de
   to tillatte konklusjonsformuleringene skrevet på forhånd.
3. Dine svar på de fire påstandene i §5, ordrett.
4. Hva du endret i Losens forslag, og hva du forkastet.
5. Kostnadsanslag: antall historier, kjøretid.
6. Det som ikke lar seg måle, og hvorfor.

Ingen push, ingen deploy, ingen RAG-sync. Ingen fysikkpåstand. Ingen konklusjon
sterkere enn tallene.
