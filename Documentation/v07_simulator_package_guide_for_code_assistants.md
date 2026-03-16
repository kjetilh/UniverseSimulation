# Guide for kodeassistenter: simulatorpakken for relasjonell universgraf

## Formål

Denne kodebasen brukes til å teste en enkel, bakgrunnsløs universmodell der universet er en dynamisk graf med én relasjonstype. Lokale stokastiske rewrite-hendelser driver utviklingen. Prosjektet prøver ikke å bevise fysikk direkte; det prøver å finne ut hvilke regimer som samtidig viser:

- lokal kausalitet eller begrenset påvirkningsspredning,
- repair eller meeting mellom nesten like grener,
- lav makrodrift i utvalgte størrelser,
- og geometri-lignende makromønstre.

## Hvilke simulatorer som faktisk er aktive

- `relational_universe_sim.py`
  Grunnsimulatoren for den relasjonelle grafdynamikken. Brukes når du trenger rå tidsserier, kandidat-invarianter eller koblede runs på lavt nivå.
- `relational_universe_sim_energy.py`
  Variant for energikandidater og mer eksplisitt driftanalyse i åpne og lukkede regimer.
- `relational_universe_feature_lab.py`
  Feature-lab for quasi-invarianter, redusert basis, SVD-lignende analyse og tolkning av målestørrelser.
- `relational_universe_rule_delta_lab.py`
  Regel-delta-lab for regelbetingede `ΔF`, redusert basis og lokal struktur i rewrite-reglene.
- `relational_universe_perturbation_lab.py`
  Perturbasjonslab for lokal skade, radiusutbredelse, causal-cone-lignende diagnose og batch/multirun.
- `relational_universe_uniformized_coupling_lab.py`
  Familywise uniformization i åpne regimer med `birth`/`death`.
- `relational_universe_uniformized_scan.py`
  Scan over uniformized coupling-regimer.
- `relational_universe_local_max_coupling_lab.py`
  v0.7-laben. Beholder familywise uniformization, men kobler de endelige lokale kjernene med eksplisitt maksimal kobling. Dette er hovedverktøyet for repair, `meeting_fraction` og `same_descriptor_rate`.
- `relational_universe_v07_phase_probe.py`
  v0.8-scan på toppen av v0.7. Kartlegger repair, radius/front, makrodrift og geometri-proksier i ett parameterkart.

## Representative eksperimenter

Representative v0.7-verifikasjon:

```bash
python3 relational_universe_local_max_coupling_lab.py \
  --mode verify \
  --label v07_local_max_coupling \
  --out-prefix Documentation/v07_local_max_coupling \
  --verification-trials 4000 \
  --verification-event-steps 1200 \
  --multirun-seeds 12 \
  --seed 101 \
  --r-birth 0.05 \
  --r-death 0.05 \
  --p-swap 0.08 \
  --p-triad 0.0 \
  --p-del 0.0
```

Representative v0.8-fasekart:

```bash
python3 relational_universe_v07_phase_probe.py \
  --out-prefix Documentation/v08_phase_map \
  --steps 400 \
  --multirun-seeds 3 \
  --start-seed 1600 \
  --r-birth-grid 0.02,0.05,0.08 \
  --r-death-grid 0.00,0.02,0.05 \
  --p-swap-grid 0.02,0.04,0.08 \
  --p-triad-grid 0.00,0.01,0.03 \
  --p-del-grid 0.00,0.01
```

Representative perturbasjonsbatch:

```bash
python3 relational_universe_perturbation_lab.py \
  --mode batch \
  --steps 500 \
  --seeds 101,102,103 \
  --regimes closed_topological,open_topological \
  --perturbations local_swap,add_chord \
  --out-prefix Documentation/perturbation_batch
```

## Hvordan sentrale mål skal tolkes

### `local_overlap_prob`

Data:
- overlap-massen mellom to endelige lokale kjerner i en gitt event-familie.

Tolkning:
- høyere verdi betyr at grenene hadde større teoretisk sjanse til å velge identisk lokal hendelse.

Ikke lov å konkludere:
- høy `local_overlap_prob` betyr ikke at hele prosessen er kontraktiv eller at spacetime er funnet.

### `same_descriptor_rate`

Data:
- hvor ofte de to grenene faktisk valgte samme lokale hendelsesdeskriptor når begge aksepterte samme familie.

Tolkning:
- hvis denne øker når `local_overlap_prob` øker, fungerer den lokale koblingen skarpere.

