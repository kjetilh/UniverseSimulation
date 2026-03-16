# README – relasjonell universgraf bundle v6

## Nye filer i v0.7-pakken
- `relasjonell_universgraf_v0_7_lokal_maksimal_kobling_og_repair.md`
- `relasjonell_universgraf_status_v0_7.md`
- `prosjektoversikt_v0_7.md`
- `relasjonell_universgraf_for_ikke_spesialister_v0_7.md`
- `v0_7_seed109_sammenligning.md`
- `v0_7_faseprobe_kandidater.md`
- `relational_universe_local_max_coupling_lab.py`
- `relational_universe_v07_phase_probe.py`

## Viktigste resultater
- v0.7 forbedrer lokal overlap og same-descriptor rate tydelig i hovedregimet.
- v0.7 viser ikke hyppig full meeting i dette regimet.
- faseproben peker mot et lite område med moderat birth og lav swap/triad som særlig interessant.

## Eksempelkommandoer
```bash
python relational_universe_local_max_coupling_lab.py   --mode compare   --label v07_bd_closed_swap   --out-prefix v07_bd_closed_swap   --steps 1200   --seed 101   --multirun-seeds 12   --r-birth 0.05   --r-death 0.05   --p-swap 0.08   --p-triad 0.0   --p-del 0.0
```

```bash
cd /mnt/data
python relational_universe_v07_phase_probe.py   --out-prefix v07_phase_probe_repr   --steps 500   --multirun-seeds 6   --start-seed 1300   --r-birth-grid 0.0,0.05   --r-death-grid 0.0,0.05   --p-swap-grid 0.04,0.08   --p-triad-grid 0.0,0.03   --p-del-grid 0.0
```