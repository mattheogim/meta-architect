#!/usr/bin/env python3
"""Cross-reference validator for claim tags.

Scans documents for [src:paper-XX] tags and validates:
1. Does the referenced paper exist in papers-catalog.md?
2. Does research/verified/XX.md exist? (has it been read?)
3. Do numbers near the tag match numbers in verified/XX.md?

Usage:
    python research/validate_claims.py                    # scan all docs
    python research/validate_claims.py research/MASTER-PLAN.md  # scan one file
"""

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
RESEARCH_DIR = PROJECT_ROOT / "research"
VERIFIED_DIR = RESEARCH_DIR / "verified"
CATALOG_PATH = RESEARCH_DIR / "papers-catalog.md"

# Files to scan for claim tags
SCAN_TARGETS = [
    RESEARCH_DIR / "MASTER-PLAN.md",
    RESEARCH_DIR / "EXPERIMENT-DESIGN.md",
    RESEARCH_DIR / "MASTER-PLAN-REVIEW.md",
    PROJECT_ROOT / "PRE-REGISTRATION.md",
    PROJECT_ROOT / "v2" / "meta-architect-v2.md",
]

# Regex patterns
SRC_TAG = re.compile(r"\[src:([^\]]+)\]")
PAPER_REF = re.compile(r"paper-([A-Z]\d+)")
NUMBER_NEAR_TAG = re.compile(
    r"(\d+(?:\.\d+)?%?)\s*(?:\[src:|.{0,30}\[src:)"
)


def load_catalog_ids() -> set[str]:
    """Extract paper IDs (A1, B1, etc.) from papers-catalog.md."""
    if not CATALOG_PATH.exists():
        return set()
    text = CATALOG_PATH.read_text()
    # Match headers like "### A1." or "### E6."
    ids = set()
    for match in re.finditer(r"###\s+(?:.*?)([A-Z]\d+)\.", text):
        ids.add(match.group(1))
    # Also match inline refs like "A1", "E6" after ### headers
    for match in re.finditer(r"###\s+([A-Z]\d+)", text):
        ids.add(match.group(1))
    return ids


def load_verified_ids() -> set[str]:
    """List paper IDs that have been verified (research/verified/XX.md exists)."""
    if not VERIFIED_DIR.exists():
        return set()
    return {p.stem for p in VERIFIED_DIR.glob("*.md")}


def load_verified_numbers(paper_id: str) -> set[str]:
    """Extract numbers from a verified paper file for cross-checking."""
    path = VERIFIED_DIR / f"{paper_id}.md"
    if not path.exists():
        return set()
    text = path.read_text()
    return set(re.findall(r"\d+(?:\.\d+)?%", text))


def scan_file(filepath: Path, catalog_ids: set, verified_ids: set) -> list[dict]:
    """Scan a file for claim tags and validate them."""
    if not filepath.exists():
        return []

    text = filepath.read_text()
    lines = text.split("\n")
    issues = []

    for line_num, line in enumerate(lines, 1):
        for tag_match in SRC_TAG.finditer(line):
            full_src = tag_match.group(1)

            # Check paper references
            for paper_match in PAPER_REF.finditer(full_src):
                paper_id = paper_match.group(1)

                # Check 1: Does paper exist in catalog?
                if paper_id not in catalog_ids:
                    issues.append({
                        "file": str(filepath.relative_to(PROJECT_ROOT)),
                        "line": line_num,
                        "severity": "ERROR",
                        "message": f"Paper {paper_id} not found in papers-catalog.md",
                        "tag": full_src,
                    })

                # Check 2: Is paper verified?
                if paper_id not in verified_ids:
                    issues.append({
                        "file": str(filepath.relative_to(PROJECT_ROOT)),
                        "line": line_num,
                        "severity": "WARN",
                        "message": f"Paper {paper_id} not verified (research/verified/{paper_id}.md missing)",
                        "tag": full_src,
                    })

    # Check for numbers without source tags (potential hallucination)
    for line_num, line in enumerate(lines, 1):
        # Skip code blocks and headers
        if line.strip().startswith(("```", "#", "|", "-")):
            continue
        # Find percentages or key numbers
        numbers = re.findall(r"(\d+(?:\.\d+)?)\s*%", line)
        for num in numbers:
            if not SRC_TAG.search(line):
                # Number exists but no source tag on this line
                issues.append({
                    "file": str(filepath.relative_to(PROJECT_ROOT)),
                    "line": line_num,
                    "severity": "INFO",
                    "message": f"Number '{num}%' without [src:] tag — potential untracked claim",
                    "tag": None,
                })

    return issues


def main():
    catalog_ids = load_catalog_ids()
    verified_ids = load_verified_ids()

    if len(sys.argv) > 1:
        targets = [Path(sys.argv[1])]
    else:
        targets = SCAN_TARGETS

    all_issues = []
    for target in targets:
        issues = scan_file(target, catalog_ids, verified_ids)
        all_issues.extend(issues)

    if not all_issues:
        print("All claim tags validated. No issues found.")
        return

    # Group by severity
    errors = [i for i in all_issues if i["severity"] == "ERROR"]
    warns = [i for i in all_issues if i["severity"] == "WARN"]
    infos = [i for i in all_issues if i["severity"] == "INFO"]

    print(f"=== Claim Validation Results ===\n")
    print(f"  ERRORS: {len(errors)}  (broken references)")
    print(f"  WARNS:  {len(warns)}  (unverified papers)")
    print(f"  INFO:   {len(infos)}  (untagged numbers)")
    print()

    for issue in errors:
        print(f"  ERROR  {issue['file']}:{issue['line']} — {issue['message']}")

    if warns:
        print()
        # Deduplicate warnings by paper ID
        seen_papers = set()
        for issue in warns:
            paper_id = PAPER_REF.search(issue["tag"] or "")
            if paper_id:
                pid = paper_id.group(1)
                if pid not in seen_papers:
                    seen_papers.add(pid)
                    print(f"  WARN   Paper {pid} referenced but not verified")

    if infos and len(infos) <= 20:
        print()
        for issue in infos:
            print(f"  INFO   {issue['file']}:{issue['line']} — {issue['message']}")
    elif infos:
        print(f"\n  INFO   {len(infos)} untagged numbers (run with specific file for details)")


if __name__ == "__main__":
    main()
