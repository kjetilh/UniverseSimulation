# Relasjonell universgraf v0.11d: lokal triad-raffinement

Dette er et dokumentasjonsskall for neste smale frontier-runde etter `v11c`.

## Status

Denne filen er foreløpig et plan-/skall-dokument.
Det ligger ingen fabrikerte runtime-resultater her.
Når `relational_universe_v11d_local_triad_refinement.py` kjøres med default output-stier, blir denne filen overskrevet med ekte lokale resultater.

## Formål

Spørsmålet i `v11d` er ikke en ny bred frontier-scan.
Spørsmålet er:

**Er `bridge_0010_0000` et ekte lokalt optimum langs `p_triad`-aksen ved fast `p_swap = 0.02` og `p_del = 0.0`, eller er det bare beste punkt på et fortsatt litt grovt grid?**

## Faste parametre

- `p_swap = 0.02`
- `p_del = 0.0`
- fire størrelsesnivåer beholdes for sammenlignbarhet med `v11c`

## Planlagt kandidatsett

- `band_zero_del`
- `bridge_0005_0000`
- `bridge_00075_0000`
- `bridge_0010_0000`
- `bridge_00125_0000`
- `bridge_0015_0000`

Valgfritt diagnostisk ytterpunkt:

- `bridge_0020_0000`

## Paakrevde outputs ved ekte kjøring

- `Documentation/v11d_local_triad_refinement_target_summary.csv`
- `Documentation/v11d_local_triad_refinement_candidate_summary.csv`
- `Documentation/v11d_local_triad_refinement_pairwise.csv`
- `Documentation/v0_11d_operativ_anbefaling.md`

## Beslutningslogikk

- `robust_local_optimum`: samme bridge-punkt vinner raw, CI-low og pairwise med tydelig margin, og target summary er ren
- `local_plateau`: flere naere bridge-punkter ligger tett, mens `band_zero_del` fortsatt taper operativt
- `unresolved`: metrikken splitter seg eller target summary blir uklar
- `frontier_revised`: `band_zero_del` tar tilbake raw, CI-low og pairwise under ren size-separasjon

## Hva som ma holdes adskilt

- algebraiske identiteter / definisjonelle forhold
- generator-/ensembleartefakter
- scoringartefakter
- dynamiske simulasjonsresultater
