# Meta Architect — 전체 논문 카탈로그

> 모든 인용 논문의 full citation, 핵심 수치, 알고리즘, 구현 시 강제 읽기 여부를 정리한다.
> ⚠️ 표시 = 수치를 웹 검색으로만 확인 (논문 원문 직접 확인 필요)
> 🔴 MUST-READ = 구현 시 반드시 논문 원문을 읽어야 함

---

## Section A: 멀티에이전트 토론/다양성 (v2 Phase 4 도전 구조의 근거)

### A1. 🔴 MUST-READ — Du et al. (2023)
- **제목**: Improving Factuality and Reasoning in Language Models through Multiagent Debate
- **저자**: Yilun Du, Shuang Li, Antonio Torralba, Joshua B. Tenenbaum, Igor Mordatch
- **출처**: ICML 2024 (arXiv: 2305.14325)
- **URL**: https://arxiv.org/abs/2305.14325
- **핵심 수치**:
  - 3 에이전트 × 2 라운드 토론 → single-agent CoT 대비 **5~10% 절대 정확도 향상** ⚠️
  - 모델: gpt-3.5-turbo-0301
  - 태스크: arithmetic, GSM8K, chess reasoning
- **핵심 방법**: 각 에이전트가 독립적으로 답 생성 → 다른 에이전트의 답을 보고 수정 → 반복
- **구현 시 읽어야 할 부분**: §3 Method (debate protocol), §4 실험 설정
- **v2 관련**: Phase 4 adversarial challenge 구조의 직접적 근거

### A2. 🔴 MUST-READ — Liang et al. (2023)
- **제목**: Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate
- **저자**: Tian Liang, Zhiwei He, Wenxiang Jiao, Xing Wang, Yan Wang, Rui Wang, Yujiu Yang, Zhaopeng Tu, Shuming Shi
- **출처**: ACL 2024 (arXiv: 2305.19118)
- **URL**: https://arxiv.org/abs/2305.19118
- **코드**: https://github.com/Skytliang/Multi-Agents-Debate
- **핵심 발견**:
  - **Degeneration-of-Thought (DoT) 문제** 정의: LLM이 한번 확신하면 reflection으로도 새 사고 불가
  - MAD 프레임워크: agents가 "tit-for-tat" 토론 + judge가 관리
- **핵심 수치**: commonsense MT와 counter-intuitive arithmetic에서 효과 입증 ⚠️ (구체적 수치는 원문 확인 필요)
- **구현 시 읽어야 할 부분**: §3.1 DoT 정의, §3.2 MAD 프레임워크 설계, Algorithm 1
- **v2 관련**: 17개 에이전트 분리의 이론적 근거. 왜 self-critique가 아닌 별도 에이전트가 필요한가.

### A3. 🔴 MUST-READ — Hegazy (2024)
- **제목**: Diversity of Thought Elicits Stronger Reasoning Capabilities in Multi-Agent Debate Frameworks
- **저자**: Mahmood Hegazy
- **출처**: arXiv: 2410.12853 (October 2024)
- **URL**: https://arxiv.org/abs/2410.12853
- **핵심 수치**:
  - 다양 모델 3개 (Gemini-Pro 78% + Mixtral-7Bx8 64% + PaLM2-M 70%) → 4라운드 토론 후 **GSM-8K 91%**
  - 동질 모델 3개 (Gemini-Pro × 3) → **82%** (zero-shot CoT)
  - **다양성 프리미엄: +9%p**
- **핵심 방법**: Du et al.의 debate framework에 heterogeneous models 적용
- **구현 시 읽어야 할 부분**: §4 실험 결과 (모델 조합별 비교 테이블)
- **v2 관련**: Multi-model 배정 전략의 직접적 근거

### A4. Wang et al. (2024)
- **제목**: Mixture-of-Agents Enhances Large Language Model Capabilities
- **저자**: Junlin Wang et al.
- **출처**: arXiv: 2406.04692 (June 2024)
- **URL**: https://arxiv.org/abs/2406.04692
- **코드**: https://github.com/togethercomputer/MoA
- **핵심 수치**:
  - 오픈소스 MoA: AlpacaEval 2.0 **65.1%** (GPT-4o: 57.5%)
  - MT-Bench, FLASK에서도 SOTA
