# Agent Line Map: Cortex PM Chief-of-Staff Agent

> Module 1 · The Agent Line
>
> ✅ **What this validates:** every risky action has a clear owner, by the end you'll have proven an above/below-the-line map with HITL checkpoints, scored on reversibility, blast radius, and measurability.

## The workflow, decision by decision

List every discrete decision or action in your agent's workflow, then score each one and place it **above** the line (a human owns it) or **below** (the agent owns it). Borderline calls get an HITL checkpoint.

| Decision / action | Reversibility (H/M/L) | Blast radius (H/M/L) | Measurability (H/M/L) | Above / Below | HITL? |
|---|---|---|---|---|---|
| Pull project state + recent GitHub/Jira activity | H | L | H | Below | — |
| Decide which pulled context is relevant | H | L | H | Below | spot-check |
| Draft the weekly leadership status update | H | L | H | Below | spot-check |
| Decide tone / commitment level (green vs. yellow, date language) | L | H | H | HITL | required |
| Flag at-risk items / raise an escalation | H | L | M | Below | spot-check |
| Choose what to escalate to a human | H | L | M | Below | spot-check |
| Propose next sprint's stories from the PRD (within cap) | H | L | H | Below | ✓ approval |
| Post the update to a channel / approve a company-wide message | L | H | H | Above | required |

**Reading the scores:** Reversibility is *how easily undone* — H = easy to undo, L = hard/impossible to undo. Blast radius is *how much damage before someone catches it*. Measurability is *can you tell after the fact whether it was right*.

## Agent anatomy (sketch)

- **Model:** `claude-sonnet-5` as the default fast model for the drafting loop and the independent critic; escalate to a frontier model (`claude-opus-5`) for high-stakes judgment or when the critic repeatedly rejects a draft (ambiguous norms, a borderline confidential call).
- **Tools:** read-only lookups — `get_project`, `get_activity`, `search_past_updates`, `get_roadmap`, `get_norms` — plus `propose_stories` (queues a capped batch for human approval, creates nothing). **Deliberately absent:** any `post_update`, `create_issue`, `merge_pr`, or `commit_ship_date` tool. The line is enforced in the tool list, not by the prompt.
- **Memory:** persists across runs — roadmap, team norms, decision log, past updates (reference data read each run). Purged — per-run drafting context and scratch reasoning.
- **Loop:** _placeholder, defined in M2 loop-spec.md_
- **Bounds:** _placeholder, defined in M5 bounds-and-evals.md_ (cost cap, iteration cap, revision cap, and the story-queue cap already live in code)
- **Evals:** _placeholder, defined in M5 bounds-and-evals.md_

## The golden rule, applied

_One sentence per decision, naming the deciding axis._

- **Pull project state + activity — Below:** high to reverse, low blast radius, high to verify — deciding factor: blast radius (reading data harms no one).
- **Decide relevant context — Below (spot-check):** high to reverse, low blast radius (any leak is caught at the post gate and by the critic), high to verify from the source log — deciding factor: measurability.
- **Draft the weekly update — Below (spot-check):** high to reverse, low blast radius because it's an unposted draft, high to verify against pulled data — deciding factor: blast radius.
- **Decide tone / commitment level — HITL (required):** low to reverse because a commitment can't be un-heard once leadership anchors on it, high blast radius, high to verify — deciding factor: reversibility.
- **Flag at-risk / escalation — Below (spot-check):** high to reverse, low blast radius since over-flagging is safe and misses are caught at review, medium to verify — deciding factor: blast radius.
- **Choose what to escalate — Below (spot-check):** high to reverse, low blast radius because escalating hands control *to* a human, medium to verify — deciding factor: blast radius.
- **Propose story batch (capped) — Below (mandatory approval):** high to reverse, low blast radius held down by the item cap and the human-approval gate, high to verify against the PRD — deciding factor: blast radius.
- **Post / approve company-wide — Above (required):** low to reverse because you can't un-send it, high blast radius, high to verify — deciding factor: reversibility.

## Hardest call

**Propose next sprint's stories (capped) — Below or HITL?**

My first instinct was that proposing a batch of stories was a **high blast radius** action — Cortex reaching into sprint planning and shaping real work felt dangerous. What changed my mind was looking at what actually happens: `propose_stories` **creates nothing**. Nobody has read or acted on the stories yet — they sit queued until a human approves them, and even then they're capped at 10. So the realized blast radius is effectively **zero** until a person opts in.

That reframed it: the action is safe for Cortex to own (**Below the line**), *but only because* of the approval gate and the cap. Remove the human approval and the same action would jump toward Above, because the stories would become real committed work with no brake. So I placed it **Below with a mandatory HITL approval checkpoint** — and the single axis that settled it was **blast radius**, once I scored the *gated* action rather than the action I imagined.

_The bigger lesson: a bound (the cap) and a checkpoint (the approval gate) are what shrink an action's blast radius — the same action is a different risk with and without them._
