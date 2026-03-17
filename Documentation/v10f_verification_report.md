# v0.10f verifikasjon og regresjon

- base-nivåer: ok
- frontier-orden: ok
- anbefalingstekst uten band_small_triad som operativ front: ok

## Kritiske regresjoner

- hvis 48, 96, 192 og 256 ikke lenger er eksakt realiserte, faller v0.10f-frontieren metodisk sammen
- hvis `band_small_triad` igjen behandles som operativ frontkandidat, er v13-dommen brutt
- hvis raw winner og focused-score-winner ikke lenger skilles riktig, mister v0.10f sin viktigste frontier-innsikt