- **핵심 발견**: "Collaborativeness" 현상 — LLM은 다른 모델 출력을 보면 더 나은 응답 생성
- **핵심 방법**: layered architecture, 각 레이어의 에이전트가 이전 레이어 전체 출력을 auxiliary info로 사용
- **v2 관련**: Blackboard 공유 구조의 근거. 에이전트가 다른 에이전트 출력을 읽으면 더 나은 결과.

---

## Section B: 멀티에이전트 스케일링 (에이전트 수 관련)

### B1. 🔴 MUST-READ — Qian et al. (2024)
- **제목**: Scaling Large Language Model-based Multi-Agent Collaboration
- **저자**: Chen Qian, Zihao Xie et al.
- **출처**: ICLR 2025 (arXiv: 2406.07155)
- **URL**: https://arxiv.org/abs/2406.07155
- **핵심 수치**:
  - 1000+ 에이전트까지 테스트
  - 성능 = **로지스틱 성장 패턴** (에이전트 수에 따라) ⚠️ 구체적 수식은 원문 확인 필요
  - 비정규(irregular) 토폴로지 > 정규(regular) 토폴로지
  - small-world 속성 토폴로지가 최적
- **핵심 방법**: MacNet — DAG로 에이전트 조직, topological orchestration
- **구현 시 읽어야 할 부분**: §3 MacNet 설계, §4 Collaborative Scaling Law 수식, Figure 3-4
- **v2 관련**: 17개 에이전트가 과하지 않다는 근거. 토폴로지 설계 참고.

### B2. Li et al. (2024)
- **제목**: More Agents Is All You Need
- **저자**: Junyou Li, Qin Zhang, Yangbin Yu, Qiang Fu, Deheng Ye
- **출처**: arXiv: 2402.05120 (February 2024)
- **URL**: https://arxiv.org/abs/2402.05120
- **핵심 수치**: 에이전트 수 증가 → sampling-and-voting으로 성능 일관 향상 ⚠️ 구체적 수치 원문 확인
- **핵심 발견**: 작은 모델 × 많은 에이전트 > 큰 모델 × 적은 에이전트 (특정 조건)
- **v2 관련**: 에이전트 수 증가의 단순한 이점

---

## Section C: Blackboard 패턴 (v2 핵심 아키텍처 근거)

### C1. 🔴 MUST-READ — Han & Zhang (2025)
- **제목**: Exploring Advanced LLM Multi-Agent Systems Based on Blackboard Architecture
- **저자**: Bochen Han, Songmao Zhang et al.
- **출처**: arXiv: 2507.01701 (July 2025)
- **URL**: https://arxiv.org/abs/2507.01701
- **핵심 수치**: commonsense, reasoning, math에서 SOTA MAS와 경쟁 + **더 적은 토큰** ⚠️ 구체적 수치 원문 확인
- **핵심 방법**: LLM 에이전트(decider, planner, critic, conflict-resolver, cleaner)가 Blackboard 통해 소통
- **구현 시 읽어야 할 부분**: §3 아키텍처 설계, §4 에이전트 역할 정의, §5 실험 결과
- **v2 관련**: Blackboard 패턴의 현대적 LLM 적용 검증. v2 구현 시 반드시 참고.

### C2. Li et al. (2025)
- **제목**: LLM-Based Multi-Agent Blackboard System for Information Discovery in Data Science
- **출처**: arXiv: 2510.01285
- **URL**: https://arxiv.org/abs/2510.01285
- **v2 관련**: 데이터 과학 분야에서의 Blackboard MAS 검증

---

## Section D: 멀티에이전트 시스템 벤치마크 (참고 시스템)

### D1. Hong et al. (2023) — MetaGPT
- **제목**: MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework
- **출처**: ICLR 2024 (arXiv: 2308.00352)
- **URL**: https://arxiv.org/abs/2308.00352
- **핵심 수치**: HumanEval Pass@1 **85.9%**, MBPP Pass@1 **87.7%** (GPT-4)
- **Ablation**: executable feedback 제거 시 HumanEval -4.2%, MBPP -5.4%
- **핵심 방법**: SOP(표준 운영 절차) 기반 에이전트 조정
- **v2 관련**: SOP 개념이 v2의 에이전트 공통 프로토콜(13장)과 유사

