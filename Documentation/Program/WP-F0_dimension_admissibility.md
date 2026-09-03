# WP-F0: Adgangstest for dimensjonsspørsmålet

Repo: /Users/kjetil/Build/Digipomps/HAVEN/UniverseSimulation (gren master).
Fingeravtrykk: `event-dag-dimension-admissibility`.
Les `Documentation/Status_Og_Retninger_2026-08-23.md`, seksjonen **RETTELSE —
24. august 2026**, før du begynner. Den er premisset for hele pakken.

## Objektiv

Avgjør om hendelses-DAG-en i det hele tatt er et objekt man kan tilordne en
dimensjon. Dette er en adgangstest, ikke en dimensjonsmåling. Utfallet avgjør om
den dyre runden skal kjøres eller ikke.

Alt her kjøres på **eksisterende historier**. Ingen ny dynamikk. Anslått kostnad:
timer, ikke dager.

## Premiss (verifisert, ikke antatt)

- Riktig Myrheim–Meyer-normalisering for `comparable_pair_fraction` (normalisert
  på C(N,2)) er `r = Γ(d+1)Γ(d/2) / (2 Γ(3d/2))`. Kontroll: d=2 skal gi nøyaktig
  0,5. Den tidligere brukte `/4`-formen er gal her.
- Myrheim–Meyer er degenerert i tynne regimer: den tildeler d ≈ 5,4 også til en
  disjunkt union av kjeder. Den kan derfor ikke brukes uten en bestått
  adgangstest først.
- Kjedelengde-estimatoren er `L ≃ m_d · N^(1/d)` med `m_d ≈ 1,85` for d i 2–6 ved
  N ≤ 6144, ikke `ln N / ln L`.

## Oppgave

Skriv **ett** verktøy, `Tools/causet_admissibility.py`, som leser eksisterende
hendelses-DAG-er og regner ut størrelsene under. Ikke ett script per størrelse.

Finn historiene ved å lese hvordan `relational_universe_v16b_intrinsic_event_dag_gate.py`
og `v16i_causal_interval_abundance_gate.py` bygger DAG-en, og gjenbruk den
konstruksjonen. Ikke bygg en ny DAG-definisjon.

**Regn ut, per historie og per scheduler-arm:**

1. **G0.1 — gulvforholdet.** `r_floor = Σ_v depth(v) / C(N,2)` der `depth(v)` er
   lengste vei inn til v. Rapporter `r / r_floor`.
   *Sjekk først og rapporter eksplisitt hva `causal_depth` faktisk er i denne
   koden: lengste vei, korteste vei eller topologisk nivå. Er det ikke lengste
   vei, holder ikke gulvgrensen og må regnes om.*
2. **G0.2 — lenker per element.** Transitivt reduser DAG-en først; konfliktkanter
   er ikke automatisk dekkrelasjoner. Rapporter både rå kanter/hendelse og
   lenker/hendelse etter reduksjon, som funksjon av N.
3. **G0.3 — største Alexandrov-intervall.** `max |I(p,q)|` over alle komparable
   par, som andel av N.
4. **G0.4 — Θ.** `Θ = r·(N−1)/(h−1)` der h = lengste kjede.
5. **Desimeringseksponenten.** For p ∈ {1, ½, ¼, ⅛, 1/16, 1/32}: trekk hvert
   element uavhengig med sannsynlighet p, ta indusert delposet av den transitive
   lukningen, mål L(p). Minst 20 trekk per p per historie. Tilpass
   `s = ∂ln L / ∂ln p` med tilpasningen begrenset til L ≥ 8. Rapporter s med
   bootstrap-KI, per arm.
   Mål samtidig r(p) over hele spennet.

**Referansetall å sammenligne mot (fra rådgiverens simuleringer, oppgitt her så
du ikke trenger å regne dem ut på nytt — men verifiser gjerne):**

