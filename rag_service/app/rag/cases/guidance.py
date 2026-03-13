from __future__ import annotations

import re
from typing import Any


_PROMPT_KEYWORDS = {
    "prompt",
    "prompts",
    "persona",
    "template",
    "mal",
    "instruksjon",
    "instruksjoner",
    "llm",
    "modell",
}

_PROMPT_PHRASES = (
    "system prompt",
    "system persona",
    "answer template",
    "hvordan instruere modellen",
    "hvordan bor modellen svare",
    "hvilken promptprofil",
)


def case_quick_actions(case_id: str) -> list[dict[str, str]]:
    if case_id == "universe_project":
        return [
            {
                "label": "Prosjektstatus",
                "description": "Oppsummer hvor prosjektet er na og hva som mangler.",
                "prompt": "Hvor er prosjektet na, og hva er hovedgapet mellom rapporten og simulatoren?",
            },
            {
                "label": "Neste steg",
                "description": "Foresla de næreste, mest realistiske neste stegene.",
                "prompt": "Hva er de viktigste neste stegene hvis vi vil ga fra dagens toy-simulator til mer presise hypotesetester?",
            },
            {
                "label": "Rapport vs kode",
                "description": "Skill tydelig mellom matematisk ramme og implementert kode.",
                "prompt": "Hva i rapporten er formelt spesifisert, og hva er bare approximert i dagens kode?",
            },
        ]
    if case_id == "universe_tools":
        return [
            {
                "label": "Kjor simulator",
                "description": "Vis hvordan simuleringen startes og hvilke parametere som er viktige.",
                "prompt": "Hvordan kjorer jeg dagens simulator, og hvilke parametere bor jeg justere for a se runaway densifisering eller mer stabil vekst?",
            },
            {
                "label": "Les trajectory",
                "description": "Forklar hva kolonnene i trajectory.csv forteller.",
                "prompt": "Hvordan skal jeg tolke nodes, edges, avg_degree, clustering og eff_dim i trajectory.csv?",
            },
            {
                "label": "Synk korpus",
                "description": "Forklar hvordan prosjektfilene synkes inn i RAG-en uten a flyttes.",
                "prompt": "Hvordan bor jeg bruke sync_folder for a laste inn rapport, statusdokumenter og prompts i denne RAG-en uten a flytte kildefilene?",
            },
        ]
    if case_id == "universe_argumentation":
        return [
            {
                "label": "Primitive antagelser",
                "description": "Vis hva prosjektet tar som primitive byggesteiner.",
                "prompt": "Hva er de primitive antagelsene i rapporten, og hvorfor er de valgt sa minimalt som mulig?",
            },
            {
                "label": "Energi og invariants",
                "description": "Forklar hvordan energi og bevaring er formulert.",
                "prompt": "Hvordan begrunner rapporten energi som aktivitetsrate, Noether-lignende ladninger og monsterenergi?",
            },
            {
                "label": "Lorentz-test",
                "description": "Vis hvordan rapporten foreslar a teste Lorentz-likhet.",
                "prompt": "Hva er rapportens testprogram for Lorentz-likhet, universell c_* og observator-malbare diagnostikker?",
            },
        ]
    if case_id == "universe_prompts":
        return [
            {
                "label": "Systemprompt",
                "description": "Lag eller revider systeminstruksjoner for prosjektassistenten.",
                "prompt": "Hvilke systeminstruksjoner bor en modell fa for a arbeide korrekt med UniverseSimulation-korpuset?",
            },
            {
                "label": "Evidensskille",
                "description": "Tving modellen til a skille rapport, kode, data og inferens.",
                "prompt": "Hvordan bor vi instruere modellen til a skille mellom rapporten, dagens kode, trajectory-data og egen inferens?",
            },
            {
                "label": "Tool prompts",
                "description": "Velg riktig promptprofil for verktøysporsmal.",
                "prompt": "Hvilken promptprofil passer best for spørsmål om bruk av simulatoren og RAG-verktøyene, og hvorfor?",
            },
        ]
    return []


def case_guidance(case_id: str) -> dict[str, Any]:
    if case_id == "universe_project":
        return {
            "intended_for": "Generell prosjektassistanse der man trenger bade status, teori, verktøybruk og videre retning.",
            "use_when": "Bruk dette caset for overblikk, gap-analyse og tverrgaende sporsmal om prosjektets retning.",
            "avoid_when": "Unnga dette hvis du bare vil ha ren promptdesign eller bare vil ha den teoretiske argumentasjonen isolert.",
            "preferred_alternative_case_id": "universe_argumentation",
            "quick_actions": case_quick_actions(case_id),
        }
    if case_id == "universe_tools":
        return {
            "intended_for": "Arbeid med simulator, trajectory-data, ingest/sync og praktisk bruk av verktøyene.",
            "use_when": "Bruk dette caset for kjoring, parametere, outputtolkning og RAG-drift.",
            "avoid_when": "Unnga dette for ren teori- eller promptutforming.",
            "preferred_alternative_case_id": "universe_prompts",
            "quick_actions": case_quick_actions(case_id),
        }
    if case_id == "universe_argumentation":
        return {
            "intended_for": "Diskusjoner om ontologi, argumentasjon, regelsett, invariants og testbare konsekvenser.",
            "use_when": "Bruk dette caset for rapportforankret teoriarbeid og vurdering av hva som faktisk er begrunnet.",
            "avoid_when": "Unnga dette for ren verktoybruk eller prompt-engineering.",
            "preferred_alternative_case_id": "universe_tools",
            "quick_actions": case_quick_actions(case_id),
        }
    if case_id == "universe_prompts":
        return {
            "intended_for": "Utforming av systemprompts, answer templates og modellregler for prosjektet.",
            "use_when": "Bruk dette caset for promptprofiler, modellinstruksjoner og arbeidsregler for LM-er.",
            "avoid_when": "Unnga dette hvis du egentlig trenger konkret simulatorbruk eller ren teorianalyse.",
            "preferred_alternative_case_id": "universe_tools",
            "quick_actions": case_quick_actions(case_id),
        }
    return {}


def looks_like_composition_question(message: str | None) -> bool:
    text = (message or "").strip().lower()
    if not text:
        return False
    if any(phrase in text for phrase in _PROMPT_PHRASES):
        return True
    tokens = re.findall(r"\w+", text)
    hits = sum(1 for token in tokens if token in _PROMPT_KEYWORDS)
    return hits >= 2


def query_case_guidance(case_id: str | None, message: str | None) -> dict[str, Any] | None:
    if case_id == "universe_prompts":
        return None
    if not looks_like_composition_question(message):
        return None
    return {
        "level": "info",
        "message": "Dette spørsmålet ser ut som prompt- eller modellinstruksjonsarbeid. Bruk `universe_prompts` for systemregler, personas og svarmaler.",
        "suggested_case_id": "universe_prompts",
    }
