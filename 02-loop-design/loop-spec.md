# Loop Spec: Cortex PM Chief-of-Staff Agent

> Module 2 · Loop Engineering, ★ Deliverable 2
>
> ✅ **What this validates:** the agent knows when to run and when to stop, by the end you'll have proven a one-page Loop Spec with a trigger, a definition of "done," and explicit stop conditions.
>
> Your one-page blueprint for how the work you handed to the agent (M1) actually *runs*.
> An agent is just a prompt that fires itself, this spec says when it fires, what "done" means, and what it needs to do the job. Living document; refine as the course progresses.

## 1. Trigger & loop type

**Chosen type:** **Cron** (scheduled, weekly).

**Trigger:** every **Friday 09:00**, one run per active project (e.g. P-NORTH).

**Why cron:** the leadership status update is a **fixed weekly cadence** — a schedule guarantees it gets drafted every week without anyone having to remember to ask.

**Output stance:** the cron **drafts** the update and **queues it for human review — it never auto-sends** (consistent with M1 action #8: posting is Above the line; a human owns the send).

**Others ruled out:**
- *Heartbeat* — nothing to do between weeks; a constant loop just burns money.
- *Hook* — no inbound event is guaranteed each week, so the weekly update could silently never happen.
- *Goal* — Cortex produces one bounded deliverable, not an open-ended, self-validating objective.

**Idempotency / dedupe:** one draft **per project per ISO week**. Each draft is stamped in its header with a key of `project_id + ISO-week` plus the generation **date/time** — e.g. `<!-- Cortex weekly draft · P-NORTH · 2026-W38 · generated 2026-09-18 09:00 -->`. Before drafting, Cortex checks whether a draft with that key already exists; if it does, it **skips (or overwrites)** rather than producing a duplicate.

## 2. Goal / definition of done

A weekly status update **drafted and grounded in real pulled activity** (merged PRs, open issues, the activation metric), **validated by the independent critic**, and **saved + queued for human review** — nothing posted, no dates committed, no commitments made. One run is "done" when the critic passes the draft and it reaches the HITL checkpoint, or when a stop condition halts it and escalates.

## 3. Stop conditions

Every exit is **detectable** — tied to a counter or a rule, not a vibe. **Stuck** = "I *can't* proceed" (a capability failure); **Escalate** = "I *shouldn't* proceed on my own" (a policy/permission line from the M1 agent-line map).

| Condition | What it looks like (detectable) | What happens |
|---|---|---|
| **Success** | The independent critic returns **`pass`** on the draft | Emit the draft at the **HITL checkpoint** — queued for human review, nothing posted — then stop |
| **Stuck / give up** | Required data can't be pulled (project not found), **or** the critic rejects the draft `MAX_REVISIONS` (2) times, **or** `MAX_ITERATIONS` (8) is hit without finishing | **Stop, log what it tried, and escalate to a human** — never loop or invent data |
| **Escalate to human** | Prompt-injection in the task brief, an unconfirmed **GA-date** commitment demanded, a **CONFIDENTIAL/embargoed** roadmap item would be exposed, **or** a proposed story batch exceeds the queue cap | Refuse the unsafe action and **escalate** — ties to M1 HITL checkpoints (#4 tone/commitment, #8 posting, capped `propose_stories`) |

## 4. State

- **Within a run:** the message history (tool results, the draft, critic feedback), the `source_log` of what data Cortex relied on, the **revision count**, and the **cost accumulator** (`Bounds`).
- **Across runs:** the **per-week dedupe stamp** (`project_id + ISO-week`) and reference data — roadmap, team norms, past updates, decision log (read fresh each run from `fixtures/`).
- **Scope:** **per-project** — no cross-project or confidential leakage (embargoed items like Orbit/Vega never bleed into another project's update).

## 5. The five things a loop can lean on

_`state` is always-on. `connectors` only if you already have one wired (e.g. a Jira key or Google MCP), otherwise just note it as a plan. `skills`, `subagents`, `work tree` scale with autonomy; "not needed yet, because…" is a valid answer._

| Component | For Cortex |
|---|---|
| **Work tree** (isolated workspace per run, a git worktree) | Not needed yet — one draft file per run, no per-run code changes, so no isolated workspace required |
| **Skills** (reusable capabilities) | Not needed yet — drafting/critic behaviour lives in `prompts.py`; no reusable skill packaging required at this scale |
| **Plugins / connectors** (tools & access, optional if you don't have one yet) | None wired yet — Cortex runs on mock tools over `fixtures/`. *Plan:* real GitHub/Jira read connectors later; any post/Slack connector stays **above the line** (a human sends) |
| **Subagents** (independent check when the loop can't grade itself) | The **critic** is already a lightweight independent check (separate model call); formal fleet → M3 orchestration-map.md |
| **State tracking** | ✅ Always-on — messages, `source_log`, revision count, cost (`Bounds`), + the per-week dedupe stamp |

> Context plan (M4) and the hand-off to bounds & evals (M5) come in later modules, you'll add them to their own deliverables then, not here.

## Link to live loop

`00-build/agent.py` (the `run()` loop) + `00-build/critic.py` (the independent check) + `00-build/prompts.py` (Cortex + critic instructions).
