# Meta Architect — Master Plan v2

> v2 설계서 + 45+ 논문 + Deep Research 8건 + Plan Review + 실험 프레임워크를 종합한 최종 실행 계획.
> v1 플랜의 19개 수정 항목을 반영함. (이전 버전: MASTER-PLAN-v1.md)
>
> **원칙**: "아이디어를 넣으면, 내가 모르는 것까지 포함해서 최적의 구조를 제안해주는 시스템"
> **방법론**: 만드는 과정 = 실험 데이터 수집 과정. 구현과 검증을 분리하지 않는다.
> **Hallucination 방지**: 모든 핵심 주장에 `[src:]` + `[FACT/DECISION/ASSUMPTION]` + `[VERIFIED/UNVERIFIED]` 태그. 상세: `research/TAGGING-SYSTEM.md`

---

## 0. 현재 상태 + 프로젝트 구조

### 완료된 것
- ✅ v2 설계서 (1,852줄) — `v2/meta-architect-v2.md`
- ✅ QOC 의사결정 기록 — `v2/meta-architect-v2-qoc.md`
- ✅ 논문 리서치 45+ — `research/papers-catalog.md`
- ✅ Deep Research 8건 — `research/deep-*.md`
- ✅ 60+ 개념 LLM 적용 가능성 검증 — `research/00-research-index.md`
- ✅ 논문 기반 구현 강제 시스템 — `CLAUDE.md` §5 + `research/check_paper_deps.py` + hook
- ✅ 실험 프레임워크 코드화 — `eval/` 전체 (runner, measure, judge, scenarios, tables)
- ✅ Pre-registration — `PRE-REGISTRATION.md`
- ✅ 플랜 자체 평가 — `research/MASTER-PLAN-REVIEW.md`

### 남은 것
- ⬜ v2 설계서 보강 7개 항목 반영
- ⬜ 프로젝트 셋업 (pyproject.toml, src/)
- ⬜ 3-agent MVP 구현 + 첫 번째 실험 데이터
- ⬜ 점진적 확장 → 17-agent
- ⬜ 전체 실험 252회 실행
- ⬜ 논문 작성

### 현재 파일 구조
```
meta-architect/
├── CLAUDE.md                              ← 행동 가이드라인 + 논문 강제 + 실험 프로토콜
├── PRE-REGISTRATION.md                    ← 가설 H1~H4 사전 등록 (수정 금지)
├── README.md
├── .claude/settings.local.json            ← hook 등록
│
├── v1/meta-architect-v1.md                ← 원본 설계서
├── v2/
│   ├── meta-architect-v2.md               ← 현재 최종 설계서 (보강 대상)
│   └── meta-architect-v2-qoc.md           ← QOC 의사결정 기록
│
├── research/
│   ├── 00-research-index.md               ← 전체 리서치 인덱스
│   ├── papers-catalog.md                  ← 45+ 논문 (섹션별, MUST-READ 표시)
│   ├── paper-feature-map.json             ← 기능↔논문 매핑 (11개 기능)
│   ├── check_paper_deps.py                ← pre-implementation 체크 스크립트
│   ├── verified/                          ← 논문 읽기 완료 마킹
│   ├── deep-1-prototype-validator.md
│   ├── deep-2-measuring-blind-spots.md
│   ├── deep-3-llm-as-judge.md
│   ├── deep-4-convergence.md
│   ├── deep-5-long-context-vs-multiagent.md
│   ├── deep-6-precedent-rag.md
│   ├── deep-7-output-format.md
│   ├── deep-8-multi-model.md
│   ├── MASTER-PLAN.md                     ← 이 파일
│   ├── MASTER-PLAN-v1.md                  ← 이전 버전
│   ├── MASTER-PLAN-REVIEW.md              ← 플랜 자체 평가
│   └── EXPERIMENT-DESIGN.md               ← 논문용 실험 설계
│
├── eval/                                  ← ✅ 이미 코드화됨
│   ├── experiment_config.py               ← 252회 매트릭스 생성
│   ├── experiment_runner.py               ← 실행 wrapper (유일한 진입점)
│   ├── auto_measure.py                    ← 자동 측정 (coverage, cost 등)
│   ├── maj_eval.py                        ← LLM-as-Judge (3 persona)
│   ├── scenarios/*.yaml                   ← 5개 표준 시나리오
│   ├── judges/rubric.yaml                 ← 평가 루브릭 (고정)
│   ├── paper/generate_tables.py           ← 논문 테이블 자동 생성
│   └── experiments/{EXP-*}/runs/          ← 실험 데이터 자동 저장
│
├── src/                                   ← ⬜ 구현 대상
│   ├── blackboard/
│   ├── orchestrator/
│   ├── agents/
│   ├── llm/
│   ├── sandbox/
│   └── recorder/
│
└── tests/                                 ← ⬜ 구현 대상
```

---

## 1. v2 설계서 보강 7개 항목

> 이 항목들은 **Phase 0 (프로젝트 셋업) 시점에 v2 설계서에 직접 반영**한다.
> 구현 전에 설계서가 최신이어야 한다.

