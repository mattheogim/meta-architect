# PRE-REGISTRATION — Meta Architect Experiment

> **STATUS: DRAFT** — Finalize before first experiment run.
> After finalization, this document MUST NOT be modified. 
> Any post-hoc changes constitute HARKing (Hypothesizing After Results are Known).
> 
> Git commit hash at finalization: [TO BE FILLED]

---

## 1. Hypotheses

### H1 (Primary): Forced Cognitive Diversity
The Meta Architect system (17 specialized LLM agents with forced cognitive diversity
via Blackboard pattern) produces software architecture designs that cover more
perspectives (measured by concept coverage) and achieve higher quality scores
(measured by LLM-as-Judge) than a single LLM agent with equivalent instructions.

- **Directional**: Meta Architect > Single Agent on both Coverage and Quality
- **Test**: Paired t-test on Coverage and Quality scores
- **Significance level**: alpha = 0.05

### H2 (Secondary): Logistic Scaling
Architecture design quality follows a logistic growth pattern as the number of
agents increases from 1 to 17, with collaborative emergence occurring in the
3-6 agent range.

- **Directional**: Quality = L / (1 + exp(-k(N - N0))) where N = agent count
- **Test**: Logistic regression fit, report R-squared
- **Reference**: Qian et al. (ICLR 2025, arXiv:2406.07155)

### H3 (Secondary): Adversarial Challenge Value
Including an adversarial challenge phase (Phase 4: Simplicity Advocate + Risk Analyst)
produces more feasible architecture designs than skipping directly to decision.

- **Directional**: With Phase 4 > Without Phase 4 on Feasibility Score
- **Test**: Paired t-test
- **Significance level**: alpha = 0.05

### H4 (Secondary): Model Diversity
Using different LLM models across agents (mixed configuration) produces more
unique perspectives than using the same model for all agents (homogeneous),
while the quality difference depends on model capability distribution.

- **Directional**: Mixed > Homogeneous on Unique Perspective Count
- **Directional**: Quality difference depends on model mix (exploratory)
- **Test**: Paired t-test on perspectives; descriptive analysis on quality
- **Reference**: Hegazy (2024, arXiv:2410.12853) vs Li et al. (2025, arXiv:2502.00674)

---

## 2. Experimental Design

### Independent Variables
| Variable | Levels | Experiment |
|----------|--------|------------|
| Agent count | 1, 3, 6, 10, 17 | EXP-SCALE |
| Agent removed | Each of 17 agents | EXP-ABLATION |
| Phase 4 enabled | True, False | EXP-CHALLENGE |
| Model config | all-opus, mixed, all-sonnet | EXP-MODEL |

### Dependent Variables
| Variable | Measurement | Source |
|----------|-------------|--------|
| Concept Coverage | 60+ keyword checklist match | auto_measure.py |
| Quality Score | LLM-as-Judge aggregate (1-5) | maj_eval.py |
| Feasibility Score | Architect judge feasibility (1-5) | maj_eval.py |
| Unique Perspectives | Concepts unique to condition | auto_measure.py |
| Challenge Rate | Actionable challenges / total | auto_measure.py |
| Cost | USD from token counts | auto_measure.py |
| Latency | Wall clock seconds | auto_measure.py |

### Controls (Fixed)
- Temperature: 0.7
- Seed: 42
- Max tokens per agent: 4096
- Max global rounds: 50
- Runs per condition: 3
- Judge model: Claude Opus (independent instance)
- Scenarios: 5 fixed (see eval/scenarios/)

---

## 3. Analysis Plan

### For H1 (Primary)
1. Compute mean Coverage and Quality for 17-agent and 1-agent conditions
2. Paired t-test (paired by scenario and repetition)
3. Report: t-statistic, p-value, Cohen's d effect size
4. If p < 0.05 and d > 0.5: H1 supported

### For H2
1. Plot agent count (x) vs mean Quality (y) for EXP-SCALE
2. Fit logistic curve: Q = L / (1 + exp(-k(N - N0)))
3. Report: L, k, N0 parameters, R-squared
4. Compare with Qian et al.'s collaborative scaling law shape

### For H3
1. Compute mean Feasibility for with-phase4 and without-phase4
2. Paired t-test
3. Also report Challenge Rate (descriptive)

### For H4
1. Compute mean Unique Perspectives for mixed vs all-opus vs all-sonnet
2. One-way ANOVA + Tukey HSD post-hoc
3. Descriptive comparison of Quality and Cost

---

## 4. Sample Size Justification
- 5 scenarios x 3 repetitions = 15 data points per condition
- For paired t-test with alpha=0.05, power=0.8, d=0.8 (large effect):
  Minimum n = 15 (sufficient)
- For logistic regression (5 data points on x-axis, 15 each):
  Exploratory — report R-squared, no formal power analysis

---

## 5. Stopping Rules
- All 252 runs must complete before analysis begins
- If API failure rate > 20%, investigate and restart failed runs
- Missing data: exclude run, note in paper

---

## 6. Deviations
Any deviation from this plan must be:
1. Documented in a DEVIATIONS.md file
2. Explicitly labeled as exploratory (not confirmatory) in the paper
3. Git committed with message "DEVIATION: [reason]"
