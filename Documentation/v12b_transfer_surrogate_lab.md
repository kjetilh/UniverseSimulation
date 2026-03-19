# Relasjonell universgraf v0.12b: transfer og surrogate-lab

## Formål

Denne runden tester om den lille geometriske basisen fra v0.12 er lokalt nyttig bare i `band_zero_del`, eller om den transfererer til nærliggende triad-varianter.

## Startstorrelser

| target | mean_initial | q10 | q90 | separated_from_prev |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |
| 192 | 192.0 | 192.0 | 192.0 | 1 |
| 256 | 256.0 | 256.0 | 256.0 | 1 |

## Regimeutfall per størrelse

| regime | target | overlap | radius | fit_speed | rel_drift_triangles |
| --- | --- | --- | --- | --- | --- |
| band_zero_del | 48 | 0.685 | 4.375 | 0.221 | 0.177 |
| band_zero_del | 96 | 0.714 | 5.062 | 0.178 | 0.049 |
| band_zero_del | 192 | 0.763 | 6.125 | 0.199 | 0.044 |
| band_zero_del | 256 | 0.566 | 8.812 | 0.253 | 0.046 |
| bridge_00075_0000 | 48 | 0.747 | 3.625 | 0.176 | 0.201 |
| bridge_00075_0000 | 96 | 0.582 | 6.500 | 0.218 | 0.071 |
| bridge_00075_0000 | 192 | 0.723 | 6.188 | 0.185 | 0.072 |
| bridge_00075_0000 | 256 | 0.545 | 9.312 | 0.276 | 0.048 |
| bridge_0010_0000 | 48 | 0.644 | 4.438 | 0.209 | 0.229 |
| bridge_0010_0000 | 96 | 0.613 | 6.000 | 0.195 | 0.127 |
| bridge_0010_0000 | 192 | 0.679 | 6.250 | 0.184 | 0.045 |
| bridge_0010_0000 | 256 | 0.621 | 8.188 | 0.239 | 0.050 |

## Transfer av redusert basis

| metric | test_regime | basis | rmse | baseline_rmse | relative_skill |
| --- | --- | --- | --- | --- | --- |
| final_radius_control | band_zero_del | spectral_only | 2.4832 | 2.7597 | 0.100 |
| final_radius_control | band_zero_del | spectral_plus_clustering | 2.4817 | 2.7597 | 0.101 |
| final_radius_control | band_zero_del | full_basis | 2.2392 | 2.7597 | 0.189 |
| final_radius_control | bridge_00075_0000 | spectral_only | 2.2767 | 2.7998 | 0.187 |
| final_radius_control | bridge_00075_0000 | spectral_plus_clustering | 2.3000 | 2.7998 | 0.178 |
| final_radius_control | bridge_00075_0000 | full_basis | 2.3359 | 2.7998 | 0.166 |
| final_radius_control | bridge_0010_0000 | spectral_only | 2.2450 | 2.5432 | 0.117 |
| final_radius_control | bridge_0010_0000 | spectral_plus_clustering | 2.2574 | 2.5432 | 0.112 |
| final_radius_control | bridge_0010_0000 | full_basis | 2.3778 | 2.5432 | 0.065 |
| avg_local_overlap | band_zero_del | spectral_only | 0.2307 | 0.2307 | 0.000 |
| avg_local_overlap | band_zero_del | spectral_plus_clustering | 0.2241 | 0.2307 | 0.029 |
| avg_local_overlap | band_zero_del | full_basis | 0.2028 | 0.2307 | 0.121 |
| avg_local_overlap | bridge_00075_0000 | spectral_only | 0.2279 | 0.2276 | -0.002 |
| avg_local_overlap | bridge_00075_0000 | spectral_plus_clustering | 0.2408 | 0.2276 | -0.058 |
| avg_local_overlap | bridge_00075_0000 | full_basis | 0.2166 | 0.2276 | 0.048 |
| avg_local_overlap | bridge_0010_0000 | spectral_only | 0.2509 | 0.2511 | 0.001 |
| avg_local_overlap | bridge_0010_0000 | spectral_plus_clustering | 0.2577 | 0.2511 | -0.026 |
| avg_local_overlap | bridge_0010_0000 | full_basis | 0.2616 | 0.2511 | -0.042 |

## Tolkning

- Hvis `spectral_plus_clustering` holder positiv skill også utenfor `band_zero_del`, er det et bedre tegn på ekte struktur enn om den bare virker på anchor-regimet.
- Hvis full basis ikke slår en liten basis, tyder det på at vi ikke trenger mange koordinater for å bære det nyttige signalet.
- Hvis transfer bryter sammen med én gang, er geometrihypotesen fortsatt for lokal eller for svak.

## Operativ lesning

- For `final_radius_control` transfererer en liten basis faktisk til nærliggende regimer. Best off-anchor er `spectral_only` mot `bridge_00075_0000` med relative skill `0.187`.
- For `avg_local_overlap` er transfer svakere. Best off-anchor er `full_basis` mot `bridge_00075_0000` med relative skill `0.048`, sa dette sporet ser ikke robust ut ennå.
- Konklusjonen i denne runden er derfor moderat positiv for radius-prediksjon, men ikke for overlap/repair.