### 1-1. No Rubber-Stamping Rule
- **반영 위치**: v2 8장 Phase 4, 각 에이전트 정의에 추가
- **내용**: Phase 4 에이전트(Simplicity Advocate, Risk Analyst)는 "이건 괜찮다"만 출력 불가. 반드시:
  - 대안 최소 1개 제시 (없으면 이유 명시)
  - 리스크/단순화 포인트 최소 1개 식별
  - "no_contribution"은 허용 (무의미한 반박보다 나음)
- **근거**: Liang(2023) DoT, Wynn(ICML 2025) 동의 편향
- **검증**: Phase 4 출력에서 "alternative_proposed" 필드 존재 확인 (Pydantic validator)

### 1-2. 구조화된 Review 루브릭
- **반영 위치**: v2 3.2 Review Authority + 새 섹션 3.2.1 추가
- **내용**: 각 슬롯별 review 체크리스트:
  ```yaml
  review_rubric:
    context:
      checklist:
        - "hard_constraints가 명시적인가?"
        - "priorities 가중치 합이 1.0인가?"
        - "feasibility_boundary가 현실적인가?"
      reviewer_must: "각 항목에 pass/fail + 1줄 이유"
    architecture:
      checklist:
        - "changeability_score가 있는가?"
        - "change_scenarios가 2개 이상인가?"
        - "anti_patterns가 명시되었는가?"
      reviewer_must: "각 항목에 pass/fail + 1줄 이유"
    # ... 13슬롯 각각
  ```
- **CoT reasoning 강제**: reviewer가 "이유 없이 reviewed로 올리기" 불가
- **순서 무작위화**: Blackboard 항목을 reviewer에게 보여줄 때 순서를 랜덤으로
- **근거**: MAJ-Eval(2025) Spearman 0.47, LLM-as-Judge Survey 편향 완화

### 1-3. 수렴 메커니즘 강화 (글로벌 상한 → Phase별 상한 + 동적 종료)
- **반영 위치**: v2 4.1 Router + 새 섹션 3.7 "수렴 규칙" 추가
- **내용**:
  ```yaml
  convergence_rules:
    per_phase_max_rounds: 10
    dynamic_termination:
      condition: "3연속 Phase에서 accepted 항목 변화 < 5%"
      action: "State Assessor가 '충분' 판정, 다음 Phase로"
    global_safety_net:
      max_total_agent_calls: 200
      on_exceed: "Interaction Gate가 사용자에게 알림 + 현재 상태로 강제 결정"
  ```
- **v1의 "50라운드"를 대체**: Phase당 10 × 6 Phase = 60이 자연스러운 상한. 
  하지만 대부분 Phase당 3~5라운드면 충분 (수렴 연구: 7라운드에서 0.892).
  200 agent calls는 안전망.
- **근거**: Deep-4 수렴 연구, Review M3

### 1-4. Think in NL, Write in Schema
- **반영 위치**: v2 13장 공통 프로토콜 → 13.6절 추가
- **내용**:
  ```
  13.6 출력 형식 원칙: Think in NL, Write in Schema
  
  에이전트 출력은 두 부분으로 나뉜다:
  1. reasoning (자연어): 에이전트의 사고 과정. 자유 형식.
     → Blackboard에 저장하지 않음. Recorder가 QOC 변환 시 참고.
  2. contribution (구조화): Pydantic 스키마에 맞는 슬롯 기여.
     → Blackboard에 저장.
  
  이유: JSON 강제 시 추론 10~15% 하락 (Tam et al., arXiv:2408.02442).
  하지만 에이전트 간 통신은 구조화되어야 모호성 감소 (La Malfa, NeurIPS 2025).
  → 추론은 자연어, 결과물만 구조화. 양쪽의 장점을 취한다.
  ```
- **구현**: `base_agent.py`에서 LLM 응답을 `{reasoning: str, contribution: SlotModel}` 으로 파싱

### 1-5. Prototype Validator 검증 가능성 분류
- **반영 위치**: v2 9장 Phase 4.5
- **내용**:
  ```yaml
  success_criteria_classification:
    code_verifiable:
      examples: ["API 응답 2초 이내", "데이터 모델 정합성", "알고리즘 O(n log n)"]
      action: Prototype Validator가 코드 생성 + 실행
    simulation_possible:
      examples: ["동시 접속 100명 처리", "DB 쿼리 50ms 이내"]
      action: 목 서버/인메모리 DB로 시뮬레이션 (한계 명시)
    manual_only:
      examples: ["1만 TPS", "99.9% 가용성", "보안 감사 통과"]
      action: Interaction Gate가 사용자에게 전달 + "수동 확인 필요" 태그
  ```
- **Prototype Validator가 success_criteria를 먼저 분류** → 검증 가능한 것만 실행
- **근거**: Deep-1 연구

### 1-6. Precedent Researcher = web_search + LLM (v1에서 RAG defer)
- **반영 위치**: v2 5장 Agent 3 수정
- **v1 구현**: RAG pipeline 없이 `web_search` 도구를 직접 호출
  ```
  Precedent Researcher 동작 (v1):
  1. 문제 키워드 추출
  2. web_search 도구로 GitHub, 기술 블로그, 논문 검색
  3. 결과에서 유사 프로젝트 식별 + 장단점 분석 (LLM)
  4. evidence_level 자동 연동:
     - 3+ 독립 소스 → empirical
     - 1~2 소스 → anecdotal
     - 0 소스 → no_contribution (hallucination 방지)
  ```
