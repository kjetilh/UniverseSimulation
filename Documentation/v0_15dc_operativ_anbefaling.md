# Operativ anbefaling v0.15dc

- `data_scope`: `no_new_dynamics_v15da_only` fordi Analysen leser bare v15da runs og component trajectories.
- `censoring_rule`: `pre_first_high_or_early_limit` fordi Established-runs sensureres foer first_high_step; no-high-runs bruker early_step_limit.
- `primary_result`: `pre_horizon_route_precursor_weak` fordi Beste censored pre-horizon observabel `pre_far8_slope_per_100` er bare delvis separerende (p1-vs-p0-false AUC=0.780, established-vs-no AUC=0.794).
- `group_reading`: `p1_vs_p0_false_positive_pre_horizon` fordi p1 established median coherence=0.339 og pre_far8=0.166; p0 false positives median coherence=0.125 og pre_far8=0.066.
- `baseline_check`: `genealogy_intensity_still_not_selector` fordi Baseline genealogy-intensity har p1-vs-p0-false AUC=0.280; pre_route_coherence har AUC=0.620.
- `next_step`: `instrument_snapshot_route_entry_directly` fordi Treng mer direkte per-snapshot route-entry/retention logging; eksisterende sensurerte komponentfelt er ikke nok.

- Ikke bruk v15db downstream route-score som selector.
- Hvis v15dc bare gir svakt signal, neste steg er direkte snapshot-instrumentering av route-entry/retention.
