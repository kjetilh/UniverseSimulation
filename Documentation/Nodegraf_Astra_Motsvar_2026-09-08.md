# Astra: motsvar til nodegrafvurderingen

[vurdering] Vurderingen trenger vesentlig korrigering. De sterkeste innvendingene er at admissibiliteten bygger på en misvisende sammenstilling av referanser, at «ett par av 24» ikke dokumenterer en forbedring over β₁, og at den angivelig gjennomførte nye porten ikke håndheves. Selve fortegnspermutasjonen er derimot ikke feilen.

[vurdering] Avgrensning: én kildekritisk gjennomgang av de seks spørsmålene, med filhenvisninger relativt `UniverseSimulation/`. Grunnlaget er arbeidskopien ved commit `ac9b11a3fc13b01d1466449618c53b763a6097a7` på `losen/nodegraph-vurdering-20260908`. Vurderingsfilens SHA-256 ved lesing var `29e2260780aab051c17249750df8888a7af1629ac0fe61e87160a825d31126a2`. Jeg har lest kode og eksisterende resultater, beregnet avgrensede sammendrag direkte fra JSON og kontrollert statistiske premisser mot primærkilder. Simulator, søk, kompilator og testsuite er ikke kjørt på nytt; backendmoteksemplene nedenfor er kildeutledninger. Leveransen er bare denne fila.

## 1. Permutasjonsnullen

[belagt: Tools/nodegraph/arena/observable_purpose.py:50] Den faktiske statistikkimplementasjonen er nå importert fra `stats.py`. [belagt: Tools/nodegraph/stats.py:47] Den klipper differansene symmetrisk ved en empirisk kvantil av absoluttverdiene, beregner middel og populasjonsstandardavvik på de klippede differansene og bruker `min(abs(mean)*sqrt(n)/(sd+1e-12), 50)`.

[vurdering] For endelige differanser innenfor det numeriske arbeidsområdet holder algebraen: sett `c(d)=Q₀․₉(|d|)` og `W(d)ᵢ=clip(dᵢ,−c,c)`. For enhver fortegnsvektor `s` er `c(s⊙d)=c(d)` og `W(s⊙d)=s⊙W(d)`. Å bytte hi og lo gir nettopp `−dᵢ`. Det er klippingen som kommuterer; middelverdien og standardavviket må fortsatt beregnes for hver permutasjon.

[belagt: Tools/nodegraph/stats.py:142] NumPy-grenen gjør dette: én felles fortegnsvektor per permutasjon brukes på alle kandidatene, og både middel, standardavvik og maksimum beregnes på nytt. [vurdering] Den bevarer dermed avhengigheten mellom kandidatene. Å trekke uavhengige fortegn for hver kandidat ville vært feil for denne maksimumsnullen; det gjør koden ikke.

[vurdering] Maksimumsnullen er en passende utvalgsgate for den faktisk evaluerte, faste kandidatmengden under en felles null om at armene kan byttes innen par. Den kalibrerer ikke automatisk andre søkeseeds, andre statistikker eller en søkeprosess som endrer kandidatene etter å ha sett responsen. For en adaptiv forslagsstiller må hele den responsavhengige utvelgelsen inngå i hver nullkjøring, eller en uavhengig bekreftelse bære testen.

[belagt: Tools/nodegraph/stats.py:98] `null_single_p95` i `null_references` gjelder den første kandidaten, og NumPy-grenen tar tilsvarende kolonne 0 på linje 148. [vurdering] Dette feltet er ikke en universell terskel for en vilkårlig vinner. Kandidatenes differansemagnituder gir ulike nullfordelinger, også når statistikken er studentisert.

[belagt: Tools/nodegraph/run_experiment.py:106] Eksperimentet bruker heldigvis ikke dette treningsfeltet på holdout: det velger vinneren, beregner dens holdout-differanser og lager dens egen fortegnsnull på linje 108–111. [vurdering] Dette er riktig beslutningsstruktur for én på forhånd valgt vinner. At holdoutens absoluttverdier inngår i dens egen permutasjonsfordeling er ikke utvalgslekkasje; det er betingingen testen bygger på.