- **v2 (향후)**: GraphRAG + Semantic Scholar API + 도메인 특화 knowledge base
- **근거**: Review M5 — RAG pipeline은 별도 프로젝트 수준

### 1-7. 읽기 뷰에 Phase 전환 reasoning 요약 추가
- **반영 위치**: v2 12장 읽기/쓰기 뷰
- **내용**: Phase 전환 시 State Assessor가 이전 Phase의 핵심 reasoning을 요약 (200 토큰 이내)
  ```yaml
  phase_transition_summary:
    trigger: State Assessor가 "phase_sufficient: true" 판정 시
    content: |
      이전 Phase에서 도달한 결론 요약:
      - 핵심 결정 3개 이내
      - 미해결 질문 (있으면)
      - 다음 Phase에 전달할 context
    max_tokens: 200
    저장: Blackboard 각 슬롯의 metadata에 phase_summary 필드 추가
    대상: 다음 Phase 에이전트의 읽기 뷰에 자동 포함
  ```
- **전체 reasoning trace는 전달하지 않음** — 요약만. 토큰 비용 통제.
- **근거**: Wang(2024) Collaborativeness + Deep-5 Lost in the Middle 방어

---

## 2. 아키텍처 핵심 결정 (리서치 기반)

### 2-1. Blackboard = 데이터 계층, Phase = 제어 계층 (M4 해결)

v2의 "Blackboard Pattern"이라는 이름이 혼란을 줬다.
실제로 v2는 두 가지를 동시에 사용한다:

```
┌─────────────────────────────────────────┐
│          제어 계층 (Control Flow)          │
│   LangGraph DAG: Phase 1→2→3→4→5       │
│   + 루프백 (Phase 4→3, validation fail) │
│   + Router 규칙 15개                     │
│   + State Assessor Phase 충분성 게이트   │
└──────────────────┬──────────────────────┘
                   │ 읽기/쓰기
┌──────────────────▼──────────────────────┐
│         데이터 계층 (Shared State)         │
│   Pydantic 모델: 13슬롯 + 메타데이터     │
│   + 에이전트별 읽기/쓰기 뷰              │
│   + 상태 전이 4원칙 (validator)          │
│   + GC 규칙                              │
└─────────────────────────────────────────┘
```

**"Blackboard"는 데이터 계층의 이름이다. 제어 흐름은 DAG 상태 머신이다.**
이 분리를 v2 설계서 1장에 명시한다.

**Blackboard의 "자유 기여" 해석**: Phase 내에서 에이전트가 Blackboard에 자유롭게 쓸 수 있다는 의미.
Phase 간 전환은 게이트로 통제. 이건 모순이 아니라 의도적 설계.

### 2-2. 에이전트 17개 유지 — 단, Lazy Loading이 핵심

**유지 근거**:
- Qian(ICLR 2025): 에이전트 수 로지스틱 성장
- v2의 각 에이전트 "왜 별도인가" 근거가 타당 (관심사 분리, 편향 방지)

**DeepMind(2025) "실효 3~4개" 반박 회피**:
- v2의 Lazy Loading: 동시 활성 2~4개
- 17개가 **동시에** 돌지 않음. Phase별로 2~4개만 활성
- 조정 비용 1.724승은 **동시 활성 에이전트 수**에 적용 → 2~4개면 안전 범위

**EXP-ABLATION으로 검증**: 17개 중 실제로 가치 없는 에이전트가 있으면 데이터로 제거

### 2-3. 모델 배정: 초기 All-Sonnet → 실험 후 결정 (M2 해결)

**문제**: Hegazy(2024) "다양성 +9%p" vs Li(2025) "Self-MoA +6.6%"
**해결**: 단정하지 않고 실험으로 해결.

```
초기 구현: All-Sonnet (가장 저렴, 빠른 이터레이션)
EXP-MODEL 실행 후: All-Opus / Mixed / All-Sonnet 비교
데이터 기반으로 최종 결정
```

이유: 처음부터 Mixed-Model로 가면 디버깅 복잡도 증가.
All-Sonnet으로 시스템을 안정화시킨 후 모델 교체는 `model_assignment.py` 한 파일만 수정.

### 2-4. 에이전트 프롬프트 ≠ 페르소나 (E4 반영)

Basil(2025): "너는 전문가야" → 추론 개선 안 됨, 최대 30% 하락.

**v2 에이전트 프롬프트 원칙**:
```
❌ "You are a Graph Theory expert."
✅ "Your task is to analyze entity relationships using graph-based methods.
    You MUST output: entity_graph, relation_types, structural_constraints, potential_issues.
    You can ONLY write to the 'relationships' slot.
    You can ONLY read: problem, architecture slots."
```

차이: 페르소나(정체성)가 아니라 **구조적 제약**(뭘 읽고, 뭘 쓰고, 뭘 출력하는가)으로 역할 분리.
이게 v2의 "왜 별도 에이전트인가"의 실제 구현.

---

## 3. 평가 체계

### 3-1. 가설 (PRE-REGISTRATION.md에서 가져옴)

