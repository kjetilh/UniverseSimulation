# Feature Lab: Algebraic vs Dynamic Structure

Dette er den korte metodiske avgrensningen som bør følge all bruk av feature-labben.

## Rent algebraiske deler

Disse følger av definisjonene og er ikke dynamiske funn:

- `beta1 = edges - nodes + components`
- `deg_sq_sum = 2*wedges + 2*edges`

Konsekvens:
- dersom en SVD-kandidat hovedsakelig ligger i dette delrommet, er det ikke en ny bevaringslov
- i redusert basis fjernes derfor `beta1` og `deg_sq_sum`

## Dynamiske deler

Disse bestemmes av reglene og parameterregimet:

- om `tokens` faktisk bevares
- om `nodes` og `edges` vokser eller ikke
- om `components` holder seg konstant eller fragmenterer
- om triangler, `c4`, `clustering` og `dim_proxy` stabiliserer seg eller driver

Dette er de delene som kan gi ekte invariants eller quasi-invarianter.

## Viktig tommelfingerregel

Hvis en kandidat:
- ser sterk ut i rå analyse
- men forsvinner i standardisert analyse

da er den sannsynligvis skala-dominert, ikke fysisk robust.

Hvis en kandidat:
- overlever både rå og standardisert analyse
- og ikke ligger i identitetssektoren

da er den interessant som mulig quasi-invariant.
