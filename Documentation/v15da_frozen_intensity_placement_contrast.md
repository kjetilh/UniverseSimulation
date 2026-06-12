# Relasjonell universgraf v0.15da: frozen intensity placement contrast

## Formal

Denne runden tester frossen v15cz `genealogy_intensity_index` mot en fresh placement-kontrast.
Nye dynamiske runs er `1024/add_chord` for `p0`, `p1` og `p2` paa samme friske seed-deltaer.
Score-spec er lastet fra v15cz og ikke refittet.

## Advisor panel

- Claude CLI ble forsokt, men svarte `Not logged in`.
- To remote Codex-subagenter anbefalte frozen-score placement-kontrast, ikke p1-only extension.
- Panelets claim-tak er lavt: hoyst `robust placement-conditioned mesoscale structure signal`, ikke partikler eller spacetime.

## Pre-registered scope

| field | value |
| --- | --- |
| target | 1024 |
| growth seed | 202 |
| perturbation | add_chord |
| placements | p0;p1;p2 |
| seed deltas | 9341;9391;9433;9479;9533;9587;9631;9677;9733;9781;9833;9887 |
| primary score | genealogy_intensity_index |
| primary outcome | established vs no_far_shell; non-decisive labels excluded |

## Placement summary

| placement | role | n | established | no | mixed | mean score | mean horizon | labels |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| p0 | fresh_weak_control | 12 | 1 | 10 | 0 | 0.618 | 13.917 | established_far_shell_horizon:1;failed_far_shell_horizon:1;no_far_shell_horizon:10 |
| p1 | fresh_positive_anchor | 12 | 10 | 1 | 1 | 0.678 | 144.417 | established_far_shell_horizon:10;mixed_far_shell_horizon:1;no_far_shell_horizon:1 |
| p2 | fresh_weak_control | 12 | 0 | 12 | 0 | 0.343 | 0.000 | no_far_shell_horizon:12 |

## Primary and secondary metrics

| metric | role | decisive | est | no | mixed | AUC | p | method | median delta | span rho |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| genealogy_intensity_index | primary | 34 | 11 | 23 | 1 | 0.711 | 0.025 | exact_rank_dp | 0.282 | 0.344 |
| compress_per_step | secondary | 34 | 11 | 23 | 1 | 0.480 | 0.576 | exact_rank_dp | 0.000 | -0.077 |
| first_split_earliness | secondary | 34 | 11 | 23 | 1 | 0.711 | 0.024 | exact_rank_dp | 0.103 | 0.328 |
| max_component_count_per_target | secondary | 34 | 11 | 23 | 1 | 0.680 | 0.048 | exact_rank_dp | 0.009 | 0.282 |
| churn_per_step | secondary | 34 | 11 | 23 | 1 | 0.704 | 0.030 | exact_rank_dp | 0.148 | 0.332 |
| birth_death_per_step | secondary | 34 | 11 | 23 | 1 | 0.708 | 0.027 | exact_rank_dp | 0.095 | 0.344 |

## Matched seed contrast

| seed | p0 label | p1 label | p2 label | p0 score | p1 score | p2 score | p1-p0 | p1-p2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9341 | failed_far_shell_horizon | established_far_shell_horizon | no_far_shell_horizon | 0.446 | 0.809 | 0.000 | 0.364 | 0.809 |
| 9391 | no_far_shell_horizon | established_far_shell_horizon | no_far_shell_horizon | 0.790 | 0.657 | 0.084 | -0.133 | 0.573 |
| 9433 | no_far_shell_horizon | established_far_shell_horizon | no_far_shell_horizon | 0.095 | 0.905 | 0.469 | 0.810 | 0.436 |
| 9479 | no_far_shell_horizon | established_far_shell_horizon | no_far_shell_horizon | 0.999 | 0.900 | 0.054 | -0.099 | 0.846 |
| 9533 | no_far_shell_horizon | established_far_shell_horizon | no_far_shell_horizon | 0.816 | 0.484 | 0.266 | -0.332 | 0.218 |
| 9587 | established_far_shell_horizon | established_far_shell_horizon | no_far_shell_horizon | 0.568 | 0.785 | 0.061 | 0.217 | 0.723 |
| 9631 | no_far_shell_horizon | established_far_shell_horizon | no_far_shell_horizon | 0.777 | 0.643 | 0.871 | -0.134 | -0.228 |
| 9677 | no_far_shell_horizon | mixed_far_shell_horizon | no_far_shell_horizon | 0.594 | 0.461 | 0.430 | -0.133 | 0.030 |
| 9733 | no_far_shell_horizon | established_far_shell_horizon | no_far_shell_horizon | 0.492 | 0.832 | 0.000 | 0.340 | 0.832 |
| 9781 | no_far_shell_horizon | no_far_shell_horizon | no_far_shell_horizon | 0.418 | 0.467 | 0.285 | 0.049 | 0.182 |
| 9833 | no_far_shell_horizon | established_far_shell_horizon | no_far_shell_horizon | 0.853 | 0.448 | 0.781 | -0.404 | -0.332 |
| 9887 | no_far_shell_horizon | established_far_shell_horizon | no_far_shell_horizon | 0.566 | 0.751 | 0.817 | 0.184 | -0.066 |

## Scope summary

- labels: `established_far_shell_horizon:11;failed_far_shell_horizon:1;mixed_far_shell_horizon:1;no_far_shell_horizon:23`
- primary AUC: `0.711`
- primary one-sided p: `0.025` via `exact_rank_dp`
- primary median delta: `0.282`
- p1 minus control mean score: `0.198`

## Operativ lesning

- `advisor_panel`: `remote_codex_panel_used_claude_unavailable` fordi Claude CLI svarte Not logged in; to remote Codex sub-agents anbefalte frozen-score placement-kontrast. Lokale modeller ble unngatt.
- `artifact_control`: `clean` fordi Startstorrelse er ren og alle requested add_chord-perturbations matcher faktisk perturbasjon.
- `pre_registration_control`: `frozen_v15cz_score_no_refit` fordi Score-spec er lastet fra v15cz-artefakten og brukt uten refit paa fresh p0/p1/p2-runs.
- `primary_contrast`: `frozen_intensity_placement_contrast_failed` fordi Balansen er nok, men primarscoren holder ikke: AUC=0.711, p=0.025, median_delta=0.282.
- `next_step`: `downgrade_score_to_descriptive_observable` fordi Genealogy-intensity bor da brukes deskriptivt, ikke som selector.

## Hva dette kan og ikke kan vise

- Positivt funn her kan styrke at frossen genealogy-intensitet skiller etablerte far-shell-runs fra no-horizon-runs i et placement-betinget add_chord-landskap.
- Det beviser ikke partikler, Lorentz-likhet, entanglement, global invariant eller universell emergent geometri.
- For en forsiktig `dette kan bygge univers-lignende struktur`-claim maa repoet vise flere uavhengige robuste signaler: repeterbare defects, ikke-trivielle interaksjoner, skalaoverforing, kontrollert anisotropi og minst en pre-registrert observabel som generaliserer uten refit.
