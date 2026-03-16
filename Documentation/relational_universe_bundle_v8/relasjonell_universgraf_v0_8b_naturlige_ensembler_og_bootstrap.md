# Relasjonell universgraf v0.8b – p_del, naturlige startensembler og bootstrap-robusthet

## Sammendrag

v0.8b er den første eksplisitte robusthetstesten som tar Codex-innvendingen på alvor: lovende regimer må ikke bare se bra ut på små seedede leketøytilstander, men også på større og mer naturlige startensembler.

Dette steget gjør tre ting samtidig:

1. åpner `p_del`-aksen lokalt rundt v0.8-kandidatbåndet,
2. erstatter små rene sykler som eneste startpunkt med flere større og mer naturlige ensembler vokst frem av modellens egen dynamikk,
3. legger til bootstrap-baserte usikkerhetsintervaller for ensemblevis og samlet naturlig robusthet.

## Hva som regnes som 'naturlige' startensembler her

I stedet for å hånddesigne store startgrafer lar vi modellen selv vokse dem frem fra en liten sykel under en moderat åpen referansedynamikk. Det gir tre naturlige ensembler:

- `natural24`: vokst til rundt 24 noder
- `natural48`: vokst til rundt 48 noder
- `natural_jitter`: vokst til tilfeldig moderat størrelse og gitt ekstra burn-in

I tillegg beholdes `toy_cycle8` som ren kontinuitetsbaseline mot eldre trinn, men denne inngår ikke i den naturlige robusthetsscoren.

## Viktigste funn

- Beste kandidat etter **naturlig robusthet** hadde parametere `(r_birth, r_death, p_swap, p_triad, p_del)=(0.02, 0.00, 0.02, 0.00, 0.01)` med mean natural composite ≈ 0.730 og bootstrap-lower-bound ≈ 0.688.
- Nest beste kandidat lå svært nær: mean natural composite ≈ 0.717, lower-bound ≈ 0.634.
- Det lovende kandidatbåndet overlevde i hovedsak overgangen til større og mer naturlige starttilstander, men rangeringen ble strammere og mer selektiv.
- `p_del` oppførte seg ikke monotont overalt: små positive verdier var enkelte steder kompatible med høy score, men høyere `p_del` presset oftere opp radius eller trakk ned overlap.
- De største naturlige starttilstandene var nyttige fordi de skilte bedre mellom regimer som bare så bra ut på små sykler og regimer som faktisk beholdt struktur under mer moden initial geometri.

## Toppkandidater rangert etter bootstrap-lower-bound på naturlig composite

| r_birth | r_death | p_swap | p_triad | p_del | mean_nat | ci_low_nat | ci_high_nat | min_nat | sd_nat | radius | overlap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.02 | 0 | 0.02 | 0 | 0.01 | 0.730 | 0.688 | 0.771 | 0.650 | 0.057 | 2.867 | 0.660 |
| 0.02 | 0.02 | 0.02 | 0.02 | 0 | 0.717 | 0.634 | 0.858 | 0.634 | 0.100 | 2.933 | 0.660 |
| 0.02 | 0.02 | 0.02 | 0 | 0.01 | 0.674 | 0.620 | 0.756 | 0.620 | 0.059 | 2.933 | 0.643 |
| 0.02 | 0.02 | 0.02 | 0 | 0 | 0.662 | 0.589 | 0.735 | 0.589 | 0.099 | 3.600 | 0.644 |
| 0.02 | 0 | 0.02 | 0 | 0 | 0.666 | 0.586 | 0.744 | 0.586 | 0.104 | 3.600 | 0.649 |
| 0.08 | 0.02 | 0.02 | 0 | 0.01 | 0.635 | 0.568 | 0.700 | 0.568 | 0.090 | 3.533 | 0.664 |
| 0.02 | 0.05 | 0.02 | 0 | 0.01 | 0.650 | 0.565 | 0.724 | 0.565 | 0.099 | 3.200 | 0.630 |
| 0.02 | 0 | 0.02 | 0 | 0.02 | 0.660 | 0.565 | 0.813 | 0.532 | 0.116 | 3.200 | 0.674 |
| 0.02 | 0.05 | 0.02 | 0 | 0.02 | 0.616 | 0.560 | 0.662 | 0.560 | 0.042 | 3.333 | 0.639 |
| 0.08 | 0.02 | 0.02 | 0 | 0.04 | 0.611 | 0.551 | 0.658 | 0.551 | 0.045 | 3.600 | 0.690 |

