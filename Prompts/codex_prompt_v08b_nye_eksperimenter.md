# Codex-prompt: kjør nye eksperimenter i relasjonell universgraf

## Formål
Du skal bruke den aktive simulatorpakken i repoet til å kjøre nye eksperimenter, ikke rekonstruere prosjektet fra historiske notater.

## Hva modellen er
Modellen beskriver et "univers" som en stokastisk omskrevet graf:
- noder og kanter er den eneste primitive strukturen,
- lokale rewrite-hendelser endrer grafen,
- spacetime-lignende struktur skal eventuelt oppstå som makromønster, ikke bygges inn for hånd.

## Viktigste filer
- `relational_universe_local_max_coupling_lab.py`: dynamisk kjerne for lokalt maksimal kobling og skade-/repair-diagnostikk.
- `relational_universe_v08_phase_atlas.py`: faseatlas og scorefamiliene `repair`, `causal`, `quasi`, `geom`.
- `relational_universe_v08b_natural_ensemble_robustness.py`: v0.8b-scan med naturlige startensembler og bootstrap-robusthet.
- `relational_universe_v09_scale_natural_ensembles.py`: v0.9-skalaanalyse for større naturlige ensembler og burn-in-regimer.
- `Documentation/relasjonell_universgraf_v0_8b_naturlige_ensembler_og_bootstrap.md`: teknisk status for v0.8b.
- `Documentation/relasjonell_universgraf_v0_9_skala_og_naturlige_ensembler.md`: teknisk status for v0.9.

## Hva scorefamiliene betyr i praksis
- `repair`: hvor ofte to nesten like grener fortsatt velger kompatible lokale hendelser og bevarer lokal struktur.
- `causal`: hvor begrenset skadefronten forblir i radius, hastighet og edge-differanse.
- `quasi`: hvor lite quasi-invariante størrelser divergerer mellom grenene.
- `geom`: hvor lite geometri-proksier som spektralradius, clustering og dim-proxy driver fra hverandre.

## Naturlige startensembler
Med "naturlige startensembler" menes ikke hånddesignede grafer, men grafer som først er vokst frem av modellens egen enkeltdynamikk og så brukt som starttilstander i koblede run.

## Arbeidsregler
- Bruk filer på disk som ground truth.
- Skille alltid mellom rå målinger og tolkning.
- Ikke kall noe en fase eller bevaringslov bare fordi én score er høy.
- Hvis du lager nye scorer, dokumenter formelen eksplisitt.
- Hold dokumentasjon i Markdown og skriv CSV-er til `Documentation/`.

## Første steg
1. Les siste relevante statusnotat.
2. Les den aktive Python-filen du skal bygge videre på.
3. Kjør minst én smoke test før større batcher.
4. Rapporter alltid hvilke parametere og hvilke outputfiler som ble brukt.
