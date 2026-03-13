# UniverseSimulation Corpus Plan

Dette dokumentet beskriver hvordan korpuset er delt opp i `source_type`-er og cases.

## Source types

### `universe_status`

Brukes for dokumenter som beskriver faktisk prosjektstatus og modenhet.

Anbefalte filer:

- `../README.md`
- `docs/UNIVERSE_RAG_STATUS.md`
- eventuelle fremtidige statusnotater eller milepaelsoppdateringer

### `universe_tools`

Brukes for dokumenter om simulatorbruk, RAG-drift og arbeidsflyt.

Anbefalte filer:

- `docs/UNIVERSE_TOOL_RUNBOOK.md`
- `docs/RAG_SERVICE_API.md`
- eventuelle fremtidige runbooks for sweep, plotting eller analyse

### `universe_argumentation`

Brukes for teori, ontologi, testprogram og argumentkart.

Anbefalte filer:

- `../Documentation/grundig-research-rapport-16.md`
- `docs/UNIVERSE_ARGUMENTATION_MAP.md`

### `universe_prompts`

Brukes for promptprofiler, modelleringsregler og instruksjonsmaler.

Anbefalte filer:

- hele `prompts/`
- `docs/UNIVERSE_DEEP_RESEARCH_PROMPT.md`

## Cases

### `universe_project`

Samlet case for generelle prosjektsporsmal.

Source types:

- `universe_status`
- `universe_tools`
- `universe_argumentation`
- `universe_prompts`

### `universe_tools`

Smalere case for simulator, metrics og RAG-arbeidsflyt.

Source types:

- `universe_status`
- `universe_tools`

### `universe_argumentation`

Smalere case for teori, ontologi og testbar argumentasjon.

Source types:

- `universe_argumentation`
- `universe_status`

### `universe_prompts`

Smalere case for promptdesign og modellregler.

Source types:

- `universe_prompts`
- `universe_status`
- `universe_argumentation`
- `universe_tools`

## Hvorfor denne delingen

Prosjektet trenger tydelig separasjon mellom:

- teori
- faktisk kode og toolbruk
- status
- instruksjoner til modeller

Hvis alt blandes i ett udifferensiert korpus, oker risikoen for at modellen:

- overdriver hva simulatoren faktisk kan bevise
- blander promptmaler med prosjektfakta
- svarer med teori nar brukeren egentlig spurte om verktøy

## Anbefalt synk-rekkefolge

Fra `rag_service/`:

```bash
python -m scripts.sync_folder --path ../Documentation/grundig-research-rapport-16.md --source-type universe_argumentation --ingest-root ..
python -m scripts.sync_folder --path ../README.md --source-type universe_status --ingest-root ..
python -m scripts.sync_folder --path docs/UNIVERSE_RAG_STATUS.md --source-type universe_status --ingest-root ..
python -m scripts.sync_folder --path docs/UNIVERSE_TOOL_RUNBOOK.md --source-type universe_tools --ingest-root ..
python -m scripts.sync_folder --path docs/RAG_SERVICE_API.md --source-type universe_tools --ingest-root ..
python -m scripts.sync_folder --path docs/UNIVERSE_ARGUMENTATION_MAP.md --source-type universe_argumentation --ingest-root ..
python -m scripts.sync_folder --path prompts --source-type universe_prompts --ingest-root ..
```

## Kvalitetsregel for nye dokumenter

Nye dokumenter bor skrives slik at de tydelig sier:

- om de beskriver faktisk kode eller bare foreslatt retning
- hvilke filer eller kjoredata de bygger pa
- hva som fortsatt er usikkert
