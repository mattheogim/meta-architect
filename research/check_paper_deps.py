#!/usr/bin/env python3
"""
Pre-implementation paper dependency checker.
Warns if required papers haven't been verified before implementing a feature.

Usage (standalone): python research/check_paper_deps.py <file_path>
Usage (hook):       Called by .claude/settings.json PreToolUse hook
"""

import json
import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
FEATURE_MAP = PROJECT_ROOT / "research" / "paper-feature-map.json"
VERIFIED_DIR = PROJECT_ROOT / "research" / "verified"


def load_feature_map():
    if not FEATURE_MAP.exists():
        return {}
    with open(FEATURE_MAP) as f:
        return json.load(f).get("features", {})


def find_matching_features(file_path: str, features: dict) -> list:
    """Find features whose source_files match the given file path."""
    matches = []
    normalized = file_path.replace(str(PROJECT_ROOT) + "/", "")
    for feature_name, feature_data in features.items():
        for source_pattern in feature_data.get("source_files", []):
            # Match exact path or directory prefix
            if normalized.startswith(source_pattern.rstrip("/")):
                matches.append((feature_name, feature_data))
                break
    return matches


def check_paper_verified(paper: dict) -> bool:
    """Check if a paper has been verified (read and documented)."""
    paper_id = paper.get("id", "unknown")
    verified_file = VERIFIED_DIR / f"{paper_id}.md"
    return verified_file.exists()


def main():
    if len(sys.argv) < 2:
        return

    # Extract file path from tool input
    tool_input = " ".join(sys.argv[1:])

    # Try to extract file_path from the input
    file_path = ""
    if "file_path" in tool_input:
        # Simple extraction - look for file path patterns
        for part in tool_input.split('"'):
            if "/" in part and not part.startswith("{"):
                file_path = part
                break

    if not file_path:
        # Try direct path
        file_path = tool_input.strip().strip('"')

    if not file_path or not any(
        file_path.endswith(ext)
        for ext in [".py", ".ts", ".js", ".json", ".yaml", ".yml"]
    ):
        return

    features = load_feature_map()
    matches = find_matching_features(file_path, features)

    if not matches:
        return

    warnings = []
    for feature_name, feature_data in matches:
        for paper in feature_data.get("required_papers", []):
            if not check_paper_verified(paper):
                paper_id = paper.get("id", "?")
                arxiv = paper.get("arxiv", paper.get("url", "?"))
                sections = ", ".join(paper.get("sections", []))
                why = paper.get("why", "")
                warnings.append(
                    f"  [{paper_id}] arxiv:{arxiv} {sections} -- {why}"
                )

    if warnings:
        print(f"PAPER_CHECK_WARNING: {file_path}")
        print(f"Feature: {matches[0][0]}")
        print("Unverified required papers:")
        for w in warnings:
            print(w)
        print(
            "Run WebFetch on each paper, extract key findings, "
            "then save to research/verified/{paper_id}.md"
        )
        # Exit 0 so the hook warns but doesn't block
        # Change to sys.exit(1) to hard-block implementation without reading


if __name__ == "__main__":
    main()
