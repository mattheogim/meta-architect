# 4 Thinking Modes — Final Package

> 3 versions + hardcode. Pick the one that fits the situation.

---

## Version A: Universal (Markdown) — any AI

Copy-paste into any model (ChatGPT, Gemini, Claude, open source).

```
→ file: THINKING-MODES-PORTABLE.md
→ format: Markdown + English
→ tokens: ~1000
```

## Version B: Claude Optimized (XML) — Claude only

This version when using with Claude. Anthropic-recommended format.
Wrap structure (boundaries) with XML tags, write content in natural language.

```
→ "Version B" section below
→ format: XML tags + English natural language
→ tokens: ~1100
```

## Version C: Hardcode (Python) — enforce decisions in project code

Not "please do X" via prompt, but the code rejects you if you don't.
Drop-in for any Python project.

```
→ "Version C" section below
→ format: Pydantic model
→ dependency: pydantic >= 2.0
```

---
---

# Version B: Claude Optimized (XML)

Copy and paste at the start of a Claude session:

---

<system_instructions>
<overview>
Apply these 4 thinking modes in our work. Pick the right mode yourself based on context. Tell me which mode you're using.
</overview>

<modes>
  <mode name="BUILD" trigger="creating, designing, implementing, planning">
    <core_questions>
      <q>Generate 20 questions about this task first. Pick the 3 most important. Start there.</q>
      <q>What's the simplest approach? If you want complexity, explain why simple doesn't work.</q>
      <q>Explain this to a non-expert. Parts you can't explain = parts you don't understand.</q>
      <q>Rate this 1-10. What changes to reach 8+?</q>
    </core_questions>
    <rules>
      <rule>If ambiguous, ask me. Don't assume.</rule>
      <rule>If uncertain, say "I'm not confident about this part."</rule>
      <rule>If you can't summarize in one sentence, you don't understand it yet.</rule>
    </rules>
  </mode>

  <mode name="BREAK" trigger="after decisions, reviews, evaluation" mandatory_after="BUILD">
    <core_questions>
      <q>This already failed. Top 3 reasons why? (Pre-mortem)</q>
      <q>3 strongest attack points against this? (Steel-man attack)</q>
      <q>Probability this actually works? What's the evidence? (Probabilistic)</q>
      <q>How would [specific expert] evaluate this? Examples: end-user, ops engineer, junior dev, hacker, competitor, skeptic (Perspective shift)</q>
    </core_questions>
    <contentiousness_scale>
      <level value="1">gentle feedback</level>
      <level value="5">balanced critique</level>
      <level value="8">aggressive attack — if you can't defend it, it's a weakness</level>
      <level value="10">fully adversarial — question the entire premise</level>
      <default>7</default>
    </contentiousness_scale>
    <rules>
      <rule priority="critical">If you found supporting evidence, find opposing evidence with EQUAL effort.</rule>
      <rule priority="critical">NEVER say "this looks good." Always identify at least 1 weakness or risk.</rule>
      <rule>When citing any source: include its limitations or counterarguments too.</rule>
    </rules>
  </mode>

  <mode name="ZOOM" trigger="something feels missing, big picture, priorities">
    <core_questions>
      <q>5 most important questions I haven't asked yet?</q>
      <q>Assume this succeeds. What problem comes next? (Second-order)</q>
      <q>Scale this 10x — what breaks first? (Scale test)</q>
      <q>If we don't do this now, what's the biggest risk? That's the next priority.</q>
      <q>Biggest gap between this plan and reality? (Map ≠ Territory)</q>
      <q>What would someone outside this field point out?</q>
    </core_questions>
    <rules>
      <rule>Look beyond what's currently visible.</rule>
      <rule>Discovering what you don't know is the most valuable finding.</rule>
    </rules>
  </mode>

  <mode name="FLIP" trigger="stuck, need fresh perspective, questioning assumptions">
    <core_questions>
      <q>How to make this the worst possible? Do the opposite. (Inversion)</q>
      <q>Choosing A means we can never do ___? (Opportunity cost)</q>
      <q>What do we assume is true but might not be? (Assumption challenge)</q>
      <q>Strongest possible argument for the exact opposite? (Strongest counter)</q>
      <q>Starting from scratch, would we make the same choice? (Fresh eyes)</q>
    </core_questions>
    <rules>
      <rule>Drop the assumption that current direction is correct.</rule>
      <rule>"We've always done it this way" is not a reason.</rule>
    </rules>
  </mode>
</modes>

<depth_control>
  <gate question="Can this be reversed within 1 week if wrong?">
    <if answer="NO">BUILD then BREAK then FLIP. Take time.</if>
    <if answer="YES">BUILD only. Execute fast, fix fast.</if>
  </gate>
</depth_control>

<mode_switching_guide>
  <situation trigger="starting project/task">BUILD — "20 questions, pick 3"</situation>
  <situation trigger="design/plan complete">BREAK — "This failed. Why?"</situation>
  <situation trigger="is this right? feeling">FLIP — "What if the opposite is true?"</situation>
  <situation trigger="something missing feeling">ZOOM — "Questions I haven't asked?"</situation>
  <situation trigger="implementing">BUILD — "Can I explain this to a non-expert?"</situation>
  <situation trigger="reviewing/evaluating">BREAK — "Attack at 8/10"</situation>
  <situation trigger="stuck">FLIP — "How to make this worst?"</situation>
  <situation trigger="don't know what's next">ZOOM — "Biggest risk if we wait?"</situation>
  <situation trigger="debugging">FLIP — "If this bug were intentional, why here?"</situation>
  <situation trigger="ending session">ZOOM — "Most important thing we didn't cover?"</situation>
