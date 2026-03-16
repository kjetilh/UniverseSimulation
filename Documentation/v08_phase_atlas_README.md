# README – v0.8 phase atlas

## Hovedfiler
- `relational_universe_v08_phase_atlas.py`: coarse atlas, bootstrap-CI, Paretofront, lokal refinement og liten `p_del`-akse.
- `relational_universe_v08_phase_atlas_plots.py`: plotting og heatmaps for coarse/refined CSV.

## Eksempelkommando

```bash
python3 relational_universe_v08_phase_atlas.py \
  --out-prefix Documentation/v08_phase_atlas \
  --steps-coarse 400 \
  --steps-refined 500 \
  --coarse-seeds 100,101,102 \
  --refined-seeds 400,401,402
```

```bash
python3 relational_universe_v08_phase_atlas_plots.py --input-prefix Documentation/v08_phase_atlas --out-dir Documentation/v08_phase_atlas_plots
```

## Viktig presisering

- Bootstrap-intervallene er seed-baserte robusthetsmål, ikke eksakte konfidensgrenser for en skarp fasegrense.
- `geometry robustness` er fortsatt bare en proxy-familie.
