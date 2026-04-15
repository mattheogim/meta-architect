# Hallucination 방지 태깅 시스템

> 긴 문서에서 모든 주장(claim)의 출처와 검증 상태를 추적한다.
> LLM이 이 문서를 읽을 때 "이건 어디서 나온 말인가?"를 즉시 판단할 수 있게 한다.

---

## 1. 소스 태그 `[src:...]`

모든 주장에 출처를 붙인다.

| 태그 | 의미 | 예시 |
|------|------|------|
| `[src:v2-§3.1]` | v2 설계서 3.1절 | "자기검증 금지 원칙 [src:v2-§3.1]" |
| `[src:paper-A1]` | 논문 카탈로그 A1 | "토론이 사실성 향상 [src:paper-A1]" |
| `[src:deep-3]` | Deep Research 3번 | "Spearman 0.47 [src:deep-3]" |
| `[src:qoc-Q5]` | QOC 의사결정 기록 Q5 | "에이전트 실패 프로토콜 [src:qoc-Q5-4]" |
| `[src:review-C1]` | Plan Review C1 | "MVP 없으면 실패 [src:review-C1]" |
| `[src:exp-design]` | 실험 설계 문서 | "252회 [src:exp-design]" |
| `[src:code-eval/X]` | 실제 코드 파일 | "ExperimentRunner [src:code-eval/experiment_runner.py]" |

## 2. 주장 유형 태그

| 태그 | 의미 | 검증 방법 |
|------|------|----------|
| `[FACT]` | 논문/외부 출처에서 온 사실 | 원문 확인 가능 |
| `[DECISION]` | 우리의 설계 결정 | QOC/이유 추적 가능 |
| `[ASSUMPTION]` | 아직 검증 안 된 가정 | 실험으로 검증 필요 |
| `[DERIVED]` | 사실에서 논리적으로 도출 | 추론 chain 확인 |
| `[EMPIRICAL]` | 우리 실험 데이터에서 나옴 | eval/experiments/ 데이터 |

## 3. 검증 상태 태그

| 태그 | 의미 |
|------|------|
| `[VERIFIED]` | research/verified/{id}.md 존재. 원문 직접 확인 완료 |
| `[UNVERIFIED]` | 논문 요약/검색 결과에서만 확인. 원문 미확인 |
| `[STALE]` | 이전에 확인했지만 상황이 변했을 수 있음 |

## 4. 복합 사용 예시

```markdown
Phase 4 에이전트는 반드시 대안을 1개 이상 제시해야 한다.
[DECISION][src:review-C1][src:paper-A2] 
이유: LLM은 한번 확신하면 self-reflection으로 사고 전환 불가 (DoT 문제)
[FACT][src:paper-A2][UNVERIFIED]
```

```markdown
에이전트 수 스케일링은 로지스틱 성장을 따른다.
[FACT][src:paper-B1][UNVERIFIED]
구체적 수식은 원문 확인 필요.
```

```markdown
3-agent MVP가 1-agent보다 Coverage 10%+ 높을 것이다.
[ASSUMPTION] Phase 0.5에서 검증.
```

## 5. 규칙

1. **모든 핵심 주장에 최소 1개 태그** 필수
2. **수치가 있으면 반드시 `[src:]`** — "91%" → 어디서 나온 91%?
3. **`[UNVERIFIED]` 수치로 코드를 짜지 말 것** — `[VERIFIED]`만 코드 주석에 사용
4. **`[ASSUMPTION]`은 PRE-REGISTRATION.md에도 기록** — 검증 대상임을 명시
5. **태그가 없는 주장 = hallucination 가능성** — 리뷰 시 태그 없는 문장 우선 확인
