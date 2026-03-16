# v0.7 lokal maksimal kobling – verifikasjonsnotat

## Hva som er eksakt i implementasjonen

- Familywise uniformization og Bernoulli-aksept per familie er eksakte konstruksjoner gitt de aktuelle familie-ratene.
- Når to grener er identiske og bruker `maximal`, er koblingen absorberende fordi familie-rater, lokale kjerner og ID-allokering er identiske.
- `local_overlap_prob` er den eksakte overlap-massen `sum_i min(p_i, q_i)` for de to endelige lokale kjernene.

## Hva som er numerisk verifisert her

- Maksimal kernel-normaliseringsfeil over sjekkede kjerner: `0`
- Maksimal feil mellom empirisk same-descriptor-rate og teoretisk overlap-masse: `0.016`
- Maksimal frekvensfeil for familywise potensialfamilier: `0.00815`
- Maksimal TV-avstand mellom empiriske descriptor-marginaler og lokale kjerner: `0.0289`
- Absorpsjonstest under maksimal kobling: `PASS` over 4 seeds x 400 steg

## Hva som fortsatt er heuristisk eller dynamisk

- `meeting_fraction`, `total_unequal_time` og `shared_token_fraction_final` er regimeavhengige dynamiske mål, ikke algebraiske garantier.
- Høy lokal overlap betyr bare at den lokale koblingen er skarpere; det beviser ikke global kontraksjon av hele CTMC-en.

## Kernel-sanity

| pair | branch | family | support | kernel_sum | sum_error | empty|rate>0 |
| --- | --- | --- | --- | --- | --- | --- |
| initial_pair | control | seed | 4 | 1 | 0 | 0 |
| initial_pair | control | token | 16 | 1 | 0 | 0 |
| initial_pair | control | birth | 4 | 1 | 0 | 0 |
| initial_pair | control | death | 4 | 1 | 0 | 0 |
| initial_pair | perturbed | seed | 4 | 1 | 0 | 0 |
| initial_pair | perturbed | token | 18 | 1 | 0 | 0 |
| initial_pair | perturbed | birth | 4 | 1 | 0 | 0 |
| initial_pair | perturbed | death | 4 | 1 | 0 | 0 |
| evolved_pair | control | seed | 6 | 1 | 0 | 0 |
| evolved_pair | control | token | 30 | 1 | 0 | 0 |
| evolved_pair | control | birth | 6 | 1 | 0 | 0 |
| evolved_pair | control | death | 6 | 1 | 0 | 0 |
| evolved_pair | perturbed | seed | 5 | 1 | 0 | 0 |
| evolved_pair | perturbed | token | 27 | 1 | 0 | 0 |
| evolved_pair | perturbed | birth | 5 | 1 | 0 | 0 |
| evolved_pair | perturbed | death | 5 | 1 | 0 | 0 |

## Maksimal kobling og descriptor-marginaler

| pair | family | alpha | same_desc_emp | |emp-alpha| | tv_control | tv_perturbed |
| --- | --- | --- | --- | --- | --- | --- |
| initial_pair | seed | 1 | 1 | 0 | 0.0152 | 0.0152 |
| initial_pair | token | 0.87 | 0.872 | 0.002 | 0.024 | 0.0252 |
| initial_pair | birth | 1 | 1 | 0 | 0.006 | 0.006 |
| initial_pair | death | 1 | 1 | 0 | 0.0105 | 0.0105 |
| evolved_pair | seed | 0.833333 | 0.8445 | 0.0112 | 0.0137 | 0.0095 |
| evolved_pair | token | 0.277778 | 0.29375 | 0.016 | 0.0229 | 0.0289 |
| evolved_pair | birth | 0.74183 | 0.74725 | 0.00542 | 0.0118 | 0.00899 |
| evolved_pair | death | 0.685755 | 0.689 | 0.00324 | 0.00701 | 0.00253 |

## Familywise marginaltest

| family | observed_freq | expected_freq | |diff| | observed_count | expected_count |
| --- | --- | --- | --- | --- | --- |
| seed | 0.00166667 | 0.00108395 | 0.000583 | 2 | 1.301 |
| token | 0.91 | 0.901942 | 0.00806 | 1092 | 1082.330 |
| birth | 0.0816667 | 0.0821609 | 0.000494 | 98 | 98.593 |
| death | 0.00666667 | 0.0148133 | 0.00815 | 8 | 17.776 |

## Testpakken som prompten ba om

| mode | meeting_fraction | mean_overlap | same_descriptor_rate | mean_unequal_time | shared_token_fraction_final |
| --- | --- | --- | --- | --- | --- |
| rank | 0 | 0.0504299 | 0.0326923 | 41.4679 | 0.0641548 |
| maximal | 0 | 0.0819646 | 0.0792709 | 39.3436 | 0.215917 |

## Kommandoeksempler

```bash
python relational_universe_local_max_coupling_lab.py --mode verify --label v07_local_max_coupling --out-prefix Documentation/v07_local_max_coupling --steps 1200 --multirun-seeds 12
```

```bash
python relational_universe_local_max_coupling_lab.py --mode compare --label v07_local_max_coupling --out-prefix Documentation/v07_local_max_coupling --steps 1200 --multirun-seeds 12
```

_Per-seed compare CSV: `Documentation/v07_local_max_coupling_verification_multirun.csv`_