### D2. Qian et al. (2023) — ChatDev
- **제목**: ChatDev: Communicative Agents for Software Development
- **출처**: ACL 2024 (arXiv: 2307.07924)
- **URL**: https://arxiv.org/abs/2307.07924
- **핵심 수치**: 평균 토큰 **48,470개**/소프트웨어, 비용 **~$0.30**, 시간 **<7분**
- **v2 관련**: 비용/시간 벤치마크 참고

### D3. Chen et al. (2023) — AgentVerse
- **제목**: AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors
- **출처**: arXiv: 2308.10848
- **URL**: https://arxiv.org/abs/2308.10848
- **핵심 발견**: 멀티에이전트 그룹이 단일 에이전트를 초과 (동적 구성 조정)
- **v2 관련**: 에이전트 그룹의 emergent behavior 연구

---

## Section E: 반박/비판 논문 (v2 위험 요소)

### E1. 🔴 MUST-READ — La Malfa et al. (NeurIPS 2025)
- **제목**: Large Language Models Miss the Multi-Agent Mark
- **출처**: NeurIPS 2025 Position Track (arXiv: 2505.21298)
- **URL**: https://arxiv.org/abs/2505.21298
- **핵심 비판**: 60+ 논문 분석 → 대부분 MAS LLM은 자율성, 사회적 상호작용, 구조화된 환경이 부족. 자연어 조정의 모호성/정보 손실
- **구현 시 읽어야 할 부분**: §3 네 가지 비판 영역, §5 권장 사항
- **v2에 대한 함의**: Blackboard에 구조화된 스키마(Pydantic) 사용으로 자연어 모호성 완화 필요

### E2. 🔴 MUST-READ — Google DeepMind (2025)
- **제목**: Towards a Science of Scaling Agent Systems
- **출처**: arXiv: 2512.08296
- **URL**: https://arxiv.org/html/2512.08296v1
- **핵심 수치**:
  - 조정 비용 = 에이전트 수의 **1.724승**으로 증가
  - 실효 팀 크기: **~3~4개**
  - 싱글 에이전트 정확도 **>45%** 이면 추가 에이전트의 수익 체감/역전
  - tool-heavy 환경(10+ tools): MAS 효율 **2~6배 하락**
- **구현 시 읽어야 할 부분**: §4 Scaling Law 수식, §5 실효 팀 크기 분석
- **v2에 대한 함의**: Lazy Loading(동시 활성 2~4개)이 이 비판을 이미 회피할 수 있음

### E3. Li et al. (2025)
- **제목**: Rethinking Mixture-of-Agents: Is Mixing Different Large Language Models Beneficial?
- **출처**: arXiv: 2502.00674
- **URL**: https://arxiv.org/abs/2502.00674
- **핵심 수치**:
  - Self-MoA(같은 모델) > MoA(다른 모델) AlpacaEval 2.0에서 **+6.6%**
  - MMLU, CRUX, MATH에서 평균 **+3.8%**
- **핵심 발견**: "Quality trumps diversity" — 약한 모델을 섞으면 평균 품질 하락
- **v2에 대한 함의**: Hegazy(A3)과 직접 모순. **같은 역할에는 같은 모델, 다른 역할에는 다른 모델**이 해법일 수 있음

### E4. 🔴 MUST-READ — Basil et al. (2025)
- **제목**: Prompting Science Report 4: Playing Pretend: Expert Personas Don't Improve Factual Accuracy
- **출처**: SSRN: 5879722
- **URL**: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5879722
- **핵심 수치**:
  - 전문가 페르소나 → 추론/사실 정확도 **향상 없음**, 최대 **30%p 하락** 가능
  - R² < 0.10 (성능 분산의 10% 미만 설명)
- **구현 시 읽어야 할 부분**: 전체 (짧은 보고서). 페르소나 vs 구조적 역할 분리의 차이점
- **v2에 대한 함의**: 에이전트 프롬프트가 "너는 Graph Theory 전문가야" 식의 페르소나가 아닌, **구조적으로 다른 입력/출력/판단 기준**을 강제해야 함

