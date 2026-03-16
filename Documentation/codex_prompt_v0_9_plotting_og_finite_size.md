# Codex-prompt: plotting, finite-size og bootstrap-diagnostikk for v0.9

Oppgave:
Lag en analysemodule som leser `v09_scale_group_rows.csv` og `v09_scale_candidate_summary.csv` og produserer:

1. plott av composite-score mot initial størrelse,
2. plott av radius mot størrelse både lineært og log-log,
3. plott av overlap og quasi-score mot log størrelse,
4. en markdown-rapport som forklarer hvilke figurer som støtter eller svekker hypotesen om sublineær skadeutbredelse.

Krav:
- bruk matplotlib, ikke seaborn,
- ett plot per figur,
- ingen spesifikk fargestil,
- lagre alle figurer til filer,
- skriv en kort tolkning per figur i markdown.
