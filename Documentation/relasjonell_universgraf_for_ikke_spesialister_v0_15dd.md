# Relasjonell universgraf for ikke-spesialister v0.15dd

Denne runden logger ikke bare om en fjernhale finnes til slutt, men naar et run faktisk gaar inn i en fjern rute og om det holder seg der.

- Hovedlesning: `direct_route_entry_retention_separates_false_positives`.
- Neste steg: `derive_pre_entry_features_from_direct_route_log` fordi Bruk snapshot-loggen til aa lage eksplisitte pre-entry kandidater; ikke bruk direct route outcome som predictor.

Kort sagt: vi prover aa skille ekte rute/retensjon fra lokal uro som bare ser kraftig ut.
