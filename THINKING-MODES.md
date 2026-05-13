# 4 Thinking Modes

> No need to memorize 15 question patterns. Just switch between 4 modes.
> Once you enter a mode, the questions emerge naturally.

```
        BUILD                    BREAK
     "create"                  "attack"
    ┌──────────┐           ┌──────────┐
    │ implement│           │ attack   │
    │ design   │ ───────── │ counter  │
    │ plan     │           │ risk     │
    └──────────┘           └──────────┘
         │                      │
         └──────────┬───────────┘
                    │
        ZOOM                     FLIP
     "look further"            "reverse"
    ┌──────────┐           ┌──────────┐
    │ expand   │           │ opposite │
    │ contract │ ───────── │ shift    │
    │ connect  │           │ question │
    └──────────┘           └──────────┘
```

---

## MODE 1: BUILD (create)

> **When**: early ideation, planning, starting implementation

| Question | Effect |
|------|------|
| "Generate 20 questions first. Pick 3 and start there." | Prevents jumping in without direction |
| "What's the simplest way?" | Prevents over-engineering |
| "Explain this to a 5-year-old." | Reveals what you don't know |
| "Rate 1-10. What would make it an 8?" | Vague state → concrete improvement |

**Core of this mode**: Build, but simply. Stop if you don't understand.

---

## MODE 2: BREAK (attack)

> **When**: after design completion, right after a decision, during review

| Question | Effect |
|------|------|
| "This failed. Why?" (Pre-mortem) | Breaks optimism bias. 30% more accurate failure causes |
| "An adversary saw this. Top 3 strongest attack points?" | Forces strongest counter |
| "Find opposing papers too" | Prevents confirmation bias |
| "If you wanted to deliberately break this, where?" | Vulnerabilities surface immediately |
| "If an ICSE reviewer rejected it, top 3 reasons?" | Identifies academic weaknesses |

**Core of this mode**: Break what you built yourself. If it doesn't break, it's real.

---

## MODE 3: ZOOM (look further)

> **When**: feeling like something is missing, checking the big picture, checking details

| Question | Effect |
|------|------|
| "Top 5 most important questions I haven't asked?" | Discovers blind spots |
| "Assume this works. What's the next problem?" (Second-order) | Looks beyond stage 1 |
| "Scale this 10x? Shrink to 1/10?" | Structural issues emerge from scale change |
| "If we don't do this, what's the biggest risk?" | Automatic priority setting |

**Core of this mode**: See beyond what's visible. What you can't see is most dangerous.

---

## MODE 4: FLIP (reverse)

> **When**: stuck, need a new perspective, questioning assumptions

| Question | Effect |
|------|------|
| "How to make this worst possible? Do the opposite." (Inversion) | Reverse direction is faster than forward |
| "Choosing A means you can't do what?" (Opportunity cost) | "What you lose" beats "what you gain" |
| "What do we take for granted that's actually wrong?" | Exposes hidden assumptions |
| "Attack at contentiousness 9/10" | Weak critique → strongest counter |

**Core of this mode**: Flip the premise. Question the obvious.

---

## Which mode when?

```
Project start
  │
  ├── BUILD: "20 questions → pick 3 → plan"
  │
  ├── Design complete ──→ BREAK: "If this failed, why?"
  │                    │
  │                    └── FLIP: "What's the simplest alternative?"
  │
  ├── Something feels missing ──→ ZOOM: "5 questions I haven't asked?"
  │
  ├── During implementation ──→ BUILD: "Can I explain in one sentence?"
  │                │
  │                └── BREAK: "How to break this?"
  │
  ├── Stuck ──→ FLIP: "How to make this worst? Reverse"
  │
  ├── Evaluation ──→ BREAK: "Top 3 reject reasons"
  │              │
  │              └── ZOOM: "What's the next problem?"
  │
  └── End of session ──→ ZOOM: "What's the most important thing not covered?"
```

---

## Combining with Type 1 / Type 2

```
When making a decision:
  "Would it take more than 1 week to reverse if wrong?"
  
  YES (Type 1) → all of BUILD + BREAK + FLIP
                  OK to take time
  
  NO  (Type 2) → BUILD only
                  Execute immediately, fix if wrong
```

---

## Actual mode switches in this session

```
BUILD: "Where are we?" → "Make a plan"
FLIP:  "Doubt everything" → "Is Blackboard the best?"  
BREAK: "Find counter papers too" → "Evaluate the plan itself"
ZOOM:  "Anything missing?" → "Anything else to research?"
BUILD: "Codify it" → "Implement the experiment framework"
FLIP:  "Is this questioning method itself correct?"  ← we are here now
```

You were naturally cycling through all 4 modes.
The difference: consciously switching modes means **no mode gets skipped.**
Most people stay in BUILD and skip BREAK/FLIP. You're already using all of them.
