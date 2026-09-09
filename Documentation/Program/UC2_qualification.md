# UC2 — kvalifisering, kjørebok og avgrensning

**Oppdatert etter måling:** Den frosne kalibreringen og kandidaten er nå kjørt
og fullt replay-verifisert. Se [UC2_report.md](UC2_report.md) for resultatet:
én kort tidslig løkkesekvens i 16 kjøringer; ingen etablert metastabilitet.
RAG-synk virker, men full generativ query-audit er blokkert av leverandørens
oppbrukte API-kreditter. Resten nedenfor bevarer kvalifiseringen før måling.

Dato: 2026-09-10. Work ID `UC2`; utgangspunkt `3cedd21`;
branch `program/wp-f2-f3-20260908`. Koordinator/integrator: root.
Tilstand ved første publiseringsetappe: **VERIFIED — klar for frosset,
avgrenset kandidatkjøring; full kalibrering og kandidat ikke kjørt ennå**.

## Ansvar og begrensning

`historical_signal_check` eide bare den nye simulatorkjernen og dens tester.
`latest_results_review` eide bare RAG-smoke-rettelsen, tilhørende tester og
deretter egne runner-regresjonstester. `provenance_index` eide bare generatoren
for den deklarerte proveniensindeksen og dens tester. Root integrerer,
registrerer protokollen, kjører målingene og eier alle Git-/serverendringer.
Gamle, urelaterte arbeidsfiler beholdes urørt og utenfor committene.

Dette kvalifiserer **den nye UC2-kjernen for det beskrevne forsøket**, ikke alle
historiske simulatorer eller alle mulige fremtidige vekstregler. Historisk
`relational_universe_sim.py` er ikke endret. Modellen har ingen fødsler,
fragmentering, fysisk tidsskala eller romlige koordinater.

## Målrettet verifisering før måling

Alle følgende tester ble faktisk kjørt, uten samlet skanning av Documentation:

| Testfil | Bestått | Dekning |
| --- | ---: | --- |
| `tests/test_local_change_candidate.py` | 11 | Alle 285 graf/posisjonstilstander og 198 lovlige trekk for enkle grafer med 1–4 noder; invers, lokalitet, enhetsbevaring, komponenter, ommerking, ugyldige kall, blokkerte enheter, delt minne, replay og observatørisolasjon |
| `tests/test_local_change_runner.py` | 15 | Preregistrert arbeidsmengde, initialisering, frø, klokker, råspor, summer, referansegate og hasher; avviser manipulert eller utdatert evidens |
| `rag_service/tests/test_research_smoke_audit.py` | 14 | Falske/manglende audits, tomme sitater, feil backend, token-echo og krav til faktisk sitert UC2-dokument |
| `tests/test_research_provenance.py` | 15 | Kildehash, entydige noder, gyldige kanter, determinisme, avgrensede kildebaner og vern mot overskriving |
| `tests/test_units_of_change_conformance.py` | 6 | UC1-detektorens analytiske terskel, ommerking, reversering og fortegnsregning |

Totalt **61 målrettede tester bestått**. Runner-testene bruker bittesmå,
midlertidige fixture-protokoller og er ikke kandidatmålinger. Initialiseringens
Prüfer-konstruksjon ble dessuten uavhengig kontrollert mot alle 1 441 ord for
n=2…6; den var entydig og ga sammenhengende trær. Den varige testsuiten dekker
de 145 ordene for n=2…5.

En separat fler-enhetsstresstest besto **40 000 forsøk**, med 22 299 vellykkede
endringer, 17 701 blokkerte forsøk og **0 invariantbrudd**. For hvert frø ble
`random.Random(seed)` brukt til `uniform_tree(64, rng)`, deretter 32 plasseringer
fra `rng.randrange(64)`, og 5 000 `attempt_step`-kall med samme strøm.
Hvert kall kontrollerte en enkel, symmetrisk graf, 64 noder/63 kanter,
opprinnelig komponentpartisjon, alle 32 enhetene på eksisterende noder,
uendrede ikke-valgte enheter og riktig kilde. Et vellykket kall krevde en
eksisterende hoppkant, nøyaktig én kanterstatning og tikk+1; et blokkert kall
måtte bevare graf, posisjoner og tikk. Ingen sirkulasjonsmål ble beregnet.

| Frø | Forsøk | Vellykkede | Blokkerte |
| --- | ---: | ---: | ---: |
| 4200 | 5000 | 2671 | 2329 |
| 4201 | 5000 | 3011 | 1989 |
| 4202 | 5000 | 2520 | 2480 |
| 4203 | 5000 | 2897 | 2103 |
| 4204 | 5000 | 3566 | 1434 |
| 4205 | 5000 | 2066 | 2934 |
| 4206 | 5000 | 2728 | 2272 |
| 4207 | 5000 | 2840 | 2160 |

Uavhengig gjennomgang fant og stoppet to reelle hull før måling: runneren stolte
først på en lagret gateverdi og håndhevet ikke hele registrerte kjøreplanen.
Begge er rettet. Nå rekonstrueres initialisering, PRNG-sekvens, alle lovlige
hendelser og aggregatene; kandidatverifikasjon kontrollerer også de refererte
kalibreringsdataene. Den sekundære målteksten ble før frys presisert til
**enkle** eksakte tilstandssykluser, slik implementasjonen faktisk måler.

## Frosne kilder

| Fil | SHA-256 |
| --- | --- |
| `UC2_preregistration.json` | `56de517f878efb184485373af87c801732be7a4b5651c0d427b4a7f4396349ed` |
| `Tools/local_change_candidate.py` | `c4f63b6fea5835bd06fb25e6586e094508e2e2e006fda91fe2c88bb7eb218c44` |
| `Tools/run_local_change_candidate.py` | `d55a2f02332ca5232bf810ed1f3cbc1b5fd989fd7c3158d3b2d1f4d31cf3f586` |

Kalibreringskjøringen skal skrive sine egne kilde- og rådatahasher. Kandidaten
nekter å starte med endrede kilder eller ukvalifiserte referanser. Ingen
parametertilpasning på kandidatresultatene er tillatt i denne runden.

## Drift og faktisk gjenfinning

SSH er gjenopprettet med den dokumenterte Hetzner-identiteten. Standardnøklene
ble avvist også utenfor sandbox; eksplisitt identitet virket for ops og root.
Den dedikerte Universe-RAG svarte HTTP 200 på health. Health er ikke bevis på
oppdatert korpus, fungerende sitater eller publisert forskningsresultat.

RAG-smoke krever nå at både `citation_audit.ok` og `freshness.ok` er bokstavelig
true og at faktiske sitater finnes. `--required-citation-substring UC2` krever
treff i sitatidentitet, ikke bare omtale i svarteksten. Revisjonsferskhet må i
tillegg kontrolleres mot de speilede dokumentenes bytes og forventet innhold.
En kildesjekksummet proveniensgraf legges inn som Markdown/CSV, **ikke** som en
ny grafdatabase eller automatisk verifiserte vitenskapelige konklusjoner.

Første etappe committes/pushes før full kandidatmåling. Serverens eksisterende
master-checkout bevares; publisering og synk bruker en separat release av den
pushede committen. Endelig publiseringskvittering skal skille statisk HTTPS,
RAG-synk, autentisering, PostgreSQL-rate-limit, sitatkontroll og ferskhet. Ingen
av disse erklæres bestått på grunnlag av denne forhåndskvalifiseringen alene.
