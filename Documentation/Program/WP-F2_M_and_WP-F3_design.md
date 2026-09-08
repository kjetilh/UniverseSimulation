# WP-F2 modus M, WP-H, og design av WP-F3 — med Astra og rådgiverpanel

Repo: /Users/kjetil/Build/Digipomps/HAVEN/UniverseSimulation, gren
`losen/nodegraph-vurdering-20260908`, HEAD `3ab0fd5`.
Fingeravtrykk: `influence-order-geometry-calibration` (forsøk 3) og, for del C,
et nytt: `universe-influence-order-form-test-design`.
Utsendt 8. september 2026 av Claude (Losen) på oppdrag fra Kjetil.

Les først, i denne rekkefølgen: `WP-F2_amendment_2.md`,
`WP-F2_amendment_1.md`, `WP-F2_influence_order_calibration.md`,
`Documentation/Geometribevarende_orden_2026-09-06.md`,
`Tools/nodegraph/INSTRUKSJONER.md`.

**Kjetil har bestemt at Astra (gpt-6-astra) skal brukes i denne pakken, og at
dere sammen skal komme fram til hvordan dette testes ut. Bruk rådgiverpanel.**
Del A og B er deterministisk arbeid Codex gjør alene. Del C er den delen Astra
og rådgiverne er til for.

---

## Formål

To ting, som ikke må blandes:

1. **Ferdigstille kalibreringen.** Bærer innflytelsesordenen underlagets
   dimensjon også når metrikken er frosset (modus M)? Og skiller
   tilstandsgrafens egen dimensjon seg fra en gradbevarende null (WP-H)?
2. **Finne ut hva som faktisk kan måles på universet.** Kalibreringen er ikke
   svaret på lesning G. Den er instrumentet. WP-F3 finnes ikke, og skal
   designes her — ikke kjøres.

Hvert steg under måles mot ett av disse to. Blander et steg dem, er steget feil.

---

## Del A — Modus M (Codex alene)

Modus M er kjørt for ring (2 historier ligger på disk). Resten mangler.

1. Kjør ferdig M for alle fire underlag, fire seeds hver, 8192 steg, med
   seed-policy `mark` som avklart i `WP-F2_M_seed_resolution.json`.
2. Analyser med amendment 2s grid (τ = 0,25·2^(k/4) til T/2, α og γ på minst
   seks punkter, γ på middelavstand).
3. Evaluer **F2a** (formskille: ring/lat2/lat3 skal foretrekke potenslov, rrg
   eksponentiell — rapporter R² for begge former per historie) og **F2b**
   (α-rekkefølge med disjunkte KI blant potenslov-underlagene), samt
   mekanismeleddet γ ≤ 0,10 spenn.
4. Rapporter M ved siden av R i `WP-F2_report.md`. Tersklene er frosset.

**Dette er den avgjørende sammenligningen i hele pakken.** I R drifter
underlaget 10–20 % under målingen; i M står det stille. Er α-tallene like i M
og R, måler instrumentet geometrien og ikke driften. Er de ulike, si hvor mye
og i hvilken retning.

## Del B — WP-H (Codex alene)

Kjør som spesifisert i `WP-F2_influence_order_calibration.md`, del WP-H:
tilstandsgrafenes `d_vol(r)` for r ≤ 10 og spektraldimensjon `d_s` mot en
gradbevarende konfigurasjonsnull, med gitter og ring som positive referanser.
Forhåndsregistreringen ligger i `WP-H_frozen.json`. Terskel uendret.

---

## Del C — Design av WP-F3, sammen med Astra

Dette er ikke en kjøring. Leveransen er et **spesifikasjonsutkast** som kommer
tilbake til Claude og Kjetil for gating. G1 gjelder: den som skriver koden
skriver ikke gaten, og Codex og Astra skriver her et forslag, ikke en godkjent
gate.

### Problemet som skal løses

Kalibreringen har fire underlag med **kjent** dimensjon. Universet har ingen.
F2b — «α skal ordne seg riktig» — kan derfor ikke brukes på universet i det
hele tatt: det finnes ingen riktig rekkefølge å sjekke mot. Uten en erstatning
er hele kalibreringen et instrument uten et spørsmål.

Det som *kan* overføres er F2a, fordi den er en **binær egenskap med målt
referanse på begge sider**: 16 av 16 kalibreringshistorier falt på riktig side
av potenslov mot eksponentiell, uten unntak. Spørsmålet «foretrekker universets
fortidsvolum en potenslov eller en eksponentiell?» har dermed en målt null og en
målt positiv referanse allerede, og er billig å stille.

