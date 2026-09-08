# nodegraph

Typede nodegrafer: noder er funksjonsdefinisjoner med deklarert aritet og inn-
og ut-typer, grafer er hash-consede DAG-er over dem, og en formålskontrakt
bestemmer hva som teller som et funn.

Formålet står i `PURPOSE.md`. Vurderingen av om dette er verdt å bygge videre
på, med alle måletall, står i
`../../Documentation/Nodegraf_Vurdering_2026-09-08.md`.

**Skal du bruke det:** les `INSTRUKSJONER.md` og kjør
`python3 examples/minimal_purpose.py`. Den er hele arbeidsflyten på under 130
linjer, med planta effekt, så du ser maskineriet svare riktig på et spørsmål
der fasiten er kjent. På den arenaen finner søket `gini(x)`, mens de to
opplagte håndplukkede observablene så vidt klarer holdout-porten.

## Filene

| fil | hva den er |
|---|---|
| `INSTRUKSJONER.md` | hvordan du peker dette mot et nytt problem: seks steg, tre nektelser, og fallgruvene med måletall |
| `examples/minimal_purpose.py` | hele arbeidsflyten, selvstendig, med planta effekt |
| `core.py` | typer, noder, DAG, typesjekk, referanseevaluator, komposittnoder, parser |
| `stats.py` | den parede statistikken, de målte nullene og fortegnstesten. Vet ingenting om arenaen — det er meningen |
| `library.py` | 45 basisnoder. Python- og C-implementasjon side om side, per node |
| `compile_py.py` | graf → rett-fram Python |
| `compile_c.py` | graf → C → `gcc -O2` → ctypes, med konformansharness |
| `purpose.py` | formålskontrakten. Nekter å gate uten målt null *og* målt positiv referanse |
| `search.py` | trinnvis typet enumerering med observasjonell deduplisering; `Proposer` er sømmen der en språkmodell kobles på |
| `arena/build_substrate.py` | kjører simulatoren, reduserer hver kjøring til typede råkanaler |
| `arena/observable_purpose.py` | formålet søket peker mot, statistikken og de målte nullene |
| `run_experiment.py` | hele sløyfen én gang, med beslutningene forhåndsregistrert i toppen av fila |
| `replicate.py` | måler den forhåndsvalgte vinneren på ferske seeds. Søker ikke |
| `demo_compile.py` | komposittnode → inlining → C → sertifisering → speedup |
| `tests/test_nodegraph.py` | 19 tester. `python3 tests/test_nodegraph.py` eller pytest |

## To regler som er verdt å ikke bryte

**Én semantikk.** `core.Graph.evaluate` er definisjonen. En backend som ikke
består `compile_c.conformance` sertifiseres ikke og deles ikke ut. Det er
`certify()` som håndhever det, ikke disiplin.

**Ingen gate uten to målte referanser.** En `PurposeContract` uten målt
nullreferanse *og* målt positiv referanse nekter å gate, og en kontrakt hvis
statistikk ikke skiller sine egne to referanser melder seg selv umålbar. Dette
er `Documentation/v17_program_closure.md` del 7 i kjørbar form.

## Ingen fysikkpåstand

Dette er instrumentering. Ingen v-runde er åpnet og `attempt_ledger.csv` er
urørt.
