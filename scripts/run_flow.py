#!/usr/bin/env python3
"""教育フロー自動実行スクリプト。

LLM 呼び出し部分は未実装だが、フローの入出力とバージョン管理を
ローカルで試せるようにする。
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
import sys
from typing import Iterable

import yaml


def call_teacher_agent(concept_id: str, current_concept_yaml: str) -> str:
    """TODO: teacher_agent_prompt.md を使って concept_v{n+1}.yaml を生成する"""

    raise NotImplementedError


def call_mext_agent(concept_id: str, new_concept_yaml: str) -> str:
    """TODO: mext_agent_prompt.md を使って mext_review_v{n+1}.yaml を生成する"""

    raise NotImplementedError


def call_license_agent(concept_id: str, mext_review_yaml: str) -> str:
    """TODO: license_agent_prompt.md を使って license_v{n+1}.yaml を生成する"""

    raise NotImplementedError


def _load_yaml_text(path: pathlib.Path) -> str:
    text = path.read_text(encoding="utf-8")
    # Validate YAML structure even though we keep original text for output.
    yaml.safe_load(text)
    return text


def _dump_yaml_string(data: object) -> str:
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False)


def _find_latest_version(files: Iterable[pathlib.Path]) -> tuple[int, pathlib.Path]:
    version_pattern = re.compile(r"concept_v(\d+)\.yaml$")
    latest_version = -1
    latest_path: pathlib.Path | None = None
    for path in files:
        match = version_pattern.search(path.name)
        if not match:
            continue
        version = int(match.group(1))
        if version > latest_version:
            latest_version = version
            latest_path = path
    if latest_path is None:
        raise FileNotFoundError("No concept_v{n}.yaml found")
    return latest_version, latest_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--concept-id", required=True, help="Concept ID (e.g., docdd)")
    args = parser.parse_args()

    concept_dir = pathlib.Path("concepts") / args.concept_id
    if not concept_dir.exists():
        print(f"Concept directory not found: {concept_dir}", file=sys.stderr)
        sys.exit(1)

    concept_paths = list(concept_dir.glob("concept_v*.yaml"))
    try:
        current_version, current_path = _find_latest_version(concept_paths)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)

    current_concept_yaml = _load_yaml_text(current_path)
    next_version = current_version + 1

    try:
        new_concept_yaml = call_teacher_agent(args.concept_id, current_concept_yaml)
    except NotImplementedError:
        new_concept_yaml = current_concept_yaml
    new_concept_path = concept_dir / f"concept_v{next_version}.yaml"
    new_concept_path.write_text(new_concept_yaml, encoding="utf-8")

    try:
        mext_review_yaml = call_mext_agent(args.concept_id, new_concept_yaml)
    except NotImplementedError:
        mext_review_yaml = _dump_yaml_string({"concept_id": args.concept_id, "version": next_version})
    mext_review_path = concept_dir / f"mext_review_v{next_version}.yaml"
    mext_review_path.write_text(mext_review_yaml, encoding="utf-8")

    try:
        license_yaml = call_license_agent(args.concept_id, mext_review_yaml)
    except NotImplementedError:
        license_yaml = _dump_yaml_string({"concept_id": args.concept_id, "version": next_version})
    license_path = concept_dir / f"license_v{next_version}.yaml"
    license_path.write_text(license_yaml, encoding="utf-8")

    log_line = f"{dt.date.today()} {args.concept_id} v{current_version}->v{next_version} score=TODO/16\n"
    logs_dir = pathlib.Path("logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "education_sessions.md").open("a", encoding="utf-8").write(log_line)

    print(f"Saved {new_concept_path}")
    print(f"Saved {mext_review_path}")
    print(f"Saved {license_path}")
    print(f"Logged session to {logs_dir / 'education_sessions.md'}")


if __name__ == "__main__":
    main()