| ID | 가설 | 검정 | 기준 |
|----|------|------|------|
| **H1** | 17-agent > 1-agent (Coverage + Quality) | Paired t-test | p < 0.05, d > 0.5 |
| **H2** | Quality = logistic(agent_count) | Logistic regression | R² 보고 |
| **H3** | With Phase 4 > Without Phase 4 (Feasibility) | Paired t-test | p < 0.05 |
| **H4** | Mixed model > Homogeneous (Unique Perspectives) | ANOVA + Tukey HSD | p < 0.05 |

### 3-2. 평가 방법: LLM-as-Judge (전문가 대체) — C3 해결

| 항목 | 내용 |
|------|------|
| **Judge 3명** | Senior Architect (Opus), DevOps/SRE (GPT-4o), Junior Dev (Sonnet) |
| **채점** | `eval/judges/rubric.yaml` 고정 루브릭 (4 criteria × 1-5점 × 3 judge) |
| **일치도** | Cohen's Kappa (judge 간) |
| **인간 보정** | 252회 중 20회(8%)를 인간 1명이 평가 → Spearman ρ 계산 |
| **신뢰 기준** | ρ > 0.6이면 LLM judge 유효 |
| **코드** | `eval/maj_eval.py` (이미 구현) |

### 3-3. 5개 시나리오 (이미 코드화)

| ID | 이름 | 복잡도 | 핵심 테스트 |
|----|------|--------|-----------|
| 1 | Todo App | simple | 시스템이 과설계하지 않는가 |
| 2 | 실시간 채팅 | medium | 표준적인 아키텍처 설계 품질 |
| 3 | 멀티에이전트 시스템 | complex | 재귀적 자기 설계 (blind spot 발견) |
| 4 | "SNS 같은 거" | ambiguous | 모호한 요구사항에서 관점 다양성 |
| 5 | $0 예산, 1주 | extreme | 제약 경계에서의 feasibility 판단 |

### 3-4. 도메인 불일치 인정 (M1, Threats to Validity)

> **인정**: 인용 논문 대부분(Du, Hegazy, Qian 등)은 math/reasoning/code 벤치마크에서 측정됨.
> 소프트웨어 아키텍처 설계는 정답이 없는 주관적 판단이라는 점에서 근본적으로 다름.
> 이 Gap은 본 실험(EXP-SCALE~MODEL)이 메우는 역할을 하며,
> 논문에서 "threats to validity"로 명시적으로 기술한다.

---

## 4. 기술 스택

| 항목 | 선택 | 근거 |
|------|------|------|
| **언어** | Python 3.11+ | LLM 에코시스템, Pydantic, LangGraph |
| **프레임워크** | LangGraph | DAG 상태머신 + 공유 상태 + interrupt + checkpointing |
| **스키마** | Pydantic v2 | 13슬롯 + 메타데이터 + 상태 전이 validator |
| **LLM 통합** | LiteLLM | 멀티 모델 통합 API. 모델 교체 시 코드 변경 0 |
| **초기 모델** | All Claude Sonnet 4.6 | 저렴 + 빠름. EXP-MODEL 후 변경 가능 |
| **샌드박스** | E2B (fallback: Docker) | Prototype Validator 코드 실행 |
| **검색** | web_search 도구 (v1) | Precedent Researcher. RAG는 v2로 defer |
| **저장** | LangGraph state (in-memory) + 마크다운 (QOC/ADR) | |
| **테스트** | pytest | 상태 전이, Router, GC |
| **실험** | `eval/` 프레임워크 (이미 구현) | ExperimentRunner + auto_measure + MAJ-Eval |

### 하드코드 범위 (LLM 호출이 아닌 코드로 구현하는 것)

| 컴포넌트 | 구현 방식 | LLM 필요? |
|---------|----------|----------|
| Router 15개 규칙 | LangGraph 조건부 엣지 (if/else) | ❌ |
| 상태 전이 4원칙 | Pydantic validator | ❌ |
| Review Authority 매트릭스 | dict 룩업 | ❌ |
| GC 4규칙 | cleanup 함수 | ❌ |
| 읽기/쓰기 뷰 | 에이전트별 슬롯 매핑 dict | ❌ |
| Interaction Gate 트리거 4/6개 | 수치 비교 (confidence < 0.8 등) | ❌ |
| Deadlock Resolver 트리거 | 카운터 (version >= 3) | ❌ |
| Recorder 로깅 | 이벤트 리스너 + 파일 쓰기 | ❌ |
| Recorder QOC 변환 | LLM (Haiku) | ✅ 경량 |
| Recorder ADR 생성 | LLM (Sonnet) | ✅ 중간 |
| Interaction Gate 판단 2/6개 | "cost_of_error" 판단 등 | ✅ 경량 |
| State Assessor | Phase 충분성 정성 판단 | ✅ 경량 |
| 13개 Phase 에이전트 | 핵심 추론 | ✅ 필수 |

### 에러 핸들링 전략 (A2)

```yaml
error_handling:
  llm_call_failure:
    retry: 3회 (exponential backoff: 1s, 2s, 4s)
    fallback_model:
      opus → sonnet
      gpt-4o → opus
      sonnet → haiku
      haiku → (skip + no_contribution)
    timeout_per_agent: 30초
    
  sandbox_failure:
    retry: 2회
    fallback: Docker (E2B 실패 시)
    ultimate_fallback: 코드 생성만 하고 실행 skip + "실행 실패" 태그
    
  rate_limit:
    strategy: LiteLLM 내장 rate limit handler
    queue: 동시 최대 3 LLM 호출
```

