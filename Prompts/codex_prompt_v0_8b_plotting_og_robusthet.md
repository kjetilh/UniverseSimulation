# Codex-prompt: plotting og robusthetsvisualisering for v0.8b

Les følgende filer:

- `relational_universe_v08b_natural_ensemble_robustness.py`
- `v08b_natural_ensemble_runs.csv`
- `v08b_natural_ensemble_aggregate.csv`
- `v08b_candidate_robustness.csv`

Lag en plotting-modul som produserer:
1. heatmaps over `p_del` vs `r_birth` for natural mean composite
2. errorbar-plott for bootstrap-intervaller per kandidat
3. ensemble-sammenligning av initial size distributions
4. scatter-plott av overlap vs radius, fargekodet etter `p_del`

Krav:
- bruk matplotlib, ikke seaborn
- ett plott per figur
- ingen hardkodede farger hvis det ikke er nødvendig
- lagre filer til disk og skriv en kort `.md`-rapport som forklarer hvert plott
