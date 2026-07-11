# Relasjonell universgraf v0.15du: relabel- og symmetrigate

## Formaal og maal

`purposeRef`: `purpose://prompt.unknown`.
Candidate intake: undersoek om en minimal relasjonell rewrite-modell kan gi robuste univers-lignende effektive lover uten aa lese implementasjonsartefakter som fysikk.

| goal | baseline | target | status | evidence |
| --- | --- | --- | --- | --- |
| G1: representation gate | node-id invarians var antatt, ikke direkte auditert | maal kernel og constructor separat | satisfied | v15du relabel trials |
| G2: symmetry witness | tidligere near-symmetry var feature-avstand | krev eksakt markert lokal isomorfi | satisfied | radius 1-3 isomorphism audit |
| G3: research decision | flere konkurrerende neste spor | velg stopp/go uten fabricated physics claim | satisfied | evaluation + panel adjudication |

## Premissene som faktisk testes

- Mikrotilstanden er en endelig, enkel, urettet graf med node-ID-er som representasjon, ikke fysisk koordinat.
- Lokale stokastiske rewrite-hendelser er units of action; simulatorens tokens og placement-indekser er instrumentering og skal ikke automatisk leses som primitive partikler.
- Tid, geometri, excitations og bevaringslover maa i prosjektets sterke program oppstaa som robuste makrobeskrivelser; de er ikke gitt av at koden kan kjoere.
- En ommerking av node-ID-er skal ikke endre overgangssannsynlighetene. En perturbasjonskonstruktoer som velger etter numerisk nodeorden maa auditeres separat.

## Evidensstige

| level | hva som kan hevdes | minste evidenstype | dagens status |
| --- | --- | --- | --- |
| 0 | modellen er matematisk og maskinelt definert | spesifikasjon + reproducerbar kode | oppfylt |
| 1 | observabelen er fri for kjente representasjons-/generatorartefakter | relabel-, kontroll- og hygiene-gater | delvis; v15du avgjoer ny gate |
| 2 | en ikke-triviell lokal respons finnes | matched controls og reproduserbare trajectories | avgrenset stotte |
| 3 | responsen er robust | fresh growth seeds, skalaer, korrekte koblinger og alternative konstruktoerer | ikke oppfylt samlet |
| 4 | en effektiv klasse/lov predikerer nytt | helt frossen analyse og minst to uavhengige holdout-blokker | ikke oppfylt |
| 5 | en mekanisme er identifisert | preregistrerte inngrep/ablasjoner som endrer effekten | ikke oppfylt |
| 6 | univers-lignende lovstruktur | samtidig lokalitet, symmetri, quasi-invariant/skala, stabile excitations og prediktiv coarse-graining | ikke oppfylt |
| 7 | en mulig universbygger er konstruktivt vist | ett fullt spesifisert system som passerer level 1-6 robust | aapen |

Ett konstruktivt system kan logisk vise mulighet, men bare dersom hele claim-bunten er demonstrert samtidig og artefaktfritt. Mange mislykkede kandidater kan avvise konkrete selectors, mekanismer og avgrensede regelklasser, men kan ikke bevise at den brede ideen er umulig. En sterk negativ konklusjon krever et no-go-teorem for en presist definert klasse eller uttommende analyse av et endelig rom.

## Hvor mye evidens er nok

- Tre fresh graph-witnesses er bare en kandidatgate for lokal quasi-ekvivalens, ikke endelig bevis.
- Robusthetsclaims maa bruke growth seed som generaliseringsenhet, rapportere usikkerhet og effektstoerrelse, og overleve minst to frosne holdout-runder.
- Skala- eller lovclaims maa vise samme dimensjonsloese relasjon over minst tre stoerrelser med en predefinert finite-size trend; et enkelt scale jump er ikke renormalisering.
- Symmetri maa foerst ha en eksplisitt transformasjon og kernel-kovarians. Dynamisk quasi-symmetri maa deretter slaa matched ikke-isomorfe nullpar.
- Lorentz-lignende språk krever placement-/mode-uavhengig propagasjon, isotropi og en stabil dispersjons-/frontlov; dagens repo er fortsatt `not_yet`.
- En endelig run-mengde bestemmes med power/precision fra observert variasjon. Fast n alene er ikke bevisstandarden.

## v15du design

- target: `1024`
- perturbation: `add_chord`
- growth seeds: `202;303;404;505;606;707;808;909;1001;1103;1201;1301;1409;1511;1601;1709`
- placements: `p0;p1;p2`
- relabel seeds per context: `19001;19037;19081;19121`
- local witnesses: exact marked graph isomorphism at radius 1, 2, and 3, both without and with boundary-degree marks
- existing dynamics only: v15dq + v15dr + v15ds placement outcomes; no new defect dynamics

## Relabel-resultat

