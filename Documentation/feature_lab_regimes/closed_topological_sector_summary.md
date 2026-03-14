# Closed Topological Sector

Kilder:
- CSV: `closed_topological_sector.csv`
- Autoanalyse: `closed_topological_sector_auto.md`

## Regime

- steps: 12000
- initial_cycle: 10
- initial_tokens: 6
- r_seed = 0
- r_birth = 0
- r_death = 0
- p_triad = 0
- p_del = 0
- p_swap = 0.18
- avoid_disconnect = True

Dette regimet holder systemet i en lukket sektor med ren edge-swap-dynamikk. Det finnes ingen kanal som kan endre token-antall, node-antall eller kant-antall.

## Eksakte algebraiske identiteter

- `beta1 = edges - nodes + components`
- `deg_sq_sum = 2*wedges + 2*edges`

Disse er sanne for alle loggede rader og er ikke dynamiske funn.

## Eksakte dynamiske invariants i denne sektoren

- `tokens` er konstant lik 6
- `nodes` er konstant lik 10
- `edges` er konstant lik 10
- `components` er konstant lik 1
- `beta1` er konstant lik 1

Dette er ekte regimedefinerte invariants, ikke bare identiteter. De folger av at bare bridge-frie edge-swaps er tillatt, og at seed/birth/death er skrudd av.

## Kandidater til quasi-invariants

Etter at de eksakte invariantene og de algebraiske identitetene er trukket ut, blir det lite igjen som er robust quasi-invariant. Triangler, 4-sykluser, clustering, spektralradius og dimensjonsproxy fluktuerer, men de drifter ikke systematisk mot en ny bevart linearkombinasjon.

Den standardiserte SVD-en viser nullretninger som i praksis bare reflekterer:
- at `tokens` er helt konstant
- at `nodes`, `edges`, `components` og `beta1` sitter i en lavdimensjonal identitet/invariant-sektor
- at `wedges` og `deg_sq_sum` er koblet algebraisk nar `edges` er konstant

## Tolkning

Dette er det reneste kontrollregimet i labben. Det viser at feature-labben faktisk kan skille:
- rene algebraiske nullretninger
- ekte dynamiske invariants fra regelsettet
- og variable motiv/geometrifeatures som ikke er bevart

Fysisk lesning: dette er en topologisk lukket sektor med lokal omkobling, men uten netto produksjon av volum eller loop-ladning.
