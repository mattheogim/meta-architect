# Deep Research #1: Prototype Validator (Phase 4.5) 실현 가능성

## 질문
v2의 Prototype Validator가 "50~100줄 코드로 아키텍처 가정을 실제 검증"하는 것이 가능한가?

## 찾은 근거

### 코드 실행 샌드박스 — 성숙 단계
- **E2B**: Firecracker microVM 기반, Fortune 500 50% 사용, 월 1500만 세션 (2025.3 기준)
  - sub-second cold start, 멀티테넌트 격리
  - URL: https://e2b.dev/
- **llm-sandbox**: 경량 Python 라이브러리, Docker 기반 격리
  - URL: https://github.com/vndee/llm-sandbox
- **Multi-Programming Language Sandbox (2024)**: 다중 언어 실행 환경
  - URL: https://arxiv.org/html/2410.23074v2
- **Promptfoo**: Docker 기반 LLM 코드 평가 도구
  - URL: https://www.promptfoo.dev/docs/guides/sandboxed-code-evals/

### LLM 코드 생성 검증 기법
- **Best-of-N Sampling**: 같은 프롬프트로 N번 샘플링 → verifier로 최적 선택
- **LLMLOOP (ICSME 2025)**: LLM이 코드+테스트를 반복 생성, Docker 샌드박스에서 실행
- **TDD 워크플로우**: 사용자가 테스트 케이스 정의 → LLM이 코드 생성 → 테스트 통과 확인
- **Adversarial Testing**: test manager가 테스트 케이스를 구성, code generator가 반복 개선

### 실현 가능성 판단

| 검증 유형 | 가능성 | 방법 |
|----------|--------|------|
| API 응답 시간 테스트 | ✅ 높음 | HTTP 클라이언트 + 시간 측정 코드 |
| DB 쿼리 성능 테스트 | ⚠️ 중간 | 로컬 DB 셋업 필요. Docker compose로 가능 |
| "1만 TPS" 부하 테스트 | ❌ 낮음 | 실제 인프라 없이 50줄로 불가. 시뮬레이션만 가능 |
| 데이터 모델 정합성 | ✅ 높음 | Pydantic 모델 생성 + validation |
| 알고리즘 복잡도 검증 | ✅ 높음 | 벤치마크 코드 생성 + 실행 |
| 외부 API 호출 비용 | ⚠️ 중간 | 목 서버로 시뮬레이션 가능 |

### 결론
- **샌드박스 인프라는 충분히 성숙** (E2B, Docker, Firecracker)
- **50~100줄로 검증 가능한 범위는 제한적** — 정합성, 알고리즘, API 호출은 가능. 부하 테스트/인프라 수준은 불가
- **v2의 success_criteria가 핵심** — "1만 TPS"는 코드로 검증 불가, "응답 2초 이내"는 가능
- **권장**: success_criteria에 "코드로 검증 가능한 것"과 "수동 확인 필요한 것" 구분 추가

### v2 보강 제안
- Prototype Validator에 "검증 가능성 사전 분류" 단계 추가
- 검증 불가 가정은 Interaction Gate로 사용자에게 전달
- E2B 또는 Docker sandbox를 기본 실행 환경으로 채택
