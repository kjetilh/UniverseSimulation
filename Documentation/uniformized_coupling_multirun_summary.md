# Uniformized coupling – multikjøringsoppsummering

## Oppsett
- 20 seeds per regime
- 5000 steg per kjøring
- perturbasjon: `local_swap`
- initialsyklus: 8
- initialt token-antall: 4

## Regime A: token-open moderate
Parametre:
- `p_triad = 0.0`
- `p_del = 0.0`
- `p_swap = 0.08`
- `r_birth = 0.01`
- `r_death = 0.009`
- `birth_degree_bias = 0.75`
- `death_inverse_degree_scale = 1.0`

Resultater:
- mean final radius: 3.650
- sd final radius: 1.182
- mean max radius: 5.200
- sd max radius: 1.105
- mean fit-speed: 0.006345
- mean both-accept fraction: 0.873
- mean one-sided fraction: 0.127

Kommentar:
Dette regimet ser ut til å være et godt kandidatregime for videre spacetime-testing:
det er åpent nok til at v0.6 faktisk betyr noe, men ikke så åpent at geometri drukner i scrambling.

## Regime B: full-open moderate
Parametre:
- `p_triad = 0.05`
- `p_del = 0.03`
- `p_swap = 0.08`
- `r_birth = 0.01`
- `r_death = 0.009`
- `birth_degree_bias = 0.75`
- `death_inverse_degree_scale = 1.0`

Resultater:
- mean final radius: 0.550
- sd final radius: 1.146
- mean max radius: 3.150
- sd max radius: 0.933
- mean fit-speed: 0.006497
- mean both-accept fraction: 0.585
- mean one-sided fraction: 0.415

Kommentar:
Dette regimet er mer genuint åpent, men ser mindre lovende ut som første kandidat for pen causal-cone-geometri.
Divergensen ser oftere ut til å gå inn i token- og feature-drift enn i stor radiusvekst.

## Foreløpig dom
Hvis målet er å finne et regime der modellen både er levende og geometrisk lesbar, peker dataene foreløpig mot **moderat åpenhet** snarere enn maksimal åpenhet.
