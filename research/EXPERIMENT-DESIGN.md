# Meta Architect — 논문용 실험 설계 + 데이터 수집 강제

> 이 프로젝트를 학술 논문으로 발표할 수 있도록 실험을 설계한다.
> 모든 실행 데이터를 자동으로 수집하여 논문 테이블/그래프를 바로 생성 가능하게 한다.

---

## 1. 논문 프레임워크

### 가설 (Pre-registered)

```
H1 (주 가설): 강제된 인지 다양성(forced cognitive diversity)을 가진 멀티에이전트 시스템이 
  단일 에이전트보다 소프트웨어 아키텍처 설계에서 더 많은 관점을 커버하고, 
  더 높은 품질의 결과를 산출한다.

H2 (부 가설): 에이전트 수를 점진적으로 증가시킬 때, 
  아키텍처 설계 품질은 로지스틱 성장 패턴을 보인다.

H3 (부 가설): 적대적 도전(adversarial challenge) Phase가 있는 시스템이 
  없는 시스템보다 더 실현 가능한 아키텍처를 산출한다.

H4 (부 가설): 서로 다른 LLM 모델을 사용하는 에이전트 조합이 
  동일 모델 조합보다 더 다양한 관점을 산출한다.
```

### 타겟 학회

| 학회 | 트랙 | 적합도 | 마감 |
|------|------|--------|------|
| **ICSE** | Technical Track / NIER | 높음 | 매년 9~10월 |
| **ESEM** | Registered Reports | 높음 — pre-registration 지원 | 매년 4~5월 |
| **ASE** | Research Track | 높음 | 매년 5~6월 |
| **ICSME** | Registered Reports | 중 | 매년 4~5월 |
| **MSR** | Registered Reports | 중 | 매년 2월 |
| **NeurIPS** | Datasets & Benchmarks | 낮 (SE 도메인) | 매년 5월 |
| **ICML** | Position Papers | 중 | 매년 1월 |

### 논문 구조 (ICSE 형식)

```
Title: "Meta Architect: Forced Cognitive Diversity in Multi-Agent LLM Systems 
        for Software Architecture Design"

Abstract
1. Introduction
   - 문제: LLM이 아키텍처 설계할 때 blind spot
   - 가설: 강제된 인지 다양성이 이를 해결
   - 기여: (1) 17-agent 시스템 설계, (2) Blackboard 패턴 LLM 적용, 
           (3) 점진적 에이전트 추가 실험, (4) 평가 프레임워크
2. Background & Related Work
3. System Design (v2 설계서 요약)
4. Experimental Design (이 문서)
5. Results
6. Discussion (위협 요인, 한계, 도메인 불일치 인정)
7. Conclusion
```

---

## 2. 실험 설계

### 독립 변수 (Independent Variables — 우리가 조작하는 것)

| 변수 | 값 | 실험 이름 |
|------|-----|----------|
| **에이전트 수** | 1, 3, 6, 10, 17 | EXP-SCALE |
| **에이전트 구성** | {어떤 에이전트가 포함?} | EXP-ABLATION |
| **모델 다양성** | All-Opus, Mixed, All-Sonnet | EXP-MODEL |
| **Phase 4 유무** | with Challenge / without Challenge | EXP-CHALLENGE |
| **Blackboard 유무** | shared state / direct pass | EXP-BLACKBOARD |

### 종속 변수 (Dependent Variables — 우리가 측정하는 것)

| 지표 | 측정 방법 | 단위 |
|------|----------|------|
| **Concept Coverage** | 60+ 개념 체크리스트 자동 매칭 | 개수 (0~60+) |
| **Unique Perspectives** | 해당 구성에서만 나온 관점 수 | 개수 |
| **Quality Score** | LLM-as-Judge (MAJ-Eval 프레임워크) | 1.0~5.0 |
| **Feasibility Score** | 제약 조건 충족 비율 | 0.0~1.0 |
| **Challenge Rate** | actionable challenge / total challenge | 비율 |
| **Conflict Count** | conflicts_with 발생 수 | 개수 |
| **Decision Trace** | QOC chain 완전성 | 비율 |
| **Cost** | 총 토큰 (input + output) | 토큰 수 |
| **Latency** | 시작~종료 시간 | 초 |
| **Rounds** | 총 에이전트 호출 수 | 횟수 |

### 통제 변수 (Controls — 고정하는 것)

```yaml
controls:
  scenarios: 5개 고정 시나리오 (동일 입력)
  temperature: 0.7 (모든 에이전트 동일)
  max_tokens_per_agent: 4096
  random_seed: 42 (재현성)
  evaluation_rubric: 고정 (CLAUDE.md에 정의)
  judge_model: Claude Opus (평가용 별도 인스턴스)
  runs_per_condition: 3 (통계적 안정성)
```

