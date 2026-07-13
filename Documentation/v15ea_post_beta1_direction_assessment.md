# UniverseSimulation v0.15ea: grundig retningsvurdering etter v15dz

Dato: 2026-07-12

## Kort konklusjon

Prosjektet boer ikke fortsette med flere observabelvarianter innen far-shell, placement eller beta1. Den riktige neste retningen er en ny fase, `v16`, som begynner med en billig og eksakt **regeladekvans-gate**:

> Formaliser hvert events read/write-stoette og test om alle deklarert uavhengige eventpar kommuterer opp til node-relabeling naar tilfeldige input og identitetsallokering holdes faste.

Dette er load-bearing for all videre tale om intrinsic causality, scheduler-uavhengighet, causal cones og coarse-grained spacetime. En stor simulasjonsrunde foer denne testen har lavere informasjonsverdi og hoeyere risiko for aa raffinere scheduler- eller observabelartefakter.

## Formaal og maal

`purposeRef`: `purpose://prompt.unknown`.

Root claim under vurdering:

`Den naavaerende modellklassen kan fortsatt gi en avgjoerende test av robust emergent geometri/lovstruktur uten mer observabeljakt.`

| goal | maal | status |
| --- | --- | --- |
| G1 repo-loyal diagnose | skill fakta, deduksjon og spekulasjon | satisfied |
| G2 konkurrerende retninger | vurder A-F med motargumenter og stoppruter | satisfied |
| G3 neste program | ett lite foerste steg med eksakte kriterier | satisfied |
| G4 Fabel 5 | faktisk ekstern respons, ikke alias-antakelse | blocked |

## Hva repoet faktisk har vist

### Positive, avgrensede fakta

- Transition-kjernen er node-relabel-equivariant i v15du.
- Uniform token-rooted add_chord reparerer constructorens distributionelle relabel-invarians i v15dv.
- Defekter kan interagere ikke-trivielt; dette er mer enn enkel superposisjon, men familiene er heterogene.
- `beta1=E-N+C` er en eksakt eventwise invariant i `band_zero_del` og add_chord oppretter en eksakt +1-sektor.

### Negative eller pensjonerte tolkninger

- Lorentz-likhet er fortsatt `not_yet`; placement-, mode- og anisotropiproblemet er ikke loest.
- Far-shell/damage-responsen feilet constructor x coupling-gaten i v15dw og er pensjonert som physics-facing observabel.
- beta1 er ikke universell: triad/delete bryter den kontrollert.
- v15dy og v15dz fant ingen robust global eller justert lokal dynamisk konsekvens av beta1-sektoren.
- Placement/family selectors transfererte ikke paa fresh bases.
- Modellen har ingen quantum state eller operasjonell entanglement-struktur. Stokastisk korrelasjon er ikke entanglement.

## Arkitekturdiagnose

Den viktigste nye deduksjonen er at flere av prosjektets founding-egenskaper ennaa ikke er veldefinerte objekter i modellen:

| krav | dagens status | konsekvens |
| --- | --- | --- |
| Relabel-uavhengighet | god for kernel og ny constructor | behold som hard constraint |
| Lokalitet | descriptors er lokale, men read/write-sett er ikke formalisert | finite propagation kan ikke bevises ennaa |
| Intrinsic causality | ekstern eventrekkefolge, ingen eksplisitt event-poset | damage-front er ikke en kausal struktur |
| Scheduler-uavhengighet | ukjent | observerte forloep kan vaere ordenssensitive |
| Reversibilitet/detailed balance | ikke i anchor; birth/seed mangler motsatt anchor-rate | tidsretning er bygd inn eller uavklart, ikke emergent |
| Topologisk dynamikk | beta1 er frosset av anchor-alfabetet | bevaring er algebraisk, ikke dynamisk emergens |
| Coarse-graining | ingen delt scale-map | target-sammenligninger er ikke RG-flow |

Dette beviser ikke at brede relasjonelle modeller ikke kan bygge universlik struktur. Det undergraver derimot paastanden om at enda en stor runde i dagens observabelstakk er neste riktige test.

## Raadgiverpanelet

Panelet var argumentstruktur, ikke avstemning.

### Fabel 5

Fabel 5 ble forsoekt via to faktiske ruter:

1. `claude -p --model claude-fable-5` svarte `401 Invalid authentication credentials`.
2. NanoGPT-panelet med modell-ID `anthropic/claude-fable-5` kunne ikke starte fordi `NANOGPT_API_KEY` ikke var satt.

Claude auth-status hevdet innlogging, men et reelt kall feilet; uten `ANTHROPIC_API_KEY` rapporterte CLI-en `Not logged in`. Derfor finnes ingen Fabel-respons i denne vurderingen. Panelspesifikasjonen ligger i `Documentation/v15ea_direction_panel_spec.json` og kan kjoeres etter auth-reparasjon.

