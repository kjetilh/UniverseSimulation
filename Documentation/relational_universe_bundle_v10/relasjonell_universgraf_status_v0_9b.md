# Status v0.9b

## Kort status

v0.9b er fullført som en asymptotisk kontrolltest over v0.9-kandidatene.

Dette steget gjorde tre ting:

1. utvidet størrelsesvinduet opp til naturlige ensembler rundt 192-nivå,
2. innførte eksplisitte finite-size-diagnostikker (`alpha_large`, `alpha_jump`, `linear_margin`),
3. kjørte lokal ekstrarefinering på de mest interessante kandidatene.

## Viktigste konklusjon

`band_best` er nå den mest interessante kandidaten i prosjektet.

Ikke fordi den vinner på ren rå composite alene, men fordi den:

- har lav `alpha_large`,
- har svært liten eller negativ `alpha_jump`,
- og får positiv `linear_margin`.

Dette er et langt bedre asymptotisk signal enn det vi ser for `balanced_pdel`, som gjorde det godt i v0.9, men faller tydelig tilbake når finite-size-risiko måles direkte.

## Hva som ble falsifisert eller svekket

- Hypotesen om at v0.9-vinneren automatisk også er asymptotisk best: **svekket**
- Hypotesen om at lave all-skala-eksponenter alene er nok: **falsifisert som tilstrekkelig kriterium**
- Hypotesen om at kandidatbåndet fortsatt er interessant etter strengere test: **styrket**

## Hva som nå er den operative arbeidsantagelsen

Det mest lovende arbeidsregimet ser foreløpig ut til å være nær:

- `r_birth ≈ 0.02`
- `r_death ≈ 0.00`
- `p_swap ≈ 0.02`
- `p_triad ≈ 0.00`
- `p_del ≈ 0.01`

Det er altså et svakt åpent, topologisk forholdsvis konservativt regime.

## Neste steg

v0.10 bør:

1. løfte skalaen videre,
2. gi toppkandidatene flere growth seeds,
3. prøve enkel skaleringskollaps,
4. teste om `band_best` fortsatt holder når ensemblevariansen økes ytterligere.
