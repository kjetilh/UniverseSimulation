# Relasjonell universgraf v0.15z for ikke-spesialister

Denne runden prøver ikke å bevise ny fysikk. Den prøver bare å forklare hvorfor tre små lokale tilfeller mellom `p0` og `p1` oppfører seg forskjellig.

Kort sagt fant vi at de tre utvalgte tilfellene ikke ser ut som tilfeldig støy:

- `151` ser ut som `p1_compact_radius_trigger`.
- `239` ser ut som `fragmented_fast_tradeoff_trigger`.
- `271` ser ut som `p0_calm_singleton_trigger`.

Det betyr ikke at vi har en universell lov. Det betyr at den lille `p0`/`p1`-familien nå ser mer strukturert ut enn før: noen ganger vinner `p1` fordi den låser mer kompakt og raskt, noen ganger taper `p1` fordi den blir for fragmentert, og noen ganger vinner `p0` fordi den holder en roligere singleton-lås.

Neste naturlige steg er `targeted_trigger_holdout`: Neste steg bør teste om disse triggerne holder på noen få nærliggende holdout-seeds, ikke åpne en ny bred scan.
