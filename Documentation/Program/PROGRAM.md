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
| WP-A | Mål β₁-bokføringens troverdighet | — | utsendt |
| WP-B | Fullfør loop-detektoren (bit 7 + rapport) | — | utsendt |
| WP-C | Miljøspesifikasjon + CI | WP-B | ikke startet |
| WP-D | Publiser fra HEAD, lukk Gate 4 | — | ikke startet |
| WP-E | v17-programmets konklusjonsdokument | — | Claude skriver |
| WP-F0 | Adgangstest for dimensjonsspørsmålet | — | **fullført 3. sep — Gate 0 ikke bestått (0/36)** |
| WP-F1 | Dimensjonsrunden (v18) | WP-F0 består | **skal ikke kjøres** |

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