### 실험 매트릭스

#### EXP-SCALE: 에이전트 수 → 품질 곡선
```
조건: 1-agent, 3-agent, 6-agent, 10-agent, 17-agent
시나리오: 5개 × 3회 반복 = 75회 실행
측정: 모든 종속 변수
목적: H2 검증 (로지스틱 성장 패턴?)
```

구성:
| 조건 | 포함 에이전트 |
|------|-------------|
| 1-agent | Single Opus (mega-prompt) |
| 3-agent | Architect + Critic + Synthesizer |
| 6-agent | Understanding + Explorer + Design + Challenger + Validator + Decision |
| 10-agent | 6 + Relationship + Data + Invention + Recorder |
| 17-agent | 전체 |

#### EXP-ABLATION: 개별 에이전트 기여도
```
조건: 17-agent에서 하나씩 제거 (17개 조건)
시나리오: 시나리오 2(medium) + 시나리오 3(complex) × 3회 = 102회 실행
측정: Quality Score + Coverage 변화
목적: 어떤 에이전트가 가장 중요한가?
```

#### EXP-CHALLENGE: 적대적 도전의 가치
```
조건: Phase 4 있음 vs Phase 4 없음 (3→5 직행)
시나리오: 5개 × 3회 = 30회 실행
측정: Feasibility Score + Quality Score
목적: H3 검증
```

#### EXP-MODEL: 모델 다양성
```
조건: All-Opus vs Mixed(Opus+GPT4o+Sonnet) vs All-Sonnet
시나리오: 5개 × 3회 = 45회 실행
측정: Unique Perspectives + Quality Score + Cost
목적: H4 검증 + Hegazy vs Li 모순 해결
```

### 총 실행 예산
```
EXP-SCALE:     75회
EXP-ABLATION: 102회
EXP-CHALLENGE:  30회
EXP-MODEL:      45회
────────────────────
합계:          252회

예상 비용 (Mixed-Model 기준 ~$2/회):
  252 × $2 = ~$504

예상 비용 (All-Opus 포함):
  ~$800~$1,200
```

---

## 3. 평가 방법: LLM-as-Judge (MAJ-Eval 기반)

전문가 3명 대신 **MAJ-Eval 프레임워크** 적용:

### Judge 구성
```yaml
judges:
  - role: "Software Architect (10년 경력)"
    model: claude-opus
    rubric: feasibility + scalability
  - role: "DevOps Engineer"
    model: gpt-4o
    rubric: deployability + operational concerns
  - role: "Junior Developer (구현자)"
    model: claude-sonnet
    rubric: understandability + implementation clarity

process:
  1. 각 judge가 독립적으로 1-5점 평가 + CoT reasoning
  2. 3 judge의 점수 집계
  3. 불일치 시 debate round (1회)
  4. 최종 점수 = 가중 평균
  
metrics:
  - Cohen's Kappa (judge 간 일치도)
  - Spearman ρ (인간 평가와의 상관 — 샘플 검증용)
```

### 보정: 인간 평가 샘플
```
252회 중 20회(~8%)를 무작위 선택
→ 실제 인간 1명이 평가 (본인 가능)
→ LLM judge 점수와 인간 점수의 Spearman ρ 계산
→ ρ > 0.6이면 LLM judge 신뢰 가능
```

---

## 4. 데이터 수집 강제 (하드코드)

### 4-1. experiment_runner.py — 모든 실행을 감싸는 wrapper

```python
# 의사 코드
class ExperimentRunner:
    def run(self, config: ExperimentConfig) -> ExperimentResult:
        """모든 실행은 이 함수를 통해야 함. 직접 시스템 호출 금지."""
        
        # 1. 실행 전 기록
        run_id = uuid4()
        log_start(run_id, config)
        
        # 2. 시스템 실행
        result = meta_architect.run(
            scenario=config.scenario,
            agent_config=config.agents,
            model_config=config.models,
            seed=config.seed,
        )
        
        # 3. 자동 측정
        metrics = auto_measure(result)
        # - concept_coverage: 60+ 체크리스트 자동 매칭
        # - unique_perspectives: 다른 조건과 비교하여 고유 관점 추출
        # - cost: 토큰 수 집계
        # - latency: 시간 측정
        # - rounds: 에이전트 호출 횟수
        # - conflicts: Blackboard conflicts_with 수
        # - challenge_rate: Phase 4 actionable ratio
        # - decision_trace: QOC chain 완전성
        
        # 4. LLM-as-Judge 평가
        judge_scores = maj_eval.evaluate(result.final_output)
        
        # 5. 결과 저장 (구조화)
        save_result(run_id, config, result, metrics, judge_scores)
        
        return ExperimentResult(run_id, metrics, judge_scores)
```

