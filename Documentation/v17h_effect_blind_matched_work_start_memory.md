# v17h effect-blind matched accepted-work start-memory gate

Status: `v17h_expanded_kernel_no_uniform_matched_work_gain`.

## Purpose and frozen design

Purpose `purpose://validation`: test whether the reverse-closed expanded length-2-to-5 kernel reduces finite start memory more efficiently than the qualified old length-2-to-4 kernel at exactly equal realized accepted work. Six frozen spaces, both starts and two new seed families are used. Source spectra and observed effects are prohibited.

Every chain targets exactly `192` accepted removed-edge units. The terminal rule rejects a Metropolis-accepted cycle only if it would overshoot the target or leave one unreachable unit. This is a symmetric finite stopping rule, not stationary sampling, and may add a small terminal conditioning bias.

## Frozen gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| effect_blind_integrity | pass | spectrum=0;effect=0 | 0;0 | continue |
| frozen_start_integrity | pass | 12/12 | 12/12 | continue |
| exact_matched_work_and_endpoint_integrity | pass | 48/48;work=192 | 48/48;each=192 | continue |
| retained_reverse_support | pass | 48/48 | 48/48 | continue |
| finite_movement_and_length5_exercise | pass | movement=48/48;expanded_length5=24/24 | 48/48;24/24 | continue |
| resource_bound | pass | 48/48;max=16.421854s | 48/48;each<=120s | continue |
| primary_matched_work_cross_start_reduction | fail | 0/6;ratio=0.980433-1.013939 | 6/6;each<=0.90 | retire_current_length5_as_uniform_start_memory_remedy |
| v17h_overall | v17h_expanded_kernel_no_uniform_matched_work_gain | exclusion=1;starts=12/12;work=48/48;support=48/48;movement=48/48;length5=24/24;resource=48/48;primary=0/6 | 1;12/12;48/48;48/48;48/48;24/24;48/48;6/6 | v17h_expanded_kernel_no_uniform_matched_work_gain |

## Primary matched-work response

| growth_seed | run_offset | old_median_cross_start_distance | expanded_median_cross_start_distance | expanded_over_old_cross_start_distance_ratio | directional_cross_start_reduction | material_cross_start_reduction_pass |
| --- | --- | --- | --- | --- | --- | --- |
| 9299 | 123078 | 0.444046 | 0.440601 | 0.992241 | 1 | 0 |
| 9299 | 123403 | 0.400392 | 0.392557 | 0.980433 | 1 | 0 |
| 9299 | 127341 | 0.413994 | 0.417542 | 1.008570 | 0 | 0 |
| 9365 | 123078 | 0.446173 | 0.449678 | 1.007854 | 0 | 0 |
| 9365 | 123403 | 0.388180 | 0.393590 | 1.013939 | 0 | 0 |
| 9365 | 127341 | 0.445358 | 0.444801 | 0.998748 | 1 | 0 |

Directional reduction occurred in `3/6`; material reduction passed `0/6`. Expanded/old cross-start ratios ranged `0.980433-1.013939` with median `1.003301`.

## Finite execution

All results are based on `48` finite chains. Maximum runtime was `16.421854` seconds, maximum attempts `887`, and minimum accepted length-5 count in the expanded arm `4`.

## Claim boundary

This is a relative finite efficiency/start-memory comparison. Even a pass would not establish global connectivity, convergence, mixing, a source effect, geometry or physics. A failure rejects only this fixed length-5 expansion as a uniform start-memory remedy under the frozen work target.
