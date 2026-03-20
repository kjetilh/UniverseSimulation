# Relasjonell universgraf v0.12l: hybrid screening + adaptiv oppfølging

## Formål

Denne runden kombinerer dagens sterkeste screeningreferanse med adaptiv follow-up. Sporsmalet er om vi kan spare reell oppfolgingstid ved a bruke screening til a velge hvilke baser som far videre oppmerksomhet, og adaptiv follow-up til a begrense hvor mye arbeid hver valgt base far.

## Metode

- Regime holdes fast ved `band_zero_del`.
- Basene er de samme som i den maelte adaptive `v12k`-runden.
- Screening trener pa stratified holdout-splitt og rangerer testbaser innen hver størrelse.
- Deretter far bare de screenede basene follow-up, enten som `full_followup` eller adaptivt `probe2_top_half`.
- Datasett: `24` baser. Screeningsplitt: `40`. Timing-lokker per screeningpass: `300`.
- Dette er fortsatt arbeidsflyt og kostnad, ikke ny fysikk.

## Realiserte startstørrelser

| target | bases | mean_initial_nodes | q10 | q90 | separated_from_prev | mean_actual_radius | sd_actual_radius |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 48 | 6 | 48.0 | 48.0 | 48.0 | 1 | 4.472 | 0.565 |
| 96 | 6 | 96.0 | 96.0 | 96.0 | 1 | 5.194 | 1.684 |
| 192 | 6 | 192.0 | 192.0 | 192.0 | 1 | 8.028 | 1.781 |
| 256 | 6 | 256.0 | 256.0 | 256.0 | 1 | 7.028 | 2.026 |

## Hybrid policy-sammendrag

| rank | hybrid | screen | budget | followup | best_hit | recall | pairwise | total_s | speedup | d_best_hit | d_recall | near_match | faster_and_match |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | full_basis__full_followup | full_basis | 0.500 | full_followup | 0.656 | 0.656 | 0.654 | 26.890 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 |
| 2 | full_basis__probe2_top_half | full_basis | 0.500 | probe2_top_half | 0.575 | 0.575 | 0.590 | 18.052 | 1.494 | -0.081 | -0.081 | 0.675 | 0.675 |
| 3 | spectral_only__probe2_top_half | spectral_only | 0.500 | probe2_top_half | 0.556 | 0.556 | 0.601 | 17.679 | 1.525 | -0.100 | -0.100 | 0.475 | 0.475 |
| 4 | spectral_plus_dim__probe2_top_half | spectral_plus_dim | 0.667 | probe2_top_half | 0.494 | 0.494 | 0.562 | 18.079 | 1.494 | -0.163 | -0.163 | 0.475 | 0.475 |
| 5 | spectral_only__full_followup | spectral_only | 0.500 | full_followup | 0.662 | 0.662 | 0.668 | 26.372 | 1.020 | 0.006 | 0.006 | 0.650 | 0.400 |
| 6 | random_baseline__full_followup | random_baseline | 0.500 | full_followup | 0.644 | 0.644 | 0.646 | 27.599 | 0.976 | -0.013 | -0.013 | 0.725 | 0.275 |

## Operativ lesning

- Referansen `full_basis__full_followup` bruker i snitt `26.890` sekunder og setter nullpunktet for hit/recall.
- `full_basis__probe2_top_half` isolerer verdien av adaptiv oppfolging under samme screening. Den har `speedup=1.494`, `best_hit=0.575` og `recall=0.575`.
- `spectral_only__full_followup` isolerer verdien av enkel screening uten adaptiv follow-up. Den har `speedup=1.020`, `best_hit=0.662`, `recall=0.662` og `near_match=0.650`.
- `spectral_only__probe2_top_half` er den rene kompakt+adaptiv-hybriden. Den har `speedup=1.525`, `best_hit=0.556` og `recall=0.556`.
- `spectral_plus_dim__probe2_top_half` er kostnadssensitiv utfordrer. Den har `speedup=1.494` og `near_match=0.475`.
- Lesningen splitter seg derfor i to: `spectral_only__full_followup` er den naermeste same-budget-utfordreren pa middelverdier, mens `full_basis__probe2_top_half` er den tydeligste reelle tidsutfordreren. Ingen av dem er likevel robuste nok til a erstatte referansen.
- Denne runden skal derfor ikke leses som at vi har funnet en ny billig standard, men som at hybridsporet er mer lovende gjennom dypere adaptiv oppfolging enn gjennom enda mer finjustering av screeningbasiser.

