# Relasjonell universgraf v0.12i: målt arbeidsflyt-tid for screening og oppfølging

## Formål

Denne runden erstatter den abstrakte skjermkostnaden i v12h med direkte lokal måling. Sporsmalet er ikke lenger bare hvilken policy som ser billig ut i en modell, men hvilken som faktisk gir en raskere arbeidsflyt pa denne maskinen og denne kodebanen.

## Metode

- Samme arbeidsregime som v12f-v12h: `band_zero_del`.
- Samme policyfamilie som aktiv arbeidslesning: `full_basis@0.50`, `spectral_only@0.50`, `spectral_plus_dim@0.667`, pluss `random_baseline@0.50` som diagnostisk kontroll.
- Screeningtiden maales som virkelig veggklokketid for score+seleksjon pa de samme stratified holdout-splitt som v12f brukte.
- Oppfolgingstiden maales som virkelig veggklokketid for en full dynamikk-bundle per valgt base, altsa alle run-seeds for den basen.
- Dette er fortsatt en arbeidsflyttest, ikke ny fysikk. Hvis en policy vinner her, betyr det at den ser ut til a gi en raskere praksis under dagens benchmarkoppsett.
- Screening-splitt: `60`. Timing-lokker per screeningpass: `300`.
- Oppfolgingstid kalibrert med `3` growth-baser per størrelse og `2` repeats per bundle.

## Målt oppfølgingstid per størrelse

| target | samples | mean_bundle_seconds | mean_seconds_per_run | mean_steps_per_run | q10_bundle | q90_bundle |
| --- | --- | --- | --- | --- | --- | --- |
| 48 | 6 | 0.5265 | 0.0877 | 240.0 | 0.4720 | 0.6232 |
| 96 | 6 | 1.6317 | 0.2719 | 480.0 | 1.5719 | 1.6752 |
| 192 | 6 | 5.2708 | 0.8785 | 800.0 | 4.1837 | 6.9104 |
| 256 | 6 | 5.9391 | 0.9899 | 800.0 | 4.5227 | 7.1424 |

## Målt pipeline-sammendrag

| rank | policy | budget | total_s | speedup_vs_ref | best_hit | recall | d_best_hit | d_recall | near_match | faster | faster_and_match | screen_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | full_basis | 0.500 | 40.1041 | 1.000 | 0.525 | 0.548 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 |
| 2 | spectral_only | 0.500 | 40.1041 | 1.000 | 0.542 | 0.540 | 0.017 | -0.008 | 0.467 | 1.000 | 0.467 | 0.000 |
| 3 | random_baseline | 0.500 | 40.1040 | 1.000 | 0.471 | 0.446 | -0.054 | -0.102 | 0.400 | 1.000 | 0.400 | 0.000 |
| 4 | spectral_plus_dim | 0.667 | 53.4721 | 0.750 | 0.679 | 0.692 | 0.154 | 0.144 | 0.833 | 0.000 | 0.000 | 0.000 |

## Operativ lesning

- Referansen `full_basis@0.50` bruker i snitt `40.1041` sekunder per split i denne lokale modellen.
- Selve screeningdelen er bare ca. `0.000129` sekunder for `full_basis@0.50`, mot `40.1040` sekunder i oppfolging. Det tilsvarer omtrent `3.2e-6` av totalen og forklarer hvorfor screeningdelen er praktisk neglisjerbar ved dagens størrelser.
- `spectral_only@0.50` er same-budget-kandidaten: `speedup_vs_ref=1.000`, `near_match=0.467` og `faster_and_match=0.467`.
- `spectral_plus_dim@0.667` er den dyrere kompakte utfordreren: `speedup_vs_ref=0.750`, `near_match=0.833` og `faster_and_match=0.000`.
- Dette skal leses som en praktisk arbeidsdom. Hvis de kompakte policyene ikke blir raskere her, er det et tegn pa at de forelopig gir en ryddigere beskrivelse mer enn en faktisk spart arbeidsflyt.
