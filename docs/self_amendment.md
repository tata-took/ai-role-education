Self-Amendment: Prompt Legislature (National Diet)

This document defines how the AI Nation OS can propose
self-amendments to its own system prompts.

The goal:

Let the OS say:
“Given recent failures, we should change line X in teacher.md to Y.”

Final approval always belongs to the Founder.

⸻

1. When to Propose Amendments

Typical triggers:
- Repeated mistakes of the same kind by a role (e.g. Trainee always skipping Collect).
- MEXT finding systemic issues in education patterns.
- Contract seeing the same type of risk ignored by PM / Teacher.
- Router noticing that:
  - a role frequently misunderstands its scope,
  - or the current prompt encourages bad patterns.

In such cases, the OS may initiate an Amendment Proposal.

⸻

2. Amendment Proposal Format

An amendment proposal should look like a small pull request.

Suggested format:

# Prompt Amendment Proposal

- Target role: Teacher
- Target file: `system_prompts/teacher.md`
- Location (approx): Section "Process Flow", bullet about `Generate`

## Problem (Observation)

- In recent projects:
  - Trainee often jumps into `Generate` (coding) without enough `Collect` or `Structure`.
  - This leads to many reworks and misunderstandings.

## Root Cause (Hypothesis)

- Teacher’s prompt currently says:
  - "You may let Trainee start Generate when they seem ready."
- This wording is vague and invites early coding.

## Proposed Change

**Before:**

> You may let Trainee start `Generate` when they seem ready.

**After:**

> Require Trainee to:
> - finish at least one round of `Collect`,
> - produce a `Structure` artifact that you approve,
> before they are allowed to start `Generate` on any non-trivial task.

## Expected Effect

- Fewer premature coding attempts,
- Clearer checkpoints,
- Better habit of "Collect → Structure → Generate".

These proposals may be:
- Logged under learning_logs/amendments/,
- Or surfaced to the Founder through the UI / console.

⸻

3. Roles in the Amendment Process
- **MEXT / Education Auditor**
  - Detects patterns in education failures.
  - Often the one to write Problem and Root Cause.
- **Router**
  - Can aggregate signals from multiple projects.
  - Can initiate or co-author proposals, especially when the issue spans multiple roles.
- **Contract**
  - May suggest changes related to:
    - Unreasonableness Score,
    - Debt Score,
    - risk communication wording.
- **Founder**
  - The only one who can:
    - approve (merge),
    - reject,
    - or modify proposed amendments.

⸻

4. Human-in-the-Loop is Mandatory

Even if the OS proposes a strong amendment,
no system_prompt should be auto-edited without Founder approval.

Reason:
- Prompts are part of the “Constitution”.
- Automatic self-editing without oversight can:
  - lock in new bad patterns,
  - gradually drift away from Founder’s intent.

The safe pattern is:
1. OS writes an Amendment Proposal (markdown).
2. Founder reviews:
   - Problem,
   - Root Cause,
   - Proposed Change.
3. Founder applies the change manually or via a simple merge workflow.

⸻

5. Future Automation Ideas (Optional)

In the future, this flow could be automated via:
- A CLI or script like:
  - scripts/propose_prompt_amendments.py
  - That:
    - reads recent logs,
    - asks MEXT/Router to produce proposals,
    - saves them under learning_logs/amendments/.

But for now, the key is:
- The OS understands how to talk about prompt changes,
- And roles like MEXT/Router know they are allowed to propose them.

–– docs/self_amendment.md ここまで ––
