# Meta Architect

[![Live docs](https://img.shields.io/badge/docs-meta--architect.vercel.app-black?style=flat-square)](https://meta-architect.vercel.app)

> Put in an idea. Get an architecture that covers what you don't know.

A multi-agent system where **17 specialized LLM agents** collaborate via a **Blackboard pattern** to design software architecture — surfacing blind spots, challenging assumptions, and producing traceable decisions.

---

## Why This Exists

When you ask an LLM to design architecture, it gives you **one perspective**. It anchors on familiar patterns, skips trade-off analysis, and never challenges its own proposals.

Meta Architect forces **cognitive diversity** by separating concerns into independent agents — each with a different knowledge base, different evaluation criteria, and structural constraints that prevent one viewpoint from dominating another.

**Core hypothesis**: Forced cognitive diversity produces systematically better architecture designs than a single well-prompted agent.

## How It Works

```
You: "I want to build a real-time chat app"

         Understanding          Exploration           Design
    ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
    │ Context Profiler │   │ Design Space    │   │ Structure       │
    │ Problem Decomp.  │   │ Cross-Domain    │   │ Relationship    │
    │ Precedent Search │   │ Invention Engine│   │ Data Strategist │
    └────────┬────────┘   └────────┬────────┘   └────────┬────────┘
             │                     │                     │
             └─────────────────────┼─────────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │     BLACKBOARD (shared)      │
                    │  13 slots + 19-field metadata │
                    └──────────────┬──────────────┘
                                   │
             ┌─────────────────────┼─────────────────────┐
             │                     │                     │
    ┌────────┴────────┐   ┌────────┴────────┐   ┌────────┴────────┐
    │   Challenge      │   │   Validation    │   │   Decision      │
    │ Simplicity Adv.  │   │ Prototype Val.  │   │ Decision Eval.  │
    │ Risk Analyst     │   │ (runs code!)    │   │ (weighted score) │
    └─────────────────┘   └─────────────────┘   └─────────────────┘

Output: Architecture + QOC Records + ADR + Mermaid Diagrams
```

**Key differentiators vs existing tools:**
- Architecture is the **primary output**, not a side effect of code generation
- **Adversarial challenge phase** — agents actively argue against the design
- **Prototype validation** — actually runs code to test assumptions
- **Full decision traceability** — every choice has a QOC record

## Research Foundation

Built on 45+ academic papers. Both supporting and opposing evidence.

| Evidence For | Evidence Against |
|-------------|-----------------|
| Multi-agent debate improves factuality (Du et al., ICML 2024) | Coordination overhead scales at 1.724x (Google DeepMind, 2025) |
| Diversity of thought: 91% vs 82% on GSM-8K (Hegazy, 2024) | Persona prompting doesn't improve reasoning (Basil et al., 2025) |
| LLM Blackboard MAS = SOTA + fewer tokens (Han & Zhang, 2025) | 80% of cases: single agent matches multi-agent (Zhao et al., 2025) |
| Agent scaling follows logistic growth (Qian et al., ICLR 2025) | Debate can decrease accuracy via echo chambers (Wynn, ICML 2025) |

Full catalog: [`research/papers-catalog.md`](research/papers-catalog.md) (MUST-READ 12 papers identified)

## Experiment Design

4 experiments, 252 runs, 4 hypotheses. Pre-registered to prevent HARKing.

| Experiment | Question | Runs |
|-----------|----------|------|
| **EXP-SCALE** | Does quality improve with more agents (1→3→6→10→17)? | 75 |
| **EXP-ABLATION** | Which individual agent contributes most? | 102 |
| **EXP-CHALLENGE** | Does adversarial Phase 4 improve feasibility? | 30 |
| **EXP-MODEL** | Does mixing different LLMs increase diversity? | 45 |

Target: ICSE / ESEM / ASE paper submission.

## Project Status

| Phase | Status | Description |
|-------|--------|-------------|
| v2 Design | Done | 1,852-line design doc, 17 agents + 4-module orchestrator |
| Research | Done | 45+ papers, 8 deep research topics, plan self-review |
| Experiment Framework | Done | Runner, auto-metrics, LLM-as-Judge, 5 scenarios |
| Hallucination Prevention | Done | 4-layer system (tags + hooks + validator + runner) |
| **Phase 0: Setup** | **Next** | pyproject.toml + v2 reinforcement |
| Phase 0.5: 3-Agent MVP | Planned | Core hypothesis validation |
| Phase 1-3: Full System | Planned | 17 agents + full experiments |

## File Structure

```
meta-architect/
├── CLAUDE.md                     # Behavioral guidelines (7 rules)
├── PRE-REGISTRATION.md           # Hypotheses H1-H4 (do not modify)
├── SESSION-LOG.md                # Per-session change/decision/error log
├── NEXT-SESSION.md               # Next session checklist
│
├── v2/
│   ├── meta-architect-v2.md      # System design (1,852 lines)
│   └── meta-architect-v2-qoc.md  # Design decision records
│
├── research/
│   ├── MASTER-PLAN.md            # Execution plan (MVP-first)
│   ├── papers-catalog.md         # 45+ papers with citations
│   ├── paper-feature-map.json    # Feature ↔ paper mapping
│   ├── check_paper_deps.py       # Pre-implementation paper check (hook)
│   ├── validate_claims.py        # Claim tag cross-reference validator (hook)
│   ├── TAGGING-SYSTEM.md         # [src:][FACT][VERIFIED] rules
│   ├── deep-{1..8}.md            # Deep research on 8 critical gaps
│   └── EXPERIMENT-DESIGN.md      # Paper-grade experiment methodology
│
├── eval/
│   ├── experiment_config.py      # 252-run experiment matrix
│   ├── experiment_runner.py      # Only entry point (blocks direct calls)
│   ├── auto_measure.py           # Coverage, cost, latency measurement
│   ├── maj_eval.py               # 3-persona LLM-as-Judge
│   ├── paper/generate_tables.py  # Auto-generate paper tables + figures
│   ├── scenarios/*.yaml          # 5 standard test scenarios
│   └── judges/rubric.yaml        # Fixed evaluation rubric
│
├── src/                          # Implementation (Phase 0.5+)
└── tests/                        # Unit tests (Phase 0.5+)
```

## Hallucination Prevention (4 Layers)

This project takes hallucination seriously — every claim is traceable.

| Layer | When | What |
|-------|------|------|
| **L1: Claim Tags** | Writing docs | Every claim gets `[src:paper-A1][FACT][VERIFIED]` |
| **L2: Paper Deps** | Writing code | Hook warns if required paper hasn't been read |
| **L3: Claim Validator** | After edits | Auto-checks tag references + untagged numbers |
| **L4: Experiment Runner** | Running system | Forces data collection, blocks direct calls |

## Quick Start (for next session)

```bash
# 1. Read the next-session checklist
cat NEXT-SESSION.md

# 2. Verify experiment framework
python eval/experiment_config.py
# → EXP-SCALE: 75, EXP-ABLATION: 102, EXP-CHALLENGE: 30, EXP-MODEL: 45, TOTAL: 252

# 3. Run claim validator
python research/validate_claims.py

# 4. Start Phase 0 (see NEXT-SESSION.md for details)
```

## Key Design Decisions

| Decision | Rationale | Alternative Considered |
|----------|-----------|----------------------|
| 17 agents (not 3-6) | Forced cognitive diversity; lazy loading keeps active count at 2-4 | Fewer broader agents |
| Blackboard pattern | Validated by Han & Zhang (2025); shared context + decoupled agents | Pipeline, Swarm, MoE |
| MVP-first (3→17) | Validate hypothesis early; each addition = experiment data point | Build all 17 first |
| LLM-as-Judge | Expert review infeasible; MAJ-Eval achieves Spearman 0.47 | Human expert panel |
| Think NL, Write Schema | JSON-mode hurts reasoning 10-15% (Tam 2024) | All structured output |
| All-Sonnet initially | Cheapest for iteration; EXP-MODEL decides final mix | Mixed models from start |

## License

TBD

## Citation

If you use this work, please cite:
```
@misc{meta-architect-2026,
  title={Meta Architect: Forced Cognitive Diversity in Multi-Agent LLM Systems for Software Architecture Design},
  author={galileii},
  year={2026},
  note={Work in progress}
}
```