---

## 5. 구현 로드맵 (MVP-First)

> **핵심 변경**: "전부 만들고 평가"가 아니라 "조금 만들고 검증, 추가하고 검증".
> 구현의 각 단계가 EXP-SCALE의 데이터 포인트를 생산한다.

### 예산 (A1)

| 항목 | 예상 비용 |
|------|----------|
| 개발 중 테스트 (All-Sonnet) | ~$100~$200 |
| EXP-SCALE (75회) | ~$150~$300 |
| EXP-ABLATION (102회) | ~$200~$400 |
| EXP-CHALLENGE (30회) | ~$60~$120 |
| EXP-MODEL (45회, Opus 포함) | ~$200~$400 |
| 인간 보정 (20회 재실행) | ~$40 |
| **총 예산 상한** | **$1,500** |

---

### Phase 0: 프로젝트 셋업 + v2 보강 반영 (2~3일)

#### 0-1. 프로젝트 초기화
```bash
# 작업 목록
1. pyproject.toml 생성
   - dependencies: langgraph, pydantic>=2.0, litellm, pyyaml, pytest
   - optional: e2b, matplotlib (논문 그래프용)
2. src/ 디렉토리 구조 생성 (빈 __init__.py들)
3. .env.example 생성 (ANTHROPIC_API_KEY, OPENAI_API_KEY)
4. .gitignore 업데이트 (.env, eval/experiments/*/runs/)
```

#### 0-2. v2 설계서 보강 반영
```bash
# v2/meta-architect-v2.md에 7+4개 항목 직접 추가

# 보강 7개:
1. 8장에 No Rubber-Stamping Rule [DECISION][src:paper-A2,E6]
2. 3.2.1에 Review 루브릭 [DECISION][src:paper-G2,G1]
3. 3.7에 수렴 규칙 (Phase당 10라운드 + 동적 종료 + 200 calls 안전망) [DECISION][src:deep-4]
4. 13.6에 Think in NL, Write in Schema [DECISION][src:paper-I1]
5. 9장에 검증 가능성 분류 [DECISION][src:deep-1]
6. 5장에 web_search 기반 (RAG defer) [DECISION][src:deep-6,review-M5]
7. 12장에 Phase 전환 reasoning 요약 [DECISION][src:paper-A4]
+ 1장에 Blackboard = 데이터 계층, Phase = 제어 계층 명시 [DECISION][src:review-M4]

# QOC 미해결 4개 확정 (G1):
8. Observability (11장 Recorder) — 유지 [DECISION] 이유: Phase 0.5부터 기본 로깅 필요
9. Evaluation (11장 Recorder) — 유지 [DECISION] 이유: 실험 프레임워크와 연동
10. Security & Governance (13.4) — 유지 [DECISION] 이유: 제거 비용 > 유지 비용
11. 13.5 Evidence Source — 유지 [DECISION] 이유: web_search 도구 연동의 근거

# 로드맵 동기화 (G4):
12. 16장 구현 로드맵을 Master Plan Phase 0→0.5→1→2→3→4로 업데이트
```

#### 0-3. QOC "🟡 나중에" 4개 재검토 시점 확정 (G2)
```yaml
deferred_items:
  reviewability_matrix:
    source: "GPT 피드백 [src:qoc-Q5]"
    review_at: "Phase 4 (반복 개선) — QOC 50건 이상 시"
  accepted_auto_promotion:
    source: "GPT 피드백 [src:v2-§3.3]"
    review_at: "Phase 4 — QOC 50건 이상 시"
  shared_vocabulary:
    source: "GPT 피드백 [src:qoc-Q5]"
    review_at: "Phase 2 — Knowledge Curator 구현 시 재평가"
  expires_after_rounds:
    source: "GPT 피드백 [src:qoc-Q5]"
    review_at: "Phase 1 — GC 규칙 구현 시 필요 여부 판단"
```

#### 0-4. 검증
- [ ] `python eval/experiment_config.py` → 252 runs 확인
- [ ] `pytest` 실행 가능 확인 (빈 테스트라도)
- [ ] v2 설계서 라인 수 확인 (보강 후 ~2000줄 예상)

**MUST-READ 논문**: 없음 (셋업 단계)

---

### Phase 0.5: 3-Agent MVP + 첫 번째 데이터 (1~2주) ← 신규

> **이 Phase가 가장 중요.** 3개 에이전트로 핵심 가설을 빠르게 검증.

#### 0.5-1. MUST-READ 논문 (이 Phase 시작 전 반드시 읽기)
```
C1: Han & Zhang (arXiv:2507.01701) — §3 아키텍처, §4 에이전트 역할
E1: La Malfa (arXiv:2505.21298) — §3 네 가지 비판
I1: Tam (arXiv:2408.02442) — §3 실험, §4 완화 (Think NL, Write Schema)
```
→ 각각 `research/verified/{C1,E1,I1}.md`에 핵심 내용 기록

#### 0.5-2. 승격 정책 확정 (G5)
```yaml
# Phase 0.5 MVP에서의 승격 정책:
promotion_policy:
  phase_0_5: "수동 승격 (v2 §3.3의 v1 정책)"
  # Interaction Gate가 사용자에게 "이 항목을 accepted 해도 되나요?" 확인
  # Phase 0.5에서는 3 에이전트뿐이므로 자동 승격 불필요
  # [DECISION][src:v2-§3.3]
  
  full_system: "reviewed + conflict 0 + 최신 version + evidence ≥ empirical 시 자동"
  # QOC 50건 이상 누적 후 전환 [src:v2-§3.3]
```

