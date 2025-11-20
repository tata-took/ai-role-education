#!/usr/bin/env python3
"""ペルソナとDDコンセプトのバトルをシミュレートするスクリプト。

LLM 呼び出し部分は未実装であり、フロー構築と入出力の動作確認にフォーカスする。
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
import sys
from typing import Iterable

import yaml


def call_battle_agent(battle_prompt: str) -> str:
    """
    TODO: ここで OpenAI や他の LLM API を呼び出し、
    battle_prompt を system/user プロンプトとして投げ、
    「対戦結果（Markdownテキスト）」を返す想定。
    今は NotImplementedError でOK。
    """

    raise NotImplementedError


def _load_yaml_text(path: pathlib.Path) -> str:
    text = path.read_text(encoding="utf-8")
    # Validate YAML structure even though we keep original text for output.
    yaml.safe_load(text)
    return text


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


def _build_battle_prompt(persona_text: str, dd_texts: list[tuple[str, str]]) -> str:
    intro = (
        "あなたはAIロール教育エンジンのRouterです。\n"
        "- ペルソナ = クライアント\n"
        "- DD = DocDD / TDD / UXDD / OpsDD などの専門家ロール\n"
        "流れ:\n"
        "1) ペルソナ要約\n"
        "2) ペルソナとして相談内容を1つ生成\n"
        "3) 各DDの意見を順番に提示\n"
        "4) Routerとして統合案を提示\n"
        "5) ペルソナのsuccess_criteria / anti_patternsに基づいて10〜20点で採点\n"
    )

    parts = [intro, "# Persona YAML", persona_text.strip()]

    for dd_id, dd_text in dd_texts:
        parts.append(f"\n# DD Concept: {dd_id}")
        parts.append(dd_text.strip())

    parts.append("\n上記の情報をもとに、1ラウンドのバトル結果を出力してください。")
    return "\n\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--persona-id", required=True, help="Persona ID (e.g., enterprise_regulated_owner)")
    parser.add_argument("--dd-ids", nargs="+", required=True, help="DD Concept IDs (e.g., docdd opsdd riskdd)")
    args = parser.parse_args()

    persona_path = pathlib.Path("personas") / f"{args.persona_id}.yaml"
    if not persona_path.exists():
        print(f"Persona file not found: {persona_path}", file=sys.stderr)
        sys.exit(1)
    persona_text = _load_yaml_text(persona_path)

    dd_texts: list[tuple[str, str]] = []
    for dd_id in args.dd_ids:
        concept_dir = pathlib.Path("concepts") / dd_id
        if not concept_dir.exists():
            print(f"Concept directory not found: {concept_dir}", file=sys.stderr)
            sys.exit(1)

        concept_paths = list(concept_dir.glob("concept_v*.yaml"))
        try:
            _, concept_path = _find_latest_version(concept_paths)
        except FileNotFoundError as exc:
            print(str(exc), file=sys.stderr)
            sys.exit(1)

        dd_texts.append((dd_id, _load_yaml_text(concept_path)))

    battle_prompt = _build_battle_prompt(persona_text, dd_texts)

    try:
        battle_output = call_battle_agent(battle_prompt)
    except NotImplementedError:
        battle_output = battle_prompt

    logs_dir = pathlib.Path("logs") / "battles"
    logs_dir.mkdir(parents=True, exist_ok=True)
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M")
    dd_suffix = "_".join(args.dd_ids)
    log_path = logs_dir / f"{args.persona_id}__{dd_suffix}_{timestamp}.md"

    header = (
        f"# Battle Simulation Log\n"
        f"persona-id: {args.persona_id}\n"
        f"dd-ids: {' '.join(args.dd_ids)}\n"
        f"executed_at: {dt.datetime.now().isoformat(timespec='seconds')}\n\n"
        f"## Battle Output\n"
    )

    log_path.write_text(header + battle_output + "\n", encoding="utf-8")
    print(f"Saved battle log to {log_path}")


if __name__ == "__main__":
    main()
