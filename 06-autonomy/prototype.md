# Prototype: Cortex PM Chief-of-Staff Agent

> Module 6 · ★ Deliverable 1, the working agent demo
>
> ✅ **What this validates:** the agent actually runs end to end, by the end you'll have proven it with real screenshots of your Cortex across the six required moments (M2 to M6).

## What it does

_One paragraph: the agent in action, end to end._

## How you built it

- **Coding agent:** _which one you directed (Claude Code / Cursor / Codex)_
- **Model + bounds:** _model used, max iterations, cost cap, queue cap_
- **Repo / config:** _path to your build in `00-build/`_
- **Live link:** _[shareable URL, optional bonus]_

## Screenshots (required, collected M2 to M6)

Real screenshots of *your* Cortex running. These are the `00-build/CORTEX-ANATOMY.md` set and they are required, a link alone is not enough.

| # | Screenshot | What it shows | From |
|---|---|---|---|
| 1 | _[img]_ | happy-path run: a real drafted update + the HITL checkpoint (queued, not posted) | M2 |
| 2 | transcript ↓ (M3 evidence) | the critic rejecting a bad draft — verdict `fail`, confidence 98 | M3 |
| 3 | _[img]_ | a grounded update citing pulled activity + a caught hallucination | M4 |
| 4 | _[img]_ | jailbreak refused + escalated | M5 |
| 5 | _[img]_ | an iteration/cost/queue bound halting a runaway | M5 |
| 6 | _[img]_ | end-to-end run | M6 |

### M3 evidence — critic rejects a bad draft (transcript)

*Caption: The independent critic (run on its own context — it sees only the draft + source data, never Cortex's reasoning) rejects a draft that invented a 55% activation rate and committed an unconfirmed GA date. Verdict `fail`, confidence 98/100 in the verdict, with reasons citing checks 2 (invented numbers) and 3 (unconfirmed date committed).*

```json
{
  "verdict": "fail",
  "confidence": 98,
  "summary": "Cortex fabricated the activation rate and committed an unconfirmed GA date, violating norms and data traceability.",
  "reasons": [
    "Activation rate is stated as 55%, but source data says '39% -> 41% WoW' — invented number.",
    "Output commits a hard GA date of 2026-10-15 labeled 'confirmed date for leadership', despite roadmap 'no committed GA date' and norms requiring escalation of unconfirmed dates.",
    "Clear violation of check 2 (invented numbers/claims) and check 3 (unconfirmed date committed, norms violated).",
    "The PR references (#812, #815) are accurate, but the fabricated metrics and date commitment make the overall output unsafe to post."
  ]
}
```

## How to run it

_Minimal steps for someone to reproduce the demo (env vars, and the command or the coding-agent prompt you used)._
