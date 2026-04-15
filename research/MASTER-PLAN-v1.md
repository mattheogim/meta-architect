# Meta Architect — Master Plan

> v2 설계서 + 45+ 논문 리서치 + Deep Research 8건을 종합한 최종 실행 계획
> 
> 원칙: "아이디어를 넣으면, 내가 모르는 것까지 포함해서 최적의 구조를 제안해주는 시스템"

---

## 0. 현재 상태

- ✅ v2 설계서 완성 (1,852줄, 17 에이전트 + 4모듈 Orchestrator + Blackboard)
- ✅ 논문 리서치 완료 (45+ 논문, 지지 + 반박 균형)
- ✅ Deep Research 8건 완료 (Prototype Validator, LLM-as-Judge, 1M Context 등)
- ✅ 60+ 개념 LLM 적용 가능성 검증
- ✅ 하드코드 가능 범위 분석
- ✅ 논문 기반 구현 강제 시스템 (CLAUDE.md + hook + paper-feature-map.json)
- ⬜ v2 보강/발전 반영
- ⬜ 구현 시작

---

## 1. v2 보강사항 (리서치 기반)

### 반드시 반영 (v2 설계에 추가해야 할 것)

| # | 보강 | 근거 | 반영 위치 |
|---|------|------|----------|
| 1 | **No Rubber-Stamping Rule** — Phase 4 에이전트는 "이건 괜찮다"만 출력 불가. 반드시 대안 1개 이상 제시 | Liang(2023) DoT 문제, Wynn(ICML 2025) 동의 편향 | v2 8장 Phase 4 |
| 2 | **구조화된 Review 루브릭** — peer review 시 슬롯별 체크리스트 + CoT reasoning 강제 | MAJ-Eval(2025) Spearman 0.47, LLM-as-Judge Survey(2024) 편향 완화 | v2 3.2 Review Authority |
| 3 | **글로벌 라운드 상한** — 전체 시스템 최대 50라운드 | 수렴 연구: 7라운드에서 0.892 수렴. v2에 글로벌 상한 없음 | v2 4.1 Router |
| 4 | **Think in NL, Write in Schema** — 에이전트 추론은 자연어, Blackboard 출력은 Pydantic | Tam(2024) JSON 강제 시 추론 10~15% 하락 | v2 13장 공통 프로토콜 |
| 5 | **Prototype Validator 검증 가능성 분류** — success_criteria를 "코드 검증 가능/수동 확인 필요"로 구분 | Deep-1 연구: 50줄로 정합성 가능, 부하 테스트 불가 | v2 9장 Phase 4.5 |
| 6 | **Precedent Researcher = RAG + LLM 하이브리드** — 검색은 코드(RAG), 판단은 LLM | Deep-6 연구: GraphRAG 성숙, evidence_level 자동 연동 | v2 5장 Agent 3 |
| 7 | **읽기 뷰에 Phase 전환 reasoning 요약 추가** — Phase 전환 시 이전 Phase의 "왜 이 결론인가" 요약 전달 | Wang(2024) Collaborativeness 현상 | v2 12장 읽기/쓰기 뷰 |

### 구현 시 적용 (설계서 수정 불필요, 구현에서 반영)

| # | 사항 | 근거 |
|---|------|------|
| 8 | **Multi-Model 배정** — Phase 4 도전 에이전트에 다른 LLM (GPT-4o) | Hegazy(2024) 다양성 프리미엄 +9%p |
| 9 | **LiteLLM 통합** — 멀티 모델 오케스트레이션 | Deep-8 연구: 즉시 구현 가능 |
| 10 | **E2B 또는 Docker sandbox** — Prototype Validator 실행 환경 | Deep-1 연구: E2B 성숙 |
| 11 | **MoE 라우팅 (simple만)** — complexity_grade:simple일 때 Phase 2 축소 | DeepMind(2025) 조정비용, Zhao(2025) hybrid routing |
| 12 | **Review 순서 무작위화** — position bias 방지 | LLM-as-Judge Survey 편향 완화 |
| 13 | **에이전트 프롬프트 ≠ 페르소나** — "너는 전문가야" 대신 구조적 역할 분리 | Basil(2025) 페르소나 추론 개선 안함 |

