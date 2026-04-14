# Meta Architect: 17-Agent System Design v1

> "아이디어를 넣으면, 내가 모르는 것까지 포함해서 최적의 구조를 제안해주는 시스템"

---

## 핵심 아키텍처: Blackboard Pattern

선형(순서대로) 구조가 아닌 **Blackboard(공유 칠판)** 구조를 사용한다.

```
┌─────────────────────────────────────────────────────┐
│              BLACKBOARD (공유 작업 공간)                │
│                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │ 문제 정의  │ │ 선택지들   │ │ 제안된 구조 │            │
│  └──────────┘ └──────────┘ └──────────┘            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │ 도전/반박  │ │ 결정 기록  │ │ 시각화     │            │
│  └──────────┘ └──────────┘ └──────────┘            │
│  ┌──────────┐ ┌──────────┐                         │
│  │ 유사 사례  │ │ 지식 참조  │                         │
│  └──────────┘ └──────────┘                         │
└─────────┬──────────┬──────────┬──────────┬──────────┘
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

---

## Orchestrator: The Controller

모든 에이전트 위에 존재하는 **컨트롤러**. 에이전트가 아니라 시스템의 두뇌.

```
역할:
- Blackboard 상태를 관찰
- 지금 어떤 에이전트가 기여해야 하는지 판단
- Phase 전환 결정 (이해 → 탐색 → 설계 → 도전 → 결정)
- 합의 도달 여부 판단
- 교착 상태 감지 및 해결

판단 기준:
- 문제가 충분히 분해됐는가? → 아니면 Problem Decomposer 호출
- 선택지가 충분한가? → 아니면 Design Space Explorer 호출
- 반박이 있었는가? → 아니면 Simplicity Advocate, Risk Analyst 호출
- 합의에 도달했는가? → 맞으면 Decision Evaluator로 최종 결정
```

---

## Phase 1: Understanding (이해) — 3 Agents

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

Blackboard에 쓰는 것:
- 사용자 프로필 (기술 수준, 도구, 환경)
- 제약 조건 목록
- "현실적으로 가능한 범위" 경계

왜 별도 에이전트인가:
- 최적의 아키텍처는 "누가 만드느냐"에 따라 완전히 달라짐
- 다른 에이전트들은 이 정보를 전제로 깔고 작동함
- 이걸 빠뜨리면 "이론적으로 최적이지만 만들 수 없는" 구조가 나옴
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
- 문제 분해 트리
- 각 하위 문제의 성격 태그 (data/relationship/flow/learning/...)
- 복잡도 등급
- 도메인 용어 사전 (Ubiquitous Language)

왜 별도 에이전트인가:
- 문제를 잘못 분해하면 이후 모든 단계가 틀어짐
- DDD의 Bounded Context를 정확히 적용하려면 전문적 분석이 필요
- 구조 설계와 분리해야 문제 정의가 구조에 끌려가지 않음
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
- 유사 프로젝트 목록 + 각각의 접근법
- 검증된 기술 스택 조합
- "이 부분은 이미 있으니 가져다 쓸 것" 목록
- "이 부분은 새로 만들어야 함" 목록

왜 별도 에이전트인가:
- "아는 것에 갇히는" 문제의 직접적 해결
- 다른 에이전트들이 이론 기반이라면, 이건 실증 기반
- 검색과 분석에 집중해야 hallucination이 줄어듬
```

---

## Phase 2: Exploration (탐색) — 3 Agents

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
- 차원별 옵션 매트릭스
- 유효한 조합 목록
- 각 조합의 1줄 특성 설명

왜 별도 에이전트인가:
- "선택지를 넓히는 것"과 "선택하는 것"은 반대 사고방식
- 같은 에이전트가 둘 다 하면 탐색이 좁아짐
- 의도적으로 발산적 사고에 집중해야 함
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
- 구조적 유사성 매핑
- 타 분야 해결책 + 현재 문제에의 적용 방법
- "이런 관점도 있다" 목록

