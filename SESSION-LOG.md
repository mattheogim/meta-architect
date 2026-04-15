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

### 미해결 사항

| ID | 항목 | 상태 | 다음 행동 |
|----|------|------|----------|
| O1 | research/verified/ 비어있음 (12개 MUST-READ 논문 미읽음) | 대기 | Phase 0.5 시작 전 C1, E1, I1 읽기 |
| O2 | v2 설계서 보강 7+4개 미반영 | 대기 | Phase 0에서 반영 |
| O3 | validate_claims.py INFO 9개 (태그 없는 수치) | 낮음 | Master Plan에 태그 추가 |
| O4 | pyproject.toml 미생성 | 대기 | Phase 0 |
| O5 | src/ 디렉토리 미생성 | 대기 | Phase 0 |

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