### E5. Smit et al. (ICML 2024)
- **제목**: Should we be going MAD? A Look at Multi-Agent Debate Strategies for LLMs
- **출처**: ICML 2024 (arXiv: 2311.17371)
- **URL**: https://arxiv.org/abs/2311.17371
- **핵심 발견**: 기본 MAD가 self-consistency보다 자주 이기지 못함. MAD는 하이퍼파라미터에 매우 민감.
- **v2에 대한 함의**: Phase 4 토론 구조의 하이퍼파라미터(라운드 수, 참여 에이전트 수 등) 튜닝 필요

### E6. 🔴 MUST-READ — Wynn et al. (ICML 2025)
- **제목**: Talk Isn't Always Cheap: Understanding Failure Modes in Multi-Agent Debate
- **출처**: ICML 2025 (arXiv: 2509.05396)
- **URL**: https://arxiv.org/abs/2509.05396
- **핵심 발견**:
  - 토론이 정확도를 **감소**시킬 수 있음 (강한 모델이 다수여도)
  - 모델이 **정답→오답으로 전환** — 동의를 우선시, 반박 회피
  - echo chamber / 다수의 횡포 효과
- **구현 시 읽어야 할 부분**: §4 failure mode taxonomy, §5 mitigation
- **v2에 대한 함의**: Phase 4에 anti-conformity 메커니즘 필요 (no rubber-stamping 규칙)

### E7. Zhao et al. (2025)
- **제목**: Single-agent or Multi-agent Systems? Why Not Both?
- **출처**: arXiv: 2505.18286
- **URL**: https://arxiv.org/abs/2505.18286
- **핵심 수치**:
  - MAS 토큰: SAS 대비 **2~12배** (decoding), **4~220배** (prefill)
  - **~80%** 케이스에서 SAS = MAS (Both Pass 또는 Both Fail)
  - Hybrid routing: 정확도 **+1.1~12%**, 비용 **-88.1%**
- **v2에 대한 함의**: MoE 스타일 complexity-based routing의 근거

### E8. Cemri et al. (2025) — MAST
- **제목**: Why Do Multi-Agent LLM Systems Fail?
- **출처**: arXiv: 2503.13657
- **URL**: https://arxiv.org/abs/2503.13657
- **핵심 수치**: ChatDev 정확도 **최저 25%**. 14개 고유 실패 모드. 3개 범주(시스템 설계, 에이전트 간 불일치, 작업 검증)
- **v2에 대한 함의**: 14개 실패 모드에 대한 v2의 방어 메커니즘 매핑 필요

### E9. Error Cascade (2026)
- **제목**: From Spark to Fire: Modeling and Mitigating Error Cascades in LLM-Based Multi-Agent Collaboration
- **출처**: arXiv: 2603.04474
- **URL**: https://arxiv.org/abs/2603.04474
- **핵심 수치**: 비구조적 MAS에서 에러 **17.2배 증폭** (vs 싱글 에이전트)
- **v2에 대한 함의**: 상태 전이 4원칙 + peer review가 이 증폭을 방지하는지 실증 필요

### E10. AgentArk (2026)
- **제목**: AgentArk: Distilling Multi-Agent Intelligence into a Single LLM Agent
- **출처**: arXiv: 2602.03955
- **URL**: https://arxiv.org/abs/2602.03955
- **핵심 방법**: 멀티에이전트 토론 trajectories → 단일 모델로 distillation (SFT + PRM + GRPO)
- **v2에 대한 함의**: 장기적으로 v2 시스템의 경험을 단일 모델로 압축 가능 (로드맵 Phase 5)

---

## Section F: Sycophancy/편향 (상태 전이 원칙의 근거)

### F1. Sharma et al. (2024)
- **제목**: Towards Understanding Sycophancy in Language Models
- **출처**: ICLR 2024 (arXiv: 2310.13548)
- **URL**: https://arxiv.org/abs/2310.13548
- **핵심 발견**: 5개 프로덕션 AI 어시스턴트에서 sycophancy 확인. preference conditioning 하에서 응답이 사용자 만족도 방향으로 이동
- **v2 관련**: 원칙 1 (자기검증 금지)의 직접적 근거

---

## Section G: LLM-as-Judge (Peer Review 메커니즘)

