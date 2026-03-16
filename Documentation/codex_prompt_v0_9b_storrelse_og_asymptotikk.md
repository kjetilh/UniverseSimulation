# Codex-prompt: v0.9b størrelse, asymptotikk og større naturlige ensembler

Du arbeider i en kodebase for prosjektet `relational_universe_*`.

Mål:
1. utvid v0.9-analysen til større naturlige ensembler (for eksempel målskala 144 og 192 noder),
2. bevar samme metodiske struktur som i v0.9: naturlig vekst, delt basebibliotek per ensemble/seed, lokal swap-perturbasjon, maksimal lokal kobling,
3. legg til eksplisitt asymptotisk analyse av radius, overlap og quasi-score,
4. skill tydelig mellom rå endring i observabler og skalaekstrapolasjon.

Krav:
- bruk markdown-filer for dokumentasjon,
- skriv ny Python-kode i egen fil,
- gjenbruk eksisterende hjelpefunksjoner der det er naturlig,
- lag CSV-utdata både på run-nivå, group-nivå og candidate-nivå,
- beregn bootstrap-intervaller for skalahelninger,
- dokumenter antakelser og begrensninger.

Tekniske føringer:
- hold lokalitet eksplisitt,
- ikke innfør nye primitive relasjonstyper,
- ikke bytt ut scoring uten å dokumentere hvorfor,
- dersom du lager plots, bruk matplotlib og lagre dem til filer.

Lever:
- ny Python-fil,
- minst tre nye markdown-filer,
- README,
- kort oppsummering av funn og hva de innebærer.
