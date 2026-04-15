# Deep Research #3: LLM-as-Judge — Peer Review가 실제로 작동하는가?

## 질문
v2의 상태 전이 원칙 1-2 (자기검증 금지 + peer review)가 실제로 의미있게 작동하는가?

## 찾은 근거

### LLM-as-Judge 포괄 서베이
- **[Survey on LLM-as-a-Judge (2024)](https://arxiv.org/abs/2411.15594)**: 5가지 관점(기능, 방법론, 적용, 메타평가, 한계) 포괄 분석
- **[LLMs-as-Judges Comprehensive Survey (2024)](https://arxiv.org/html/2412.05579v2)**: LLM 기반 평가 방법 전체 서베이

### 알려진 편향들
| 편향 유형 | 설명 | v2에 대한 영향 |
|----------|------|-------------|
| **Position bias** | 앞/뒤에 있는 것을 선호 | Blackboard 슬롯 순서가 review에 영향 |
| **Verbosity bias** | 긴 응답을 높게 평가 | 많이 쓴 에이전트가 유리 |
| **Sycophancy** | 이전 판단에 동조 | reviewer가 원저자 결론에 동조 |
| **Bandwagon** | 다수 의견에 동조 | 여러 에이전트가 같은 방향이면 반박 어려움 |
| **Concreteness** | 구체적 예시가 있으면 높게 평가 | 추상적이지만 중요한 관점이 묻힐 수 있음 |

### 편향 완화 기법 (SOTA)
1. **구조화된 루브릭**: 명시적 평가 기준표 → 자의적 판단 감소
2. **Pairwise comparison + 순서 교체**: 두 출력을 비교, 순서 바꿔서 2회 실행 → position bias 완화
3. **Multi-agent judge**: 여러 에이전트가 독립 평가 후 토론 → 단일 judge보다 **인간 합의에 더 가까움**
   - MAJ-Eval: Spearman correlation 0.47 (단일 judge 0.15~0.36)
4. **Chain-of-thought reasoning 강제**: judge가 평가 근거를 명시적으로 서술
5. **Cohen's Kappa / Krippendorff's Alpha**: judge 간 일치도 메트릭으로 신뢰도 측정

### v2의 현재 설계와 대조

| v2 메커니즘 | 효과적인가? | 보강 필요 |
|-----------|-----------|---------|
| 자기검증 금지 (원칙 1) | ✅ sycophancy 방지에 효과적 | — |
| Peer review (원칙 2) | ⚠️ position/verbosity bias에 취약 | 구조화된 루브릭 추가 |
| Review Authority 매트릭스 | ✅ 자격 제한은 좋음 | — |
| conflicts_with 필드 | ✅ 모순 명시적 추적 | — |
| evidence_level | ✅ 판단 근거 수준 명시 | — |

### 핵심 발견
> "Multi-agent (debate/committee) evaluators는 단일 모델보다 더 높은 신뢰도와 인간 합의에 가까운 정렬을 달성한다"

→ v2의 peer review 구조는 **원칙적으로 올바르지만**, 구현 시 편향 완화 기법을 반드시 적용해야 함

### v2 보강 제안
1. **Review 시 구조화된 루브릭 사용**: 각 슬롯별 "무엇을 확인해야 하는가" 체크리스트
2. **Reviewer에게 confidence + reasoning 강제**: "왜 이걸 reviewed로 올리는가" 명시
3. **Review 결과 순서 무작위화**: Blackboard에 쓰인 순서가 review에 영향 안 주도록
4. **Meta-evaluation 메트릭 도입**: reviewer 간 일치도 추적 (Recorder가 수집)
