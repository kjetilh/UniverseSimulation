# Operativ anbefaling etter v16z

Formal status: `v16z_cycle_representation_not_qualified`.

Post-run edge-move-kovarians passerte `6/6`; den formelle feilen kom fra direkte
sammenligning av `SlotClass`-nokler som endres under semantisk relabeling. Den
formelle gaten omskrives ikke.

Neste gate er en effect-blind, state-independent alternerende-syklusproposal med
eksplisitt forward/reverse proposal-sannsynlighet og lazy Metropolis-korreksjon.
Kvalifiser proposal og ressursbruk foer en ny sampler- eller mixingrunde. Ikke
doble dagens target-directed 2x2-sok, ikke kall `0/6` bevis for disconnection,
og ikke aapne v16s-spektrumet.
