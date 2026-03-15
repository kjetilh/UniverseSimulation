# README – v0.5 perturbasjonslab

## Nye filer i dette steget
- `relational_universe_perturbation_lab.py`  
  Ny simulator for kopla replikater, lokal perturbasjon og causal-cone-målinger.

- `relasjonell_universgraf_v0_5_perturbasjon_og_kausalitet.md`  
  Hoveddokumentet for dette steget.

- `relasjonell_universgraf_status_v0_5.md`  
  Kort statusnotat.

- `relasjonell_universgraf_for_ikke_spesialister_v0_5.md`  
  Legmannsversjon av status og betydning.

- `perturbation_closed_summary.md`  
  Representativ lukket kjøring.

- `perturbation_open_summary.md`  
  Representativ åpen kjøring.

- `perturbation_closed_chord_summary.md`  
  Representativ charge-injiserende kontrollkjøring.

- `perturbation_multirun_stats.csv`  
  Rå oppsummeringsstatistikk for 6 kjøringer per regime.

- `perturbation_multirun_summary.md`  
  Kompakt markdown-oppsummering av multikjøringene.

## Rask start
### Lukket topologisk regime
```bash
python relational_universe_perturbation_lab.py   --label closed_v05   --steps 20000   --seed 123   --initial-cycle 10   --initial-tokens 4   --closed-topological   --r-seed 0.04   --r-token 1.0   --p-swap 0.08   --perturbation local_swap   --log-every 50
```

### Åpent topologisk regime
```bash
python relational_universe_perturbation_lab.py   --label open_v05   --steps 20000   --seed 123   --initial-cycle 10   --initial-tokens 4   --open-topological   --r-seed 0.04   --r-token 1.0   --p-triad 0.10   --p-del 0.06   --p-swap 0.08   --perturbation local_swap   --log-every 50
```

### Charge-injiserende test
```bash
python relational_universe_perturbation_lab.py   --label closed_chord_v05   --steps 8000   --seed 123   --initial-cycle 10   --initial-tokens 4   --closed-topological   --perturbation add_chord   --log-every 50
```

## Viktig metodisk note
Denne laben er laget for en token-lukket sektor.
Det er derfor shared-SSA-koblingen er eksakt.
Når birth/death skal inn igjen, må det bygges en ny koblingsmekanisme.