### 4-2. 데이터 저장 구조

```
eval/
├── experiments/
│   ├── EXP-SCALE/
│   │   ├── config.yaml         ← 실험 설계 (고정)
│   │   ├── runs/
│   │   │   ├── run-001.json    ← 개별 실행 결과
│   │   │   ├── run-002.json
│   │   │   └── ...
│   │   └── summary.json        ← 집계 결과
│   ├── EXP-ABLATION/
│   ├── EXP-CHALLENGE/
│   └── EXP-MODEL/
├── scenarios/
│   ├── scenario-1-crud.yaml
│   ├── scenario-2-chat.yaml
│   ├── scenario-3-multiagent.yaml
│   ├── scenario-4-ambiguous.yaml
│   └── scenario-5-extreme.yaml
├── judges/
│   ├── rubric.yaml             ← 평가 루브릭 (고정)
│   └── calibration/            ← 인간 보정 데이터
└── paper/
    ├── tables/                 ← 자동 생성 테이블
    ├── figures/                ← 자동 생성 그래프
    └── stats/                  ← 통계 분석 결과
```

### 4-3. 개별 실행 데이터 스키마 (run-XXX.json)

```json
{
  "run_id": "uuid",
  "timestamp": "ISO-8601",
  "experiment": "EXP-SCALE",
  "condition": "6-agent",
  "scenario": "scenario-2-chat",
  "repetition": 1,
  
  "config": {
    "agents": ["context_profiler", "problem_decomposer", ...],
    "models": {"context_profiler": "claude-opus-4-6", ...},
    "temperature": 0.7,
    "seed": 42,
    "max_rounds": 50
  },
  
  "execution": {
    "total_rounds": 23,
    "agent_calls": [
      {"agent": "context_profiler", "round": 1, "tokens_in": 3200, "tokens_out": 800, "latency_ms": 4500},
      ...
    ],
    "phase_transitions": [
      {"from": "phase1", "to": "phase2", "round": 6, "reason": "all slots reviewed"},
      ...
    ],
    "conflicts": [...],
    "deadlocks": [...],
    "user_interactions": [...]
  },
  
  "output": {
    "blackboard_final": { ... },
    "qoc_records": [...],
    "adr_records": [...],
    "diagrams": [...]
  },
  
  "metrics": {
    "concept_coverage": 42,
    "concept_coverage_list": ["DDD", "FMEA", ...],
    "unique_perspectives": 5,
    "unique_perspectives_list": ["..."],
    "total_tokens": 128000,
    "total_cost_usd": 2.34,
    "total_latency_sec": 180,
    "conflict_count": 7,
    "challenge_rate": 0.67,
    "decision_trace_completeness": 0.95
  },
  
  "judge_scores": {
    "architect_judge": {"score": 4.2, "reasoning": "..."},
    "devops_judge": {"score": 3.8, "reasoning": "..."},
    "developer_judge": {"score": 4.5, "reasoning": "..."},
    "aggregate": 4.17,
    "cohens_kappa": 0.72
  }
}
```

### 4-4. 자동 논문 테이블/그래프 생성

```python
# eval/paper/generate_tables.py

def table_1_scale_results():
    """Table 1: Effect of Agent Count on Architecture Quality"""
    # EXP-SCALE 데이터에서 자동 생성
    # 행: 1-agent, 3-agent, 6-agent, 10-agent, 17-agent
    # 열: Coverage, Quality, Cost, Latency
    # 각 셀: mean ± std (3회 반복)
    
def table_2_ablation():
    """Table 2: Ablation Study — Individual Agent Contribution"""
    # EXP-ABLATION 데이터에서 자동 생성
    # 각 에이전트 제거 시 Quality 변화 (delta)
    
def figure_1_scaling_curve():
    """Figure 1: Architecture Quality vs Agent Count (logistic fit)"""
    # EXP-SCALE 데이터로 로지스틱 곡선 피팅
    # Qian(ICLR 2025)의 collaborative scaling law와 비교
    
def figure_2_cost_quality_frontier():
    """Figure 2: Cost-Quality Pareto Frontier"""
    # 모든 조건의 (cost, quality) 산점도
    # Pareto optimal 조건 하이라이트

def table_3_model_diversity():
    """Table 3: Effect of Model Diversity"""
    # EXP-MODEL 데이터
    # Hegazy vs Li 모순 실험적 해결

def figure_3_challenge_impact():
    """Figure 3: Impact of Adversarial Challenge Phase"""
    # EXP-CHALLENGE 데이터
    # with/without Phase 4 비교
```

