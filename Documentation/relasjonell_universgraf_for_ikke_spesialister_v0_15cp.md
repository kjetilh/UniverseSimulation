# Relasjonell universgraf for ikke-spesialister v0.15cp

Denne runden sjekker om target-1024 feilet i forrige p2-test bare fordi den fikk for lite tid.

- Hovedresultat: `scaled_budget_p2_not_supported`.
- Kontrollstatus: `clean`.
- Budsjett: `scaled_from_target768`.

Hvis p2 kommer tilbake med mer tid, er 1024-negativen fra forrige runde mindre alvorlig.
Hvis p2 fortsatt ikke kommer tilbake, blir det mer sannsynlig at p2-lommen er lokal for 768 eller trenger en annen skalaovergang.

- Neste steg: `intermediate_scale_or_retire_p2_as_scale_selector` fordi Neste steg bor enten teste ett mellomtarget eller nedgradere p2 som skala-selector.
