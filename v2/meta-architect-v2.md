# Meta Architect: System Design v2

> "아이디어를 넣으면, 내가 모르는 것까지 포함해서 최적의 구조를 제안해주는 시스템"

---

## 목차

1. [핵심 아키텍처: Blackboard Pattern](#1-핵심-아키텍처-blackboard-pattern)
2. [Blackboard 스키마](#2-blackboard-스키마)
3. [Blackboard 운영 규칙](#3-blackboard-운영-규칙)
4. [Orchestrator: 4-Module Controller](#4-orchestrator-4-module-controller)
5. [Phase 1: Understanding (이해) — 3 Agents](#5-phase-1-understanding-이해--3-agents)
6. [Phase 2: Exploration (탐색) — 3 Agents](#6-phase-2-exploration-탐색--3-agents)
7. [Phase 3: Design (설계) — 3 Agents](#7-phase-3-design-설계--3-agents)
8. [Phase 4: Challenge (도전) — 2 Agents](#8-phase-4-challenge-도전--2-agents)
9. [Phase 4.5: Validation (검증) — 1 Agent](#9-phase-45-validation-검증--1-agent)
10. [Phase 5: Decision (결정) — 1 Agent](#10-phase-5-decision-결정--1-agent)
11. [상시 작동 에이전트 — 4 Agents](#11-상시-작동-에이전트--4-agents)
12. [에이전트별 Blackboard 읽기/쓰기 뷰](#12-에이전트별-blackboard-읽기쓰기-뷰)
13. [에이전트 공통 프로토콜](#13-에이전트-공통-프로토콜)
14. [전체 작동 흐름](#14-전체-작동-흐름)
15. [60+ 개념 커버리지 맵](#15-60-개념-커버리지-맵)
16. [구현 로드맵](#16-구현-로드맵)
17. [v1 대비 변경 이력](#17-v1-대비-변경-이력)

---

## 1. 핵심 아키텍처: Blackboard Pattern

선형(순서대로) 구조가 아닌 **Blackboard(공유 칠판)** 구조를 사용한다.

```
┌──────────────────────────────────────────────────────────┐
│                BLACKBOARD (공유 작업 공간)                  │
│                                                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │ context   │ │ problem  │ │precedents│ │design_   │    │
│  │           │ │          │ │          │ │space     │    │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │cross_    │ │inventions│ │architec- │ │relation- │    │
│  │domain    │ │          │ │ture      │ │ships     │    │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │data_     │ │challenges│ │validation│ │decision  │    │
│  │strategy  │ │          │ │          │ │          │    │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘    │
│  ┌──────────┐                                            │
│  │ diagrams │                                            │
│  └──────────┘                                            │
└───────┬──────────┬──────────┬──────────┬─────────────────┘
        │          │          │          │
    Agent A    Agent B    Agent C    Agent D ...
    (읽고 쓴다)  (읽고 쓴다) (읽고 쓴다) (읽고 쓴다)
```

**왜 Blackboard인가:**
- 에이전트들이 순서 없이 자유롭게 기여할 수 있음
- 한 에이전트의 발견이 다른 에이전트의 사고를 촉발함
- 자연스럽게 반복적(iterative) — 합의에 도달할 때까지 계속
- 에이전트 추가/제거가 쉬움 (다른 에이전트를 건드릴 필요 없음)
- 모든 과정이 칠판에 남으므로 자동으로 기록됨
- 에이전트별 읽기 뷰(View)로 토큰 비용 40~60% 절감

---

## 2. Blackboard 스키마

### 2.1 슬롯 정의 (13개)

```yaml
blackboard:
  # ── Phase 1: Understanding ──
  context:
    description: "사용자 프로필, 제약, 자원, 우선순위"
    contains:
      - user_profile: { technical_level, tools, environment }
      - hard_constraints:
          - budget_max: "$500/month"      # 위반 시 즉시 탈락
          - deadline: "2_weeks"
          - team_size: 1
      - priorities:                        # 가중치 비교용
          simplicity: 0.3
          cost: 0.25
          scalability: 0.2
          changeability: 0.15
          build_speed: 0.1
      - feasibility_boundary: string

  problem:
    description: "분해 트리, 도메인 용어, 복잡도"
    contains:
      - decomposition_tree: nested
      - sub_problem_tags: [data, relationship, flow, learning]
      - complexity_grade: simple | complicated | complex | chaotic
      - ubiquitous_language: { term: definition }
      - bounded_contexts: [ { name, entities, complexity } ]

  precedents:
    description: "기존 솔루션, 재사용 가능/불가 목록"
    contains:
      - similar_projects: [ { name, approach, pros, cons, url } ]
      - verified_stacks: [ { stack, evidence } ]
      - reuse_list: [ string ]
      - build_new_list: [ string ]

  # ── Phase 2: Exploration ──
  design_space:
    description: "옵션 매트릭스, 유효 조합"
    contains:
      - dimension_options: { storage: [], communication: [], processing: [], ui: [] }
      - valid_combinations: [ { id, description, one_line_trait } ]
      - eliminated_combinations: [ { id, reason } ]

  cross_domain:
    description: "구조적 유사성, 타 분야 매핑"
    contains:
      - structural_mappings: [ { source_domain, target_application, similarity } ]
      - alternative_perspectives: [ string ]

  inventions:
    description: "모순, TRIZ 적용, 창의적 우회"
    contains:
      - contradictions: [ { improving, worsening, description } ]
      - triz_applications: [ { principle_number, name, concrete_application } ]
      - csp_solutions: [ object ]
      - creative_alternatives: [ string ]

  # ── Phase 3: Design ──
  architecture:
    description: "추천 구조, 컴포넌트 분해, 변경 용이성"
    contains:
      - recommended: [ { pattern, prerequisites, component_breakdown } ]
      - anti_patterns: [ { pattern, reason_not_to_use } ]
      - changeability_score: 0.0 ~ 1.0    # Evolution Planner 역할
      - change_scenarios:
          - scenario: "DB 교체"
            effort: high
            files_touched: 12
          - scenario: "에이전트 추가"
            effort: low
            files_touched: 2

  relationships:
    description: "엔티티 그래프, 제약, 병목"
    contains:
      - entity_graph: { nodes: [], edges: [] }
      - relation_types: [ { from, to, type, cardinality } ]
      - structural_constraints: [ string ]
      - potential_issues: [ { type: cycle | bottleneck | orphan, description } ]

  data_strategy:
    description: "스키마, DB 선택, 데이터 흐름"
    contains:
      - data_model: object
      - db_recommendation: { type, name, rationale }
      - data_flow: { sources: [], transformations: [], sinks: [] }
      - query_patterns: [ { pattern, index_strategy } ]

  # ── Phase 4: Challenge ──
  challenges:
    description: "단순화 요청, 리스크 경고, 비용 영향, 사용자 피드백"
    contains:
      - entries:
          - type: simplicity | risk | cost | scale | user_feedback
                  | deadlock_resolution    # Deadlock Resolver가 기록
                  | consistency_warning    # Recorder가 과거 결정 충돌 시 기록
                  | inconsistency          # Meta Verifier가 모순 감지 시 기록
            severity: low | medium | high | critical
            suggested_fix: string
            cost_impact: optional string   # Risk, Cost & Scale Analyst가 태그

  # ── Phase 4.5: Validation ──
  validation:
    description: "Prototype Validator 출력"
    contains:
      - entries:
          - assumption_tested: string
            code_snippet: string
            result: pass | fail | inconclusive
            metrics: { latency_ms, memory_mb, cost_estimate }
            success_criteria: string       # 원저자가 정의한 기준

  # ── Phase 5: Decision ──
  decision:
    description: "평가 매트릭스, 최종 선택, 트레이드오프"
    contains:
      - hard_constraint_filter: [ { option_id, constraint_violated, eliminated: bool } ]
      - evaluation_matrix: { criteria: [], options: [], scores: [][] }
      - winner: { option_id, rationale } | null   # 전부 탈락 시 null
      - tradeoffs: [ { chosen, sacrificed, justification } ]
      - confidence_score: 0.0 ~ 1.0
      - status: decided | infeasible              # 정상 완료 or 후보 전멸
      - reason: optional string                   # infeasible일 때 사유

  # ── 시각화 ──
  diagrams:
    description: "Mermaid 코드, 시각화"
    contains:
      - entries:
          - type: c4_context | c4_container | c4_component | sequence | erd | flowchart | state
            mermaid_code: string
            abstraction_level: high | medium | low
            missing_elements_flag: [ string ]
```

### 2.2 항목 메타데이터 (모든 entry에 부착)

```yaml
entry_metadata:
  id: string                    # 고유 식별자
  author: agent_id              # 누가 썼는가
  timestamp: ISO-8601           # 언제 썼는가
  confidence: 0.0 ~ 1.0        # 확신도
  status: draft | reviewed | accepted | rejected | needs_input
          | deadlocked | no_contribution
  reason: optional string          # status 설명 (no_contribution 사유, rejected 사유 등)
  version: int                  # 같은 항목의 몇 번째 수정인지
  references: [entry_id]        # 이 항목이 근거로 삼은 다른 항목
  conflicts_with: [entry_id]    # 모순되는 항목
  cost_impact: optional string  # Risk, Cost & Scale Analyst가 태그
  evidence_level: anecdotal | empirical | theoretical | validated
  assumptions: [string]         # 이 항목이 가정하는 것들
  impact_on_decision: low | medium | high   # 의사결정에 미치는 영향도
  success_criteria: optional string  # 이 항목의 핵심 가정이 맞으려면 충족해야 할 조건
                                     # (예: "1만 TPS 버텨야 함", "응답 2초 이내")
                                     # Prototype Validator가 검증 시 이 기준을 사용
  needs_response_from: optional agent_id    # mediated query 대상
  response_to: optional entry_id            # 어떤 질문에 대한 답변인지
  tags: [string]                # 자유 태그 (예: "overridden_by_priority:simplicity",
                                #   "validation_failed_2x", "user_approved")
```

---

## 3. Blackboard 운영 규칙

### 3.1 상태 전이 규칙 (4원칙)

```
원칙 1: 자기 검증 금지
  - 저자(author)는 자기 항목을 draft → reviewed로 올릴 수 없다.
  - 자기 자신을 검증하는 것은 불가능하다.

원칙 2: Peer Review
  - 같은 슬롯에 대해 읽기 권한이 있는 다른 에이전트가 reviewed로 올린다.
  - 단, 해당 슬롯의 review 자격이 있는 에이전트만 가능하다 (아래 매트릭스 참조).

원칙 3: Conflict 해소 전제
  - conflicts_with가 1개라도 남아있으면 accepted로 승격 불가.
  - conflict 해소 = 관련 항목 중 하나가 rejected되거나 양쪽이 수정되어
    conflicts_with가 비워져야 함.

원칙 4: 영구 Conflict → Deadlock 강제 해결
  - 같은 두 항목 간에 conflict가 version 3 이상 유지되면
    → status: deadlocked
    → Deadlock Resolver가 Decision Evaluator에 위임
    → Decision Evaluator가 context.priorities 가중치로 강제 선택
    → 패배한 쪽은 rejected + "overridden_by_priority: {기준}" 태그
```

상태 전이 다이어그램:
```
draft ──(peer review)──→ reviewed ──(v1: Interaction Gate 사용자 승인)──→ accepted
  │                         │         (v2+: conflict 0 + 최신 version       │
  │                         │          + evidence ≥ empirical 시 자동)       │
  │                         │                                               │
  │                         ├──(conflict 발견)──→ draft (수정 필요)           │
  │                         │                                               │
  └──(불필요 판단)──→ rejected                                              │
                                                                            │
  ※ needs_input: 다른 에이전트에게 질문 중 (mediated query)
  ※ no_contribution: 에이전트가 meaningful output을 못 냄 (실패 프로토콜)
  ※ deadlocked: 3 version 이상 conflict 유지 → Decision Evaluator 강제 결정
```

### 3.2 Review 자격 매트릭스

각 슬롯을 reviewed로 올릴 수 있는 에이전트를 명시한다 (v1 운영 후 조정 가능):

```yaml
review_authority:
  context:        [problem_decomposer]
  problem:        [context_profiler, precedent_researcher]
  precedents:     [problem_decomposer, knowledge_curator]
  design_space:   [cross_domain_connector, invention_engine]
  cross_domain:   [design_space_explorer, knowledge_curator]
  inventions:     [cross_domain_connector, simplicity_advocate]
  architecture:   [simplicity_advocate, risk_cost_scale_analyst, data_strategist]
  relationships:  [data_strategist, structure_advisor]
  data_strategy:  [relationship_architect, risk_cost_scale_analyst]
  challenges:     [structure_advisor, decision_evaluator]
  validation:     [risk_cost_scale_analyst, decision_evaluator]
  decision:       [meta_verifier]                 # 최종 결정은 검증자만 review
  diagrams:       [structure_advisor, relationship_architect]
```

### 3.3 Accepted 승격 정책

v1 초기에는 **수동 승격**을 사용한다:
- Interaction Gate가 사용자에게 "이 항목을 accepted 해도 되나요?" 확인
- 사용자가 승인하면 accepted

v2 이후 자동 승격 전환 조건:
```
자동 승격 = reviewed + conflict 0 + 최신 version + evidence_level ≥ empirical
```

운영 패턴이 충분히 쌓이면(QOC 기록 50건 이상) 자동 승격으로 전환.

### 3.4 Mediated Query 프로토콜

에이전트 간 직접 통신 대신, Blackboard를 이벤트 버스처럼 활용한다.

```yaml
# 질문하는 에이전트가 Blackboard에 쓰는 항목:
question_entry:
  id: arch_q1
  author: structure_advisor
  content: "이벤트 소싱 쓰면 CQRS랑 충돌?"
  status: needs_input
  needs_response_from: data_strategist
  confidence: null                         # 아직 답이 없음
  references: [architecture.v3]

# Router 규칙:
- needs_response_from이 있고 status가 needs_input이면
  → 해당 에이전트를 다음 턴에 최우선 호출

# 답변하는 에이전트가 쓰는 항목:
response_entry:
  id: arch_a1
  author: data_strategist
  content: "이벤트 소싱 + CQRS는 상호보완적. 단, read model 별도 구축 필요."
  status: draft
  response_to: arch_q1
  references: [data_strategy.v2]
```

장점:
- Blackboard를 통한 mediated 통신이라 coupling 없음
- Recorder가 자동으로 질문/답변 기록
- 다른 에이전트도 그 질문을 볼 수 있음 ("아 그 질문 나도 궁금했는데")

### 3.5 사용자 피드백 루프

시스템이 결론을 내놓은 뒤 사용자가 피드백하면, 처음부터 다시 돌리지 않는다.

```yaml
# 사용자 피드백 수신 시:
on_user_feedback:
  1. challenges 슬롯에 새 항목 기록:
     - type: user_feedback
     - status: draft
     - content: 사용자 피드백 원문
     - severity: 사용자가 명시 또는 State Assessor가 추정

  2. 영향 받는 슬롯 식별:
     - 피드백 내용과 관련된 슬롯을 State Assessor가 판단
     - 예: "DB가 맘에 안 들어" → data_strategy, architecture

  3. 관련 에이전트 재호출:
     - Router가 해당 슬롯의 작성 에이전트를 호출
     - Phase 4 (Challenge)로 직접 점프

  4. 결과:
     - 전체 재실행 없이 해당 부분만 수정
     - Recorder가 "사용자 피드백에 의한 수정" QOC 기록
```

### 3.6 Garbage Collection (가비지 컬렉션)

Blackboard가 무한정 커지는 것을 방지한다. Recorder가 GC 실행 전에 반드시 QOC/ADR로 요약 보존한다.

```
GC 규칙:

1. Rejected 정리:
   - status: rejected이고 age > 2 라운드
   → Recorder가 QOC에 요약 보존 (왜 rejected됐는지 포함)
   → Blackboard에서 제거

2. 오래된 Version 정리:
   - 같은 항목의 version이 3개 이상
   → 최신 2개만 Blackboard에 유지
   → 나머지는 Recorder로 이동
   - 단, accepted 항목의 선행 version은 삭제하지 않고
     lineage summary로 압축 (어떻게 결론에 도달했는지 보존)

3. Phase 전환 시 정리:
   - 이전 Phase의 draft 항목을 archive 후보로 표시
   - 단, references가 남아있는 항목(다른 항목이 참조 중)은 유지
   - 참조 끊긴 draft만 Recorder로 이동 후 Blackboard에서 제거

4. needs_input 만료:
   - status: needs_input이고 2 라운드 이상 응답 없음
   → Recorder가 "미해결 질의" 기록
   → Blackboard에서 제거 또는 질문자에게 반환
```

---

## 4. Orchestrator: 4-Module Controller

Orchestrator는 에이전트가 아니라 시스템의 **제어 계층**이다. 4개 독립 모듈로 분해하여 God Agent 문제를 방지한다.

### 4.1 Router (규칙 기반)

```
역할: "다음 누구 차례인가"만 결정. LLM 판단 없이 규칙으로 동작.

핵심 규칙:

Phase 진입 조건:
  Phase 1:
  - context가 비어있으면          → Context Profiler 호출
  - problem이 비어있으면          → Problem Decomposer 호출
  - precedents가 비어있으면       → Precedent Researcher 호출

  Phase 2:
  - design_space가 비어있으면     → Design Space Explorer 호출
  - 3개 미만 valid_combinations   → Design Space Explorer 재호출
  - cross_domain이 비어있으면     → Cross-Domain Connector 호출
  - inventions가 비어있으면       → Invention Engine 호출

  Phase 3:
  - architecture가 비어있으면     → Structure Advisor 호출
  - relationships가 비어있으면    → Relationship Architect 호출
  - data_strategy가 비어있으면    → Data Strategist 호출

  Phase 4:
  - challenges가 0개면            → Simplicity Advocate 강제 호출

  Phase 4.5:
  - validation이 비어있고 Phase 4 완료면 → Prototype Validator 호출

Mediated Query 우선:
  - needs_response_from이 있고 status: needs_input
    → 해당 에이전트를 다음 턴에 최우선 호출

사용자 피드백:
  - user_feedback 타입의 challenge가 들어오면
    → 영향 받는 슬롯의 작성 에이전트 호출
    → Phase 4로 직접 점프

기본:
  - 현재 Phase의 모든 에이전트가 기여를 완료(또는 no_contribution)하면
    → State Assessor에게 Phase 충분성 평가 요청

Circuit Breaker:
  - 동일 Phase 내에서 특정 에이전트가 no_contribution을 냈다면,
    해당 에이전트의 입력 슬롯에 변경이 발생하지 않는 한 재호출하지 않음
  - 필수 슬롯(예: architecture)이 no_contribution으로 비어있으면:
    → State Assessor가 Phase 진행을 막음
    → Interaction Gate가 사용자에게 알림:
      "이 부분은 AI가 판단할 수 없습니다. 수동 입력이 필요합니다"
```

### 4.2 State Assessor (경량 LLM)

```
역할: "지금 Phase가 충분한가"를 평가. Router와 분리하여 각각 단순하게 유지.

판단 기준:
  - 현재 Phase의 모든 슬롯에 reviewed 이상 항목이 있는가?
    (v1에서는 accepted가 아닌 reviewed를 Phase 충분성 기준으로 사용.
     accepted는 최종 decision에서만 Interaction Gate 사용자 승인으로 부여.
     매 Phase마다 모든 슬롯을 사용자가 승인하면 시스템이 실질적으로 멈추므로.)
    (또는 해당 에이전트가 justified no_contribution을 냈는가?
     → no_contribution + reason이 있으면 "이 슬롯은 충분"으로 간주)
  - 핵심 질문(각 Phase별)에 답이 나왔는가?
  - 미해결 conflict가 남아있는가?
  - evidence_level이 모두 theoretical인 항목이 과반인가?

출력:
  - phase_sufficient: true | false
  - reason: string
  - suggestion: "Agent X가 추가 기여 필요" | "Phase 전환 가능"
```

### 4.3 Deadlock Resolver (이벤트 트리거)

```
역할: 교착 상태가 감지됐을 때만 호출. 상시가 아니라 event-triggered.

트리거 조건:
  - 같은 두 항목 간 conflict가 version 3 이상 유지 (상태 전이 원칙 4)
  - 같은 Phase에서 3라운드 이상 진전 없음
  - 2개 이상 에이전트가 연속으로 no_contribution

동작:
  1. 교착 원인 분석 (어떤 항목들이 충돌하는지)
  2. context.priorities 가중치 참조
  3. Decision Evaluator에게 강제 결정 위임
     또는 Interaction Gate에게 사용자 개입 요청
  4. 결과를 challenges 슬롯에 기록 (type: deadlock_resolution)

최대 시도: 2회. 2회 실패 시 Interaction Gate가 사용자에게 직접 질문.
```

### 4.4 Interaction Gate (사용자 타이밍)

```
역할: "사용자한테 물어볼 타이밍인가?"만 판단.
State Assessor와 분리 — State Assessor는 "뭘 해야 하나", 
Interaction Gate는 "사용자에게 물어야 하나".

트리거 조건 (OR):
  - confidence < 0.8인 accepted 후보가 있음
  - cost_of_error > 되돌릴 수 없는 결정 (DB 선택, 아키텍처 패턴 확정)
  - options.count ≥ 3 AND 상위 2개의 score 차이 < 0.15
  - user_preference_required == true (Context Profiler가 태그)
  - Deadlock Resolver가 사용자 개입 요청
  - accepted 승격 확인 (v1 수동 승격 정책)

동작 모드:
  - 동기식: Phase 2-3 경계에서 
    "5개 중 2개로 좁혔는데, 이 방향이 맞나요?"
  - 동기식: Phase 5 직전
    "최종안 나왔는데, 이 트레이드오프 괜찮나요?"
  - 동기식: priorities 확인
    "가장 중요한 두 가지가 단순성과 비용이 맞나요?"
    (숫자 자체보다 순위와 극단값을 확인)

출력:
  - 사용자 응답을 해당 슬롯에 기록
  - 또는 context.priorities 업데이트
```

---

## 5. Phase 1: Understanding (이해) — 3 Agents

### Agent 1: Context Profiler

```
핵심 질문: "누가, 어떤 상황에서, 무엇을 만들려 하는가?"

지식 기반:
  - Stakeholder Analysis
  - Resource Assessment
  - Constraint Mapping

하는 일:
  - 사용자의 기술 스택, 능력, 시간, 인프라 파악
  - "이 사람이 2주 안에 혼자 만들 수 있는가?"를 판단
  - 제약 조건 명시 (예산, 시간, 인력, 기술 수준)
  - hard_constraints와 priorities를 분리하여 수집
    - hard_constraints: 위반 시 즉시 탈락 (예: 예산 $500/월 이하)
    - priorities: 가중치 비교 (예: simplicity 0.3, cost 0.25)

Blackboard에 쓰는 것:
  - context 슬롯 전체:
    - user_profile (기술 수준, 도구, 환경)
    - hard_constraints 목록
    - priorities (가중치)
    - feasibility_boundary ("현실적으로 가능한 범위")

왜 별도 에이전트인가:
  - 최적의 아키텍처는 "누가 만드느냐"에 따라 완전히 달라짐
  - 다른 에이전트들은 이 정보를 전제로 깔고 작동함
  - 이걸 빠뜨리면 "이론적으로 최적이지만 만들 수 없는" 구조가 나옴
  - hard/soft constraint 분리가 Decision Evaluator의 정확도를 결정함

활성화: Phase 1 시작 시 최우선 호출
비활성화 조건: context 슬롯이 reviewed 이상
```

### Agent 2: Problem Decomposer

```
핵심 질문: "이 문제의 본질은 무엇이고, 어떻게 나뉘는가?"

지식 기반:
  - Domain-Driven Design (DDD): Bounded Context, Aggregate, Entity
  - Systems Theory: 구성 요소, 상호작용, 창발성
  - Complexity Science: 단순/복잡/혼돈 영역 분류 (Cynefin)

하는 일:
  - 아이디어를 핵심 도메인과 하위 문제로 분해
  - 문제의 성격 분류: 데이터 문제? 관계 문제? 흐름 문제? 학습 문제?
  - 각 하위 문제의 복잡도 평가
  - Bounded Context 식별 (어디서 경계를 나눌 것인가)

Blackboard에 쓰는 것:
  - problem 슬롯:
    - decomposition_tree (문제 분해 트리)
    - sub_problem_tags (data/relationship/flow/learning/...)
    - complexity_grade
    - ubiquitous_language (도메인 용어 사전)
    - bounded_contexts

왜 별도 에이전트인가:
  - 문제를 잘못 분해하면 이후 모든 단계가 틀어짐
  - DDD의 Bounded Context를 정확히 적용하려면 전문적 분석이 필요
  - 구조 설계와 분리해야 문제 정의가 구조에 끌려가지 않음

활성화: context가 draft 이상일 때
비활성화 조건: problem 슬롯이 reviewed 이상
```

### Agent 3: Precedent Researcher

```
핵심 질문: "이 문제를 누가 이미 풀었는가?"

지식 기반:
  - SOTA 논문/프로젝트 검색
  - 오픈소스 레포지토리 분석
  - 산업별 사례 연구

하는 일:
  - 유사한 시스템/프로젝트 검색
  - "이미 존재하는 해결책"과 "아직 없는 부분" 구분
  - 기존 솔루션의 장단점 분석
  - "바퀴를 다시 발명하지 마라" 검증

Blackboard에 쓰는 것:
  - precedents 슬롯:
    - similar_projects (각각의 접근법, 장단점, URL)
    - verified_stacks (검증된 기술 스택 조합)
    - reuse_list ("이 부분은 이미 있으니 가져다 쓸 것")
    - build_new_list ("이 부분은 새로 만들어야 함")

RAG 가드레일:
  - "이미 존재한다"고 주장할 때는 URL 또는 구체적 출처 3개 이상 필수
  - 출처가 없으면 evidence_level: anecdotal로 표시
  - 이 에이전트의 hallucination이 전체 시스템을 망가뜨리므로 가드레일 필수

왜 별도 에이전트인가:
  - "아는 것에 갇히는" 문제의 직접적 해결
  - 다른 에이전트들이 이론 기반이라면, 이건 실증 기반
  - 검색과 분석에 집중해야 hallucination이 줄어듦

활성화: context, problem이 draft 이상일 때
비활성화 조건: precedents 슬롯이 reviewed 이상
```

---

## 6. Phase 2: Exploration (탐색) — 3 Agents

### Agent 4: Design Space Explorer

```
핵심 질문: "가능한 모든 접근법이 테이블 위에 있는가?"

지식 기반:
  - Design Space Exploration (DSE)
  - Morphological Analysis (차원별 조합 탐색)
  - Wardley Mapping (가치 사슬 분석)

하는 일:
  - 문제의 각 차원(저장, 통신, 처리, UI 등)별로 가능한 옵션 나열
  - 조합 가능성 생성 (Morphological Box)
  - 명백히 불가능한 조합 제거
  - "아무도 생각 안 한 조합"을 의도적으로 탐색

Blackboard에 쓰는 것:
  - design_space 슬롯:
    - dimension_options (차원별 옵션 매트릭스)
    - valid_combinations (유효한 조합 목록)
    - eliminated_combinations (제거된 조합 + 이유)

왜 별도 에이전트인가:
  - "선택지를 넓히는 것"과 "선택하는 것"은 반대 사고방식
  - 같은 에이전트가 둘 다 하면 탐색이 좁아짐
  - 의도적으로 발산적 사고에 집중해야 함

활성화: Phase 1의 3개 슬롯이 모두 draft 이상일 때
비활성화 조건: valid_combinations ≥ 3개이고 reviewed 이상
```

### Agent 5: Cross-Domain Connector

```
핵심 질문: "다른 분야에서 이 문제를 어떻게 풀었는가?"

지식 기반:
  - Category Theory (구조 간 유사성 매핑)
  - Biomimicry (자연에서 영감)
  - 분야 간 유추 (생물학↔컴퓨터, 경제학↔네트워크 등)
  - Topology (구조적 동치 관계)

하는 일:
  - 현재 문제의 추상적 구조를 추출
  - 다른 분야에서 같은 구조를 가진 해결책 검색
  - "당신의 블록 분류 문제는 생물학의 종 분류와 구조가 같다" 같은 통찰
  - 의외의 분야에서 가져온 해결책 제안

Blackboard에 쓰는 것:
  - cross_domain 슬롯:
    - structural_mappings (구조적 유사성)
    - alternative_perspectives ("이런 관점도 있다")

왜 별도 에이전트인가:
  - "아는 것에 갇히는" 문제의 가장 강력한 해결책
  - 소프트웨어만 아는 사람은 소프트웨어 해법만 생각함
  - Category Theory 관점은 다른 에이전트와 완전히 다른 사고 방식
  - 이 에이전트가 없으면 시스템이 결국 한 분야에 갇힘

활성화: problem, design_space가 draft 이상일 때
비활성화 조건: cross_domain 슬롯이 reviewed 이상
```

### Agent 6: Invention Engine

```
핵심 질문: "기술적 모순을 어떻게 돌파하는가?"

지식 기반:
  - TRIZ 40가지 발명 원리 + 모순 매트릭스
  - Constraint Satisfaction Problem (CSP)
  - Lateral Thinking (수평적 사고)

하는 일:
  - "A를 개선하면 B가 나빠진다" 같은 모순 식별
  - TRIZ 원리 중 적용 가능한 것 제안
  - 제약 조건들을 동시에 만족하는 해 탐색
  - "불가능해 보이는" 문제에 대한 창의적 우회 경로

Blackboard에 쓰는 것:
  - inventions 슬롯:
    - contradictions (식별된 기술적 모순)
    - triz_applications (적용 가능한 TRIZ 원리 + 구체적 방법)
    - csp_solutions (있다면)
    - creative_alternatives

왜 별도 에이전트인가:
  - 다른 에이전트들이 "이건 안 된다"고 했을 때 작동
  - 모순 해결은 완전히 다른 사고 프레임이 필요
  - TRIZ 40원리를 정확히 적용하려면 전문적 매핑이 필요

읽기 특이사항: precedents를 읽음 — TRIZ로 모순 돌파할 때
  "이미 누가 이렇게 풀었나"를 모르면 바퀴 재발명

활성화: problem + design_space가 draft 이상일 때
        (challenges는 있으면 참고하지만, 없어도 활성화 가능 — Phase 2 첫 라운드에서도 동작해야 함)
비활성화 조건: inventions 슬롯이 reviewed 이상
```

---

## 7. Phase 3: Design (설계) — 3 Agents

### Agent 7: Structure Advisor

```
핵심 질문: "이 시스템의 뼈대를 어떻게 세울 것인가?"

지식 기반:
  - 소프트웨어 아키텍처 패턴:
    Microservices, Event-Driven, Layered, Hexagonal,
    CQRS, Actor Model, Pipe-and-Filter, Blackboard
  - AI/에이전트 아키텍처:
    MAS, Swarm, Orchestrator, MoE, ReAct, CoT,
    Multi-Agent Debate, Constitutional AI
  - 분산 시스템 패턴

하는 일:
  - 문제 성격(Phase 1)과 선택지(Phase 2)를 보고 아키텍처 제안
  - 패턴 조합 가능성 탐색 (예: Hexagonal + Event-Driven)
  - 각 패턴의 전제 조건과 제약 명시
  - Context Profiler의 제약을 반영한 현실적 제안

필수 출력 — 변경 용이성 (Evolution Planner 역할 포함):
  - changeability_score: 0.0 ~ 1.0
  - change_scenarios:
      각 시나리오별 effort(high/medium/low)와 영향 범위
      예: "DB 교체": effort: high, files_touched: 12
          "에이전트 추가": effort: low, files_touched: 2
  - 이 출력이 없으면 reviewed로 승격 불가

Blackboard에 쓰는 것:
  - architecture 슬롯:
    - recommended (1~3개 아키텍처 + 전제조건)
    - anti_patterns ("이 패턴을 쓰면 안 되는 이유")
    - changeability_score + change_scenarios
    - component_breakdown

왜 별도 에이전트인가:
  - 아키텍처 패턴이 20개 이상이고 조합까지 하면 수백 가지
  - 패턴 선택은 문제 분해, 데이터 설계와 독립적 전문성
  - 에이전트 아키텍처까지 포함하면 지식량이 매우 큼

활성화: Phase 2의 3개 슬롯 중 최소 2개가 draft 이상
비활성화 조건: architecture가 reviewed 이상
```

### Agent 8: Relationship Architect

```
핵심 질문: "요소들이 어떻게 연결되는가?"

지식 기반:
  - Graph Theory: DAG, 순환, 최단 경로, 중심성
  - Network Science: 커뮤니티, 허브, 클러스터링
  - Ontology: 개념 계층, is-a/has-a/part-of 관계
  - Set Theory: 집합 연산, 포함 관계

하는 일:
  - 엔티티 간 관계 유형 정의 (계층? 네트워크? 순서?)
  - 그래프 구조 설계 (방향? 가중치? 다중?)
  - 관계의 제약 조건 정의
  - 순환 의존성, 고아 노드 등 구조적 문제 감지

Blackboard에 쓰는 것:
  - relationships 슬롯:
    - entity_graph (노드와 엣지)
    - relation_types (from, to, type, cardinality)
    - structural_constraints
    - potential_issues (순환, 병목 등)

왜 별도 에이전트인가 (Data Strategist와 분리하는 이유):
  - 관계 설계는 저장(Data)과도, 구조(Structure)와도 다른 관심사
  - Graph Theory + Ontology + Network Science를 동시에 적용해야 함
  - 합치면 "PostgreSQL에 넣기 쉬운 관계"로 휘어짐
  - 관계 구조가 저장소에 끌려가면 안 됨 — 분리가 핵심

활성화: problem, architecture가 draft 이상
비활성화 조건: relationships가 reviewed 이상
```

### Agent 9: Data Strategist

```
핵심 질문: "데이터를 어떻게 저장하고, 흐르게 하고, 검색할 것인가?"

지식 기반:
  - Database Theory: RDB, Document, Graph, Time-series, Vector
  - Information Theory: 엔트로피, 신호 대 잡음비
  - Data Modeling: 정규화, 비정규화, 이벤트 소싱
  - Knowledge Graph: 지식 표현, 추론

하는 일:
  - 데이터의 성격 분석 (정형? 비정형? 관계 중심? 시계열?)
  - 적합한 DB 유형 추천
  - 데이터 흐름 설계 (어디서 생성, 어디서 변환, 어디서 소비)
  - 검색/쿼리 패턴 예측 및 인덱싱 전략

Blackboard에 쓰는 것:
  - data_strategy 슬롯:
    - data_model (스키마 또는 스키마리스 설계)
    - db_recommendation (유형 + 이름 + 근거)
    - data_flow (소스 → 변환 → 싱크)
    - query_patterns (패턴 + 인덱싱 전략)

왜 별도 에이전트인가 (Relationship Architect와 분리하는 이유):
  - 잘못된 DB 선택은 나중에 바꾸기 가장 비싼 결정
  - 데이터 관심사는 구조 관심사, 관계 관심사와 독립적
  - Information Theory 관점(어떤 데이터가 가치 있는가)은 다른 에이전트에 없음

활성화: problem, architecture, relationships가 draft 이상
비활성화 조건: data_strategy가 reviewed 이상
```

---

## 8. Phase 4: Challenge (도전) — 2 Agents

> ⚡ **이 Phase는 반드시 거쳐야 한다.** Challenge 없는 설계는 과설계로 가는 지름길.

### Agent 10: Simplicity Advocate

```
핵심 질문: "이거 너무 복잡한 거 아냐?"

지식 기반:
  - Axiomatic Design: 독립성 공리, 정보 공리
  - YAGNI / KISS 원칙
  - Occam's Razor
  - 기술 부채 패턴

하는 일:
  - 다른 에이전트들의 제안을 보고 "이거 과하다" 반박
  - 더 단순한 대안 제시
  - "지금 필요한 것"과 "나중에 필요할지도 모르는 것" 구분
  - Phase 1의 제약 조건 대비 복잡도 체크

Blackboard에 쓰는 것:
  - challenges 슬롯:
    - type: simplicity
    - severity + suggested_fix
    - "이건 나중에 해도 된다" 목록
    - "이 복잡도는 정당화된다 / 안 된다" 판정

왜 별도 에이전트인가:
  - 다른 에이전트들은 본능적으로 "더 많이, 더 정확하게" 추구
  - 의도적으로 반대 방향을 주장하는 역할이 없으면 시스템이 과설계됨
  - 이 에이전트는 adversarial(적대적) 역할 — 다른 에이전트를 견제
  - 가장 중요하지만 가장 무시되는 관점

활성화: architecture, relationships, data_strategy 중 하나라도 draft 이상
비활성화 조건: 모든 challenge 항목이 처리됨 (fixed 또는 accepted)
```

### Agent 11: Risk, Cost & Scale Analyst

```
핵심 질문: "뭐가 잘못될 수 있고, 얼마 들고, 커지면 어떻게 되는가?"

지식 기반:
  - Failure Mode Analysis (FMEA)
  - Cybernetics: 피드백 루프, 안정성
  - 확장성 패턴: 수평/수직, 캐싱, 큐
  - 보안 기본 원칙
  - 비용 추정 모델 (인프라, API 호출, 인건비)

하는 일:
  - 제안된 구조의 실패 지점 식별
  - "사용자 10명일 때는 되지만 1만 명이면?" 분석
  - 단일 장애 지점 (SPOF) 감지
  - 보안 취약점 기본 체크
  - 기술 부채 누적 경고
  - 비용 영향 분석 (cost_impact 태그 부착)
  - "월 100달러 이하" "2초 안에 응답" 같은 현실 제약 검증

Blackboard에 쓰는 것:
  - challenges 슬롯:
    - type: risk | cost | scale
    - severity
    - 리스크 매트릭스 (확률 × 영향도)
    - 실패 시나리오 목록
    - 스케일 병목 지점
    - cost_impact 태그 (다른 에이전트 항목에도 부착)
    - 완화 방안

왜 별도 에이전트인가 (Cost Auditor를 흡수한 이유):
  - 비용도 리스크의 일종임 — "예산 초과"는 "서버 다운"만큼 치명적
  - 리스크 분석가가 이미 "커지면 어떻게 되는가"를 보니까
    "커지면 얼마 드는가"는 같은 사고 흐름
  - 별도 Cost Auditor를 두면 challenges에 두 에이전트가 비슷한 걸 씀
  - Simplicity Advocate와 함께 "도전 팀"으로 설계 팀을 견제

활성화: architecture, relationships, data_strategy 중 하나라도 draft 이상
비활성화 조건: 모든 challenge 항목이 처리됨
```

### Phase 4 루프백 규칙

```
Challenge 결과에 따른 분기:

1. suggested_fix가 있는 challenge → 해당 슬롯의 에이전트가 수정
   예: Simplicity Advocate가 "이 마이크로서비스 3개는 1개로 합쳐도 됨"
   → Structure Advisor가 architecture 수정

2. severity: critical인 challenge → Phase 2 또는 3로 복귀
   예: Risk Analyst가 "이 아키텍처는 근본적으로 SPOF"
   → Design Space Explorer부터 재탐색

3. 모든 challenge가 처리되면 → Phase 4.5 (Validation)으로 진행

4. Challenge 처리 후에도 반박이 남으면:
   → 최대 3라운드까지 반복
   → 3라운드 후에도 미해결이면 Deadlock Resolver 개입
```

---

## 9. Phase 4.5: Validation (검증) — 1 Agent

### Agent 12: Prototype Validator

```
핵심 질문: "제안된 구조의 핵심 가정이 실제로 작동하는가?"

지식 기반:
  - Spike Solution / Walking Skeleton
  - Load Testing 기초
  - Benchmark 설계
  - Feasibility Analysis

하는 일:
  - 핵심 가정 중 검증이 필요한 것을 자동 필터링 (아래 규칙 참조)
  - 최소 실행 코드 생성 (Python/TS, 50~100줄)
  - 로컬 실행 또는 시뮬레이션
  - 결과: pass/fail + 실제 측정치

검증 대상 자동 필터링 규칙:
  조건 (AND):
    - evidence_level == theoretical
    - confidence < 0.7
    - impact_on_decision == medium 이상
  우선순위:
    - impact_on_decision 높은 것 우선
    - 동점이면 confidence 낮은 것 우선
  제한:
    - 한 라운드에 최대 2개 가정만 검증
    - 코드 상한: 100줄
    - 실행 시간 상한: 30초
    - success_criteria가 원저자에 의해 원본 항목의 메타데이터에 정의되어 있어야 함
      (예: Structure Advisor가 architecture 항목을 쓸 때
       success_criteria: "1만 TPS 버텨야 함"을 같이 적음)
      → 없으면 검증 불가 → 원저자에게 반환 (needs_input)

Blackboard에 쓰는 것:
  - validation 슬롯:
    - assumption_tested
    - code_snippet
    - result: pass | fail | inconclusive
    - metrics: { latency_ms, memory_mb, cost_estimate }
    - success_criteria (원저자가 정의한 기준)
  
  검증 후 원본 항목의 메타데이터 업데이트:
    - pass → evidence_level: empirical → validated로 승격
    - fail → 해당 항목에 conflict 추가, severity: critical
    - inconclusive → evidence_level은 유지, 추가 검증 필요 태그

  Validation 루프 상한 (무한 루프 방지):
    - 동일한 설계 옵션이 Validation에서 2회 이상 fail 판정을 받으면:
      → 해당 옵션은 강제 rejected (tags: ["validation_failed_2x"])
      → Decision Evaluator가 다른 대안을 선택해야 함
      → 대안이 없으면 Interaction Gate가 사용자에게
        "검증 통과하는 옵션이 없습니다. 제약 조건 조정이 필요합니다" 알림

왜 별도 에이전트인가:
  - 지금까지 모든 에이전트가 "생각"만 함. 아무도 "해보지" 않음
  - Risk Analyst가 "이게 깨질 수 있다"는 이론이고,
    Prototype Validator가 "실제로 깨졌다"는 증거
  - Decision Evaluator가 "이론상 최적"이 아니라 "검증된 최적"을 선택하게 됨
  - TDD적 접근: 에이전트는 "이걸 통과하면 내 주장이 맞다"를 먼저 정의해야 함

위치: Phase 4 (Challenge) 후, Phase 5 (Decision) 전
활성화: challenges가 모두 처리되고 validation이 비어있을 때
비활성화 조건: 검증 대상이 0개이거나 validation이 reviewed 이상
```

---

## 10. Phase 5: Decision (결정) — 1 Agent

### Agent 13: Decision Evaluator

```
핵심 질문: "모든 것을 고려했을 때, 어떤 선택이 최적인가?"

지식 기반:
  - Multi-Criteria Decision Making (MCDM)
  - Trade-off Analysis
  - Decision Matrix (Pugh Matrix)
  - Decision Science
  - Constraint Satisfaction

하는 일 — 2단계 평가:

  단계 1: Hard Constraint 필터 (탈락 조건)
    - context.hard_constraints를 기준으로 후보 제거
    - 예: 예산 초과 → 즉시 탈락
    - 예: 기한 초과 → 즉시 탈락
    - 예: 혼자 구현 불가 → 즉시 탈락
    - 결과: hard_constraint_filter에 기록
    - ⚠️ 전부 탈락 시:
      → decision.winner: null
      → decision.status: infeasible
      → decision.reason: "모든 후보가 hard constraint를 위반함"
      → Interaction Gate가 사용자에게 알림:
        "현재 제약 조건으로는 실현 가능한 아키텍처가 없습니다.
         제약 조건 완화가 필요합니다."
      → 사용자 응답을 context.hard_constraints에 반영 후 Phase 3 복귀

  단계 2: Weighted Scoring (남은 후보만)
    - context.priorities 가중치로 평가 매트릭스 구성
    - 각 선택지를 기준별로 평가
    - validation 결과 반영 (validated > empirical > theoretical)
    - 최종 추천 + 근거 + 포기하는 것 명시

Blackboard에 쓰는 것:
  - decision 슬롯:
    - hard_constraint_filter (어떤 후보가 왜 탈락했는지)
    - evaluation_matrix (선택지 × 기준 × 점수)
    - winner (최종 추천 + 근거) | null (전부 탈락 시)
    - tradeoffs ("이걸 선택하면 X는 포기")
    - confidence_score
    - status: decided | infeasible
    - reason (infeasible일 때 사유)

Deadlock 강제 결정 역할:
  - Deadlock Resolver가 위임한 영구 conflict에 대해
  - context.priorities 가중치로 어느 쪽 관점이 우선인지 결정
  - 패배한 쪽에 rejected + "overridden_by_priority" 태그

왜 별도 에이전트인가:
  - "평가"를 "제안"하는 에이전트가 하면 자기 제안에 편향됨
  - 중립적으로 모든 에이전트의 기여를 종합하는 역할 필요
  - hard constraint 필터와 weighted scoring을 분리 실행해야
    "기한 넘기지만 확장성 높아서 1등" 같은 이상한 결과 방지

활성화: Phase 4.5 완료 후 (또는 Deadlock Resolver 위임 시)
비활성화 조건: decision이 reviewed 이상
```

---

## 11. 상시 작동 에이전트 — 4 Agents

### 11.1 활성화 정책

상시 작동은 "항상 LLM을 돌린다"가 아니라, 특정 이벤트에 반응한다:

```
에이전트             트리거 조건                        빈도
─────────────────────────────────────────────────────────────
Recorder            Blackboard에 항목이 쓰이거나        매 턴
                    status가 변경될 때
                    
Modeler             Phase 5 완료 후                     최종 1회
                    (또는 사용자가 명시적 요청 시)
                    
Knowledge Curator   Phase 전환 시                       Phase당 1회
                    (또는 에이전트가 개념 참조 요청 시)
                    
Meta Verifier       사용자가 명시적으로 호출할 때         요청 시
                    (또는 Phase 5 직전 자동 1회)
```

### Agent 14: Recorder (상시)

```
핵심 질문: "무슨 판단이 있었고, 왜, 어떤 맥락에서?"

지식 기반:
  - QOC (Questions, Options, Criteria)
  - ADR (Architecture Decision Records)
  - IBIS (Issue-Based Information System)
  - DRL (Decision Representation Language)

하는 일:
  - Blackboard의 모든 변경을 시간순으로 기록
  - 에이전트 간 합의/반박 과정을 QOC 형식으로 변환
  - 결정마다 자동으로 ADR 생성
  - 패턴 분석: "이 사용자는 성능보다 단순성을 우선하는 경향"
  - 과거 결정과의 일관성 체크
  - GC 실행 전 보존 (rejected 항목 요약, 오래된 version의 lineage summary)
  - Observability 메트릭 수집 (아래 참조)
  - 시스템 평가 데이터 축적 (아래 참조)

상세 설계 — QOC 변환 규칙:

  1. 새 항목이 쓰이면:
     - Question: 해당 슬롯의 핵심 질문 + 구체적 맥락
     - Option: 항목의 content
     - Criteria: context.priorities에서 관련 기준 추출

  2. conflict가 등록되면:
     - 기존 QOC에 반박(Counter-argument) 추가
     - 양쪽 근거(references) 정리

  3. status가 accepted로 변경되면:
     - QOC 마감 + ADR 생성
     - ADR 형식:
       - Title: 결정 요약
       - Status: Accepted
       - Context: 해당 시점의 관련 슬롯 상태 요약
       - Decision: 선택한 것 + 근거
       - Consequences: 트레이드오프 + 영향

  4. rejected가 되면:
     - QOC에 "기각 이유" 기록
     - GC 보존용 요약 생성

  5. deadlocked → 강제 결정 시:
     - 특별 ADR: "강제 결정" 태그 + 사용자 priority 근거

저장소:
  - Blackboard 외부의 별도 저장소에 보관
  - QOC 기록: 시간순 + 슬롯별 인덱스
  - ADR 문서: 번호순 (ADR-001, ADR-002, ...)
  - 패턴 분석: 사용자별 누적 데이터

GC 담당 역할:
  - Blackboard에서 제거되는 항목을 QOC/ADR로 보존
  - lineage summary 생성 (accepted 항목의 선행 version 압축)
  - "왜 이 선택지가 버려졌는지" 항상 추적 가능하게 유지

Observability (관측 가능성):
  Recorder가 QOC 외에 시스템 레벨 메트릭도 수집한다.
  별도 에이전트 불필요 — Recorder가 이미 모든 변경을 보고 있으므로 자연스럽게 확장.

  tracing:
    - 각 에이전트 호출마다 trace_id 생성
    - Blackboard 쓰기/읽기 모두 로그
    - Phase 전환 시점 기록

  metrics:
    - 에이전트별 latency (호출 → 출력까지 시간)
    - 에이전트별 토큰 사용량 (읽기 뷰 효과 측정)
    - conflict 발생률 (Phase별, 에이전트별)
    - deadlocked 발생 횟수
    - no_contribution 비율 (에이전트별)

  system_logging:
    - Router 결정 이유 (어떤 규칙이 매칭됐는지)
    - State Assessor 판단 근거
    - Interaction Gate 호출 사유 + 사용자 응답

Evaluation (시스템 평가):
  Recorder가 패턴 분석할 때 같이 수집. 로드맵 Phase 5 (학습하는 시스템)의 기초 데이터.

  agent_performance:
    - 각 에이전트의 accepted 비율
    - no_contribution 빈도
    - conflict 유발률 (이 에이전트가 다른 항목과 얼마나 자주 충돌하는가)

  system_metrics:
    - Phase별 소요 시간
    - 총 토큰 사용량 (세션당)
    - 사용자 만족도 (Interaction Gate 피드백 + 최종 사용자 확인)

  quality_gates (경고 조건):
    - evidence_level: theoretical이 전체의 50% 초과 → 경고
    - confidence 평균이 0.5 미만 → 경고
    - deadlocked 발생률이 세션당 2회 초과 → 구조 재검토 권고

Blackboard에 쓰는 것:
  - Blackboard에는 직접 쓰지 않음 (단방향: 읽기 전용)
  - 별도 QOC/ADR 저장소에 기록
  - 예외: 과거 결정과 충돌 감지 시 challenges에
    type: consistency_warning으로 기록

왜 별도 에이전트이며 상시인가:
  - 기록은 "항상" 일어나야 하며, 다른 작업에 방해되면 안 됨
  - 4가지 기록 체계(QOC/ADR/IBIS/DRL)를 상황에 맞게 선택
  - 패턴 분석은 장기적으로 메타 아키텍트의 핵심 데이터
  - GC의 보존 담당이 분리되어야 "삭제하면서 기록"이 안전함
  - QOC 기록은 다른 에이전트 출력에 의존하지만
    다른 에이전트에 영향을 안 줌 → 완전히 단방향이라 분리가 깔끔

활성화: 매 턴 (Blackboard 변경 이벤트마다)
비활성화 조건: 없음 (시스템 종료 시까지)
```

### Agent 15: Modeler (최종 출력 시)

```
핵심 질문: "이걸 어떻게 눈으로 볼 수 있게 만드는가?"

지식 기반:
  - C4 Model (4단계 줌: Context → Container → Component → Code)
  - UML (클래스, 시퀀스, 유스케이스, 활동, 상태)
  - State Machine / Statechart
  - Flowchart / BPMN
  - ER Diagram
  - Mermaid / PlantUML 문법

하는 일:
  - decision 슬롯의 winner를 먼저 확인하고, 해당 옵션에 포함된 항목만 시각화
    (winner 없이 모든 옵션을 다이어그램으로 그리는 참사 방지)
  - Blackboard의 설계 내용을 적합한 다이어그램으로 변환
  - 추상도에 맞는 시각화 선택 (전체 그림 → C4 Context, 세부 → UML)
  - 에이전트 간 상호작용을 시퀀스 다이어그램으로
  - 데이터 흐름을 ERD/플로우차트로
  - Context Profiler의 user_technical_level을 읽고 복잡도 조절
    (출력 레이어 역할 — HITL Translator 불필요)

Blackboard에 쓰는 것:
  - diagrams 슬롯:
    - type (c4_context, sequence, erd 등)
    - mermaid_code
    - abstraction_level
    - missing_elements_flag ("이 수준의 추상화에서 빠진 것")

왜 별도 에이전트인가:
  - 시각화는 이해를 돕는 것이지 설계가 아님 — 분리해야 함
  - C4의 4단계 줌을 제대로 쓰려면 전문적 판단이 필요
  - 적절한 다이어그램 유형 선택이 이해도에 큰 영향

활성화: Phase 5 완료 후 (또는 사용자 명시적 요청)
비활성화 조건: diagrams가 reviewed 이상
```

### Agent 16: Knowledge Curator (Phase 전환 시)

```
핵심 질문: "60개 개념 중 지금 이 문제에 관련 있는 건 뭔가?"

지식 기반:
  - 조사 목록의 60+ 개념 전체
  - 각 개념의 적용 조건, 한계, 다른 개념과의 관계
  - Ontology (개념 간 관계 정의)
  - Semiotics (용어와 의미의 정확한 매핑)
  - RAG (검색 기반 지식 제공)

하는 일:
  - Phase 전환 시 다음 Phase에 관련된 개념을 자동으로 서핑
  - "이 문제에 Information Theory가 관련 있다"를 다른 에이전트에게 알림
  - 개념 간 관계 유지 (Graph Theory와 Network Science의 차이점 등)
  - 핵심 용어 정의 (shared vocabulary 역할):
    relationship, entity, event, constraint, evidence 등
    → 다른 에이전트가 이 사전을 참조하여 용어 혼동 방지
  - 조사 목록의 체크박스 자동 업데이트
  - 새로운 개념 발견 시 목록에 추가

Blackboard에 쓰는 것:
  - 각 슬롯에 "관련 개념" 주석으로 추가
  - 핵심 용어 정의 (context 슬롯에 vocabulary 섹션)
  - "이 개념은 아직 조사 안 됨 — 조사 필요" 플래그

왜 별도 에이전트인가 (Meta Verifier와 분리하는 이유):
  - 사서(librarian)와 감사(auditor)는 완전히 다른 역할
  - 합치면 검증자가 새로운 개념을 도입하면서 판정 → 중립성 상실
  - 60개 개념을 모든 에이전트가 아는 것은 비효율적
  - "지금 이 책이 필요하다"를 알려주는 전문 사서 역할

활성화: Phase 전환 시 (또는 에이전트가 개념 참조 요청 시)
비활성화 조건: 다음 Phase의 에이전트들이 모두 활성화된 후
```

### Agent 17: Meta Verifier (요청 시)

```
핵심 질문: "이 전체 시스템의 출력이 일관적이고 신뢰할 수 있는가?"

지식 기반:
  - Systems Engineering: 전체 시스템 정합성
  - Cybernetics: 피드백 루프, 자기 수정
  - Philosophy of Science: 검증 가능성, 반증 가능성
  - Epistemology: 지식의 확실성 수준
  - Constitutional AI: 원칙 기반 검증

하는 일:
  - 에이전트 간 출력의 모순 감지
  - "Structure Advisor는 A를 추천하는데 Data Strategist는 A와 안 맞는 B를 추천"
  - 전체 제안의 논리적 일관성 검증
  - conflicts_with 필드를 기반으로 그래프 순회
  - references 체인을 따라가며 근거의 타당성 검증
  - evidence_level 분포 분석 ("대부분 theoretical이면 경고")
  - "우리가 모르는 것"을 명시적으로 표시

Blackboard에 쓰는 것:
  - 별도 일관성 보고서 (Recorder에 전달)
  - 모순 목록 → challenges에 type: inconsistency로 기록
  - "불확실한 영역" 플래그
  - 최종 품질 등급

왜 별도 에이전트인가 (Knowledge Curator와 분리하는 이유):
  - 정보 제공자(사서)와 논리 검증자(감사)는 이해 상충
  - 합치면 검증자가 스스로 새 개념을 들여오면서 판정 → 중립성 흐림
  - 자기 자신을 검증하는 것은 불가능 — 독립적 검증자 필요
  - 17개 에이전트의 출력을 동시에 보고 교차 검증하는 역할

활성화: 사용자 명시적 호출 (또는 Phase 5 직전 자동 1회)
비활성화 조건: 일관성 보고서 완료 후
```

---

## 12. 에이전트별 Blackboard 읽기/쓰기 뷰

에이전트가 관련 슬롯만 읽으면 토큰이 40~60% 절감된다.

```
에이전트                   읽기                              쓰기
──────────────────────────────────────────────────────────────────────────

Phase 1:
Context Profiler          (없음 — 첫 주자)                   context
Problem Decomposer        context                           problem
Precedent Researcher      context, problem                  precedents

Phase 2:
Design Space Explorer     problem, precedents, context      design_space
Cross-Domain Connector    problem, design_space             cross_domain
Invention Engine          problem, design_space,            inventions
                          precedents, challenges(optional)

Phase 3:
Structure Advisor         problem, design_space,            architecture
                          cross_domain, inventions,
                          context, precedents
Relationship Architect    problem, architecture             relationships
Data Strategist           problem, architecture,            data_strategy
                          relationships

Phase 4:
Simplicity Advocate       architecture, relationships,      challenges
                          data_strategy, context
Risk, Cost & Scale        architecture, relationships,      challenges
  Analyst                 data_strategy, context

Phase 4.5:
Prototype Validator       architecture, data_strategy,      validation
                          validation(기존)
                          # success_criteria는 architecture/data_strategy
                          # 항목의 메타데이터에서 읽음 (별도 슬롯 아님)

Phase 5:
Decision Evaluator        전체                               decision

상시:
Recorder                  전체 (수동 감시)                    별도 QOC/ADR 저장소
                                                            (예외: challenges에
                                                             consistency_warning)
Modeler                   architecture, relationships,      diagrams
                          data_strategy, decision
Knowledge Curator         problem, design_space,            각 슬롯에 주석
                          challenges
Meta Verifier             전체                               challenges
                                                            (type: inconsistency)
```

---

## 13. 에이전트 공통 프로토콜

### 13.1 에이전트 실패 프로토콜

에이전트가 meaningful output을 못 내는 경우를 처리한다. 억지 출력(hallucination의 온상)을 방지.

```yaml
failure_protocol:
  trigger: 에이전트가 자신의 핵심 질문에 답할 수 없을 때
  
  동작:
    1. 해당 슬롯에 특수 항목 기록:
       - status: no_contribution
       - reason: "이 문제에 대한 타 분야 유사성을 찾지 못함"
       - confidence: 0.0
    
    2. Router가 해당 에이전트를 이번 라운드에서 skip
    
    3. Recorder가 "이 에이전트가 기여 못 한 이유" QOC 기록
    
    4. State Assessor가 "이 에이전트 없이 Phase가 충분한가" 재평가
       - 충분하면 → 다음 Phase로
       - 불충분하면 → 관련 에이전트에게 보완 요청
         (예: Cross-Domain Connector가 실패하면
          Design Space Explorer에게 추가 탐색 요청)

  원칙:
    - "모르겠다"는 유효한 출력이다
    - 억지로 무언가를 만들어내는 것보다 낫다
    - no_contribution이 시스템을 멈추지 않는다
```

### 13.2 에이전트 Lazy Loading 정책

17개 에이전트를 동시에 활성화하지 않는다. 필요할 때만 로드.

```
활성화 규칙:
  - Router가 호출할 때만 활성화
  - Phase 내에서도 필요한 에이전트만 깨움
  - 슬롯이 이미 accepted면 해당 에이전트 호출하지 않음
  
비활성화 규칙:
  - 담당 슬롯이 reviewed 이상이면 비활성화
  - no_contribution 후 비활성화
  - Phase가 넘어가면 이전 Phase 에이전트 비활성화

결과:
  - 동시 활성 에이전트 수: 평균 2~4개
  - 토큰 비용: 17개 eager loading 대비 70% 절감
```

### 13.3 출력 레이어 (HITL Translator 대체)

별도 에이전트가 아닌, 모든 에이전트의 최종 출력에 적용되는 포맷팅 규칙.

```
규칙:
  - context.user_profile.technical_level을 참조
  - technical_level: beginner → 전문 용어에 한줄 설명 추가
  - technical_level: intermediate → 용어 그대로, 근거 요약 제공
  - technical_level: expert → 원문 그대로
  
적용 대상:
  - Modeler: 다이어그램 복잡도 조절
  - Decision Evaluator: 최종 보고서의 설명 수준 조절
  - 사용자에게 직접 표시되는 모든 출력
```

### 13.4 Security & Governance (보안 및 거버넌스)

기존 구조가 이미 기본 보안 원칙을 갖추고 있음을 명시한다. 별도 구현 불필요.

```yaml
security_governance:
  access_control:
    - 에이전트는 자신의 읽기/쓰기 뷰(12장) 외 슬롯 접근 불가
    - Blackboard 제약으로 강제 (DB 권한 수준)
    - 상태 전이 4원칙이 무단 승격 방지

  audit_trail:
    - Recorder의 QOC/ADR이 감사 추적(audit trail) 역할
    - who(author) / when(timestamp) / why(references, reason) 모두 기록
    - Observability 로그가 시스템 레벨 감사 보완

  data_retention:
    - GC 규칙(3.6)이 데이터 보존 정책 역할
    - Recorder가 보존 기간 관리 (lineage summary 영구 보존)
    - rejected 항목도 QOC 요약으로 보존 → 완전 삭제 없음

  integrity:
    - 상태 전이 원칙 1 (자기 검증 금지)이 데이터 무결성 보장
    - conflicts_with 필드가 모순 항목 간 교차 참조 유지
    - Meta Verifier가 전체 정합성 검증
```

### 13.5 Evidence Source 원칙

**도구가 필요한 종류의 주장은, 내부 추론보다 외부 도구 반환값이 우선한다.**

에이전트가 사실적 주장(기존 솔루션 존재, 기술 한계, 성능 수치, 비용 등)을 할 때는
내부 추론만으로 확정하지 않고, 가용한 도구(web_search, code_sandbox, local_rag_db 등)의
반환값을 근거로 삼아야 한다. 도구 없이 한 주장은 evidence_level이 올라갈 수 없다.

구체적 도구 매핑(어떤 에이전트가 어떤 도구를 쓰는가)은 각 에이전트의 지식 문서(로드맵 Phase 2)에서 정의한다. 설계 문서에 도구 이름을 고정하면 도구가 바뀔 때마다 설계 문서를 수정해야 하므로.

```yaml
tool_failure_handling:
  trigger: API timeout, 검색 결과 0건, sandbox 실행 실패, DB 미연결 등

  규칙:
    - 추정으로 대체 금지 (도구가 실패했다고 추론으로 메우지 않는다)
    - reason에 도구 실패 사유를 구체적으로 기록
    - 대응:
        경미한 실패 (결과가 부분적):
          → evidence_level: anecdotal로 강등
          → 해당 주장에 tags: ["tool_partial_failure"] 부착
        완전한 실패 (결과 없음):
          → no_contribution + reason: "도구 실패: {사유}"
          → 또는 도구 없이 가능한 범위만 partial contribution

  Recorder 연동:
    - 어떤 주장에 어떤 도구 반환값이 붙었는지 기록
    - tool-less claim(도구 없이 한 주장)이 있었는지 추적
    - 시스템 평가(Evaluation)에 도구 활용률 메트릭 추가
```

---

## 14. 전체 작동 흐름

```
사용자: "나 이런 거 만들고 싶어"
         │
         ▼
    ┌────────────────────────────────────────────────┐
    │              Orchestrator (4 modules)            │
    │  ┌────────┐ ┌──────────┐ ┌────────┐ ┌────────┐ │
    │  │ Router │ │  State   │ │Deadlock│ │Interact│ │
    │  │(규칙)  │ │ Assessor │ │Resolver│ │ Gate   │ │
    │  │        │ │(경량 LLM)│ │(이벤트)│ │(타이밍)│ │
    │  └────────┘ └──────────┘ └────────┘ └────────┘ │
    └──────┬─────────────────────────────────────────┘
           │
    Phase 1: Understanding
    ├── Context Profiler → 사용자 상황 + hard_constraints + priorities
    ├── Problem Decomposer → 문제 분해
    └── Precedent Researcher → 기존 사례 검색 (RAG 가드레일 적용)
           │
           ├── [Interaction Gate: priorities 확인 — "이 우선순위 맞나요?"]
           │
    Phase 2: Exploration
    ├── Design Space Explorer → 모든 선택지 나열
    ├── Cross-Domain Connector → 타 분야에서 영감
    └── Invention Engine → 모순 돌파 아이디어
           │
           ├── [Interaction Gate: 방향 확인 — "이 2개 중 어느 쪽?"]
           │
    Phase 3: Design
    ├── Structure Advisor → 아키텍처 제안 + changeability_score
    ├── Relationship Architect → 관계 설계
    └── Data Strategist → 데이터 전략
           │
    Phase 4: Challenge ← ⚡ 반드시 거쳐야 함
    ├── Simplicity Advocate → "과하다" 반박
    └── Risk, Cost & Scale Analyst → "이게 깨진다/비싸다" 경고
           │
         ┌─┤ 도전에 의해 수정 필요?
         │ ├── severity: critical → Phase 2 또는 3로 복귀
         │ ├── suggested_fix → 해당 에이전트 수정
         │ └── 3라운드 미해결 → Deadlock Resolver 개입
         │
         No (모든 challenge 처리됨)
           │
    Phase 4.5: Validation
    └── Prototype Validator → 핵심 가정 실제 검증 (코드 실행)
           │
         ┌─┤ fail인 항목?
         │ ├── 1회차 fail → 해당 항목 conflict + Phase 3 복귀
         │ └── 동일 옵션 2회 fail → 강제 rejected + 대안 선택
         │
         No (pass 또는 검증 대상 없음)
           │
           ├── [Meta Verifier: 전체 일관성 검증 (자동 1회)]
           ├── [Interaction Gate: "최종안 확인 — 이 트레이드오프 괜찮나요?"]
           │
    Phase 5: Decision
    └── Decision Evaluator
        ├── 1단계: hard_constraints로 후보 탈락
        │   └── ⚠️ 전부 탈락 시: infeasible → 사용자에게 제약 완화 요청
        └── 2단계: priorities 가중치로 weighted scoring
           │
           ▼
    Output: 최종 아키텍처 + QOC 기록 + ADR + 다이어그램
           │
           ├── [사용자 피드백 수신 시]
           │   └── challenges에 user_feedback 기록 → Phase 4로 점프
           │
    ────────────────────────────────────────────────
    상시: Recorder (매 턴)
    Phase 전환 시: Knowledge Curator
    최종 출력 시: Modeler
    요청 시: Meta Verifier
```

---

## 15. 60+ 개념 커버리지 맵

### 1. 관계/구조 기초 (9개) — 전부 커버됨
| 개념 | 담당 에이전트 |
|------|------------|
| Graph Theory | Relationship Architect |
| Network Science | Relationship Architect |
| Ontology | Relationship Architect + Knowledge Curator |
| Database Theory | Data Strategist |
| Systems Theory | Problem Decomposer + Meta Verifier |
| Category Theory | Cross-Domain Connector |
| Set Theory | Relationship Architect (기초로 내재) |
| Topology | Cross-Domain Connector |
| Information Theory | Data Strategist + Decision Evaluator |

### 2. 설계/의사결정 방법론 (10개) — 전부 커버됨
| 개념 | 담당 에이전트 |
|------|------------|
| DSE | Design Space Explorer |
| ADR | Recorder |
| Trade-off Analysis | Decision Evaluator |
| TRIZ | Invention Engine |
| DDD | Problem Decomposer |
| CSP | Invention Engine + Decision Evaluator |
| MCDM | Decision Evaluator |
| Decision Matrix | Decision Evaluator |
| Morphological Analysis | Design Space Explorer |
| Axiomatic Design | Simplicity Advocate + Decision Evaluator |

### 3. 아키텍처 패턴 (8개) — 전부 커버됨
| 개념 | 담당 에이전트 |
|------|------------|
| Microservices ~ Blackboard 전부 | Structure Advisor |

### 4. AI/에이전트 구조 (10개) — 전부 커버됨
| 개념 | 담당 에이전트 |
|------|------------|
| MAS, Swarm, Orchestrator 등 | Structure Advisor |
| Knowledge Graph, RAG | Knowledge Curator |
| Constitutional AI | Meta Verifier |

### 5. 모델링/시각화 (7개) — 전부 커버됨
| 개념 | 담당 에이전트 |
|------|------------|
| UML ~ Mermaid 전부 | Modeler |
| Wardley Mapping | Design Space Explorer + Context Profiler |

### 6. 상위 학문 (7개) — 전부 커버됨
| 개념 | 담당 에이전트 |
|------|------------|
| Systems Engineering | Meta Verifier |
| Decision Science | Decision Evaluator |
| Cybernetics | Meta Verifier + Risk, Cost & Scale Analyst |
| Complexity Science | Problem Decomposer + Risk, Cost & Scale Analyst |
| Philosophy of Science | Meta Verifier |
| Epistemology | Meta Verifier + Knowledge Curator |
| Semiotics | Knowledge Curator |

### 7. 검증/실행 (v2 추가)
| 개념 | 담당 에이전트 |
|------|------------|
| Spike Solution | Prototype Validator |
| Load Testing | Prototype Validator |
| FMEA | Risk, Cost & Scale Analyst |
| Cost Modeling | Risk, Cost & Scale Analyst |

---

## 16. 구현 로드맵

### Phase 1: Blackboard 스키마 + Orchestrator 규칙 (최우선)
```
먼저 해야 할 것:
  1. Blackboard 스키마를 TypeScript interface 또는 Pydantic 모델로 정의
  2. 상태 전이 4원칙을 constraint engine으로 구현
  3. Router 규칙 15개를 코드로 작성
  4. entry_metadata 구조 확정

왜 최우선인가:
  - 스키마 없이 에이전트를 만들면 에이전트가 각자 다른 형식으로 쓴다
  - Router 규칙이 없으면 Orchestrator가 다시 God Agent가 된다
  - 이 두 개가 시스템의 뼈대
```

### Phase 2: 지식 문서 (1~2주)
```
각 에이전트를 마크다운 지식 문서로 작성
  - 17개 파일 + Orchestrator 4개 모듈 문서
  - 해당 분야의 핵심 원리
  - 판단 기준 (언제 이걸 쓰고, 언제 안 쓰는가)
  - 적용 사례 5~10개
  - 읽기/쓰기 뷰 명시
  - 실패 조건 명시 (언제 no_contribution을 내는가)
```

### Phase 3: 단일 AI + 역할 전환 (즉시)
```
Claude Code에서 세션별 역할 분리
  - 아키텍처 상담 세션: 위 17개 역할을 Phase 순서대로 적용
  - Recorder 세션: QOC/ADR 정리 (별도 문서)
  - Blackboard는 마크다운 파일로 시뮬레이션
  - Router 규칙은 체크리스트로 수동 적용
```

### Phase 4: 실제 멀티 에이전트 (Phase 1~3 검증 후)
```
프레임워크 선택: LangGraph (그래프 기반, Blackboard 구현 적합)
  - Blackboard = 공유 상태 (TypedDict 또는 Pydantic)
  - 각 에이전트 = 노드 (lazy loading)
  - Router = 규칙 기반 라우터
  - State Assessor = 경량 LLM 노드
  - Deadlock Resolver = 조건부 엣지
  - Interaction Gate = interrupt 노드
  - Phase 전환 = 엣지 조건
  - GC = 주기적 cleanup 노드
```

### Phase 5: 학습하는 시스템 (Phase 4 운영 후)
```
  - Recorder의 QOC 데이터로 판단 패턴 분석
  - 에이전트별 정확도 추적
  - 자주 쓰는 조합 → 템플릿화
  - accepted 자동 승격 전환 (QOC 50건 이상 누적 후)
  - 새로운 개념 발견 → Knowledge Curator가 자동 통합
```

---

## 17. v1 대비 변경 이력

### v1 → v2 주요 변경

| 변경 사항 | 이유 | 출처 |
|-----------|------|------|
| Orchestrator를 4개 모듈로 분해 (Router + State Assessor + Deadlock Resolver + Interaction Gate) | God Agent / 단일 병목 방지. Router는 규칙 기반으로 LLM 의존도 최소화 | 전체 AI 피드백 공통 + 자체 판단 |
| Blackboard 13슬롯 스키마 정의 + 풍부한 메타데이터 | 에이전트 간 소통 형식 표준화. 스키마 없으면 채팅방일 뿐 | 전체 AI 피드백 공통 |
| 에이전트별 읽기/쓰기 뷰 | 토큰 40~60% 절감. 불필요한 정보 차단 | Gemini 피드백 |
| 상태 전이 4원칙 (자기검증 금지, peer review, conflict 전제, deadlock 강제) | Blackboard constraint로 God Agent 재발 방지 | GPT 피드백 + 자체 발전 |
| Prototype Validator 추가 (Phase 4.5) | 모든 에이전트가 "생각"만 하고 아무도 "해보지" 않는 문제 해결 | Meta AI 피드백 |
| Cost & Latency Auditor → Risk, Cost & Scale Analyst에 흡수 | 비용도 리스크의 일종. 별도 에이전트는 중복 | 자체 판단 |
| HITL Translator → 출력 레이어로 대체 | 에이전트가 아닌 포맷팅 규칙. 프롬프트 한 줄로 해결 가능 | 자체 판단 |
| Hard constraints와 priorities 분리 | "예산 초과지만 확장성 높아서 1등" 같은 이상한 결과 방지 | GPT 피드백 |
| Mediated query 프로토콜 (direct_query 대신) | Blackboard 철학 유지 + coupling 방지 + Recorder 자동 기록 | Gemini 피드백 + 자체 발전 |
| 사용자 피드백 루프 | 전체 재실행 없이 부분 수정 가능 | 자체 발견 |
| Blackboard GC 규칙 | Blackboard 무한 팽창 방지. Recorder 존재 이유 강화 | 자체 발견 |
| 에이전트 실패 프로토콜 | 억지 출력(hallucination) 방지. "모르겠다"는 유효한 출력 | 자체 발견 |
| Lazy loading 정책 | 동시 활성 2~4개로 토큰 70% 절감 | 자체 판단 |
| Structure Advisor에 changeability_score 필수 출력 | "지금은 되지만 6개월 뒤 못 바꾸는" 구조 방지 | 자체 발견 |
| evidence_level + assumptions + impact_on_decision 메타데이터 | 검증 대상 자동 필터링, Simplicity Advocate의 반박 근거 | GPT + Meta AI 피드백 |
| Always Running 재정의 (상시 1 + 이벤트 3) | 토큰 비용 + 자기참조 루프 방지 | GPT 피드백 + 자체 판단 |
| Recorder 상세 설계 (QOC 변환 규칙 + GC 보존 + ADR 자동 생성) | "상시 빼둔다"만으로는 설계가 아님. 구체적 동작 명세 필요 | 자체 판단 |
| Interaction Gate 판단 로직 (confidence, cost_of_error, score 차이) | 사용자 상호작용 타이밍을 명시적 모듈로 | 자체 발견 |
| review_authority 매트릭스 | 아무 에이전트나 review 방지. v1 운영 후 조정 가능 | GPT 피드백 |
| 영구 conflict → deadlocked → 강제 결정 | 무한 루프 방지. Decision Evaluator가 priorities로 결정 | Gemini 피드백 |
| Phase 4 루프백 규칙 (severity별 분기) | 반박 후 어디로 돌아가는지 명확화 | Meta AI 피드백 |
| validation 슬롯 추가 (13번째) | Prototype Validator 출력 저장소 | Meta AI 피드백 |
| Decision Evaluator 2단계 (hard filter → weighted scoring) | 탈락 조건과 선호도를 분리 | GPT 피드백 |
| Precedent Researcher RAG 가드레일 | hallucination 방지. URL 3개 이상 필수 | Meta AI 피드백 |

### v2 내부 수정 (피드백 반영)

| 변경 사항 | 이유 | 출처 |
|-----------|------|------|
| status enum에 no_contribution 추가 | 실패 프로토콜에서 사용하는데 스키마에 없었음 (문서 내부 불일치) | GPT 피드백 |
| challenge type enum 확장 (deadlock_resolution, consistency_warning, inconsistency) | 실제 사용되는 type이 스키마에 누락 | GPT 피드백 |
| 상태 전이 다이어그램에 v1 수동 승격 명시 | 3.1과 3.3이 충돌하여 구현자 혼란 | GPT 피드백 |
| Decision Evaluator에 infeasible 상태 추가 | hard constraint에서 전부 탈락 시 종료 상태 없었음 | GPT 피드백 |
| 메타데이터에 tags 필드 추가 | overridden_by_priority 등 자유 태그 저장할 곳 없었음 | GPT 피드백 |
| State Assessor가 no_contribution을 충분성으로 인정 | 실패 허용과 Phase 충분성 규칙이 접합 안 됐었음 | GPT 피드백 |
| Modeler 읽기 뷰에 decision 추가 | winner 모르고 모든 옵션 다이어그램 그리는 참사 방지 | Gemini 피드백 |
| Router에 Circuit Breaker 추가 | no_contribution → 슬롯 비었네? → 재호출 무한 루프 방지 | Gemini 피드백 |
| Prototype Validator에 validation 루프 상한 추가 | Phase 3→4→4.5→fail→3 무한 루프 방지. 동일 옵션 2회 fail 시 강제 rejected | Gemini 피드백 |
| Recorder에 Observability 메트릭 수집 추가 | 시스템 레벨 tracing/metrics/logging 없으면 프로덕션에서 디버깅 불가 | Meta AI 피드백 |
| Recorder에 Evaluation 데이터 축적 추가 | 에이전트 성능 추적 없으면 학습 시스템(로드맵 Phase 5)으로 진행 불가 | Meta AI 피드백 |
| Security & Governance 섹션 추가 (13.4) | 기존 구조가 이미 보안 원칙을 갖추고 있음을 명시 | Meta AI 피드백 |

### 에이전트 수 변경

```
v1: 16 에이전트 + 1 Orchestrator (= "17-Agent")
v2: 17 에이전트 + 4-Module Orchestrator

변경 내역:
  - 추가: Prototype Validator (+1)
  - 흡수: Cost & Latency Auditor → Risk, Cost & Scale Analyst (별도 추가 없음)
  - 제거: HITL Translator → 출력 레이어로 대체 (에이전트 아님)
  - 유지: 나머지 16개 전부 유지
  - 합계: 17 에이전트 (13 Phase별 + 4 상시/이벤트)

분리하지 않은 것들과 이유:
  - Relationship Architect + Data Strategist: 관계가 저장소에 끌려가면 안 됨
  - Knowledge Curator + Meta Verifier: 사서와 감사는 이해 상충
  - Recorder를 이벤트 리스너로 축소하지 않음: QOC/ADR 변환은 해석 작업
```

---

## 부록 A: 용어 사전

| 용어 | 정의 |
|------|------|
| Blackboard | 모든 에이전트가 읽고 쓰는 공유 작업 공간 |
| 슬롯 (Slot) | Blackboard 내의 주제별 구획 (13개) |
| 항목 (Entry) | 슬롯 내에 에이전트가 작성한 개별 기록 |
| 메타데이터 | 항목에 부착되는 구조화된 정보 (author, confidence 등) |
| Mediated Query | Blackboard를 통한 간접적 에이전트 간 질문/응답 |
| Phase | 시스템의 작동 단계 (Understanding → Exploration → Design → Challenge → Validation → Decision) |
| Lazy Loading | 필요할 때만 에이전트를 활성화하는 정책 |
| GC | Garbage Collection — Blackboard의 오래된/불필요한 항목 정리 |
| QOC | Questions, Options, Criteria — 의사결정 기록 형식 |
| ADR | Architecture Decision Records — 아키텍처 결정 기록 |
| Lineage Summary | accepted 항목의 이전 version을 압축 보존한 것 |
| Circuit Breaker | no_contribution 무한 루프를 방지하는 Router 규칙 |
| Infeasible | 모든 후보가 hard constraint를 위반하여 선택 불가능한 상태 |
| Observability | 시스템 내부 상태를 외부에서 관측할 수 있게 하는 tracing/metrics/logging |

## 부록 B: 메타데이터 전체 스키마 (복사용)

```yaml
entry_metadata:
  id: string                    # 고유 식별자 (uuid 또는 slot_name.vN)
  author: string                # 작성 에이전트 ID
  timestamp: string             # ISO-8601 형식
  confidence: number            # 0.0 ~ 1.0
  status: string                # draft | reviewed | accepted | rejected
                                # | needs_input | deadlocked | no_contribution
  reason: string | null         # status 설명 (no_contribution 사유, rejected 사유 등)
  version: integer              # 같은 항목의 수정 횟수
  references: [string]          # 근거로 삼은 다른 항목 ID 목록
  conflicts_with: [string]      # 모순되는 항목 ID 목록
  cost_impact: string | null    # Risk, Cost & Scale Analyst 태그
  evidence_level: string        # anecdotal | empirical | theoretical | validated
  assumptions: [string]         # 이 항목이 가정하는 것들
  impact_on_decision: string    # low | medium | high
  success_criteria: string | null  # Prototype Validator가 검증 시 사용할 기준
                                   # 원저자가 항목 작성 시 정의
  needs_response_from: string | null    # mediated query 대상 에이전트 ID
  response_to: string | null            # 응답 대상 질문 항목 ID
  tags: [string]                # 자유 태그 (예: "overridden_by_priority:simplicity",
                                #   "validation_failed_2x", "user_approved")
```
