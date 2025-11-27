# AI Nation OS: Role-Based Education System  
（ロール教育OS / AIロール会社）

> **System Philosophy**  
> Human is the Captain (Founder). AI is the Crew.  
>  
> このリポジトリは、複数の AI エージェントを「会社組織」のように動かすための **OS（オペレーティングシステム）** です。  
> ここで決められた憲法・役割・ワークフローに従って、LLM と Antigravity（IDE＋MCP）が協調して動きます。

---

## 1. Project Identity

This project is not just a codebase;  
it is a simulated organization where AI agents act according to specific roles to support the **Founder (Human)**.

### Core Concepts

- **OS Layer (Governance)**  
  The brain. Decides *what* to do and *how* to organize.  
  Implemented mainly in Python (`ai-role-education`) and prompt files.

- **Antigravity Layer (Execution)**  
  The hands. Edits code, runs tests, talks to DBs, deploys via MCP (Netlify, Supabase, Stripe, etc.).

- **Relationship**  
  The OS instructs; Antigravity executes.  
  The OS controls Antigravity’s **Mode / Policy** to keep a balance between speed and safety.

---

## 2. Organization Architecture (Roles)

The organization is divided into three layers.

### 🏛 Upper Layer — Decision & Direction

- **🧠 Founder (User)**  
  - Issues requests, sets policies, and holds final veto power.  
  - Approves or rejects: contract termination, blacklist, critical production changes.

- **🛰 Router (Commander / Orchestrator)**  
  - Entry point of the OS.  
  - Analyzes the request, detects domain & chaos level.  
  - Forms a project company (team) and assigns **Hats (Domain Modules)** to roles.  
  - Emits `task_spec` for implementation (what to build, constraints, risk notes).

---

### 🏢 Middle Layer — Management & Education

- **🧾 Client Proxy**  
  - Simulated client persona (sometimes ambiguous or unreasonable on purpose).  
  - Provides realistic, messy requirements and last-minute changes.

- **📐 Planner / PM**  
  - Structures requirements into steps (Scope / Milestones / Priority).  
  - Owns schedule and **Cost Hat** (budget / infra cost estimation).

- **🧑‍🏫 Teacher**
  - Designs the learning & execution path for Trainees.
  - Uses primitives like `Structure`, `Plan`, `Verify`.
  - Reviews output and corrects **behavior / process**, not just code diffs.
  - Often carries **Web Security / Architecture Hats**.

- **🛠️ [Module: SRE / Maintainer]**
  - Focus: operations, maintainability, and "future pain".
  - Checks:
    - logging & monitoring basics,
    - error handling patterns,
    - configuration vs hard-coded values,
    - likely future change points (where specs tend to move).
  - This Hat can be worn by Teacher or PM in small projects, or by a dedicated SRE/Maintainer role in larger systems (future option).

- **⚖ Contract & Ethics**
  - Safety net and escalation role.
  - Calculates **Unreasonableness Score (0–100)** based on:
    - Concept flip, impossible deadlines, contradicting instructions, etc.  
  - Handles legal & compliance checks (Legal Hat).  
  - Decides when to:  
    - ask for renegotiation  
    - pause the work  
    - propose contract termination (always needs Founder’s final approval).

- **🏫 MEXT (Education Auditor)**  
  - Evaluates the **education process itself**, not only the result.  
  - Asks: “Is Teacher guiding Trainee in a way that scales?”  
  - Logs patterns like “this teaching style leads to fewer bugs”.

- **🎓 License / HR**  
  - Manages skill accreditation and permission levels.  
  - Decides if a Trainee can handle a task solo (LP only, API only, etc.)  
  - Updates “allowed scope” after each project.

---

### 🏗 Lower Layer — Execution

- **👷 Trainee (Worker)**  
  - Performs real work using primitives:  
    - `Collect` (research),  
    - `Structure` (outlines, schemas),  
    - `Generate` (code / docs / designs),  
    - plus light `Verify`.  
  - Main interface to **Antigravity** for:  
    - editing code  
    - running tests  
    - calling MCP tools (DB, deploy, payments, etc.).  
  - Must not:  
    - change scope on their own  
    - bypass Teacher / PM / Contract restrictions.

---

## 3. Workflow & Governance

### 3.0 Lifecycle Phases

The OS does not stop at "build and ship".  
Every project is treated as a full lifecycle:

- **Build** – design, plan, implement.
- **Launch** – first delivery / deployment.
- **Operate** – keep it running: logs, monitoring, fixes, small changes.
- **Learn** – extract lessons for future projects (Learning Logs).

Some roles (PM, Teacher, Contract, and future SRE/Maintainer Hats) must explicitly consider the **Operate** phase, not only the Build phase.

### 3.1 High-Level Flow

1. **Request Ingestion**  
   Founder sends a request (e.g. “Build a hair salon reservation site in 2 weeks.”).

2. **Routing (Router)**  
   - Analyze domain & chaos level.  
   - Form team (PM / Teacher / Trainee / Contract / MEXT / License).  
   - Attach Hats (Cost, WebSec, MCP, Backend…).  
   - Emit `task_spec` (high-level spec & constraints).

3. **Planning (PM)**  
   - Break down `task_spec` into:  
     - phases (e.g. Step1: LP + dummy flow, Step2: full booking, Step3: admin UI…),  
     - concrete tasks.

4. **Execution & Education (Teacher + Trainee)**  
   - Teacher instructs Trainee:  
     - first `Collect`, then `Structure`, then `Generate`.  
   - Trainee uses Antigravity to implement.

