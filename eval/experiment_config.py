"""Experiment configuration models.

All experiment conditions, scenarios, and controls are defined here.
These are the independent/control variables for the paper.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class ExperimentName(str, Enum):
    SCALE = "EXP-SCALE"
    ABLATION = "EXP-ABLATION"
    CHALLENGE = "EXP-CHALLENGE"
    MODEL = "EXP-MODEL"


class ScenarioID(str, Enum):
    CRUD = "scenario-1-crud"
    CHAT = "scenario-2-chat"
    MULTIAGENT = "scenario-3-multiagent"
    AMBIGUOUS = "scenario-4-ambiguous"
    EXTREME = "scenario-5-extreme"


class AgentID(str, Enum):
    """Agent identifiers mapped to v2 design doc names.

    Code ID → v2 Full Name (section):
      context_profiler      → Context Profiler (v2 §5, Agent 1)
      problem_decomposer    → Problem Decomposer (v2 §5, Agent 2)
      precedent_researcher  → Precedent Researcher (v2 §5, Agent 3)
      design_space_explorer → Design Space Explorer (v2 §6, Agent 4)
      cross_domain_connector→ Cross-Domain Connector (v2 §6, Agent 5)
      invention_engine      → Invention Engine (v2 §6, Agent 6)
      structure_advisor     → Structure Advisor (v2 §7, Agent 7)
      relationship_architect→ Relationship Architect (v2 §7, Agent 8)
      data_strategist       → Data Strategist (v2 §7, Agent 9)
      simplicity_advocate   → Simplicity Advocate (v2 §8, Agent 10)
      risk_analyst          → Risk, Cost & Scale Analyst (v2 §8, Agent 11)
      prototype_validator   → Prototype Validator (v2 §9, Agent 12)
      decision_evaluator    → Decision Evaluator (v2 §10, Agent 13)
      recorder              → Recorder (v2 §11, Agent 14) — always-on
      modeler               → Modeler (v2 §11, Agent 15) — final output
      knowledge_curator     → Knowledge Curator (v2 §11, Agent 16) — phase transition
      meta_verifier         → Meta Verifier (v2 §11, Agent 17) — on-demand

    MVP mapping (Phase 0.5):
      architect_agent  = structure_advisor (expanded to cover Phase 1-3)
      critic_agent     = simplicity_advocate + risk_analyst (merged)
      synthesizer_agent= decision_evaluator
    """

    CONTEXT_PROFILER = "context_profiler"
    PROBLEM_DECOMPOSER = "problem_decomposer"
    PRECEDENT_RESEARCHER = "precedent_researcher"
    DESIGN_SPACE_EXPLORER = "design_space_explorer"
    CROSS_DOMAIN_CONNECTOR = "cross_domain_connector"
    INVENTION_ENGINE = "invention_engine"
    STRUCTURE_ADVISOR = "structure_advisor"
    RELATIONSHIP_ARCHITECT = "relationship_architect"
    DATA_STRATEGIST = "data_strategist"
    SIMPLICITY_ADVOCATE = "simplicity_advocate"
    RISK_ANALYST = "risk_analyst"  # v2: "Risk, Cost & Scale Analyst"
    PROTOTYPE_VALIDATOR = "prototype_validator"
    DECISION_EVALUATOR = "decision_evaluator"
    RECORDER = "recorder"
    MODELER = "modeler"
    KNOWLEDGE_CURATOR = "knowledge_curator"
    META_VERIFIER = "meta_verifier"


ALL_AGENTS = list(AgentID)


# ---------------------------------------------------------------------------
# Predefined agent sets for EXP-SCALE
# ---------------------------------------------------------------------------

AGENT_SETS: dict[str, list[AgentID]] = {
    "1-agent": [],  # single mega-prompt, no agents
    "3-agent": [
        AgentID.STRUCTURE_ADVISOR,      # Architect
        AgentID.SIMPLICITY_ADVOCATE,    # Critic
        AgentID.DECISION_EVALUATOR,     # Synthesizer
    ],
    "6-agent": [
        AgentID.PROBLEM_DECOMPOSER,     # Understanding
        AgentID.DESIGN_SPACE_EXPLORER,  # Explorer
        AgentID.STRUCTURE_ADVISOR,      # Design
        AgentID.SIMPLICITY_ADVOCATE,    # Challenger
        AgentID.PROTOTYPE_VALIDATOR,    # Validator
        AgentID.DECISION_EVALUATOR,     # Decision
    ],
    "10-agent": [
        AgentID.CONTEXT_PROFILER,
        AgentID.PROBLEM_DECOMPOSER,
        AgentID.PRECEDENT_RESEARCHER,
        AgentID.DESIGN_SPACE_EXPLORER,
        AgentID.INVENTION_ENGINE,
        AgentID.STRUCTURE_ADVISOR,
        AgentID.RELATIONSHIP_ARCHITECT,
        AgentID.DATA_STRATEGIST,
        AgentID.SIMPLICITY_ADVOCATE,
        AgentID.DECISION_EVALUATOR,
    ],
    "17-agent": ALL_AGENTS,
}


# ---------------------------------------------------------------------------
# Model presets for EXP-MODEL
# ---------------------------------------------------------------------------

MODEL_PRESETS: dict[str, dict[str, str]] = {
    "all-opus": {a.value: "claude-opus-4-6" for a in ALL_AGENTS},
    "all-sonnet": {a.value: "claude-sonnet-4-6" for a in ALL_AGENTS},
    "mixed": {
        # Phase 1-3: Opus
        "context_profiler": "claude-opus-4-6",
        "problem_decomposer": "claude-opus-4-6",
        "precedent_researcher": "claude-opus-4-6",
        "design_space_explorer": "claude-opus-4-6",
        "cross_domain_connector": "claude-opus-4-6",
        "invention_engine": "claude-opus-4-6",
        "structure_advisor": "claude-opus-4-6",
        "relationship_architect": "claude-opus-4-6",
        "data_strategist": "claude-opus-4-6",
        # Phase 4: GPT-4o (different bias — Hegazy 2024)
        "simplicity_advocate": "gpt-4o",
        "risk_analyst": "gpt-4o",
        # Phase 4.5: Sonnet (code gen)
        "prototype_validator": "claude-sonnet-4-6",
        # Phase 5: Opus
        "decision_evaluator": "claude-opus-4-6",
        # Utility: lightweight
        "recorder": "claude-haiku-4-5",
        "modeler": "claude-sonnet-4-6",
        "knowledge_curator": "claude-haiku-4-5",
        "meta_verifier": "claude-sonnet-4-6",
    },
}


# ---------------------------------------------------------------------------
# Config models
# ---------------------------------------------------------------------------


class Controls(BaseModel):
    """Fixed across all experiments. Change these = new experiment."""

    temperature: float = 0.7
    max_tokens_per_agent: int = 4096
    seed: int = 42
    max_global_rounds: int = 50
    runs_per_condition: int = 3


class ExperimentConfig(BaseModel):
    """One experimental condition."""

    experiment: ExperimentName
    condition_name: str = Field(description="e.g. '6-agent', 'no-phase4', 'mixed'")
    scenario: ScenarioID
    repetition: int = Field(ge=1, le=10)

    agents: list[AgentID] = Field(default_factory=lambda: ALL_AGENTS)
    models: dict[str, str] = Field(
        default_factory=lambda: MODEL_PRESETS["mixed"]
    )
    enable_phase4: bool = True
    enable_blackboard: bool = True

    controls: Controls = Field(default_factory=Controls)


# ---------------------------------------------------------------------------
# Experiment matrix generators
# ---------------------------------------------------------------------------


def generate_scale_matrix(controls: Controls | None = None) -> list[ExperimentConfig]:
    """EXP-SCALE: vary agent count across all scenarios."""
    c = controls or Controls()
    configs = []
    for condition_name, agent_set in AGENT_SETS.items():
        for scenario in ScenarioID:
            for rep in range(1, c.runs_per_condition + 1):
                configs.append(
                    ExperimentConfig(
                        experiment=ExperimentName.SCALE,
                        condition_name=condition_name,
                        scenario=scenario,
                        repetition=rep,
                        agents=agent_set,
                        controls=c,
                    )
                )
    return configs


def generate_ablation_matrix(controls: Controls | None = None) -> list[ExperimentConfig]:
    """EXP-ABLATION: remove one agent at a time from 17-agent."""
    c = controls or Controls()
    target_scenarios = [ScenarioID.CHAT, ScenarioID.MULTIAGENT]
    configs = []
    for removed in ALL_AGENTS:
        remaining = [a for a in ALL_AGENTS if a != removed]
        for scenario in target_scenarios:
            for rep in range(1, c.runs_per_condition + 1):
                configs.append(
                    ExperimentConfig(
                        experiment=ExperimentName.ABLATION,
                        condition_name=f"without-{removed.value}",
                        scenario=scenario,
                        repetition=rep,
                        agents=remaining,
                        controls=c,
                    )
                )
    return configs


def generate_challenge_matrix(controls: Controls | None = None) -> list[ExperimentConfig]:
    """EXP-CHALLENGE: with vs without Phase 4."""
    c = controls or Controls()
    configs = []
    for enable in [True, False]:
        label = "with-phase4" if enable else "without-phase4"
        for scenario in ScenarioID:
            for rep in range(1, c.runs_per_condition + 1):
                configs.append(
                    ExperimentConfig(
                        experiment=ExperimentName.CHALLENGE,
                        condition_name=label,
                        scenario=scenario,
                        repetition=rep,
                        enable_phase4=enable,
                        controls=c,
                    )
                )
    return configs


def generate_model_matrix(controls: Controls | None = None) -> list[ExperimentConfig]:
    """EXP-MODEL: vary model diversity."""
    c = controls or Controls()
    configs = []
    for preset_name, model_map in MODEL_PRESETS.items():
        for scenario in ScenarioID:
            for rep in range(1, c.runs_per_condition + 1):
                configs.append(
                    ExperimentConfig(
                        experiment=ExperimentName.MODEL,
                        condition_name=preset_name,
                        scenario=scenario,
                        repetition=rep,
                        models=model_map,
                        controls=c,
                    )
                )
    return configs


def total_runs() -> int:
    """Print total experiment count for budget estimation."""
    return (
        len(generate_scale_matrix())
        + len(generate_ablation_matrix())
        + len(generate_challenge_matrix())
        + len(generate_model_matrix())
    )


if __name__ == "__main__":
    print(f"EXP-SCALE:     {len(generate_scale_matrix())} runs")
    print(f"EXP-ABLATION:  {len(generate_ablation_matrix())} runs")
    print(f"EXP-CHALLENGE: {len(generate_challenge_matrix())} runs")
    print(f"EXP-MODEL:     {len(generate_model_matrix())} runs")
    print(f"TOTAL:         {total_runs()} runs")
