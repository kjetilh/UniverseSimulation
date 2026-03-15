# Codex-prompt: bruk og tolkning av v0.6 uniformized coupling lab

Du skal arbeide videre på prosjektet "relasjonell universgraf" i filen `relational_universe_uniformized_coupling_lab.py`.

## Kontekst
Modellen forsøker å undersøke om et univers kan beskrives som en dynamisk graf med:
- noder
- én relasjonstype
- lokale units of action
- emergent tid, geometri og kausal struktur

v0.6 introduserer en familywise uniformized coupling mellom to nesten identiske replikater:
- en kontrollgren
- en perturbert gren

Poenget er å kunne sammenligne dem også i åpne regimer der token-antall og totalrate kan divergere.

## Oppgave
1. Les koden og identifiser:
   - family-ratene
   - den dominerende family-klokken
   - thinning-regelen
   - de lokale koblingsmekanismene innen hver familie

2. Forklar eksplisitt:
   - hva som er eksakt i denne koblingen
   - hva som bare er en praktisk eller heuristisk kobling
   - hva som måles av `radius_control`, `delta_tokens`, `core_l1`, `regime_l1`,
     `both_accept_total` og `one_sided_total`

3. Kjør minst to representative regimer:
   - et moderat token-open regime
   - et moderat full-open regime

4. Lag:
   - én CSV med rå resultater
   - én Markdown-oppsummering
   - én kort layman-oppsummering

## Viktig
- Ikke endre ontologien: én relasjonstype, ingen skjult bakgrunn.
- Ikke innfør nye primitive objekter uten å forklare hvorfor.
- Skill tydelig mellom:
  - mathematically exact marginal correctness
  - coupling quality
  - fysisk tolkning

## Leveranse
Gi:
- forbedret kode hvis du finner feil eller svakheter
- en tydelig vurdering av om dette regimet er en god kandidat for videre spacetime-testing
- forslag til neste eksperiment
