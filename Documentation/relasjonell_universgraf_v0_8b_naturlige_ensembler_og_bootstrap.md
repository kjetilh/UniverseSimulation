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

- Beste kandidat etter **naturlig robusthet** hadde parametere `(r_birth, r_death, p_swap, p_triad, p_del)=(0.02, 0.00, 0.02, 0.00, 0.01)` med mean natural composite ≈ 0.718 og bootstrap-lower-bound ≈ 0.659.
- Nest beste kandidat lå svært nær: mean natural composite ≈ 0.680, lower-bound ≈ 0.656.
- Det lovende kandidatbåndet overlevde i hovedsak overgangen til større og mer naturlige starttilstander, men rangeringen ble strammere og mer selektiv.
- `p_del` oppførte seg ikke monotont overalt: små positive verdier var enkelte steder kompatible med høy score, men høyere `p_del` presset oftere opp radius eller trakk ned overlap.
- De største naturlige starttilstandene var nyttige fordi de skilte bedre mellom regimer som bare så bra ut på små sykler og regimer som faktisk beholdt struktur under mer moden initial geometri.

## Toppkandidater rangert etter bootstrap-lower-bound på naturlig composite

| r_birth | r_death | p_swap | p_triad | p_del | mean_nat | ci_low_nat | ci_high_nat | min_nat | sd_nat | radius | overlap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.02 | 0 | 0.02 | 0 | 0.01 | 0.718 | 0.659 | 0.787 | 0.659 | 0.053 | 3.333 | 0.582 |
| 0.02 | 0.02 | 0.02 | 0 | 0.01 | 0.680 | 0.656 | 0.713 | 0.656 | 0.025 | 3.733 | 0.556 |
| 0.02 | 0.02 | 0.02 | 0 | 0 | 0.686 | 0.610 | 0.768 | 0.610 | 0.065 | 4.133 | 0.548 |
| 0.02 | 0 | 0.02 | 0 | 0 | 0.687 | 0.603 | 0.809 | 0.603 | 0.088 | 4.000 | 0.562 |
| 0.02 | 0.05 | 0.02 | 0 | 0 | 0.659 | 0.590 | 0.718 | 0.590 | 0.077 | 3.867 | 0.526 |
| 0.02 | 0.02 | 0.02 | 0.02 | 0 | 0.650 | 0.582 | 0.747 | 0.582 | 0.070 | 3.467 | 0.583 |
| 0.02 | 0 | 0.02 | 0 | 0.02 | 0.720 | 0.558 | 0.843 | 0.558 | 0.120 | 3.467 | 0.617 |
| 0.02 | 0.05 | 0.02 | 0 | 0.01 | 0.634 | 0.552 | 0.709 | 0.552 | 0.064 | 4.000 | 0.540 |
| 0.08 | 0.02 | 0.02 | 0 | 0.01 | 0.636 | 0.551 | 0.766 | 0.551 | 0.093 | 4.000 | 0.570 |
| 0.02 | 0.05 | 0.02 | 0 | 0.02 | 0.586 | 0.544 | 0.669 | 0.544 | 0.059 | 4.267 | 0.543 |

## Oppsummering per ensemble

| ensemble | mean init nodes | mean init tokens | mean init beta1 | mean composite(best point) | best point |
| --- | --- | --- | --- | --- | --- |
| natural24 | 33.20 | 4.60 | 2.00 | 0.843 | (0.02,0.00,0.02,0.00,0.02) |
| natural48 | 53.00 | 13.20 | 9.60 | 0.787 | (0.02,0.00,0.02,0.00,0.01) |
| natural_jitter | 40.80 | 9.00 | 6.00 | 0.891 | (0.08,0.02,0.02,0.00,0.00) |
| toy_cycle8 | 8.00 | 4.00 | 1.00 | 0.827 | (0.02,0.05,0.02,0.00,0.02) |

## p_del-snitt for de viktigste basislinjene

### refined_winner-linjen `(0.08, 0.02, 0.02, 0.00, p_del)`

| p_del | mean_nat | ci_low | ci_high | min_nat | radius | overlap |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.684 | 0.519 | 0.891 | 0.519 | 4.133 | 0.548 |
| 0.01 | 0.636 | 0.551 | 0.766 | 0.551 | 4.000 | 0.570 |
| 0.02 | 0.438 | 0.311 | 0.572 | 0.283 | 5.000 | 0.526 |
| 0.04 | 0.514 | 0.482 | 0.552 | 0.482 | 4.200 | 0.602 |

### coarse_balanced-linjen `(0.02, 0.02, 0.02, 0.00, p_del)`

| p_del | mean_nat | ci_low | ci_high | min_nat | radius | overlap |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.686 | 0.610 | 0.768 | 0.610 | 4.133 | 0.548 |
| 0.01 | 0.680 | 0.656 | 0.713 | 0.656 | 3.733 | 0.556 |
| 0.02 | 0.581 | 0.398 | 0.706 | 0.398 | 4.133 | 0.560 |
| 0.04 | 0.415 | 0.314 | 0.500 | 0.314 | 4.667 | 0.523 |

### macro_stable-linjen `(0.02, 0.05, 0.02, 0.00, p_del)`

| p_del | mean_nat | ci_low | ci_high | min_nat | radius | overlap |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.659 | 0.590 | 0.718 | 0.590 | 3.867 | 0.526 |
| 0.01 | 0.634 | 0.552 | 0.709 | 0.552 | 4.000 | 0.540 |
| 0.02 | 0.586 | 0.544 | 0.669 | 0.544 | 4.267 | 0.543 |
| 0.04 | 0.479 | 0.349 | 0.657 | 0.349 | 4.200 | 0.539 |

## Tolkning

Det v0.8b viser er ikke at vi allerede har 'funnet fysikken'. Det viser noe mer beskjedent og metodisk viktigere: når testene blir strengere, krymper kandidatrommet på en disiplinert måte i stedet for å kollapse helt. Det er et godt tegn i en tidlig forskningskodebase.

Samtidig må man være ærlig: denne robustheten er fortsatt vist i en lokal kandidatregion og på relativt små til moderate grafstørrelser. Neste terskel er derfor å teste samme kandidatbånd på enda bredere naturlige ensembler og større skala, og å legge på eksplisitte usikkerhetsmål for selve kausalfronten.

## Filer

- run-level data: `Documentation/v08b_natural_ensemble_runs.csv`
- ensemble-aggregate data: `Documentation/v08b_natural_ensemble_aggregate.csv`
- overall candidate robustness data: `Documentation/v08b_candidate_robustness.csv`