[vurdering] Den viktige mangelen er spranget fra en korrekt algebraisk identitet til en «eksakt» inferensiell null. Det kreves at den felles fordelingen er invariant under de tillatte armbyttene, eller tilsvarende begrunnede symmetri- og uavhengighetsantakelser for fortegnsflippingen. Null forventet differanse alene er ikke nok. Dette er skillet mellom utbyttbarhet og fortegnssymmetri hos [Winkler mfl.](https://wrap.warwick.ac.uk/65670/1/WRAP_1-s2.0-S1053811914000913-main.pdf).

[belagt: Tools/nodegraph/arena/build_substrate.py:137] Starttilstanden får startseeden, mens hendelsesstrømmen får en annen seed; linje 188 setter den systematisk til `s*7919` for lo og `s*7919+1` for hi. [vurdering] Dette er ikke tilfeldig tildeling av armetiketter som i seg selv gir et randomiseringsbevis. [usikker] Jeg har ikke belegg for at koblingen gir skjevhet i disse dataene, men heller ikke et dokumentert bevis eller en nullarmkalibrering som etablerer den nødvendige utbyttbarheten for hele prosedyren.

[vurdering] Tilsvarende kansellerer en felles starttilstand et additivt startbidrag; den kansellerer ikke automatisk start×arm-interaksjon eller startavhengig støy. For eksempel gir `O(s,L)=a(s)+b(s)L+ε` en paredifferanse som fortsatt avhenger av `b(s)`. [belagt: Tools/nodegraph/arena/observable_purpose.py:15] Formuleringen om at startfamilievarians kanselleres «by construction» er derfor sterkere enn designet alene bærer.

[belagt: Tools/nodegraph/run_experiment.py:144] Standardkjøringen bruker 2 000 permutasjoner. [vurdering] Det er Monte Carlo-kalibrering, ikke uttømmende beregning av en eksakt terskel. Ved åtte par finnes bare 256 fortegnsvektorer; alle kan tas med. Ved større n ville jeg rapportert rangbasert permutasjons-p med tie-regel og Monte Carlo-presisjon, ikke bare en avrundet p95-gate. [belagt: Tools/nodegraph/replicate.py:29] Replikasjonskoden bruker allerede `(ge+1)/(reps+1)`, en gyldig konservativ konstruksjon ved tilfeldig trukne permutasjoner; se [Phipson og Smyth](https://gksmyth.github.io/pubs/PermPValuesPreprint.pdf).

## 2. Holdout og deduplisering

[belagt: Tools/nodegraph/run_experiment.py:87] Påstanden om at holdout først *leses* etter utvalget er bokstavelig feil: hele substratet lastes, og holdout-parene konstrueres på linje 89, før `build_pool`. [belagt: Tools/nodegraph/run_experiment.py:97] Kandidatene scores likevel bare på train, sorteringen bruker treningsscore og kostnad, og vinnerens første holdout-evaluering kommer på linje 108. [vurdering] Jeg finner ingen direkte tilbakekobling fra holdout-verdier til vinnerutvalget i denne kjøreveien. Tidlig innlasting er en svak tilgangsgrense, men er ikke i seg selv statistisk lekkasje.

[belagt: Tools/nodegraph/run_experiment.py:45] Probe-miljøene tas fra begge armnivåene i de første `n_probes` treningsparene; standarden er tre på linje 143. [belagt: Tools/nodegraph/arena/observable_purpose.py:86] Parene sorteres etter startseed. [belagt: Tools/nodegraph/_cache/substrate_weak.json:1] De tre første treningsseedene er 1000, 1001 og 1002; holdouten ligger på 9000–9023.

[vurdering] Datastyrt deduplisering gjør ikke den faste maksimumsnullen ugyldig her: bytter man lo/hi i en probe, omordnes de samme miljøene for alle kandidatene. Likhetsrelasjonene mellom fingeravtrykkene og filtreringen av nulluttrykk bevares, selv om selve hashverdiene endres. Med samme søkeseed forblir også kostnadsvalg og tilfeldig trimming de samme. Dette argumentet gjelder dagens bruk av begge armnivåer og fraværet av scorefeedback; det gjelder ikke vilkårlige senere brukere av `Proposer.observe`.

[belagt: Tools/nodegraph/search.py:90] Vektorene i probene kuttes til de første 48 elementene. [belagt: Tools/nodegraph/search.py:29] Fingeravtrykkene runder tall til ni signifikante sifre og undersøker ved lengre vektorsvar bare første/siste 32 elementer. [belagt: Tools/nodegraph/search.py:153] En allerede sett kandidat forkastes uten å sammenligne kostnaden med representanten som er beholdt.

[vurdering] Dermed er både «samme funksjon» og «bare den billigste overlever» for sterke beskrivelser. To fullverdier som `[0]*48+[1]` og `[0]*49` ser identiske ut etter probekuttet, men har forskjellig sum. Dette er en søkeheuristikk som kan fjerne nyttige kandidater, ikke bevis for semantisk ekvivalens. Den gir heller ingen identifisert holdout-lekkasje i seg selv.

[belagt: Tools/nodegraph/_cache/substrate_weak.json:1] Den svake armen har 24 komplette train-par på 1000–1023 og 24 komplette holdout-par på 9000–9023, uten dupliserte `(split,start_seed,level)`-nøkler. [belagt: Tools/nodegraph/_cache/substrate_weak_rep.json:1] Replikasjonen har 24 komplette par på 501000–501023, uten overlapp med disse to seedsettene. [vurdering] Dette dokumenterer separate seedidentifikatorer, ikke i seg selv uavhengighet i alle mulige datagenereringsmekanismer.

[belagt: Tools/nodegraph/arena/observable_purpose.py:84] Loaderen overskriver derimot dupliserte nivåoppføringer og utelater ufullstendige par på linje 88; den validerer ikke at splittene er disjunkte. [belagt: Tools/nodegraph/arena/observable_purpose.py:66] En lokal `.json` overstyrer den komprimerte fila. [vurdering] Datakontrollen i denne gjennomgangen fant like JSON-innhold i de tre aktuelle plain/gzip-parene, men koden håndhever ingen slik proveniensgrense for neste kjøring.

[belagt: Tools/nodegraph/_cache/substrate_strong.json:1] Den sterke armen gjenbruker 1000–1007 og 9000–9007 som startseeds. [belagt: Tools/nodegraph/run_experiment.py:154] Den sterke kjøringen, inklusive dens holdout-resultat, utføres og skrives ut før den svake kjøringen ved `--only both`. [vurdering] Dette er en mulig indirekte kanal dersom observasjoner på den sterke holdouten påvirker senere valg av statistikk, kanaler eller søkestrategi for den svake armen. Koden sender ikke den sterke holdout-scoren inn i svakarmens rangering. [usikker] Jeg kan derfor ikke kalle dette påvist seleksjonslekkasje uten historikk over slike valg.

[belagt: Tools/nodegraph/run_experiment.py:211] Programmet beregner også holdout-score for alle håndplukkede baseliner og velger den beste av dem på linje 243. [belagt: Tools/nodegraph/_cache/transform_ladder.json:205] Transformasjonsfila inneholder dessuten en annen søkeseeds vinner målt på både holdout og replikasjon. [vurdering] «Bare én vinner ble målt» beskriver ikke hele den dokumenterte analysen. Diagnostikk etter et fryst primærvalg ugyldiggjør ikke automatisk det opprinnelige primærresultatet, men disse dataene kan ikke samtidig brukes til nye bekreftende valg uten ny korreksjon eller nye data.

[usikker] Jeg kan ikke etablere den menneskelige forhåndsregistreringens tidsrekkefølge fra kodekommentarene og resultatfilene alene. [vurdering] Konklusjonen om renhet må derfor være avgrenset: ingen direkte holdoutavhengighet funnet i dagens `run_arm`-utvalg; flere åpne veier for senere gjenbruk og analysevalg.

## 3. Respons, teststyrke og statistikk-shopping

[vurdering] Her går vurderingen fra én overtolkning til en annen. En monoton transformasjon tilfører ingen informasjon til en allerede observert variabel, men kan gjøre en bestemt test mer effektiv ved å endre hvilke deler av informasjonen testen utnytter. Lik fortegnsvektor beviser likhet for fortegnstesten; det beviser ikke at gevinst for en magnitudebasert test er falsk.

[vurdering] For positive `h` og `l` er `h⁴−l⁴=(h−l)(h+l)(h²+l²)`. β₁⁴ endrer dermed parvektene på en presis måte, ikke bare skalaen med én felles konstant. Om det er hensiktsmessig avhenger av alternativet og støyen. Påstanden om reell *teststyrkegevinst* krever høyere sannsynlighet for korrekt forkastning ved samme kontrollerte falsk-positiv-rate over nye datasett; én større observert score er ikke dette målet.

[belagt: Tools/nodegraph/_cache/transform_ladder.json:21] Replikasjonstallene for β₁ er score 4,261559 og permutasjons-p 0,0001499925. [belagt: Tools/nodegraph/_cache/transform_ladder.json:79] For β₁⁴ er de 4,427515 og 0,0002499875. [belagt: Tools/nodegraph/_cache/transform_ladder.json:195] For hovedvinneren er de 4,943287 og 0,0000499975.

[vurdering] β₁⁴ har altså høyere score, men *høyere* permutasjons-p enn β₁ i replikasjonen. Den egne nullfordelingen flytter seg også. Tallene tilsvarer henholdsvis 2, 4 og 0 overskridelser blant 20 000 permutasjoner, så presis rangering helt ute i halen er dessuten usikker. Ingen av disse p-verdiene tester om kandidaten er bedre enn β₁; de tester hver sin respons mot sin null.

[belagt: Tools/nodegraph/stats.py:68] Ved 24 par velger kvantilregelen element nummer 22 i sorterte absoluttverdier. [vurdering] Uten ties klippes dermed to par strengt, og tre ligger på eller over grensen før klipping. En høyere potens presser ikke automatisk *flere* par til taket; den kan endre hvilke par som klippes og resten av den relative vektfordelingen.

[belagt: Tools/nodegraph/_cache/substrate_weak_rep.json:1] I replikasjonsdataene er de to strengt klippede parene for både β₁ og β₁⁴ seed 501003 og 501005, begge med positiv differanse; begge transformasjonene har tre par på eller over sin grense. [belagt: Tools/nodegraph/_cache/substrate_weak.json:1] På holdout skifter det ene strengt klippede paret fra 9002 til 9004 når β₁ erstattes av β₁⁴; 9005 beholdes, og antallet er fortsatt to. [vurdering] Hypotesen om en winsoriseringseffekt er fortsatt mulig, men forklaringen «flere par mot taket» beskriver ikke det som faktisk skjer her.

[belagt: Tools/nodegraph/library.py:353] `vshift(tokdeg,beta1)` trekker β₁ fra hvert element. [belagt: Tools/nodegraph/library.py:189] `vmin` tar minimum, og `sq` kvadrerer på linje 67. [vurdering] Hovedvinneren er derfor `(β₁−min(tokdeg))⁴` for disse endelige, ikke-tomme inputene. Den bruker en ekstra kanal. [belagt: Documentation/Nodegraf_Vurdering_2026-09-08.md:191] «Alle tre er β₁ i fjerde potens» er bokstavelig galt, selv om samme vurdering senere gir en mer presis formel.

[belagt: Tools/nodegraph/_cache/substrate_weak_rep.json:1] Det eneste fortegnsskiftet mellom β₁ og hovedvinneren i replikasjonen er seed 501017: β₁ går fra 825 til 816, mens `min(tokdeg)` går fra 34 til 1. [vurdering] β₁-differansen er −9, mens den korrigerte grunnstørrelsen går fra 791 til 815 og dermed gir positiv differanse etter fjerdepotensen.

[belagt: Tools/nodegraph/_cache/substrate_weak.json:1] I holdout går seed 9000 fra β₁=753/min=4 til β₁=757/min=17, mens seed 9016 går fra β₁=719/min=20 til β₁=701/min=1. [vurdering] Vinneren taper derfor ett positivt fortegn og vinner ett annet; nettogevinsten er null. [belagt: Tools/nodegraph/_cache/sign_decomposition.json:47] Begge har 20 positive av 24 på holdout og samme fortegnstest-p.

[vurdering] På replikasjonen er den direkte parede sammenligningen én forbedring og null forverringer. En eksakt McNemar-/binomialtest på det ene diskordante paret gir tosidig p=1 og ensidig p=0,5. Dette er den relevante sammenligningen av positive responsrater, forutsatt at positiv retning er valgt på forhånd; se [NISTs definisjon av McNemar-testen](https://itl.nist.gov/div898/software/dataplot/refman1/auxillar/mcnemar.htm). De separate fortegnstestene med p≈0,00028 og p≈0,00154 tester ikke forskjellen mellom observablene.

[vurdering] Formuleringen «den reelle gevinsten er ett par av 24» kan beholdes bare som et deskriptivt nettotall i dette datasettet. Den kan ikke bære en konklusjon om en replikert forbedring. Et positivt fortegn er heller ikke en uavhengig fasit for at ett enkelt stokastisk par er «riktig». Den forsvarlige konklusjonen er: responsen finnes også for β₁; merverdien av den søkte observabelen er uavklart.

[belagt: Tools/nodegraph/replicate.py:82] Spearman-beregningen gir fortløpende, forskjellige ranger også til like verdier, i stedet for midtranker. [belagt: Tools/nodegraph/_cache/substrate_weak_rep.json:1] Replikasjonsdataene inneholder ties i både β₁ og vinnerverdiene. [vurdering] Med midtranker blir korrelasjonen omtrent 0,980617, mot lagret 0,980352. Det endrer ikke avrundingen 0,98 eller hovedinnvendingen, men tallet er beregnet med feil tie-behandling.

[vurdering] For å skille styrke fra shopping ville jeg fryse en liten sammenligning av β₁, β₁⁴ og `(β₁−min(tokdeg))⁴`, og krysse den med forhåndsvalgte klippekvantiler, inklusive ingen winsorisering. Hver variant må få sin egen korrekte null. Hvis variantene skal velges mellom, må dette valget inngå i treningen og maksimumsnullen. På mange nye, uavhengige datasett ville jeg målt både falske positive og forskjell i teststyrke, med paret usikkerhet mellom metodene, samt fulgt hvilke par klippingen endrer. En ablasjon av `min(tokdeg)` skiller kanalbidraget fra potensbidraget. Fortegnstesten er nyttig diagnostikk, men kan ikke avgjøre hele denne sammenligningen alene.

## 4. Konformans og «sertifisert»

[belagt: Tools/nodegraph/compile_c.py:191] Dagens `random_env` trekker også lengdene 4 096 og 20 000; påstanden om at den nå stopper ved 128 ville være feil. Vektorelementene kommer likevel bare fra null eller intervallene [−50,50] og [0,3], mens skalarer kommer fra null, [−50,50] eller [0,10⁶] på linje 196.

[vurdering] Generatoren dekker verken ikke-endelige input, ekstreme eksponenter, systematiske grenseverdier rundt EPS, lange nesten-konstante vektorer eller målrettet kansellering. Den dekker heller ikke vilkårlige komposisjoner eller ressursgrenser ved å øke maksimal tilfeldig lengde til 20 000.

[belagt: Tools/nodegraph/core.py:160] Referansetolken videresender inputverdier til nodene uten global numerisk normalisering. [belagt: Tools/nodegraph/library.py:40] Python-nodene normaliserer NaN og infinities med `_f`; flere C-noder normaliserer bare resultatet eller gjør rå sammenligning. [belagt: Tools/nodegraph/compile_c.py:127] C-kalleren konverterer input til `double` uten å avvise slike verdier.

[vurdering] Følgende er konkrete, kildeutledede divergenser som `random_env` ikke kan trekke. De er ikke rapportert som nykjørte backendtester:

| Uttrykk og input | Python-referanse | C-kode | Grunnlag |
|---|---:|---:|---|
| [vurdering] `add(x,y)`, `x=NaN`, `y=3` | 3 | 0 | [belagt: Tools/nodegraph/library.py:90] Python renser operandene; C renser `a+b`. |
| [vurdering] `min2(x,y)`, `x=NaN`, `y=3` | 0 | 3 | [belagt: Tools/nodegraph/library.py:112] C bruker `a<b?a:b` på rå input. |
| [vurdering] `gt(x,y)`, `x=+inf`, `y=1` | false | true | [belagt: Tools/nodegraph/library.py:414] Python sammenligner `_f(a)` og `_f(b)`; C sammenligner direkte. |
| [vurdering] `mean(v)`, `v=[+inf,2]` | 1 | 0 | [belagt: Tools/nodegraph/library.py:149] Python renser hvert element; C renser den akkumulerte summen før middelberegningen på linje 156. |

[vurdering] En eksplisitt, håndhevet kontrakt om bare endelige input kunne avgrense bort disse tilfellene. Dagens grensesnitt og totalitetsformulering gir ikke den avgrensningen. Innenfor endelige tall bør prøvesettet også inneholde `±1e308`, `±5e-324`, `0.999999999999e-12`, `1e-12`, `1.000000000001e-12`, kansellerende `[1e16,1,−1e16]` og lange konstante/nesten-konstante vektorer. Disse er foreslåtte prøver, ikke påstander om at hvert eksempel gir avvik i dagens maskinmiljø.

[belagt: Tools/nodegraph/tests/test_nodegraph.py:109] Vektorutdata i nodetesten reduseres til `sum + count + std`. [vurdering] Denne kontrollen er blind for permutasjon av elementene. For `sortdesc([1,2,3])` ville en feilaktig identitetsimplementasjon bestå aggregatkontrollen, selv om referansen returnerer `[3,2,1]`. Den etterfølgende grafen `corr(sortdesc(v),w)` med `v=w=[1,2,3]` ville derimot skille dem: −1 for referansen og +1 for den tenkte feilimplementasjonen. At vektornoder bare kan kontrolleres via skalaraggregater er en konkret svakhet ved denne harnessen, ikke et bevis for at dagens `sortdesc` har denne feilen.

[belagt: Tools/nodegraph/compile_c.py:213] Feilkontrollen er bare `err > tol`; den krever ikke at referanse, resultat og feil er endelige. [vurdering] En backend som returnerer NaN kan derfor unnslippe denne sammenligningen, fordi NaN ikke er større enn toleransen. [belagt: Tools/nodegraph/compile_c.py:137] Den ordinære `CompiledC`-wrapperen reiser riktignok unntak ved NaN, men klassifiserer alle slike resultater som `ArenaTooSmall`. [vurdering] Harnessen og wrapperen må vurderes separat; dette er ikke belegg for at vanlig C-kalling ubemerket godtar alle NaN-resultater.

[belagt: Tools/nodegraph/tests/test_nodegraph.py:118] Den sjekkede nodetesten bruker nå 90 tilfeldige forsøk per node, ikke 250. [belagt: Tools/nodegraph/tests/test_nodegraph.py:159] Ekstremverdiprøven bruker `[1e308,−1e308]`, men evaluerer bare referansetolken. [belagt: Tools/nodegraph/tests/test_nodegraph.py:273] Det finnes også målrettede C-regresjoner for en lang pipeline og utsultet arena. [vurdering] De siste er verdifulle, men underbygger ikke generell ekvivalens. En historisk 250-prøvekjøring kan ha eksistert; dagens testsuite alene reproduserer ikke det oppgitte sertifikatet.

[vurdering] Ordet bør være «bestått den spesifiserte konformansprøven», med inputdomene, backend- og kompilatoridentitet, toleranser og ressursgrenser. «Sertifisert» uten dette gjør et endelig utvalg av forsøk til en garanti det ikke kan gi.

## 5. Den positive referansen

[belagt: Tools/nodegraph/_cache/experiment.json:93] Den sterke referansen har åtte par, søkenull 37,176075 og vinner `n` med score 50 på både train og holdout. [belagt: Tools/nodegraph/_cache/experiment.json:168] Den svake kjøringen har 24 par og søkenull 5,051415. [belagt: Tools/nodegraph/run_experiment.py:190] Admissibilitetskontrakten kombinerer den svake nullen med den sterke vinnerens treningsscore.

[vurdering] «Separasjon 9,9» er derfor `50/5,051415`, ikke en konservativ sammenligning mot den sterke nullen. [belagt: Tools/nodegraph/run_experiment.py:204] Kommentaren som begrunner konservativitet med at den sterke nullen er høyest, beskriver motsatt valg av nevner fra det koden faktisk gjør.

[vurdering] Brukes den sterke kjøringens egen null, blir forholdet `50/37,176075 ≈ 1,345`, under kontraktens krav på 2. Med scoretaket 50 kan ingen kandidat i akkurat denne kalibreringen nå et forhold på 2. Det viser en uforenlighet mellom scoretaket, den målte referansen og forholdsporten; det viser ikke at den sterke armen mangler respons. Å bytte inn en lavere null fra en annen oppstilling løser ikke kalibreringsproblemet.

[vurdering] Taktreffet er informativt om at instrumentet reagerer på en stor kontrast, men sensurerer hvor langt over 50 den ukappede statistikken ligger, variasjonen mellom sterke kandidater og følsomheten nær relevant effektstørrelse. Dessuten gjelder referansen en annen observabel og en annen regelendring. Den etablerer ikke følsomheten til svakarmens vinner overfor små endringer i `p_local_rewire`.

[belagt: Tools/nodegraph/stats.py:57] Statistikken avhenger eksplisitt av √n og har et fast additivt EPS-ledd. [vurdering] Skårer og skårforhold er derfor ikke en felles, direkte kalibreringsskala på tvers av n, transformasjoner og kandidatmengder. At en annen arm med færre par likevel treffer 50 kan være en god røykprøve, men kan ikke gi det rapporterte forholdet betydningen «instrumentet er kalibrert».

[vurdering] Det som burde vært målt, er en respons- og styrkekurve med samme parantall, hendelsesbudsjett, søkebudsjett og datamekanisme som målet: nullkontrast og flere kjente, små til store positive kontroller. Nullkontrollen må bruke separate hendelsesstrømmer, slik at den ikke bare produserer identiske kopier og trivielle nulldifferanser. Rapporter rå differanser, klippede differanser, middel/standardavvik, ukappet score, andel taktreff og forkastningsrater på uavhengige testsett, med usikkerhet. Positive kontroller bør både kontrollere hele søkeprosedyren og den fryste observabelen.

## 6. Portene i del 7

[belagt: Documentation/Nodegraf_Vurdering_2026-09-08.md:350] Den sjekkede vurderingen har fem porter, ikke fire; transformasjonsporten er nummer 4 og den eksterne formålskontrakten nummer 5. [vurdering] Jeg svarer på den versjonen som faktisk ligger i repoet.

[vurdering] **Den manglende porten er kalibrert merverdi for hele beslutningsprosedyren.** Før mer søkeinvestering bør en fryst prosedyre vise at falsk-positiv-raten holder avtalt nivå på uavhengige nullbatcher, og at styrke eller bruksnytte forbedres over en forhåndsvalgt β₁-baseline på uavhengige positive batcher. En konkret port kan kreve øvre ensidig 95 % konfidensgrense for nullforkastning ≤0,05 og nedre grense for forbedringen større enn en forhåndsdefinert praktisk margin. Antall batcher må bestemmes før kjøring. Søkevalg, transformasjonsvalg og eventuelle modellforslag må alle være innenfor det som fryses og kalibreres.

[vurdering] **Jeg ville strøket port 2, Spearman <0,9 som krav til et funn.** Korrelasjonsavstand er verken ny informasjon, bedre måling eller nytte. Den belønner også at man blander inn støy. Motsatt kan et nyttig korreksjonsledd ha korrelasjon over 0,9 med baselinen. [belagt: Documentation/Nodegraf_Vurdering_2026-09-08.md:355] Porten er dessuten skrevet som en fortegnsbestemt øvre grense. [vurdering] Lest bokstavelig består `neg(beta1)` med Spearman −1, selv om den bare snur fortegnet og har identisk absolutt responsstatistikk. Selv `abs(rho)<0,9` ville ikke løst det grunnleggende nytteproblemet.

[vurdering] Port 1 bør kreve en definert bruksflate og de målrettede semantikkprøvene fra punkt 4, ikke kopiere tallet «250 tilfeldige input». Port 3 kan være en fornuftig sammenligning av forslagsstillere, men må måle samlet kostnad og bekreftet resultat på fryste, nye testsett; gjentatt optimalisering av «holdout-score per krone» ville gjøre holdouten til trening. Port 5 kan måle overførbarhet, men erstatter verken nullkalibrering eller merverdiprøven.

[belagt: Documentation/Nodegraf_Vurdering_2026-09-08.md:362] Port 4 sier både at begge tester må forbedres, og at rettelsen er gjennomført. [belagt: Tools/nodegraph/purpose.py:129] Implementasjonen beregner valgfritt to p-verdier, men sammenligner dem ikke; `transform_only` på linje 138 tester bare identisk fortegnsvektor. [belagt: Tools/nodegraph/purpose.py:147] PASS-feltene bruker bare skårene og én felles terskel, uten å ta hensyn til `transform_only` eller invariant-p.

[vurdering] En annen, men dårligere fortegnsvektor får derfor `transform_only=False`. Også en ren global fortegnsvending kan få False, selv om den tosidige fortegnstesten og den absolutte scoren er uendret. Identisk vektor er heller ikke bevis for at to funksjoner er monotone omskrivninger; mange forskjellige funksjoner kan tilfeldigvis gi samme 24 fortegn. Feltet kan være en beskrivelse av dette datasettet, men er ikke den annonserte forbedringsporten.

[belagt: Tools/nodegraph/run_experiment.py:178] Hovedeksperimentet oppretter kontrakten uten `invariant` og `reference_graph`, med konstante nullfunksjoner for `score` og `holdout`; det kaller bare `admissibility()` på linje 209. [belagt: Tools/nodegraph/run_experiment.py:129] Resultatets PASS-felt beregnes separat inne i `run_arm`. [vurdering] Den nye mekanismen er altså ikke koblet inn i denne resultatløypa. Generalkontraktens ene terskel implementerer heller ikke eksperimentets skille mellom maksimumsnull for utvalg og vinneregen null for holdout.

[vurdering] Port 4 bør omskrives til rapportering av både retning og størrelse, med direkte, forhåndsdefinert sammenligning mot baseline. Jeg ville ikke krevd at enhver nyttig forbedring må endre fortegn: det ville på forhånd utelukke reelle styrkegevinster som skyldes bedre utnyttelse av magnituder. Det avgjørende er dokumentert forbedring ved kontrollert feilrate, ikke at en kandidat må tilfredsstille en bestemt fortelling om nyhet.

## Hva jeg ville gjort annerledes

- [vurdering] Beholdt fortegnsalgebraen, men skrevet eksplisitt hvilken nullhypotese og utbyttbarhet den trenger.
- [vurdering] Fryst data, søkevalg, statistikk, baseline og beslutningskode før neste bekreftende kjøring.
- [vurdering] Flyttet holdout bak en kontrollert evalueringsgrense og validert seedoverlapp, par og datahash.
- [vurdering] Målt hele prosedyren på uavhengige nullbatcher og relevante positive kontroller med samme n.
- [vurdering] Erstattet forholdet 50/5,05 med matchede kalibreringskurver og synliggjort taksensureringen.
- [vurdering] Skilt ekstra kanal, potens og winsorisering med en liten fryst ablasjon.
- [vurdering] Målt direkte merverdi over β₁ med usikkerhet; omtalt 21 mot 20 som foreløpig deskriptivt.
- [vurdering] Strøket Spearman-porten og omskrevet fortegnsporten til en etterprøvbar sammenligning.
- [vurdering] Krevd målrettede numeriske, komposisjonelle og ressursmessige konformansprøver før en ny backend.
- [vurdering] Kalt resultatet respons på nye seeds med uavklart merverdi, og backendstatus bestått avgrenset prøve.

FERDIG-MARKØR-ASTRA