### 의식적으로 유지 (반박에도 불구하고 지키는 것)

| v2 설계 | 반박 | 유지 이유 |
|---------|------|----------|
| **17개 에이전트** | DeepMind: 실효 3~4개 | v2의 Lazy Loading이 동시 활성 2~4개로 이미 조정비용 회피. Qian(ICLR 2025) 로지스틱 성장 지지 |
| **Blackboard 패턴** | La Malfa: 자연어 모호성 | Han&Zhang(2025)이 LLM Blackboard 검증. Pydantic 스키마로 모호성 제거 |
| **Cross-Domain Connector** | "95% 노이즈" 주장 | Nature Comms(2026): 유추 가이드 시 10배 향상. v2의 핵심 가치("내가 모르는 것")의 직접 구현. 대신 프롬프트에 유추 프레임 명시적 주입 |
| **상태 전이 4원칙** | 에러 17.2배 증폭 | 원칙 자체가 에러 증폭 방어 메커니즘. peer review + conflict 해소 전제 + deadlock 강제 |

---

## 2. 평가 기준

### 핵심 가설
> "강제된 인지 다양성이 단일 에이전트보다 체계적으로 더 나은 아키텍처를 만든다"

### 5개 평가 축

| 축 | 지표 | 측정 방법 | 성공 기준 |
|----|------|----------|----------|
| **Blind Spot Coverage** | 60+ 개념 중 커버한 수 + Unique Perspective Count | 체크리스트 비교 (Single vs 3-Agent vs 17-Agent) | +30% 커버리지 |
| **Architecture Quality** | 실현가능성/확장성/유지보수성/보안 각 1-5점 | 전문가 blind review (3명) | 유의미한 차이 (p < 0.05) |
| **Decision Traceability** | QOC/ADR chain 완전성 | 최종 결정에서 근거 역추적 | 95%+ 추적 가능 |
| **Challenge Effectiveness** | actionable challenge rate | Phase 4 challenge 중 설계 변경 유발 비율 | 50%+ |
| **Cost-Quality Frontier** | quality_score / cost | 비용 대비 품질 비율 | Baseline 대비 비용증가율 < 품질향상율 |

### 비교 대상 4개

| Baseline | 설명 | 예상 비용 |
|----------|------|----------|
| A | Single Claude Opus (1M context mega-prompt) | ~$0.42 |
| B | 3-Agent (Architect + Critic + Synthesizer) | ~$0.24 |
| C | Meta Architect Mixed-Model (17 agent) | ~$1.50~$3.00 |
| D | Meta Architect All-Opus (17 agent) | ~$10+ |

### 5개 테스트 시나리오

1. **Simple** — Todo app (CRUD)
2. **Medium** — 실시간 채팅 앱 (WebSocket + DB + Auth)
3. **Complex** — 멀티 에이전트 시스템 (재귀: Meta Architect가 자기 자신을 설계)
4. **Ambiguous** — "SNS 같은 거" (요구사항 모호)
5. **Extreme** — "예산 $0, 혼자, 1주" (제약 극단)

---

## 3. 기술 스택

| 항목 | 선택 | 이유 |
|------|------|------|
| **언어** | Python 3.11+ | LLM 에코시스템, Pydantic, LangGraph |
| **프레임워크** | LangGraph | 그래프 기반 상태머신, interrupt, checkpointing |
| **스키마** | Pydantic v2 | 13슬롯 + 메타데이터 타입 안전 |
| **LLM 통합** | LiteLLM | 멀티 모델 통합 API |
| **샌드박스** | E2B (또는 Docker fallback) | Prototype Validator 코드 실행 |
| **RAG** | Semantic Scholar API + GitHub API | Precedent Researcher |
| **저장** | In-memory (LangGraph state) + 마크다운 파일 | Blackboard + QOC/ADR |
| **테스트** | pytest | 상태 전이, Router 규칙, GC 단위 테스트 |

### LLM 배정

