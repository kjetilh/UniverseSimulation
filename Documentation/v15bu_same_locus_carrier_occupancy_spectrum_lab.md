# Relasjonell universgraf v0.15bu: same-locus carrier occupancy spectrum lab

## Formal

Denne runden tester om add_chord og local_swap skiller lag tydeligere i hvor konsentrert haleopptreden er over skadede noder.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 96 | 96.0 | 96.0 | 96.0 | 1 |

## Occupancy spectrum summary

| perturbation | tail union | entropy | top1 share | top3 share | top5 share | occ sd | coarse return |
| --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord | 91.333 | 0.974 | 0.016 | 0.049 | 0.082 | 0.295 | 0.769 |
| local_swap | 95.000 | 0.970 | 0.016 | 0.049 | 0.081 | 0.295 | 0.743 |

## Spectrum deltas

| entropy gap swap-add | top3 gap add-swap | union gap swap-add | occ sd gap add-swap |
| --- | --- | --- | --- |
| -0.004 | 0.001 | 3.667 | -0.000 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle occupancy-runs matcher onsket perturbasjon.
- `carrier_occupancy_compare`: `occupancy_spectrum_still_mixed` fordi Heller ikke occupancy-spekteret splitter carrierne rent ved samme locus.
- `next_step`: `pause_same_locus_duels` fordi Neste steg bor forlate samme-locus-duellene og heller lete etter en ny familiestruktur eller et nytt skalahopp.

## Tolkning

- Dette er en ny observabelklasse pa samme locus, ikke mer av de gamle timing- eller core/shell-snittene.
- Positivt signal her betyr at carrierne skiller lag i konsentrasjonsgeometri, ikke nodvendigvis i alle andre beskrivelser samtidig.
