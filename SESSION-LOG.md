# Session Log

> 각 세션에서 한 일, 결정, 오류, 다음 할 일을 기록한다.
> QOC 형식이 아닌 **변경 로그 + 결정 로그 + 오류 로그** 분리 방식.
> 이유: QOC는 설계 결정용이고, 세션 기록은 작업 추적용이다. 목적이 다르다.

---

## Session 1 — 2026-04-15 (이번 세션)

### 요약
v2 설계서 기반으로 전면 리서치 수행 → 플랜 수립 → 실험 프레임워크 코드화 → hallucination 방지 시스템 구축.

### 변경 로그 (생성/수정된 파일)

| 파일 | 행동 | 내용 |
|------|------|------|
| `CLAUDE.md` | 생성 | 행동 가이드라인 §1-4 + §5 논문 강제 + §6 실험 프로토콜 + §7 태그 규칙 |
| `PRE-REGISTRATION.md` | 생성 | 가설 H1~H4 + 분석 계획 + HARKing 방지 |
| `research/00-research-index.md` | 생성 | 전체 리서치 인덱스 (완료/진행중) |
| `research/papers-catalog.md` | 생성 | 45+ 논문, 11 섹션, MUST-READ 12편 식별 |
| `research/paper-feature-map.json` | 생성 | 11개 기능 × 필수 논문 매핑 |
| `research/check_paper_deps.py` | 생성 | PreToolUse hook: 구현 시 논문 읽기 강제 |
| `research/validate_claims.py` | 생성 | PostToolUse hook: 태그↔출처 정합성 자동 체크 |
| `research/TAGGING-SYSTEM.md` | 생성 | [src:][FACT][VERIFIED] 태그 규칙 |
| `research/deep-{1..8}.md` | 생성 | Deep Research 8건 |
| `research/MASTER-PLAN.md` | 생성→v2 | 최종 실행 계획 (19개 수정 반영) |
| `research/MASTER-PLAN-v1.md` | 보존 | v1 플랜 (수정 전) |
| `research/MASTER-PLAN-REVIEW.md` | 생성 | 플랜 자체 평가 (6.1/10) |
| `research/EXPERIMENT-DESIGN.md` | 생성 | 논문용 실험 설계 (4실험, 252회) |
| `eval/experiment_config.py` | 생성 | 실험 매트릭스 자동 생성 (252회 검증) |
| `eval/experiment_runner.py` | 생성 | 실험 실행 wrapper (유일 진입점) |
| `eval/auto_measure.py` | 생성 | 자동 측정 (coverage, cost, latency 등) |
| `eval/maj_eval.py` | 생성 | LLM-as-Judge (3 persona, Cohen's κ) |
| `eval/paper/generate_tables.py` | 생성 | 논문 Table 1-3 + Figure 1 (logistic fit) |
| `eval/scenarios/*.yaml` | 생성 | 5개 표준 시나리오 |
| `eval/judges/rubric.yaml` | 생성 | 평가 루브릭 (고정) |
| `.claude/settings.local.json` | 수정 | hook 등록 (check_paper_deps + validate_claims) |
| `research/verified/` | 생성 | 빈 디렉토리 (논문 읽기 완료 마킹용) |
| `SESSION-LOG.md` | 생성 | 이 파일 |

### 결정 로그

| ID | 결정 | 이유 | 대안 | 근거 |
|----|------|------|------|------|
| D1 | 17개 에이전트 유지 | Lazy Loading으로 동시 2~4개. 관심사 분리가 핵심 가치 | 3~6개로 축소 | [src:paper-B1][src:v2-전체] |
| D2 | MVP-first (3-agent → 확장) | 전체 구축 후 평가는 실패 리스크 높음 | 바로 17개 구현 | [src:review-C1] |
| D3 | LLM-as-Judge (전문가 대체) | 전문가 3명 섭외 비현실적 | 전문가 blind review | [src:paper-G2][src:review-C3] |
| D4 | 초기 All-Sonnet → 실험 후 모델 결정 | Hegazy vs Li 모순 미해결. 데이터로 결정 | 처음부터 Mixed-Model | [src:paper-A3][src:paper-E3] |
| D5 | Blackboard=데이터, Phase=제어 분리 명시 | "자유 기여" vs "순서 강제" 모순 해결 | 하나를 포기 | [src:review-M4] |
| D6 | RAG는 v2로 defer, v1은 web_search | RAG pipeline은 별도 프로젝트 수준 | 바로 RAG 구축 | [src:review-M5] |
| D7 | Think in NL, Write in Schema | JSON 강제 시 추론 10~15% 하락 | 전부 JSON | [src:paper-I1] |
| D8 | 태그 + Cross-Reference Validator | 태그만으로는 검증 불가. Assertion DB는 과잉 | Assertion DB / 태그만 | 실용성 판단 |
| D9 | QOC 미해결 4개 모두 유지 | 제거 비용 > 유지 비용 | 제거 | [src:qoc-§미해결] |

### 오류 로그

| ID | 오류 | 발생 시점 | 원인 | 해결 |
|----|------|----------|------|------|
| E1 | 초기 리서치가 v2 의도를 안 읽고 "줄이면 되지" 접근 | Tier 0 리서치 | v2의 "왜 별도 에이전트인가" 근거를 안 읽음 | 사용자 지적 → v2 재분석 → 논문 재검색 |
| E2 | 논문 인용 시 실제 검색 없이 기억에 의존 | 첫 번째 논문 리서치 에이전트 | 에이전트에 WebSearch 권한 없었음 | 직접 WebSearch로 전환 |
| E3 | hook 스키마 오류 (settings.json) | hook 등록 | `hooks` 배열 구조를 잘못 씀 (중첩 필요) | 스키마 에러 메시지로 수정 |
| E4 | hook이 사라짐 (settings.local.json 덮어쓰기) | 이후 작업 중 | 사용자/시스템이 permissions만 있는 버전으로 덮어씀 | 재등록 |
| E5 | pydantic 미설치 | experiment_config.py 테스트 | 시스템 Python에 미설치 | pip3 install --break-system-packages |

### 후반부 추가 작업 (Session 1 후반)

| 파일 | 행동 | 내용 |
|------|------|------|
| `QUESTION-PROTOCOL.md` | 생성 | 6개 프로토콜 (세션/리서치/결정/구현/평가/종료) |
| `THINKING-MODES.md` | 생성 | 4 Thinking Modes (BUILD/BREAK/ZOOM/FLIP) 상세 |
| `THINKING-MODES-PORTABLE.md` | 생성 | 복사붙여넣기용 범용 프롬프트 (한계점 포함) |
| `eval/decision_gate.py` | 생성 | BREAK 모드 하드코드 강제 (Pydantic ValidationError) |

### 후반부 결정 로그

| ID | 결정 | 이유 |
|----|------|------|
| D10 | 15개 질문 패턴 → 4 Thinking Modes로 압축 | 개별 패턴 기억 비효율. 모드 전환이 자연스럽게 질문 생성 |
| D11 | BREAK만 하드코드, 나머지는 프롬프트 | BREAK가 가장 무시되기 쉽고 가장 중요 |
| D12 | Layer 2 의미 검증은 지금 안 함 | Phase 3 MAJ-Eval에서 커버됨. 지금 추가는 인프라의 인프라 |
| D13 | 현재 5계층 시스템이 최선 | 구조 강제 60% + 프롬프트 40%. 더 추가해도 수확체감 |

### 후반부 오류 로그

| ID | 오류 | 해결 |
|----|------|------|
| E6 | hook이 다시 사라짐 (settings.local.json) | 재등록. 근본 원인: 다른 edit이 덮어씀 |

### 미해결 사항

| ID | 항목 | 상태 | 다음 행동 |
|----|------|------|----------|
| O1 | research/verified/ 비어있음 (12개 MUST-READ 논문 미읽음) | 대기 | Phase 0.5 시작 전 C1, E1, I1 읽기 |
| O2 | v2 설계서 보강 7+4개 미반영 | 대기 | Phase 0에서 반영 |
| O3 | validate_claims.py INFO 9개 (태그 없는 수치) | 낮음 | Master Plan에 태그 추가 |
| O4 | pyproject.toml 미생성 | 대기 | Phase 0 |
| O5 | src/ 디렉토리 미생성 | 대기 | Phase 0 |
| O6 | settings.local.json hook이 반복적으로 사라짐 | 반복 | 원인 파악 필요 |

---

## Session 2 — 2026-04-15 (논문 검증 세션)

### 요약
papers-catalog.md와 paper-feature-map.json의 논문 인용 정확성을 arXiv 원문 대조로 검증. 6개 핵심 논문 spot-check.

### 변경 로그

| 파일 | 행동 | 내용 |
|------|------|------|
| `research/papers-catalog.md` | 수정 | A1,A2,A3,B1,C1,E2 — 섹션 번호, 학회명, 수치 정밀화, ✅ VERIFIED 태그 추가 |
| `research/paper-feature-map.json` | 수정 | 검증된 섹션 번호로 교체 + `"verified": true` 플래그 추가 |
| `SESSION-LOG.md` | 수정 | Session 2 추가 |

### 검증 결과 (Hallucination Audit)

**검증 방법**: arXiv 원문을 WebFetch로 직접 접근하여 대조

| 논문 | 존재 | 제목 | 저자 | 핵심수치 | 섹션번호 | 학회 |
|------|------|------|------|----------|----------|------|
| A1 Du et al. | ✅ | ✅ | ✅ | ⚠️ 5-10%→7-16pp | ❌ §3→§2 | ✅ ICML 2024 |
| A2 Liang et al. | ✅ | ✅ | ✅ | ✅ | ❌ §3.1/3.2→§1/§2, Algo1 없음 | ❌ ACL→EMNLP |
| A3 Hegazy | ✅ | ✅ | ✅ | ✅ 91%/82% | ⚠️ 테이블→차트 | ✅ |
| B1 Qian et al. | ✅ | ✅ | ✅ | ✅ | ❌ §3/§4→§2/§3.3 | ✅ ICLR 2025 |
| C1 Han & Zhang | ✅ | ✅ | ⚠️ 2인 not et al. | ✅ | ❌ §3/§4→§3(모두)/§4(실험) | ✅ |
| E2 DeepMind+ | ✅ | ✅ | ⚠️ 다기관 | ✅ 1.724 정확 | ❌ §4/§5→§4.3/§5(Limitations) | ✅ |

**핵심 발견**:
- 6개 모두 실존 논문, 제목 정확, 핵심 발견 대체로 정확
- **섹션 번호: 6개 중 5개 틀림** — 전형적 LLM hallucination 패턴
- 학회명 1개 오류 (ACL→EMNLP)
- 존재하지 않는 요소 1개 (Algorithm 1)

### 오류 로그

| ID | 오류 | 원인 | 해결 |
|----|------|------|------|
| E7 | 섹션 번호 5/6 틀림 | LLM이 "§3이 Method겠지" 추측 | arXiv 원문 대조로 수정 |
| E8 | A2 학회명 틀림 (ACL→EMNLP) | 기억 의존 | 원문 확인으로 수정 |
| E9 | A2 Algorithm 1 존재하지 않음 | 기억 의존 | 삭제 |
| E10 | A1 수치 범위 과소표현 (5-10%→7-16pp) | 기억 의존, 대략적 기술 | 정확한 수치로 교체 |

### Session 2.5 — 2026-04-15 (논문 관리 파이프라인 구축)

#### 요약
논문 관리 hardcode 방법을 논문+반증 리서치 후, Level 3 전체 파이프라인 구축.
42개 논문을 YAML로 전환하고 arXiv/S2 API 자동검증 스크립트로 추가 hallucination 9건 발견.

#### 변경 로그

| 파일 | 행동 | 내용 |
|------|------|------|
| `research/papers_schema.py` | 생성 | Pydantic 스키마: PaperEntry(4-state 검증) + PaperCatalog + validate_catalog() |
| `research/papers.yaml` | 생성 | 42개 논문 구조화 YAML (papers-catalog.md 대체) |
| `research/verify_papers.py` | 생성 | arXiv API + Semantic Scholar API 자동검증 + auto-fill |

#### 자동검증으로 발견된 추가 hallucination

| 논문 | 오류 유형 | 내가 적은 것 | 실제 |
|------|----------|-------------|------|
| E2 | 첫 저자 | Samuel Schmidgall | **Yubin Kim** |
| E7 | 첫 저자 | Zhao et al. | **Mingyan Gao** |
| H2 | 제목 | Lost in the Haystack | **Hidden in the Haystack: Smaller Needles...** |
| J2 | 제목 | AutoTRIZ | **AutoTRIZ: Automating Engineering Innovation...** |
| J3 | 제목 | TRIZ Agents | **TRIZ Agents: A Multi-Agent LLM Approach...** |
| J6 | 제목 | LLM + MCDM | **One for All: A General Framework...** |
| K1a | 제목 | SwarmBench | **Benchmarking LLMs' Swarm intelligence** |
| K4 | 제목 | LLM-assisted ADD | **An LLM-assisted approach to designing...** |
| K5 | 제목 | CodeAgents | **CodeAgents: A Token-Efficient Framework...** |

#### 리서치 근거 (논문 관리 방법)

| 출처 | 핵심 발견 | 지지/반증 |
|------|-----------|----------|
| 인용오류 메타분석 (PMC12285159, 2025) | 인간 논문 인용 오류율 16.9%, major 8.0% | 지지 — 인간도 못하니 자동화 필요 |
| GhostCite (arXiv:2602.06718) | LLM 인용 hallucination 14-95% | 지지 — API 검증 필수 |
| SemanticCite (arXiv:2511.16198) | AI 인용 검증 4단계 분류 | 지지 — 자동화 가능 |
| Ioannidis (2016) Milbank Q | 기계적 체계화 → 자체가 waste | 반증 — 과잉 인프라 경고 |
| Cognitive Debt (Storey 2025) | 과도한 자동화 → 깊이 읽기 안 함 | 반증 — 읽기를 대체하면 안 됨 |
| Automation Bias (PubMed 2016) | 복잡한 검증 → 맹목적 신뢰 | 반증 — 단순하게 유지 |

### 미해결 사항

| ID | 항목 | 상태 | 다음 행동 |
|----|------|------|----------|
| O7 | 36개 논문 미검증 (unverified) | 높음 | 구현 시 해당 논문 검증 |
| O8 | E1,E3~E6,F1,G1,G2,H1,I1 섹션 번호 미검증 | 높음 | verify_papers.py는 섹션 내용 검증 불가 — 수동 필요 |
| O9 | E9 arXiv ID 유효하지 않음 | 중간 | 올바른 ID 찾기 |
| O10 | verified/*.md 파일 미생성 (검증 6개 포함) | 낮음 | 구현 시 생성 |
| O11 | Semantic Scholar rate limit (429) | 낮음 | API key 발급 또는 지연 증가 |

---

## 기록 규칙

각 세션 시작 시:
1. 이전 세션의 "다음 할 일"을 확인
2. 이번 세션 로그 섹션 추가 (Session N — 날짜)

각 세션 종료 시:
1. 변경 로그: 생성/수정/삭제한 파일
2. 결정 로그: 내린 결정 + 이유 + 대안 + 근거 [src:]
3. 오류 로그: 발생한 오류 + 원인 + 해결
4. 미해결 사항: 아직 안 끝난 것
5. 다음 할 일: 구체적 단계
