# WP-F0 rapport: adgangstest for dimensjonsspørsmålet

Kjørt 3. september 2026 av Claude (cowork) i mount-VM-en, ikke av Codex.
Fingeravtrykk: `event-dag-dimension-admissibility`. Spesifikasjon:
`Documentation/Program/WP-F0_dimension_admissibility.md` (24. aug, terskler
frosset der før første tall ble regnet).

## Avvik fra G1 — skriv det først

G1 sier at den som skriver koden ikke skriver gaten. Tersklene ble skrevet og
frosset 24. august av Claude på grunnlag av rådgiverkjøringen; koden ble
skrevet 3. september av Claude fordi Codex ikke var nåbar (ledger-fingeravtrykk
`codex-mcp-session-dies-after-a-few-minutes`, eskalert; `RUN_PACKAGES.sh` er
ikke kjørt lokalt). Gate og kode har altså samme forfatter, med ti dagers
avstand. Tersklene er uendret (`WP-F0_thresholds_frozen.json` skrives av
verktøyet selv fra konstanter i koden, og kan diffes mot spec-teksten).
Kompensasjonen er at alt er etterprøvbart: verktøyet er 300 linjer ren Python
uten avhengigheter og kjører på 11 sekunder. **En uavhengig gjennomkjøring av
Codex eller Kjetil er den manglende G1-kvitteringen**, ikke denne rapporten.

## 1. Hva `causal_depth` faktisk måler

`DependencyDAG.analyze()` i `relational_universe_v16b_intrinsic_event_dag_gate.py`
(linje 316–334) setter `depth = max(depth, depths[pred] + 1)` over alle direkte
forgjengere. Det er **lengste vei inn** (ikke korteste, ikke topologisk nivå).
`causal_depth = max(depths) + 1` er dermed lengste kjede målt i elementer.
Gulvgrensen i G0.1 holder: hvert element har minst `depth(v)` forfedre.

Verktøyet leser `*_dependency_edges.csv` fra v16-kjøringene og bygger samme
DAG (kanter = RAW/WAW/WAR-konflikter, hendelses-id er topologisk orden).
Ingen ny DAG-definisjon, ingen ny dynamikk.

## 2. Datagrunnlag

36 historier som fantes før pakken: v16b (12, N=2048), v16c fin (12, N=2048),
v16d fin (12, N=3072). Begge scheduler-armer i alle tre. Referanseposets
generert av samme kode: kjedebunt (32 × 64) og Minkowski-sprinklinger d=2 og
d=4 i kausaldiamant, N=2048.

## 3. Referansekontroll (G5)

| størrelse | kjedebunt målt | rådgiver | d=2 målt | rådgiver | d=4 målt | rådgiver |
| --- | --- | --- | --- | --- | --- | --- |
| Θ | 1,00 | 1,00 | 12,6 | 12,3 | 16,6 | 18,4 |
| lenker/element | 0,98 | 0,98 | 6,2 | — | 28,1 | 28,4 |
| s | 0,72 [0,69; 0,75] | 0,76 | 0,57 [0,55; 0,59] | 0,538 | 0,22 [0,18; 0,28] | 0,302 |
| d_MM (rettet) | 5,38 | 5,38 | 2,03 | 2 | 4,03 | 4 |

Rettet Myrheim–Meyer gir d=2,03 på d=2-sprinkling og 4,03 på d=4 — formelen
er riktig. Kjedebunten leses som d=5,38 — degenerasjonen er reprodusert.
Eneste merkbare avvik fra rådgiverens tabell er s for d=4: lengste kjede er
bare 13 ved N=2048, så L≥8-vilkåret etterlater to p-verdier i tilpasningen og
et bredt KI. Det påvirker ikke historiene (h = 41–72).

## 4. Målte tall, per arm og N (median [min; maks] over historier)

| arm | N | n | rå kanter/hendelse | lenker/hendelse | r | r/r_floor | h | Θ | maks\|I\|/N | d_MM | s (pooled, 95 % KI) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| current_global | 2048 | 12 | 1,14 [1,09; 1,22] | 1,03 [1,01; 1,05] | 0,033 | 1,31 [1,12; 1,65] | 49 [41; 60] | 1,24 [1,02; 1,57] | 0,052 [0,025; 0,071] | 5,45 | 0,662 [0,646; 0,679] |
| exposure_matched_local | 2048 | 12 | 1,14 [1,09; 1,20] | 1,03 [1,01; 1,04] | 0,030 | 1,27 [1,20; 1,70] | 52 [41; 64] | 1,21 [0,94; 1,66] | 0,047 [0,033; 0,084] | 5,45 | 0,678 [0,664; 0,693] |
| current_global | 3072 | 6 | 1,18 [1,13; 1,20] | 1,04 [1,03; 1,07] | 0,031 | 1,60 [1,39; 2,05] | 61 [57; 70] | 1,66 [1,32; 2,12] | 0,050 [0,047; 0,107] | 5,38 | 0,676 [0,658; 0,692] |
| exposure_matched_local | 3072 | 6 | 1,18 [1,12; 1,20] | 1,05 [1,02; 1,06] | 0,031 | 1,49 [1,12; 1,95] | 64 [54; 72] | 1,51 [1,08; 2,01] | 0,081 [0,038; 0,108] | 5,64 | 0,679 [0,660; 0,696] |