#### 0.5-3. Blackboard 핵심만 구현
```python
# src/blackboard/schema.py — 13슬롯 중 핵심 4개만 먼저
# context, problem, architecture, decision
# 나머지 9개는 빈 슬롯으로 예약

# src/blackboard/entry.py — 19필드 메타데이터
# 전체 구현 (스키마는 처음부터 완전해야 함)

# src/blackboard/state.py — 상태 전이 4원칙
# 전체 구현 (핵심 제약이므로)

# src/blackboard/views.py — 3개 에이전트의 읽기/쓰기 뷰만
```

#### 0.5-3. 3-Agent 구현
```python
# 3개 에이전트:
# 1. Architect Agent (= Structure Advisor 확장)
#    - Phase 1~3을 하나의 구조화된 체크리스트로 수행
#    - 읽기: (없음 — 첫 주자) + 사용자 입력
#    - 쓰기: context, problem, architecture
#
# 2. Critic Agent (= Simplicity Advocate + Risk Analyst 통합)
#    - Phase 4 adversarial challenge
#    - 읽기: context, architecture
#    - 쓰기: challenges
#    - No Rubber-Stamping 규칙 적용
#
# 3. Synthesizer Agent (= Decision Evaluator)
#    - Phase 5 최종 결정
#    - 읽기: 전체
#    - 쓰기: decision

# src/agents/base_agent.py — Think NL, Write Schema 공통 로직
# src/agents/architect_agent.py
# src/agents/critic_agent.py
# src/agents/synthesizer_agent.py
# src/agents/prompts/architect.md (300~500줄로 시작)
# src/agents/prompts/critic.md
# src/agents/prompts/synthesizer.md
```

#### 0.5-4. 최소 Orchestrator
```python
# src/orchestrator/graph.py — LangGraph 그래프
# 단순 선형: Architect → Critic → Synthesizer
# 루프: Critic이 severity:critical이면 Architect로 복귀 (최대 3회)

# src/llm/provider.py — LiteLLM 통합 (All-Sonnet)
# src/llm/model_assignment.py — 3개 에이전트 모두 Sonnet
```

#### 0.5-5. ExperimentRunner 연결
```python
# eval/experiment_runner.py의 _execute_system()을
# 실제 LangGraph 그래프 실행으로 연결

# 연결 인터페이스:
# ExperimentRunner → graph.run(scenario, agent_config) → blackboard_output
```

#### 0.5-6. 첫 번째 실험 데이터 수집
```bash
# EXP-SCALE의 "3-agent" 조건 실행
python -c "
from eval.experiment_runner import ExperimentRunner
from eval.experiment_config import ExperimentConfig, ExperimentName, ScenarioID, AGENT_SETS

runner = ExperimentRunner(use_mock_judge=False)  # 실제 judge 사용
for scenario in ScenarioID:
    for rep in range(1, 4):
        config = ExperimentConfig(
            experiment=ExperimentName.SCALE,
            condition_name='3-agent',
            scenario=scenario,
            repetition=rep,
            agents=AGENT_SETS['3-agent'],
        )
        runner.run(config)
"
# → eval/experiments/EXP-SCALE/runs/ 에 15개 데이터 포인트

# 1-agent baseline도 실행 (단일 Opus mega-prompt)
# → 15개 추가 데이터 포인트
```

#### 0.5-7. 중간 검증 — 여기서 방향 결정
```
if 3-agent가 1-agent보다 Coverage 10%+ 높으면:
    → Phase 1로 진행 (에이전트 확장에 가치 있음)
    
if 3-agent ≈ 1-agent:
    → 프롬프트 튜닝 먼저 (에이전트 추가보다 프롬프트 품질이 핵심)
    → 또는 Critic Agent 강화 (adversarial이 핵심인지 테스트)
    
if 3-agent < 1-agent:
    → 심각한 문제. 에이전트 간 정보 손실 조사.
    → Blackboard 스키마/전달 방식 재검토.
```

#### 0.5-8. 관측성 기본 구현 (m4: Phase 1으로 당김)
```python
# src/recorder/logger.py — 기본 이벤트 로깅
# 최소한:
# - 에이전트별 호출 시간/토큰
# - Blackboard 상태 변화 (before/after diff)
# - Phase 전환 시점 + 이유
# → 파일 기반 로그 (logs/{session_id}.jsonl)
```

**Phase 0.5 완료 조건**: 
- 3-agent + 1-agent 각 15회 = 30회 실험 데이터
- Table 1의 2개 행 채워짐
- 중간 검증 결과에 따른 방향 결정

---

### Phase 1: Blackboard 완성 + Orchestrator 확장 (1~2주)

#### MUST-READ 논문
```
B1: Qian (arXiv:2406.07155) — §3 MacNet, §4 Scaling Law
E2: DeepMind (arXiv:2512.08296) — §4 Scaling Law, §5 실효 팀 크기
```

