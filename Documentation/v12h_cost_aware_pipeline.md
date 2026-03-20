# Relasjonell universgraf v0.12h: kostnadsbevisst oppfølgingspipeline

## Formål

Denne runden legger et enkelt kostnadsregnskap oppa v12g. Maalet er a skille mellom to forskjellige pastander: 'samme oppfolgingsbudsjett' og 'samme totale arbeidskostnad'.

## Kostnadsmodell

- En dyr oppfolgingskjoring teller som kostnad `1.0`.
- Screening teller `screen_cost_per_feature` per feature per testkandidat.
- Dette er en eksplisitt arbeidsmodell, ikke ny fysikk. Den bor leses som ingeniormessig regnskap.

## Policyer per skjermkostnad

| screen_cost | policy | budget | cost_ratio_vs_ref | best_hit | recall | d_best_hit | d_recall | cost_neutral_rate | near_match_eps_02 | cost_neutral_and_match |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.000 | full_basis | 0.500 | 1.000 | 0.525 | 0.548 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |
| 0.000 | random_baseline | 0.500 | 1.000 | 0.496 | 0.496 | -0.029 | -0.052 | 1.000 | 0.517 | 0.517 |
| 0.000 | spectral_only | 0.500 | 1.000 | 0.542 | 0.540 | 0.017 | -0.008 | 1.000 | 0.467 | 0.467 |
| 0.000 | spectral_only | 0.667 | 1.333 | 0.704 | 0.706 | 0.179 | 0.158 | 0.000 | 0.817 | 0.000 |
| 0.000 | spectral_plus_dim | 0.500 | 1.000 | 0.504 | 0.504 | -0.021 | -0.044 | 1.000 | 0.467 | 0.467 |
| 0.000 | spectral_plus_dim | 0.667 | 1.333 | 0.679 | 0.692 | 0.154 | 0.144 | 0.000 | 0.833 | 0.000 |
| 0.010 | full_basis | 0.500 | 1.000 | 0.525 | 0.548 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |
| 0.010 | random_baseline | 0.500 | 0.909 | 0.496 | 0.496 | -0.029 | -0.052 | 1.000 | 0.517 | 0.517 |
| 0.010 | spectral_only | 0.500 | 0.927 | 0.542 | 0.540 | 0.017 | -0.008 | 1.000 | 0.467 | 0.467 |
| 0.010 | spectral_only | 0.667 | 1.230 | 0.704 | 0.706 | 0.179 | 0.158 | 0.000 | 0.817 | 0.000 |
| 0.010 | spectral_plus_dim | 0.500 | 0.945 | 0.504 | 0.504 | -0.021 | -0.044 | 1.000 | 0.467 | 0.467 |
| 0.010 | spectral_plus_dim | 0.667 | 1.248 | 0.679 | 0.692 | 0.154 | 0.144 | 0.000 | 0.833 | 0.000 |
| 0.020 | full_basis | 0.500 | 1.000 | 0.525 | 0.548 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |
| 0.020 | random_baseline | 0.500 | 0.833 | 0.496 | 0.496 | -0.029 | -0.052 | 1.000 | 0.517 | 0.517 |
| 0.020 | spectral_only | 0.500 | 0.867 | 0.542 | 0.540 | 0.017 | -0.008 | 1.000 | 0.467 | 0.467 |
| 0.020 | spectral_only | 0.667 | 1.144 | 0.704 | 0.706 | 0.179 | 0.158 | 0.000 | 0.817 | 0.000 |
| 0.020 | spectral_plus_dim | 0.500 | 0.900 | 0.504 | 0.504 | -0.021 | -0.044 | 1.000 | 0.467 | 0.467 |
| 0.020 | spectral_plus_dim | 0.667 | 1.178 | 0.679 | 0.692 | 0.154 | 0.144 | 0.000 | 0.833 | 0.000 |
| 0.040 | full_basis | 0.500 | 1.000 | 0.525 | 0.548 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |
| 0.040 | random_baseline | 0.500 | 0.714 | 0.496 | 0.496 | -0.029 | -0.052 | 1.000 | 0.517 | 0.517 |
| 0.040 | spectral_only | 0.500 | 0.771 | 0.542 | 0.540 | 0.017 | -0.008 | 1.000 | 0.467 | 0.467 |
| 0.040 | spectral_only | 0.667 | 1.010 | 0.704 | 0.706 | 0.179 | 0.158 | 0.000 | 0.817 | 0.000 |
| 0.040 | spectral_plus_dim | 0.500 | 0.829 | 0.504 | 0.504 | -0.021 | -0.044 | 1.000 | 0.467 | 0.467 |
| 0.040 | spectral_plus_dim | 0.667 | 1.067 | 0.679 | 0.692 | 0.154 | 0.144 | 0.000 | 0.833 | 0.000 |
| 0.060 | full_basis | 0.500 | 1.000 | 0.525 | 0.548 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |
| 0.060 | random_baseline | 0.500 | 0.625 | 0.496 | 0.496 | -0.029 | -0.052 | 1.000 | 0.517 | 0.517 |
| 0.060 | spectral_only | 0.500 | 0.700 | 0.542 | 0.540 | 0.017 | -0.008 | 1.000 | 0.467 | 0.467 |
| 0.060 | spectral_only | 0.667 | 0.908 | 0.704 | 0.706 | 0.179 | 0.158 | 1.000 | 0.817 | 0.817 |
| 0.060 | spectral_plus_dim | 0.500 | 0.775 | 0.504 | 0.504 | -0.021 | -0.044 | 1.000 | 0.467 | 0.467 |
| 0.060 | spectral_plus_dim | 0.667 | 0.983 | 0.679 | 0.692 | 0.154 | 0.144 | 1.000 | 0.833 | 0.833 |
| 0.080 | full_basis | 0.500 | 1.000 | 0.525 | 0.548 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |
| 0.080 | random_baseline | 0.500 | 0.556 | 0.496 | 0.496 | -0.029 | -0.052 | 1.000 | 0.517 | 0.517 |
| 0.080 | spectral_only | 0.500 | 0.644 | 0.542 | 0.540 | 0.017 | -0.008 | 1.000 | 0.467 | 0.467 |
| 0.080 | spectral_only | 0.667 | 0.830 | 0.704 | 0.706 | 0.179 | 0.158 | 1.000 | 0.817 | 0.817 |
| 0.080 | spectral_plus_dim | 0.500 | 0.733 | 0.504 | 0.504 | -0.021 | -0.044 | 1.000 | 0.467 | 0.467 |
| 0.080 | spectral_plus_dim | 0.667 | 0.919 | 0.679 | 0.692 | 0.154 | 0.144 | 1.000 | 0.833 | 0.833 |
| 0.100 | full_basis | 0.500 | 1.000 | 0.525 | 0.548 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 |
| 0.100 | random_baseline | 0.500 | 0.500 | 0.496 | 0.496 | -0.029 | -0.052 | 1.000 | 0.517 | 0.517 |
| 0.100 | spectral_only | 0.500 | 0.600 | 0.542 | 0.540 | 0.017 | -0.008 | 1.000 | 0.467 | 0.467 |
| 0.100 | spectral_only | 0.667 | 0.767 | 0.704 | 0.706 | 0.179 | 0.158 | 1.000 | 0.817 | 0.817 |
| 0.100 | spectral_plus_dim | 0.500 | 0.700 | 0.504 | 0.504 | -0.021 | -0.044 | 1.000 | 0.467 | 0.467 |
| 0.100 | spectral_plus_dim | 0.667 | 0.867 | 0.679 | 0.692 | 0.154 | 0.144 | 1.000 | 0.833 | 0.833 |

