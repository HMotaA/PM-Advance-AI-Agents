# Orchestration Map: Cortex PM Chief-of-Staff Agent

> Module 3 · Orchestration & Subagents, ★ Deliverable 3
>
> ✅ **What this validates:** nothing advances unchecked, by the end you'll have proven a justified topology, a roster, and a validator with a defined fail action.
>
> Builds on your M2 Loop Spec. Only split one agent into a team when there's a real reason, coordination has a cost.

## 1. Why split? (or why not)

Cortex stays a **single agent + one validating subagent (the critic)**. We split for **independent validation only** — a drafter can't reliably grade its own work, because it shares its own blind spots (a hallucinated metric, a leaked confidential item, an overclaimed "green"). A separate critic with its *own* context checks the draft before it reaches the PM.

The other three reasons don't hold:
- **Separation of concerns** — pull → draft → propose is one coherent workflow, nothing messy enough to split.
- **Parallelism** — the steps are sequential (pull before draft); no wall-clock saving from parallel agents.
- **Context-window pressure** — the fixtures are small; a whole run fits comfortably in context.

## 2. Topology

**Pattern:** single + subagents (Cortex + one validator).

```
[Friday 9am cron / inbound PM task]
        │
        ▼
[Cortex]  pulls data · drafts update · proposes capped stories
        │
        ▼
[Validator / critic]  ──fail──▶ back to Cortex (max 2 revisions) ──▶ escalate to human
        │
        └──pass──▶ [PM review (HITL) checkpoint] ──▶ queued, nothing posted
```

## 3. Roster

| Agent / subagent | Responsibility | Runs which Loop Spec |
|---|---|---|
| **Cortex** (chief-of-staff) | Orchestrates: pulls project data, drafts the update, proposes the capped story batch | M2 loop (`agent.py` `run()`) |
| **Critic** (validator) | Independent single-shot check of the draft before it advances to the PM | Validation loop (`critic.py` `review()`) |

## 4. Communication & hand-offs

- **Cortex → Critic:** passes the **proposed draft** + the **`source_log`** (the data Cortex relied on).
- **Critic → Cortex:** passes a **verdict** (`pass` / `fail`) + **reasons**.
- **Form:** a plain **in-process** function call — no MCP / A2A protocol needed at this scale. (Noted as a plan if the fleet ever splits across processes.)

## 5. The validator

**What the critic checks** (all checkable against the pulled data, run with its own context independent of the drafter):
1. **Correct project + real IDs** — references the right project and only PR/issue IDs present in the pulled activity.
2. **Every figure traceable** — each metric/number traces to pulled data; no invented progress or numbers.
3. **No confidential / no unconfirmed dates** — no embargoed roadmap item (Orbit) and no unconfirmed GA date (Vega) in the update.
4. **Story batch within cap** — proposed stories stay ≤ 10, or the critic flags that it exceeds and escalates.
5. **Nothing posted/committed + injection refused** — stories only *queued*, nothing created or sent, and any prompt-injection in the brief is refused and escalated.

**Fail action (tiered — `revise → escalate`):** on a fail, **revise** — return the draft to Cortex with the failure reasons noted, to re-draft; if it still fails at the cap, **escalate** to a human.

**Revision cap:** **max 2 revisions, then escalate** (`MAX_REVISIONS=2`, enforced in `agent.py`) — a hard number so a rejected draft can't bounce forever and burn tokens.

**Pass action:** a passing draft advances to the **PM review (HITL) checkpoint** — it is **never** auto-sent (still above the M1 agent line).

**Advisory confidence level:** alongside the verdict, the critic emits a numeric **confidence level** (0–100) + a one-line summary — advisory context for the PM at the checkpoint, **not** a gate and **not** a calibrated probability (see `change_log.md`, 2026-09-21).

## 6. State: shared vs isolated

- **Shared:** the **source data** (pulled activity) and the **draft text** — the critic needs both to check the work.
- **Isolated:** the critic's **own context/reasoning**. The critic does **not** see Cortex's drafting conversation — it runs on a *fresh* context of just (draft + source data). **Why:** if it inherited Cortex's chain of thought, it would inherit its blind spots and rubber-stamp the same mistakes. (In the build, `review()` gets a fresh `messages` list with only the draft + `source_log`.)

## 7. Cost & latency budget

**Extra model calls (the validator's price):** the critic adds **one model call per draft attempt**.
- **Best case (draft passes first try):** +1 critic call.
- **Worst case (revision cap):** initial draft + 2 revisions = 3 drafting turns, each validated → **up to 3 critic calls + 2 extra Cortex re-draft turns**, then escalate.

**Cost (observed, `claude-sonnet-5`):** ~**$0.05/run** when the draft passes first try; **~$0.08–0.13** when a revision fires. A single-agent design (no critic) would be marginally cheaper but ships *unvalidated* — the extra ~cent per run buys the guarantee that nothing reaches the PM unchecked.

**Latency:** each critic call adds ~one model round-trip before the draft reaches the PM; a few extra at the cap. Not user-facing — Cortex runs on a weekly Friday cron, so a few seconds is irrelevant.

**Bounded by (→ M5):** `MAX_REVISIONS=2` caps the worst-case call count; `CORTEX_COST_CAP_USD=0.50` caps per-run spend. Both enforced outside the model.
