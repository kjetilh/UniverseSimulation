# WP-F2: Geometribevaring av innflytelsesordenen — kalibrering på kjente underlag

Repo: /Users/kjetil/Build/Digipomps/HAVEN/UniverseSimulation (gren master, HEAD b8e8891).
Fingeravtrykk: `influence-order-geometry-calibration`.
Utsendt 6. september 2026 av Claude på oppdrag fra Kjetil. Kjetil har valgt
**lesning G** i `Documentation/Geometribevarende_orden_2026-09-06.md`: spørsmålet er
om det finnes en geometri med stabil, null-separert dimensjon — ikke om ordenen
er Lorentz-lik. Les det dokumentet først; del 1–3 er premisset.

Denne filen inneholder to uavhengige pakker, **WP-F2** og **WP-H**. Utfør F2 først.
Separate commits. WP-F3 (det relasjonelle universet) finnes ikke ennå og skal ikke
kjøres i denne utsendelsen.

---

## WP-F2

### Formål

Avgjøre om innflytelsesordenen som følger av *denne* regelen (v7-kernel + v16a-
ressursmodell) bærer underlagets dimensjon når underlaget har en kjent dimensjon.
Det er kravet WP-F0 manglet: positiv kontroll og null skal gjennom hele kjeden
dynamikk → ordensuttrekk → estimator, ikke sammenlignes som ferdige posets.

Begge utfall er gyldige. Det negative er at ordenen ikke skiller ring fra gitter fra
ekspander selv der geometrien er kjent; da er svaret på lesning G nei for denne
regelen, og det er programmets sluttresultat.

### Underlag (fire, alle ≈1024 noder)

| id | graf | kjent d |
| --- | --- | --- |
| ring | syklus på 1024 noder | 1 |
| lat2 | 32×32 periodisk kvadratgitter | 2 |
| lat3 | 10×10×10 periodisk kubisk gitter (1000 noder) | 3 |
| rrg | tilfeldig 3-regulær graf, 1024 noder | ∞ (ekspander) |

Konstruer dem som `v7.UGraph`. Start med samme antall tokens som v16b (bruk
`initial_tokens` fra `Documentation/v16b_run_summary.csv`, plasser dem uniformt).
Frys `Params` fra `relational_universe_v16b_intrinsic_event_dag_gate.frozen_spec` —
ikke velg egne verdier. Arm: bare `exposure_matched_local` (v16ac-adapteren), én arm.

### To regelmoduser — begge kjøres

**Modus M (merke, frossen metrikk).** Kalibreringsvariant der metrikken står fast:
når kernelen trekker en strukturell deskriptor (`delete`/`triad`/`swap`), utføres den
*ikke* som kantendring, men som skriving av ressursen `mark:v` (tell opp et heltall på
noden). `local_token_kernel` leser `mark:*` i 2-hopps naboskap og vekter `move` mot
nabo u med faktor `(1 + ε·mark[u])`, ε = 0,25, frosset her. Dette gir en ekte
statistisk avhengighet mellom hendelser med bevart geometri. Skriv varianten som en
egen adapter i `Tools/influence_order_lab.py`; ikke rør v7-laben.

**Modus R (reell regel, drift).** v7-regelen uendret. Metrikken drifter; mål driften
(andel kanter endret over kjøringen) og rapporter den. Dette er broen til universet.

### Ordensuttrekk — kandidat B fra analysedokumentet

Utvid `action_access` til **kernel-lesesettet**: for en token-hendelse ved v leses
`node:v`, `adj:v`, `node:u` og `adj:u` for alle naboer u, `edge:v:u`, og i modus M i
tillegg `mark:*` for v, naboer og naboers naboer. Skrivesett som før (modus R) eller
`mark:v` + `token:t` (modus M). Bygg DAG-en med `DependencyDAG.add` fra v16b uendret.
Bevar den gamle (v16a-) ordenen parallelt som kontroll: den skal gi de samme tynne
tallene som WP-F0, ellers er noe galt.

