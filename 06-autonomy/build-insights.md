# Build Insights: Cortex PM Chief-of-Staff Agent

> Module 6 · ★ Deliverable 4 — what you learned building it
>
> ✅ **What this validates:** the friction, the learning, and the aha that changes how you'd design your next agent.

## Friction

- **Porting the starter from OpenAI to Anthropic.** The build shipped OpenAI-wired; moving to Claude meant rewriting the tool-call shape (flat `input_schema`, `tool_use`/`tool_result` blocks, system as a top-level param) and the token accounting — a real change, not a key swap.
- **A provider-specific gotcha:** Sonnet runs *adaptive thinking by default*, which ate the critic's `max_tokens` budget and truncated its JSON verdict → flaky "unparseable" failures. Fix: disable thinking on the critic (it's pure classification).
- **Account plumbing:** an org-level API key was rejected (needed a **workspace-scoped** key), and the account later ran out of credits mid-lab.

## Learning

The two or three things I now understand about shipping agents that I didn't before:
1. **The agent line is enforced in *tools*, not prompts.** Cortex can't post because there is no post tool — not because the prompt asks it nicely. Capability is removed, not discouraged.
2. **Bounds must live *outside* the model.** A counter, a budget, a credential scope — if the model can talk its way past it, it isn't a bound. The iteration/cost/revision caps are the real safety, not the system prompt.
3. **An independent critic is what lets you trust output without reading every word** — but only if it runs on its *own* context, or it inherits the drafter's blind spots.

## Aha moment

**"Capability is not permission"** — and the sharper corollary: **a bound (a cap + an approval gate) is what shrinks an action's blast radius.** The same action (`propose_stories`) is high-risk without the cap + human gate and low-risk with them. Risk is a property of the *guardrails*, not just the action.

## What you'd do differently

- **Write the eval suite in M1, not M5.** If the trajectory evals had existed from the start, every module's changes (the Anthropic port, the confidence level) would have been regression-tested instead of eyeballed.
- **Tune the cost cap down** from the generous $0.50 toward ~$0.15 once a week of real runs confirms typical spend, with the daily account cap as the real backstop.
- **Add the advisory confidence level earlier** — it made borderline drafts easier to triage at the checkpoint.
