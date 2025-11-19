# ai-role-education

This repository contains the first version of an **AI role education system**.
It simulates a vocational school + education ministry + licensing office flow
for teaching AI agents actionable work concepts and certifying them through a
repeatable, auditable process.

The scope of `v1` focuses on three roles:

- **teacher_agent** — drafts a Concept by following a strict YAML template.
- **mext_agent** — reviews a Concept using eight scoring axes and decides whether
  it should be approved, revised, or rejected.
- **license_agent** — designs a License definition for each approved Concept so
  other AI roles can be granted a measurable credential.

## Repository structure

```
ai-role-education/
├─ README.md
├─ concepts/
│  └─ docdd/
│     ├─ concept_v1.yaml
│     ├─ mext_review_v1.yaml
│     └─ license_v1.yaml
├─ roles/
│  ├─ teacher_agent_prompt.md
│  ├─ mext_agent_prompt.md
│  └─ license_agent_prompt.md
├─ flow/
│  └─ education_flow_v1.md
├─ scripts/
│  └─ run_flow.py
└─ logs/
   └─ education_sessions.md (optional manual logs)
```

## Getting started

1. **Review the prompts** under `roles/`. They are ready-to-use instruction
   templates for each AI role.
2. **Read the education flow** (`flow/education_flow_v1.md`) to understand how
   the teacher → mext → license loop is orchestrated.
3. **Inspect the sample DocDD Concept** in `concepts/docdd/` to see the expected
   YAML shape for Concepts, review logs, and licenses.
4. **Use the helper script** to preview the current state (requires `PyYAML`):

   ```bash
   python scripts/run_flow.py --concept concepts/docdd/concept_v1.yaml --license concepts/docdd/license_v1.yaml
   ```

   The script prints a concise summary and validates that mandatory fields are
   present before you run the agents.

## Current Concept inventory

- **DocDD (Document Driven Development)** — `concepts/docdd/`
  - `concept_v1.yaml` defines the practice of documenting requirements first so
    every stakeholder shares the same references before implementation begins.
  - `mext_review_v1.yaml` records a total score of 14/16 with an **approved**
    decision; it also requests richer anti-pattern mitigations and deeper root
    causes for the failure case in a future revision.
  - `license_v1.yaml` introduces the DocDD license for software development
    teams, starting at 50 points, reviewed every 90 days, and governed by
    detailed scoring, suspension, and revocation rules.

## Operating the education flow

### Adding a new `concept_id`

1. **Prepare**: read the three role prompts in `roles/` and the canonical flow
   description in `flow/education_flow_v1.md` so you understand the required
   YAML structure and review loop.
2. **Draft the Concept (teacher_agent)**: create `concepts/<concept_id>/` and
   author `concept_v1.yaml`, mirroring the DocDD template to fill every section
   with the new practice.
3. **Audit the Concept (mext_agent)**: evaluate the draft against the eight
   scoring axes, write `mext_review_v1.yaml`, and set the decision to approved,
   needs_revision, or rejected. If it is not approved, iterate with the teacher
   until the comments are addressed.
4. **Issue the License (license_agent)**: once approved, produce
   `license_v1.yaml` for the same concept, covering domain, scoring rules,
   validity period, and enforcement conditions.

### Updating an existing `concept_id`

1. **Review the latest files** (`concept_vN.yaml`, `mext_review_vN.yaml`, and
   `license_vN.yaml`) to understand past critiques and licensing constraints.
2. **Draft a revision** (`concept_vN+1.yaml`) that addresses review feedback and
   any newly discovered operational lessons.
3. **Re-run the audit** by creating `mext_review_vN+1.yaml`; loop with the
   teacher stage up to a few times until the decision becomes **approved**.
4. **Update the license** (`license_vN+1.yaml`) only if the Concept changes
   alter its certification requirements, then re-run any scripts or manual
   checks before committing.

## Extending the system

- Implement additional Concepts by cloning the DocDD structure and updating IDs.
- Automate the teacher ↔ mext loop by building CLI tools (for instance, calling
  OpenAI APIs or other orchestration layers) and storing outputs in `logs/`.
- Expand Licenses with richer scoring logic or integrate real usage telemetry.
- Add future actors such as client personas, auto-curriculum builders, and MCP
  integrations when you are ready for v2.

## License

This repository currently focuses on documentation and sample data. Use and
extend it within your AI experimentation projects.
