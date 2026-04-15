# Deep Research #4: 수렴(Convergence) 보장

## 질문
17개 에이전트가 합의에 도달하는 게 보장되는가? 몇 라운드면 되는가?

## 찾은 근거

### 경험적 수렴 데이터
- **7 라운드 토론** → 평균 수렴도 0.892 (σ = 0.074) — 안정적
- **A-HMAD**: 최종 라운드에서 산술 92%, GSM8K 85% 만장일치
- 이질적(heterogeneous) 에이전트가 동질적보다 수렴률 약간 높음

### 종료 조건 메커니즘
| 방법 | 설명 | v2 적용 |
|------|------|--------|
| **합의 체크** | 매 라운드 에이전트 답변 비교 → 일치 시 종료 | State Assessor가 할 수 있음 |
| **고정 라운드** | N 라운드 후 강제 종료 | v2의 "3라운드 후 Deadlock Resolver" |
| **Reflection-gain threshold** | 이전 라운드 대비 개선이 임계값 이하면 종료 | 추가 필요 |
| **Dual-loop (CIR3)** | 명시적 종료 조건 + 유한 반복 보장 | v2의 Phase 4 루프백 규칙과 유사 |

### v2의 기존 수렴 메커니즘
- ✅ Deadlock Resolver: version 3+ conflict → 강제 결정
- ✅ Phase 4 루프백: 최대 3라운드 반복
- ✅ Validation 루프 상한: 동일 옵션 2회 fail → 강제 rejected
- ✅ Circuit Breaker: no_contribution → 재호출 방지
- ⚠️ 없는 것: **전체 시스템의 글로벌 종료 조건** (최대 총 라운드 수)

### v2 보강 제안
- **글로벌 라운드 상한** 추가: 전체 시스템이 N 라운드(예: 50) 이내에 종료하도록
- **Reflection-gain threshold**: Phase 간 전환 시 "이전 Phase 대비 개선이 10% 미만이면 충분" 판단
- Recorder가 라운드별 수렴 메트릭 추적
