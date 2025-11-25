#!/usr/bin/env python3
"""教育フロー自動実行スクリプト。

LLM クライアントを差し替えることで、ロールプロンプトを使った
フロー実行をローカルで試せるようにする。
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
import sys
from typing import Iterable

import yaml

from llm_client import DummyEchoClient, LLMClient, get_llm_client, get_model_settings
from role_paths import load_role_prompt


def _complete_with_role(
    role_name: str,
    *,
    client: LLMClient | None,
    system_prompt: str,
    user_prompt: str,
    debug: bool,
) -> str:
    """Resolve model configuration for a role and run completion."""

    settings = get_model_settings(role_name)
    provider = settings.get("provider", "openai")
    model = settings.get("model")
    temperature = settings.get("temperature")

    selected_client = client or get_llm_client(provider)
    if debug:
        client_name = selected_client.__class__.__name__
        print(
            f"[DEBUG] role={role_name} provider={provider} model={model} "
            f"temperature={temperature} client={client_name}"
        )

    return selected_client.complete(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model=model,
        temperature=temperature,
    )


def call_teacher_agent(
    concept_id: str,
    current_concept_yaml: str,
    *,
    client: LLMClient | None,
    output_path: pathlib.Path,
    extra_context: str = "",
    debug: bool = False,
) -> str:
    """Use teacher_agent prompt to propose the next concept version."""

    system_prompt = load_role_prompt("teacher")
    user_prompt = "\n\n".join(
        [
            f"# Concept ID: {concept_id}",
            "## Current Concept YAML",
            current_concept_yaml,
            "## Additional Context",
            extra_context or "(none)",
        ]
    )
    response = _complete_with_role(
        "teacher",
        client=client,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        debug=debug,
    )
    return _parse_or_fallback_yaml(
        response,
        output_path=output_path,
        fallback_yaml=current_concept_yaml,
    )


def call_mext_agent(
    concept_id: str,
    new_concept_yaml: str,
    *,
    client: LLMClient | None,
    output_path: pathlib.Path,
    extra_context: str = "",
    debug: bool = False,
) -> str:
    """Use mext_agent prompt to produce a review YAML."""

    system_prompt = load_role_prompt("mext")
    user_prompt = "\n\n".join(
        [
            f"# Concept ID: {concept_id}",
            "## Concept Draft",
            new_concept_yaml,
            "## Additional Context",
            extra_context or "(none)",
        ]
    )
    response = _complete_with_role(
        "mext",
        client=client,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        debug=debug,
    )
    fallback = _dump_yaml_string({"concept_id": concept_id, "status": "pending"})
    return _parse_or_fallback_yaml(response, output_path=output_path, fallback_yaml=fallback)


def call_license_agent(
    concept_id: str,
    mext_review_yaml: str,
    *,
    client: LLMClient | None,
    output_path: pathlib.Path,
    extra_context: str = "",
    debug: bool = False,
) -> str:
    """Use license_agent prompt to produce a license YAML."""

    system_prompt = load_role_prompt("license")
    user_prompt = "\n\n".join(
        [
            f"# Concept ID: {concept_id}",
            "## MEXT Review",
            mext_review_yaml,
            "## Additional Context",
            extra_context or "(none)",
        ]
    )
    response = _complete_with_role(
        "license",
        client=client,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        debug=debug,
    )
    fallback = _dump_yaml_string({"concept_id": concept_id, "license": "TBD"})
    return _parse_or_fallback_yaml(response, output_path=output_path, fallback_yaml=fallback)


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


def _parse_or_fallback_yaml(text: str, *, output_path: pathlib.Path, fallback_yaml: str) -> str:
    """Parse LLM output as YAML or store a draft and return fallback."""

    try:
        parsed = yaml.safe_load(text)
    except yaml.YAMLError:
        draft_path = output_path.with_name(output_path.stem + "_draft" + output_path.suffix)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        draft_path.write_text(text, encoding="utf-8")
        return fallback_yaml

    return _dump_yaml_string(parsed)


def _format_stage_path(template: str, *, concepts_root: str, concept_id: str, version: int) -> pathlib.Path:
    next_version = version + 1
    resolved = template.replace("{concepts_root}", concepts_root)
    resolved = resolved.replace("{concept_id}", concept_id)
    resolved = resolved.replace("{n+1}", str(next_version))
    resolved = resolved.replace("{n}", str(version))
    return pathlib.Path(resolved)


def _load_inputs(paths: list[pathlib.Path], generated_artifacts: dict[pathlib.Path, str]) -> list[str]:
    texts: list[str] = []
    for path in paths:
        if path.exists():
            texts.append(path.read_text(encoding="utf-8"))
            continue
        if path in generated_artifacts:
            texts.append(generated_artifacts[path])
            continue
        latest_text = _find_latest_existing(path, generated_artifacts)
        if latest_text is not None:
            texts.append(latest_text)
            continue
        texts.append(f"(missing input: {path})")
    return texts


def _find_latest_existing(path: pathlib.Path, generated_artifacts: dict[pathlib.Path, str]) -> str | None:
    match = re.match(r"(.+)_v(\d+)(\.[^.]+)$", path.name)
    if not match:
        return None

    prefix, _, suffix = match.groups()
    version_pattern = re.compile(rf"{re.escape(prefix)}_v(\d+){re.escape(suffix)}$")
    latest_version = -1
    latest_text: str | None = None

    for candidate, text in generated_artifacts.items():
        candidate_match = version_pattern.match(candidate.name)
        if candidate_match:
            version = int(candidate_match.group(1))
            if version > latest_version:
                latest_version = version
                latest_text = text

    for candidate in path.parent.glob(f"{prefix}_v*{suffix}"):
        candidate_match = version_pattern.match(candidate.name)
        if candidate_match:
            version = int(candidate_match.group(1))
            if version > latest_version and candidate.exists():
                latest_version = version
                latest_text = candidate.read_text(encoding="utf-8")

    return latest_text


def _invoke_generic_stage(
    *,
    stage_id: str,
    role_prompt_path: str | None,
    inputs: list[pathlib.Path],
    outputs: list[pathlib.Path],
    generated_artifacts: dict[pathlib.Path, str],
    client: LLMClient | None,
    description: str,
    concept_id: str,
    version: int,
    debug: bool,
) -> None:
    system_prompt = load_role_prompt(stage_id, explicit_path=pathlib.Path(role_prompt_path) if role_prompt_path else None)
    input_texts = _load_inputs(inputs, generated_artifacts)
    user_prompt = "\n\n".join(
        [
            f"# Stage: {stage_id} (v{version})",
            f"Description: {description}",
            "## Inputs",
            "\n---\n".join(input_texts) if input_texts else "(no inputs)",
        ]
    )
    response = _complete_with_role(
        stage_id,
        client=client,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        debug=debug,
    )

    for idx, output_path in enumerate(outputs):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if output_path.suffix == ".yaml":
            fallback = _dump_yaml_string(
                {
                    "concept_id": concept_id,
                    "stage": stage_id,
                    "version": version,
                    "note": "auto-generated placeholder",
                }
            )
            text = _parse_or_fallback_yaml(response, output_path=output_path, fallback_yaml=fallback)
        else:
            text = response
        output_path.write_text(text, encoding="utf-8")
        generated_artifacts[output_path] = text


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--concept-id", required=True, help="Concept ID (e.g., docdd)")
    parser.add_argument(
        "--flow",
        "--flow-config",
        dest="flow_config",
        default="flow/education_flow_v1.yaml",
        help="Flow definition to use (default: flow/education_flow_v1.yaml)",
    )
    parser.add_argument(
        "--llm-provider",
        choices=["dummy", "openai"],
        default="dummy",
        help="LLM provider to use for all roles (default: dummy)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable verbose logging for role-to-model resolution",
    )
    args = parser.parse_args()

    flow_path = pathlib.Path(args.flow_config)
    if not flow_path.exists():
        print(f"Flow file not found: {flow_path}", file=sys.stderr)
        sys.exit(1)

    try:
        flow_config = yaml.safe_load(flow_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:  # pragma: no cover - defensive path
        print(f"Failed to parse flow YAML: {exc}", file=sys.stderr)
        sys.exit(1)

    flow_name = flow_config.get("flow_name", "(unknown flow)")
    flow_version = flow_config.get("version", "(unknown version)")
    print(f"Using flow: {flow_name} v{flow_version} ({flow_path})")

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
    concepts_root = flow_config.get("concepts_root", "concepts")
    generated_artifacts: dict[pathlib.Path, str] = {current_path: current_concept_yaml}
    client: LLMClient | None
    if args.llm_provider == "openai":
        client = get_llm_client("openai")
    else:
        client = DummyEchoClient()

    stage_version = current_version
    final_version = current_version
    for stage in flow_config.get("stages", []):
        stage_id = stage.get("id", "(unknown)")
        print(f"Running stage: {stage_id} (v{stage_version})")

        inputs = [
            _format_stage_path(
                template,
                concepts_root=concepts_root,
                concept_id=args.concept_id,
                version=stage_version,
            )
            for template in stage.get("inputs", [])
        ]
        outputs = [
            _format_stage_path(
                template,
                concepts_root=concepts_root,
                concept_id=args.concept_id,
                version=stage_version,
            )
            for template in stage.get("outputs", [])
        ]
        role_prompt_path = stage.get("role_prompt")
        description = stage.get("description", "")

        if stage_id == "teacher":
            concept_output_path = outputs[0] if outputs else concept_dir / f"concept_v{stage_version + 1}.yaml"
            extra_context = "\n\n".join(_load_inputs(inputs, generated_artifacts))
            new_concept_yaml = call_teacher_agent(
                args.concept_id,
                current_concept_yaml,
                client=client,
                output_path=concept_output_path,
                extra_context=extra_context,
                debug=args.debug,
            )
            concept_output_path.parent.mkdir(parents=True, exist_ok=True)
            concept_output_path.write_text(new_concept_yaml, encoding="utf-8")
            generated_artifacts[concept_output_path] = new_concept_yaml

            for extra_output in outputs[1:]:
                extra_output.parent.mkdir(parents=True, exist_ok=True)
                client_name = client.__class__.__name__ if client else "ConfiguredClient"
                teacher_note = (
                    f"Teacher produced concept v{stage_version + 1} using {client_name}."
                )
                extra_output.write_text(teacher_note, encoding="utf-8")
                generated_artifacts[extra_output] = teacher_note

            stage_version += 1
            current_concept_yaml = new_concept_yaml
            final_version = stage_version
            continue

        if stage_id == "mext":
            mext_output_path = outputs[0] if outputs else concept_dir / f"mext_review_v{stage_version}.yaml"
            input_payloads = _load_inputs(inputs, generated_artifacts)
            extra_context = "\n\n".join(input_payloads)
            mext_review_yaml = call_mext_agent(
                args.concept_id,
                current_concept_yaml,
                client=client,
                output_path=mext_output_path,
                extra_context=extra_context,
                debug=args.debug,
            )
            mext_output_path.parent.mkdir(parents=True, exist_ok=True)
            mext_output_path.write_text(mext_review_yaml, encoding="utf-8")
            generated_artifacts[mext_output_path] = mext_review_yaml
            final_version = stage_version
            continue

        if stage_id == "license":
            license_output_path = outputs[0] if outputs else concept_dir / f"license_v{stage_version}.yaml"
            input_payloads = _load_inputs(inputs, generated_artifacts)
            extra_context = "\n\n".join(input_payloads)
            mext_review_source = ""
            for path, payload in zip(inputs, input_payloads):
                if "mext_review" in path.name:
                    mext_review_source = payload
                    break
            if not mext_review_source:
                mext_review_source = input_payloads[0] if input_payloads else ""
            license_yaml = call_license_agent(
                args.concept_id,
                mext_review_source,
                client=client,
                output_path=license_output_path,
                extra_context=extra_context,
                debug=args.debug,
            )
            license_output_path.parent.mkdir(parents=True, exist_ok=True)
            license_output_path.write_text(license_yaml, encoding="utf-8")
            generated_artifacts[license_output_path] = license_yaml
            final_version = stage_version
            continue

        _invoke_generic_stage(
            stage_id=stage_id,
            role_prompt_path=role_prompt_path,
            inputs=inputs,
            outputs=outputs,
            generated_artifacts=generated_artifacts,
            client=client,
            description=description,
            concept_id=args.concept_id,
            version=stage_version,
            debug=args.debug,
        )

    logs_dir = pathlib.Path("logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_line = f"{dt.date.today()} {args.concept_id} v{current_version}->v{final_version} flow={flow_name} score=TODO/16\n"
    (logs_dir / "education_sessions.md").open("a", encoding="utf-8").write(log_line)

    print(f"Logged session to {logs_dir / 'education_sessions.md'}")
    print(f"Flow complete. Latest concept version: v{final_version}")


if __name__ == "__main__":
    main()
