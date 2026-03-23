# v0.12m operativ anbefaling

Behold `full_followup` som referanse under fast `full_basis@0.50` screening.
Bruk `probe2_top_half` som baseline for adaptiv kvalitet/tid fra v12k-v12l: `speedup=1.506`, `best_hit=0.613`, `recall=0.613`.
Beste dypere utfordrer i denne runden er `probe3_top_half`, med `speedup=1.358`, `best_hit=0.669` og `recall=0.669`.
Les `probe3_top_half` som den første seriøse adaptive utfordreren: den matcher referansen på mean hit/recall og er fortsatt raskere. Det som gjenstår å avklare er om den lille pairwise-svikten er akseptabel eller kan rettes med en smartere beslutningsregel.
Neste smale steg bør derfor være en valideringsrunde som bare sammenligner `full_followup` mot `probe3_top_half`, og eventuelt en liten variant med bedre tie-break eller forlengelsesregel.
