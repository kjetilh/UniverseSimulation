# Relasjonell universgraf status v0.12n

## Kort status

Prosjektet er fortsatt i struktur- og arbeidsflytfasen.
`band_zero_del` er fortsatt frontier-standarden fra `v11e`.

`v12n` er den strengeste lokale valideringen så langt av den beste adaptive utfordreren fra `v12m`.

## Live operative konklusjoner

### Frontier

- Live frontier-standard: `band_zero_del`

### Arbeidsflyt / adaptiv oppfølging

Det nye bildet etter `v12n` er:

- `full_followup` holder seg som referanse
- `probe3_top_half` er fortsatt en tydelig rask utfordrer
- men den er ikke robust nok til å erstatte referansen

Det viktige er ikke bare at `probe3_top_half` er raskere.
Det viktige er at den i denne runden også faller litt tilbake på kvalitet:

- `best_hit ~= 0.650`
- `recall ~= 0.650`
- `pairwise ~= 0.590`

mot referansen:

- `best_hit ~= 0.669`
- `recall ~= 0.669`
- `pairwise ~= 0.644`

## Hva som ikke hjalp

`v12n` testet også to små lokale varianter:

- `probe3_top_half_screen_tiebreak`
- `probe3_guarded_half`

Ingen av dem forbedret resultatet meningsfullt.

Det betyr at:

- enkel tie-break på screening-score ikke er nok
- enkel guarded-forlengelse heller ikke er nok

## Riktig lesning

`v12m` viste et mer optimistisk bilde av `probe3_top_half`.
`v12n` viser at dette signalet ikke er stabilt nok ennå.

Den repo-lojale dommen nå er derfor:

- `probe3_top_half` er fortsatt verdt å ta på alvor
- men det er ikke riktig å oppgradere den til ny standard
- `full_followup` bør fortsatt brukes som operativ referanse

## Neste naturlige steg

Det riktige neste steget er ikke flere nesten-like lokale policyvarianter.

Hvis vi skal videre på dette sporet, bør det være ett av disse:

- en smartere tidlig beslutningsstatistikk for hvilke screenede baser som skal forlenges
- eller et større valideringssett som kan avgjøre om `probe3_top_half`-signalet er for svakt eller bare for lite målt

Hvis vi ikke vil investere i det nå, er det også rimelig å midlertidig fryse arbeidsflytsporet og gå tilbake til geometri-/invariantspørsmål.
