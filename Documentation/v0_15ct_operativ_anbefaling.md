# Operativ anbefaling v0.15ct

- `p0_label_stability`: `not_stable` fordi add_chord_p0 is strong at 896 on fresh seeds but collapses at 1024; old 1024 p0 did not replicate. Beslutning: `do_not_continue_p0_as_scale_law`.
- `p2_label_stability`: `not_stable` fordi add_chord_p2 is not target-768 supported, partial at 896, absent in old 1024, but active in fresh 1024. Beslutning: `do_not_revive_p2_as_primary_scale_selector`.
- `carrier_level_signal`: `add_chord_placement_sensitive_live` fordi add_chord has 8 persistent-far-shell observations versus local_swap 2, but placement/seed identity changes. Beslutning: `map_add_chord_placements_before_more_label_claims`.
- `seed_stability`: `unstable` fordi 4/6 old-vs-fresh scaled profile comparisons change response class. Beslutning: `treat_label_specific_pockets_as_seed_sensitive`.
- `next_step`: `placement_response_map` fordi Response fingerprints support add_chord carrier-level activity but not p0/p2 label stability. Beslutning: `v15cu_add_chord_placement_response_map`.

- `next_step`: `v15cu_add_chord_placement_response_map` fordi response-fingerprints peker mot add_chord carrier-level aktivitet, men ikke stabil p0/p2-label.
- Ikke les dette som global invariant-, Lorentz- eller entanglement-evidens.