왜 별도 에이전트인가:
- "아는 것에 갇히는" 문제의 가장 강력한 해결책
- 소프트웨어만 아는 사람은 소프트웨어 해법만 생각함
- Category Theory 관점은 다른 에이전트와 완전히 다른 사고 방식
- 이 에이전트가 없으면 시스템이 결국 한 분야에 갇힘
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
- 식별된 기술적 모순
- 적용 가능한 TRIZ 원리 + 구체적 적용 방법
- CSP 해 (있다면)
- 창의적 대안 제안

왜 별도 에이전트인가:
- 다른 에이전트들이 "이건 안 된다"고 했을 때 작동
- 모순 해결은 완전히 다른 사고 프레임이 필요
- TRIZ 40원리를 정확히 적용하려면 전문적 매핑이 필요
```

---

## Phase 3: Design (설계) — 3 Agents

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

Blackboard에 쓰는 것:
- 추천 아키텍처 (1~3개)
- 각 아키텍처의 전제 조건
- 컴포넌트 분해도
- "이 패턴을 쓰면 안 되는 이유" (해당 시)

왜 별도 에이전트인가:
- 아키텍처 패턴이 20개 이상이고 조합까지 하면 수백 가지
- 패턴 선택은 문제 분해, 데이터 설계와 독립적 전문성
- 에이전트 아키텍처까지 포함하면 지식량이 매우 큼
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
- 엔티티 관계 그래프
- 관계 유형 정의서
- 구조적 제약 조건
- 잠재적 문제 (순환, 병목 등)

왜 별도 에이전트인가:
- 관계 설계는 저장(Data)과도, 구조(Structure)와도 다른 관심사
- Graph Theory + Ontology + Network Science를 동시에 적용해야 함
- 이걸 빠뜨리면 "컴포넌트는 좋은데 연결이 엉망" 상황 발생
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
- 데이터 모델 (스키마 또는 스키마리스 설계)
- DB 선택 추천 + 근거
- 데이터 흐름도
- 검색 패턴 + 인덱싱 전략

왜 별도 에이전트인가:
- 잘못된 DB 선택은 나중에 바꾸기 가장 비싼 결정
- 데이터 관심사는 구조 관심사, 관계 관심사와 독립적
- Information Theory 관점(어떤 데이터가 가치 있는가)은 다른 에이전트에 없음
```

---

## Phase 4: Challenge (도전) — 2 Agents

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
- 복잡도 경고
- 단순화된 대안
- "이건 나중에 해도 된다" 목록
- "이 복잡도는 정당화된다 / 안 된다" 판정

왜 별도 에이전트인가:
- 다른 에이전트들은 본능적으로 "더 많이, 더 정확하게" 추구
- 의도적으로 반대 방향을 주장하는 역할이 없으면 시스템이 과설계됨
- 이 에이전트는 adversarial(적대적) 역할 — 다른 에이전트를 견제
- 가장 중요하지만 가장 무시되는 관점
```

### Agent 11: Risk & Scale Analyst
```
핵심 질문: "뭐가 잘못될 수 있고, 커지면 어떻게 되는가?"

지식 기반:
- Failure Mode Analysis (FMEA)
- Cybernetics: 피드백 루프, 안정성
- 확장성 패턴: 수평/수직, 캐싱, 큐
- 보안 기본 원칙

하는 일:
- 제안된 구조의 실패 지점 식별
- "사용자 10명일 때는 되지만 1만 명이면?" 분석
- 단일 장애 지점 (SPOF) 감지
- 보안 취약점 기본 체크
- 기술 부채 누적 경고

Blackboard에 쓰는 것:
- 리스크 매트릭스 (확률 × 영향도)
- 실패 시나리오 목록
- 스케일 병목 지점
- 완화 방안

왜 별도 에이전트인가:
- 리스크 분석은 낙관적인 설계자들이 가장 못 하는 것
- "잘 돌아갈 때"가 아니라 "잘못될 때"를 전문적으로 생각하는 역할 필요
- Simplicity Advocate와 함께 "도전 팀"으로 설계 팀을 견제
```

---

## Phase 5: Decision (결정) — 1 Agent

### Agent 12: Decision Evaluator
```
핵심 질문: "모든 것을 고려했을 때, 어떤 선택이 최적인가?"

지식 기반:
- Multi-Criteria Decision Making (MCDM)
- Trade-off Analysis
- Decision Matrix (Pugh Matrix)
- Decision Science
- Constraint Satisfaction

