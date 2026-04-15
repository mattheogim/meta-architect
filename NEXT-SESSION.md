# 다음 세션 할 일

> 이 파일을 세션 시작 시 가장 먼저 읽는다.
> 완료하면 체크 표시하고 SESSION-LOG.md에 기록.

---

## 컨텍스트 로딩 순서 (새 세션 시작 시)

```
1. 이 파일 (NEXT-SESSION.md) 읽기
2. CLAUDE.md 읽기 (행동 규칙 확인)
3. SESSION-LOG.md 이전 세션 확인
4. research/MASTER-PLAN.md §5 Phase 0 확인
```

---

## Phase 0: 프로젝트 셋업 + v2 보강 (예상 2~3시간)

### Step 0-1: pyproject.toml + 프로젝트 구조
```
[ ] pyproject.toml 생성
    dependencies:
      - langgraph >= 0.2
      - pydantic >= 2.0
      - litellm
      - pyyaml
      - pytest
    optional:
      - e2b
      - scipy (logistic fitting)
      - matplotlib (논문 그래프)

[ ] src/ 디렉토리 구조 생성 (빈 __init__.py)
    src/
    ├── __init__.py
    ├── blackboard/
    │   └── __init__.py
    ├── orchestrator/
    │   └── __init__.py
    ├── agents/
    │   ├── __init__.py
    │   └── prompts/
    ├── llm/
    │   └── __init__.py
    ├── sandbox/
    │   └── __init__.py
    └── recorder/
        └── __init__.py

[ ] tests/ 디렉토리 구조 생성 (빈 test 파일)
    tests/
    ├── __init__.py
    ├── test_state_transition.py
    ├── test_router.py
    └── test_gc.py

[ ] .env.example 생성
    ANTHROPIC_API_KEY=sk-ant-...
    OPENAI_API_KEY=sk-...

[ ] .gitignore 업데이트
    .env
    __pycache__/
    eval/experiments/*/runs/
    *.pyc
```

**검증**: `python -c "import pydantic; print('OK')"` + `pytest --collect-only`

---

### Step 0-2: v2 설계서 보강 (7+4+1개 항목)

v2/meta-architect-v2.md에 직접 추가:

```
[ ] 1장: "Blackboard = 데이터 공유 계층, Phase = 제어 흐름 계층" 명시 추가
[ ] 3.2.1: Review 루브릭 섹션 추가 (13슬롯 각각의 체크리스트)
[ ] 3.3: Phase 0.5 MVP는 수동 승격 정책 명시
[ ] 3.7: 수렴 규칙 섹션 추가 (Phase당 10, 동적 종료, 200 calls 안전망)
[ ] 5장 Agent 3: Precedent Researcher를 web_search 기반으로 수정 (RAG defer)
[ ] 8장: No Rubber-Stamping Rule 추가 (대안 1개 필수)
[ ] 9장: success_criteria 검증 가능성 분류 (code/simulation/manual)
[ ] 12장: Phase 전환 reasoning 요약 (200 토큰) 추가
[ ] 13.6: Think in NL, Write in Schema 원칙 추가
[ ] QOC 미해결 4개: "유지" 결정 기록 (Observability, Evaluation, Security, Evidence Source)
[ ] 16장: 구현 로드맵을 Master Plan Phase 0→0.5→1→2→3→4로 업데이트
```

**검증**: `bash verification/verify.sh` (기존 45개 항목 통과 + 새 항목)

---

### Step 0-3: validate_claims.py INFO 9개 해결

```
[ ] MASTER-PLAN.md의 태그 없는 수치에 [src:] 태그 추가
[ ] python research/validate_claims.py → INFO 0개 확인
```

---

### Step 0-4: git commit

```
[ ] git add -A
[ ] git commit -m "Phase 0: project setup + v2 reinforcement + experiment framework"
```

---

## Phase 0 완료 후 → Phase 0.5 시작 준비

### Step 0.5-prep: MUST-READ 논문 3편 읽기

```
[ ] C1: Han & Zhang (arXiv:2507.01701)
    - WebFetch로 arxiv HTML 접근
    - §3 아키텍처, §4 에이전트 역할 핵심 추출
    - research/verified/C1.md 작성

[ ] E1: La Malfa (arXiv:2505.21298)
    - §3 네 가지 비판 핵심 추출
    - research/verified/E1.md 작성

[ ] I1: Tam (arXiv:2408.02442)
    - §3 실험, §4 완화 핵심 추출
    - research/verified/I1.md 작성
```

**검증**: `python research/validate_claims.py` → WARN에서 C1, I1 사라짐

---

## Phase 0.5 (다다음 세션): 3-Agent MVP

```
[ ] src/blackboard/schema.py — 13슬롯 Pydantic (핵심 4개 활성, 9개 예약)
[ ] src/blackboard/entry.py — 19필드 메타데이터
[ ] src/blackboard/state.py — 상태 전이 4원칙 validator
[ ] src/blackboard/views.py — 3개 에이전트 읽기/쓰기 뷰
[ ] src/agents/base_agent.py — Think NL, Write Schema 공통
[ ] src/agents/architect_agent.py — Phase 1~3 통합
[ ] src/agents/critic_agent.py — Phase 4 adversarial
[ ] src/agents/synthesizer_agent.py — Phase 5 결정
[ ] src/agents/prompts/{architect,critic,synthesizer}.md — 각 300~500줄
[ ] src/llm/provider.py — LiteLLM 통합 (All-Sonnet)
[ ] src/orchestrator/graph.py — LangGraph 조립 (선형 + 1 루프)
[ ] src/recorder/logger.py — 기본 이벤트 로깅
[ ] eval/experiment_runner.py _execute_system() 연결
[ ] 시나리오 2 (채팅 앱)로 첫 end-to-end 실행
[ ] EXP-SCALE "1-agent" + "3-agent" 각 15회 = 30회 데이터 수집
[ ] 중간 검증: 3-agent > 1-agent? → 방향 결정
```

---

## 주의사항

1. **논문 안 읽고 구현 시작하지 말 것** — check_paper_deps.py hook이 경고함
2. **실험은 반드시 ExperimentRunner를 통해** — 직접 호출 RuntimeError
3. **수치를 쓸 때 [src:] 태그 필수** — validate_claims.py가 체크함
4. **결정을 내릴 때 SESSION-LOG.md에 기록** — 결정 이유 + 대안 + 근거
5. **PRE-REGISTRATION.md 수정 금지** — 가설 확정 후 변경 = HARKing
