# Codex-prompt: v0.8 fasekart over repair, kausalitet, energi og geometri

Du skal bygge neste forskningssteg på toppen av v0.7. Les først:

- `relasjonell_universgraf_v0_7_lokal_maksimal_kobling_og_repair.md`
- `v0_7_faseprobe_kandidater.md`
- `relational_universe_v07_phase_probe.py`

## Mål
Lag et ekte v0.8-fasekart som kobler sammen:
1. repair / meeting,
2. radiusutbredelse / front-hastighet,
3. quasi-invariants / makrodrift,
4. geometri-proksier.

## Krav
- Bruk maksimal lokal kobling som standard.
- Ikke bryt CLI uten god grunn.
- Alle rapporter skal være i Markdown.
- Produser én CSV med én rad per parameterpunkt.

## Parameterrom
Start med et fokusert område rundt de mest lovende punktene:
- `r_birth in {0.02, 0.05, 0.08}`
- `r_death in {0.00, 0.02, 0.05}`
- `p_swap in {0.02, 0.04, 0.08}`
- `p_triad in {0.00, 0.01, 0.03}`
- `p_del in {0.00, 0.01}`

## Metrikker
For hvert punkt, estimer:
- `meeting_fraction`
- `mean_first_meeting_time_conditional`
- `mean_total_unequal_time`
- `mean_final_radius_control`
- `fit_speed_control`
- `mean_avg_local_overlap`
- `mean_same_descriptor_rate`
- `drift_beta1`
- `drift_tokens`
- `mean_spectral_radius`
- `mean_clustering`
- `mean_dim_proxy`

## Analyse
1. Ranger punktene etter:
   - høy repair,
   - lav drift,
   - lav/moderat radius,
   - stabil geometri.
2. Finn om det finnes et “sweet spot”.
3. Skill tydelig mellom:
   - repair-vennlig,
   - cone-vennlig,
   - invariant-vennlig,
   - og geometri-vennlig.

## Leveranser
- ny Python-scan-kode,
- Markdown-hovedrapport,
- kort statusnotat,
- egen lay-summary i Markdown.