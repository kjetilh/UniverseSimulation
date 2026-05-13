# Relasjonell universgraf v0.15ct: response fingerprint synthesis

## Formal

Denne runden kjorer ingen ny dynamikk. Den samler v15cn/v15cp/v15cq/v15cs og klassifiserer profile-respons etter fingerprint i stedet for p0/p2-label.

## Response classes

| class | meaning |
| --- | --- |
| strong_persistent_far_shell | established, long horizon, high retention/far-shell metrics |
| moderate_persistent_far_shell | established with nontrivial horizon, but weaker than strong |
| diffuse_far_mass_no_horizon | far mass/distance exists but no sustained horizon |
| no_horizon | no established horizon and no far-mass class |
| transient_or_partial_horizon | nonzero horizon without established response |

## Fingerprint highlights

| lab | target | profile | seed scope | class | score | established | horizon | distance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v15cn | 768 | add_chord_p2 | old_seed_deltas | strong_persistent_far_shell | 5 | 0.500 | 64.500 | 4.503 |
| v15cn | 768 | local_swap_p2 | old_seed_deltas | moderate_persistent_far_shell | 4 | 0.500 | 64.500 | 3.890 |
| v15cn | 1024 | add_chord_p0 | old_seed_deltas | moderate_persistent_far_shell | 5 | 0.500 | 33.500 | 5.601 |
| v15cp | 1024 | add_chord_p0 | old_seed_deltas | strong_persistent_far_shell | 6 | 0.500 | 86.000 | 5.774 |
| v15cq | 896 | add_chord_p0 | old_seed_deltas | moderate_persistent_far_shell | 4 | 0.500 | 75.000 | 3.351 |
| v15cq | 896 | add_chord_p2 | old_seed_deltas | moderate_persistent_far_shell | 6 | 0.500 | 49.500 | 5.805 |
| v15cs | 896 | add_chord_p0 | fresh_seed_deltas | strong_persistent_far_shell | 6 | 1.000 | 136.000 | 6.683 |
| v15cs | 896 | add_chord_p2 | fresh_seed_deltas | moderate_persistent_far_shell | 6 | 0.500 | 45.500 | 5.873 |
| v15cs | 896 | local_swap_p0 | fresh_seed_deltas | strong_persistent_far_shell | 6 | 0.500 | 86.500 | 6.293 |
| v15cs | 1024 | add_chord_p2 | fresh_seed_deltas | strong_persistent_far_shell | 5 | 0.500 | 82.500 | 3.989 |

## Seed stability

| target | profile | old class | fresh class | changed | horizon delta |
| --- | --- | --- | --- | --- | --- |
| 896 | add_chord_p0 | moderate_persistent_far_shell | strong_persistent_far_shell | 1 | 61.000 |
| 896 | add_chord_p2 | moderate_persistent_far_shell | moderate_persistent_far_shell | 0 | -4.000 |
| 896 | local_swap_p0 | no_horizon | strong_persistent_far_shell | 1 | 86.500 |
| 1024 | add_chord_p0 | strong_persistent_far_shell | no_horizon | 1 | -86.000 |
| 1024 | add_chord_p2 | diffuse_far_mass_no_horizon | strong_persistent_far_shell | 1 | 82.500 |
| 1024 | local_swap_p0 | diffuse_far_mass_no_horizon | diffuse_far_mass_no_horizon | 0 | 0.000 |

## Decisions

- `p0_label_stability`: `not_stable` -> `do_not_continue_p0_as_scale_law` fordi add_chord_p0 is strong at 896 on fresh seeds but collapses at 1024; old 1024 p0 did not replicate.
- `p2_label_stability`: `not_stable` -> `do_not_revive_p2_as_primary_scale_selector` fordi add_chord_p2 is not target-768 supported, partial at 896, absent in old 1024, but active in fresh 1024.
- `carrier_level_signal`: `add_chord_placement_sensitive_live` -> `map_add_chord_placements_before_more_label_claims` fordi add_chord has 8 persistent-far-shell observations versus local_swap 2, but placement/seed identity changes.
- `seed_stability`: `unstable` -> `treat_label_specific_pockets_as_seed_sensitive` fordi 4/6 old-vs-fresh scaled profile comparisons change response class.
- `next_step`: `placement_response_map` -> `v15cu_add_chord_placement_response_map` fordi Response fingerprints support add_chord carrier-level activity but not p0/p2 label stability.

## Operativ tolkning

- P0 er ikke stabil nok til aa behandles som scale-law-kandidat.
- P2 skal ikke gjenopplives som primaer scale-selector.
- Add_chord-carrieren er fortsatt live, men responsen er placement-/seed-sensitiv.
- Neste dynamiske steg boer derfor mappe add_chord placements ved 896/1024, ikke bruke mer budsjett paa en enkelt p0/p2-label.
