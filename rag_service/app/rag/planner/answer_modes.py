from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class AnswerModePlan:
    answer_mode: str
    source_strategy: str
    response_shape: str
    streaming_allowed: bool
    rewrite_query: bool
    use_subquery_planner: bool
    default_prompt_case_id: str | None = None
    question_set_path: str | None = None
    answer_contract: str | None = None
    planner_focus: str | None = None
    detail_level: str = "standard"
    retrieval_hint: str | None = None

    def as_trace(self) -> dict[str, object]:
        return {
            "answer_mode": self.answer_mode,
            "source_strategy": self.source_strategy,
            "response_shape": self.response_shape,
            "streaming_allowed": self.streaming_allowed,
            "rewrite_query": self.rewrite_query,
            "use_subquery_planner": self.use_subquery_planner,
            "default_prompt_case_id": self.default_prompt_case_id,
            "question_set_path": self.question_set_path,
            "detail_level": self.detail_level,
            "retrieval_hint": self.retrieval_hint,
        }


def _contains_any(message_lc: str, patterns: Iterable[str]) -> bool:
    return any(pattern in message_lc for pattern in patterns)


def _word_hits(message_lc: str, patterns: Iterable[str]) -> int:
    return sum(1 for pattern in patterns if pattern in message_lc)


DETAIL_PATTERNS = [
    "grundig",
    "detaljert",
    "utfyllende",
    "dypt",
    "dypere",
    "med sitater",
    "vis sitater",
    "vis kilder",
]

PROMPT_PATTERNS = [
    "prompt",
    "prompts",
    "system prompt",
    "systempersona",
    "system persona",
    "persona",
    "template",
    "answer template",
    "instruksjon",
    "instruksjoner",
    "instruction",
    "llm",
    "sprakmodell",
    "sprakmodeller",
    "language model",
]

EXPERIMENT_PATTERNS = [
    "hypotese",
    "hypoteser",
    "eksperiment",
    "eksperimenter",
    "testprogram",
    "parametere",
    "parameter",
    "maal",
    "male",
    "observabel",
    "observabler",
    "diagnostikk",
    "diagnostikker",
    "runaway",
    "densifisering",
    "trajectory",
    "csv",
    "simulator",
    "simulering",
    "kjore",
    "run",
]

ARGUMENTATION_PATTERNS = [
    "ontologi",
    "primitive",
    "relasjonell",
    "relasjonelt",
    "spacetime",
    "romtid",
    "entanglement",
    "energi",
    "invariant",
    "invariants",
    "noether",
    "metastabilitet",
    "partikkel",
    "partikler",
    "lorentz",
    "causal",
    "kausal",
    "dpo",
    "ctmc",
    "ssa",
    "r_seed",
    "r_slide",
    "r_tri",
    "coarse-graining",
    "grovkorning",
]

STATUS_PATTERNS = [
    "status",
    "hvor er prosjektet",
    "hvor star prosjektet",
    "naa",
    "nå",
    "dagens",
    "repo",
    "implementert",
    "arbeidsstatus",
    "gap",
    "forskjell mellom rapporten og simulatoren",
]


GENERAL_DIRECT_CONTRACT = """Svar direkte og uten staffasje.
Skill eksplisitt mellom:
- hva rapporten formaliserer
- hva dagens kode faktisk implementerer
- hva observerte kjoredata viser
- hva som bare er inferens eller forslag
Hvis en av disse delene ikke er relevant, utelat den i stedet for a fylle ut med tom struktur."""


STATUS_CONTRACT = """## Kort status
Gi en konsis oppsummering av hvor prosjektet faktisk er na.

## Hva som finnes
Skill mellom rapport, kode, kjoredata og ny RAG-dokumentasjon.

## Viktigste gap
Forklar kort hva som mangler mellom forskningsrammen og dagens implementasjon.

## Narmeste neste steg
Foresla bare neste steg som passer med dagens verktoy og korpus."""


ARGUMENTATION_CONTRACT = """## Kort svar
Svar kort pa kjernepoenget forst.

## Primitive antagelser og rammeverk
Forklar hvilke antagelser, regler eller begreper argumentet hviler pa.

## Hvordan dette er begrunnet i kildene
Skill tydelig mellom rapportforankring, kodeforankring og eventuelle observasjoner.

## Testbare konsekvenser
Beskriv hva som i prinsippet eller praksis kan males for a styrke eller svekke argumentet.

## Apne hull eller svakheter
Si tydelig hva som fortsatt er uklart, uprøvd eller bare foreslatt."""


EXPERIMENT_CONTRACT = """## Kort anbefaling
Svar med det viktigste operative grepet forst.

## Hypotese eller sporsmal som testes
Formuler eksplisitt hva dagens verktøy faktisk kan si noe om.

## Hvordan bruke dagens verktøy
Beskriv konkrete steg, relevante parametere og hvilke output-felt som bor leses.

## Hva man bor se etter i resultatene
Knytt forventede tegn til metrics, trajectory eller andre dokumenterte observabler.

## Begrensninger
Si tydelig hva dagens toy-simulator ikke kan bevise."""


PROMPT_CONTRACT = """## Kort anbefaling
Gi en kort anbefaling om hvilken promptprofil eller instruksjonsretning som passer best.

## Instruksjoner modellen bor fa
List de viktigste systemreglene eller arbeidsreglene.

## Hva modellen ma skille eksplisitt
Krev at modellen skiller mellom rapport, kode, kjoredata og inferens.

## Anbefalt outputform
Si kort hvordan svarene bor struktureres for dette prosjektet.

## Fallgruver
Pek ut hva modellen spesielt ikke ma overdrive eller finne pa."""


