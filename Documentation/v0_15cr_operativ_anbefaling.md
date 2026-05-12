# Operativ anbefaling v0.15cr

- `p2_scale_selector`: `retire_as_primary_selector` fordi target 768 har en lokal p2-lomme, men target 896 er bare partial/not-supported og target 1024 er unsupported ogsa etter skalert budsjett.
- `p2_status`: `keep_as_target768_local_contrast` fordi p2 fortsatt er nyttig som lokal kontrast, men ikke som skalerende struktur.
- `new_best_candidate`: `add_chord_p0_scale_response` fordi add_chord_p0 horizon vokser fra `2.000` ved target 768 til `75.000` ved 896 og `86.000` ved 1024.
- `caveat`: `small_n_control_discovery` fordi add_chord_p0 var en kontrollprofil og er bare testet med to seed-deltaer per target.
- `next_step`: `v15cs_add_chord_p0_scale_response_holdout` fordi en fresh-seed holdout av p0 ved 896/1024 er mer informativ enn mer p2-budsjett.
- `do_not`: `do_not_reopen_lorentz_or_global_rules` fordi dagens evidens fortsatt ikke stoetter Lorentz-, global invariant- eller entanglement-sprak.

- Hvis v15cs bekrefter p0-responsen, kan den bli ny scale-response kandidat. Hvis den kollapser, boer neste steg vaere respons-fingerprint-syntese uten nye dynamiske runs.
