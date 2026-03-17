# v0.10f regresjonstester og hvorfor de finnes

- `base_levels_exact`: beskytter mot at frontier-runden mister de eksakt separerte startnivåene 48, 96, 192 og 256.
- `frontier_order`: beskytter mot at raw winner og focused-score-vinner blandes sammen eller at `band_small_triad` feilaktig glir tilbake inn i finalefronten.
- `recommendation_excludes_band_small_triad`: beskytter den operative tolkningen mot å omtale `band_small_triad` som aktiv frontkandidat etter v13.
