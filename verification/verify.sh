#!/bin/bash
FILE="/home/claude/meta-architect-v2.md"
PASS=0
FAIL=0
EXTRA=0

echo "# Meta Architect v2 — 검증 보고서"
echo ""
echo "> 생성 시점: $(date '+%Y-%m-%d %H:%M')"
echo "> 대상 파일: meta-architect-v2.md ($(wc -l < $FILE) lines)"
echo ""
echo "---"
echo ""

check() {
  local id="$1"
  local label="$2"
  local pattern="$3"
  local approval="$4"
  local result=$(grep -n "$pattern" "$FILE" | head -3)
  if [ -n "$result" ]; then
    echo "### $id: $label"
    echo "- 승인: $approval"
    echo "- 상태: ✅ 확인됨"
    echo '```'
    echo "$result"
    echo '```'
    echo ""
    PASS=$((PASS+1))
  else
    echo "### $id: $label"
    echo "- 승인: $approval"
    echo "- 상태: ❌ 미발견 (패턴: $pattern)"
    echo ""
    FAIL=$((FAIL+1))
  fi
}

cross_check() {
  local id="$1"
  local label="$2"
  local desc="$3"
  shift 3
  echo "### $id: [교차검증] $label"
  echo "- 설명: $desc"
  local all_found=true
  for pattern in "$@"; do
    local result=$(grep -n "$pattern" "$FILE" | head -2)
    if [ -n "$result" ]; then
      echo "- ✅ \`$pattern\`:"
      echo '```'
      echo "$result"
      echo '```'
    else
      echo "- ❌ \`$pattern\` 미발견"
      all_found=false
    fi
  done
  if $all_found; then
    echo "- **결과: ✅ 정합성 확인**"
  else
    echo "- **결과: ⚠️ 일부 누락 — 수동 확인 필요**"
  fi
  echo ""
}

echo "## Part 1: 사전 승인 항목 (✅)"
echo ""

check "A01" "Orchestrator 4모듈 분해" "Router.*규칙" "✅ 사전"
check "A02" "State Assessor" "State Assessor" "✅ 사전"
check "A03" "Deadlock Resolver" "Deadlock Resolver" "✅ 사전"
check "A04" "Interaction Gate" "Interaction Gate" "✅ 사전"
check "A05" "Blackboard 13슬롯" "validation:" "✅ 사전"
check "A06" "에이전트별 읽기/쓰기 뷰" "에이전트.*읽기.*쓰기" "✅ 사전"
check "A07" "상태 전이 원칙 1: 자기 검증 금지" "자기 검증 금지" "✅ 사전"
check "A08" "상태 전이 원칙 2: Peer Review" "Peer Review" "✅ 사전"
check "A09" "상태 전이 원칙 3: Conflict 해소 전제" "conflicts_with.*남아있으면" "✅ 사전"
check "A10" "상태 전이 원칙 4: Deadlocked 강제 결정" "deadlocked" "✅ 사전"
check "A11" "hard_constraints vs priorities 분리" "hard_constraints" "✅ 사전"
check "A12" "impact_on_decision 메타데이터" "impact_on_decision" "✅ 사전"
check "A13" "에이전트 실패 프로토콜 (no_contribution)" "no_contribution" "✅ 사전"
check "A14" "Prototype Validator (Phase 4.5)" "Prototype Validator" "✅ 사전"
check "A15" "Cost Auditor → Risk에 흡수" "Risk, Cost & Scale" "✅ 사전"
check "A16" "HITL → 출력 레이어" "출력 레이어" "✅ 사전"
check "A17" "Mediated Query 프로토콜" "needs_response_from" "✅ 사전"
check "A18" "사용자 피드백 루프" "user_feedback" "✅ 사전"
check "A19" "GC 규칙" "Garbage Collection" "✅ 사전"
check "A20" "Lazy Loading" "Lazy Loading" "✅ 사전"
check "A21" "changeability_score" "changeability_score" "✅ 사전"
check "A22" "Recorder 상세 설계 (QOC 변환)" "QOC 변환 규칙" "✅ 사전"
check "A23" "Decision Evaluator 2단계" "Hard Constraint 필터" "✅ 사전"
check "A24" "evidence_level 메타데이터" "evidence_level" "✅ 사전"

echo ""
echo "## Part 1b: 버그 수정 (✅ — 문서 내부 불일치 수정)"
echo ""

