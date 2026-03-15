# Batch-rapport: perturbation_multirun_v05

## Konfigurasjon

- mode: batch
- steps: 400
- log_every: 40
- seeds: 101,102,103
- regimes: closed_topological,open_topological,aggressive_triad_delete
- perturbations: local_swap,add_chord

## Deskriptiv statistikk

Denne delen er ren observasjonsoppsummering. Den er ikke teoretisk tolkning.

| regime | perturbation | n | mean final_radius | std final_radius | mean max_radius | mean fit_speed | mean regime_L1 | mean delta_beta1 | mean edge_jaccard |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| aggressive_triad_delete | add_chord | 3 | 1.66667 | 0.57735 | 2.66667 | -0.00296067 | 285.718 | 6 | 0.693537 |
| aggressive_triad_delete | local_swap | 3 | 1.66667 | 0.57735 | 2.33333 | -0.00248033 | 414.702 | 5.33333 | 0.707009 |
| closed_topological | add_chord | 3 | 2.66667 | 0.57735 | 3.33333 | 0.011955 | 6.02702 | 1 | 0.812938 |
| closed_topological | local_swap | 3 | 2.66667 | 0.57735 | 3.33333 | 0.0181827 | 21.3453 | 0 | 0.84036 |
| open_topological | add_chord | 3 | 1.66667 | 0.57735 | 3 | -0.0119303 | 211.55 | 4 | 0.745505 |
| open_topological | local_swap | 3 | 1.66667 | 0.57735 | 3 | -0.0119303 | 297.593 | -1 | 0.824362 |

## Per-run oversikt

| regime | perturbation | seed | final_radius | max_radius | fit_speed | final_regime_L1 | delta_beta1 | edge_jaccard |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| closed_topological | local_swap | 101 | 3 | 4 | 0.023394 | 44.6004 | 0 | 0.869565 |
| closed_topological | local_swap | 102 | 2 | 3 | 3e-06 | 15.1581 | 0 | 0.818182 |
| closed_topological | local_swap | 103 | 3 | 3 | 0.031151 | 4.27732 | 0 | 0.833333 |
| closed_topological | add_chord | 101 | 3 | 4 | 0.023394 | 5.527 | 1 | 0.772727 |
| closed_topological | add_chord | 102 | 2 | 3 | 3e-06 | 8.29747 | 1 | 0.826087 |
| closed_topological | add_chord | 103 | 3 | 3 | 0.012468 | 4.25659 | 1 | 0.84 |
| open_topological | local_swap | 101 | 2 | 3 | -0.003566 | 123.987 | -5 | 0.878788 |
| open_topological | local_swap | 102 | 1 | 4 | -0.03168 | 252.272 | 9 | 0.875 |
| open_topological | local_swap | 103 | 2 | 2 | -0.000545 | 516.519 | -7 | 0.719298 |
| open_topological | add_chord | 101 | 2 | 3 | -0.003566 | 276.419 | 5 | 0.837209 |
| open_topological | add_chord | 102 | 1 | 4 | -0.03168 | 275.994 | 9 | 0.84375 |
| open_topological | add_chord | 103 | 2 | 2 | -0.000545 | 82.2382 | -2 | 0.555556 |
| aggressive_triad_delete | local_swap | 101 | 1 | 2 | 0.000399 | 916.403 | 7 | 0.439394 |
| aggressive_triad_delete | local_swap | 102 | 2 | 3 | -0.00784 | 52.7004 | 0 | 0.795918 |
| aggressive_triad_delete | local_swap | 103 | 2 | 2 | 0 | 275.004 | 9 | 0.885714 |
| aggressive_triad_delete | add_chord | 101 | 1 | 3 | -0.002762 | 398.793 | 2 | 0.46875 |
| aggressive_triad_delete | add_chord | 102 | 2 | 3 | -0.00612 | 168.405 | 6 | 0.754717 |
| aggressive_triad_delete | add_chord | 103 | 2 | 2 | 0 | 289.956 | 10 | 0.857143 |

## Første-treff-kurver per radius

