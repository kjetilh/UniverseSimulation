# Relasjonell universgraf for ikke-spesialister v0.15cn

Denne runden sjekker om det lille p2-monsteret ved storrelse 768 ogsaa finnes naar vi oker storrelsen til 1024.

- Hovedresultat: `target768_specific_under_current_budget`.
- Kontrollstatus: `clean`.
- Budsjett-scope: `same_absolute_budget`.

Hvis signalet holder, er det mer interessant enn et rent target-768-uhell.
Hvis det ikke holder, kan det enten vaere ekte skala-brudd eller bare at den storre grafen trenger mer tid.

- Neste steg: `target1024_budget_extension_or_intermediate_scale` fordi Neste steg bor teste om 1024 trenger lengre budsjett, eller om et mellomtarget bryter overgangen.
