# v0.8b plottingrapport

## Hva figurene viser

- Heatmaps viser `mean_composite_natural` i slicer der `(r_death, p_swap, p_triad)` holdes fast og aksene er `r_birth` mot `p_del`.
- Errorbar-plottet viser punktestimat og bootstrap-intervall for hver kandidat rangert etter `ci_low_mean_composite_natural`.
- Size-distribution-plottet viser hvor store de ulike startensemblefamiliene faktisk ble målt i `initial_nodes`.
- Scatter-plottet viser koblingen mellom `avg_local_overlap` og `final_radius_control`, med `p_del` som fargekode.

## Hvordan figurene bør leses

- Heatmaps er nyttige for å se hvor følsom den naturlige robustheten er for små endringer i `p_del` og `r_birth`.
- Errorbars skiller mellom høye punktestimater og kandidater som også har løftet hele nedre bootstrap-båndet.
- Size-distribution-plottet er en ren ensemblekontroll: her skal de naturlige ensemblefamiliene ligge klart over `toy_cycle8`.
- Scatter-plottet sier ikke hva som er årsak, men det viser om høy overlap typisk sammenfaller med mindre slutt-radius i dette datasettet.

## Filer

- `v08b_heatmap_rd0.00_ps0.02_pt0.00.png`
- `v08b_heatmap_rd0.02_ps0.02_pt0.00.png`
- `v08b_heatmap_rd0.02_ps0.02_pt0.02.png`
- `v08b_heatmap_rd0.05_ps0.02_pt0.00.png`
- `v08b_bootstrap_errorbars.png`
- `v08b_initial_size_distributions.png`
- `v08b_overlap_vs_radius.png`
