# v0.9b – toppkandidater og lokal refinering

## Hovedrangering i v0.9b

| candidate | r_birth | r_death | p_swap | p_triad | p_del | mean composite | CI low | alpha_large | alpha_jump | linear margin | asym score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| band_best | 0.02 | 0.00 | 0.02 | 0.00 | 0.01 | 0.623 | 0.568 | 0.303 | 0.025 | 0.059 | 0.810 |
| macro_stable | 0.02 | 0.05 | 0.02 | 0.00 | 0.01 | 0.608 | 0.598 | 0.237 | 0.263 | 0.007 | 0.689 |
| triad_runner | 0.02 | 0.02 | 0.02 | 0.02 | 0.00 | 0.520 | 0.541 | 0.898 | 0.373 | -0.092 | 0.446 |
| balanced_pdel | 0.02 | 0.02 | 0.02 | 0.00 | 0.01 | 0.644 | 0.614 | 1.266 | 0.742 | -0.103 | 0.333 |

## Hva som er mest interessant

- `band_best` blir beste asymptotiske kandidat.
- `macro_stable` er en respektabel kontrollkandidat.
- `balanced_pdel` svekkes kraftig når finite-size-artefakter måles direkte.

## Refineringsrunde

| candidate | refine seeds | mean composite | CI low | alpha_large | alpha_jump | linear_margin | burn-in sens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| band_best | 101,202,303 | 0.591 | 0.558 | 0.141 | -0.082 | 0.111 | 0.155 |
| macro_stable | 101,202,303 | 0.604 | 0.576 | 0.406 | 0.287 | -0.038 | 0.222 |

## Kort konklusjon

Hvis man bare så på tidligere gjennomsnittsskårer, ville man lett overvurdere `balanced_pdel`.
Hvis man ser på asymptotiske indikatorer, peker dataene tydeligere mot `band_best`.