하는 일:
- Blackboard의 모든 제안, 반박, 대안을 수집
- 평가 기준(Criteria) 명시적으로 정의
- 각 선택지를 기준별로 평가
- Context Profiler의 제약 반영
- 최종 추천 + 근거 + 포기하는 것 명시

Blackboard에 쓰는 것:
- 평가 매트릭스 (선택지 × 기준)
- 최종 추천안
- Trade-off 명시 ("이걸 선택하면 X는 포기")
- 신뢰도 점수

왜 별도 에이전트인가:
- "평가"를 "제안"하는 에이전트가 하면 자기 제안에 편향됨
- 중립적으로 모든 에이전트의 기여를 종합하는 역할 필요
- QOC의 "C(Criteria)"를 가장 엄밀하게 적용하는 지점
```

---

## Always Running (상시 작동) — 4 Agents

### Agent 13: Recorder
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

Blackboard에 쓰는 것:
- QOC 기록
- ADR 문서
- 판단 패턴 분석
- 과거 결정과의 충돌 경고

왜 별도 에이전트인가:
- 기록은 "항상" 일어나야 하며, 다른 작업에 방해되면 안 됨
- 4가지 기록 체계(QOC/ADR/IBIS/DRL)를 상황에 맞게 선택
- 패턴 분석은 장기적으로 메타 아키텍트의 핵심 데이터
```

### Agent 14: Modeler
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
- Blackboard의 설계 내용을 적합한 다이어그램으로 변환
- 추상도에 맞는 시각화 선택 (전체 그림 → C4 Context, 세부 → UML)
- 에이전트 간 상호작용을 시퀀스 다이어그램으로
- 데이터 흐름을 ERD/플로우차트로

Blackboard에 쓰는 것:
- 다이어그램 (Mermaid 코드)
- 시각화 설명
- "이 수준의 추상화에서 빠진 것" 플래그

왜 별도 에이전트인가:
- 시각화는 이해를 돕는 것이지 설계가 아님 — 분리해야 함
- C4의 4단계 줌을 제대로 쓰려면 전문적 판단이 필요
- 적절한 다이어그램 유형 선택이 이해도에 큰 영향
```

### Agent 15: Knowledge Curator
```
핵심 질문: "60개 개념 중 지금 이 문제에 관련 있는 건 뭔가?"

지식 기반:
- 조사 목록의 60+ 개념 전체
- 각 개념의 적용 조건, 한계, 다른 개념과의 관계
- Ontology (개념 간 관계 정의)
- Semiotics (용어와 의미의 정확한 매핑)
- RAG (검색 기반 지식 제공)

하는 일:
- 다른 에이전트가 작업할 때 관련 개념을 자동으로 서핑
- "이 문제에 Information Theory가 관련 있다"를 다른 에이전트에게 알림
- 개념 간 관계 유지 (Graph Theory와 Network Science의 차이점 등)
- 조사 목록의 체크박스 자동 업데이트
- 새로운 개념 발견 시 목록에 추가

Blackboard에 쓰는 것:
- "지금 관련 있는 개념" 목록
- 각 개념의 핵심 원리 요약
- 개념 간 관계 맵
- "이 개념은 아직 조사 안 됨 — 조사 필요" 플래그

왜 별도 에이전트인가:
- 60개 개념을 모든 에이전트가 아는 것은 비효율적
- 전문 사서(librarian)처럼 "지금 이 책이 필요하다"를 알려주는 역할
- 지식의 메타 관리 — 다른 에이전트는 자기 분야만 깊이 알면 됨
```

### Agent 16: Meta Verifier
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
- 에이전트별 신뢰도 추적 (이 에이전트가 과거에 얼마나 정확했나)
- "우리가 모르는 것"을 명시적으로 표시

Blackboard에 쓰는 것:
- 일관성 보고서
- 모순 목록 + 해결 요청
- 신뢰도 점수
- "불확실한 영역" 플래그
- 최종 품질 등급

왜 별도 에이전트인가:
- 자기 자신을 검증하는 것은 불가능 — 독립적 검증자 필요
- 15개 에이전트의 출력을 동시에 보고 교차 검증하는 역할
- 이 에이전트가 없으면 에이전트들이 각자 "맞다"고 하는 것을 걸러낼 수 없음
```

