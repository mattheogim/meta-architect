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

**이 프로젝트의 기능은 특정 논문에 근거한다. 논문을 안 읽고 구현하면 hallucination이다.**

논문 기반 기능을 구현할 때:
1. `research/paper-feature-map.json`에서 해당 기능의 `required_papers`를 확인
2. 각 논문의 arxiv HTML 또는 PDF를 `WebFetch`/`Read`로 **직접 읽기**
3. 핵심 수치/알고리즘을 원문에서 추출하여 코드 주석에 인용
4. "기억"이나 "요약"에 의존하지 말 것 -- 반드시 원문 확인
5. `research/verified/{paper_id}.md`에 읽기 완료 기록 남기기

**위반 시**: `research/check_paper_deps.py` hook이 경고를 발생시킨다.

## 6. Experiment Protocol

**모든 시스템 실행은 ExperimentRunner를 통해야 한다.**

- `meta_architect.run()` 직접 호출 금지 — `ExperimentRunner.run(config)`만 허용
- 모든 실행은 `eval/experiments/{EXP}/runs/`에 자동 저장
- 실행 후 metrics 자동 계산 + LLM-as-Judge 자동 평가
- 논문 테이블/그래프 재생성: `python eval/paper/generate_tables.py`
- `PRE-REGISTRATION.md` 확정 후 가설/분석 계획 수정 금지 (HARKing 방지)
- 사후 변경은 반드시 `DEVIATIONS.md`에 기록

## 7. 4 Thinking Modes

모든 작업에서 4가지 모드를 의식적으로 전환한다. 상세: `THINKING-MODES.md`

```
BUILD (만들어)  →  설계, 구현, 플랜
BREAK (부숴봐)  →  공격, 반박, 리스크. "이게 실패했다면 왜?"
ZOOM  (더 봐)   →  빠진 것, 다음 단계. "안 물어본 질문은?"
FLIP  (뒤집어)  →  반대, 가정 의심. "최악으로 만들려면?"
```

적용 기준:
- **Type 1 결정** (되돌리기 어려움): BUILD + BREAK + FLIP 전부
- **Type 2 결정** (되돌리기 쉬움): BUILD만. 바로 실행.
- 판단: "이걸 잘못 정하면 1주일 이상 되돌리기 어려운가?"
- **절대 하면 안 되는 것**: BUILD만 하고 BREAK를 안 하기 (confirmation bias)

## 8. Claim Tagging (Hallucination 방지)

**모든 핵심 주장에 출처 + 유형 + 검증 상태 태그를 붙인다.**

문서(설계서, 플랜, 리서치)에 주장을 쓸 때:
- `[src:X]` — 출처 (예: `[src:paper-A1]`, `[src:v2-§3.1]`, `[src:deep-3]`)
- `[FACT]` / `[DECISION]` / `[ASSUMPTION]` / `[DERIVED]` / `[EMPIRICAL]` — 주장 유형
- `[VERIFIED]` / `[UNVERIFIED]` — 검증 상태

규칙:
- 수치가 있으면 반드시 `[src:]` — "91%"는 어디서 나온 91%인가?
- `[UNVERIFIED]` 수치로 코드를 짜지 말 것
- 태그 없는 주장 = hallucination 후보 → 리뷰 시 우선 확인
- 상세 규칙: `research/TAGGING-SYSTEM.md`

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, clarifying questions come before implementation rather than after mistakes, and every claim has a traceable source.
