"""Decision Gate — BREAK 모드를 하드코드로 강제.

모든 주요 결정은 이 게이트를 통과해야 한다.
필수 필드가 비어있으면 결정을 거부한다.

프롬프트에 "BREAK 해줘"라고 부탁하는 게 아니라,
코드가 BREAK 없는 결정을 물리적으로 차단한다.

Usage:
    gate = DecisionGate()

    # 이렇게 하면 통과:
    decision = gate.validate(Decision(
        choice="Blackboard 패턴 사용",
        alternatives=["Pipeline", "Swarm"],
        weaknesses=["자연어 모호성", "구현 복잡도"],
        pre_mortem="Phase 간 에러 전파로 25% 정확도",
        probability=0.7,
        evidence=["paper-C1", "paper-E1"],
        reversible=False,
    ))

    # 이렇게 하면 거부 (alternatives 비어있음):
    decision = gate.validate(Decision(
        choice="Blackboard 패턴 사용",
        alternatives=[],  # ← ValidationError!
        ...
    ))
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class Decision(BaseModel):
    """하드코드된 BREAK 강제 — 모든 필수 필드가 있어야 유효한 결정.

    BUILD만 하고 BREAK를 안 하면 이 모델을 채울 수 없다.
    → BREAK를 안 하는 것이 물리적으로 불가능.
    """

    # BUILD (뭘 할 건가)
    choice: str = Field(description="선택한 것")
    reason: str = Field(description="왜 이걸 선택했는가")

    # BREAK (왜 실패하는가) — 비어있으면 거부
    alternatives: list[str] = Field(
        min_length=1,
        description="고려한 대안 최소 1개. 없으면 결정 불가.",
    )
    weaknesses: list[str] = Field(
        min_length=1,
        description="이 결정의 약점 최소 1개. 없으면 결정 불가.",
    )
    pre_mortem: str = Field(
        min_length=10,
        description="'이게 실패했다. 왜?' — 10자 이상",
    )
    probability: float = Field(
        ge=0.0,
        le=1.0,
        description="이게 실제로 작동할 확률 0.0~1.0",
    )

    # ZOOM (빠진 것)
    unasked_questions: list[str] = Field(
        default_factory=list,
        description="아직 안 다룬 질문들 (선택)",
    )

    # 메타
    evidence: list[str] = Field(
        default_factory=list,
        description="근거 [src:paper-X] 목록",
    )
    reversible: bool = Field(
        description="이 결정을 1주일 안에 되돌릴 수 있는가?",
    )
    type1_full_review: bool = Field(
        default=False,
        description="Type 1 결정이면 True. FLIP 모드도 적용했는지 확인.",
    )

    @field_validator("pre_mortem")
    @classmethod
    def pre_mortem_not_empty(cls, v: str) -> str:
        if v.strip().lower() in ("없음", "none", "n/a", "해당없음"):
            raise ValueError(
                "pre_mortem에 '없음'은 불가. "
                "모든 결정은 실패할 수 있다. 실패 이유를 써야 한다."
            )
        return v

    @field_validator("probability")
    @classmethod
    def probability_not_certain(cls, v: float) -> float:
        if v >= 1.0:
            raise ValueError(
                "probability=1.0은 불가. 100% 확실한 것은 없다. "
                "최대 0.95까지."
            )
        return v


class DecisionGate:
    """결정 게이트. validate()를 통과해야 유효한 결정."""

    def __init__(self):
        self.decisions: list[Decision] = []

    def validate(self, decision: Decision) -> Decision:
        """결정을 검증하고 기록한다.

        Pydantic이 자동으로:
        - alternatives 비어있으면 → ValidationError
        - weaknesses 비어있으면 → ValidationError
        - pre_mortem 10자 미만이면 → ValidationError
        - probability 1.0이면 → ValidationError

        즉, BREAK를 안 하면 물리적으로 통과 불가.
        """
        # Type 1 결정인데 FLIP 안 했으면 경고
        if not decision.reversible and not decision.type1_full_review:
            print(
                f"WARNING: 되돌릴 수 없는 결정인데 type1_full_review=False. "
                f"FLIP 모드(Inversion, Opportunity Cost)를 적용했는지 확인하세요."
            )

        self.decisions.append(decision)
        return decision

    def summary(self) -> str:
        """모든 결정의 요약."""
        lines = []
        for i, d in enumerate(self.decisions, 1):
            lines.append(
                f"D{i}: {d.choice} "
                f"(prob={d.probability:.0%}, "
                f"reversible={d.reversible}, "
                f"weaknesses={len(d.weaknesses)}, "
                f"alternatives={len(d.alternatives)})"
            )
        return "\n".join(lines)


if __name__ == "__main__":
    gate = DecisionGate()

    # 좋은 결정 (통과)
    d1 = gate.validate(
        Decision(
            choice="Blackboard 패턴 사용",
            reason="에이전트 간 데이터 공유에 적합. Han&Zhang(2025) 검증됨.",
            alternatives=["Pipeline (순차)", "Swarm (분산)"],
            weaknesses=["자연어 모호성 (La Malfa 2025)", "구현 복잡도"],
            pre_mortem="Phase 간 에러 전파로 정확도 25% 하락 가능 (MAST 2025)",
            probability=0.75,
            evidence=["paper-C1", "paper-E1"],
            reversible=False,
            type1_full_review=True,
        )
    )
    print(f"통과: {d1.choice}")

    # 나쁜 결정 (거부 — alternatives 없음)
    try:
        gate.validate(
            Decision(
                choice="그냥 Pipeline으로",
                reason="단순하니까",
                alternatives=[],  # ← 거부됨!
                weaknesses=["유연성 부족"],
                pre_mortem="변경 요청 시 전체 재설계 필요",
                probability=0.6,
                reversible=True,
            )
        )
    except Exception as e:
        print(f"거부: {e}")

    # 나쁜 결정 (거부 — pre_mortem 없음)
    try:
        gate.validate(
            Decision(
                choice="All-Opus 모델",
                reason="제일 좋으니까",
                alternatives=["All-Sonnet"],
                weaknesses=["비용"],
                pre_mortem="없음",  # ← 거부됨!
                probability=0.8,
                reversible=True,
            )
        )
    except Exception as e:
        print(f"거부: {e}")

    print(f"\n{gate.summary()}")
