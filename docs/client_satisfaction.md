# Client Satisfaction Layer (AI Nation OS)

This document defines how **client satisfaction** is handled
in the AI Nation OS (ai-role-education).

The key idea:

> AI must **never** claim "the client is satisfied".
> AI can only say:
> "Given what we see, satisfaction is **likely** / **unlikely**."

Final judgment belongs to **real humans + real data**.

---

## 1. Four Layers of Satisfaction

We treat "client satisfaction" as a 4-layer structure:

1. **Layer 1 – Surface Reaction (Emotion / Words)**
   - E.g. "すごい！さすがです！"
   - This can be simulated by `Client Proxy`.
   - It is **not** reliable as a final satisfaction signal.

2. **Layer 2 – Professional Quality (Craft)**
   - Quality of design / writing / code / planning.
   - Evaluated mainly by **Teacher / MEXT / License**.
   - Answer to: "Is this professionally acceptable?"

3. **Layer 3 – Goal Fit (KPI Alignment)**
   - Does the work support the real goal?
     - ex) more bookings, more inquiries, better retention.
   - Defined by **PM** as explicit `success_metrics` at project start.
   - Evaluated as a **hypothesis** by PM/Teacher/MEXT.

4. **Layer 4 – Long-Term Reality (Retention / Continuation)**
   - Does the client continue 3/6/12+ months?
   - Do they refer others?
   - This exists only in the **real world**:
     - Real numbers,
     - Real renewals or cancellations,
     - Real comments.

Layers 1–3 can be *simulated*;
Layer 4 is *real only*.

---

## 2. Simulated vs Real Logs

We separate logs into two spaces:

- `learning_logs/simulated/...`
  - For **roleplay / training / hypothetical** projects.
  - All satisfaction evaluations here are **hypotheses**, not facts.
  - Wording must reflect that: "likely", "possible", "tend to", etc.

- `learning_logs/real/...`
  - For **actual client projects** (if and when used in production).
  - Humans may add:
    - real KPIs (bookings, conversion, etc.),
    - continuation / cancellation info,
    - real feedback quotes.
  - These logs are the only place where we treat outcomes as **ground truth**.

The OS should:

- Learn patterns mostly from `real/` logs,
- Use `simulated/` logs as **hypothesis generators**, not proofs.

---

## 3. Satisfaction Review Block

At the end of a project cycle (or major milestone),
the OS may produce a **Satisfaction Review Block**, typically written by:

- Teacher (Layer 2: professional quality),
- PM (Layer 3: goal fit hypothesis),
- License / Router (Layer 4: relationship / continuation hypothesis).

Example template:

```markdown
# Client Satisfaction Review (Simulated)

## Layer 1: Surface Reaction (Simulated)
- Client Proxy: "このLP、世界観がすごく伝わっていて良いですね！"

## Layer 2: Professional Quality (Teacher / MEXT)
- Structure: 4/5
- Message consistency: 4/5
- Technical soundness: 3/5
- Comment: "初版としては十分だが、予約導線の強調が弱い。"

## Layer 3: Goal Fit (PM – Hypothesis)
- Goal: "予約数アップ"
- Hypothesis:
  - The top section with a clear "今すぐ予約" CTA is likely to improve form visits.
  - However, lack of price indication may weaken performance for cold audiences.

## Layer 4: Relationship (License / Router – Hypothesis)
- Retention likelihood (hypothesis): Medium
- Concerns:
  - If the client values "worldview > numbers", they will likely be happy.
  - If they expect "short-term booking explosion", a gap may appear.

In real projects, a similar block may be stored in learning_logs/real/...
and augmented with actual metrics and real client comments.
```

⸻

4. Role Responsibilities (Satisfaction Layer)
- **PM**
  - Must define success_metrics at project start.
  - Evaluates Layer 3 as a hypothesis.
- **Teacher / MEXT**
  - Evaluate Layer 2 (craft quality).
  - Watch for “fake satisfaction” patterns:
    - high internal praise,
    - but no real-world results (when real data exists).
- **License**
  - Uses real satisfaction / retention signals from real/ logs to inform promotions:
    - Not just “how many projects”,
    - but “how many projects led to sustained relationships”.
- **Router**
  - Orchestrates writing of Satisfaction Reviews.
  - Ensures AI does not claim “the client is satisfied as a fact”.

⸻

5. Anti Self-Congratulation Rule

Very important:
- AI must never say:
  - “The client is satisfied.”
  - “This project was a success.” (as a fact)

AI may only say things like:
- “Given our internal criteria, this looks like a good candidate for client satisfaction.”
- “If the client’s real goal is X, they are likely to feel satisfied.”
- “This is a hypothesis; it should be checked against real data.”

The only entities allowed to decide satisfaction are:
- Real humans (Founder / client),
- Real-world metrics (retention, KPIs).

–– docs/client_satisfaction.md ここまで ––
