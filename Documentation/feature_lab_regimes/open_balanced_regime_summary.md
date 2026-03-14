# Open Balanced Regime

Kilder:
- CSV: `open_balanced_regime.csv`
- Autoanalyse: `open_balanced_regime_auto.md`

## Regime

- steps: 12000
- initial_cycle: 10
- initial_tokens: 6
- r_seed = 0.02
- r_birth = 0.01
- r_death = 0.01
- p_triad = 0.08
- p_del = 0.04
- p_swap = 0.06
- avoid_disconnect = False

Dette regimet er apent, men moderat. Token-birth og token-death er balansert i rater, mens seed-attachment og lokal rewrite fortsatt lar grafen vokse og reorganisere seg.

## Eksakte algebraiske identiteter

- `beta1 = edges - nodes + components`
- `deg_sq_sum = 2*wedges + 2*edges`

Disse dukker opp som nesten-nullretninger i bade ra og standardisert SVD, og ma derfor ikke kalles bevaringslover.

## Eksakte invariants observert i denne kjøringen

- `components` holdt seg lik 1 gjennom hele tidsserien

Dette er ikke en algebraisk identitet. Det er et dynamisk resultat for akkurat denne parameterpakken: systemet vokser, men forblir sammenhengende i den observerte kjøringen.

## Kandidater til quasi-invariants

Den mest stabile ikke-trivielle sektoren etter at `components` er tatt ut, er en linearkombinasjon av:
- `edges`
- `beta1`
- `wedges`
- `deg_sq_sum`

Men denne sektoren er i stor grad forklart av de to identitetene over. Nar man standardiserer feature-skalaene, blir det enda tydeligere at SVD-kandidatene hovedsakelig lever i denne identitetsdominerte delmangfoldet. Jeg ser derfor ingen robust ny quasi-invariant her utover:
- sammenhengskomponenten `components = 1` i denne kjøringen
- og en svak metastabil kobling mellom tett lokal struktur og global vekst

## Dynamiske resultater som ikke er identiteter

- `tokens` går fra 6 til 10
- `nodes` gaar fra 10 til 27
- `edges` gaar fra 10 til 225
- `triangles` gaar fra 0 til 1010
- `clustering` gaar mot et hoyt niva rundt 0.77-0.81
- `dim_proxy` faller mot ca. 0.23

Dette ligner mer pa tett lokal klyngedannelse enn pa et tynt, spacetime-lignende nettverk. Regimet holder sammen, men bygger opp en kompakt og sterkt triadisk struktur.

## Tolkning

Det mest interessante her er ikke en ny bevaringslov, men at sammenheng holdes oppe samtidig som lokal motivtetthet eksploderer. `components` oppforer seg som en effektiv dynamisk invariant i denne runnen, mens `triangles`, `c4`, `spectral_radius` og `clustering` fungerer som vekst- og kondensasjonsdiagnostikker.
