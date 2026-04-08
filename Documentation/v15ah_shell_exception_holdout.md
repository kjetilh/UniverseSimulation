# Relasjonell universgraf v0.15ah: shell exception holdout

## Formål

Denne runden tester om de små unntaksmekanismene fra `v15ag` faktisk replikerer på noen få nærliggende holdout-seeds, eller om de fleste holdouts faller tilbake til hovedfamilien `early_fragment_lock`.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Holdout summary

| placement | anchor seed | expected | match | revert to main | different exception | unresolved | exact return |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 239 | alternating_to_late_lock | 0.000 | 1.000 | 0.000 | 0.000 | 0.818 |
| 1 | 151 | alternating_to_late_lock | 0.000 | 0.500 | 0.000 | 0.500 | 1.000 |
| 1 | 179 | two_stage_fragment_lock | 0.000 | 0.500 | 0.000 | 0.500 | 0.872 |
| 1 | 211 | near_lock_boundary_case | 0.000 | 1.000 | 0.000 | 0.000 | 0.826 |
| 2 | 151 | singleton_resistance_case | 0.000 | 1.000 | 0.000 | 0.000 | 0.713 |
| 2 | 211 | alternating_to_late_lock | 0.000 | 1.000 | 0.000 | 0.000 | 0.709 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert og alle holdout-radene matcher ønsket add_chord-perturbasjon.
- `exception_holdout_status`: `exceptions_mostly_revert_to_main_family` fordi De fleste nærliggende holdouts faller tilbake til `early_fragment_lock`, så hovedkunnskapen er at unntakene er lokale avvik rundt en sterk hovedfamilie.
- `next_step`: `stop_exception_expansion` fordi Neste steg bør ikke være bredere unntaks-scan; vi bør heller bruke dette som støtte for at early-lock-familien er den robuste live-lesningen.

## Tolkning

- Dette er en liten holdout-runde rundt de kjente unntakene, ikke en ny bred seed-scan.
- Les dette som test av lokal generalisering, ikke som bevis for nye defect-arter.
