# Deep Research #2: "내가 모르는 것" 측정 방법

## 질문
시스템의 핵심 가치("내가 모르는 것까지")를 어떻게 측정하는가?

## 찾은 근거

### Unknown Unknowns (UU) 연구
- **[MIT (2024)](https://arxiv.org/abs/2403.17860)** — "Illuminating Blind Spots of Language Models"
  - UU = 모델이 높은 확신으로 틀리는 것. feature space에서 클러스터로 나타남
  - 에이전트를 사용하여 UU 패턴을 식별 → synthetic data로 보완
  - 측정: UU count + accuracy on UU samples

### v2에 적용 가능한 측정 방법

| 방법 | 설명 | 실현 가능성 |
|------|------|-----------|
| **Concept Coverage Delta** | 60+ 개념 체크리스트에서 Single Agent vs Meta Architect가 커버한 개념 수 차이 | ✅ 높음 — 가장 직접적 |
| **Expert Blind Spot Audit** | 전문 아키텍트가 "이걸 빠뜨렸을 것"이라 예상한 항목 vs 실제 커버 여부 | ⚠️ 중간 — 전문가 필요 |
| **Retrospective Analysis** | 설계 후 3개월 뒤 "그때 놓친 것"을 역추적 | ❌ 시간 소요 |
| **Cross-System Comparison** | 같은 입력 → Single/3-Agent/17-Agent 출력에서 고유하게 나온 관점 수 | ✅ 높음 |
| **Contradiction Discovery Rate** | 시스템이 발견한 모순(conflicts_with)의 수와 품질 | ✅ 높음 — Blackboard에서 자동 추적 |

### 핵심 결론
- "내가 모르는 것"의 직접 측정은 불가능 (모르는 걸 모르니까)
- **간접 측정**: coverage delta + 고유 관점 수 + 모순 발견율로 proxy 측정
- **비교 실험이 핵심**: 같은 입력에 대해 시스템 간 출력 차이 분석

### v2 보강 제안
- 평가 축에 "Unique Perspective Count" 추가: 특정 시스템만 제기한 관점 수
- Recorder가 "어떤 에이전트가 다른 에이전트가 안 본 것을 발견했는가" 자동 추적