## Oppsummering per ensemble

| ensemble | mean init nodes | mean init tokens | mean init beta1 | mean composite(best point) | best point |
| --- | --- | --- | --- | --- | --- |
| natural24 | 33.20 | 4.60 | 2.00 | 0.838 | (0.02,0.05,0.02,0.00,0.00) |
| natural48 | 53.00 | 13.20 | 9.60 | 0.858 | (0.02,0.02,0.02,0.02,0.00) |
| natural_jitter | 40.80 | 9.00 | 6.00 | 0.846 | (0.08,0.02,0.02,0.00,0.00) |
| toy_cycle8 | 8.00 | 4.00 | 1.00 | 0.871 | (0.02,0.05,0.02,0.00,0.02) |

## p_del-snitt for de viktigste basislinjene

### refined_winner-linjen `(0.08, 0.02, 0.02, 0.00, p_del)`

| p_del | mean_nat | ci_low | ci_high | min_nat | radius | overlap |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.646 | 0.406 | 0.846 | 0.406 | 3.400 | 0.637 |
| 0.01 | 0.635 | 0.568 | 0.700 | 0.568 | 3.533 | 0.664 |
| 0.02 | 0.461 | 0.360 | 0.602 | 0.300 | 4.333 | 0.624 |
| 0.04 | 0.611 | 0.551 | 0.658 | 0.551 | 3.600 | 0.690 |

### coarse_balanced-linjen `(0.02, 0.02, 0.02, 0.00, p_del)`

| p_del | mean_nat | ci_low | ci_high | min_nat | radius | overlap |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.662 | 0.589 | 0.735 | 0.589 | 3.600 | 0.644 |
| 0.01 | 0.674 | 0.620 | 0.756 | 0.620 | 2.933 | 0.643 |
| 0.02 | 0.599 | 0.418 | 0.698 | 0.418 | 3.000 | 0.640 |
| 0.04 | 0.525 | 0.478 | 0.614 | 0.478 | 3.400 | 0.635 |

### macro_stable-linjen `(0.02, 0.05, 0.02, 0.00, p_del)`

| p_del | mean_nat | ci_low | ci_high | min_nat | radius | overlap |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.676 | 0.535 | 0.838 | 0.535 | 3.133 | 0.628 |
| 0.01 | 0.650 | 0.565 | 0.724 | 0.565 | 3.200 | 0.630 |
| 0.02 | 0.616 | 0.560 | 0.662 | 0.560 | 3.333 | 0.639 |
| 0.04 | 0.533 | 0.374 | 0.651 | 0.374 | 3.267 | 0.643 |

## Tolkning

Det v0.8b viser er ikke at vi allerede har 'funnet fysikken'. Det viser noe mer beskjedent og metodisk viktigere: når testene blir strengere, krymper kandidatrommet på en disiplinert måte i stedet for å kollapse helt. Det er et godt tegn i en tidlig forskningskodebase.

Samtidig må man være ærlig: denne robustheten er fortsatt vist i en lokal kandidatregion og på relativt små til moderate grafstørrelser. Neste terskel er derfor å teste samme kandidatbånd på enda bredere naturlige ensembler og større skala, og å legge på eksplisitte usikkerhetsmål for selve kausalfronten.

## Filer

- run-level data: `v08b_natural_ensemble_runs.csv`
- ensemble-aggregate data: `v08b_natural_ensemble_aggregate.csv`
- overall candidate robustness data: `v08b_candidate_robustness.csv`
