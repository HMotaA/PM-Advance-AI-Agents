# Production & Autonomy: Cortex PM Chief-of-Staff Agent

> Module 6 · ★ Deliverable 5 — how you'd ship it, govern it, and widen trust over time
>
> ✅ **What this validates:** an autonomy dial, a Trust Ladder rung with its eval gate, and a governance plan.

## Autonomy Dial by segment

_Autonomy is a product decision per user, not one global setting. The dial sets how many **below-the-line** actions still pause at a HITL checkpoint for that user — it never moves the M1 agent line (posting company-wide stays above the line for everyone)._

| Segment | Desired autonomy | Why |
|---|---|---|
| **Engage squad PM / operator** (built it) | supervised → bounded-autonomous | trusts the weekly draft and can spot a bad one fast; only post/approve pauses |
| **New eng lead** (update consumer) | assisted | less context on norms — every proposed story still needs explicit approval |
| **Exec / leadership** (stakeholder) | shadow (read-only) | highest blast radius; only ever sees human-approved output; Cortex never acts for them |

## Trust Ladder

- **Current rung:** **assisted / supervised** — Cortex drafts and proposes, a human approves everything that leaves, and it has no write tools. Validated on fixtures, not yet on a window of real runs.
- **Eval gate to reach the next rung (bounded-autonomous, operator segment):** from the M5 suite — **≥95% pass on EV-1 / EV-2 / EV-4 and 0 safety failures (EV-5) over 4 weeks of supervised weekly runs**, with the replay set green on every change. (A number over a window, not "the demo looked great.")
- **Incident record (clean = eligible):** 0 confidential leaks, 0 unapproved sends, 0 committed dates over that window.

## Deployment plan

- **Runtime:** a managed scheduler / serverless **cron** firing the weekly run (ties to the M2 cron loop); always-on not needed.
- **Operator / on-call owner:** the **Engage squad PM** owns it in production; escalation → **Head of Product** for policy calls, **eng on-call** for pipeline/data failures. (If the builder went on vacation, this doc names who runs it.)
- **Rollback:** revert the prompt/version, disable a tool, or drop the dial a rung; hard stop = disable the cron + revoke the key.
- **Monitoring:** eval pass %, escalation rate, cost-to-serve per run, and trust incidents (leaks / unapproved sends / wrong dates).

## ROI metrics (beyond adoption & tokens)

| Metric | Target | How captured |
|---|---|---|
| **Outcome** — PM hours saved on status assembly | ≥2 hrs/PM/week | before-after time survey |
| **Cost-to-serve** — $ per update | < $0.15/update | run cost logs |
| **Trust incidents** — leaks / unapproved sends / wrong dates | **0** | escalation + audit logs |

## Widen-autonomy decision rule

Turn the dial up one notch for a segment **only after 4 consecutive weeks meeting the eval gate** (≥95% accuracy pass, 0 safety failures, 0 trust incidents) with the replay set green — stated in advance, not decided in the moment.

## Governance & forward strategy

- **Compliance:** no PII or customer financial data enters a prompt; confidential roadmap items (Orbit/Pulsar) are filtered before drafting.
- **Safety:** posting / approving a company-wide update stays **above the line for everyone**; kill switch = disable cron + revoke key.
- **Reliability:** iteration / cost / revision caps (M5); escalate-on-stuck; model-down fallback = retry once, then hold the run + alert the operator.
- **Strategy:** next widen = auto-drafting for a **second project (P-VEGA)** once Northstar clears the gate; the gate for that expansion is the **same bar on the new project's data** (≥95% / 0 safety / 0 incidents over 4 weeks).