### G1. Survey on LLM-as-a-Judge (2024)
- **출처**: arXiv: 2411.15594
- **URL**: https://arxiv.org/abs/2411.15594
- **핵심 편향**: position bias, verbosity bias, sycophancy, bandwagon, concreteness bias
- **완화 기법**: 구조화된 루브릭, 순서 교체, multi-agent judge, CoT 강제, Cohen's Kappa

### G2. 🔴 MUST-READ — MAJ-Eval (2025)
- **제목**: Multi-Agent-as-Judge: Aligning LLM-Agent-Based Automated Evaluation
- **출처**: arXiv: 2507.21028
- **URL**: https://arxiv.org/abs/2507.21028
- **핵심 수치**: Spearman ρ **0.47** (vs 기존 baseline 0.15~0.36)
- **핵심 방법**: 자동 persona 추출 → multi-agent in-group debate → aggregator
- **구현 시 읽어야 할 부분**: §3 MAJ-Eval 프레임워크 설계
- **v2 관련**: peer review 구현 시 이 프레임워크 참고

---

## Section H: Long Context (1M context 대안 분석)

### H1. 🔴 MUST-READ — Liu et al. (TACL 2024)
- **제목**: Lost in the Middle: How Language Models Use Long Contexts
- **저자**: Nelson F. Liu, Kevin Lin, John Hewitt et al.
- **출처**: TACL 2024 (arXiv: 2307.03172)
- **URL**: https://arxiv.org/abs/2307.03172
- **핵심 수치**: 중간 위치 정보 → **30%+ 정확도 하락**. 시작/끝은 잘 활용.
- **v2 관련**: 멀티에이전트의 구조적 이점 — 에이전트별 짧은 context = lost in the middle 회피

### H2. Lost in the Haystack (2025)
- **출처**: arXiv: 2505.18148
- **URL**: https://arxiv.org/abs/2505.18148
- **핵심 발견**: 골드 컨텍스트가 짧을수록 성능 급락. 7개 SOTA LLM에서 공통.

---

## Section I: 구조화된 출력 (에이전트 간 통신)

### I1. 🔴 MUST-READ — Tam et al. (2024)
- **제목**: Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance of LLMs
- **출처**: arXiv: 2408.02442
- **URL**: https://arxiv.org/abs/2408.02442
- **핵심 발견**: JSON-mode 등 구조 강제 시 추론 태스크에서 성능 **유의미 하락**. 분류 태스크에서는 향상.
- **완화**: "Think in NL, Output in Schema" 하이브리드
- **v2 관련**: "Think in NL, Write in Schema" 원칙의 근거

---

## Section J: 기반 이론/방법론

### J1. Hofmeister et al. (2007)
- **제목**: A General Model of Software Architecture Design Derived from Five Industrial Approaches
- **출처**: Journal of Systems and Software, Vol. 80
- **URL**: https://www.sciencedirect.com/science/article/abs/pii/S0164121206001634
- **핵심 모델**: Architectural Analysis ↔ Synthesis ↔ Evaluation 순환
- **v2 관련**: Phase 구조의 이론적 근거

### J2. AutoTRIZ (2024)
- **출처**: arXiv: 2403.13002
- **URL**: https://arxiv.org/html/2403.13002v2
- **핵심 방법**: LLM이 모순 식별 → contradiction matrix 자동 매핑 → inventive principles 적용
- **v2 관련**: Invention Engine 에이전트 구현 참고

### J3. TRIZ Agents (2025)
- **출처**: arXiv: 2506.18783
- **URL**: https://arxiv.org/html/2506.18783v1
- **핵심 방법**: 멀티에이전트가 TRIZ 프로세스를 협업 수행
- **v2 관련**: Invention Engine + Blackboard의 조합이 이미 검증됨

### J4. Kluender (2011)
- **제목**: TRIZ for Software Architecture
- **URL**: https://www.sciencedirect.com/science/article/pii/S1877705811001767
- **v2 관련**: TRIZ를 소프트웨어 아키텍처에 적용하는 선행 연구

### J5. AI-driven FMEA (2025)
- **출처**: Cambridge Design Science
- **URL**: https://www.cambridge.org/core/journals/design-science/article/aidriven-fmea-integration-of-large-language-models-for-faster-and-more-accurate-risk-analysis/22F110A2BF0DB4D01A69472CF17A0B43
- **v2 관련**: Risk Analyst 에이전트의 FMEA 적용 근거