Logg per hendelse: tid, token, node, deskriptor, lese-/skrivesett, og **grafavstand**
er tilgjengelig fra underlaget (BFS på det faste gitteret i M; på øyeblikksgrafen
hvert 512. steg i R).

### Kjørelengde

STEPS = 16 384 per historie (åtte ganger v16b, fordi tverrbindinger er sjeldne).
4 historier per underlag per modus, ulike seed. 4 underlag × 4 seed × 2 modi = 32
historier. Anslå kjøretid på én historie først og skriv den til hjerteslaget før du
starter alle; overstiger totalen 3 timer, halver STEPS og rapporter det.

### Observabler — regnes for hver historie, begge ordener

1. **Fortidsvolum.** For hendelse e og tidsvindu τ: `V_e(τ) = |{a ≺ e : t_e − t_a ≤ τ}|`.
   Median over alle e med t_e ≥ T/2 (unngå startkant). τ på logaritmisk grid
   {1, 2, 4, …, T/4} i tidsenheter. Tilpass `α = ∂ ln V / ∂ ln τ` over punktene med
   V ≥ 8. Bootstrap over historier (ikke over hendelser).
2. **Romlig rekkevidde.** For a ≺ e: `dist(node_a, node_e)` i underlagets metrikk.
   `R(τ)` = 90-persentil av avstand over par med t_e − t_a ≤ τ. Tilpass
   `γ = ∂ ln R / ∂ ln τ`. γ ≈ ½ er diffusivt, γ ≈ 1 ballistisk.
3. **Tverrbindingsandel.** Andel DAG-kanter som binder ulike tokens. Rapporter for begge
   ordener; dette er tallet som var 8,5 % i WP-F0.
4. Til sammenligning, samme fire tall som WP-F0 (lenker/hendelse, Θ, r/r_floor,
   maks|I|/N) — bare for å dokumentere at kausalmengde-gatene *fortsatt* ikke ser
   geometrien. Ikke gate på dem.

### Forhåndsregistrerte terskler — frys før første tall

**Gate F2 (bærer ordenen dimensjon?)** består i en modus hvis alle tre holder:
- **Rekkefølge:** median α(ring) < α(lat2) < α(lat3) < α(rrg).
- **Separasjon:** 95 %-bootstrap-KI for α er disjunkte for hvert nabopar i rekkefølgen.
- **Mekanisme:** γ er innenfor 0,10 av hverandre for ring, lat2 og lat3 (samme
  spredningslov på alle endelige underlag). Rapporter om γ ligger nær ½ eller 1.

Forventning (skrevet her på forhånd så den ikke kan justeres): modus M består med
γ ≈ 0,5; modus R består rekkefølge men feiler separasjon ved denne STEPS, fordi
strukturelle skrivinger er 1,3 % av hendelsene. Den gamle v16a-ordenen feiler
rekkefølge i begge modi.

**Ikke juster ε, STEPS-grid, τ-grid eller terskler etter at tall er sett.** Mener du
noe er feil satt: skriv det som begrunnet observasjon, la det stå.

### Utfall (G4)

- **M består, R består:** ordensuttrekket er dokumentert geometribevarende for denne
  regelen. Skriv det. WP-F3 (universet, samme uttrekk, primærobservabel α og γ) kan
  spesifiseres.
- **M består, R feiler separasjon:** uttrekket virker, men den reelle regelens
  redigeringsrate er for lav til at ordenen bærer geometri ved nåværende N/T. Skriv
  hva som skal til (fra tverrbindingsandelen) — men ikke kjør det.
- **M feiler:** ordenen bærer ikke dimensjon selv med frossen metrikk og ekte
  avhengighet. Da er svaret på lesning G nei for denne regelfamilien. Skriv det rett
  ut; det er ikke en mislykket pakke.

### Grunnsannhet (G5)

Underlagenes dimensjon er kjent ved konstruksjon. Ingen tall her er selvprodusert av
universets historier.