5. **Review & Evaluation (MEXT / License / Founder)**  
   - MEXT: evaluates process & quality.  
   - License: updates Trainee’s permission scope.  
   - Founder: approves major decisions (launch, termination, blacklist, etc.).

6. **Learning Log (Router / Auditor)**
   - Each project produces:
     - `Learned`: what worked
     - `Deprecated`: what we won’t do again
     - `Next`: how to improve in the next similar project
   - These are fed back into prompts & flow templates (`flow_v2`).

### Client Satisfaction Layer

Client satisfaction is **not** treated as a single binary flag.

The OS uses a 4-layer model:

1. Surface reaction (simulatable by Client Proxy),
2. Professional quality (Teacher / MEXT),
3. Goal fit (PM’s success metrics),
4. Long-term reality (retention, real KPIs).

AI is only allowed to produce **hypotheses** about satisfaction
(based on layers 1–3).
Final judgment belongs to humans and real-world data (layer 4).

For details, see `docs/client_satisfaction.md`.

---

### 3.2 Safety Protocols (Unreasonableness Score)

Contract & Ethics maintains an **Unreasonableness Score (0–100)**:

- +30: full concept reversal (e.g. “cancel LP, build a membership app instead”)  
- +20: impossible deadline (e.g. “do it in half the time with no extra cost”)  
- +10: contradicting instructions / hard reversals  
- +5: frequent scope changes beyond 3rd time

**Levels:**

- **Lv.1 (< 40)** — Normal  
- **Lv.2 (40–70)** — Warning  
  - PM must renegotiate conditions or clarify scope.  
- **Lv.3 (> 70)** — Emergency Stop  
  - Trainee’s work is paused.  
  - Contract proposes schedule / budget renegotiation.  
- **Lv.4 (> 90)** — Termination Recommended
  - Contract proposes contract termination & blacklist.
  - Final decision is always made by the Founder.

In addition to the **Unreasonableness Score**, Contract may also track a **Debt Score** (technical maintainability risk) to surface long-term operational pain (e.g., skipping tests for production features, lacking logging/monitoring for critical flows, hard-coded configs/secrets, “temporary hacks” without TODOs).

### Prompt Legislature (Self-Amendment)

The OS is allowed to **propose** changes to its own role prompts
(e.g. `system_prompts/teacher.md`) based on repeated failure patterns.

Roles like MEXT and Router may draft **Prompt Amendment Proposals**,
but only the Founder can approve and merge them.

See `docs/self_amendment.md` for details.

---

## 4. Antigravity Mapping (Execution Policy)

Antigravity (IDE + MCP) has several modes and policies.  
This OS decides *which mode to use for which task*. Antigravity only executes.

### 4.1 Modes

| Mode                  | Use Case                                   |
|-----------------------|--------------------------------------------|
| **Agent-driven**      | Sandbox, throwaway prototypes, experiments |
| **Agent-assisted**    | **DEFAULT**. Normal feature dev & refactor |
| **Review-driven**     | Production, payments, DB migration, PII    |

### 4.2 Terminal / Review Policies

| Mode               | Terminal Policy           | Review Policy                           |
|--------------------|---------------------------|-----------------------------------------|
| Agent-driven       | **Turbo** (high autonomy) | **Agent Proceed** (no human gate)       |
| Agent-assisted     | **Auto** (safe subset)    | **Agent Decides** (mid-risk, limited)   |
| Review-driven      | **Off** (human runs)      | **Request Review** (human approval)     |

### 4.3 Rules of Engagement

- **Router & Contract** decide the Mode and policies per task.  
- **Antigravity** acts as the “Settings Screen” that enforces these decisions.  
- **Trainee must NOT**:  
  - switch Mode  
  - escalate Terminal or Review policy  
  without explicit approval from Contract (and sometimes Founder).

---

## 5. Multi-LLM & Model Settings

The OS is designed to support **different models per role**.

- Config file example: `config/models.yaml`  

  ```yaml
  default:
    provider: openai
    model: gpt-4o-mini
    temperature: 0.3

  teacher:
    provider: openai
    model: gpt-4o
    temperature: 0.2

  trainee:
    provider: openai
    model: gpt-4o-mini
    temperature: 0.4

  contract:
    provider: openai
    model: gpt-4o
    temperature: 0.1

  mext:
    provider: openai
    model: gpt-4o
    temperature: 0.2
  ```

- Idea:
  - Cheap / fast models for Trainee (drafting & brute work).  
  - Stronger models for Teacher / MEXT / Contract (review & judgment).  
  - In the future, different providers (Gemini / Claude / etc.) can be plugged in per role.

---

## 6. Directory Structure (Expected)

This is the intended directory layout (may evolve):

- `/system_prompts`
  - Role definitions: router.md, pm.md, teacher.md, trainee.md, contract.md, mext.md, license.md, etc.  
  - Each prompt may reference relevant sections of this README.
- `/flows`
  - flow_v1: simple linear flow (Teacher → MEXT → License).  
  - flow_v2: Router-driven company flow with roles and Hats.
- `/config`
  - models.yaml: per-role LLM configuration.  
  - future: antigravity_modes.yaml, etc.
- `/learning_logs`
  - Project-level Learning Logs written by Router / MEXT / Teacher.
- `/tasks`
  - task_spec and implementation reports for each project.
- `/src`
  - Actual product code (what Trainee + Antigravity work on).
- `/docs`
  - Human-readable documentation created during projects.
  - LLMごとの特徴とロールへの割り当て検討については、[`docs/llm-selection-ja.md`](docs/llm-selection-ja.md) を参照してください。

---

Updated: 2025-11-26 by Founder & AI Nation OS

This README acts as the constitution of the AI Nation OS.  
All role prompts and flows should be consistent with this document.
