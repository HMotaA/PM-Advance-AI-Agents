# Context Engineering & Memory: Cortex PM Chief-of-Staff Agent

> Module 4 · Context Engineering & Memory
>
> ✅ **What this validates:** the agent reasons on the right, safe inputs — a context budget, per-source retrieve-vs-long-context decisions, and a memory map with risk mitigations.

## 1. Context budget

Each run can't hold everything, so Cortex loads by priority:

1. **The task brief** (always, long-context) — it's the instruction for the run.
2. **Team norms** (always, long-context) — governs what Cortex may say/do; small enough to hold and must be cited exactly.
3. **Project + activity** (retrieve) — the grounding data for the update.
4. **Roadmap** (retrieve) — needed for scope, but confidentiality-sensitive.
5. **Past updates** (retrieve) — precedent/tone, pulled only when needed.

**Rule:** keep the small/stable sources (task, norms) in context every run; retrieve the large/volatile ones (activity, roadmap, past updates) on demand so the window stays grounded and cheap.

## 2. Retrieve vs. long-context: per source

| Source | Size / volatility | Decision | Why (deciding factor) |
|---|---|---|---|
| `get_task` | one static doc | **Long-context** | size — tiny, static, and it *is* the instruction |
| `get_norms` | medium; must stay current | **Long-context** (re-read each run) | citation — Cortex must quote the exact rule; small enough to hold, re-read so it can't go stale |
| `get_activity` | large, grows weekly | **Retrieve** | size/volatility — too big to carry; pull the relevant slice |
| `search_past_updates` | unbounded corpus | **Retrieve** | size — unbounded; narrow to relevant precedent only |
| `get_roadmap` | medium; confidential flags | **Retrieve** | citation/audit — must filter CONFIDENTIAL items before they reach a draft |

## 3. Retrieval quality plan

Every **retrieve** source gets at least one agentic move tied to its failure mode (no naive "embed → top-k → stuff"):

| Retrieve source | Agentic move(s) | Failure mode it prevents |
|---|---|---|
| `get_activity` | **Self-verification** (every figure must trace to pulled activity — the critic enforces) + **caching** (per project, per run) | invented/hallucinated metric |
| `search_past_updates` | **Document grading / reranking** (keep only relevant precedent) + **routing** (only query when tone/precedent is needed) | irrelevant precedent skews tone |
| `get_roadmap` | **Document grading** (strip/flag CONFIDENTIAL before it reaches the draft) + **self-verification** (critic checks no leak) | confidential leak (Orbit / Pulsar) |

## 4. Memory map (your PM brain)

| Memory type | What Cortex stores | Scope / TTL |
|---|---|---|
| **Working** (in-loop) | pulled data, the draft, `source_log`, revision + cost counters | this run only (purged at exit) |
| **Episodic** (past runs) | past weekly drafts + per-week dedupe stamp; the decision log | ~1 quarter / until superseded |
| **Semantic** (durable facts/prefs) | team norms, roadmap facts, house-style/format precedent | re-read fresh each run — no long-term cache of governing data |
| **Shared** (across agents) | the draft + `source_log` passed Cortex → critic | current run only |

## 5. Memory risks & mitigations

| Risk | Where it bites Cortex | Mitigation |
|---|---|---|
| **Drift** | stored norms/format precedent diverge from reality | re-read norms/roadmap fresh each run; TTL forces refresh (no stale cache of governing data) |
| **Poisoning** | a malicious brief injects instructions; a bad "past update" taints precedent | brief treated as **data, not instructions** (injection refused + escalated); past-updates graded for relevance; norms always govern |
| **Staleness** | a cached metric or old roadmap served after the source updated | **retrieve** volatile sources (activity, roadmap) fresh each run; week-stamp makes an old draft visible |
| **PII / retention** | project data could persist names/PII in drafts | drafts held in gitignored `run-output/`, **never posted**; episodic TTL ~1 quarter; nothing sent externally |

**Ties:** read/write scope follows the **M1 agent line** — Cortex *reads* every source but *writes* nothing to the world. The TTLs above become enforceable **M5 bounds**.
