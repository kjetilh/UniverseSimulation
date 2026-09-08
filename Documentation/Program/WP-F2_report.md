# WP-F2 rapport

Forsøk 2 følger amendment 1. Forsøk 1 er bevart separat i sin helhet.

Original frys SHA-256: `8b220334d2fbe55054d92c215fec608f378fd8ec2a9ddcbf3e6e54cc09990c42`.
Forsøk 2 frys SHA-256: `bb2805971fe744433353d61cb9577cddb170e3c450436ee15f6e688ab4065896`.

Metode: τ = 0,25·2^(k/4) til T/2; hendelser ved t≥T/2. Begge helninger bruker median V≥8 og τ≤T/4, minst seks punkter. γ bruker middelavstand; R90 og R90-γ rapporteres diagnostisk. KI er eksakt bootstrap over 256 trekk av fire historier. Udefinerte historier beholdes. Alle v7/v16-kilder og den opprinnelige laben er uendret. Separat wrapper erstatter bare M-seed-lese-/skrivesettet; M-dynamikken bruker den opprinnelige MarkAdapter med seed-policy mark. Ingen R-dynamikk kjøres.

## Forsøk 2 — R

|orden|underlag|n|α [95% KI]|γ middel [95% KI]|γ R90|minste fit-punkter α/γ|
|---|---|---|---|---|---|---|
|kernel|ring|4|1.621158 [1.377219, 1.868694]|0.331278 [0.280660, 0.392217]|0.353052|7/7|
|kernel|lat2|4|2.053882 [1.882598, 2.324796]|0.460400 [0.427132, 0.464781]|0.397631|6/6|
|kernel|lat3|4|2.755761 [2.667896, 2.792386]|0.455726 [0.452883, 0.467821]|0.338829|6/6|
|kernel|rrg|4|1.756612 [1.738640, 1.810818]|0.629536 [0.576845, 0.637790]|0.388132|6/6|
|legacy|ring|4|1.162586 [1.085637, 1.285781]|0.364755 [0.350275, 0.395276]|0.414473|6/6|
|legacy|lat2|4|nan [nan, nan]|nan [nan, nan]|nan|5/5|
|legacy|lat3|4|nan [nan, nan]|nan [nan, nan]|nan|3/3|
|legacy|rrg|4|nan [nan, nan]|nan [nan, nan]|nan|5/5|

Alle kurver, parantall, avstandssummer, WP-F0-observabler, drift og tverrbindinger er lagret i forsøk 2-CSV-ene.

## Forsøk 2 — M

|orden|underlag|n|α [95% KI]|γ middel [95% KI]|γ R90|minste fit-punkter α/γ|
|---|---|---|---|---|---|---|
|kernel|ring|4|1.667715 [1.572883, 1.945987]|0.368336 [0.320182, 0.415745]|0.373417|7/7|
|kernel|lat2|2|2.198334 [2.108913, 2.287754]|0.531591 [0.508870, 0.554312]|0.524275|7/7|
|legacy|ring|4|1.190327 [1.148943, 1.338890]|0.411130 [0.377005, 0.428754]|0.444118|6/6|
|legacy|lat2|2|nan [nan, nan]|nan [nan, nan]|nan|5/5|

Alle kurver, parantall, avstandssummer, WP-F0-observabler, drift og tverrbindinger er lagret i forsøk 2-CSV-ene.

## Forsøk 1 — R (bevart)

Full original rapport: [WP-F2_attempt1_report.md](WP-F2_attempt1_report.md). Tallene under bruker det gamle gridet og γ på R90.

|orden|underlag|α|γ R90|
|---|---|---|---|
|kernel|ring|1.701186|0.305889|
|kernel|lat2|nan|0.350591|
|kernel|lat3|nan|0.412062|
|kernel|rrg|nan|0.500000|
|legacy|ring|1.152003|0.258496|
|legacy|lat2|nan|0.361441|
|legacy|lat3|nan|0.438082|
|legacy|rrg|nan|0.435168|

## Uendrede porter / G4

Gatene evalueres etter R og M, i bestilt rekkefølge.

## Status og avslutning

Målinger og integrasjon har separate statuser. Commit/push, offentlig arkiv, live-revisjon, RAG-sync og autentisert ferskhets-/sitasjonskontroll er ikke bekreftet. Ved faktisk .git-blokkering gjelder amendmentets stoppregel; integratoren committer. Uavhengig G1-kvittering gjenstår. Ingen fysikkpåstand.