---

## 5. 하드코드 강제 메커니즘

### 5-1. CLAUDE.md 추가 규칙

```markdown
## 6. Experiment Protocol
모든 시스템 실행은 experiment_runner.py를 통해야 한다.
- 직접 meta_architect.run() 호출 금지
- 모든 실행은 eval/experiments/{EXP_NAME}/runs/에 자동 저장
- 실행 후 metrics 자동 계산 + judge 자동 평가
- 테이블/그래프 재생성: python eval/paper/generate_tables.py
```

### 5-2. 코드 레벨 강제

```python
# src/meta_architect.py
class MetaArchitect:
    def run(self, scenario, **kwargs):
        if not kwargs.get("_from_experiment_runner"):
            raise RuntimeError(
                "직접 호출 금지. ExperimentRunner.run()을 사용하세요. "
                "모든 실행은 논문 데이터로 기록되어야 합니다."
            )
        ...
```

### 5-3. hook 추가 (eval 디렉토리 보호)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command", 
            "command": "python3 research/check_paper_deps.py \"$TOOL_INPUT\""
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$TOOL_INPUT\" | grep -q 'eval/experiments.*\\.json' && echo 'WARNING: eval/experiments/ 데이터를 직접 수정하지 마세요. ExperimentRunner만 쓸 수 있습니다.' || true"
          }
        ]
      }
    ]
  }
}
```

### 5-4. Pre-registration 문서

```markdown
# PRE-REGISTRATION.md (실험 시작 전 작성, 이후 수정 금지)

## 가설
H1, H2, H3, H4 (위에 정의)

## 분석 계획
- H1: 17-agent vs 1-agent, paired t-test, α = 0.05
- H2: 에이전트 수 vs Quality, logistic regression fit, R² 보고
- H3: with vs without Phase 4, paired t-test, α = 0.05  
- H4: Mixed vs Homogeneous, paired t-test, α = 0.05

## 표본 크기
- 각 조건 × 5 시나리오 × 3 반복 = 15 데이터 포인트
- 효과 크기 d=0.8 (large) 기준 power analysis

## 데이터 수집 완료 조건
- 모든 실험 매트릭스 완료 (252회)
- 결측 데이터 10% 미만

## 분석 시작 조건  
- 데이터 수집 100% 완료 후 분석 시작
- 데이터 확인 후 가설/분석 계획 수정 금지 (HARKing 방지)
```

---

## 6. MVP → 논문 연결

Master Plan Review의 C1(MVP 없음) 수정과 논문 설계를 결합:

```
Phase 0.5: 3-agent MVP
  → EXP-SCALE의 "3-agent" 조건 데이터 수집 시작
  → 이 시점에서 이미 논문 Table 1의 한 행이 채워짐

Phase 1-2: 점진적 에이전트 추가
  → 에이전트 추가할 때마다 EXP-SCALE + EXP-ABLATION 데이터 수집
  → Table 1이 점진적으로 완성됨

Phase 3: 통합
  → EXP-CHALLENGE, EXP-MODEL 실행
  → Table 3, Figure 3 완성

Phase 4: 전체 평가 + 논문 작성
  → generate_tables.py 실행 → 테이블/그래프 자동 생성
  → 논문 초고 작성
```

**핵심**: 구현 과정 자체가 실험 데이터 수집 과정이다. 
별도의 "평가 Phase"가 아니라, 만들면서 동시에 논문 데이터가 쌓인다.

---

## 7. 구현할 파일 목록

| 파일 | 역할 |
|------|------|
| `eval/experiment_runner.py` | 실험 실행 wrapper + 자동 측정 + 자동 저장 |
| `eval/experiment_config.py` | ExperimentConfig Pydantic 모델 |
| `eval/auto_measure.py` | concept coverage 자동 매칭 등 측정 함수들 |
| `eval/maj_eval.py` | LLM-as-Judge (MAJ-Eval) 구현 |
| `eval/paper/generate_tables.py` | 논문 테이블/그래프 자동 생성 |
| `eval/scenarios/*.yaml` | 5개 표준 시나리오 정의 |
| `eval/judges/rubric.yaml` | 평가 루브릭 |
| `PRE-REGISTRATION.md` | 가설 + 분석 계획 (수정 금지) |
| `CLAUDE.md` 업데이트 | §6 Experiment Protocol 추가 |
