# Amendment 1, forsøk 2 — ferdig måling

Oppdatert 9. september 2026 (CEST). Brukerordre: R → M → gater → WP-H.
Alle fire steg er utført i denne rekkefølgen. Ingen forskningsprosess gjenstår.

- R: 16 lagrede historier reanalysert, 67,782 s, ingen ny dynamikk.
- M: 16 historier à 8192 steg, 1201,465 s, seed=mark og null kantdrift.
- F2: begge kernel-gater feiler rekkefølge, separasjon og mekanisme.
  γ-spenn R=0,129122101194; M=0,129154885821. Kernel-fit 32/32 er evaluerbare.
  Legacy har manglende fit i 10/16 R og 9/16 M, og gates ikke som negativt funn.
- H: replay 12/12 nøyaktig, 107,019 s; analyse av 144 grafer, 37,112 s.
  Registrert rotmedian-d_s gir 12/12 under null95. Alle 96 nuller frakoblet;
  d_s fra gjennomsnittlig returkurve gir motsatt retning 96/96. Ingen stabil,
  aggregasjonsuavhengig eller asymptotisk dimensjon er dokumentert.
- Verifikasjon: F2-ressursaudit 33/33 inklusive gammel pilot; forsøk 2-audit 32/32;
  fem analysetester+fire runtime-tester+små-DAG-selvtest. H 144/144 grafer,
  9216 rotkontroller og analytisk selvtest består.

Rapporter: WP-F2_report.md og WP-H_report.md. Eksakte data, frys og
verifikasjonskvitteringer står i tilsvarende CSV/JSON-er. Originale R-filer,
begge originale forhåndsregistreringer og frosne lab/v7/v16-kilder er uendret.
Forsøk 1 er bevart i WP-F2_attempt1_* og original R-analyse.

En annen prosess committet deldata som 3ab0fd5 og opprettet amendment 2 mens
M kjørte, og laget senere aa6e954. Denne økten utførte bare amendment 1.
Ekstern ledger attempts=3 og historisk notat er bevart; våre endelige
amendment 1-resultater er tilføyd. Ingen WP-F3 eller nye terskler er kjørt.

Siste gjenstående steg er integrasjon og eventuell full publiseringsclosure.
Se de separate integrasjonsfillistene og WP-F2_H_closure_status.json for
faktisk status. Ved .git-blokkering krever amendmentet stopp og integrator.
Ikke start forsøk2-kommandoene igjen; de vil avvise duplisering. Ikke endre
frosne filer eller gjenkjøre simuleringer for å løse en integrasjonsfeil.

## Endelig stoppunkt

Faktisk git add feilet exit 128: fatal: Unable to create '/Users/kjetil/Build/Digipomps/HAVEN/UniverseSimulation/.git/index.lock': Operation not permitted
Alle målinger er ferdige. Integratoren committer; ingen omkjøring, push, deploy eller RAG-kontroll utført her. Se WP-F2_H_closure_status.json.
