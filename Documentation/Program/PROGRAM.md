# Program: fra pause til svar

Opprettet 24. august 2026. Administreres av Claude (Opus 5) på oppdrag fra Kjetil.
Utførende: Codex. Grunnlag: `Documentation/Status_Og_Retninger_2026-08-23.md`.

## Målet

Ett etterprøvbart svar på om hendelses-DAG-en har en stabil, null-separert
dimensjon. Ja eller nei — begge er resultater. Alt annet i programmet finnes for
å gjøre det svaret verdt å stole på.

## Styringsregler

Disse gjelder programmet selv, ikke bare repoet. De er generalisert fra
`Documentation/Agent_Loop_Dynamics.md` del 6.

- **G1 (R8).** Den som skriver koden skriver ikke gaten. Claude spesifiserer
  akseptansekriterier og verifiserer mot disk. Codex implementerer. Codex'
  egenrapport er aldri godkjenning.
- **G2 (R1+R2).** Hver arbeidspakke har et identitetsstrippet fingeravtrykk i
  `attempt_ledger.csv`. Forsøkstallet går bare opp. Ny pakkeidentitet nullstiller
  det ikke.
- **G3 (R3).** To strikes på samme fingeravtrykk stopper pakken og eskalerer til
  Kjetil. Ikke til neste variant.
- **G4 (R6).** Hver pakke har et forhåndsdefinert negativt utfall som er gyldig
  og skal skrives. «Vi målte og fant ingenting» er en fullført pakke.
- **G5 (R7).** Hver pakke navngir hva den måler mot som ikke er selvprodusert.
- **G6.** `python3 -m Tools.loop_detector.cli --repo . --check` kjøres ved hver
  milepæl. Utløste signaturer rapporteres, ikke bortforklares.

## Arbeidspakker

| ID | Navn | Avhenger av | Status |
| --- | --- | --- | --- |
| WP-A | Mål β₁-bokføringens troverdighet | — | fullført 4. sep — 0 avvik i 791×2 kall |
| WP-B | Fullfør loop-detektoren (bit 7 + rapport) | — | delvis: rapport 25. aug, tester ukjørt |
| WP-C | Miljøspesifikasjon + CI | WP-B | ikke startet |
| WP-D | Publiser fra HEAD, lukk Gate 4 | — | ikke startet |
| WP-E | v17-programmets konklusjonsdokument | — | Claude skriver |
| WP-F0 | Adgangstest for dimensjonsspørsmålet | — | **fullført 3. sep — Gate 0 ikke bestått (0/36)** |
| WP-F1 | Dimensjonsrunden (v18) | WP-F0 består | **veto trukket 6. sep (WP-G1); avgjørelse hos Kjetil** |

WP-E skrives av Claude og ikke av Codex, med hjemmel i G1: Codex eide gatene i
v17-serien og kan ikke være den som feller den.

## Status per milepæl

Rådgiverkjøring 24. aug felte del 6 i statusdokumentet: Myrheim-Meyer-normaliseringen
var gal med faktor 2, og estimatoren er degenerert for tynne posets. Se RETTELSE i
`Documentation/Status_Og_Retninger_2026-08-23.md`. WP-F1 er nå betinget av WP-F0.

Loop-detektoren kjørt 24. aug 2026 mot HEAD 084e286 + arbeidstre:
S1 ja, S2 ja, S3 nei, S4 ja, S5 ja, S6 nei, S7 ja. Exit 1.
S4 flagger ikke lenger de fem `*_verify.py` — de ble rettet 23. aug.

WP-F0 kjørt 3. sep 2026 av Claude i mount-VM-en (Codex unåbar, se ledger). Gate 0
ikke bestått på 0 av 36 historier; lenker/hendelse 1,03, Θ 1,2–1,7, s 0,66–0,68 —
alt ved kjedebunt-referansen. Programmets svar på dimensjonsspørsmålet er nei.
G1-avvik: gate og kode har samme forfatter; uavhengig gjennomkjøring utestående.
Se `Documentation/Program/WP-F0_report.md`.

| WP-G1 | Adversariell replikasjon av WP-F0 (G1-kvittering) | WP-F0 | fullført 6. sep — bred dom veltet |

WP-G1 (Codex, 6. sep, lokal `codex exec`): Gate 0-tallene i WP-F0 reprodusert eksakt
36/36. Men en verifisert d=2-sprinkling (r≈0,5, Θ≈12) presset gjennom samme
konflikt-DAG-konstruksjon som v16b (1–3 tilfeldige ressurser per hendelse) gir lenker≈1
og Θ≈1 — Gate 0 avviser 24/24 kjente d=2-inputt. Gaten måler altså
ressurskonflikt-projeksjonen, ikke underliggende orden. Kalibrert kjedebunt med
tverrkanter bommer med faktor 3 på Θ og r/r_floor: «kjedebunt» er feil ord; riktig er
«sparsom konflikt-DAG med langt mindre miksing enn tilfeldige tverrkanter».
**Står:** den lagrede konflikt-DAG-en er tynn og ikke selv sprinklinglik; d_MM er
meningsløs på den. **Faller:** «derfor skal v18 ikke kjøres». Programmets svar på
spørsmålet slik det ble stilt (dimensjon av *denne* DAG-en) er fortsatt nei; det nye
er at spørsmålet var stilt til feil objekt. Neste beslutning (Kjetil): finnes en
geometribevarende orden å måle på? Se `Documentation/Program/WP-G1_report.md`.

| WP-F2 | Geometribevaring av innflytelsesordenen (ring/lat2/lat3/rrg, modus M og R) | WP-G1 | utsendt 6. sep |
| WP-H | Tilstandsgrafens dimensjon mot konfigurasjonsnull, r ≤ 10 | — | utsendt 6. sep |
| WP-F3 | Innflytelsesordenen på universet (α, γ som primærobservabler) | WP-F2 består | betinget |

6. sep: Kjetil valgte **lesning G** (geometri med stabil, null-separert dimensjon, ikke
Lorentz-likhet) etter `Documentation/Geometribevarende_orden_2026-09-06.md`. WP-F1/v18
er erstattet av WP-F2 → WP-F3. Mekanismeargumentet (moves skriver bare eget token;
innflytelse bæres av vandrende tokens → diffusiv) står som premiss.
