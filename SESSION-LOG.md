# Session Log

> Records work done, decisions, errors, and next steps for each session.
> Not QOC format but a **change log + decision log + error log** separated approach.
> Reason: QOC is for design decisions; session records are for work tracking. Different purposes.

---

## Session 1 — 2026-04-15 (this session)

### Summary
Conducted comprehensive research grounded in the v2 design doc → developed plan → codified the experiment framework → built hallucination-prevention system.

### Change log (created/modified files)

| File | Action | Content |
|------|------|------|
| `CLAUDE.md` | created | Behavioral guidelines §1-4 + §5 paper enforcement + §6 experiment protocol + §7 tag rules |
| `PRE-REGISTRATION.md` | created | Hypotheses H1-H4 + analysis plan + HARKing prevention |
| `research/00-research-index.md` | created | Full research index (completed/in-progress) |
| `research/papers-catalog.md` | created | 45+ papers, 11 sections, 12 MUST-READ identified |
| `research/paper-feature-map.json` | created | 11 features × required-papers mapping |
| `research/check_paper_deps.py` | created | PreToolUse hook: enforce paper reading at implementation |
| `research/validate_claims.py` | created | PostToolUse hook: automatic tag-to-source consistency check |
| `research/TAGGING-SYSTEM.md` | created | [src:][FACT][VERIFIED] tagging rules |
| `research/deep-{1..8}.md` | created | 8 Deep Research notes |
| `research/MASTER-PLAN.md` | created→v2 | Final execution plan (19 revisions applied) |
| `research/MASTER-PLAN-v1.md` | preserved | v1 plan (before revisions) |
| `research/MASTER-PLAN-REVIEW.md` | created | Plan self-evaluation (6.1/10) |
| `research/EXPERIMENT-DESIGN.md` | created | Paper-grade experiment design (4 experiments, 252 runs) |
| `eval/experiment_config.py` | created | Automatic experiment matrix generation (252 runs verified) |
| `eval/experiment_runner.py` | created | Experiment runner wrapper (sole entry point) |
| `eval/auto_measure.py` | created | Automatic measurement (coverage, cost, latency, etc.) |
| `eval/maj_eval.py` | created | LLM-as-Judge (3 personas, Cohen's κ) |
| `eval/paper/generate_tables.py` | created | Paper Table 1-3 + Figure 1 (logistic fit) |
| `eval/scenarios/*.yaml` | created | 5 standard scenarios |
| `eval/judges/rubric.yaml` | created | Evaluation rubric (fixed) |
| `.claude/settings.local.json` | modified | Hook registration (check_paper_deps + validate_claims) |
| `research/verified/` | created | Empty directory (for marking completed paper reads) |
| `SESSION-LOG.md` | created | This file |

### Decision log

| ID | Decision | Reason | Alternatives | Evidence |
|----|------|------|------|------|
| D1 | Keep 17 agents | Lazy Loading runs 2-4 concurrently. Separation of concerns is the core value | Reduce to 3-6 | [src:paper-B1][src:v2-overall] |
| D2 | MVP-first (3-agent → expand) | Build-all-then-evaluate has high failure risk | Implement all 17 from start | [src:review-C1] |
| D3 | LLM-as-Judge (replacing experts) | Recruiting 3 domain experts is unrealistic | Expert blind review | [src:paper-G2][src:review-C3] |
| D4 | Start All-Sonnet → decide model after experiments | Hegazy vs Li contradiction unresolved. Let data decide | Mixed-Model from the start | [src:paper-A3][src:paper-E3] |
| D5 | Make explicit: Blackboard=data, Phase=control | Resolves "free contribution" vs "enforced order" contradiction | Give one up | [src:review-M4] |
| D6 | Defer RAG to v2, v1 uses web_search | RAG pipeline is itself a project-level effort | Build RAG now | [src:review-M5] |
| D7 | Think in NL, Write in Schema | Forcing JSON drops reasoning by 10-15% | All JSON | [src:paper-I1] |
| D8 | Tag + Cross-Reference Validator | Tags alone cannot verify. Assertion DB is overkill | Assertion DB / tag-only | Pragmatic judgment |
| D9 | Keep all 4 unresolved QOC | Removal cost > retention cost | Remove | [src:qoc-§unresolved] |

### Error log

| ID | Error | Occurred at | Cause | Resolution |
|----|------|----------|------|------|
| E1 | Early research took a "just reduce them" approach without reading v2's intent | Tier 0 research | Didn't read v2's "why separate agents" rationale | User pointed it out → re-analyzed v2 → re-searched papers |
| E2 | First paper-research agent cited papers from memory without actual search | First paper research agent | Agent lacked WebSearch permission | Switched to direct WebSearch |
| E3 | Hook schema error (settings.json) | Hook registration | Incorrect `hooks` array structure (needed nesting) | Fixed using schema error message |
| E4 | Hooks disappeared (settings.local.json overwritten) | During later work | User/system overwrote with permissions-only version | Re-registered |
| E5 | pydantic not installed | experiment_config.py test | Not installed in system Python | pip3 install --break-system-packages |

### Late-session additional work (Session 1, second half)

| File | Action | Content |
|------|------|------|
| `QUESTION-PROTOCOL.md` | created | 6 protocols (session/research/decision/implementation/evaluation/end) |
| `THINKING-MODES.md` | created | Detailed 4 Thinking Modes (BUILD/BREAK/ZOOM/FLIP) |
| `THINKING-MODES-PORTABLE.md` | created | Copy-paste universal prompt (limitations included) |
| `eval/decision_gate.py` | created | BREAK mode hardcoded enforcement (Pydantic ValidationError) |

### Late-session decision log

| ID | Decision | Reason |
|----|------|------|
| D10 | Compressed 15 question patterns → 4 Thinking Modes | Memorizing individual patterns is inefficient. Mode switching naturally generates questions |
| D11 | Hardcode only BREAK, leave the rest as prompts | BREAK is the most easily ignored and most important |
| D12 | Skip Layer-2 semantic validation for now | Covered by Phase 3 MAJ-Eval. Adding now is infrastructure of infrastructure |
| D13 | Current 5-layer system is the best | 60% structural enforcement + 40% prompts. Adding more yields diminishing returns |

### Late-session error log

| ID | Error | Resolution |
|----|------|------|
| E6 | Hooks disappeared again (settings.local.json) | Re-registered. Root cause: another edit overwrote |

### Open items

| ID | Item | Status | Next action |
|----|------|------|----------|
| O1 | research/verified/ empty (12 MUST-READ papers unread) | pending | Read C1, E1, I1 before starting Phase 0.5 |
| O2 | v2 design doc reinforcement 7+4 items not applied | pending | Apply in Phase 0 |
| O3 | validate_claims.py 9 INFO items (untagged numbers) | low | Add tags to Master Plan |
| O4 | pyproject.toml not created | pending | Phase 0 |
| O5 | src/ directory not created | pending | Phase 0 |
| O6 | settings.local.json hooks repeatedly disappear | recurring | Need to find root cause |

---

## Session 2 — 2026-04-15 (paper verification session)

### Summary
Verified citation accuracy of papers-catalog.md and paper-feature-map.json by cross-checking arXiv originals. Spot-checked 6 core papers.

### Change log

| File | Action | Content |
|------|------|------|
| `research/papers-catalog.md` | modified | A1, A2, A3, B1, C1, E2 — refined section numbers, venue names, numbers; added ✅ VERIFIED tag |
| `research/paper-feature-map.json` | modified | Replaced section numbers with verified ones + added `"verified": true` flag |
| `SESSION-LOG.md` | modified | Added Session 2 |

### Verification result (Hallucination Audit)

**Verification method**: directly accessed arXiv originals via WebFetch and cross-referenced

| Paper | Exists | Title | Authors | Key numbers | Section number | Venue |
|------|------|------|------|----------|----------|------|
| A1 Du et al. | ✅ | ✅ | ✅ | ⚠️ 5-10%→7-16pp | ❌ §3→§2 | ✅ ICML 2024 |
| A2 Liang et al. | ✅ | ✅ | ✅ | ✅ | ❌ §3.1/3.2→§1/§2, no Algo1 | ❌ ACL→EMNLP |
| A3 Hegazy | ✅ | ✅ | ✅ | ✅ 91%/82% | ⚠️ table→chart | ✅ |
| B1 Qian et al. | ✅ | ✅ | ✅ | ✅ | ❌ §3/§4→§2/§3.3 | ✅ ICLR 2025 |
| C1 Han & Zhang | ✅ | ✅ | ⚠️ 2 authors not et al. | ✅ | ❌ §3/§4→§3(all)/§4(experiments) | ✅ |
| E2 DeepMind+ | ✅ | ✅ | ⚠️ multi-institution | ✅ 1.724 accurate | ❌ §4/§5→§4.3/§5(Limitations) | ✅ |

**Key findings**:
- All 6 are real papers, titles accurate, key findings mostly accurate
- **Section numbers: 5 of 6 wrong** — typical LLM hallucination pattern
- 1 venue name error (ACL→EMNLP)
- 1 non-existent element (Algorithm 1)

### Error log

| ID | Error | Cause | Resolution |
|----|------|------|------|
| E7 | 5/6 section numbers wrong | LLM guessed "§3 is probably Method" | Corrected via arXiv original cross-reference |
| E8 | A2 venue wrong (ACL→EMNLP) | Memory reliance | Corrected via original |
| E9 | A2 Algorithm 1 does not exist | Memory reliance | Removed |
| E10 | A1 number range underspecified (5-10%→7-16pp) | Memory reliance, approximate description | Replaced with exact numbers |

### Session 2.5 — 2026-04-15 (paper management pipeline construction)

#### Summary
After researching paper management hardcode methods + counter-evidence, built full Level 3 pipeline.
Converted 42 papers to YAML; arXiv/S2 API automatic-verification script found 9 additional hallucinations.

#### Change log

| File | Action | Content |
|------|------|------|
| `research/papers_schema.py` | created | Pydantic schema: PaperEntry (4-state validation) + PaperCatalog + validate_catalog() |
| `research/papers.yaml` | created | Structured YAML for 42 papers (replaces papers-catalog.md) |
| `research/verify_papers.py` | created | arXiv API + Semantic Scholar API automatic verification + auto-fill |

#### Additional hallucinations found by automatic verification

| Paper | Error type | What I wrote | Actual |
|------|----------|-------------|------|
| E2 | first author | Samuel Schmidgall | **Yubin Kim** |
| E7 | first author | Zhao et al. | **Mingyan Gao** |
| H2 | title | Lost in the Haystack | **Hidden in the Haystack: Smaller Needles...** |
| J2 | title | AutoTRIZ | **AutoTRIZ: Automating Engineering Innovation...** |
| J3 | title | TRIZ Agents | **TRIZ Agents: A Multi-Agent LLM Approach...** |
| J6 | title | LLM + MCDM | **One for All: A General Framework...** |
| K1a | title | SwarmBench | **Benchmarking LLMs' Swarm intelligence** |
| K4 | title | LLM-assisted ADD | **An LLM-assisted approach to designing...** |
| K5 | title | CodeAgents | **CodeAgents: A Token-Efficient Framework...** |

#### Research basis (paper management methods)

| Source | Key finding | Supports/refutes |
|------|-----------|----------|
| Citation-error meta-analysis (PMC12285159, 2025) | Human paper citation error rate 16.9%, major 8.0% | Supports — humans fail too, so automation needed |
| GhostCite (arXiv:2602.06718) | LLM citation hallucination 14-95% | Supports — API verification required |
| SemanticCite (arXiv:2511.16198) | AI citation verification 4-stage classification | Supports — automation feasible |
| Ioannidis (2016) Milbank Q | Mechanical systematization → itself becomes waste | Refutes — warns against over-infrastructure |
| Cognitive Debt (Storey 2025) | Over-automation → deep reading is skipped | Refutes — must not replace reading |
| Automation Bias (PubMed 2016) | Complex verification → blind trust | Refutes — keep it simple |

### Open items

| ID | Item | Status | Next action |
|----|------|------|----------|
| O7 | 36 papers unverified | high | Verify the relevant paper at implementation time |
| O8 | E1, E3-E6, F1, G1, G2, H1, I1 section numbers unverified | high | verify_papers.py cannot verify section content — needs manual |
| O9 | E9 arXiv ID invalid | medium | Find the correct ID |
| O10 | verified/*.md files not created (including 6 verified) | low | Create at implementation time |
| O11 | Semantic Scholar rate limit (429) | low | Get API key or increase delay |

---

## Logging rules

At each session start:
1. Check "next steps" from the previous session
2. Add this session's log section (Session N — date)

At each session end:
1. Change log: files created/modified/deleted
2. Decision log: decisions made + reasons + alternatives + evidence [src:]
3. Error log: errors that occurred + cause + resolution
4. Open items: things not yet done
5. Next steps: concrete actions
