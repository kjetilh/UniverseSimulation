# Relasjonell universgraf v0.9 – skala og naturlige ensembler

## Hva som ble gjort

v0.9 tar v0.8b-kandidatbåndet og presser det mot større, modellvokste startensembler. I denne runden brukes naturlige målområder rundt 64, 96 og 128 noder, og hvert størrelsesnivå kjøres i to burn-in-regimer: `moderate` og `deep`.

De faktiske realiserte startstørrelsene må leses fra `mean_initial_nodes` i aggregate-CSV-en; veksten treffer ikke alltid nominalt mål eksakt.

Kandidatene i denne runden er hentet fra toppdelen av v0.8b-rangeringen etter `ci_low_mean_composite_natural`; v0.9 innfører ingen ny samlescore. Fokus ligger i stedet på rå størrelsesavhengige mål og bootstrap-intervaller.

## Mål som rapporteres

- `avg_local_overlap`
- `final_radius_control`
- `final_edge_diff_count`
- `abs_drift_beta1_per_step`
- `abs_drift_spectral_radius_per_step`

Merk forskjellen mellom observasjon og fortolkning:

- observasjon: bootstrap-intervallene og slope-estimatene i CSV-filene,
- fortolkning: om små eller flate slope-verdier faktisk betyr en robust makroskopisk klasse.

## Kandidater i v0.9-shortlisten

- `v08b_top_1` = (0.02, 0.00, 0.02, 0.00, 0.01)
- `v08b_top_2` = (0.02, 0.02, 0.02, 0.00, 0.01)
- `v08b_top_3` = (0.02, 0.02, 0.02, 0.00, 0.00)
- `v08b_top_4` = (0.02, 0.00, 0.02, 0.00, 0.00)

## Aggregerte gruppeestimater

| candidate | burnin | target | mean init | overlap | radius | edge diff | |beta1 drift| | |spectral drift| |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v08b_top_3 | moderate | 128 | 106.0 | 0.977 | 2.000 | 2.000 | 0.0000 | 0.0001 |
| v08b_top_3 | deep | 96 | 89.0 | 0.971 | 1.500 | 2.000 | 0.0000 | 0.0002 |
| v08b_top_4 | moderate | 128 | 106.0 | 0.969 | 1.250 | 2.000 | 0.0000 | 0.0001 |
| v08b_top_1 | moderate | 96 | 78.5 | 0.966 | 0.750 | 2.000 | 0.0063 | 0.0004 |
| v08b_top_4 | deep | 96 | 89.0 | 0.965 | 2.000 | 2.000 | 0.0000 | 0.0003 |
| v08b_top_2 | moderate | 96 | 78.5 | 0.962 | 0.750 | 2.000 | 0.0073 | 0.0005 |
| v08b_top_3 | deep | 128 | 103.5 | 0.957 | 2.250 | 2.500 | 0.0000 | 0.0002 |
| v08b_top_2 | moderate | 128 | 106.0 | 0.954 | 1.750 | 2.250 | 0.0042 | 0.0005 |
| v08b_top_4 | moderate | 96 | 78.5 | 0.952 | 1.750 | 2.000 | 0.0000 | 0.0002 |
| v08b_top_2 | deep | 128 | 103.5 | 0.951 | 2.250 | 3.250 | 0.0104 | 0.0005 |
| v08b_top_1 | deep | 96 | 89.0 | 0.951 | 2.750 | 2.250 | 0.0073 | 0.0005 |
| v08b_top_1 | moderate | 128 | 106.0 | 0.950 | 2.500 | 2.250 | 0.0052 | 0.0005 |

## Skalaslope-estimater

| candidate | burnin | metric | slope | ci_low | ci_high |
| --- | --- | --- | --- | --- | --- |
| v08b_top_1 | deep | abs_drift_beta1_per_step | 0.00018 | -0.00003 | 0.00036 |
| v08b_top_1 | deep | abs_drift_spectral_radius_per_step | 0.00000 | -0.00002 | 0.00001 |
| v08b_top_1 | deep | avg_local_overlap | 0.00132 | -0.00034 | 0.00380 |
| v08b_top_1 | deep | final_radius_control | 0.00831 | -0.08825 | 0.08425 |
| v08b_top_1 | moderate | abs_drift_beta1_per_step | 0.00005 | -0.00008 | 0.00021 |
| v08b_top_1 | moderate | abs_drift_spectral_radius_per_step | 0.00000 | -0.00001 | 0.00001 |
| v08b_top_1 | moderate | avg_local_overlap | 0.00767 | 0.00176 | 0.02071 |
| v08b_top_1 | moderate | final_radius_control | -0.02975 | -0.12343 | 0.00785 |
| v08b_top_2 | deep | abs_drift_beta1_per_step | 0.00011 | -0.00006 | 0.00026 |
| v08b_top_2 | deep | abs_drift_spectral_radius_per_step | 0.00000 | -0.00003 | 0.00001 |
| v08b_top_2 | deep | avg_local_overlap | 0.00313 | -0.00049 | 0.00905 |
| v08b_top_2 | deep | final_radius_control | -0.02301 | -0.10632 | 0.06791 |
| v08b_top_2 | moderate | abs_drift_beta1_per_step | 0.00003 | -0.00011 | 0.00015 |
| v08b_top_2 | moderate | abs_drift_spectral_radius_per_step | 0.00000 | -0.00001 | 0.00001 |
| v08b_top_2 | moderate | avg_local_overlap | 0.00820 | 0.00155 | 0.02349 |
| v08b_top_2 | moderate | final_radius_control | -0.04755 | -0.16575 | 0.00337 |

## Foreløpig tolkning

Hvis et regime er virkelig robust på tvers av naturlig skala, bør vi se at overlap ikke kollapser raskt når initial størrelse vokser, samtidig som slutt-radius og de to driftmålene ikke blåser opp ukontrollert. Det er dette slope-tabellen forsøker å synliggjøre.

Denne runden beviser ikke en skarp faseovergang. Den svarer bare på en smalere, viktigere metodefråge: om de beste v0.8b-kandidatene fortsatt ser lesbare ut når starttilstandene blir større og mer naturlig genererte.

## Filer

- run CSV: `Documentation/v09_scale_runs.csv`
- aggregate CSV: `Documentation/v09_scale_aggregate.csv`
- slope CSV: `Documentation/v09_scale_slopes.csv`