STATUS_RETRIEVAL_HINT = (
    "repository status current implementation trajectory.csv relational_universe_sim.py "
    "research report project gap rag service"
)

ARGUMENTATION_RETRIEVAL_HINT = (
    "R_seed R_slide R_tri CTMC SSA DPO energy invariants metastability coarse-graining "
    "Lorentz causal cones emergent spacetime"
)

EXPERIMENT_RETRIEVAL_HINT = (
    "parameters trajectory.csv avg_degree clustering eff_dim metastability runaway densification "
    "simulator observables diagnostics"
)

PROMPT_RETRIEVAL_HINT = (
    "system persona answer template prompt profile language model instructions "
    "report code trajectory inference"
)


def _detail_level(message_lc: str) -> str:
    return "detailed" if _contains_any(message_lc, DETAIL_PATTERNS) else "standard"


def _source_groups(source_types: Iterable[str]) -> tuple[list[str], list[str]]:
    articles = list(source_types)
    return [], articles


def choose_answer_mode(
    *,
    message: str,
    case_id: str | None,
    docs_source_types: Iterable[str],
    selected_domain: str,
) -> AnswerModePlan:
    del docs_source_types
    message_lc = (message or "").strip().lower()
    detail_level = _detail_level(message_lc)

    prompt_hits = _word_hits(message_lc, PROMPT_PATTERNS)
    experiment_hits = _word_hits(message_lc, EXPERIMENT_PATTERNS)
    argument_hits = _word_hits(message_lc, ARGUMENTATION_PATTERNS)
    status_hits = _word_hits(message_lc, STATUS_PATTERNS)

    if case_id == "universe_prompts" or selected_domain == "prompts" or prompt_hits > 0:
        return AnswerModePlan(
            answer_mode="prompt_guidance",
            source_strategy="articles",
            response_shape="direct",
            streaming_allowed=False,
            rewrite_query=False,
            use_subquery_planner=False,
            default_prompt_case_id="universe_prompts",
            answer_contract=PROMPT_CONTRACT,
            planner_focus=(
                "Prioriter eksplisitte modellinstruksjoner, tydelig evidensskille og konkrete "
                "regler for hvordan prosjektets kilder skal brukes."
            ),
            detail_level=detail_level,
            retrieval_hint=PROMPT_RETRIEVAL_HINT,
        )

    if case_id == "universe_tools" or experiment_hits > max(argument_hits, status_hits):
        return AnswerModePlan(
            answer_mode="experiment_design",
            source_strategy="articles",
            response_shape="direct",
            streaming_allowed=False,
            rewrite_query=False,
            use_subquery_planner=experiment_hits >= 2,
            default_prompt_case_id="universe_tools",
            answer_contract=EXPERIMENT_CONTRACT,
            planner_focus=(
                "Prioriter dagens faktisk implementerte verktøy, målbare observabler og begrensninger "
                "i toy-simulatoren fremfor spekulative utvidelser."
            ),
            detail_level=detail_level,
            retrieval_hint=EXPERIMENT_RETRIEVAL_HINT,
        )

    if case_id == "universe_argumentation" or argument_hits > 0:
        return AnswerModePlan(
            answer_mode="argumentation",
            source_strategy="articles",
            response_shape="direct",
            streaming_allowed=False,
            rewrite_query=False,
            use_subquery_planner=False,
            default_prompt_case_id="universe_argumentation",
            answer_contract=ARGUMENTATION_CONTRACT,
            planner_focus=(
                "Prioriter rapportens formelle ramme, knyt den til dagens kode bare der det finnes klar dekning, "
                "og merk alle hopp som inferens."
            ),
            detail_level=detail_level,
            retrieval_hint=ARGUMENTATION_RETRIEVAL_HINT,
        )

    if case_id == "universe_project" or status_hits > 0:
        return AnswerModePlan(
            answer_mode="project_status",
            source_strategy="articles",
            response_shape="direct",
            streaming_allowed=True,
            rewrite_query=False,
            use_subquery_planner=False,
            default_prompt_case_id="universe_project",
            answer_contract=STATUS_CONTRACT,
            planner_focus=(
                "Prioriter status, modenhetsnivå, gap mellom teori og implementasjon, og nære neste steg."
            ),
            detail_level=detail_level,
            retrieval_hint=STATUS_RETRIEVAL_HINT,
        )

    return AnswerModePlan(
        answer_mode="general",
        source_strategy="articles",
        response_shape="direct",
        streaming_allowed=True,
        rewrite_query=True,
        use_subquery_planner=False,
        default_prompt_case_id=case_id or "universe_project",
        answer_contract=GENERAL_DIRECT_CONTRACT,
        planner_focus="Hold fast pa forskjellen mellom formell rapport, kjørbar toy-simulator og videre hypoteseutvikling.",
        detail_level=detail_level,
        retrieval_hint=STATUS_RETRIEVAL_HINT,
    )


def source_types_for_strategy(source_strategy: str, docs_source_types: Iterable[str]) -> list[str]:
    _, articles = _source_groups(docs_source_types)
    if source_strategy == "articles":
        return articles
    if source_strategy == "hybrid":
        return articles
    if source_strategy == "interviews":
        return []
    return list(docs_source_types)


def sanitize_text_without_citations(text: str) -> str:
    cleaned = re.sub(r"\[(\d+)\]", "", text or "")
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def trim_excerpt(text: str, limit: int = 220) -> str:
    collapsed = re.sub(r"\s+", " ", (text or "")).strip()
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[: limit - 1].rstrip() + "…"
