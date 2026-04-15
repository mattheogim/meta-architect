# Deep Research #8: Multi-Model 오케스트레이션

## 질문
에이전트별로 다른 LLM(Claude, GPT, Gemini)을 쓰려면 어떻게 해야 하는가?

## 찾은 근거

### 현재 상태 (2025-2026)
- **LiteLLM**: 통합 프록시. OpenAI format으로 모든 provider 호출. 코드 변경 없이 provider 교체
  - URL: https://github.com/BerriAI/litellm
- **Bifrost**: 오픈소스 AI gateway. 20+ provider 지원. 요청당 11μs 오버헤드
- **Vellum**: 같은 프롬프트로 GPT/Claude/Gemini 비교 평가 내장
- 기업 60%가 multi-LLM 접근으로 운영 비용 60% 절감 보고

### 실전 패턴
```
일반 패턴:
- GPT-5 → 복잡한 추론
- Claude Opus → 상세 분석  
- Gemini → 멀티모달/속도
- 오픈소스 → 비용 민감 태스크
```

### v2에 적용 시 아키텍처

```
Meta Architect
  └── LiteLLM Proxy (통합 API 계층)
       ├── Claude Opus → Phase 1-3 에이전트 (깊은 추론)
       ├── GPT-4o → Phase 4 도전 에이전트 (다른 편향)
       ├── Claude Sonnet → Prototype Validator, Modeler
       ├── Haiku/GPT-4o-mini → State Assessor, Recorder
       └── Gemini → Knowledge Curator (검색 강점)
```

### Li et al. (2025) 반박과의 조화
- "Self-MoA > Mixed-MoA" — 하지만 이건 **같은 역할**에서의 비교
- v2는 **다른 역할**에 다른 모델 → 직접 비교 안 됨
- 핵심: **같은 에이전트의 여러 인스턴스**는 같은 모델이 나음, **다른 에이전트**에는 다른 모델이 다양성 증가

### 실현 가능성
- ✅ LiteLLM으로 **즉시 구현 가능**
- ⚠️ 프롬프트를 모델별 특성에 맞게 조정 필요 (Claude는 XML 태그, GPT는 system message 등)
- ⚠️ 모델 업데이트 시 행동 변화 → 프롬프트 regression test 필요
- ✅ LangGraph와 LiteLLM 통합은 표준적

### v2 보강 제안
- LiteLLM을 기본 LLM 계층으로 채택
- 에이전트별 model_id를 설정 가능하게 (기본값 + override)
- 모델 변경 시 영향 테스트를 Recorder가 자동 추적