| regime | perturbation | radius | hit_fraction | mean_hit_time | mean_hit_step |
| --- | --- | --- | --- | --- | --- |
| aggressive_triad_delete | add_chord | 0 | 1 | 0 | 0 |
| aggressive_triad_delete | add_chord | 1 | 1 | 10.823 | 40 |
| aggressive_triad_delete | add_chord | 2 | 1 | 14.7304 | 53.3333 |
| aggressive_triad_delete | add_chord | 3 | 0.666667 | 31.968 | 120 |
| aggressive_triad_delete | add_chord | 4 | 0 | NA | NA |
| aggressive_triad_delete | add_chord | 5 | 0 | NA | NA |
| aggressive_triad_delete | add_chord | 6 | 0 | NA | NA |
| aggressive_triad_delete | add_chord | 7 | 0 | NA | NA |
| aggressive_triad_delete | add_chord | 8 | 0 | NA | NA |
| aggressive_triad_delete | local_swap | 0 | 1 | 0 | 0 |
| aggressive_triad_delete | local_swap | 1 | 1 | 10.823 | 40 |
| aggressive_triad_delete | local_swap | 2 | 1 | 14.7304 | 53.3333 |
| aggressive_triad_delete | local_swap | 3 | 0.333333 | 30.8758 | 120 |
| aggressive_triad_delete | local_swap | 4 | 0 | NA | NA |
| aggressive_triad_delete | local_swap | 5 | 0 | NA | NA |
| aggressive_triad_delete | local_swap | 6 | 0 | NA | NA |
| aggressive_triad_delete | local_swap | 7 | 0 | NA | NA |
| aggressive_triad_delete | local_swap | 8 | 0 | NA | NA |
| closed_topological | add_chord | 0 | 1 | 0 | 0 |
| closed_topological | add_chord | 1 | 1 | 14.7304 | 53.3333 |
| closed_topological | add_chord | 2 | 1 | 14.7304 | 53.3333 |
| closed_topological | add_chord | 3 | 1 | 31.1372 | 120 |
| closed_topological | add_chord | 4 | 0.333333 | 43.7138 | 160 |
| closed_topological | add_chord | 5 | 0 | NA | NA |
| closed_topological | add_chord | 6 | 0 | NA | NA |
| closed_topological | add_chord | 7 | 0 | NA | NA |
| closed_topological | add_chord | 8 | 0 | NA | NA |
| closed_topological | local_swap | 0 | 1 | 0 | 0 |
| closed_topological | local_swap | 1 | 1 | 20.8199 | 80 |
| closed_topological | local_swap | 2 | 1 | 20.8199 | 80 |
| closed_topological | local_swap | 3 | 1 | 31.1372 | 120 |
| closed_topological | local_swap | 4 | 0.333333 | 43.7138 | 160 |
| closed_topological | local_swap | 5 | 0 | NA | NA |
| closed_topological | local_swap | 6 | 0 | NA | NA |
| closed_topological | local_swap | 7 | 0 | NA | NA |
| closed_topological | local_swap | 8 | 0 | NA | NA |
| open_topological | add_chord | 0 | 1 | 0 | 0 |
| open_topological | add_chord | 1 | 1 | 10.823 | 40 |
| open_topological | add_chord | 2 | 1 | 10.823 | 40 |
| open_topological | add_chord | 3 | 0.666667 | 21.6446 | 80 |
| open_topological | add_chord | 4 | 0.333333 | 10.2291 | 40 |
| open_topological | add_chord | 5 | 0 | NA | NA |
| open_topological | add_chord | 6 | 0 | NA | NA |
| open_topological | add_chord | 7 | 0 | NA | NA |
| open_topological | add_chord | 8 | 0 | NA | NA |
| open_topological | local_swap | 0 | 1 | 0 | 0 |
| open_topological | local_swap | 1 | 1 | 10.823 | 40 |
| open_topological | local_swap | 2 | 1 | 10.823 | 40 |
| open_topological | local_swap | 3 | 0.666667 | 21.6446 | 80 |
| open_topological | local_swap | 4 | 0.333333 | 10.2291 | 40 |
| open_topological | local_swap | 5 | 0 | NA | NA |
| open_topological | local_swap | 6 | 0 | NA | NA |
| open_topological | local_swap | 7 | 0 | NA | NA |
| open_topological | local_swap | 8 | 0 | NA | NA |

## Sammenlikning mellom `local_swap` og `add_chord`

| regime | delta radius (chord-swap) | delta fit_speed | delta regime_L1 | delta delta_beta1 |
| --- | --- | --- | --- | --- |
| aggressive_triad_delete | 0 | -0.000480333 | -128.984 | 0.666667 |
| closed_topological | 0 | -0.00622767 | -15.3183 | 1 |
| open_topological | 0 | 0 | -86.0428 | 5 |

## Kort batchtolking