## Beste policy per skjermkostnad

| screen_cost | best_policy | budget | cost_neutral_and_match | near_match_eps_02 | mean_cost_delta_vs_ref |
| --- | --- | --- | --- | --- | --- |
| 0.000 | full_basis | 0.500 | 1.000 | 1.000 | 0.000 |
| 0.010 | full_basis | 0.500 | 1.000 | 1.000 | 0.000 |
| 0.020 | full_basis | 0.500 | 1.000 | 1.000 | 0.000 |
| 0.040 | full_basis | 0.500 | 1.000 | 1.000 | 0.000 |
| 0.060 | full_basis | 0.500 | 1.000 | 1.000 | 0.000 |
| 0.080 | full_basis | 0.500 | 1.000 | 1.000 | 0.000 |
| 0.100 | full_basis | 0.500 | 1.000 | 1.000 | 0.000 |

## Beste ikke-referanse-policy per skjermkostnad

| screen_cost | compact_policy | budget | compact_cost_neutral_and_match | compact_near_match_eps_02 | compact_mean_cost_delta_vs_ref |
| --- | --- | --- | --- | --- | --- |
| 0.000 | spectral_only | 0.500 | 0.467 | 0.467 | 0.000 |
| 0.010 | spectral_plus_dim | 0.500 | 0.467 | 0.467 | -0.720 |
| 0.020 | spectral_plus_dim | 0.500 | 0.467 | 0.467 | -1.440 |
| 0.040 | spectral_plus_dim | 0.500 | 0.467 | 0.467 | -2.880 |
| 0.060 | spectral_plus_dim | 0.667 | 0.833 | 0.833 | -0.320 |
| 0.080 | spectral_plus_dim | 0.667 | 0.833 | 0.833 | -1.760 |
| 0.100 | spectral_plus_dim | 0.667 | 0.833 | 0.833 | -3.200 |

## Operativ lesning

- Ved lav til moderat skjermkostnad ser `spectral_only@0.50` fortsatt ut som den riktige enkle same-budget-kandidaten. Ved `screen_cost=0.02` har den `cost_ratio_vs_ref=0.867` og `near_match_eps_02=0.467`.
- Repoet stotter derfor ikke en universell enkel vinner. Det stotter en betinget lesning: hvis screening er nesten gratis, behold `full_basis@0.50`; hvis screeningkostnaden faktisk teller litt, blir `spectral_only@0.50` mer konkurransedyktig; og ved hoyere skjermkostnad kan `spectral_plus_dim@0.667` bli en kostnadsnoytral utfordrer.

