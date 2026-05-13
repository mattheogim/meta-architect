# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" -> "Write tests for invalid inputs, then make them pass"
- "Fix the bug" -> "Write a test that reproduces it, then make it pass"
- "Refactor X" -> "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] -> verify: [check]
2. [Step] -> verify: [check]
3. [Step] -> verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 5. Paper-Based Implementation Rule

**This project's features are grounded in specific papers. Implementing without reading the paper is hallucination.**

When implementing paper-based features:
1. Check `required_papers` for the feature in `research/paper-feature-map.json`
2. **Directly read** each paper's arxiv HTML or PDF via `WebFetch`/`Read`
3. Extract key numbers/algorithms from the original text and cite in code comments
4. Do not rely on "memory" or "summaries" — always verify against the original
5. Record reading completion in `research/verified/{paper_id}.md`

**On violation**: The `research/check_paper_deps.py` hook raises a warning.

## 6. Experiment Protocol

**All system runs must go through ExperimentRunner.**

- No direct `meta_architect.run()` calls — only `ExperimentRunner.run(config)` is allowed
- All runs are auto-saved to `eval/experiments/{EXP}/runs/`
- After each run: automatic metrics computation + automatic LLM-as-Judge evaluation
- Regenerate paper tables/figures: `python eval/paper/generate_tables.py`
- Do not modify hypotheses/analysis plan after `PRE-REGISTRATION.md` is finalized (HARKing prevention)
- Any post-hoc changes must be recorded in `DEVIATIONS.md`

## 7. 4 Thinking Modes

Consciously switch between 4 modes in all work. Details: `THINKING-MODES.md`

```
BUILD (create)  →  design, implement, plan
BREAK (attack)  →  attack, counter, risk. "If this failed, why?"
ZOOM  (look further)  →  what's missing, what's next. "What question haven't I asked?"
FLIP  (reverse)  →  opposite, question assumptions. "How to make this worst?"
```

Application criteria:
- **Type 1 decisions** (hard to reverse): all of BUILD + BREAK + FLIP
- **Type 2 decisions** (easy to reverse): BUILD only. Execute immediately.
- Judgment: "Would it take more than 1 week to reverse if wrong?"
- **Never do**: BUILD only without BREAK (confirmation bias)

## 8. Claim Tagging (Hallucination Prevention)

**Every core claim gets a source + type + verification status tag.**

When writing claims in documents (design docs, plans, research):
- `[src:X]` — source (e.g., `[src:paper-A1]`, `[src:v2-§3.1]`, `[src:deep-3]`)
- `[FACT]` / `[DECISION]` / `[ASSUMPTION]` / `[DERIVED]` / `[EMPIRICAL]` — claim type
- `[VERIFIED]` / `[UNVERIFIED]` — verification status

Rules:
- Any number must have `[src:]` — where does the "91%" come from?
- Do not write code based on `[UNVERIFIED]` numbers
- Untagged claim = hallucination candidate → check first during review
- Detailed rules: `research/TAGGING-SYSTEM.md`

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, clarifying questions come before implementation rather than after mistakes, and every claim has a traceable source.
