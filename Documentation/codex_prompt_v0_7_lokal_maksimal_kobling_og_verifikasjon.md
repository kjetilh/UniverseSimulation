# Codex-prompt: v0.7 lokal maksimal kobling og verifikasjon

Du arbeider i et forskningsrepo for en relasjonell universgraf. Les først:

- `relational_universe_local_max_coupling_lab.py`
- `relasjonell_universgraf_v0_7_lokal_maksimal_kobling_og_repair.md`
- `v07_bd_closed_swap_multirun_summary.md`

## Mål
Forbedre og verifisere v0.7-laben uten å bryte den matematiske strukturen.

## Krav
1. Behold familywise uniformization.
2. Behold skillet mellom:
   - familywise akseptkobling,
   - lokal kobling av endelige kjerner,
   - og full tilstandslikhet.
3. Ikke innfør globale admissibility-tester eller ikke-lokale regler.

## Oppgaver
1. Refaktorer lokale kjerner slik at hver familie har:
   - `kernel(state, params) -> dict[descriptor, prob]`
   - `apply_descriptor(state, descriptor, manager, params)`
2. Legg til sanity checks:
   - sannsynlighetene summerer til 1,
   - maksimal kobling gir korrekt overlap-sannsynlighet,
   - identiske tilstander er absorberende under maksimal kobling.
3. Legg til marginaltester:
   - sammenlign empiriske family frequencies mot teoretiske familie-rater,
   - sammenlign descriptor-frekvenser mot lokal kernel.
4. Legg til en testpakke som rapporterer:
   - `local_overlap_prob`,
   - `same_descriptor_rate`,
   - `meeting_fraction`,
   - `shared_token_fraction_final`.

## Viktig tolkning
Skriv tydelig hva som er:
- eksakt,
- numerisk verifisert,
- og fortsatt heuristisk.

## Leveranser
- oppdatert Python-kode,
- Markdown-notat med testresultater,
- kommandoeksempler i Markdown.