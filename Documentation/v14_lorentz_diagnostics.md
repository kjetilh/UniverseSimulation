# Relasjonell universgraf v0.14: smal Lorentz-diagnostikk med artefaktkontroll

## Formål

Denne runden prøver ikke å bevise Lorentz-likhet. Den tester en smalere og mer operasjonell del av spørsmålet: om skadefronten har omtrent samme effektive fart for ulike lokale perturbasjoner når vi bruker de samme basegrafene, de samme seedene og en eksplisitt fallback-kontroll.

## Hva som holdes fast

- Samme dype, size-separerte startensembler brukes på tvers av alle perturbasjonstyper.
- Samme basegraf og samme run-seed brukes når vi sammenlikner perturbasjoner.
- Den aktive frontier-kandidaten `band_zero_del` er ankerregime.
- `band_pdel_0005` er en nær kontroll, ikke en ny frontier-scan.
- Vi logger faktisk perturbasjonstype etter fallback, slik at vi ikke antar at ønsket inngrep faktisk ble brukt.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |
| 192 | 192.0 | 192.0 | 192.0 | 1 |
| 256 | 256.0 | 256.0 | 256.0 | 1 |

## Perturbasjon og artefaktkontroll

| regime | requested | fallback_rate | support_size | fit_speed q10-q90 | artifact_flag |
| --- | --- | --- | --- | --- | --- |
| band_pdel_0005 | add_chord | 0.000 | 3.0-3.0 | 0.086-0.346 | clean_enough |
| band_pdel_0005 | local_swap | 0.000 | 3.0-3.0 | 0.135-0.348 | clean_enough |
| band_pdel_0005 | token_shift | 0.000 | 2.0-2.0 | 0.187-0.315 | clean_enough |
| band_zero_del | add_chord | 0.000 | 3.0-3.0 | -0.006-0.394 | clean_enough |
| band_zero_del | local_swap | 0.000 | 3.0-3.0 | 0.119-0.351 | clean_enough |
| band_zero_del | token_shift | 0.000 | 2.0-2.0 | 0.163-0.323 | clean_enough |

## Aggregert frontbilde

| regime | requested | n | strict | mean fit_speed | mean hit t(r=2) | mean hit t(r=3) | mean drop rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| band_pdel_0005 | add_chord | 16 | 16 | 0.225 | 11.546 | 14.175 | 0.113 |
| band_pdel_0005 | local_swap | 16 | 16 | 0.252 | 11.074 | 16.171 | 0.094 |
| band_pdel_0005 | token_shift | 16 | 16 | 0.255 | 8.426 | 10.057 | 0.125 |
| band_zero_del | add_chord | 16 | 16 | 0.207 | 13.649 | 14.025 | 0.163 |
| band_zero_del | local_swap | 16 | 16 | 0.250 | 9.332 | 13.935 | 0.113 |
| band_zero_del | token_shift | 16 | 16 | 0.237 | 8.449 | 10.607 | 0.100 |

## Matchede perturbasjonssammenlikninger

| regime | pair | scope | strict_fraction | rel speed gap | rel hit gap r2 | support gap |
| --- | --- | --- | --- | --- | --- | --- |
| band_pdel_0005 | add_chord__vs__token_shift | diagnostic | 1.000 | 0.467 | 0.506 | 1.0 |
| band_pdel_0005 | local_swap__vs__add_chord | primary_structural | 1.000 | 0.559 | 0.243 | 0.0 |
| band_pdel_0005 | local_swap__vs__token_shift | diagnostic | 1.000 | 0.352 | 0.462 | 1.0 |
| band_zero_del | add_chord__vs__token_shift | diagnostic | 1.000 | 0.768 | 0.495 | 1.0 |
| band_zero_del | local_swap__vs__add_chord | primary_structural | 1.000 | 0.712 | 0.183 | 0.0 |
| band_zero_del | local_swap__vs__token_shift | diagnostic | 1.000 | 0.341 | 0.338 | 1.0 |

## Nær regimekontroll

| requested | delta fit_speed (control-anchor) | delta hit t(r=2) | delta fallback |
| --- | --- | --- | --- |
| local_swap | 0.002 | 1.742 | 0.000 |
| add_chord | 0.018 | -2.103 | 0.000 |
| token_shift | 0.018 | -0.023 | 0.000 |

## Operativ lesning

- `generator_size_separation`: `clean` fordi De dype startstørrelsene er fortsatt rent separert; frontmålingene ser ikke ut som en ren ensemblekollaps.
- `perturbation_artifact_control`: `clean_enough` fordi Fallback-raten er lav nok til at de primære sammenlikningene kan leses som lokale perturbasjoner.
- `lorentz_like_front_speed`: `mode_dependent_not_yet` fordi Frontmålingene varierer fortsatt for mye mellom perturbasjonstyper og/eller nærkontrollregimer til å kalle dette Lorentz-likt.
- `next_step`: `keep_local_and_narrow` fordi Neste steg bør fortsatt være smalt: enten dypere matched perturbation-runder eller en egen isotropi-diagnostikk, ikke bred oppskalering.

## Viktig avgrensning

- Denne runden tester ikke isotropi i flere retninger på samme basegraf.
- Den tester heller ikke IR-dispersjon eller mikroframe-hiding direkte.
- Derfor kan et positivt resultat her bare være en lokal støtte for videre Lorentz-diagnostikk, ikke en full bekreftelse.
