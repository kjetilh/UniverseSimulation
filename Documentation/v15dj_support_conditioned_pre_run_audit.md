# Relasjonell universgraf v0.15dj: support-conditioned pre-run audit

## Formal

`v15dj` er en no-new-dynamics audit. Den leser `v15di_growth_seed_placement_summary.csv` og tester om billige support-/base-features kan rangere plausible `1024/add_chord` placements foer mer dynamikk brukes.

Dette er ikke en validert selector. Det er en scout for neste pre-registrerte fresh growth-seed holdout.

## Active placements used only for audit scoring

| growth_seed | placement | support_signature | established_rate | static_support_ball_1 | static_support_ball_2 | static_support_ball_3 | static_mean_support_degree |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 202 | 1 | 1,58,537 | 0.875 | 27.000 | 62.000 | 100.000 | 10.000 |
| 303 | 0 | 3,4,827 | 0.500 | 15.000 | 57.000 | 146.000 | 6.667 |
| 303 | 2 | 25,177,430 | 0.500 | 14.000 | 25.000 | 48.000 | 6.000 |

## Best simple support rules

| rule | growth_seed_hit_rate_top1 | total_active_capture_fraction_top1 | growth_seed_hit_rate_top2 | total_active_capture_fraction_top2 | inactive_selected_top1_total | status |
| --- | --- | --- | --- | --- | --- | --- |
| low_ball2_minus_ball1 | 1.000 | 0.667 | 1.000 | 0.667 | 0 | scout_candidate_top1_hits_each_seed_but_incomplete |
| low_ball3_minus_ball1 | 1.000 | 0.667 | 1.000 | 0.667 | 0 | scout_candidate_top1_hits_each_seed_but_incomplete |
| low_ball3_minus_ball2 | 1.000 | 0.667 | 1.000 | 0.667 | 0 | scout_candidate_top1_hits_each_seed_but_incomplete |
| low_static_support_ball_2 | 1.000 | 0.667 | 1.000 | 0.667 | 0 | scout_candidate_top1_hits_each_seed_but_incomplete |
| low_static_support_ball_3 | 1.000 | 0.667 | 1.000 | 0.667 | 0 | scout_candidate_top1_hits_each_seed_but_incomplete |
| high_ball1_over_ball3 | 0.500 | 0.333 | 1.000 | 0.667 | 1 | weak_broad_scout_candidate |
| high_ball2_over_ball3 | 0.500 | 0.333 | 1.000 | 0.667 | 1 | weak_broad_scout_candidate |
| high_static_mean_support_degree | 0.500 | 0.333 | 1.000 | 0.667 | 1 | weak_broad_scout_candidate |

## Best-rule per-seed predictions

| growth_seed | active_placements | ranked_placements | top1_placements | top2_placements | top1_hit | top2_hit | top1_capture_fraction | top2_capture_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 202 | p1 | p1;p2;p0 | p1 | p1;p2 | 1 | 1 | 1.000 | 1.000 |
| 303 | p0;p2 | p2;p1;p0 | p2 | p2;p1 | 1 | 1 | 0.500 | 0.500 |

## Diagnosis

| key | value | evidence |
| --- | --- | --- |
| artifact_scope | no_new_dynamics | read Documentation/v15di_growth_seed_placement_summary.csv |
| active_definition | established_rate_ge_0.50 | active placements are label-derived only for evaluating pre-run support rules |
| best_scout_rule | low_ball2_minus_ball1 | top1_hit_rate=1.000; total_capture_top1=0.667; status=scout_candidate_top1_hits_each_seed_but_incomplete |
| scout_candidate | found_sparse_candidate | low_ball2_minus_ball1;low_ball3_minus_ball1;low_ball3_minus_ball2;low_static_support_ball_2;low_static_support_ball_3 |
| selector_validation | not_validated | only two growth seeds and six placement summaries; at least one active placement remains missed by top1 scout rules |
| static_direction | not_universal | v15di already showed static degree direction changed across growth seeds; v15dj only ranks cheap base support features |
| next_step | pre_register_low_local_support_volume_holdout | run fresh growth seed with support-only ranking before dynamics; test top1/top2 scout placements plus a contrast |

## Interpretation

- En liten klasse av `low local support volume/gap`-regler treffer minst en aktiv placement i begge tilgjengelige growth seeds.
- Regelen er ikke nok til aa velge alle aktive placements: growth seed 303 har baade p0 og p2 aktive, mens low-volume-reglene typisk peker paa p2.
- Dette er dermed en nyttig pre-run prior, ikke en universell supportlov og ikke en dynamisk forklaring.
- Neste riktige dynamiske steg er aa pre-registrere support-rankingen paa en fresh growth seed foer runtime brukes, og saa teste top1/top2 pluss en kontrast.

## Files

- `relational_universe_v15dj_support_conditioned_pre_run_audit.py`
- `Documentation/v15dj_support_conditioned_placement_features.csv`
- `Documentation/v15dj_support_conditioned_rule_predictions.csv`
- `Documentation/v15dj_support_conditioned_rule_scores.csv`
- `Documentation/v15dj_support_conditioned_diagnosis.csv`
- `Documentation/v0_15dj_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dj.md`
