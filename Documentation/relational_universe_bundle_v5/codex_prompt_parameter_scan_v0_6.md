# Codex-prompt: parameter-scan og fasekart for v0.6

Du skal bruke `relational_universe_uniformized_scan.py` og `relational_universe_uniformized_coupling_lab.py` til å kartlegge parameterrommet.

## Formål
Finn regimer som samtidig gir:
- høy both-accept fraction
- moderat one-sided fraction
- ikke-triviell radiusutbredelse
- kontrollert drift i `delta_tokens` og `delta_beta1`

## Gjør dette
1. Definer et eksplisitt parametergrid over:
   - `r_birth`
   - `r_death`
   - `p_triad`
   - `p_del`
   - `p_swap`
   - `birth_degree_bias`
   - `death_inverse_degree_scale`

2. Kjør mange seeds per punkt.
3. Lag:
   - rå CSV
   - aggregert CSV
   - Markdown-rapport
   - minst ett plot som rangerer regimer etter
     - `max_radius_control_mean`
     - `both_accept_frac_mean`
     - `one_sided_frac_mean`

4. Gi en eksplisitt kandidatliste over de mest lovende regimene for videre spacetime- og energitester.

## Viktig
- Ikke tolk høye radiusverdier alene som “bedre”.
- Høyt kausal-signal uten coupling-kvalitet er metodisk svakt.
- Høy åpenhet kan gi scrambling fremfor lesbar geometri.

## Leveranse
En strukturert fasekart-rapport i Markdown med tydelige anbefalinger for neste kjøringer.