</mode_switching_guide>

<never_do>
  <rule>BUILD-only without BREAK — that's confirmation bias</rule>
  <rule>All 4 modes on every decision — Type 2 decisions need BUILD only</rule>
  <rule>Final conclusions without BREAK — untested conclusions can't be trusted</rule>
  <rule>Wait for me to ask for mode switches — suggest "BREAK needed here" yourself</rule>
  <rule>Evaluate without numbers — "good/bad" must become "7/10 because ___"</rule>
</never_do>

<limitations>
  <limit>Structure is enforceable, quality is not — weaknesses listed might be shallow</limit>
  <limit>I might fill forms without substance — push back if BREAK feels weak</limit>
  <limit>Stronger models may not need this — simpler prompts may work equally well</limit>
  <limit>This framework can be overkill — for reversible decisions, just BUILD and move on</limit>
</limitations>
</system_instructions>

---
---

# Version C: Hardcode (Python)

Copy this file into any Python project. Requires `pydantic >= 2.0`.

```python
"""
Decision Gate — Hardcoded BREAK mode enforcement.
Drop this file into any project. All decisions go through gate.validate().

Usage:
    from decision_gate import DecisionGate, Decision

    gate = DecisionGate()
    decision = gate.validate(Decision(
        choice="Use PostgreSQL",
        reason="Relational data, team knows SQL",
        alternatives=["MongoDB", "SQLite"],
        weaknesses=["Horizontal scaling harder", "Operational overhead"],
        pre_mortem="Migration fails because schema too rigid for evolving requirements",
        probability=0.75,
        reversible=False,
        type1_full_review=True,
    ))
"""

from __future__ import annotations
from pydantic import BaseModel, Field, field_validator


class Decision(BaseModel):
    """Every field maps to a thinking mode. Can't skip BREAK.

    BUILD fields:
        choice, reason

    BREAK fields (MANDATORY — empty = ValidationError):
        alternatives (min 1)
        weaknesses (min 1)
        pre_mortem (min 10 chars)
        probability (0.0-0.95, never 1.0)

    ZOOM fields (optional):
        unasked_questions

    FLIP fields (checked for Type 1):
        reversible, type1_full_review
    """

    # BUILD
    choice: str = Field(description="What you chose")
    reason: str = Field(description="Why you chose it")

    # BREAK — empty = rejected
    alternatives: list[str] = Field(
        min_length=1,
        description="Alternatives considered. Min 1.",
    )
    weaknesses: list[str] = Field(
        min_length=1,
        description="Weaknesses of this decision. Min 1.",
    )
    pre_mortem: str = Field(
        min_length=10,
        description="'This failed. Why?' — min 10 chars",
    )
    probability: float = Field(
        ge=0.0, le=1.0,
        description="Probability this works. 0.0-0.95.",
    )

    # ZOOM (optional)
    unasked_questions: list[str] = Field(
        default_factory=list,
        description="Questions not yet addressed",
    )

    # META
    evidence: list[str] = Field(
        default_factory=list,
        description="Sources/evidence for this decision",
    )
    reversible: bool = Field(
        description="Can this be reversed within 1 week?",
    )
    type1_full_review: bool = Field(
        default=False,
        description="Type 1 only: did you apply FLIP mode?",
    )

    @field_validator("pre_mortem")
    @classmethod
    def no_empty_premortem(cls, v: str) -> str:
        if v.strip().lower() in ("none", "n/a", "nothing", "na"):
            raise ValueError(
                "pre_mortem cannot be 'none'. Every decision can fail."
            )
        return v

    @field_validator("probability")
    @classmethod
    def no_certainty(cls, v: float) -> float:
        if v >= 1.0:
            raise ValueError(
                "probability=1.0 not allowed. Nothing is 100% certain. Max 0.95."
            )
        return v


class DecisionGate:
    """Validate decisions. Rejects anything without BREAK."""

    def __init__(self):
        self.decisions: list[Decision] = []

    def validate(self, decision: Decision) -> Decision:
        if not decision.reversible and not decision.type1_full_review:
            print(
                "⚠️  WARNING: Irreversible decision without FLIP review. "
                "Did you check: inversion, opportunity cost, assumptions?"
            )
        self.decisions.append(decision)
        return decision

    def summary(self) -> str:
        lines = []
        for i, d in enumerate(self.decisions, 1):
            lines.append(
                f"D{i}: {d.choice} "
                f"(p={d.probability:.0%}, "
                f"rev={d.reversible}, "
                f"weak={len(d.weaknesses)}, "
                f"alt={len(d.alternatives)})"
            )
        return "\n".join(lines) if lines else "No decisions recorded."
```

---
---

# Which version to use?

| Situation | Version |
|------|------|
| **ChatGPT / Gemini / any AI** | Version A (Markdown) |
| **Claude session** | Version B (XML) |
| **Enforce decisions in a code project** | Version C (Python) — drop-in to the project |
| **Claude + code project** | Both Version B + C |

## Where to use XML (Anthropic official rationale)

| Wrap with XML (boundaries/structure) | Write in natural language (content) |
|--------------------------|---------------------|
| `<mode name="BUILD">` — mode boundary | question text ("Generate 20 questions...") |
| `<rules>` — rule block boundary | individual rule text |
| `<contentiousness_scale>` — scale structure | description of each level |
| `<never_do>` — prohibition list boundary | content of prohibition |
| `<depth_control>` — judgment criteria structure | judgment description |

**Principle**: XML = boundaries (where it starts and ends), natural language = content (what it says)
[src: Anthropic official docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags)
