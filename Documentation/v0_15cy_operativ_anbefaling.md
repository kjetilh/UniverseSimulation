# Operativ anbefaling v0.15cy

- `input_control`: `clean` fordi Leste labs ['v15cw', 'v15cx'] fra eksisterende CSV-er; ingen ny dynamikk er kjoert.
- `coarse_label_result`: `coarse_event_labels_not_enough` fordi v15cx svekket birth_death_churn/split_fragment som kategorisk selector; v15cy tester derfor kontinuerlige genealogy-features.
- `continuous_intensity_axis`: `continuous_genealogy_intensity_promising_small_n` fordi Intensity AUC er 0.800 globalt, 0.875 for p1/1024 og 1.000 i holdout-only. Dette er lovende, men post-hoc og liten n.
- `best_p1_1024_metric`: `compress_per_step` fordi Beste p1/1024-metrikk etter AUC er compress_per_step med AUC 1.000 og Spearman mot horizon-span 0.893.
- `next_step`: `pre_register_continuous_intensity_holdout` fordi Frys intensity-score/top-metrikker og test paa nye runs foer scorevekter eller observabler justeres videre.

- Dette er en syntese av eksisterende v15cw/v15cx-resultater, ikke ny dynamikk.
- Ikke oppgrader intensity-score til global invariant, Lorentz-likhet, partikler eller entanglement.
