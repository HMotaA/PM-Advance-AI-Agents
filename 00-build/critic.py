"""Independent validator (M3). A separate model call that never saw the drafting
context, so it can't inherit the draft's blind spots. Returns a pass/fail verdict.
The revision cap that stops a critic<->drafter loop lives in `agent.py`.
"""

from __future__ import annotations

import json

from prompts import CRITIC_SYSTEM


def _extract_json(text: str) -> dict:
    """Parse the critic's reply as JSON, tolerating a stray sentence around it."""
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                pass
    return {"verdict": "fail", "reasons": ["critic returned unparseable output"]}


def review(client, model: str, proposed_output: str, source_data: str) -> dict:
    """Return {"verdict": "pass"|"fail", "reasons": [...]} for a proposed output."""
    resp = client.messages.create(
        model=model,
        max_tokens=1024,
        thinking={"type": "disabled"},  # critic is pure JSON classification; no thinking
        system=CRITIC_SYSTEM,
        messages=[
            {"role": "user", "content":
                f"SOURCE DATA Cortex used:\n{source_data}\n\n"
                f"CORTEX PROPOSED OUTPUT:\n{proposed_output}"},
        ],
    )
    text = "".join(b.text for b in resp.content if b.type == "text")
    verdict = _extract_json(text)
    verdict["_usage"] = {"prompt": resp.usage.input_tokens,
                         "completion": resp.usage.output_tokens}
    return verdict
