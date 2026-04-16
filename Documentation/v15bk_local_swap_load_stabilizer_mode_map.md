# Relasjonell universgraf v0.15bk: local_swap load-stabilizer mode map

## Formål

Denne runden samler de beste lokale last- og stabiliseringsaksene i ett lite moduskart for `p1`, `p2` og `p3`.

## Mode map

| placement | ball2 load | full stabilizer | load delta | stabilizer delta | mode |
| --- | --- | --- | --- | --- | --- |
| 1 | 37.000 | 2.455 | 2.000 | 0.408 | buffered_heavy_load |
| 2 | 42.000 | 1.743 | 7.000 | -0.305 | rare_load_risk |
| 3 | 26.000 | 1.944 | -9.000 | -0.103 | low_load_diffuse |

## Operativ lesning

- `load_stabilizer_mode_status`: `load_stabilizer_mode_map_supported` fordi p1, p2 og p3 fyller tre ulike lokale modi: tung last med buffer, tung last uten nok buffer, og lavere last med diffus retur.
- `next_step`: `explain_risk_side_only` fordi Neste steg bør gå på risiko-siden av kartet, ikke åpne en bredere scan.

## Tolkning

- Dette er fortsatt en ren synteserunde på eksisterende data, ikke en ny simulering.
- Les dette som et lite lokalt moduskart for growth_seed 202, ikke som en global law for `local_swap`.
