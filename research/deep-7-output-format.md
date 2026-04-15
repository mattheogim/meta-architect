# Deep Research #7: 에이전트 간 출력 형식 표준화

## 질문
에이전트가 Blackboard에 쓸 때 자연어 vs 구조화된 형식(JSON) 중 뭐가 좋은가?

## 찾은 근거

### 핵심 발견: JSON 강제 = 추론 10~15% 하락
- **"Let Me Speak Freely?" 연구**: JSON-mode 강제 시 수학, 기호 추론, 복잡 분석에서 10~15% 성능 저하
- 원인: 구조 준수에 토큰을 쓰느라 추론에 쓸 토큰이 줄어듦
- **Schema-Guided Reasoning (SGR)**: 단계별 추론을 스키마로 강제 → 예측 가능하지만 유연성 감소

### La Malfa (NeurIPS 2025)의 비판과 대조
- "자연어 기반 조정은 모호하고 정보 손실" → JSON이 나음
- 하지만 JSON 강제 = 추론 하락 → 딜레마

### 최적 해법: 하이브리드 (Think in NL, Output in Schema)
1. 에이전트가 자연어로 추론 (chain-of-thought)
2. 최종 output을 Pydantic 스키마에 맞게 변환
3. 변환 실패 시 retry (structured output retry)

이 방식이 현재 SOTA 접근:
- 추론 품질 유지 (자연어 CoT)
- 통신 정확성 확보 (구조화된 출력)
- v2의 entry_metadata가 이미 이 구조를 가정하고 있음

### v2에 대한 함의
- v2의 Blackboard 스키마(2장)는 YAML로 정의되어 있음 → **Pydantic 모델로 전환 시 자연스러운 하이브리드**
- 에이전트의 추론 과정(reasoning trace)은 자연어로 유지
- Blackboard에 쓰는 content + metadata는 구조화

### v2 보강 제안
- 명시적으로 "Think in NL, Write in Schema" 원칙 추가 (13장 공통 프로토콜)
- entry_metadata는 Pydantic strict mode
- content 필드는 string (자연어 허용)
- 구조화가 필요한 필드(scores, lists)는 타입 강제