#### 1-1. Blackboard 나머지 9슬롯 활성화
```python
# precedents, design_space, cross_domain, inventions,
# relationships, data_strategy, challenges, validation, diagrams
# Phase 0.5에서 스키마는 이미 정의됨 → 슬롯 활성화만
```

#### 1-2. Orchestrator 4모듈 완성
```python
# src/orchestrator/router.py — 15개 규칙 전체 (Phase 0.5에서는 3개만 있었음)
# src/orchestrator/state_assessor.py — Haiku 호출
# src/orchestrator/deadlock_resolver.py — 트리거 3개 + Decision Evaluator 위임
# src/orchestrator/interaction_gate.py — 트리거 6개 + LangGraph interrupt
# src/blackboard/gc.py — GC 4규칙
# src/blackboard/review_authority.py — 12슬롯 자격 매트릭스 + 루브릭
```

#### 1-3. 6-Agent 확장
```python
# Phase 0.5의 3개 에이전트를 분리:
# Architect → Problem Decomposer + Design Space Explorer + Structure Advisor
# Critic → Simplicity Advocate (유지)
# Synthesizer → Prototype Validator + Decision Evaluator
#
# 프롬프트: 각 200~500줄로 시작
```

#### 1-4. 테스트
```bash
pytest tests/test_state_transition.py  # 상태 전이 4원칙
pytest tests/test_router.py            # Router 15규칙
pytest tests/test_gc.py                # GC 4규칙
```

#### 1-5. EXP-SCALE "6-agent" 데이터 수집
```bash
# 15회 실행 → Table 1의 3번째 행
# 3-agent → 6-agent marginal value 측정
```

---

### Phase 2: 17-Agent 완성 (2~4주)

#### MUST-READ 논문
```
A1: Du (arXiv:2305.14325) — §3 debate protocol
A2: Liang (arXiv:2305.19118) — §3.1 DoT, §3.2 MAD, Algorithm 1
E4: Basil (SSRN:5879722) — 페르소나 vs 구조적 역할 분리
E6: Wynn (arXiv:2509.05396) — §4 debate failure modes
```

#### 2-1. 나머지 11개 에이전트 구현
```
Phase 1 추가:
  - Context Profiler
  - Precedent Researcher (web_search 기반)

Phase 2 추가:
  - Cross-Domain Connector (유추 프레임 명시적 주입)
  - Invention Engine (TRIZ — AutoTRIZ 참고)

Phase 3 추가:
  - Relationship Architect
  - Data Strategist

Phase 4 추가:
  - Risk, Cost & Scale Analyst

상시:
  - Recorder (logger=코드, QOC=Haiku, ADR=Sonnet)
  - Modeler (Mermaid 다이어그램)
  - Knowledge Curator (web_search + 경량 요약)
  - Meta Verifier (구조 체크=코드, 의미 체크=Sonnet)
```

#### 2-2. 프롬프트 작성 원칙
```
각 에이전트 프롬프트 구조:
1. 역할 정의 (구조적 제약으로, 페르소나가 아닌)
2. 읽기/쓰기 뷰 명시
3. 출력 스키마 (Pydantic 모델 포함)
4. 판단 기준 (언제 이 관점을 쓰고 안 쓰는가)
5. 실패 조건 (언제 no_contribution을 내는가)
6. 예시 (좋은 출력 2개, 나쁜 출력 1개)

분량: 핵심 에이전트 500~1000줄, 유틸리티 200~500줄
시작은 짧게 → EXP-ABLATION 결과로 중요 에이전트 프롬프트 강화
```

#### 2-3. EXP-SCALE "10-agent" + "17-agent" 데이터 수집
```bash
# 각 15회 실행 → Table 1의 4~5번째 행
# Scaling curve 데이터 완성
```

#### 2-4. 중간 점검: Scaling Curve 분석
```python
# eval/paper/generate_tables.py 실행
# Figure 1: 1→3→6→10→17 스케일링 곡선
# 로지스틱 피팅 시도 → H2 초기 검증
```

---

### Phase 3: 나머지 실험 + 논문 (2~3주)

#### MUST-READ 논문
```
A3: Hegazy (arXiv:2410.12853) — §4 다양성 프리미엄
E3: Li (arXiv:2502.00674) — Self-MoA 반론
G2: MAJ-Eval (arXiv:2507.21028) — §3 프레임워크
F1: Sharma (arXiv:2310.13548) — sycophancy
```

#### 3-1. EXP-ABLATION (102회)
```bash
# 17-agent에서 하나씩 제거 → 각 에이전트의 개별 기여도
# Table 2 완성
# "어떤 에이전트가 가장 중요한가?"에 대한 답
```

#### 3-2. EXP-CHALLENGE (30회)
```bash
# Phase 4 있음 vs 없음
# H3 검증
# Figure 3 완성
```

#### 3-3. EXP-MODEL (45회)
```bash
# All-Opus vs Mixed vs All-Sonnet
# H4 검증 + Hegazy vs Li 모순 해결
# Table 3 완성
```

#### 3-4. 인간 보정 (20회)
```bash
# 252회 중 무작위 20회 선택
# 인간 1명이 rubric.yaml 기준으로 평가
# LLM judge와 Spearman ρ 계산
```

#### 3-5. 통계 분석 + 논문 테이블/그래프 생성
```bash
python eval/paper/generate_tables.py
# Table 1: Scale, Table 2: Ablation, Table 3: Model
# Figure 1: Scaling Curve, Figure 2: Pareto, Figure 3: Challenge
```

