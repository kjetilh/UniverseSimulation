# Relasjonell universgraf v0.12g: direkte oppfølgingspipeline etter v12f

## Formål

Denne runden oversetter v12f til et mer operativt sporsmal: finnes det en kompakt screeningpolicy som faktisk kan erstatte eller naesten erstatte `full_basis@0.50` i en oppfolgingspipeline, og hvor mange dyre oppfolgingskjoringer sparer vi da?

## Referanse

- Referansepipeline er `full_basis@0.50`. Den er valgt fordi v12f viste at dette er den sterkeste praktiske benchmarken for screening.
- Vi sammenligner kompakte policyer mot denne referansen, ikke bare mot `simulate_all`.

## Hvordan metricene leses

- `mean_saved_followups_vs_all_frac`: andel dyre oppfolgingskjoringer spart mot a simulere alle kandidater.
- `mean_saved_followups_vs_reference_frac`: ekstra spart andel mot referansepipeline. Positiv verdi betyr billigere enn `full_basis@0.50`.
- `joint_match_rate_eps_00`: andel split der policyen matcher eller slar referansen pa baade `within_target_best_hit` og `within_target_top_quartile_recall` uten toleranse.
- `joint_match_rate_eps_02`: samme, men med `0.02` absolutt toleranse. Dette er den mest praktiske naer-match-metrikken her.

## Pipeline-sammendrag

| rank | policy | budget | save_vs_all | save_vs_ref | best_hit | recall | d_best_hit_vs_ref | d_recall_vs_ref | match_exact | match_eps_02 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | full_basis | 0.500 | 0.500 | 0.000 | 0.525 | 0.548 | 0.000 | 0.000 | 1.000 | 1.000 |
| 2 | spectral_plus_dim | 0.667 | 0.333 | -0.167 | 0.679 | 0.692 | 0.154 | 0.144 | 0.833 | 0.833 |
| 3 | spectral_only | 0.667 | 0.333 | -0.167 | 0.704 | 0.706 | 0.179 | 0.158 | 0.817 | 0.817 |
| 4 | random_baseline | 0.500 | 0.500 | 0.000 | 0.496 | 0.496 | -0.029 | -0.052 | 0.517 | 0.517 |
| 5 | spectral_only | 0.500 | 0.500 | 0.000 | 0.542 | 0.540 | 0.017 | -0.008 | 0.467 | 0.467 |
| 6 | spectral_plus_dim | 0.500 | 0.500 | 0.000 | 0.504 | 0.504 | -0.021 | -0.044 | 0.467 | 0.467 |
| 7 | spectral_plus_dim | 0.333 | 0.667 | 0.167 | 0.312 | 0.331 | -0.212 | -0.217 | 0.067 | 0.067 |
| 8 | spectral_only | 0.333 | 0.667 | 0.167 | 0.271 | 0.325 | -0.254 | -0.223 | 0.067 | 0.067 |

## Operativ lesning

- Referansen `full_basis@0.50` holder `best_hit=0.525` og `recall=0.548`.
- `spectral_only@0.50` er den naermeste kompakte erstatningen: `d_best_hit_vs_ref=0.017`, `d_recall_vs_ref=-0.008`, men `save_vs_ref=0.000`.
- `spectral_only@0.333` gir faktisk ekstra sparing (`save_vs_ref=0.167`), men taper tydelig mot referansen pa bade hit og recall.
- `spectral_only@0.667` matcher referansen lettere, men koster mer (`save_vs_ref=-0.167`).
- Derfor stotter repoet forelopig ikke en kompakt policy som gir klar ekstra budsjettgevinst mot `full_basis@0.50` ved omtrent samme kvalitet. Det vi har er en enkel same-budget-substitutt, ikke en klar billigere vinner.

