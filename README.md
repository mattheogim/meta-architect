# Meta Architect

> 아이디어를 넣으면, 내가 모르는 것까지 포함해서 최적의 구조를 제안해주는 시스템

17개 에이전트 + 4모듈 Orchestrator가 Blackboard Pattern 위에서 협업하여 소프트웨어 아키텍처를 설계하는 멀티 에이전트 시스템.

---

## 파일 구조

```
meta-architect/
├── README.md                          ← 이 파일
├── v1/
│   └── meta-architect-v1.md           ← 원본 설계서 (16 에이전트 + 단일 Orchestrator)
├── v2/
│   ├── meta-architect-v2.md           ← 현재 최종 설계서 (1,852줄)
│   └── meta-architect-v2-qoc.md       ← QOC 의사결정 기록 (참고용)
└── verification/
    ├── verification-report.md         ← 검증 결과 스냅샷
    └── verify.sh                      ← 재실행 가능한 검증 스크립트
```

## v1 → v2 핵심 변경

| 변경 | 요약 |
|------|------|
| Orchestrator | 단일 → 4모듈 (Router + State Assessor + Deadlock Resolver + Interaction Gate) |
| Blackboard | 개념만 → 13슬롯 스키마 + 19필드 메타데이터 |
| 에이전트 수 | 16 → 17 (Prototype Validator 추가) |
| 상태 관리 | 없음 → 상태 전이 4원칙 + GC + Mediated Query |
| 검증 | 이론만 → Prototype Validator (Phase 4.5) 실제 코드 실행 |
| 비용 제어 | 없음 → 에이전트별 읽기 뷰 + Lazy Loading |

## 검증 실행

```bash
cd verification
bash verify.sh
```

45개 항목의 존재 확인 + 6개 핵심 교차 정합성 검증.

## 다음 단계 (구현 로드맵)

1. **Blackboard 스키마 코드화** — Pydantic 모델 또는 TypeScript interface
2. **Router 규칙 코드화** — 15개 규칙을 실제 코드로
3. **에이전트 지식 문서 작성** — 17개 × 500~2000줄
4. **단일 AI 역할 전환으로 테스트** — Claude Code에서 시뮬레이션
5. **LangGraph 멀티 에이전트 구현**