### Ikke-mål

Ingen kjøring på universets historier. Ingen Myrheim–Meyer-dimensjon som gate. Ingen
endring av v7-laben eller v16-filer. Ingen ny ε-verdi. Ikke closure-policyen i
AGENTS.md.

---

## WP-H: Tilstandsgrafens dimensjon mot nuller ved r ≤ 10

Fingeravtrykk: `state-graph-dimension-vs-null`.

### Formål

Lesning G, andre avlesning: har selve tilstandsgrafen en dimensjon som skiller seg
fra en null med samme gradfordeling? v13 målte `dim_proxy` bare ved r ≤ 4, der et tre
og et gitter er nesten like.

### Data

Gjenoppbygg sluttilstandene for de 12 v16b-historiene (samme `growth_seed`/`run_seed`/
arm; bruk v16b-kodens egen `build`/`run_assignment` opp til STEPS, eller lagre
`state.g` ved slutt av en ny replay — verifiser mot `final_nodes`/`final_tokens` i
`v16b_run_summary.csv`). Ikke ny dynamikk utover replay.

### Observabler, per graf

1. **Kulevolum-eksponent** `d_vol(r)` fra `ln B(r)` mot `ln r`, r = 1…10, over 64
   tilfeldige rotnoder; rapporter lokal helning i vindu [3, 6] og [6, 10].
2. **Spektraldimensjon** `d_s` fra returnsannsynlighet `P(t) ∝ t^{−d_s/2}` for tilfeldig
   vandring, t = 4…64, gjennomsnitt over 64 startnoder.
3. **Diameter og median avstand.**

### Nuller og positive (G5), samme observabler

- **Null:** konfigurasjonsmodell med nøyaktig samme gradsekvens (degree-preserving
  rewiring, 10·E byttinger), 8 replikater per graf.
- **Positiv:** 2D-gitter og ring med samme N; og et gitter der 10 % av kantene er
  omkoblet tilfeldig (for å se hvor fort d_s går mot ∞).

### Forhåndsregistrert terskel

Universgrafene skiller seg fra nullen hvis `d_s`-medianen ligger utenfor nullens
95 %-intervall for ≥ 10 av 12 grafer, i samme retning. Rapporter retningen. Alt annet
er «ikke skilt».

Forventning på forhånd: ikke skilt — gradsekvensen alene forklarer d_s. Det er det
negative, gyldige utfallet.

---

## Felles regler

- Kode: `Tools/influence_order_lab.py` (F2) og `Tools/state_graph_dimension_lab.py` (H).
  Bruk `.codex_pydeps` og networkx der du har det. Ingen nye avhengigheter.
- Rådata til `Documentation/Program/WP-F2_*.csv` og `WP-H_*.csv`. Frosne parametre til
  `WP-F2_frozen.json` før første kjøring; hash i rapporten.
- Rapporter: `Documentation/Program/WP-F2_report.md` og `WP-H_report.md`, skrevet
  inkrementelt. Innhold: 1) frosne parametre og hash, 2) kjøretid, 3) målte tall per
  underlag/modus/orden med KI, 4) bestått/ikke bestått per terskel uten omskriving,
  5) utfallet i G4-form, 6) blokkert, 7) én setning: står lesning G eller faller den.
- Hjerteslag: `.program_logs/WP-F2.heartbeat` / `WP-H.heartbeat`, én linje per delsteg
  og minst hvert femte minutt, `<ISO-tid> <status>`.
- Stoppregel G3: to forsøk på samme feil, tredje gang «Blokkert».
- `git add` bare egne filer, eksplisitt. Ikke `.DS_Store`. To commits:
  `WP-F2: influence-order geometry calibration` og
  `WP-H: state-graph dimension vs configuration null`. Kan din sandbox ikke skrive
  `.git`: si det i rapporten og stopp — integratoren committer.
- Ingen push. Ingen fysikkpåstander. Ingen konklusjon sterkere enn tallene.