| 역할 | 모델 | 이유 |
|------|------|------|
| Phase 1-3 에이전트 | Claude Opus | 깊은 추론 |
| Phase 4 도전 에이전트 | GPT-4o | 다른 모델 = 다른 편향 (Hegazy) |
| Phase 4.5 Validator | Claude Sonnet | 코드 생성 + 비용 |
| Phase 5 Decision | Claude Opus | 최종 결정은 최강 |
| State Assessor | Haiku | 경량, 매 턴 |
| Recorder 로깅 | 코드 (LLM 불필요) | 규칙 기반 |
| Recorder QOC 변환 | Haiku | 경량 해석 |
| Knowledge Curator | RAG + Haiku | 검색 + 경량 요약 |
| Meta Verifier | Claude Sonnet | 중간 수준 일관성 체크 |
| Modeler | Claude Sonnet | 다이어그램 생성 |

### 하드코드 범위

| 컴포넌트 | 방식 |
|---------|------|
| Router 15개 규칙 | Python if/else → LangGraph 조건부 엣지 |
| 상태 전이 4원칙 | Pydantic validator |
| Review Authority | 딕셔너리 룩업 |
| GC 4규칙 | cleanup 함수 |
| 읽기/쓰기 뷰 | 에이전트별 슬롯 매핑 딕셔너리 |
| Interaction Gate 트리거 4/6 | 수치 비교 (confidence < 0.8 등) |
| Deadlock Resolver 트리거 | 카운터 (version >= 3, rounds >= 3) |

---

## 4. 구현 로드맵

### Phase 0: 프로젝트 셋업 (1일)
```
meta-architect/
├── CLAUDE.md                    ← ✅ 완료
├── research/                    ← ✅ 완료 (45+ 논문, 8 deep research)
│   ├── 00-research-index.md
│   ├── papers-catalog.md
│   ├── paper-feature-map.json
│   ├── check_paper_deps.py
│   ├── verified/                ← 논문 읽기 완료 마킹
│   └── deep-*.md
├── v2/                          ← ✅ 완료 (설계서)
├── src/
│   ├── blackboard/
│   │   ├── schema.py            ← 13슬롯 Pydantic 모델
│   │   ├── state.py             ← 상태 전이 엔진
│   │   ├── views.py             ← 읽기/쓰기 뷰
│   │   ├── review_authority.py
│   │   ├── gc.py
│   │   └── entry.py             ← 메타데이터 모델
│   ├── orchestrator/
│   │   ├── router.py            ← 15개 규칙
│   │   ├── state_assessor.py    ← 경량 LLM
│   │   ├── deadlock_resolver.py
│   │   ├── interaction_gate.py
│   │   └── graph.py             ← LangGraph 조립
│   ├── agents/
│   │   ├── base_agent.py        ← 공통 프로토콜
│   │   ├── context_profiler.py
│   │   ├── problem_decomposer.py
│   │   ├── ... (17개)
│   │   └── prompts/             ← 에이전트별 시스템 프롬프트
│   ├── llm/
│   │   ├── provider.py          ← LiteLLM 통합
│   │   └── model_assignment.py  ← 에이전트별 모델 배정
│   ├── rag/
│   │   └── pipeline.py          ← Precedent Researcher RAG
│   ├── sandbox/
│   │   └── executor.py          ← E2B/Docker 실행
│   └── recorder/
│       ├── logger.py            ← 하드코드 로깅
│       └── qoc_converter.py     ← LLM 기반 QOC 변환
├── tests/
│   ├── test_state_transition.py
│   ├── test_router.py
│   ├── test_gc.py
│   └── test_e2e.py
├── eval/
│   ├── scenarios/               ← 5개 표준 시나리오
│   ├── baselines/               ← Single/3-Agent 실행 결과
│   └── compare.py               ← 평가 축 측정
└── pyproject.toml
```

작업:
- [ ] pyproject.toml + 의존성
- [ ] src/ 디렉토리 구조 생성
- [ ] .env.example (API 키 템플릿)

### Phase 1: Blackboard + Orchestrator 뼈대 (3~5일)

**MUST-READ 논문 먼저**: C1 (Blackboard 구현), E1 (비판 방어), E2 (스케일링)

