#!/usr/bin/env python3
"""
Paper verification pipeline — Level 1-3 automated checks.

Level 0: LLM found it (lowest trust — already done, stored in papers.yaml)
Level 1: API existence check (this script) — arXiv API + Semantic Scholar
Level 2: Original text reading (manual — WebFetch + record in verified/)
Level 3: Cross-verification (manual — 2+ independent sources)

Usage:
    python research/verify_papers.py                    # verify all
    python research/verify_papers.py --paper A1         # verify one
    python research/verify_papers.py --auto-fill        # fetch & fill metadata
    python research/verify_papers.py --summary          # just show status

Design: one file, one command. No framework.
Counter-evidence applied:
- Ioannidis (2016): don't over-systematize → only check what's actionable
- Cognitive Debt (2025): don't replace reading → flag what needs human reading
- Automation Bias (2016): don't create false confidence → report uncertainty

Dependencies: pip install pyyaml requests
(arxiv and semanticscholar packages optional for richer metadata)
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Optional

import yaml

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# ── Constants ──────────────────────────────────────────────────

CATALOG_PATH = Path(__file__).parent / "papers.yaml"
VERIFIED_DIR = Path(__file__).parent / "verified"

ARXIV_API = "http://export.arxiv.org/api/query"
S2_API = "https://api.semanticscholar.org/graph/v1/paper"

# Rate limiting: arXiv asks for 3s between requests, S2 allows 100/sec unauthenticated
ARXIV_DELAY = 3.0
S2_DELAY = 0.5


# ── Data loading ───────────────────────────────────────────────

def load_catalog(path: Path = CATALOG_PATH) -> dict:
    """Load papers.yaml."""
    if not path.exists():
        print(f"❌ Catalog not found: {path}")
        sys.exit(1)
    with open(path) as f:
        return yaml.safe_load(f)


def save_catalog(data: dict, path: Path = CATALOG_PATH) -> None:
    """Save papers.yaml preserving order."""
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


# ── arXiv verification ────────────────────────────────────────

def verify_arxiv(arxiv_id: str) -> dict:
    """Check if arXiv ID exists and return metadata.

    Returns:
        {
            "exists": bool,
            "title": str or None,
            "authors": list[str] or None,
            "published": str or None,  # e.g. "2023-05-23"
            "summary": str or None,
            "error": str or None
        }
    """
    if not HAS_REQUESTS:
        return {"exists": None, "error": "requests not installed"}

    try:
        resp = requests.get(
            ARXIV_API,
            params={"id_list": arxiv_id, "max_results": 1},
            timeout=15,
        )
        resp.raise_for_status()
    except Exception as e:
        return {"exists": None, "error": str(e)}

    text = resp.text

    # arXiv API returns Atom XML. Simple parsing without lxml.
    if "<title>Error</title>" in text:
        return {"exists": False, "error": "arXiv returned Error"}

    # Check for actual entry
    if "<entry>" not in text:
        return {"exists": False, "error": "No entry found"}

    # Extract title (between first <title> inside <entry> and </title>)
    import re
    entry = text[text.index("<entry>"):]

    title_match = re.search(r"<title>(.*?)</title>", entry, re.DOTALL)
    title = title_match.group(1).strip().replace("\n", " ") if title_match else None

    # Extract authors
    authors = re.findall(r"<name>(.*?)</name>", entry)

    # Extract published date
    pub_match = re.search(r"<published>(.*?)</published>", entry)
    published = pub_match.group(1)[:10] if pub_match else None

    # Check if it's a valid paper (not the "no results" page)
    if title and "Error" not in title:
        return {
            "exists": True,
            "title": title,
            "authors": authors,
            "published": published,
            "error": None,
        }
    else:
        return {"exists": False, "error": f"Invalid entry: {title}"}


# ── Semantic Scholar verification ─────────────────────────────

def verify_semantic_scholar(arxiv_id: str = None, doi: str = None, title: str = None) -> dict:
    """Check Semantic Scholar for paper and return metadata.

    Returns:
        {
            "exists": bool,
            "s2_id": str or None,
            "title": str or None,
            "authors": list[str] or None,
            "venue": str or None,
            "year": int or None,
            "citation_count": int or None,
            "error": str or None
        }
    """
    if not HAS_REQUESTS:
        return {"exists": None, "error": "requests not installed"}

    # Build paper ID for S2 API
    if arxiv_id:
        paper_id = f"ARXIV:{arxiv_id}"
    elif doi:
        paper_id = f"DOI:{doi}"
    else:
        # Search by title (less reliable)
        return {"exists": None, "error": "No arxiv_id or doi for S2 lookup"}

    fields = "title,authors,venue,year,citationCount,externalIds"

    try:
        resp = requests.get(
            f"{S2_API}/{paper_id}",
            params={"fields": fields},
            timeout=15,
        )
        if resp.status_code == 404:
            return {"exists": False, "error": "Not found in Semantic Scholar"}
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return {"exists": None, "error": str(e)}

    authors = [a.get("name", "") for a in data.get("authors", [])]

    return {
        "exists": True,
        "s2_id": data.get("paperId"),
        "title": data.get("title"),
        "authors": authors,
        "venue": data.get("venue"),
        "year": data.get("year"),
        "citation_count": data.get("citationCount"),
        "error": None,
    }


# ── Title similarity check ────────────────────────────────────

def title_similarity(a: str, b: str) -> float:
    """Simple word-level Jaccard similarity for title comparison."""
    if not a or not b:
        return 0.0
    words_a = set(a.lower().split())
    words_b = set(b.lower().split())
    if not words_a or not words_b:
        return 0.0
    return len(words_a & words_b) / len(words_a | words_b)


# ── Main verification ─────────────────────────────────────────

def verify_paper(paper: dict, auto_fill: bool = False) -> list[str]:
    """Verify a single paper entry. Returns list of issues."""
    issues = []
    pid = paper.get("id", "???")
    title = paper.get("title", "")
    arxiv_id = paper.get("arxiv_id")
    doi = paper.get("doi")
    status = paper.get("status", "unverified")

    # ── Level 1a: arXiv existence check ──
    if arxiv_id:
        print(f"  [{pid}] Checking arXiv:{arxiv_id}...", end=" ", flush=True)
        result = verify_arxiv(arxiv_id)
        time.sleep(ARXIV_DELAY)

        if result["exists"] is True:
            print("✅ exists")

            # Title match check
            if result["title"]:
                sim = title_similarity(title, result["title"])
                if sim < 0.5:
                    issues.append(
                        f"⚠️  [{pid}] Title mismatch (similarity={sim:.2f})\n"
                        f"     Catalog: {title}\n"
                        f"     arXiv:   {result['title']}"
                    )
                elif sim < 0.8:
                    issues.append(
                        f"ℹ️  [{pid}] Title partially matches (similarity={sim:.2f})"
                    )

            # Author check
            arxiv_authors = result.get("authors", [])
            catalog_authors = paper.get("authors", [])
            if arxiv_authors and catalog_authors:
                # Check first author match
                if catalog_authors[0] and arxiv_authors:
                    first_catalog = catalog_authors[0].split()[-1].lower()  # last name
                    first_arxiv = arxiv_authors[0].split()[-1].lower()
                    if first_catalog != first_arxiv:
                        issues.append(
                            f"⚠️  [{pid}] First author mismatch: "
                            f"catalog='{catalog_authors[0]}' vs arXiv='{arxiv_authors[0]}'"
                        )

            # Auto-fill if requested
            if auto_fill and result["title"]:
                if not paper.get("authors") or paper["authors"] == []:
                    paper["authors"] = result["authors"]

        elif result["exists"] is False:
            issues.append(f"❌ [{pid}] arXiv:{arxiv_id} DOES NOT EXIST — {result['error']}")
        else:
            issues.append(f"⚠️  [{pid}] arXiv check failed: {result['error']}")

    # ── Level 1b: Semantic Scholar check ──
    if arxiv_id or doi:
        print(f"  [{pid}] Checking Semantic Scholar...", end=" ", flush=True)
        s2 = verify_semantic_scholar(arxiv_id=arxiv_id, doi=doi)
        time.sleep(S2_DELAY)

        if s2["exists"] is True:
            print(f"✅ found (citations: {s2.get('citation_count', '?')})")

            # Auto-fill metadata
            if auto_fill:
                if s2.get("citation_count") is not None:
                    paper["citation_count"] = s2["citation_count"]
                if s2.get("s2_id"):
                    paper["semantic_scholar_id"] = s2["s2_id"]
                if s2.get("venue") and not paper.get("venue"):
                    paper["venue"] = s2["venue"]
                if s2.get("year") and not paper.get("year"):
                    paper["year"] = s2["year"]

            # Year check
            if s2.get("year") and paper.get("year"):
                if abs(s2["year"] - paper["year"]) > 1:
                    issues.append(
                        f"⚠️  [{pid}] Year mismatch: catalog={paper['year']} vs S2={s2['year']}"
                    )

        elif s2["exists"] is False:
            issues.append(f"⚠️  [{pid}] Not found in Semantic Scholar")
        else:
            issues.append(f"ℹ️  [{pid}] S2 check skipped: {s2['error']}")

    # ── No identifier at all ──
    if not arxiv_id and not doi and not paper.get("ssrn_id"):
        issues.append(f"⚠️  [{pid}] No external identifier (arxiv_id, doi, or ssrn_id)")

    # ── Unverified sections warning ──
    sections_cited = paper.get("sections_cited", [])
    sections_verified = paper.get("sections_verified", [])
    if sections_cited and not sections_verified:
        issues.append(
            f"ℹ️  [{pid}] Sections cited but not verified: {sections_cited}"
        )

    # ── MUST-READ check ──
    if paper.get("must_read") and status == "unverified":
        issues.append(f"🔴 [{pid}] MUST-READ but not yet verified")

    # ── Verified/ directory check ──
    if status in ("verified", "read"):
        verified_file = VERIFIED_DIR / f"{pid}.md"
        if not verified_file.exists():
            issues.append(
                f"⚠️  [{pid}] Status={status} but no verified/{pid}.md file"
            )

    return issues


def summary(catalog: dict) -> None:
    """Print catalog summary."""
    papers = catalog.get("papers", [])
    total = len(papers)
    by_status = {}
    by_category = {}
    must_read_unverified = 0

    for p in papers:
        s = p.get("status", "unverified")
        by_status[s] = by_status.get(s, 0) + 1
        c = p.get("category", "uncategorized")
        by_category[c] = by_category.get(c, 0) + 1
        if p.get("must_read") and s == "unverified":
            must_read_unverified += 1

    print(f"\n{'='*60}")
    print(f"📚 Paper Catalog Summary")
    print(f"{'='*60}")
    print(f"Total papers: {total}")
    print(f"\nBy status:")
    for s, n in sorted(by_status.items()):
        emoji = {"verified": "✅", "read": "📖", "unverified": "⬜", "disputed": "❌"}.get(s, "?")
        print(f"  {emoji} {s}: {n}")
    print(f"\n🔴 MUST-READ unverified: {must_read_unverified}")
    print(f"\nBy category:")
    for c, n in sorted(by_category.items()):
        print(f"  {c}: {n}")
    print(f"{'='*60}\n")


# ── CLI ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Verify paper catalog against APIs")
    parser.add_argument("--paper", type=str, help="Verify specific paper by ID")
    parser.add_argument("--auto-fill", action="store_true", help="Auto-fill metadata from APIs")
    parser.add_argument("--summary", action="store_true", help="Show summary only")
    parser.add_argument("--catalog", type=str, default=str(CATALOG_PATH), help="Path to papers.yaml")
    args = parser.parse_args()

    catalog = load_catalog(Path(args.catalog))
    papers = catalog.get("papers", [])

    if args.summary:
        summary(catalog)
        return

    if not HAS_REQUESTS:
        print("❌ 'requests' package required. Install: pip install requests")
        sys.exit(1)

    all_issues = []

    if args.paper:
        # Verify single paper
        target = [p for p in papers if p.get("id") == args.paper]
        if not target:
            print(f"❌ Paper '{args.paper}' not found in catalog")
            sys.exit(1)
        issues = verify_paper(target[0], auto_fill=args.auto_fill)
        all_issues.extend(issues)
    else:
        # Verify all papers with external identifiers
        print(f"\n🔍 Verifying {len(papers)} papers...\n")
        for i, p in enumerate(papers):
            pid = p.get("id", "???")
            arxiv_id = p.get("arxiv_id")
            doi = p.get("doi")

            if not arxiv_id and not doi:
                all_issues.append(f"⬜ [{pid}] Skipped — no arxiv_id or doi")
                continue

            issues = verify_paper(p, auto_fill=args.auto_fill)
            all_issues.extend(issues)

            # Progress
            if (i + 1) % 5 == 0:
                print(f"  ... {i+1}/{len(papers)} done")

    # Save if auto-fill
    if args.auto_fill:
        save_catalog(catalog, Path(args.catalog))
        print(f"\n💾 Catalog saved with auto-filled metadata")

    # Report
    print(f"\n{'='*60}")
    print(f"📋 Verification Report")
    print(f"{'='*60}")

    errors = [i for i in all_issues if i.startswith("❌")]
    warnings = [i for i in all_issues if i.startswith("⚠️") or i.startswith("🔴")]
    info = [i for i in all_issues if i.startswith("ℹ️") or i.startswith("⬜")]

    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  {e}")

    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  {w}")

    if info:
        print(f"\nℹ️  INFO ({len(info)}):")
        for i in info:
            print(f"  {i}")

    if not errors and not warnings:
        print("\n✅ No issues found!")

    summary(catalog)


if __name__ == "__main__":
    main()
