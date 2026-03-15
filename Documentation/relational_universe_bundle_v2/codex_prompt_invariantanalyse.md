# Codex-prompt: invariantanalyse og nullrom

Kopier teksten under og gi den til Codex eller en annen kodeassistent.

---

Du skal implementere en liten matematisk modul for lineær invariantanalyse i en relasjonell universgraf.

## Mål

Implementer et verktøy som, gitt et valgt feature-sett og en samling regler med eksplisitte \(\Delta F\)-vektorer, finner alle lineære invariants.

## Kontekst

Vi arbeider med features som minst inkluderer:

- \(K\): antall tokens
- \(N\): antall noder
- \(M\): antall kanter
- \(C\): antall komponenter
- \(\beta_1 = M-N+C\)

Regler representeres ved endringsvektorer, f.eks.:

- seed-attach
- triadic closure
- nonbridge-delete
- bridge-delete
- leaf-delete-plus-prune
- edge-swap
- token birth/death

## Konkrete oppgaver

1. Representer hver regel som en feature-delta-vektor.
2. Bygg en matrise der hver rad eller kolonne representerer en regel.
3. Finn nullrommet til regelmatrisen.
4. Returner invariantene i lesbar form.
5. Lag en liten CLI eller demonstrasjon som viser resultatet for minst tre regelklasser:
   - topologisk sektor,
   - sektor med fri cycle creation,
   - åpent tokensystem.

## Krav

- ren Python er foretrukket,
- type hints,
- forklarende docstrings,
- enhetstester for minst to kjente tilfeller.

## Faglig viktig

Forklar i svaret ditt forskjellen mellom:

- eksakte invariants,
- quasi-invariants,
- invariants som bare gjelder i et sammenhengende regime.

## Format på svaret

1. Kort matematisk forklaring
2. Kode
3. Testeksempler
4. Tolkning av resultatene