Ikke lov å konkludere:
- høy `same_descriptor_rate` alene betyr ikke repair av hele tilstanden.

### `meeting_fraction`

Data:
- andel runs der kontroll og perturbert gren faktisk møtes igjen helt.

Tolkning:
- dette er et direkte repair-mål.

Ikke lov å konkludere:
- `meeting_fraction = 0` betyr ikke at lokal repair mangler; det kan fortsatt finnes høy lokal overlap og mye delt struktur uten full meeting.

### `total_unequal_time`

Data:
- total kontinuerlig tid der grenene var ulike.

Tolkning:
- lavere verdi er normalt bedre for repair eller svakere langvarig divergens.

Ikke lov å konkludere:
- lav `total_unequal_time` betyr ikke automatisk begrenset causal cone; radiusmålet må fortsatt sjekkes.

### `shared_token_fraction_final`

Data:
- andel token-identiteter som fortsatt deles ved slutt.

Tolkning:
- høyere verdi betyr at mer av token-lineagen er bevart på tvers av grenene.

Ikke lov å konkludere:
- dette er ikke en bevaringslov og ikke en energi. Det er et likhetsmål mellom to runs.

### `final_radius_control`

Data:
- største observerte grafavstand fra initialt perturbasjonssupport til skadede noder i kontrollgrenen.

Tolkning:
- lavere radius peker mot mer begrenset spredning.

Ikke lov å konkludere:
- et lite slutt-radius i én kort run er ikke en Lieb-Robinson-bound og ikke en universell hastighet.

## Hva som teller som fremgang

- Når en ny koblingsmetode øker `local_overlap_prob` og `same_descriptor_rate` uten å bryte marginals.
- Når et regime kombinerer moderat eller lav radius med lav makrodrift.
- Når `meeting_fraction` eller `shared_token_fraction_final` øker uten at dette bare skyldes trivielle eller nesten frosne regimer.
- Når samme område i parameterrommet ser bra ut på flere aksjer samtidig: repair, drift og geometri.

## Hva som ofte bare er teknisk variasjon

- Små endringer i `clustering` eller `dim_proxy` når samplet er kort og grafene er små.
- Forskjeller mellom korte runs med få seeds.
- Økning i én score når de andre kollapser, for eksempel bedre overlap men mye større radius eller drift.
- Forbedringer som bare kommer av at dynamikken nesten stopper opp.

## Konklusjoner du ikke får trekke for tidlig

- Ikke kall noe en bevaringslov før du har sjekket at det ikke bare følger algebraisk av definisjonene.
- Ikke kall et regime spacetime-lignende bare fordi radiusen er lav i ett parameterpunkt.
- Ikke bruk `geometry_score` som om det var fysisk observabel. Den er en heuristisk rangeringshjelp.
- Ikke les `meeting_fraction` som en generell kontraksjonssetning for hele modellen.
- Ikke sammenlign scorer på tvers av svært ulike run-lengder og seed-antall uten å si det eksplisitt.

## Arbeidsmåte for kodeassistenter

- Behandle filene på disk som ground truth; bundle-mapper er arkiv, ikke automatisk aktive kilder.
- Skill alltid mellom:
  - eksakte algebraiske identiteter,
  - numerisk verifiserte implementasjonsegenskaper,
  - og dynamiske eller heuristiske resultater.
- Når du foreslår nye eksperimenter, knytt dem til konkrete scripts og konkrete output-filer i `Documentation/`.
- Hvis du endrer koblingslogikk, verifiser marginals og absorpsjon på nytt før du tolker fysikk.

## Ordliste

- `familywise uniformization`
  Felles potensial-klokke der event-familien velges fra dominerende rater før hver gren aksepterer eller avviser.
- `local kernel`
  Den endelige sannsynlighetsfordelingen over konkrete lokale hendelser i én event-familie.
- `maximal coupling`
  En kobling som maksimerer sannsynligheten for identisk utfall gitt to fordelinger.
- `repair`
  Tendensen til at to nesten like grener blir mer like igjen, eller helt møtes.
- `meeting`
  Tidspunktet der to hele tilstander blir identiske.
- `causal cone`
  Operasjonell idé om at en lokal perturbasjon bare påvirker et begrenset område etter begrenset tid.
- `macro drift`
  Netto endring i utvalgte makrostørrelser som `tokens` eller `beta1`.
- `geometry proxy`
  En størrelse som `spectral_radius`, `clustering` eller `dim_proxy` som brukes som indirekte indikator på grafgeometri.