| størrelse | kjedebunt | sprinkling d=2 | d=4 | d=5 |
| --- | --- | --- | --- | --- |
| Θ ved N=2048 | 1,00 | 12,3 | 18,4 | 13,3 |
| lenker/element | 0,98 | — | 28,4 | 23,1 |
| desimeringsslope s | 0,76 | 0,538 | 0,302 | — |

## Forhåndsregistrerte terskler — frys disse før første tall regnes ut

**Gate 0 består** hvis alle fire holder:
- G0.1: `r / r_floor ≥ 2,0`
- G0.2: lenker/hendelse ≥ 5 ved N=2048
- G0.3: `max |I| ≥ 0,05 N`
- G0.4: `Θ ≥ 5`

**Gate 1 (desimering) består** hvis `s ∈ [0,20, 0,40]`, bootstrap-95 %-KI smalere
enn 0,05, og de to armene er enige innenfor 0,05.

## Forhåndsdefinert utfall (G4) — begge er gyldige, og det negative er ventet

Rådgiverens forhåndsanslag, gjort før måling: **G0.1 feiler ved ~1,3, G0.2 feiler
ved 1,22, G0.4 feiler ved ~1,34.** Det anslaget står skrevet her på forhånd
nettopp for at du ikke skal kunne justere deg til det.

- **Gate 0 feiler:** skriv konklusjonen rett ut. Formuleringen skal være at
  DAG-en er et bunt av ≈N/h svakt vekselvirkende kausale tråder, at
  Myrheim–Meyer ikke bærer geometrisk informasjon i dette regimet, og at den dyre
  runden derfor ikke skal kjøres. Det er programmets svar, ikke en mislykket
  pakke.
- **Gate 0 består:** rapporter det, og stopp. Ikke gå videre til dimensjonsmåling
  i denne pakken.

**Ikke juster terskler.** Mener du en terskel er feil satt, skriv det som en
begrunnet observasjon i rapporten og la terskelen stå.

## Grunnsannhet (G5)

Sprinkling-referansene er generert uavhengig av dette repoet og av dets
nullmodeller. DAG-ene som måles er produsert av v16-kjøringer som ble gjort før
denne pakken fantes. Ingen av tallene er selvprodusert for anledningen.

## Ikke-mål

- Ikke bruk den eksisterende lag-/indegree-bevarende nullen. Den bevarer hver
  hendelses kausaldybde eksakt og låser dermed ~76 % av r ved konstruksjon;
  den måler foreldre-lokalitet, ikke dimensjon. En forkastning mot den beviser
  ingenting her.
- Ikke regn ut spektraldimensjon. Ikke regn ut intervall-abundans. Begge er
  meningsløse før Gate 0 er bestått.
- Ikke kjør ny dynamikk.
- Ikke kjør closure-policyen i AGENTS.md. Dette er en analysepakke.
- Ingen fysikkpåstander. Ingen konklusjon sterkere enn tallene.

## Stoppregel (G3)

Maks to forsøk på samme feil. Tredje gang: stopp, skriv «Blokkert», rapporter.

## Commit

`git add` kun dine egne filer eksplisitt. `git pull --rebase` før push, inntil 3
forsøk ved konflikt — andre pakker kjører samtidig i samme repo. Ikke ta med
`.DS_Store`. Melding starter `WP-F0: causal set admissibility on existing histories`.

## Rapporter tilbake i `Documentation/Program/WP-F0_report.md`

1. Hva `causal_depth` faktisk måler i koden.
2. Målte tall for G0.1–G0.4 og for s, per arm, per N, med spredning.
3. Bestått/ikke bestått per terskel, uten omskriving.
4. Konklusjonen, formulert innenfor det tallene bærer.
5. Commit-hash.
6. Alt som ble blokkert.

## Hjerteslag (obligatorisk, lagt til 24. aug)

Skriv en linje til `.program_logs/<pakkenavn>.heartbeat` hvert femte minutt og ved
hvert delsteg, på formen `<ISO-tid> <kort statuslinje>`. En vakt leser filen for å
skille «arbeider» fra «død». Uten hjerteslag antas pakken død og blir startet på
nytt — som koster mer enn linjen gjør.