#### 3-6. 논문 초고 작성
```
타겟: ICSE Technical Track 또는 ESEM Registered Reports
구조: PRE-REGISTRATION.md의 가설 → 실험 → 결과 → 논의
Threats to Validity: 도메인 불일치 (M1) 명시적 기술
```

---

### Phase 4: 반복 개선 (ongoing)

- 프롬프트 튜닝 (EXP-ABLATION에서 약한 에이전트 강화)
- 모델 배정 최적화 (EXP-MODEL 결과 반영)
- RAG pipeline 추가 (Precedent Researcher 강화) → v2
- 비용 최적화 (Haiku 활용 확대)
- v3 설계서 업데이트

---

## 6. MUST-READ 논문 읽기 일정 (A5)

| Phase | 읽을 논문 | 이유 |
|-------|----------|------|
| **Phase 0.5 시작 전** | C1, E1, I1 | Blackboard 구현, 비판 방어, 출력 형식 |
| **Phase 1 시작 전** | B1, E2 | 스케일링 법칙, 조정 비용 |
| **Phase 2 시작 전** | A1, A2, E4, E6 | 토론 프로토콜, DoT, 페르소나 비판, 실패 모드 |
| **Phase 3 시작 전** | A3, E3, G2, F1 | 다양성, Self-MoA, judge, sycophancy |
| **필요 시** | H1 | Lost in the Middle (context 최적화 시) |

각 논문을 읽은 후:
1. `research/verified/{paper_id}.md`에 핵심 수치/알고리즘 기록
2. `check_paper_deps.py` hook이 통과되는지 확인
3. 코드 주석에 citation 포함

---

## 7. 리스크 + 완화

| 리스크 | 확률 | 영향 | 완화 | 감지 시점 |
|--------|------|------|------|----------|
| 3-agent ≈ 1-agent (MVP 실패) | 중 | 높음 | 프롬프트 튜닝 → Critic 강화 → Blackboard 재검토 | Phase 0.5-7 |
| 에러 전파 17.2배 증폭 | 중 | 높음 | 상태전이 4원칙 + peer review + 루브릭 | Phase 1 테스트 |
| Phase 4 echo chamber | 중 | 높음 | No rubber-stamping + 순서 무작위 + (향후)다른 모델 | Phase 2 EXP-CHALLENGE |
| 비용 $1500 초과 | 낮 | 중 | All-Sonnet 기본 + Haiku utility. 실험 중 비용 로깅 | 매 실행 |
| LLM judge가 인간과 불일치 (ρ < 0.6) | 중 | 높음 | 루브릭 개선 + 인간 샘플 확대 | Phase 3-4 |
| Prototype Validator 코드 실행 실패 | 중 | 중 | E2B → Docker fallback → skip + 태그 | Phase 2 |
| 수렴 실패 (200 calls 도달) | 낮 | 중 | Interaction Gate 알림 + 강제 결정 | Phase 1 |
| 논문 hallucination (잘못된 근거) | 중 | 높음 | check_paper_deps hook + verified/ 마킹 | 매 구현 |
| 타임라인 초과 | 높 | 중 | MVP-first로 각 Phase가 독립적 가치. 어디서 멈춰도 논문 가능 | 각 Phase 끝 |

---

## 8. 논문 가능 시점 (어디서 멈춰도 가치 있음)

| 시점 | 데이터 | 논문 가능? | 논문 유형 |
|------|--------|-----------|----------|
| Phase 0.5 완료 | 1-agent vs 3-agent (30회) | △ | Short paper / Workshop |
| Phase 1 완료 | + 6-agent (45회) | ○ | NIER (New Ideas) |
| Phase 2 완료 | + 10/17-agent (75회) + Ablation (102회) | ◎ | Full paper (ICSE/ASE) |
| Phase 3 완료 | + Challenge + Model (252회) | ◎◎ | Full paper + 모든 가설 검증 |

**핵심**: MVP-first 접근 덕분에 어떤 Phase에서 멈춰도 논문 데이터가 있다.
"전부 만들고 나서야 논문 가능"이 아니라 "만들면서 논문 데이터가 쌓인다".

---

## 9. 참고 문서

| 문서 | 위치 |
|------|------|
| v2 설계서 | `v2/meta-architect-v2.md` |
| QOC 기록 | `v2/meta-architect-v2-qoc.md` |
| 논문 카탈로그 | `research/papers-catalog.md` |
| 논문↔기능 매핑 | `research/paper-feature-map.json` |
| Deep Research | `research/deep-*.md` |
| 실험 설계 | `research/EXPERIMENT-DESIGN.md` |
| Pre-registration | `PRE-REGISTRATION.md` |
| 플랜 v1 | `research/MASTER-PLAN-v1.md` |
| 플랜 자체 평가 | `research/MASTER-PLAN-REVIEW.md` |
| 행동 가이드라인 | `CLAUDE.md` |

---

## 다음 행동

**Phase 0 시작:**
1. `pyproject.toml` 생성
2. v2 설계서에 7개 보강 항목 반영
3. C1, E1, I1 논문 읽기 → `research/verified/` 기록
4. Phase 0.5 (3-agent MVP) 구현 시작
