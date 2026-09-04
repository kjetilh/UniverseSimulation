# WP-A: Mål β₁-bokføringens troverdighet

Repo: /Users/kjetil/Build/Digipomps/HAVEN/UniverseSimulation (gren master).
Les `Documentation/Status_Og_Retninger_2026-08-23.md` del 5 først.
Fingeravtrykk: `beta1-bookkeeping-fidelity-measurement`.

## Objektiv

Mål hvor ofte β₁-bokføringen i perturbasjonskonstruktørene er gal.
Dette er en MÅLING, ikke en fiks. Ikke rett feilen i denne pakken.

## Bakgrunn (verifisert mot disk, ikke antatt)

`relational_universe_local_max_coupling_lab.py` linje ~370-401:

- `choose_center_token()` har en fallback: finnes ingen `w` som er nabo til `u`
  men ikke til `v`, faller den tilbake til `sorted(w for w in
  state.g.neighbors(u) if w != v)` — som kan returnere en `w` som ALLEREDE er
  nabo til `v`.
- `apply_local_swap_perturbation()` gjør `remove_edge(v,u)` + `add_edge(v,w)`.
  `networkx.add_edge` er idempotent. Treffer fallbacken: én kant fjernes, ingen
  legges til. Faktisk Δβ₁ = −1, bokført `"beta1": 0`.
- `apply_chord_perturbation()` gjør `add_edge(v,w)`. Treffer fallbacken: ingen
  kant legges til. Faktisk Δβ₁ = 0, bokført `"beta1": +1`.

Samme feilklasse som R_slide-feilen rettet i commit `53d7561`.

## Oppgave

1. Skriv `Tools/beta1_bookkeeping_audit.py` som:
   - importerer konstruktørene fra `relational_universe_local_max_coupling_lab.py`.
     Ikke reimplementer dem — mål koden som faktisk kjører.
   - måler faktisk β₁ = E − N + C direkte fra grafen før og etter hver perturbasjon
   - logger per kall: perturbasjonstype, om fallbacken ble truffet, om `add_edge`
     var en no-op, bokført Δβ₁, faktisk Δβ₁, avvik ja/nei, konfigurasjonsstørrelse
2. Kjør over startkonfigurasjonene v15-programmet faktisk bruker. Les hvilke
   targets/seeds/growth-parametere som brukes i f.eks. `relational_universe_v15cz_*`,
   `v15da_*`, `v15dk_*`, `v15dr_*` — ikke gjett. Begge konstruktører, minst 500
   kall hver.
3. Skriv `Documentation/beta1_bookkeeping_audit.md` + `.csv` med rådata og
   aggregater: fallback-frekvens, no-op-frekvens, avviksfrekvens, fordeling per
   konfigurasjonsstørrelse.
4. Rapporter hvilke `relational_universe_v15*.py` som importerer disse
   konstruktørene direkte eller transitivt.

## Grunnsannhet (G5)

Faktisk β₁ regnet fra grafens egne E, N og C med networkx — ikke fra `delta_core`,
og ikke fra noe konstruktørene selv rapporterer.

## Harde rammer

- Bruk `.codex_pydeps/`. Ikke installer pakker, ikke legg til avhengigheter.
- Ikke rett feilen. Ikke rør `relational_universe_local_max_coupling_lab.py`.
  Målingen skjer utenfra.
- Ikke kjør closure-policyen i AGENTS.md. Dette er ikke en forskningsrunde:
  ingen publisering, ingen RAG-sync.
- Ikke lag en v2 av auditen. Én implementasjon.
- Ikke juster utvalget for å få et penere tall.
- Ikke ta med `.DS_Store` i commit.

## Forhåndsdefinert utfall (G4) — begge er gyldige og skal skrives

- Avviksfrekvens ≈ 0: v15-bokføringen er renvasket. Skriv det rett ut.
- Avviksfrekvens > 0: rapporter frekvens og berørte runder. Ikke ekstrapoler til
  «v15 er ugyldig» — det er ikke det som er målt.

Ingen konklusjon sterkere enn tallene. Ingen fysikkpåstander.

## Stoppregel (G3)

Maks to forsøk på samme feil. Tredje gang: stopp, skriv observasjonen under
overskriften «Blokkert», rapporter tilbake. Gyldig og forventet utfall.

## Commit

Én commit, melding starter `WP-A: measure beta1 bookkeeping fidelity`.
Push til master.

## Rapporter tilbake i `Documentation/Program/WP-A_report.md`

1. Filer opprettet, med linjetall.
2. Målte tall: fallback-, no-op- og avviksfrekvens per konstruktør.
3. Antall og navn på berørte v15-script.
4. Commit-hash.
5. Alt som ble blokkert eller er usikkert.

## Samtidighet (lagt til 24. aug)

Andre arbeidspakker kjører samtidig i samme repo. Derfor:
- `git add` kun dine egne filer, eksplisitt oppgitt. Aldri `git add -A`.
- `git pull --rebase` før push. Ved konflikt: inntil 3 forsøk, deretter stopp og
  rapporter som blokkert.
- Ikke rør filer som tilhører andre pakker.

## Hjerteslag (obligatorisk, lagt til 24. aug)

Skriv en linje til `.program_logs/<pakkenavn>.heartbeat` hvert femte minutt og ved
hvert delsteg, på formen `<ISO-tid> <kort statuslinje>`. En vakt leser filen for å
skille «arbeider» fra «død». Uten hjerteslag antas pakken død og blir startet på
nytt — som koster mer enn linjen gjør.
