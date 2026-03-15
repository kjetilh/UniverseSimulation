# README – v0.5 perturbasjonslab

## Nye filer i dette steget
- `relational_universe_perturbation_lab.py`  
  Simulator for kopla replikater, lokal perturbasjon, batch-kjøringer og causal-cone-målinger.

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
  Per-run headline-metrics for batch-kjøringene.

- `perturbation_multirun_summary.csv`  
  Aggregert middel/std per regime og perturbasjonstype.

- `perturbation_multirun_first_hits.csv`  
  Aggregert første-treff-statistikk per radius.

- `perturbation_multirun_summary.md`  
  Markdown-oppsummering av batch-kjøringene, inkludert tolkning og svar på forskningsspørsmålene.

- `perturbation_multirun_plots/`  
  Matplotlib-plott for `radius_control`, `edge_diff_count`, `regime_L1` og `local_swap` vs `add_chord`.

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

### Batch-modus med plott
```bash
python relational_universe_perturbation_lab.py \
  --mode batch \
  --label perturbation_multirun_v05 \
  --steps 400 \
  --initial-cycle 10 \
  --initial-tokens 4 \
  --log-every 40 \
  --seeds 101,102,103 \
  --regimes closed_topological,open_topological,aggressive_triad_delete \
  --perturbations local_swap,add_chord \
  --batch-summary-csv Documentation/perturbation_multirun_stats.csv \
  --batch-aggregate-csv Documentation/perturbation_multirun_summary.csv \
  --batch-log-csv Documentation/perturbation_multirun_log.csv \
  --batch-first-hit-csv Documentation/perturbation_multirun_first_hits.csv \
  --batch-summary-md Documentation/perturbation_multirun_summary.md \
  --batch-report-json Documentation/perturbation_multirun_report.json \
  --plots-dir Documentation/perturbation_multirun_plots
```

## Regimepresets
- `closed_topological`: swap-dominert, uten triadisk lukking eller delete.
- `open_topological`: moderat triadisk lukking og delete, fortsatt lokal token-sektor.
- `aggressive_triad_delete`: mer aggressiv triadic closure og delete for raskere lokal reorganisering.

## Nye batchmål
- `edge_jaccard_distance`: relativ forskjell mellom kantmengdene.
- `front_envelope_control`: løpende maksimum for `radius_control`.
- `first_hit` per radius: første tidspunkt og første steg der skadefronten har nådd gitt radius.

## Heuristisk batchtolking
- `ballistisk`: fronten sprer seg gjennom flere radiuslag med vedvarende positiv fit-hastighet.
- `lokal scrambling`: forskjellen blir mest liggende som lokal omrøring og makrodrift uten tydelig utadgående front.
- `blandet`: begge signaturer er til stede samtidig.

## Viktig metodisk note
Denne laben er laget for en token-lukket sektor.
Det er derfor shared-SSA-koblingen er eksakt.
Når birth/death skal inn igjen, må det bygges en ny koblingsmekanisme.
