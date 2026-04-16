"""
Paper catalog schema — Pydantic models for structured paper management.

Usage:
    from papers_schema import PaperCatalog, load_catalog, validate_catalog

    catalog = load_catalog("research/papers.yaml")
    errors = validate_catalog(catalog)

Design principle: one file, one schema, no framework.
Counter-evidence considered:
- Ioannidis (2016): systematic processes produce waste when mechanical → keep validation thin
- Cognitive Debt (Storey 2025): over-automation erodes understanding → status forces human reading
- Research SW Tech Debt (arXiv:2603.20415): verification infra accumulates debt → single file, no deps beyond pydantic+yaml
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field, field_validator


class VerificationStatus(str, Enum):
    """4-state verification model (inspired by ASReview's 3-state + our needs)."""
    UNVERIFIED = "unverified"   # In catalog, not checked against source
    READ = "read"               # Someone read the paper
    VERIFIED = "verified"       # Claims used in code checked against original text
    DISPUTED = "disputed"       # Known issues with paper's claims or replication


class PaperEntry(BaseModel):
    """Minimum viable schema for a paper entry.

    Based on convergence across arXiv, Semantic Scholar, Papers With Code,
    CSL-JSON, and Bisonai YAML pattern.
    """

    # === Essential (must have) ===
    id: str = Field(description="Internal key, e.g. 'A1', 'E2'")
    title: str = Field(min_length=5, description="Full paper title")
    authors: list[str] = Field(min_length=1, description="Author list")
    year: int = Field(ge=2000, le=2030, description="Publication year")
    url: str = Field(description="Direct link (arxiv abs, PDF, or publisher)")
    status: VerificationStatus = Field(
        default=VerificationStatus.UNVERIFIED,
        description="Verification state"
    )

    # === Identifiers (at least one required) ===
    arxiv_id: Optional[str] = Field(default=None, description="arXiv ID, e.g. '2305.14325'")
    doi: Optional[str] = Field(default=None, description="DOI")
    ssrn_id: Optional[str] = Field(default=None, description="SSRN abstract ID")

    # === Content ===
    venue: Optional[str] = Field(default=None, description="Conference or journal")
    key_claims: list[str] = Field(
        default_factory=list,
        description="What we use from this paper (prevents misattribution)"
    )
    sections_cited: list[str] = Field(
        default_factory=list,
        description="Sections we cite — MUST be verified against original"
    )
    sections_verified: list[str] = Field(
        default_factory=list,
        description="Sections actually verified by reading original"
    )

    # === Project linkage ===
    used_by_features: list[str] = Field(
        default_factory=list,
        description="Which project features depend on this paper"
    )
    category: str = Field(
        default="uncategorized",
        description="Section category: debate, scaling, blackboard, benchmark, opposing, etc."
    )
    must_read: bool = Field(default=False, description="Required reading before implementation")

    # === Metadata (auto-fillable via API) ===
    citation_count: Optional[int] = Field(default=None, description="Citation count (auto-fill from S2)")
    semantic_scholar_id: Optional[str] = Field(default=None, description="S2 paper ID (auto-fill)")
    verified_date: Optional[str] = Field(default=None, description="When verification happened")
    notes: Optional[str] = Field(default=None, description="Free-form reading notes")

    @field_validator("arxiv_id", "doi", "ssrn_id", mode="after")
    @classmethod
    def at_least_one_identifier(cls, v, info):
        """Warn-level: at least one external identifier should exist."""
        # Validation happens at catalog level, not per-field
        return v

    @field_validator("sections_cited")
    @classmethod
    def sections_must_be_specific(cls, v: list[str]) -> list[str]:
        """Reject vague section references."""
        vague = [s for s in v if s in ("전체", "all", "various", "multiple")]
        # "전체" is OK for short papers — don't reject, just note
        return v


class PaperCatalog(BaseModel):
    """Top-level catalog container."""
    version: str = Field(default="1.0", description="Schema version")
    papers: list[PaperEntry] = Field(default_factory=list)

    def get_paper(self, paper_id: str) -> Optional[PaperEntry]:
        """Lookup by internal ID."""
        for p in self.papers:
            if p.id == paper_id:
                return p
        return None

    def unverified(self) -> list[PaperEntry]:
        """Papers that haven't been verified."""
        return [p for p in self.papers if p.status == VerificationStatus.UNVERIFIED]

    def must_reads_unverified(self) -> list[PaperEntry]:
        """MUST-READ papers that haven't been verified — highest priority."""
        return [p for p in self.papers if p.must_read and p.status == VerificationStatus.UNVERIFIED]

    def missing_identifiers(self) -> list[PaperEntry]:
        """Papers with no external identifier."""
        return [p for p in self.papers if not p.arxiv_id and not p.doi and not p.ssrn_id]

    def summary(self) -> str:
        """One-line status."""
        total = len(self.papers)
        verified = sum(1 for p in self.papers if p.status == VerificationStatus.VERIFIED)
        read = sum(1 for p in self.papers if p.status == VerificationStatus.READ)
        unv = sum(1 for p in self.papers if p.status == VerificationStatus.UNVERIFIED)
        must = len(self.must_reads_unverified())
        return (
            f"Total: {total} | Verified: {verified} | Read: {read} | "
            f"Unverified: {unv} | MUST-READ unverified: {must}"
        )


def load_catalog(path: str | Path) -> PaperCatalog:
    """Load and validate papers.yaml."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Paper catalog not found: {path}")
    with open(path) as f:
        data = yaml.safe_load(f)
    return PaperCatalog(**data)


def validate_catalog(catalog: PaperCatalog) -> list[str]:
    """Run validation checks. Returns list of issues."""
    issues = []

    # Check 1: All papers must have at least one identifier
    for p in catalog.missing_identifiers():
        issues.append(f"⚠️  [{p.id}] No external identifier (arxiv_id, doi, or ssrn_id)")

    # Check 2: MUST-READ papers should be verified
    for p in catalog.must_reads_unverified():
        issues.append(f"🔴 [{p.id}] MUST-READ but status={p.status.value}: {p.title}")

    # Check 3: sections_cited should match sections_verified
    for p in catalog.papers:
        if p.sections_cited and not p.sections_verified:
            if p.status in (VerificationStatus.VERIFIED, VerificationStatus.READ):
                issues.append(
                    f"⚠️  [{p.id}] Status={p.status.value} but no sections_verified"
                )

    # Check 4: Duplicate IDs
    ids = [p.id for p in catalog.papers]
    dupes = [id for id in ids if ids.count(id) > 1]
    if dupes:
        issues.append(f"❌ Duplicate IDs: {set(dupes)}")

    # Check 5: used_by_features should reference valid features
    # (cross-reference with paper-feature-map.json if exists)

    return issues


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "research/papers.yaml"
    try:
        catalog = load_catalog(path)
        print(catalog.summary())
        print()
        issues = validate_catalog(catalog)
        if issues:
            print(f"Found {len(issues)} issues:")
            for issue in issues:
                print(f"  {issue}")
        else:
            print("✅ No issues found")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