### J6. LLM + MCDM (2025)
- **출처**: arXiv: 2502.15778
- **URL**: https://arxiv.org/html/2502.15778v1
- **핵심 수치**: LoRA 파인튜닝 시 MCDM 정확도 **~95%**
- **v2 관련**: Decision Evaluator 에이전트의 근거

### J7. Six Thinking Hats + Design Creativity
- **URL**: https://www.sciencedirect.com/science/article/abs/pii/S1871187121001619
- **핵심 발견**: 강제된 사고 모드 전환이 창의성 유의미 향상
- **v2 관련**: 에이전트별 강제 관점 전환의 인지과학적 근거

### J8. LLM + DDD — Eric Evans (2024)
- **URL**: https://www.infoq.com/news/2024/03/Evans-ddd-experiment-llm/
- **핵심**: DDD 창시자가 LLM+DDD 실험 권장. bounded context 내 ubiquitous language로 LLM 훈련

### J9. Nature Communications (2026) — 유추 추론
- **제목**: Human analogical guidance amplifies LLM performance through cross-domain knowledge activation
- **URL**: https://www.nature.com/articles/s41467-026-70873-7
- **핵심 수치**: 인간 유추 가이드 → LLM 성능 **10배 향상**
- **v2 관련**: Cross-Domain Connector에 유추 프레임을 명시적으로 주입해야 하는 근거

---

## Section K: 기타 참고

### K1. Swarm Intelligence + LLM
- SwarmBench (2025): arxiv 2505.04364 — LLM이 분산 조정에서 심각하게 실패
- MAS Swarm Intelligence (2025): arxiv 2503.03800

### K2. LLM + CSP
- IJCAI 2025: LLM + Constraint Propagation
- CP 2024: In-context learning으로 CSP 모델링

### K3. LLM-Based MAS for SE Survey
- ACM TOSEM (2024): 41개 1차 연구 분석
- URL: https://dl.acm.org/doi/10.1145/3712003

### K4. LLM-assisted ADD
- arXiv: 2506.22688 — LLM으로 Attribute-Driven Design 보조

### K5. CodeAgents (2025)
- arXiv: 2507.03254 — 토큰 효율적 멀티에이전트 > 기존 프롬프팅

### K6. Rethinking Bounds of LLM Reasoning (ACL 2024)
- URL: https://aclanthology.org/2024.acl-long.331/
- 핵심: 멀티에이전트가 싱글에이전트와 "경쟁적" (명확히 우월하지 않음)

---

## ⚠️ 신뢰도 주의사항

### 웹 검색으로만 확인한 수치 (⚠️ 표시)
- 구체적 수치가 논문 요약/블로그에서 가져온 것들이 있음
- 구현 전에 **반드시 원문에서 직접 확인**해야 함

### Hallucination 방지 프로토콜
구현 시 특정 논문을 기반으로 기능을 만들 때:
1. 해당 논문의 PDF를 다운로드
2. Claude Code에서 `Read` 도구로 PDF 직접 읽기
3. 또는 arxiv HTML 버전을 `WebFetch`로 직접 접근
4. 핵심 수치/알고리즘을 원문에서 추출하여 코드 주석에 citation 포함

### 🔴 MUST-READ 목록 (구현 전 필수 읽기)
1. **A1** Du et al. — debate protocol 설계
2. **A2** Liang et al. — DoT 문제 정의 + MAD 알고리즘
3. **A3** Hegazy — 다양성 프리미엄 수치
4. **B1** Qian et al. — collaborative scaling law 수식
5. **C1** Han & Zhang — Blackboard + LLM 구현 세부
6. **E1** La Malfa — 4가지 비판 영역 + 대응
7. **E2** DeepMind — scaling law 수식 + 실효 팀 크기
8. **E4** Basil — 페르소나 vs 구조적 역할의 차이
9. **E6** Wynn — debate failure mode taxonomy
10. **G2** MAJ-Eval — peer review 프레임워크
11. **H1** Liu — lost in the middle 패턴
12. **I1** Tam — structured output 추론 패널티
