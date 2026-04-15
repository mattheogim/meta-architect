"""Automatic metric measurement for experiment runs.

Measures all dependent variables defined in EXPERIMENT-DESIGN.md.
Called by ExperimentRunner after each run — never manually.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, field

# 60+ concepts from v2 Section 15, used for coverage measurement
CONCEPT_CHECKLIST: list[str] = [
    # 1. Structural foundations (9)
    "graph theory", "network science", "ontology", "database theory",
    "systems theory", "category theory", "set theory", "topology",
    "information theory",
    # 2. Design/decision methods (10)
    "design space exploration", "architecture decision record", "trade-off analysis",
    "triz", "domain-driven design", "constraint satisfaction",
    "multi-criteria decision", "decision matrix", "morphological analysis",
    "axiomatic design",
    # 3. Architecture patterns (8)
    "microservices", "event-driven", "layered", "hexagonal",
    "cqrs", "actor model", "pipe-and-filter", "blackboard",
    # 4. AI/agent patterns (10)
    "multi-agent", "swarm", "orchestrator", "mixture of experts",
    "react", "chain-of-thought", "multi-agent debate",
    "constitutional ai", "knowledge graph", "rag",
    # 5. Modeling (7)
    "uml", "c4 model", "sequence diagram", "erd",
    "flowchart", "state machine", "mermaid",
    # 6. Higher disciplines (7)
    "systems engineering", "decision science", "cybernetics",
    "complexity science", "philosophy of science", "epistemology", "semiotics",
    # 7. Validation (4)
    "spike solution", "load testing", "fmea", "cost modeling",
    # Extra concepts often relevant
    "bounded context", "aggregate", "event sourcing", "api gateway",
    "message queue", "caching", "cdn", "load balancer",
    "authentication", "authorization", "rate limiting", "monitoring",
    "logging", "ci/cd", "containerization", "serverless",
]


@dataclass
class RunMetrics:
    """All measured dependent variables for one run."""

    concept_coverage: int = 0
    concept_coverage_list: list[str] = field(default_factory=list)
    unique_perspectives: int = 0
    unique_perspectives_list: list[str] = field(default_factory=list)
    total_tokens_in: int = 0
    total_tokens_out: int = 0
    total_cost_usd: float = 0.0
    total_latency_sec: float = 0.0
    total_rounds: int = 0
    conflict_count: int = 0
    challenge_rate: float = 0.0
    decision_trace_completeness: float = 0.0

    def to_dict(self) -> dict:
        return {
            "concept_coverage": self.concept_coverage,
            "concept_coverage_list": self.concept_coverage_list,
            "unique_perspectives": self.unique_perspectives,
            "unique_perspectives_list": self.unique_perspectives_list,
            "total_tokens": self.total_tokens_in + self.total_tokens_out,
            "total_tokens_in": self.total_tokens_in,
            "total_tokens_out": self.total_tokens_out,
            "total_cost_usd": round(self.total_cost_usd, 4),
            "total_latency_sec": round(self.total_latency_sec, 2),
            "total_rounds": self.total_rounds,
            "conflict_count": self.conflict_count,
            "challenge_rate": round(self.challenge_rate, 3),
            "decision_trace_completeness": round(self.decision_trace_completeness, 3),
        }


def measure_concept_coverage(output_text: str) -> tuple[int, list[str]]:
    """Count how many of the 60+ concepts appear in the system output.

    Simple keyword matching — intentionally basic so it's reproducible.
    A concept counts as covered if its name appears in the output (case-insensitive).
    """
    text_lower = output_text.lower()
    covered = []
    for concept in CONCEPT_CHECKLIST:
        # Match whole concept name (allow minor variations)
        pattern = re.escape(concept)
        if re.search(pattern, text_lower):
            covered.append(concept)
    return len(covered), covered


def measure_challenge_rate(challenges: list[dict]) -> float:
    """Ratio of actionable challenges (severity >= medium that led to design changes)."""
    if not challenges:
        return 0.0
    medium_plus = [c for c in challenges if c.get("severity") in ("medium", "high", "critical")]
    if not medium_plus:
        return 0.0
    actionable = [c for c in medium_plus if c.get("led_to_change", False)]
    return len(actionable) / len(medium_plus)


def measure_decision_trace(qoc_records: list[dict], decisions: list[dict]) -> float:
    """Fraction of decisions that have a complete QOC trace (question + options + criteria)."""
    if not decisions:
        return 0.0
    traced = 0
    decision_ids = {d.get("id") for d in decisions}
    for qoc in qoc_records:
        if qoc.get("decision_id") in decision_ids:
            has_question = bool(qoc.get("question"))
            has_options = bool(qoc.get("options"))
            has_criteria = bool(qoc.get("criteria"))
            if has_question and has_options and has_criteria:
                traced += 1
    return traced / len(decisions)


def measure_cost(agent_calls: list[dict]) -> float:
    """Estimate USD cost from token counts.

    Prices as of 2025 (update if prices change).
    """
    pricing = {
        "claude-opus-4-6": {"input": 15.0 / 1_000_000, "output": 75.0 / 1_000_000},
        "claude-sonnet-4-6": {"input": 3.0 / 1_000_000, "output": 15.0 / 1_000_000},
        "claude-haiku-4-5": {"input": 0.80 / 1_000_000, "output": 4.0 / 1_000_000},
        "gpt-4o": {"input": 2.50 / 1_000_000, "output": 10.0 / 1_000_000},
    }
    total = 0.0
    for call in agent_calls:
        model = call.get("model", "claude-sonnet-4-6")
        prices = pricing.get(model, pricing["claude-sonnet-4-6"])
        total += call.get("tokens_in", 0) * prices["input"]
        total += call.get("tokens_out", 0) * prices["output"]
    return total


def measure_all(run_output: dict) -> RunMetrics:
    """Compute all metrics from a run's raw output.

    Args:
        run_output: dict with keys: blackboard_text, agent_calls, challenges,
                    qoc_records, decisions, conflicts
    """
    metrics = RunMetrics()

    # Coverage
    text = run_output.get("blackboard_text", "")
    metrics.concept_coverage, metrics.concept_coverage_list = measure_concept_coverage(text)

    # Cost
    agent_calls = run_output.get("agent_calls", [])
    metrics.total_cost_usd = measure_cost(agent_calls)
    metrics.total_tokens_in = sum(c.get("tokens_in", 0) for c in agent_calls)
    metrics.total_tokens_out = sum(c.get("tokens_out", 0) for c in agent_calls)
    metrics.total_rounds = len(agent_calls)

    # Latency
    metrics.total_latency_sec = sum(c.get("latency_ms", 0) for c in agent_calls) / 1000

    # Conflicts
    metrics.conflict_count = len(run_output.get("conflicts", []))

    # Challenge effectiveness
    metrics.challenge_rate = measure_challenge_rate(run_output.get("challenges", []))

    # Decision traceability
    metrics.decision_trace_completeness = measure_decision_trace(
        run_output.get("qoc_records", []),
        run_output.get("decisions", []),
    )

    return metrics