- `aggressive_triad_delete` / `add_chord`: `lokal scrambling` fordi forskjellen blir mest liggende som lokal omorganisering og diffus makrodrift.
- `aggressive_triad_delete` / `local_swap`: `lokal scrambling` fordi forskjellen blir mest liggende som lokal omorganisering og diffus makrodrift.
- `closed_topological` / `add_chord`: `lokal scrambling` fordi forskjellen blir mest liggende som lokal omorganisering og diffus makrodrift.
- `closed_topological` / `local_swap`: `lokal scrambling` fordi forskjellen blir mest liggende som lokal omorganisering og diffus makrodrift.
- `open_topological` / `add_chord`: `lokal scrambling` fordi forskjellen blir mest liggende som lokal omorganisering og diffus makrodrift.
- `open_topological` / `local_swap`: `lokal scrambling` fordi forskjellen blir mest liggende som lokal omorganisering og diffus makrodrift.

## Svar på forskningsspørsmålene

- Robust tegn på begrenset causal cone: Ja, tentativt. aggressive_triad_delete/add_chord har monotone first-hit-kurver og endelig frontfart. aggressive_triad_delete/local_swap har monotone first-hit-kurver og endelig frontfart. closed_topological/add_chord har monotone first-hit-kurver og endelig frontfart.
- Varierer front-hastigheten sterkt mellom regimer: Ja. Effektiv frontfart varierer tydelig mellom gruppene; max/min-forholdet er omtrent 1.52.
- Universell eller ikke-universell effektiv hastighet: Dataene peker mot en ikke-universell effektiv hastighet; regimer og perturbasjonstype flytter frontfarten merkbart.

## Plott

- `Documentation/perturbation_multirun_plots/aggressive_triad_delete__add_chord_radius_time.png`
- `Documentation/perturbation_multirun_plots/aggressive_triad_delete__add_chord_edge_diff_time.png`
- `Documentation/perturbation_multirun_plots/aggressive_triad_delete__add_chord_regime_l1_time.png`
- `Documentation/perturbation_multirun_plots/aggressive_triad_delete__add_chord_radius_step.png`
- `Documentation/perturbation_multirun_plots/aggressive_triad_delete__local_swap_radius_time.png`
- `Documentation/perturbation_multirun_plots/aggressive_triad_delete__local_swap_edge_diff_time.png`
- `Documentation/perturbation_multirun_plots/aggressive_triad_delete__local_swap_regime_l1_time.png`
- `Documentation/perturbation_multirun_plots/aggressive_triad_delete__local_swap_radius_step.png`
- `Documentation/perturbation_multirun_plots/closed_topological__add_chord_radius_time.png`
- `Documentation/perturbation_multirun_plots/closed_topological__add_chord_edge_diff_time.png`
- `Documentation/perturbation_multirun_plots/closed_topological__add_chord_regime_l1_time.png`
- `Documentation/perturbation_multirun_plots/closed_topological__add_chord_radius_step.png`
- `Documentation/perturbation_multirun_plots/closed_topological__local_swap_radius_time.png`
- `Documentation/perturbation_multirun_plots/closed_topological__local_swap_edge_diff_time.png`
- `Documentation/perturbation_multirun_plots/closed_topological__local_swap_regime_l1_time.png`
- `Documentation/perturbation_multirun_plots/closed_topological__local_swap_radius_step.png`
- `Documentation/perturbation_multirun_plots/open_topological__add_chord_radius_time.png`
- `Documentation/perturbation_multirun_plots/open_topological__add_chord_edge_diff_time.png`
- `Documentation/perturbation_multirun_plots/open_topological__add_chord_regime_l1_time.png`
- `Documentation/perturbation_multirun_plots/open_topological__add_chord_radius_step.png`
- `Documentation/perturbation_multirun_plots/open_topological__local_swap_radius_time.png`
- `Documentation/perturbation_multirun_plots/open_topological__local_swap_edge_diff_time.png`
- `Documentation/perturbation_multirun_plots/open_topological__local_swap_regime_l1_time.png`
- `Documentation/perturbation_multirun_plots/open_topological__local_swap_radius_step.png`
- `Documentation/perturbation_multirun_plots/aggressive_triad_delete_local_swap_vs_add_chord_radius_time.png`
- `Documentation/perturbation_multirun_plots/closed_topological_local_swap_vs_add_chord_radius_time.png`
- `Documentation/perturbation_multirun_plots/open_topological_local_swap_vs_add_chord_radius_time.png`

## Skille mellom deskriptiv statistikk og teori

Tallene over er deskriptive. Tolkingene om causal cone og effektiv hastighet er heuristiske og må testes videre i større batcher og senere i birth/death-regimer med strengere kobling.
