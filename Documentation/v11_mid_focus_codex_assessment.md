# v11 Mid Focus Codex Assessment

Denne lokale runden var en mellomtung frontier-resolution rundt fem kandidater:

- `band_zero_del`
- `bridge_0025_0000`
- `bridge_0025_0000_swap025`
- `frontier_triad_only`
- `frontier_diag_mid`

Kjoringen brukte:

- targets `48,96,192,256`
- `growth_seeds=2`
- `run_seeds_broad=2`
- `run_seeds_final=3`
- `bootstrap_reps=60`

Resultatet flytter prosjektets operative tyngdepunkt bort fra `band_zero_del`.

## Viktigste funn

- I broad-runden var `bridge_0025_0000` tydelig ravinner med `mean_composite ~= 0.751`, `CI low ~= 0.695` og `top_prob = 1.0`.
- I samme broad-runde var `bridge_0025_0000_swap025` focused-vinner med `focused_score ~= 0.712`, men svakere ra dynamikk enn `bridge_0025_0000`.
- `band_zero_del` ble hengende bak begge bridge-kandidatene i denne runden.
- I finalen slo `bridge_0025_0000` bade `band_zero_del` og `bridge_0025_0000_swap025` pairwise med sannsynlighet `1.0`.

## Tolkning

Dette er et sterkere signal enn den minimale v0.11-smoken:

- `band_zero_del` ser ikke lenger ut som beste operative standardkandidat.
- Den relevante frontier-spenningen er na mellom en ra bridge-vinner og en focused/regularisert swap-variant.
- `bridge_0025_0000_swap025` er interessant som strukturkandidat, men ser i denne runden ut til a vinne mest pa focused-score, ikke pa ren dynamikk.

## Operativ dom

Bruk `bridge_0025_0000` som standardkandidat videre.

Hold `bridge_0025_0000_swap025` som focused-kontroll.

## Hva som bor gjores neste

Neste runde bor ikke ga tilbake til bred frontier-scan. Den bor ga smalere og dypere i bridge-korridoren:

- finere grid rundt `p_triad ~= 0.0025`
- liten `p_swap`-akse rundt `0.020-0.025`
- hold `p_del = 0` i hovedsporet
- bruk `band_zero_del` som kontroll, ikke som default-vinner

Poenget er na a avgjore om focused-fordelen til swap-varianten er robust fysikk eller bare en scoring-/regulariseringseffekt.
