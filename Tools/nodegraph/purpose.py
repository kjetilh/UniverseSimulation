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
    """A calibration point that was actually measured, with its provenance.

    `null_value` is the null measured on the SAME footing as this reference --
    same arm, same pair count, same candidate set. Without it a separation is
    not a separation. On 2026-09-08 this contract reported a separation of 9.9
    by dividing a positive reference measured on one arm (n=8) by a null
    measured on a different arm (n=24). Like for like the number was 1.35, below
    the contract's own floor of 2, and the framework should have refused itself.
    """

    role: str          # 'null' | 'positive'
    value: Optional[float]
    method: str        # how it was produced, in one line
    source: str        # file, script or procedure it can be re-derived from
    null_value: Optional[float] = None   # the null measured alongside `value`

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
    holdout_null_reference: Optional[Reference] = None

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

        pos = float(self.positive_reference.value)
        # Like for like: the positive reference is judged against the null that
        # was measured with it, never against a null from another arm.
        basis = self.positive_reference.null_value
        if basis is None:
            return Verdict(
                False,
                [
                    "positive reference has no null measured on the same footing "
                    "(Reference.null_value is unset); a ratio against a null from "
                    "another arm, another n or another candidate set is not a "
                    "separation and must not be reported as one"
                ],
            )
        basis = float(basis)
        sep = pos / basis if basis > 1e-12 else float("inf")
        if sep < self.min_separation:
            return Verdict(
                False,
                [
                    f"statistic does not separate its own references "
                    f"(positive={pos:.4g}, its own null={basis:.4g}, ratio={sep:.3g} < "
                    f"{self.min_separation:g}); the purpose is not measurable by "
                    f"this statistic and no candidate can be gated on it"
                ],
                separation=sep,
                threshold=float(self.null_reference.value),
            )
        return Verdict(True, [], separation=sep, threshold=float(self.null_reference.value))

    def holdout_threshold(self) -> float:
        """Holdout gate. A search picks the best of thousands and needs a
        max-statistic null; a holdout measures ONE pre-chosen candidate and needs
        that candidate's own null. They are different numbers and conflating them
        was one of this contract's defects."""
        r = self.holdout_null_reference or self.null_reference
        if not r.measured:
            raise AssertionError("holdout null reference not measured")
        return float(r.value)

    def gate_threshold(self) -> float:
        """Pre-registered selection pass mark: the max-statistic null."""
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
        hthr = self.holdout_threshold()
        s_sel = float(self.score(graph))
        s_hold = float(self.holdout(graph))
        extra: Dict[str, object] = {}
        if self.invariant is not None:
            p, signs = self.invariant(graph)
            extra["invariant_p"] = p
            if self.reference_graph is not None:
                rp, rsigns = self.invariant(self.reference_graph)
                extra["reference_invariant_p"] = rp
                # Up to a global flip: a two-sided sign test cannot tell d from
                # -d, so a candidate whose signs are the reference's negated
                # carries no more direction either. Comparing raw vectors called
                # that a difference, which it is not.
                a, b = tuple(signs), tuple(rsigns)
                extra["transform_only"] = (a == b) or (a == tuple(-x for x in b))
                # and the part that actually decides: does the direction evidence
                # get stronger, or only the weighted score?
                extra["invariant_improves"] = bool(p < rp)
        # One place forms the verdict. Passing both gates is not enough: if an
        # invariant companion was declared, the direction evidence must improve
        # too, or the candidate only moved the weighted score.
        finding = (s_sel > thr) and (s_hold > hthr)
        if "invariant_improves" in extra:
            finding = finding and bool(extra["invariant_improves"])
        elif self.invariant is not None:
            finding = False
        extra["is_finding"] = finding
        return {
            "admissible": True,
            "expr": graph.to_expr(),
            "size": graph.size,
            "depth": graph.depth,
            "selection_score": s_sel,
            "holdout_score": s_hold,
            "gate_threshold": thr,
            "holdout_gate_threshold": hthr,
            "passes_selection": s_sel > thr,
            "passes_holdout": s_hold > hthr,
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
