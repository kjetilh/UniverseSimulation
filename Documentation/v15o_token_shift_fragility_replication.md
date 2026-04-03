# Relasjonell universgraf v0.15o: token_shift fragility replication

## Formål

Denne runden tester om de skjøre `token_shift`-plasseringene fra v15n fortsatt er skjørere enn nærliggende levende kontroller på samme base når vi rerunner dem med flere seeds.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |

## Matchede profiler

| pair | fragile placement | control placement | distance |
| --- | --- | --- | --- |
| t48_g101_p3_vs_p4 | 3 | 4 | 4.000 |
| t48_g202_p0_vs_p3 | 0 | 3 | 8.000 |
| t96_g202_p5_vs_p4 | 5 | 4 | 8.000 |

## Pair diagnosis

| pair | token fragile ext | token control ext | token gap | add fragile ext | add control ext | status |
| --- | --- | --- | --- | --- | --- | --- |
| t48_g101_p3_vs_p4 | 0.250 | 0.000 | 0.250 | 0.000 | 0.000 | fragile_profile_replicates |
| t48_g202_p0_vs_p3 | 0.250 | 0.125 | 0.125 | 0.000 | 0.000 | weak_fragile_profile |
| t96_g202_p5_vs_p4 | 0.250 | 0.125 | 0.125 | 0.000 | 0.000 | weak_fragile_profile |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er fortsatt rent separert og alle replikerte perturbasjoner matcher ønsket type.
- `fragility_replication`: `partially_replicated` fordi Skjørhetsprofilene reproduserer noe gap mot kontrollene, men ikke rent nok til å kalles stabile lokale profiler ennå.
- `next_step`: `refine_profiles` fordi Neste steg bør være en enda smalere profilrunde rundt de beste token_shift-kandidatene med mer lokalt matchede kontroller.

## Tolkning

- Dette er en smal replikeringsrunde av lokale profiler, ikke en ny bred defect-scan.
- Les fortsatt dette som defect-fragility, ikke som partikkelbevis eller generell geometri.
