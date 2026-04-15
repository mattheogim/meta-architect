# Deep Research #5: 1M Context Window vs Multi-Agent

## 질문
Opus 4.6이 1M context인데, 17개 에이전트의 시스템 프롬프트 + 지식을 전부 한 context에 넣으면 되지 않는가?

## 찾은 근거

### Lost in the Middle 문제
- **[Liu et al. (TACL 2024)](https://arxiv.org/abs/2307.03172)** — "Lost in the Middle"
  - 긴 context의 **중간에 있는 정보는 30%+ 정확도 하락**
  - 시작과 끝에 있는 정보는 잘 활용, 중간은 거의 무시
  - 명시적 long-context 모델에서도 동일 패턴
- **[Lost in the Haystack (2025)](https://arxiv.org/abs/2505.18148)** 
  - 골드 컨텍스트가 짧을수록(= needle이 작을수록) 성능 급락
  - 7개 SOTA LLM에서 공통 패턴

### 1M Context의 실전 활용
- Agentic 워크플로우에서 1M context = 전체 작업 이력 유지 가능
- 하지만 "수백 번의 tool call" 이력을 유지하는 것 vs "17개 전문 관점을 동시 유지"는 다른 문제
- context가 길수록 비용 선형 증가 (input token 과금)

### Multi-Agent의 구조적 이점 (context와 무관)
1. **강제된 관점 전환**: 한 context 안에서 "이제 Simplicity Advocate로 생각해"는 DoT(Degeneration-of-Thought)에 취약
2. **격리된 추론**: 에이전트별 context가 분리되어 있어 한 관점이 다른 관점을 오염시키지 않음
3. **읽기 뷰**: 에이전트가 필요한 정보만 보므로 "lost in the middle" 자체가 발생하지 않음
4. **병렬 실행**: 같은 Phase 내 독립 에이전트는 동시 실행 가능

### 비교 분석

| 측면 | 1M Single Context | Multi-Agent (v2) |
|------|-------------------|-----------------|
| **Lost in the middle** | ❌ 17개 지식 중 중간것 무시 | ✅ 각 에이전트가 자기 지식만 |
| **DoT 방지** | ❌ 같은 context에서 관점 전환은 표면적 | ✅ 물리적으로 분리된 에이전트 |
| **비용** | ✅ 1회 호출 (하지만 1M input = 비쌈) | ⚠️ 여러 호출 (하지만 각각 작음) |
| **맥락 일관성** | ✅ 한 mind가 전체 보유 | ⚠️ Blackboard로 간접 공유 |
| **구현 복잡도** | ✅ 단순 | ❌ 복잡 |
| **인지 다양성** | ❌ 같은 model, 같은 context = 같은 편향 | ✅ 다른 프롬프트 + 다른 model 가능 |
| **관점 간 오염** | ❌ "구조 좋아" 생각이 "단순성" 판단을 오염 | ✅ 격리됨 |

### "Mega-Prompt" 실험이 필요
- **[A Decomposition Perspective (2024)](https://arxiv.org/html/2604.07981v1)**: 긴 context 추론을 atomic skill로 분해하는 AbR 프레임워크 제안 → 분해가 단일 context보다 나음
- **[CodeAgents (2025)](https://arxiv.org/html/2507.03254v1)**: 토큰 효율적인 멀티에이전트가 기존 프롬프팅 전략보다 우수
- **[Rethinking the Bounds (ACL 2024)](https://aclanthology.org/2024.acl-long.331/)**: 멀티에이전트가 싱글에이전트와 "경쟁적" — 즉 명확히 우월하지도 않음

### 핵심 결론
> 1M context는 "같은 관점에서 더 많은 정보를 보는 것"에 유리하고,
> Multi-agent는 "다른 관점에서 같은 문제를 보는 것"에 유리하다.
> v2의 목표가 "내가 모르는 것까지"라면, 다른 관점이 핵심 → Multi-agent가 적합.

하지만:
> **평가 Phase A에서 반드시 비교해야 함**: 
> Baseline C로 "1M mega-prompt"를 추가하여 실증 비교

### v2 보강 제안
1. 평가 Baseline에 "1M single context + 구조화된 체크리스트" 추가
2. 에이전트별 context를 최대한 짧게 유지 (읽기 뷰 최적화) → lost in the middle 방지의 구조적 이점 극대화
3. v2의 "관점 격리"가 핵심 차별화임을 명시적으로 문서화
