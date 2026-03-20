# Relasjonell universgraf v0.12f: budsjettstyrt screening av starttilstander

## Formål

Denne runden tester om de enkle geometri-basisene fra v12e faktisk kan spare full simulasjonsbudsjett. Sporsmalet er ikke bare om de korrelerer med radius, men om de kan brukes til a velge hvilke baser vi faktisk bor bruke dyre dynamikk-kjoringer pa.

## Metode

- Arbeidsregime: `band_zero_del`.
- Datasett: `48` starttilstander og `288` underliggende dynamikk-kjoringer.
- Holdout-oppsett: `60` stratified split med testandel `0.50` per størrelse.
- Budsjettstigen er innen størrelse: vi scorer alle kandidater billig, men kjører full dynamikk bare på toppfraksjonen innen hver størrelse.
- Dette holder size-effekten under kontroll. Hvis vi ikke gjør det, kan en policy se god ut bare fordi den foretrekker store ensembler.
- Budsjettfraksjoner: 0.167, 0.333, 0.500, 0.667, 0.833.

## Hvordan metricene leses

- `within_target_best_hit`: hvor ofte policyen fanger den beste testbasen innen hver størrelse.
- `within_target_top_quartile_recall`: hvor stor andel av de faktisk beste kvartil-basene som blir med videre innen hver størrelse.
- `within_target_selected_lift`: hvor mye bedre de utvalgte basene er enn gjennomsnittet innen samme størrelse.
- `auc_*`: samlet budsjettkurve-score over hele budsjettstigen. Hoy verdi betyr at policyen holder seg nyttig over mange budsjettvalg.
- `budget_to_match_full_basis_*`: minste budsjett en policy trenger for a na samme nivaa som `full_basis` ved budsjett `0.50`.

## Startstørrelser og etikettspenn

| target | bases | mean_initial | q10 | q90 | separated_from_prev | mean_actual_radius | sd_actual_radius |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 48 | 12 | 48.0 | 48.0 | 48.0 | 1 | 4.208 | 0.916 |
| 96 | 12 | 96.0 | 96.0 | 96.0 | 1 | 6.181 | 0.826 |
| 192 | 12 | 192.0 | 192.0 | 192.0 | 1 | 7.597 | 1.088 |
| 256 | 12 | 256.0 | 256.0 | 256.0 | 1 | 7.000 | 1.777 |

## Budsjettkurver

| policy | budget | within_target_best_hit | within_target_top_quartile_recall | within_target_selected_lift |
| --- | --- | --- | --- | --- |
| full_basis | 0.167 | 0.221 | 0.212 | 0.085 |
| full_basis | 0.333 | 0.358 | 0.390 | 0.040 |
| full_basis | 0.500 | 0.525 | 0.548 | 0.016 |
| full_basis | 0.667 | 0.717 | 0.729 | 0.012 |
| full_basis | 0.833 | 0.875 | 0.887 | 0.004 |
| oracle_actual | 0.167 | 1.000 | 0.500 | 0.260 |
| oracle_actual | 0.333 | 1.000 | 1.000 | 0.187 |
| oracle_actual | 0.500 | 1.000 | 1.000 | 0.134 |
| oracle_actual | 0.667 | 1.000 | 1.000 | 0.090 |
| oracle_actual | 0.833 | 1.000 | 1.000 | 0.049 |
| random_baseline | 0.167 | 0.183 | 0.165 | 0.018 |
| random_baseline | 0.333 | 0.342 | 0.340 | 0.007 |
| random_baseline | 0.500 | 0.496 | 0.496 | 0.004 |
| random_baseline | 0.667 | 0.671 | 0.654 | 0.001 |
| random_baseline | 0.833 | 0.846 | 0.827 | 0.002 |
| spectral_only | 0.167 | 0.096 | 0.150 | 0.032 |
| spectral_only | 0.333 | 0.271 | 0.325 | 0.025 |
| spectral_only | 0.500 | 0.542 | 0.540 | 0.031 |
| spectral_only | 0.667 | 0.704 | 0.706 | 0.025 |
| spectral_only | 0.833 | 0.917 | 0.877 | 0.021 |
| spectral_plus_dim | 0.167 | 0.113 | 0.142 | 0.023 |
| spectral_plus_dim | 0.333 | 0.312 | 0.331 | 0.027 |
| spectral_plus_dim | 0.500 | 0.504 | 0.504 | 0.022 |
| spectral_plus_dim | 0.667 | 0.679 | 0.692 | 0.022 |
| spectral_plus_dim | 0.833 | 0.904 | 0.867 | 0.020 |

## Budsjett-effektivitet

| rank | policy | auc_best_hit | auc_top_quartile_recall | auc_selected_lift | budget_to_match_full_basis_hit50 | budget_to_match_full_basis_recall50 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | oracle_actual | 1.000 | 0.938 | 0.142 | 0.167 | 0.333 |
| 2 | full_basis | 0.537 | 0.554 | 0.028 | 0.500 | 0.500 |
| 3 | spectral_only | 0.506 | 0.521 | 0.027 | 0.500 | 0.667 |
| 4 | random_baseline | 0.506 | 0.496 | 0.006 | 0.667 | 0.667 |
| 5 | spectral_plus_dim | 0.501 | 0.508 | 0.023 | 0.667 | 0.667 |

## Operativ lesning

- Budsjett-benchmark i denne runden er `full_basis` med auc-best-hit `0.537`.
- Beste kompakte policy er `spectral_only` med auc-best-hit `0.506` og budsjett for a matche `full_basis@0.50` lik `0.500`.
- Dette reviderer den tidligere kompakte arbeidslesningen fra v12c-v12e: i selve budsjettpolicy-oppgaven er `spectral_only` na sterkere enn `spectral_plus_dim`.
- Dette betyr at repoet na skiller mellom beste screening-benchmark og beste lille arbeidsbasis ogsa i en eksplisitt budsjettpolicy.
- Samtidig er gevinsten smal: `spectral_only` ligger bare hairline foran `random_baseline` pa budsjettkurve-sammendraget (`0.506` mot `0.506`). Den praktiske verdien ser derfor mest ut til a ligge rundt middels budsjett, ikke som en stor kurvevid separasjon.
- Denne runden ma leses som en offline beslutningsbenchmark. Den sier noe om mulig simuleringseffektivitet, ikke om ny grunnfysikk.
