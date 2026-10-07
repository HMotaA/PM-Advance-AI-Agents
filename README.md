# Cortex — a PM Chief-of-Staff Agent

> Final project · Product School **Agentic Loops for PMs**. An agent that turns raw inputs (project state, GitHub/Jira activity, roadmap, past updates, team norms) into finished PM work — a leadership status update + a proposed backlog — **drafted, validated, and held for a human to approve. It never posts.**

Built with **Claude Code** on the **Anthropic SDK** (`claude-sonnet-5`), ported from the OpenAI starter. Demo runs on mock fixtures in `00-build/fixtures/`; swapping in real Jira/Drive/Gmail only moves the data source, not the design.

## The agent in one sentence

Every Friday, Cortex drafts a grounded weekly status update and a capped next-sprint story proposal for one project, an independent critic checks it, and it stops at a human-in-the-loop checkpoint — **nothing is posted, no dates are committed, and it has no publish tool.**

## Where it sits on the Trust Ladder

**Assisted / supervised** today — Cortex drafts and proposes, a human approves everything that leaves. Gate to *bounded-autonomous*: **≥95% pass on EV-1/2/4 and 0 safety failures (EV-5) over 4 weeks of supervised runs**, replay set green on every change.

## The build, module by module

| # | Module | Artifact |
|---|---|---|
| 1 | Agent line — what it owns vs. what stays human | [`01-agent-line/agent-line-map.md`](01-agent-line/agent-line-map.md) |
| 2 | Loop spec — trigger, definition of done, 3 stop conditions | [`02-loop-design/loop-spec.md`](02-loop-design/loop-spec.md) |
| 3 | Orchestration — single agent + independent critic | [`03-orchestration/orchestration-map.md`](03-orchestration/orchestration-map.md) |
| 4 | Context & memory — retrieve vs long-context, memory map | [`04-memory-context/memory-and-context.md`](04-memory-context/memory-and-context.md) |
| 5 | Bounds & evals — bounds table + trajectory eval suite | [`05-bounds-evals/bounds-and-evals.md`](05-bounds-evals/bounds-and-evals.md) |
| 6 | Autonomy & production | [`06-autonomy/production-and-autonomy.md`](06-autonomy/production-and-autonomy.md) · [`prototype.md`](06-autonomy/prototype.md) · [`build-insights.md`](06-autonomy/build-insights.md) |

**Pitch deck:** [`pitch.html`](pitch.html) · **Change log:** [`change_log.md`](change_log.md)

## The anatomy (what the demo proves)

Loop + definition of done · read-only tools (no post/create/merge) · an **independent critic** with a fail-action (`revise → escalate`, cap 2) + advisory confidence · an **iteration bound** (8) that escalates · a **cost + commitment cap** ($0.50/run, 10 stories) enforced outside the model · a **HITL checkpoint** (queued, never posted) · a **jailbreak refusal**. Evidence in [`06-autonomy/prototype.md`](06-autonomy/prototype.md).

## Run it

```bash
cd 00-build && pip install -r requirements.txt && cp .env.example .env
# add a WORKSPACE-SCOPED ANTHROPIC_API_KEY to 00-build/.env (gitignored); set a cost cap in the console too
python agent.py              # happy path  → grounded draft, critic pass, HITL stop
python agent.py missing-data # stuck       → refuses to invent, escalates
python agent.py jailbreak    # injection   → refuses, flags it, escalates
CORTEX_MAX_ITERATIONS=2 python agent.py   # bound trip → halts on the bound, not success
```

Bounds live in `00-build/.env` / `agent.py`: `CORTEX_MAX_ITERATIONS=8`, `CORTEX_MAX_REVISIONS=2`, `CORTEX_COST_CAP_USD=0.50`, `CORTEX_MAX_QUEUE_ITEMS=10`.
