# Relasjonell universgraf v0.15z: p0-vs-p1 case trigger explainer

## Formål

Denne runden kjører ingen nye simuleringer. Den bruker `v15w` og `v15y` til å teste om de tre utvalgte p0-vs-p1-case-seedene kan forklares av et lite sett onset-triggere.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Case trigger rows

| seed | case | trigger | exact gap | first gap | first comp gap | first boundary gap | first radius gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 151 | p1_clean_case | p1_compact_radius_trigger | 0.101 | -40.0 | 0.000 | 0.051 | -2.000 |
| 239 | tradeoff_case | fragmented_fast_tradeoff_trigger | -0.147 | -16.0 | 1.000 | 0.067 | 3.000 |
| 271 | p0_clean_case | p0_calm_singleton_trigger | -0.240 | 24.0 | 1.000 | 0.122 | -2.000 |

## Trigger aggregate

| trigger | n | rate | exact gap | first gap | first comp gap | first boundary gap |
| --- | --- | --- | --- | --- | --- | --- |
| fragmented_fast_tradeoff_trigger | 1 | 0.333 | -0.147 | -16.0 | 1.000 | 0.067 |
| p0_calm_singleton_trigger | 1 | 0.333 | -0.240 | 24.0 | 1.000 | 0.122 |
| p1_compact_radius_trigger | 1 | 0.333 | 0.101 | -40.0 | 0.000 | 0.051 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert og alle p0/p1-runene matcher ønsket add_chord-perturbasjon.
- `support_bias`: `p1_denser_support__p0_wider_expansion` fordi P1 sitter i litt tettere lokal støtte, mens p0 har litt større relativ videre ekspansjon. Dette er bakgrunnsbias, ikke hele forklaringen.
- `trigger_snapshot`: `p1_compact=1;tradeoff=1;p0_calm=1;mixed=0` fordi Dette oppsummerer hvordan de tre case-seedene brytes ned i onset-trigger-typer.
- `case_trigger_status`: `three_local_triggers_supported` fordi De tre utvalgte case-seedene kan forklares av tre ulike onset-triggere: kompakt p1-lock, fragmentert tradeoff og rolig p0-singleton-lock.
- `next_step`: `targeted_trigger_holdout` fordi Neste steg bør teste om disse triggerne holder på noen få nærliggende holdout-seeds, ikke åpne en ny bred scan.

## Tolkning

- `p1` har fortsatt en svak statisk støttefordel, men `v15z` viser at denne fordelen bare blir til en ren gevinst i noen seeds.
- `151` ser ut som et kompakt `p1`-lock: samme komponenttall som `p0`, men mindre radius og mindre skadesett gir tidligere og sterkere retur.
- `239` er fortsatt det reneste tradeoff-caset: `p1` kommer tidligere, men betaler for det med fragmentering og høyere boundary-cost.
- `271` ser ut som et rolig `p0`-singleton-caset: `p1` starter mer splittet, mens `p0` låser rent og vinner på full horisont.
- Les dette som lokal case-forklaring, ikke som en generell defect-lov.
