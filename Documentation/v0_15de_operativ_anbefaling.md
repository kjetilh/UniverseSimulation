# Operativ anbefaling v0.15de

- `data_scope`: `no_new_dynamics_v15dd_only` fordi Analysen leser bare v15dd snapshot-log og run-summary.
- `leakage_guard`: `strict_windows_le_96` fordi Tidligste p1 established sustained high3 entry i v15dd er step 104; vinduer <=96 er strict pre-entry.
- `primary_result`: `pre_entry_feature_not_found` fordi Beste strict pre-entry feature `w96_mean_outer_share` har AUC=0.560.
- `entry_risk_best`: `w640_ready_both_rate` fordi Beste senere vindu har AUC=0.800 mot p0 false positives og skal behandles som entry-risk, ikke claim.
- `baseline_check`: `genealogy_intensity_still_not_selector` fordi Baseline genealogy-intensity har AUC=0.280 mot p0 false positives.
- `next_step`: `seek_non_route_pre_entry_observable` fordi Route-loggen forklarer outcome, men gir ikke tidlig selector under strict-vindu.

- Bare strict pre-entry-vinduer kan vurderes for pre-registrert selector.
- Entry-risk-vinduer er mekanistiske forklaringer, ikke selector-ready features.
