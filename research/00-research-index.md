# Meta Architect Research Index

> 모든 리서치 결과를 여기서 추적한다.

## 완료된 리서치

### Tier 0: 전제 의심
| # | 주제 | 결론 | 파일 |
|---|------|------|------|
| 0-1 | 멀티에이전트 필요한가? | 17개 과잉 주장 vs Qian(2024) 로지스틱 성장 반론 | [01-multi-vs-single.md](01-multi-vs-single.md) |
| 0-2 | Blackboard 최선인가? | Hybrid(Blackboard+DAG) 추천. Han&Zhang(2025) 검증 | [02-blackboard-alternatives.md](02-blackboard-alternatives.md) |
| 0-3/4 | 에이전트 수 + Phase 구조 | 실효 3~7개 vs v2의 Lazy Loading(동시 2~4개) | [03-agent-count-phase.md](03-agent-count-phase.md) |
| 0-5 | 비용 현실성 | $0.24(3-agent) ~ $10.65(17-agent all-Opus) | [04-cost-estimation.md](04-cost-estimation.md) |
| 1-1 | 유사 시스템 | 경쟁자 없음. 빈 공간 | [05-competitive-landscape.md](05-competitive-landscape.md) |

### 지지 논문
| 논문 | 핵심 발견 | v2 관련 |
|------|----------|---------|
| Du et al. (ICML 2024) | 멀티에이전트 토론 → 사실성+추론 향상 | Phase 4 도전 구조 지지 |
| Liang et al. (2023) | DoT 문제: 한번 확신하면 자기수정 불가 | 별도 에이전트 분리 이유 |
| Hegazy (2024) | 다양 모델 91% > 동질 모델 82% | Multi-model 배정 근거 |
| Wang et al. (2024) | Collaborativeness: 다른 출력 보면 더 잘함 | Blackboard 공유의 근거 |
| Qian et al. (ICLR 2025) | 에이전트 수 로지스틱 성장, 1000+까지 | 17개 타당성 근거 |
| Han & Zhang (2025) | LLM Blackboard MAS = SOTA + 토큰 절감 | Blackboard 패턴 검증 |

### 반박 논문
| 논문 | 핵심 발견 | v2 위험 |
|------|----------|---------|
| La Malfa (NeurIPS 2025) | MAS LLM은 진짜 멀티에이전트 특성 부족 | 자연어 조정 모호성 |
| Google DeepMind (2025) | 조정비용 1.724승, 실효 3~4개 | 17개의 오버헤드 |
| Li et al. (2025) | Self-MoA > Mixed-MoA (품질>다양성) | Multi-model 전략 재검토 |
| Basil et al. (2025) | 페르소나 프롬프팅 → 추론 개선 안함, 30% 하락 가능 | 에이전트 프롬프트 설계 주의 |
| Smit (ICML 2024) | echo chamber, 판정자가 수사에 속음 | Phase 4 도전 실효성 |
| MAST (2025) | ChatDev 25% 정확도, 에러 17.2배 증폭 | 에러 전파 방어 필수 |
| Zhao et al. (2025) | 80% SAS=MAS 무승부, 토큰 2~12배 | 비용 정당화 필요 |

### 60+ 개념 적용 가능성
| 개념 | 실현 가능성 | 근거 |
|------|-----------|------|
| TRIZ | 높음 | AutoTRIZ(2024), TRIZ Agents(2025) |
| DDD | 높음 | Eric Evans(2024) LLM+DDD 권장 |
| Morphological Analysis | 높음 | DRS Conference(2024) |
| MCDM | 높음 | LoRA 파인튜닝 시 95% |
| FMEA | 높음 | Cambridge Design Science(2025) |
| Graph/Ontology | 높음 | KG 구축 성숙 단계 |
| Category Theory/유추 | 중간 | far analogy zero-shot 약함 |
| CSP | 중간 | 이해 가능, solver 도구 필요 |
| Wardley Mapping | 낮음~중간 | 자동화 연구 부족 |
| Axiomatic Design | 낮음 | 직접 연구 없음 |
| Cynefin | 중간 | 분류 가능, 정확도 미검증 |
| Information Theory | 낮음 | 정량 계산 불가, 정성만 |

### 하드코드 가능 범위
- 완전 하드코드: Router, 상태전이, Review Authority, GC, 읽기/쓰기 뷰
- 부분 하드코드: Recorder, Meta Verifier, Knowledge Curator, Deadlock Resolver
- LLM 필수: 13개 Phase 에이전트, State Assessor

---

## 진행 중 리서치

### Deep Research: Critical Gaps (1~8번)
| # | 주제 | 상태 | 파일 |
|---|------|------|------|
| 1 | Prototype Validator 실현 가능성 | ✅ 완료 | [deep-1-prototype-validator.md](deep-1-prototype-validator.md) |
| 2 | "내가 모르는 것" 측정 방법 | ✅ 완료 | [deep-2-measuring-blind-spots.md](deep-2-measuring-blind-spots.md) |
| 3 | LLM-as-Judge: Peer Review 작동성 | ✅ 완료 | [deep-3-llm-as-judge.md](deep-3-llm-as-judge.md) |
| 4 | 수렴(Convergence) 보장 | ✅ 완료 | [deep-4-convergence.md](deep-4-convergence.md) |
| 5 | 1M Context vs Multi-Agent | ✅ 완료 | [deep-5-long-context-vs-multiagent.md](deep-5-long-context-vs-multiagent.md) |
| 6 | Precedent Researcher RAG | ✅ 완료 | [deep-6-precedent-rag.md](deep-6-precedent-rag.md) |
| 7 | 에이전트 간 출력 형식 표준화 | ✅ 완료 | [deep-7-output-format.md](deep-7-output-format.md) |
| 8 | Multi-Model 오케스트레이션 | ✅ 완료 | [deep-8-multi-model.md](deep-8-multi-model.md) |