Per-historie-tall: `WP-F0_admissibility_per_history.csv`. Alle desimeringstrekk
(36 historier × 6 p × 20 trekk): `WP-F0_decimation_draws.csv`.

Rådgiverens forhåndsanslag (skrevet i spec før måling): G0.1 ≈ 1,3, G0.2 = 1,22,
G0.4 ≈ 1,34. Målt: 1,27–1,31 (N=2048), rå kanter 1,14 / lenker 1,03, Θ 1,21–1,24.
Anslaget traff.

## 5. Terskler, uendret, bestått/ikke bestått

| gate | terskel | resultat | historier bestått |
| --- | --- | --- | --- |
| G0.1 | r/r_floor ≥ 2,0 | **ikke bestått** | 1 av 36 (v16d 3407/61001 current_global: 2,047) |
| G0.2 | lenker/hendelse ≥ 5 ved N=2048 | **ikke bestått** | 0 av 36 (maks 1,07) |
| G0.3 | maks\|I\| ≥ 0,05 N | ikke entydig | 19 av 36 |
| G0.4 | Θ ≥ 5 | **ikke bestått** | 0 av 36 (maks 2,12) |
| **Gate 0** | alle fire | **ikke bestått** | 0 av 36 |
| Gate 1 | s ∈ [0,20; 0,40], KI < 0,05, armer enige < 0,05 | **ikke bestått** (s ≈ 0,66–0,68; KI-bredde 0,03; armer enige innen 0,02) | — |

Gate 1 er formelt evaluert fordi tallene forelå, men den er uten mening når
Gate 0 feiler; den er tatt med fordi s-verdien er informativ (se under).

## 6. Konklusjon, innenfor det tallene bærer

Hendelses-DAG-en er ikke et objekt man kan tilordne en dimensjon med disse
estimatorene. På alle fire kjerneobservabler ligger historiene ved eller nær
kjedebunt-referansen og langt fra begge sprinklinger: lenker per hendelse 1,03
(bunt 0,98; d=2 6,2; d=4 28), Θ 1,2–1,7 (bunt 1,0; sprinkling 12–17),
desimeringseksponent 0,66–0,68 (bunt 0,72; d=2 0,57; d=4 0,22), r/r_floor 1,1–2,0
(bunt 1,0; sprinkling 15–30). Med h = 41–72 er DAG-en et bunt av omtrent N/h ≈
30–50 kausale tråder. Myrheim–Meyer gir d ≈ 5,4 på alle 36 historier, og gir
det samme på en kjedebunt: verdien bærer ingen geometrisk informasjon i dette
regimet. **Den dyre runden (WP-F1 / v18) skal ikke kjøres.** Dette er
programmets svar på dimensjonsspørsmålet: nei, ikke med denne DAG-en.

Det trådene gjør som en ren bunt ikke gjør, er å berøre hverandre: største
Alexandrov-intervall er 50–330 hendelser (bunt: 64 = én tråd), og r/r_floor
ligger 10–100 % over bunten. Vekselvirkningen er målbar, men den løfter verken
lenketall, Θ eller desimeringseksponent bort fra buntverdiene.

Én observasjon uten konklusjon: r/r_floor og Θ er høyere ved N=3072 enn ved
N=2048 (median Θ 1,24 → 1,66 for current_global), mens r er flat (0,031–0,033).
For en ren bunt med flere tråder skulle r falle. To N-punkter er for lite til å
si om dette er en trend; det er notert, ikke tolket.

Armene er enige på alt (Θ, s, lenker innenfor spredningen). Scheduler-valget
endrer ikke svaret.

## 7. Filer

- `Tools/causet_admissibility.py` (nytt, ~300 linjer, ingen avhengigheter utover stdlib)
- `Documentation/Program/WP-F0_admissibility_per_history.csv` (39 rader: 36 historier + 3 referanser)
- `Documentation/Program/WP-F0_admissibility_by_arm.csv`
- `Documentation/Program/WP-F0_decimation_draws.csv`
- `Documentation/Program/WP-F0_thresholds_frozen.json`
- `.program_logs/WP-F0.heartbeat` / `.log` (kjøringen tok 11 s)

Reproduksjon:

```
python3 Tools/causet_admissibility.py \
  --edges Documentation/v16b_dependency_edges.csv \
  --edges Documentation/v16c_fine_dependency_edges.csv \
  --edges Documentation/v16d_fine_dependency_edges.csv \
  --out Documentation/Program --draws 20 --references
```

Seed 20260903 er default; desimering og bootstrap er deterministiske gitt seed.

## 8. Blokkert / usikkert

- G1-kvittering mangler (se øverst). Uavhengig gjennomkjøring anbefales før
  WP-F1 lukkes formelt i PROGRAM.md.
- s for d=4-referansen er svakt bestemt ved N=2048 (to p-punkter). Ikke relevant
  for konklusjonen, som ikke hviler på d=4-tallet.
- Commit-hash: se under.
