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

Add more Concept folders (for example `concepts/tdd/`) as you scale the system.

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
