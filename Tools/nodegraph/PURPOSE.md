# Formål for `Tools/nodegraph`

Skrevet før koden. Hvert steg under er målt mot formålet, og stegene som ikke
nådde det står oppført like tydelig som de som gjorde det.

## Overordnet formål

Avgjøre, ved måling og ikke ved resonnement, om en typet nodegraf med
deklarerte inn- og ut-typer, et basisbibliotek, en søkesløyfe og en
kompilator er et verktøy som flytter UniverseSimulation-programmet framover.

Formålet er **ikke** å bygge et generelt program­synteserammeverk. Det finnes
fra før. Formålet er å finne ut om nettopp denne konstruksjonen løser et
problem dette repoet dokumenterbart har hatt.

## Delformål og måltall

| # | Delformål | Måltall | Utfall |
|---|---|---|---|
| D1 | En node er en funksjonsdefinisjon med deklarert aritet og typer, og feil type stoppes ved konstruksjon | Alle feiltypede uttrykk avvises med presis melding | Oppnådd (5 tester) |
| D2 | Komposittnoder er førsteklasses: en lagret delgraf kan brukes som node og gir samme verdi som den innsatte formen | Inlining gir identisk `key()` og identisk verdi | Oppnådd |
| D3 | Én semantikk. Enhver backend som er uenig med referansetolken sertifiseres ikke | Alle 45 noder, 250 tilfeldige input hver, 0 avvik | Oppnådd |
| D4 | Formålskontrakten nekter å gate uten målt nullreferanse og målt positiv referanse | Kontrakten avviser tre feilformer mekanisk | Oppnådd |
| D5 | Søket finner en observabel som slår permutasjonsnullen på seeds den ikke ble valgt på | Holdout-score > holdout-null | Oppnådd, men marginen er liten (se D5-forbehold) |
| D6 | Kompilering gir målbar gevinst uten å endre mening | Målt speedup med sertifisert konformans | Oppnådd (251×) med ett vesentlig forbehold (se «Det som ikke virket») |
| D7 | Resultatet skal ikke avhenge av at en språkmodell er tilgjengelig | Deterministisk enumerator, ingen tokens brukt i måleløypa | Oppnådd |

**D5-forbehold.** Vinneren er en monoton omskrivning av β₁ (Spearman 0,98).
Søket fant den riktige størrelsen og en bedre parametrisering av den. Det fant
ikke en ny størrelse. Det står som resultatet, ikke som et forbehold på det.

## Hvorfor dette formålet og ikke et penere

`Documentation/v17_program_closure.md` avslutter elleve runder med et negativt
resultat og én regel:

> En primær endepunktstørrelse skal ha en målt nullreferanse og en målt positiv
> referanse før den brukes som gate. Mangler en av dem, er runden en
> instrumenteringsrunde og skal ikke telle som en test av hypotesen.

Regelen sto i et dokument. Her står den i `purpose.py`, der en kontrakt uten
begge referanser nekter å gate i det hele tatt. Det er hele poenget med å bygge
dette i dette repoet framfor et hvilket som helst annet: den første av de to
nektelsene ville stoppet v17-serien etter runde fire.

## Påstandsklasse

Ingenting her er en fysikkpåstand. Ingen runde er åpnet, ingen gate i
v-serien er berørt, og `Documentation/Program/attempt_ledger.csv` er ikke
endret. Det som måles er en observabels statistiske respons på en
regelparameter i en toy-simulator, og et kompilatorutslag i mikrosekunder.