1. `blackboard/schema.py` — 13슬롯 Pydantic 모델
2. `blackboard/entry.py` — 19필드 메타데이터
3. `blackboard/state.py` — 상태 전이 4원칙 validator
4. `blackboard/review_authority.py` — 12슬롯 자격 매트릭스
5. `blackboard/views.py` — 에이전트별 읽기/쓰기 뷰
6. `blackboard/gc.py` — GC 4규칙
7. `orchestrator/router.py` — 15개 규칙
8. `orchestrator/state_assessor.py` — Haiku 호출
9. `orchestrator/deadlock_resolver.py` — 트리거 + Decision Evaluator 위임
10. `orchestrator/interaction_gate.py` — 6개 트리거 + LangGraph interrupt
11. `orchestrator/graph.py` — 전체 그래프 조립

검증: `pytest tests/test_state_transition.py tests/test_router.py tests/test_gc.py`

### Phase 2: 에이전트 프롬프트 + LLM 통합 (5~7일)

**MUST-READ 논문 먼저**: A1, A2 (debate protocol), E4 (페르소나 비판), I1 (structured output)

1. `agents/base_agent.py` — Think NL + Write Schema 공통 로직
2. `llm/provider.py` — LiteLLM 통합
3. `llm/model_assignment.py` — 에이전트별 모델 배정
4. 17개 에이전트 × 시스템 프롬프트 (각 500~2000줄)
5. `rag/pipeline.py` — Precedent Researcher 검색
6. `sandbox/executor.py` — Prototype Validator 실행
7. `recorder/logger.py` + `recorder/qoc_converter.py`

검증: 각 에이전트를 단독 호출하여 출력 형식 확인

### Phase 3: 통합 + 단일 시나리오 (3~5일)

1. LangGraph 그래프 조립 (노드 + 엣지 + 조건)
2. 시나리오 2 (실시간 채팅 앱)로 end-to-end 테스트
3. 모든 Phase 통과 확인
4. Recorder QOC/ADR 출력 확인
5. Modeler Mermaid 다이어그램 확인
6. 비용/토큰 로깅 확인

### Phase 4: 평가 (3일)

1. 5개 시나리오 × 4개 Baseline 실행
2. 평가 축 5개 측정
3. 비교 리포트 작성
4. 가설 검증 결론

### Phase 5: 반복 개선 (ongoing)

- 프롬프트 튜닝 (평가 결과 기반)
- 에이전트 구성 조정
- 비용 최적화
- v2 → v3 설계서 업데이트

---

## 5. 리스크 + 완화

| 리스크 | 확률 | 영향 | 완화 |
|--------|------|------|------|
| 에러 전파 (17.2배 증폭) | 중 | 높음 | 상태 전이 4원칙 + peer review + 구조화 루브릭 |
| Phase 4 echo chamber | 중 | 높음 | No rubber-stamping + 다른 모델(GPT-4o) + 대안 강제 |
| 비용 폭발 | 중 | 중 | Lazy Loading + MoE routing(simple) + Haiku for utility |
| Prototype Validator 코드 실행 실패 | 중 | 중 | E2B sandbox + 검증 가능성 사전 분류 |
| Lost in the Middle | 낮 | 중 | 에이전트별 짧은 context (읽기 뷰) |
| 수렴 실패 | 낮 | 높음 | Deadlock Resolver + 글로벌 50라운드 상한 |
| 논문 hallucination (잘못된 근거로 구현) | 중 | 높음 | paper-feature-map + hook + verified/ 마킹 |

---

## 6. 참고 문서 링크

| 문서 | 위치 |
|------|------|
| v2 설계서 | `v2/meta-architect-v2.md` |
| QOC 의사결정 기록 | `v2/meta-architect-v2-qoc.md` |
| 리서치 인덱스 | `research/00-research-index.md` |
| 논문 카탈로그 (45+) | `research/papers-catalog.md` |
| 논문↔기능 매핑 | `research/paper-feature-map.json` |
| Deep Research 1-8 | `research/deep-*.md` |
| 구현 강제 스크립트 | `research/check_paper_deps.py` |
| 행동 가이드라인 | `CLAUDE.md` |

---

## 다음 행동

1. **Phase 0 프로젝트 셋업** 시작
2. MUST-READ 논문 중 **C1 (Han & Zhang Blackboard)** 부터 읽기 (Phase 1의 전제)
3. `research/verified/C1.md` 작성 후 `blackboard/schema.py` 구현 시작
