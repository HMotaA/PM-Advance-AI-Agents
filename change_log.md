# Change Log — Cortex build (PM-Advance-AI-Agents)

Newest on top. Logs notable build/design changes so we can roll back deliberately.
(git is the real rollback mechanism; this log says *which* change to revert and why.)

## 2026-09-21 — Critic emits an advisory "confidence level" (M3)
- **What:** The independent critic (`critic.py` + `CRITIC_SYSTEM`) returns a numeric **confidence level** (0–100) plus a one-line summary, alongside the existing pass/fail verdict + reasons.
- **Why:** Gives the human at the PM-review checkpoint a quick "how confident was the check?" read; flags borderline drafts.
- **Status:** Advisory only — **pass/fail stays the hard gate** (drives revise/escalate). The confidence level is **not** a calibrated probability; treat as a soft signal, never decision-grade.
- **Semantics (chosen: A):** `confidence` attaches to the **verdict** (e.g. 98 = 98% sure the verdict is correct), *not* a draft-quality score — a confidently-rejected bad draft scores high.
- **Rollback:** revert the Step 4 commit, or remove the `confidence`/`summary` keys from `CRITIC_SYSTEM` and the parsing/print in `critic.py` + `agent.py`. Pass/fail behaviour is unaffected.