| key | value | evidence |
| --- | --- | --- |
| transition_kernel_relabel_equivariance | 1.000 | tolerance=1.0e-12 |
| add_chord_constructor_relabel_equivariance | 0.172 | transported candidate must equal candidate found after node relabel |
| post_perturbation_graph_relabel_equivariance | 0.214 | transported post-edge-set equality |

Kernel-kovarians og constructor-kovarians er ulike evidenstyper. At kjernen passerer kan ikke reparere en constructor som velger en annen fysisk chord etter ren node-ommerking.

## Markert lokal isomorfi

| radius | match_mode | isomorphic_pair_count | cross_seed_isomorphic_pair_count | repeated_equivalence_class_count | max_equivalence_class_size | cross_seed_active_agreement | cross_seed_median_absolute_rate_gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | structural | 0 | 0 | 0 | 1 | nan | nan |
| 1 | boundary_aware | 0 | 0 | 0 | 1 | nan | nan |
| 2 | structural | 0 | 0 | 0 | 1 | nan | nan |
| 2 | boundary_aware | 0 | 0 | 0 | 1 | nan | nan |
| 3 | structural | 0 | 0 | 0 | 1 | nan | nan |
| 3 | boundary_aware | 0 | 0 | 0 | 1 | nan | nan |

En radius-1 match er bare en lokal kontur. Boundary-aware radius-3 isomorfi er sterkere, men er fortsatt ikke en global graph automorphism eller en fysisk symmetry group.

## Placement-exchange audit

| comparison | n_growth_seeds | mean_established_rate | active_seed_fraction | paired_active_agreement | mean_signed_rate_difference | median_absolute_rate_difference | exact_sign_flip_pvalue |
| --- | --- | --- | --- | --- | --- | --- | --- |
| p0_marginal | 16 | 0.250 | 0.375 |  |  |  |  |
| p1_marginal | 16 | 0.211 | 0.250 |  |  |  |  |
| p2_marginal | 16 | 0.344 | 0.500 |  |  |  |  |
| p0_minus_p1 | 16 |  |  | 0.500 | 0.039 | 0.250 | 0.764 |
| p0_minus_p2 | 16 |  |  | 0.625 | -0.094 | 0.000 | 0.453 |
| p1_minus_p2 | 16 |  |  | 0.250 | -0.133 | 0.500 | 0.361 |

En hoy p-verdi er ikke bevis for exchange-symmetri. Tabellen er en sensitivitetsaudit av placement-labelene, ikke en fysisk invarianttest.

## Raadgiverpanel og claim-adjudikasjon

- Fysikk-/metodeskeptikeren krevde en eksplisitt relabel- eller marked-isomorphism witness foer symmetry-språk.
- Emergens-steelman rangerte kernel/automorphism-gaten foran nye feature-avstander, deretter lokal quasi-konjugasjon, interaction og conditional quasi-invariants.
- Evidensdommeren understreket at far-shell damage er coupling-definert, og at neste dynamiske hovedgate senere maa teste coupling-uavhengighet.
- Panelet er ikke en avstemning. Enigheten brukes som argumentstruktur; reporesultatet avgjoer diagnosen.

Root claim: `En symmetry-holdout er berettiget naa`.
Composition: `allOf(kernel relabel covariance, constructor covariance, repeated marked local witnesses)` undercuttes dersom constructor eller witness-gaten feiler.

## Eksterne metodeankere

- Bombelli, Henson og Sorkin viser at diskrethet og Lorentz-symmetri har skarpe kompatibilitetskrav; saerlig kan ikke en endelig-valens graf hentes equivariant fra en Poisson-sprinkling. Dette er en guardrail, ikke evidens for repoet: https://arxiv.org/abs/gr-qc/0605006
- Reversible Causal Graph Dynamics formaliserer shift-invariance, bounded-speed causality og reversibility som eksplisitte krav til grafdynamikk. Repoet har ikke automatisk disse egenskapene: https://arxiv.org/abs/1502.04368
- Quantum Graphity viser at permutasjonsinvariant mikrofysikk og emergent lavdimensjonal geometri er en legitim modellklasse, men analogien overfoerer ingen resultater til denne generatoren: https://arxiv.org/abs/hep-th/0611197

## Beslutning

- diagnosis: `kernel_equivariant_but_constructor_breaks_relabel_symmetry`
- next_step: `replace_constructor_with_distributionally_relabel_invariant_candidate_sampling`
- claim ceiling: `implementation-level relabel covariance and/or local marked quasi-equivalence`, aldri fysisk symmetri fra denne runden alene

## Aapne spor etter gaten

1. Coupling-invariance: samme frozen marginal observables under maximal og rank coupling.
2. Constructor/null: uniformly sampled relabel-invariant chord mot matched random chord og no-op.
3. Conditional quasi-invariants: bare innen en holdout-validert dynamisk ekvivalensklasse.
4. Ekte coarse-graining/RG: nestede beskrivelser av samme graf, ikke separate target-genereringer.
5. Lorentz-/causal-spor: eksplisitt kernel-locality og mode/placement-independent frontlov.
