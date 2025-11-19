#!/usr/bin/env python3
"""Lightweight helper to preview the teacher → mext → license flow."""

from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required to run this script") from exc

REQUIRED_CONCEPT_FIELDS = [
    "id",
    "name",
    "definition",
    "usage_context",
    "decision_axes",
    "primary_roles",
    "anti_patterns",
    "evaluation",
    "examples",
    "relations",
]


def load_yaml(path: pathlib.Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):  # pragma: no cover
        raise ValueError(f"YAML at {path} is not a mapping")
    return data


def validate_concept(concept: Dict[str, Any]) -> List[str]:
    missing = [field for field in REQUIRED_CONCEPT_FIELDS if field not in concept]
    return missing


def summarize_list(label: str, items: List[Any], limit: int = 3) -> str:
    preview = ", ".join(str(item) for item in items[:limit])
    suffix = "" if len(items) <= limit else " …"
    return f"{label}: {preview}{suffix}"


def print_concept_summary(concept: Dict[str, Any]) -> None:
    print("=== Concept ===")
    print(f"ID: {concept.get('id')} | Name: {concept.get('name')}")
    definition = concept.get("definition", {})
    print(f"Summary: {definition.get('summary', 'N/A')}")
    usage = concept.get("usage_context", {})
    print(f"Usage description: {usage.get('description', 'N/A')}")
    axes = concept.get("decision_axes", [])
    if isinstance(axes, list):
        axis_names = [axis.get("name", "?") for axis in axes if isinstance(axis, dict)]
        print(summarize_list("Decision axes", axis_names))
    roles = concept.get("primary_roles", [])
    if isinstance(roles, list):
        print(summarize_list("Primary roles", roles))


def print_license_summary(license_data: Dict[str, Any]) -> None:
    print("\n=== License ===")
    print(f"License ID: {license_data.get('license_id')} (concept {license_data.get('concept_id')})")
    domain = license_data.get("domain", {})
    print(f"Domain: {domain.get('name')} / {', '.join(domain.get('subdomains', []))}")
    print(f"Initial score: {license_data.get('initial_score')} | Review cycle: {license_data.get('validity', {}).get('review_cycle_days')} days")
    positives = license_data.get("scoring_rules", {}).get("positive", [])
    negatives = license_data.get("scoring_rules", {}).get("negative", [])
    if positives:
        print(summarize_list("Positive rules", [p.get('name', '?') for p in positives]))
    if negatives:
        print(summarize_list("Negative rules", [n.get('name', '?') for n in negatives]))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--concept", type=pathlib.Path, required=True, help="Path to concept YAML")
    parser.add_argument("--license", type=pathlib.Path, required=True, help="Path to license YAML")
    parser.add_argument("--review", type=pathlib.Path, help="Optional path to review YAML")
    args = parser.parse_args()

    concept = load_yaml(args.concept)
    missing_fields = validate_concept(concept)
    if missing_fields:
        print(f"Concept is missing required fields: {', '.join(missing_fields)}", file=sys.stderr)
        sys.exit(1)
    print_concept_summary(concept)

    license_data = load_yaml(args.license)
    if license_data.get("concept_id") != concept.get("id"):
        print("License concept_id does not match concept id", file=sys.stderr)
        sys.exit(2)
    print_license_summary(license_data)

    if args.review:
        review = load_yaml(args.review)
        decision = review.get("decision", "?")
        total = review.get("total_score", "?")
        print("\n=== Review ===")
        print(f"Decision: {decision} | Total score: {total}")
        items = review.get("items", [])
        for item in items:
            name = item.get("name")
            score = item.get("score")
            comment = item.get("comment")
            print(f" - [{score}] {name}: {comment}")


if __name__ == "__main__":
    main()
