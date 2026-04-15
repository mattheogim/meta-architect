"""LLM-as-Judge evaluation using MAJ-Eval framework.

Based on: MAJ-Eval (arXiv:2507.21028) — Multi-Agent-as-Judge
Three judge personas independently evaluate, then aggregate.

Reference: research/papers-catalog.md Section G2
MUST-READ before modifying: research/verified/G2.md
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class JudgeScore:
    """Score from one judge persona."""

    judge_role: str
    score: float  # 1.0 - 5.0
    reasoning: str
    subscores: dict[str, float]  # e.g. {"feasibility": 4.0, "scalability": 3.5}


@dataclass
class EvalResult:
    """Aggregated evaluation result."""

    scores: list[JudgeScore]
    aggregate_score: float
    cohens_kappa: float  # inter-judge agreement
    human_calibrated: bool = False
    human_score: Optional[float] = None


# ---------------------------------------------------------------------------
# Judge personas — based on MAJ-Eval's persona extraction
# ---------------------------------------------------------------------------

JUDGE_PERSONAS: list[dict] = [
    {
        "role": "Senior Software Architect (10+ years)",
        "model": "claude-opus-4-6",
        "focus": ["feasibility", "scalability", "maintainability", "pattern_appropriateness"],
        "system_prompt": (
            "You are a senior software architect with 10+ years of experience. "
            "Evaluate the given architecture design on these criteria:\n"
            "1. Feasibility: Can this realistically be built with the stated constraints?\n"
            "2. Scalability: Will this handle growth (10x users, data, features)?\n"
            "3. Maintainability: Can a team maintain and evolve this over 2+ years?\n"
            "4. Pattern Appropriateness: Are the chosen patterns right for this problem?\n\n"
            "For each criterion, give a score 1-5 with specific reasoning.\n"
            "Then give an overall score 1-5.\n"
            "Be critical. A score of 5 means you'd ship this to production.\n"
            "Output as JSON: {\"feasibility\": X, \"scalability\": X, "
            "\"maintainability\": X, \"pattern_appropriateness\": X, "
            "\"overall\": X, \"reasoning\": \"...\"}"
        ),
    },
    {
        "role": "DevOps/SRE Engineer",
        "model": "gpt-4o",  # different model for diversity
        "focus": ["deployability", "observability", "security", "cost_efficiency"],
        "system_prompt": (
            "You are a DevOps/SRE engineer. "
            "Evaluate the given architecture design on these criteria:\n"
            "1. Deployability: How easy is this to deploy and operate?\n"
            "2. Observability: Can you monitor, debug, and trace issues?\n"
            "3. Security: Are there obvious security concerns?\n"
            "4. Cost Efficiency: Is the infrastructure cost reasonable?\n\n"
            "For each criterion, give a score 1-5 with specific reasoning.\n"
            "Then give an overall score 1-5.\n"
            "Be practical. Think about what breaks at 3 AM.\n"
            "Output as JSON: {\"deployability\": X, \"observability\": X, "
            "\"security\": X, \"cost_efficiency\": X, "
            "\"overall\": X, \"reasoning\": \"...\"}"
        ),
    },
    {
        "role": "Junior Developer (implementer)",
        "model": "claude-sonnet-4-6",
        "focus": ["clarity", "learning_curve", "documentation_quality", "implementation_guidance"],
        "system_prompt": (
            "You are a junior developer who will implement this architecture. "
            "Evaluate the design on these criteria:\n"
            "1. Clarity: Do you understand what to build and why?\n"
            "2. Learning Curve: How much do you need to learn before starting?\n"
            "3. Documentation Quality: Are the decisions explained well?\n"
            "4. Implementation Guidance: Is there enough detail to start coding?\n\n"
            "For each criterion, give a score 1-5 with specific reasoning.\n"
            "Then give an overall score 1-5.\n"
            "Be honest about confusion. If something is unclear, say so.\n"
            "Output as JSON: {\"clarity\": X, \"learning_curve\": X, "
            "\"documentation_quality\": X, \"implementation_guidance\": X, "
            "\"overall\": X, \"reasoning\": \"...\"}"
        ),
    },
]


def compute_cohens_kappa(scores: list[float], num_categories: int = 5) -> float:
    """Simplified Cohen's Kappa for ordinal scores.

    Rounds scores to nearest int, computes agreement.
    For 3+ raters, uses Fleiss' Kappa approximation.
    """
    if len(scores) < 2:
        return 1.0
    rounded = [round(s) for s in scores]
    # Pairwise agreement
    agreements = 0
    pairs = 0
    for i in range(len(rounded)):
        for j in range(i + 1, len(rounded)):
            pairs += 1
            if rounded[i] == rounded[j]:
                agreements += 1
    if pairs == 0:
        return 1.0
    p_observed = agreements / pairs
    p_expected = 1.0 / num_categories  # chance agreement for uniform dist
    if p_expected == 1.0:
        return 1.0
    return (p_observed - p_expected) / (1.0 - p_expected)


async def evaluate(architecture_output: str, scenario_description: str) -> EvalResult:
    """Run MAJ-Eval: 3 judges independently evaluate, then aggregate.

    This is the async interface — will be called by ExperimentRunner.
    Actual LLM calls require litellm to be configured.
    """
    # Placeholder — actual implementation calls LLM via litellm
    # Structure is correct, LLM integration added when llm/provider.py exists

    raise NotImplementedError(
        "LLM provider not yet configured. "
        "Implement after src/llm/provider.py is ready. "
        "See eval/maj_eval.py docstring for MAJ-Eval paper reference."
    )


def evaluate_mock(architecture_output: str) -> EvalResult:
    """Mock evaluation for testing the pipeline without LLM calls."""
    mock_scores = []
    for persona in JUDGE_PERSONAS:
        mock_scores.append(
            JudgeScore(
                judge_role=persona["role"],
                score=3.5,
                reasoning="[MOCK] Placeholder evaluation",
                subscores={f: 3.5 for f in persona["focus"]},
            )
        )
    overall_scores = [s.score for s in mock_scores]
    return EvalResult(
        scores=mock_scores,
        aggregate_score=sum(overall_scores) / len(overall_scores),
        cohens_kappa=compute_cohens_kappa(overall_scores),
    )