check "B01" "status enum에 no_contribution 추가" "deadlocked | no_contribution" "✅ 버그수정"
check "B02" "challenge type enum 확장" "deadlock_resolution" "✅ 버그수정"
check "B03" "상태전이 다이어그램 v1 수동 명시" "Interaction Gate 사용자 승인" "✅ 버그수정"
check "B04" "infeasible 상태" "infeasible" "✅ 버그수정"
check "B05" "tags 필드" "tags: \[string\]" "✅ 버그수정"
check "B06" "State Assessor no_contribution 충분성" "justified no_contribution" "✅ 버그수정"
check "B07" "reason 필드 메타데이터" "reason: optional string" "✅ 버그수정"
check "B08" "decision 슬롯 status/reason" "decided | infeasible" "✅ 버그수정"
check "B09" "success_criteria 메타데이터" "success_criteria: optional string" "✅ 버그수정"
check "B10" "Router 누락 슬롯 규칙" "cross_domain.*비어있으면" "✅ 버그수정"
check "B11" "Invention Engine 활성화 조건" "challenges.*optional" "✅ 버그수정"
check "B12" "State Assessor reviewed 기준" "reviewed 이상 항목" "✅ 버그수정"
check "B13" "Prototype Validator 읽기뷰 통일" "메타데이터에서 읽음" "✅ 버그수정"
check "B14" "Decision 출력 리스트 status/reason" "status: decided" "✅ 버그수정"

echo ""
echo "## Part 2: 무단 삽입 7개 (🔴 → 사후 유지)"
echo ""

check "X01" "Modeler decision 읽기 (필요)" "Modeler.*decision" "🔴 무단→유지 (필요: 없으면 모든 옵션 다이어그램화)"
check "X02" "Circuit Breaker (필요)" "Circuit Breaker" "🔴 무단→유지 (필요: 없으면 무한 루프)"
check "X03" "Validation 루프 상한 (필요)" "validation_failed_2x\|2회.*fail" "🔴 무단→유지 (필요: 없으면 무한 반복)"
check "X04" "Observability (나중에 해도 됨)" "Observability" "🔴 무단→유지 (나중에 해도 됨)"
check "X05" "Evaluation (나중에 해도 됨)" "agent_performance\|quality_gates" "🔴 무단→유지 (나중에 해도 됨)"
check "X06" "Security & Governance (나중에 해도 됨)" "Security & Governance" "🔴 무단→유지 (나중에 해도 됨)"
check "X07" "13.5 Evidence Source (나중에 해도 됨)" "Evidence Source" "🔴 무단→사후승인 (나중에 해도 됨)"

echo ""
echo "## Part 3: 교차 검증 (핵심 정합성)"
echo ""

cross_check "C01" "deadlocked 정합성" \
  "deadlocked가 상태전이 + Deadlock Resolver + Decision Evaluator에 모두 연결돼 있는가" \
  "deadlocked" "Deadlock Resolver" "deadlock_resolution" "overridden_by_priority"

cross_check "C02" "success_criteria 정합성" \
  "success_criteria가 메타데이터 + Prototype Validator + 읽기뷰에서 일관되는가" \
  "success_criteria: optional string" "원본 항목의 메타데이터에 정의" "메타데이터에서 읽음"

cross_check "C03" "infeasible 정합성" \
  "infeasible이 decision 슬롯 + Decision Evaluator 본문 + 흐름도에 있는가" \
  "decided | infeasible" "decision.status: infeasible" "infeasible.*사용자"

cross_check "C04" "no_contribution 정합성" \
  "no_contribution이 status enum + 실패 프로토콜 + State Assessor + Circuit Breaker에 연결되는가" \
  "deadlocked | no_contribution" "status: no_contribution" "justified no_contribution" "Circuit Breaker"

cross_check "C05" "hard_constraints → Decision 2단계 정합성" \
  "hard_constraints가 context 슬롯 + Decision Evaluator 1단계에 연결되는가" \
  "hard_constraints:" "Hard Constraint 필터" "전부 탈락"

cross_check "C06" "Mediated Query 정합성" \
  "needs_response_from이 메타데이터 + 프로토콜 + Router 규칙에 연결되는가" \
  "needs_response_from: optional" "needs_response_from.*needs_input" "최우선 호출"

echo ""
echo "## Part 4: 나중에 목록 (v1 돌려보고 결정)"
echo ""
echo "| # | 항목 | 출처 | 이유 |"
echo "|---|------|------|------|"
echo "| L01 | Reviewability matrix | GPT | v1 운영 후 사례 쌓이면 도입 |"
echo "| L02 | Accepted 자동 승격 | GPT | 초기에는 수동이 안전장치 |"
echo "| L03 | Shared vocabulary layer | GPT | Knowledge Curator가 이미 커버 |"
echo "| L04 | expires_after_rounds | GPT | GC 규칙이 이미 커버 |"
echo "| L05 | Memory hierarchy (L1/L2) | Meta AI | GC 규칙이 이미 처리 |"
echo "| L06 | Agent Registry | Meta AI | 17개 고정인 v2에서 과설계 |"
echo ""

echo "## Part 5: 통계"
echo ""
echo "| 분류 | 수 |"
echo "|------|-----|"
echo "| ✅ 확인됨 | $PASS |"
echo "| ❌ 미발견 | $FAIL |"
echo ""
echo "---"
echo "*이 보고서는 1회성 스냅샷이다. 문서 수정 시 다시 실행할 것.*"

