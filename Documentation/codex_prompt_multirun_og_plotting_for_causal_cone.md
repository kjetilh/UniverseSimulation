# Codex-prompt – multirun-statistikk og plott for emergent causal cone

Arbeid på `relational_universe_perturbation_lab.py` og tilhørende analysefiler.

## Mål
Gjør den nåværende perturbasjonslaben om fra enkeltrun-verktøy til statistisk laboratorium.

## Oppgaver
1. Implementer en batch-runner som tar:
   - liste over seeds
   - liste over regimer
   - liste over perturbasjonstyper
   - felles parameterfil eller CLI-argumenter

2. For hver batch skal du beregne:
   - middel og standardavvik for final_radius_control
   - middel og standardavvik for max_radius_control
   - middel og standardavvik for fit_speed_control
   - middel og standardavvik for final_core_L1
   - middel og standardavvik for final_regime_L1
   - middel og standardavvik for final_delta_beta1

3. Lag plott:
   - gjennomsnittlig radius_control(t) med feilbånd
   - edge_diff_count(t) med feilbånd
   - regime_L1(t) med feilbånd
   - sammenlikning mellom `local_swap` og `add_chord`

4. Lag en markdown-rapport som eksplisitt svarer på:
   - finnes det et robust tegn på en begrenset causal cone?
   - varierer front-hastigheten sterkt mellom regimer?
   - peker dataene mot en universell eller ikke-universell effektiv hastighet?

## Viktig
- Lag kode som er lesbar og modulær.
- Kommenter tydelig hva som er deskriptiv statistikk og hva som er teoretisk tolkning.
- Ikke bruk seaborn; bruk matplotlib.
