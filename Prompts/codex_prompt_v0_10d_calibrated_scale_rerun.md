# Codex-prompt: kalibrert scale rerun og kandidatseleksjon

Bruk `relational_universe_v10d_calibrated_scale_collapse.py` som utgangspunkt.

## Mål
Utvid rerunden uten å miste metodisk disiplin.

## Krav
- Hold growth-regimet fast: `fast_balanced / deep`
- Bruk bare størrelser som er eksplisitt bekreftet som reelt separerte
- Rapporter realiserte initialstørrelser i alle tabeller
- Gi kandidatene samme event-budsjettregel
- Beregn:
  - mean composite
  - mean repair
  - mean causal
  - mean quasi
  - alpha_all
  - alpha_large
  - alpha_jump
  - linear_margin
- Lag bootstrap-intervaller der det er rimelig
- Marker tydelig hvis negative eller ekstreme eksponenter kommer tilbake

## Ikke gjør dette
- Ikke bland resultater fra ulike ensemble-regimer i samme kandidatdom
- Ikke tolk generatorartefakter som fysikk
- Ikke overselg svake forskjeller

## Leveranser
- oppdatert Python
- candidate summary CSV
- size profile CSV
- kort Markdown med endelig kandidatdom for runden
