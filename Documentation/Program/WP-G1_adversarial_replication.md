# WP-G1: Adversariell replikasjon av WP-F0

Repo: /Users/kjetil/Build/Digipomps/HAVEN/UniverseSimulation (gren master, HEAD e0b1321).
Fingeravtrykk: `wp-f0-independent-replication`.
Utsendt 4. september 2026 av Claude på oppdrag fra Kjetil.

## Formål

WP-F0 (`Documentation/Program/WP-F0_report.md`) konkluderer at hendelses-DAG-en er
en kjedebunt og at dimensjonsrunden ikke skal kjøres. Gate og kode har samme
forfatter (Claude). Det er et brudd på G1. **Din jobb er å prøve å velte
konklusjonen.** Lykkes du ikke, er det G1-kvitteringen. Lykkes du, er det et
viktigere resultat enn kvitteringen. Begge utfall skal skrives rett ut.

Du bekrefter ikke. Du angriper. En rapport som sier «jeg kjørte scriptet og fikk
samme tall» er ikke fullført pakke — det er steg 1 av 5.

## Steg 1 — Uavhengig reimplementasjon (ikke gjenbruk)

Skriv `Tools/causet_admissibility_replica.py` **uten å lese**
`Tools/causet_admissibility.py` først. Les kun spec-en
`Documentation/Program/WP-F0_dimension_admissibility.md` og v16b-koden. Implementer
G0.1–G0.4 og desimeringseksponenten fra spec-teksten alene. Bruk networkx fra
`.codex_pydeps` hvis det finnes der, ellers ren Python — men bruk en annen
datastruktur enn bitsett-heltall hvis du kan, så feilene ikke er korrelerte.

Kjør på samme 36 historier (v16b, v16c fin, v16d fin). Skriv
`Documentation/Program/WP-G1_replica_per_history.csv` med samme kolonner som
`WP-F0_admissibility_per_history.csv`.

**Først deretter** åpne `Tools/causet_admissibility.py` og diff tallene. Avvik
> 1 % på r, r_floor, h, lenker, maks|I| eller Θ skal forklares — hvem har rett,
og hvorfor. Avvik i s innenfor bootstrap-KI er ventet (ulik RNG).

## Steg 2 — Angrep på premissene

Svar på hvert punkt med målte tall, ikke resonnement:

1. **Er kjedebunt-referansen riktig null?** Bunten i WP-F0 er 32 × 64 disjunkte
   kjeder. Historiene har h = 41–72 og *vekselvirkende* tråder (maks|I| opptil 0,11 N
   mot buntens 0,03). Konstruer en referanse som er en bunt *med* tilfeldige
   tverrkanter kalibrert til historienes rå kantetall (1,14/hendelse) og mål alle
   fire G0-størrelser + s på den. Hvis den treffer historiene på alt, er
   «kjedebunt» riktig ord. Hvis den ikke gjør det, si hva historiene er i stedet.

2. **Er G0.2 en feil terskel for denne DAG-definisjonen?** DAG-en er en
   konflikt-DAG (RAW/WAW/WAR på ressurser). Slike DAG-er har strukturelt lave
   lenketall uansett geometri, fordi hver hendelse berører få ressurser. Test:
   ta d=2-sprinklingen, tilordne hver hendelse 1–3 tilfeldige ressurser, bygg
   konflikt-DAG-en på samme måte som `DependencyDAG.add`, og mål lenker/hendelse
   og Θ. Hvis en ekte 2D-sprinkling *gjennom konflikt-DAG-konstruksjonen* også
   gir lenker ≈ 1 og Θ ≈ 1, måler ikke WP-F0 geometrien — den måler
   konstruksjonen. Det ville velte konklusjonen.

3. **N-trenden.** Θ-median går 1,24 → 1,66 fra N=2048 til 3072 mens r er flat.
   Det finnes v16-historier med andre N (sjekk `v16c_coarse_*`, `v16f_depth_coarse_*`,
   `v16h_*`, `v16k_*`, `v16m_*`, `v16n_*`, `v16s_*`; noen er grovkornede, noen fine).
   Finn alle fine hendelses-DAG-er på disk med N ≠ 2048/3072, mål Θ og r/r_floor,
   og tilpass Θ(N). Hvis Θ vokser med N, si hvilken N Θ ≥ 5 ville nås ved
   ekstrapolasjon, og hvor usikkert det er. Ikke kjør ny dynamikk.

4. **Desimeringseksponenten.** s ≈ 0,68 på historiene, 0,72 på bunten. For en
   ren bunt er teoretisk s = 1 (L ∝ p). Hvorfor måler vi 0,72 på bunten?
   (Hint: L≥8-vilkåret og at maks over 32 kjeder ikke skalerer som én.) Regn ut
   hva s *skal* være for en 32×64-bunt under nøyaktig denne prosedyren, og
   sjekk at målingen treffer. Hvis den ikke gjør det, er fit-prosedyren feil,
   og da er også historienes s upålitelig.

## Steg 3 — Angrep på koden

Les `Tools/causet_admissibility.py` linje for linje. Rapporter hver feil du
finner med linjenummer og en test som viser den. Særlig:
- `link_count`: er «ingen annen direkte forgjenger q har p som forfar» ekvivalent
  med dekkrelasjon? Bevis eller motbevis med et 5-elements poset.
- `max_interval`: teller `desc[p] & anc[q]` + 2 riktig?
- `decimate`: induseres delposetet fra transitiv *lukning* (som spec krever) eller
  fra kantene?
- `mm_dimension`: monoton? Hva returnerer den for r=0 og r=1?
- Bootstrap: resamples per p-nivå. Er det riktig enhet? Hva om man resampler
  historier i stedet?

## Steg 4 — Løp WP-A samtidig (separat commit)

`Documentation/Program/WP-A_beta1_audit.md` er uendret og ukjørt. Kjør den etter
egen spec. Det er en ren måling og har ingen berøring med steg 1–3.

## Steg 5 — Dom

`Documentation/Program/WP-G1_report.md` med:
1. Replika-tall mot WP-F0-tall, avvik forklart.
2. Svar på 2.1–2.4 med tall.
3. Kodefeil funnet, med tester.
4. **Én setning**: står konklusjonen «DAG-en er en kjedebunt, kjør ikke v18», eller
   faller den? Hvis den faller: på hvilket punkt, og hva er det riktige svaret.
5. Commit-hasher.
6. Blokkert.

## Regler

- Terskler i WP-F0-spec-en er frosset. Du kan argumentere mot dem i rapporten;
  du kan ikke endre dem.
- Ikke rør `Tools/causet_admissibility.py` eller `WP-F0_report.md`. Skriv ved
  siden av.
- Ikke rør `relational_universe_local_max_coupling_lab.py` (WP-A måler utenfra).
- Ingen ny dynamikk. Ingen fysikkpåstander.
- `git add` kun egne filer eksplisitt. Ikke `.DS_Store`. To commits:
  `WP-G1: adversarial replication of WP-F0` og `WP-A: measure beta1 bookkeeping fidelity`.
  Ikke push.
- Hjerteslag: én linje til `.program_logs/WP-G1.heartbeat` ved hvert delsteg og
  minst hvert femte minutt, `<ISO-tid> <status>`. Uten hjerteslag antas du død.
- Stoppregel G3: to forsøk på samme feil, tredje gang «Blokkert».
- Hvis økten din blir drept før du er ferdig: alt du har skrevet til disk teller.
  Skriv rapporten inkrementelt, ikke til slutt.