---

## 전체 작동 흐름

```
사용자: "나 이런 거 만들고 싶어"
         │
         ▼
    ┌─────────────┐
    │ Orchestrator │ ← Blackboard 상태 관찰
    └──────┬──────┘
           │
    Phase 1: Understanding
    ├── Context Profiler → 사용자 상황 파악
    ├── Problem Decomposer → 문제 분해
    └── Precedent Researcher → 기존 사례 검색
           │
    Phase 2: Exploration
    ├── Design Space Explorer → 모든 선택지 나열
    ├── Cross-Domain Connector → 타 분야에서 영감
    └── Invention Engine → 모순 돌파 아이디어
           │
    Phase 3: Design
    ├── Structure Advisor → 아키텍처 제안
    ├── Relationship Architect → 관계 설계
    └── Data Strategist → 데이터 전략
           │
    Phase 4: Challenge ← ⚡ 반드시 거쳐야 함
    ├── Simplicity Advocate → "과하다" 반박
    └── Risk & Scale Analyst → "이게 깨진다" 경고
           │
         ┌─┤ 도전에 의해 수정 필요? → Phase 2 또는 3로 복귀
         │ │
         No│
           ▼
    Phase 5: Decision
    └── Decision Evaluator → 최종 선택 + 근거
           │
           ▼
    Output: 최종 아키텍처 + QOC 기록 + 다이어그램

    ────────────────────────────────────
    상시 작동: Recorder, Modeler, Knowledge Curator, Meta Verifier
```

---

## 60+ 개념 커버리지 맵

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
| Cybernetics | Meta Verifier + Risk & Scale Analyst |
| Complexity Science | Problem Decomposer + Risk & Scale Analyst |
| Philosophy of Science | Meta Verifier |
| Epistemology | Meta Verifier + Knowledge Curator |
| Semiotics | Knowledge Curator |

---

## 구현 로드맵

### Phase 1: 지식 문서 (1~2주)
```
각 에이전트를 마크다운 지식 문서로 작성
- 16개 파일, 각 500~2000줄
- 해당 분야의 핵심 원리
- 판단 기준 (언제 이걸 쓰고, 언제 안 쓰는가)
- 적용 사례 5~10개
- 다른 에이전트와의 인터페이스 정의
```

### Phase 2: 단일 AI + 역할 전환 (즉시)
```
Claude Code에서 세션별 역할 분리
- 아키텍처 상담 세션: 위 16개 역할을 순서대로 적용
- 코딩 세션: 결정된 아키텍처 따라 구현
- 기록 세션: QOC 정리
```

### Phase 3: 실제 멀티 에이전트 (Phase 1,2 검증 후)
```
프레임워크 선택: LangGraph (그래프 기반, Blackboard 구현 적합)
- Blackboard = 공유 상태
- 각 에이전트 = 노드
- Orchestrator = 라우터
- Phase 전환 = 엣지 조건
```

### Phase 4: 학습하는 시스템 (Phase 3 운영 후)
```
- Recorder의 QOC 데이터로 판단 패턴 분석
- 에이전트별 정확도 추적
- 자주 쓰는 조합 → 템플릿화
- 새로운 개념 발견 → Knowledge Curator가 자동 통합
```

---

## 이전 버전(12개)에서 추가/변경된 것

| 변경 | 이유 |
|------|------|
| + Context Profiler | 최적 구조는 "누가 만드느냐"에 따라 달라짐 |
| + Precedent Researcher | "이미 존재하는 해결책"을 빠뜨리면 바퀴 재발명 |
| + Cross-Domain Connector | "아는 것에 갇히는" 문제의 핵심 해결책 |
| + Simplicity Advocate | 시스템이 과설계를 막는 유일한 장치 |
| + Risk & Scale Analyst | "잘못될 때"를 전문적으로 생각하는 역할 |
| Orchestrator를 명시적 분리 | 에이전트가 아닌 시스템 컨트롤러로 |
| Blackboard 아키텍처 채택 | 선형 흐름 → 반복적/자유로운 기여 |
| Phase 4(Challenge) 추가 | 도전 없는 설계는 과설계로 가는 지름길 |
