# Question Protocol — automated question checklist

> Question protocol automatically applied every session, every Phase, every decision.
> Instead of the user manually asking "find counter-evidence too", "anything missing?" every time,
> this protocol is registered in CLAUDE.md and applied automatically.

---

## 1. Session start protocol

When a new session begins, **automatically** do the following:

```
[ ] Read NEXT-SESSION.md
[ ] Check the previous session in SESSION-LOG.md
[ ] Pre-mortem: "If this session's goal failed, why?"
[ ] Unasked questions: "Top 3 most important questions not yet addressed?"
```

## 2. Research protocol

When investigating something, **automatically** look at both sides:

```
Stage 1 (diverge): collect every possible approach/perspective — without filter
Stage 2 (support): evidence supporting this approach (papers, cases, data)
Stage 3 (counter): evidence opposing this approach — with equal effort, mandatory
Stage 4 (converge): synthesize both sides into a conclusion. Note contradictions
Stage 5 (invert): "How would you make this worst?" — Inversion check
```

**Never stop after stage 2. Research without stage 3 is confirmation bias.**

## 3. Decision protocol

When making a decision, **automatically** check:

```
[ ] 5 Whys: "Why this decision?" × 5 — reach the root reason
[ ] Inversion: "What's good about choosing the opposite?"
[ ] Pre-mortem: "This decision failed 6 months later. Biggest reason?"
[ ] Tag: attach [DECISION][src:source]
[ ] Record in SESSION-LOG.md decision log
```

## 4. Implementation protocol

When writing code, **automatically** check:

```
[ ] Have you read the paper? (check_paper_deps.py hook)
[ ] Feynman: "Can you explain what this code does in one sentence?"
[ ] 5 Hows: "How would you test this?" → "How would you break this?"
[ ] Is this the simplest implementation? (CLAUDE.md §2)
```

## 5. Evaluation protocol

When evaluating something, **automatically**:

```
[ ] Self-rating: score out of 10 + rationale
[ ] Reject reason: "If you were an ICSE reviewer, why would you reject this?"
[ ] What's missing: "What's the most important thing not addressed in this evaluation?"
[ ] Compare: "Compared to the simplest alternative?"
```

## 6. Session end protocol

At the end of a session, **automatically**:

```
[ ] Update SESSION-LOG.md (changes/decisions/errors/open items)
[ ] Update NEXT-SESSION.md
[ ] Unasked questions: "What's the most important thing not addressed this session?"
[ ] git commit + push (on request)
```
