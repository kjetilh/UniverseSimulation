#!/usr/bin/env python3
"""
purpose.py -- the formaal contract.

This is the file that makes the rest worth building. A node library plus a
search loop is a nicer notation for guessing; what turns guessing into a test
is a purpose that can say, before any candidate is scored, whether it is
capable of distinguishing anything at all.

The rule is taken directly from the v17 program closure
(Documentation/v17_program_closure.md, section 7):

    A primary endpoint quantity shall have a MEASURED null reference and a
    MEASURED positive reference before it is used as a gate. Missing either,
    the round is an instrumentation round and does not count as a test of the
    hypothesis.

Here that rule is mechanical rather than advisory. A PurposeContract with an
unmeasured reference refuses to gate. A contract whose two references are not
separated by its own statistic reports itself unmeasurable and refuses to gate.
Eleven rounds of the v17 series would have been stopped at round four by the
first of those two refusals.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Callable, Dict, List, Optional

from core import Graph


@dataclass
class Reference:
    """A calibration point that was actually measured, with its provenance."""

    role: str          # 'null' | 'positive'
    value: Optional[float]
    method: str        # how it was produced, in one line
    source: str        # file, script or procedure it can be re-derived from

    @property
    def measured(self) -> bool:
        return self.value is not None


@dataclass
class Verdict:
    admissible: bool
    reasons: List[str] = field(default_factory=list)
    separation: Optional[float] = None
    threshold: Optional[float] = None

    def __bool__(self) -> bool:
        return self.admissible


@dataclass
class PurposeContract:
    """What a candidate must achieve, and what makes the achievement readable."""

    id: str
    statement: str                       # the purpose in one sentence, in words
    signature: tuple                     # ((input_name, type), ...)
    output_type: str
    score: Callable[[Graph], float]      # selection split; cheap, exact, total
    holdout: Callable[[Graph], float]    # reporting split; never used to select
    null_reference: Reference
    positive_reference: Reference
    min_separation: float = 2.0          # positive must beat null by this factor
    notes: str = ""
    # Optional transform-invariant companion. Returns (p_value, sign_vector) for
    # a graph on the reporting split. Without it a candidate can win purely by
    # being a monotone re-spelling of another one -- see section 4.3 of
    # Documentation/Nodegraf_Vurdering_2026-09-08.md, where exactly that
    # happened and cost nothing only because it was caught.
    invariant: Optional[Callable[[Graph], tuple]] = None
    reference_graph: Optional[Graph] = None

    # -- the two refusals -------------------------------------------------
    def admissibility(self) -> Verdict:
        reasons: List[str] = []
        if not self.null_reference.measured:
            reasons.append(
                "null reference not measured -- this is an instrumentation round, "
                "not a test (v17_program_closure.md section 7)"
            )
        if not self.positive_reference.measured:
            reasons.append(
                "positive reference not measured -- nothing shows the statistic "
                "responds when the effect is present (v17i is the analogue)"
            )
        if reasons:
            return Verdict(False, reasons)

        null = float(self.null_reference.value)
        pos = float(self.positive_reference.value)
        sep = pos / null if null > 1e-12 else float("inf")
        if sep < self.min_separation:
            return Verdict(
                False,
                [
                    f"statistic does not separate its own references "
                    f"(positive={pos:.4g}, null={null:.4g}, ratio={sep:.3g} < "
                    f"{self.min_separation:g}); the purpose is not measurable by "
                    f"this statistic and no candidate can be gated on it"
                ],
                separation=sep,
                threshold=null,
            )
        return Verdict(True, [], separation=sep, threshold=null)

    def gate_threshold(self) -> float:
        """Pre-registered pass mark: the measured null reference."""
        v = self.admissibility()
        if not v:
            raise AssertionError("; ".join(v.reasons))
        return float(self.null_reference.value)

    def evaluate(self, graph: Graph) -> Dict[str, object]:
        """Score a candidate on both splits and apply the pre-registered gate."""
        v = self.admissibility()
        if not v:
            return {"admissible": False, "reasons": v.reasons}
        thr = self.gate_threshold()
        s_sel = float(self.score(graph))
        s_hold = float(self.holdout(graph))
        extra: Dict[str, object] = {}
        if self.invariant is not None:
            p, signs = self.invariant(graph)
            extra["invariant_p"] = p
            if self.reference_graph is not None:
                rp, rsigns = self.invariant(self.reference_graph)
                extra["reference_invariant_p"] = rp
                # A candidate whose sign vector equals the reference's carries no
                # directional information the reference did not already carry,
                # however much better its weighted score looks.
                extra["transform_only"] = (tuple(signs) == tuple(rsigns))
        return {
            "admissible": True,
            "expr": graph.to_expr(),
            "size": graph.size,
            "depth": graph.depth,
            "selection_score": s_sel,
            "holdout_score": s_hold,
            "gate_threshold": thr,
            "passes_selection": s_sel > thr,
            "passes_holdout": s_hold > thr,
            "null_reference": self.null_reference.value,
            "positive_reference": self.positive_reference.value,
            **extra,
        }

    def to_json(self) -> str:
        d = {
            "id": self.id,
            "statement": self.statement,
            "signature": [list(x) for x in self.signature],
            "output_type": self.output_type,
            "null_reference": asdict(self.null_reference),
            "positive_reference": asdict(self.positive_reference),
            "min_separation": self.min_separation,
            "admissibility": asdict(self.admissibility()),
            "notes": self.notes,
        }
        return json.dumps(d, indent=2, ensure_ascii=False)
