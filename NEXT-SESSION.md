# Next Session To-Do

> Read this file first at session start.
> Check off when done and record in SESSION-LOG.md.

---

## Context loading order (at new session start)

```
1. Read this file (NEXT-SESSION.md)
2. Read CLAUDE.md (check behavioral rules)
3. Check previous session in SESSION-LOG.md
4. Check research/MASTER-PLAN.md §5 Phase 0
```

---

## Phase 0: Project setup + v2 reinforcement (est. 2-3 hours)

### Step 0-1: pyproject.toml + project structure
```
[ ] Create pyproject.toml
    dependencies:
      - langgraph >= 0.2
      - pydantic >= 2.0
      - litellm
      - pyyaml
      - pytest
    optional:
      - e2b
      - scipy (logistic fitting)
      - matplotlib (paper figures)

[ ] Create src/ directory structure (empty __init__.py)
    src/
    ├── __init__.py
    ├── blackboard/
    │   └── __init__.py
    ├── orchestrator/
    │   └── __init__.py
    ├── agents/
    │   ├── __init__.py
    │   └── prompts/
    ├── llm/
    │   └── __init__.py
    ├── sandbox/
    │   └── __init__.py
    └── recorder/
        └── __init__.py

[ ] Create tests/ directory structure (empty test files)
    tests/
    ├── __init__.py
    ├── test_state_transition.py
    ├── test_router.py
    └── test_gc.py

[ ] Create .env.example
    ANTHROPIC_API_KEY=sk-ant-...
    OPENAI_API_KEY=sk-...

[ ] Update .gitignore
    .env
    __pycache__/
    eval/experiments/*/runs/
    *.pyc
```

**Verify**: `python -c "import pydantic; print('OK')"` + `pytest --collect-only`

---

### Step 0-2: v2 design doc reinforcement (7+4+1 items)

Add directly to v2/meta-architect-v2.md:

```
[ ] Ch.1: Add explicit "Blackboard = data sharing layer, Phase = control flow layer"
[ ] 3.2.1: Add Review rubric section (checklist for each of the 13 slots)
[ ] 3.3: Specify Phase 0.5 MVP uses manual promotion policy
[ ] 3.7: Add convergence rules section (10 per Phase, dynamic termination, 200-calls safety net)
[ ] Ch.5 Agent 3: Revise Precedent Researcher to web_search-based (defer RAG)
[ ] Ch.8: Add No Rubber-Stamping Rule (require min 1 alternative)
[ ] Ch.9: Classify success_criteria verifiability (code/simulation/manual)
[ ] Ch.12: Add Phase transition reasoning summary (200 tokens)
[ ] 13.6: Add Think in NL, Write in Schema principle
[ ] 4 unresolved QOC: record "keep" decisions (Observability, Evaluation, Security, Evidence Source)
[ ] Ch.16: Update implementation roadmap to Master Plan Phase 0→0.5→1→2→3→4
```

**Verify**: `bash verification/verify.sh` (existing 45 items pass + new items)

---

### Step 0-3: Resolve 9 INFO items from validate_claims.py

```
[ ] Add [src:] tags to untagged numbers in MASTER-PLAN.md
[ ] python research/validate_claims.py → verify 0 INFO
```

---

### Step 0-4: git commit

```
[ ] git add -A
[ ] git commit -m "Phase 0: project setup + v2 reinforcement + experiment framework"
```

---

## After Phase 0 completion → preparing to start Phase 0.5

### Step 0.5-prep: Read 3 MUST-READ papers

```
[ ] C1: Han & Zhang (arXiv:2507.01701)
    - Access arxiv HTML via WebFetch
    - Extract key points from §3 architecture, §4 agent roles
    - Write research/verified/C1.md

[ ] E1: La Malfa (arXiv:2505.21298)
    - Extract key points from §3 four critiques
    - Write research/verified/E1.md

[ ] I1: Tam (arXiv:2408.02442)
    - Extract key points from §3 experiments, §4 mitigation
    - Write research/verified/I1.md
```

**Verify**: `python research/validate_claims.py` → C1, I1 disappear from WARN

---

## Phase 0.5 (session after next): 3-Agent MVP

```
[ ] src/blackboard/schema.py — 13-slot Pydantic (4 core active, 9 reserved)
[ ] src/blackboard/entry.py — 19-field metadata
[ ] src/blackboard/state.py — state transition 4-principle validator
[ ] src/blackboard/views.py — read/write views for 3 agents
[ ] src/agents/base_agent.py — Think NL, Write Schema common base
[ ] src/agents/architect_agent.py — Phase 1-3 integrated
[ ] src/agents/critic_agent.py — Phase 4 adversarial
[ ] src/agents/synthesizer_agent.py — Phase 5 decision
[ ] src/agents/prompts/{architect,critic,synthesizer}.md — ~300-500 lines each
[ ] src/llm/provider.py — LiteLLM integration (All-Sonnet)
[ ] src/orchestrator/graph.py — LangGraph assembly (linear + 1 loop)
[ ] src/recorder/logger.py — basic event logging
[ ] Hook up eval/experiment_runner.py _execute_system()
[ ] First end-to-end run with Scenario 2 (chat app)
[ ] EXP-SCALE "1-agent" + "3-agent" × 15 runs each = 30 data points collected
[ ] Interim check: 3-agent > 1-agent? → decide direction
```

---

## Cautions

1. **Do not start implementation without reading the paper** — check_paper_deps.py hook will warn
2. **All experiments must go through ExperimentRunner** — direct calls raise RuntimeError
3. **`[src:]` tag required when writing numbers** — validate_claims.py checks
4. **When making a decision, record it in SESSION-LOG.md** — reason + alternatives + evidence
5. **Do not modify PRE-REGISTRATION.md** — change after hypothesis lock = HARKing
