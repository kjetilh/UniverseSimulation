# PROJECT_CONTEXT_LIVE

Dette dokumentet er den korteste operative inngangen til dagens repo-state i `UniverseSimulation`.

## Arbeidsregler

- Filer pa disk er ground truth.
- Nyere lokale `.py`, `.md` og `.csv`-filer overstyrer eldre promptoppsummeringer hvis de sier noe annet.
- `focused_score` alene avgjor ikke frontier-vinnere.
- `uavklart` er en legitim konklusjon hvis raw score, CI-low og pairwise peker ulikt.
- Skill alltid mellom:
  - algebraiske identiteter,
  - generator-/ensembleartefakter,
  - scoringartefakter,
  - dynamiske simulasjonsresultater.

## Siste sikre live status

Per dagens lokale state er `v11c` den viktigste aktive frontier-runden.

- Script: `relational_universe_v11c_binary_bridge_vs_band.py`
- Hovedrapport: `Documentation/v11c_binary_bridge_vs_band.md`
- Kandidatsammendrag: `Documentation/v11c_binary_bridge_vs_band_candidate_summary.csv`
- Pairwise: `Documentation/v11c_binary_bridge_vs_band_pairwise.csv`
- Startstorrelser: `Documentation/v11c_binary_bridge_vs_band_target_summary.csv`
- Operativ anbefaling: `Documentation/v0_11c_operativ_anbefaling.md`

## Live frontier akkurat na

Den nyeste repo-stottede operative kandidaten er:

- `bridge_0010_0000`

Dette er fordi `v11c` viser at `bridge_0010_0000` vinner pa:

- raw `mean_composite`
- `CI low`
- pairwise bootstrap

Mens:

- `band_zero_del` fortsatt har best `focused_score`
- `bridge_0015_0000` ikke lenger er beste bridge-punkt
- swap ikke lenger ser ut til a vare sentrum av frontieren

## Viktige tall fra v11c

Fra `Documentation/v11c_binary_bridge_vs_band_candidate_summary.csv`:

- `bridge_0010_0000`
  - `mean_composite ~= 0.688`
  - `CI low ~= 0.629`
  - `top_prob ~= 0.933`
  - `pairwise_mean ~= 0.981`
  - `focused_score ~= 0.601`

- `band_zero_del`
  - `mean_composite ~= 0.570`
  - `CI low ~= 0.540`
  - `top_prob ~= 0.058`
  - `pairwise_mean ~= 0.579`
  - `focused_score ~= 0.625`

Fra `Documentation/v11c_binary_bridge_vs_band_pairwise.csv`:

- `P(bridge_0010_0000 > band_zero_del) = 0.942`
- `P(band_zero_del > bridge_0010_0000) = 0.058`

## Generatorstatus

Den eldre generator-/storrelseskrisen ser ut til a vaere ryddet bort i den aktive kjeden.

I `Documentation/v11c_binary_bridge_vs_band_target_summary.csv` er realiserte startstorrelser rent separert:

- 48 -> 48
- 96 -> 96
- 192 -> 192
- 256 -> 256

Derfor ser den naavaerende frontier-lesningen mer dynamisk enn generator-drevet ut.

## Hva som ikke lenger bor brukes som live sannhet

Disse er fortsatt viktige historisk, men ikke siste frontier:

- `v10f`: siste sikre baseline for band-korridoren
- `v11_mid_focus`: mellomsteg der bridge-korridoren tok over
- `v11b`: legitim mellomkonklusjon om `bridge_0015_0000` vs `band_zero_del`, men overstyrt av `v11c`

## Hvis noen skal sette seg inn raskt

Les i denne rekkefolgen:

1. `PROJECT_CONTEXT_LIVE.md`
2. `PROJECT_HISTORY_INDEX.md`
3. `Documentation/v11c_binary_bridge_vs_band.md`
4. `Documentation/v11c_binary_bridge_vs_band_candidate_summary.csv`
5. `Documentation/v11c_binary_bridge_vs_band_pairwise.csv`
6. `Documentation/v11c_binary_bridge_vs_band_target_summary.csv`
7. `Documentation/v0_11c_operativ_anbefaling.md`