### Remote raadgivere

Den teoretiske raadgiveren rangerte `A > C > B > F > E > D`: symmetry-first foer causal structure, deretter coarse-graining. Den foreslo en senere tre-skala kampanje, men bare etter matematisk regelavledning.

Evidence-adjudikatoren rangerte `A > F > C > B > D > E` og identifiserte disjoint-event commutation som minste avgjoerende gate. Den viktigste undercutten var:

> Relabel-equivariance av transition-kjernen impliserer ikke scheduler-robusthet, causal isotropy, finite propagation eller emergent geometry.

Den beregningsmetodiske raadgiveren rangerte ogsaa A/C foerst, men la til en skarp locality-kontroll: dagens `family_rates` aggregerer globale family clocks. Dette kan vaere en legitim Gillespie-representasjon av lokale klokker, men det maa vises ved faktorisering; det kan ikke antas fra at den valgte descriptoren er lokal. Raadgiveren foreslo current global clock som forventet fail-kontroll og en static census paa kanoniske grafer med `4-7` noder foer noen holdout.

Panelets robuste fellesdel er derfor ikke den store run-matrisen; det er at **A maa komme foer C, og C maa komme foer B**.

## Ekstern forskningskontekst

Eksterne analogier er ikke repo-evidens, men de skjerper metodevalget:

- Rideout og Sorkin avledet en familie av causal-set growth dynamics fra eksplisitte causality- og discrete-general-covariance-krav. Metodepoenget er at symmetri/kausalitet kan begrense reglene foer simulering, ikke bare scores etterpaa: <https://arxiv.org/abs/gr-qc/9904062>.
- Quantum Graphity viser hvorfor permutation symmetry og en graf-faseovergang er relevante ideer, men en senere numerisk analyse fant at originaldynamikken favoriserte frakoblede subgrafer og maatte utvides. Det er en direkte advarsel mot aa lese oensket geometri ut av en utilstrekkelig regelarkitektur: <https://arxiv.org/abs/0801.0861> og <https://arxiv.org/abs/1506.07588>.
- Geometrisk renormalisering paa grafer krever en eksplisitt coarse-graining/rescaling-map og konvergenskriterier, for eksempel via quasi-isometri og Gromov-Hausdorff-lignende ideer: <https://arxiv.org/abs/1606.08073>.
- Stable homology i causal sets brukes som en noedvendig, ikke tilstrekkelig manifoldlikhetsindikator og leter etter plateauer over discreteness-skalaen: <https://arxiv.org/abs/0902.0434>.
- Causal spectral geometry viser at operatorer bygd fra en kausal struktur kan baere relabel-invariant geometrisk informasjon. Dette er mer relevant enn aa fortsette med snapshot-spektra uten et Lorentzian/causal objekt: <https://arxiv.org/abs/1611.09947>.
- Causal Graph Dynamics formaliserer bounded information propagation og en generalisert translation/shift symmetry som aksiomer for time-varying graphs; den reversible utvidelsen legger reversibilitet til som et separat krav: <https://arxiv.org/abs/1202.1098> og <https://arxiv.org/abs/1502.04368>.

Ingen av disse arbeidene beviser at UniverseSimulation sin arkitektur vil lykkes. De stoetter rekkefolgen: regelkrav -> causal object -> coarse-graining -> geometry tests.

## Rangering av retninger

| rang | retning | dom |
| --- | --- | --- |
| 1 | A: symmetry-first/rule derivation | start naa; hoeyest informasjon per compute |
| 2 | C: intrinsic causal event-poset | neste bare hvis A passerer |
| 3 | B: coarse-graining/universality | sentral, men prematur uten A/C |
| 4 | F: stop/pivot | obligatorisk utgang ved A- eller C-fail |
| 5 | E: property-guided rule search | defer; ekstrem Goodhart-/overfittrisiko naa |
| 6 | D: defect reset | defer/drop; behold bare som senere excitation-test |

## Anbefalt program

### v16a: disjoint-event commutation gate

Dette er neste konkrete steg. Ingen stor dynamikk skal kjoeres foerst.

#### Objekt

For hver eventtype (`seed`, `birth`, `death`, `move`, `delete`, `triad`, `swap`, `stuck`):

- deklarer `readSet`
- deklarer `writeSet`
- deklarer identitetsallokering
- deklarer tilfeldige input
- deklarer om hazard/rate kan faktoriseres i lokale klokker uten remote state
- deklarer algebraisk delta i noder, kanter, tokens, komponenter og beta1

Generer alle kanoniske lokale supportmoenstre som trengs for aa aktivere eventet, og alle eventpar som skjemaet klassifiserer som disjunkte.

#### Test

For samme initialtilstand og pre-drawn eventinput:

1. anvend `e1; e2`
2. anvend `e2; e1`
3. sammenlign terminaltilstandene opp til konsistent node-relabeling
4. gjoer samme test paa relabelled copy
5. logg overlapping-support-par som negative/excluded controls, ikke som pass

#### Eksakte kriterier

- `PASS`: alle korrekt deklarert disjunkte par kommuterer eksakt opp til relabeling; token- og ikke-node-state matcher; alle relabelled trials matcher.
- `LOCAL CLOCK PASS`: global family-rate-representasjon er eksplisitt ekvivalent med en sum av bounded-support lokale hazards; ellers kan dagens scheduler ikke brukes til finite-propagation claims.
- `SCHEMA_FIX`: et avvik skyldes dokumentert for smalt read/write-sett. Skjemaet kan korrigeres én gang og hele gaten rerunnes.
- `FAIL/PIVOT`: ett korrekt deklarert disjunkt par er fortsatt ordensavhengig. Stopp causal cone-, Lorentz- og coarse-graining-arbeid paa dagens anchor. Redesign reglene eller gjoer scheduleren til eksplisitt fysisk struktur, som er en ny modellklasse.
- `FAILED FORMALIZATION`: hvis en endelig lokal support-enumerasjon ikke kan defineres, er lokalitet ikke presis nok for causal claims.

#### Forventet compute

Dette er en endelig mikrostats-/eventmønster-gate, ikke en `N=1024`-ensemble. Den boer koste minutter til timer, ikke hundrevis av store runs.

### v16b: intrinsic event-DAG og scheduler-invariance

Kjoeres bare ved v16a-pass.

- Definer dependency edge fra read/write-overlap eller ikke-kommutasjon.
- Sammenlign flere topologiske sorteringer/schedulere av samme event-DAG.
- Primaerkrav: samme unlabeled sluttfordeling og stabile causal-cone-observabler.
- Hvis scheduleren endrer konklusjonen, maa den enten inn i fysikken eller arkitekturen forkastes for observer-independent causal claims.

### v16c: liten coarse-graining pilot

Kjoeres bare ved v16b-pass.

- Tre stoerrelser, eksempelvis `512/1024/2048`.
- Minst to eksplisitte scale-maps.
- Intrinsic causal interval growth, volume-growth dimension, return/spectral flow og stable-homology plateau som separate estimatorfamilier.
- Fresh seeds og en microscopic-rule holdout.
- Bare ved konsistent pilot forsvares den stoerre `~648`-branch matrisen foreslaatt av teori-raadgiveren.

### v16d: excitation/defect-test

Defekter kommer tilbake sist, som test av en allerede validert causal/coarse geometry. De skal ikke definere geometrien de brukes til aa teste.

## Hvor mye evidens trengs for aa si «mulig»?

En nøktern possibility-claim krever minst denne stigen:

1. **Mekanismevaliditet:** eksakt relabel-invarians, formell lokal support og disjoint commutation eller eksplisitt intrinsic scheduler.
2. **Robust causal struktur:** finite dependency cones og causal isotropy over fresh graph families, seeds og scheduler controls.
3. **Skalaatferd:** to coarse-graining-maps og flere uavhengige estimatorer konvergerer mot samme makroklasse over minst tre klart separerte stoerrelser.
4. **Ikke-triviell struktur:** repeterbare excitations/interaksjoner som transfererer og ikke er definert av observabelen selv.
5. **Rule-class robustness:** mer enn én mikroskopisk regelvariant flyter mot samme makroatferd paa nested holdout.

Foerst da kan prosjektet forsvarlig si:

> Denne avgrensede relasjonelle modellklassen inneholder minst én konstruksjon med robust intrinsic causalitet, skalaatferd og ikke-triviell struktur som er universe-like i eksplisitt definerte henseender.

Det vil fortsatt ikke vise at dette er vaart univers, at Lorentz-invarians er etablert utover de testede observablene, eller at kvantemekanikk/entanglement har oppstaatt.

## Ting vi eksplisitt ikke boer gjoere naa

- Ikke gjenapne far-shell, placement eller beta1 med nye labels.
- Ikke optimaliser rule space mot en samlet «universe score».
- Ikke bruk eksterne fysikkanalogier som labels for graph patterns.
- Ikke starte `2048+` scale runs foer v16a/v16b.
- Ikke kalle stochastic correlation for entanglement.
- Ikke tolke relabel-invarians alene som diffeomorphism- eller Lorentz-invarians.

## Beslutning

Den brede ideen boer ikke stoppes ennaa, men v15-observabelprogrammet er ferdig. Prosjektet skal enten:

1. passere v16a og bygge en faktisk intrinsic causal/coarse-graining-arkitektur, eller
2. pivoteres bort fra dagens anchor-regler.

Det er den mest informative og minst selvbedragelige veien videre.
