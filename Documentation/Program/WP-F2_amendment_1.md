# WP-F2 tillegg 1 — 7. september 2026 (forsøk 2)

Gjelder `Documentation/Program/WP-F2_influence_order_calibration.md`. Skrevet av Claude
(spec-forfatter) etter at forsøk 1 (commit `490ed34`, modus R, 16 historier) viste at
spesifikasjonen ikke var evaluerbar. Tersklene (rekkefølge, disjunkte KI, γ-spenn ≤ 0,10)
er **uendret**. Det som endres er målegrid og én uavklart regel. Ledgeren teller dette som
forsøk 2 på samme fingeravtrykk (G2); grunnen står her så den ikke kan omskrives.

## Feil 1 i spec-en: τ-grid i Gillespie-tid

Spec-en sa τ ∈ {1, 2, 4, …, T/4} «i tidsenheter» uten å sjekke T. Målt T for 8 192
hendelser er 44–98 tidsenheter, så gridet ga 4–5 punkter, og V ≥ 8 bare ved 1–2 av dem.
α ble derfor udefinert i 5/16 kernel-historier og tilpasset på to punkter i resten.
Det er en spesifikasjonsfeil, ikke en målefeil. Kurvene (f.eks. lat2 kernel: V = 1, 2, 5,
14, 56 ved τ = 1…16) viser at signalet finnes; oppløsningen manglet.

**Rettelse (frosset her, før ny analyse):**
- τ-grid geometrisk med faktor 2^{1/4} fra τ = 0,25 til τ = T/2.
- Hendelsesutvalg for V og R: alle e med t_e ≥ T/2, som før.
- α tilpasses over punktene med median V ≥ 8 **og** τ ≤ T/4. Krav: ≥ 6 punkter, ellers
  «ikke evaluerbar» for den historien.
- R(τ): rapporter både R90 (som før) og **middelavstand** over par; γ tilpasses på
  middelavstanden, fordi R90 i heltalls hopp gir trappetrinn. Samme punktkrav.
- Bootstrap som før: over historier (256 trekk av fire), ikke hendelser.

Ingen ny dynamikk for modus R: **reanalyser de 16 lagrede hendelsesloggene**
(`WP-F2_R_*_events.csv`, `parents`-kolonnen) og øyeblikksgrafene. Behold forsøk 1-tallene
i rapporten under egen overskrift; skriv forsøk 2-tallene ved siden av.

## Feil 2 i spec-en: `seed` i modus M

Spec-en nevnte bare `delete`/`triad`/`swap` som mark-erstatning, men `seed` legger til
node og kant og har positiv lokal rate (5,0·10⁻⁴). Avgjørelse (spec-forfatterens, ikke
Kjetils): **i modus M utføres `seed` som `mark:host`** — ingen node, ingen kant. Lese-/
skrivesett: leser `token:t` (ved `seed_tid`) og `node:host`, skriver `mark:host`. Lagre
som `WP-F2_M_seed_resolution.json` med denne ordlyden og tidspunkt, uten å overskrive
`WP-F2_frozen.json`.

## Observasjon fra forsøk 1 som skal følges opp i forsøk 2, ikke tolkes nå

γ (på R90) lå på 0,26–0,44 for ring/lat2/lat3 og 0,50–0,62 for rrg. Under diffusivt ½
på endelige underlag er uventet; det kan være trappetrinnsartefakt fra heltalls-R90, eller
reelt (tokens som fanges i nylig redigerte områder). Middelavstand-γ i forsøk 2 avgjør
hvilket. Ikke juster noe på grunnlag av dette.

## Rekkefølge for forsøk 2

1. Reanalyser R (ingen ny dynamikk). Skriv `WP-F2_report.md` seksjon «Forsøk 2 — R».
2. Kjør M (16 historier, 8 192 steg, seed-regelen over) og analyser med samme grid.
3. Evaluer gatene per modus, uendrede terskler. G4-utfallene fra hovedspec-en gjelder.
4. Kjør WP-H som spesifisert.
5. Hjerteslag som før. Ved `.git`-blokkering: si det og stopp; integratoren committer.
