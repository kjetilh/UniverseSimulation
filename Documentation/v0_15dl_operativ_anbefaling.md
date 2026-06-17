# Operativ anbefaling v0.15dl

- `artifact_control`: `clean` fordi Target summaries are separated and add_chord requested-match is clean.
- `landscape_state`: `base_conditioned_placement_landscape` fordi Active placements vary by growth seed: {202: [1], 303: [0, 2], 404: [1]}; unique patterns=2.
- `retired_selector`: `low_support_rank_retired` fordi v15dk top1/top2 support-rank capture was zero; low local support volume/gap should not be reused as selector.
- `morphology_screen`: `weak_posthoc_top2_scout` fordi Best placement-level AUC metric is `delta_return_t2` with posthoc AUC=0.900; best rule status=weak_posthoc_top2_scout.
- `next_step`: `freeze_best_morphology_rule_for_small_v15dm_holdout` fordi Beste post-hoc regel er `delta_return_t2`/high; den maa fryses foer ny dynamikk og kan ikke rapporteres som validert.

- Ikke gjenbruk low-support-rank som selector.
- Behandle beste morfologiregel som post-hoc kandidat, ikke som evidens.
- Hvis vi gaar til v15dm, frys `delta_return_t2` med retning `high` foer ny dynamikk.
- Ikke oppgrader funnene til invariant/Lorentz/partikkel/entanglement-claim.