**Dette er Claudes forslag, og det er ufullstendig.** Det svarer på om universet
har *en* dimensjon, ikke *hvilken*, og det er ikke opplagt at et enkelt
R²-sammenligningskriterium tåler å flyttes til et underlag som ikke ligner noen
av de fire. Deres jobb er å angripe det og komme fram til noe bedre, eller vise
at det er det beste som finnes.

### Konkrete spørsmål dere skal svare på

- Hva er nullen for universets α, når ingen kjent dimensjon finnes? Er
  gradbevarende omkobling av sluttgrafen (WP-H-nullen) riktig null også her,
  kjørt gjennom samme dynamikk?
- Universets tilstandsgraf har ~1024 noder og vokser knapt, men den *redigeres*
  hele veien. Er det nærmere modus R eller modus M? Kalibreringen har bare målt
  drift på 10–20 %; universets egen drift skal måles før den sammenlignes.
- Hvis universet foretrekker eksponentiell: er det ekspander-lik, eller er det
  et endelig-størrelse-artefakt? Kalibreringen har ett ekspander-punkt.
- Hvis det foretrekker potenslov: hva er α, og hva slags utsagn er det da
  lov å gjøre? Skriv formuleringen som *ville* vært tillatt, på forhånd, for
  begge utfall — så den ikke skrives etter at tallet er sett.
- Hvor mange historier og hvor lange kjøringer kreves for at α-KI-et blir
  smalere enn avstanden mellom kalibreringens nabodimensjoner (≈0,7)?

### Rådgiverpanel

Bruk mønsteret fra `CellScaffold/Deliverables/PDD_radgiverpanel-og-persona_2026-09-05`.
**Panelet skal ikke kjøre uten minst én rådgiver som har i oppgave å motsi.**
Gi den rådgiveren disse fire påstandene å rive ned, og skriv svarene ordrett i
rapporten:

1. At α = 1 + d_s/2 er bekreftet. Det er tre underlag, ett av dem bommer med
   0,26, og ring/lat2-separasjonen er 0,014. Tre punkter er lite.
2. At formskillet er en dimensjonsdiagnose. Alternativ forklaring: rrg har
   diameter ~10 mot lat3s 15, så vandreren når en større *andel* av grafen,
   og kurven bøyer av. Det ville også gi «eksponentiell foretrekkes» uten at
   dimensjon er årsaken. Kan dette skilles med data som allerede finnes?
3. At modus M måler det samme som R. Mark-koblingen ε = 0,25 ble frosset av
   Claude uten begrunnelse. Er ε stor nok til å bære innflytelse i det hele
   tatt, og hvordan ser vi forskjell på «M bekrefter R» og «M har for svak
   kobling til å måle noe»?
4. At γ-bruddet (0,129) er ringens skyld. Den forklaringen er ikke målt, bare
   foreslått av Claude.

### Standarden ethvert forslag skal bestå

`Tools/nodegraph/purpose.py` sine tre nektelser, anvendt på det dere foreslår,
før dere leverer: målt null; målt positiv referanse; og at statistikken kan
skille sine egne to referanser. Består ikke forslaget dem, skal det ikke
leveres som forslag — det skal leveres som «her er grunnen til at dette ikke
lar seg måle». Det er et fullgodt utfall.

Merk at nettopp den tredje nektelsen felte WP-F2-gaten: den krevde en
eksponentordning av et underlag som ikke har en eksponent. Tre spec-feil på rad
i denne pakken kom av samme antakelse — at referansene deler en egenskap, uten
at det ble målt. Se etter den feilen i deres eget forslag.

---

## Leveranser

- `Documentation/Program/WP-F2_report.md` oppdatert med modus M og F2a/F2b.
- `Documentation/Program/WP-H_report.md` med målte tall.
- `Documentation/Program/WP-F3_design_draft.md`: forslaget, panelets
  sammensetning, motrådgiverens innvendinger ordrett, og hva dere endret på
  grunn av dem. Hvis ingenting ble endret, skriv hvorfor.
- `Documentation/Program/WP-F3_advisor_transcript.md` eller tilsvarende rådata.

## Regler

- Ingen ny dynamikk på universets historier i denne pakken. Del C er design.
- Terskler i F2/H er frosset. Argumenter mot dem i teksten; ikke endre dem.
- Hjerteslag hvert femte minutt og ved hvert delsteg til
  `.program_logs/WP-F2M.heartbeat` og `.program_logs/WP-F3design.heartbeat`.
  **Forsøk 2 kjørte uten å skrive én eneste hjerteslaglinje. Ikke gjenta det** —
  vakten leser filen for å skille «arbeider» fra «død».
- Stoppregel G3: to forsøk på samme feil, tredje gang «Blokkert».
- `git add` bare egne filer. Kan sandkassen ikke skrive `.git`: si det i
  rapporten og stopp. Integratoren committer. Ingen push.
- Ingen fysikkpåstand. Ingen konklusjon sterkere enn tallene.
