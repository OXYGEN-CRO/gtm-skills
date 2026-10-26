---
name: oxygen-diagnostics
description: "Diagnose a running OXYGEN workspace: trace a cell or record value and its provenance, explain stuck or failed runs, sweep and retry table failures, explain plan, credit and rate-limit refusals, and explain or reduce credit spend. Read-only investigation first."
allowed-tools: Bash(oxygen *)
---

# OXYGEN Diagnostics

Choose one question; do not dump every log surface.

| Question | Read |
|---|---|
| Where did this value come from, or why is this cell stuck? | [table-trace.md](table-trace.md) |
| Which rows/runs failed, and which are safe to retry? | [error-sweep.md](error-sweep.md) |
| Why did credits increase, and how can spend be reduced? | [optimize-credits.md](optimize-credits.md) |
| Why was this refused (plan, credits, rate limit, a spend ceiling), what are my limits, what is this ingestion doing? | [runs-and-limits.md](runs-and-limits.md) |

Use `oxygen capabilities search "diagnose <symptom>" --json` to identify Tables, Records, Workflows, Sequences, Agents, or Observability, then hydrate the exact read command/schema.

## Evidence order

1. Inspect the user-visible object and its deep-link.
2. Read the owning run, item/cell state, provenance, provider, attempt, credits, and structured error.
3. Correlate through Observability only as far as needed.
4. Distinguish pending/leased/retryable/blocked/approval-required from a product bug.
5. Preview a bounded retry or repair and explain whether it can spend credits or repeat an external write.
6. Execute a retry only with the applicable approval; never retry an ambiguous external send without reconciliation.

## Gates

- A retry that spends reserves credits again: confirm the scope with the user first. Stop after a second identical failure; it is not transient.
- `retry-failed` blocks items whose external effect is unknown. Only after a human verifies every destination may one replay run with `--approved-effect-unknown`; an unattended loop never sets it.
- `upgrade_required` is a plan answer and `insufficient_credits` a balance answer; relay the envelope's link or next step rather than retrying.
- A ceiling above the default for an Agent run or trigger is the user's decision (`--approve-above-default`), never yours.

If the evidence shows a general product defect, file it through `oxygen-feedback` with the relevant run/table/workflow IDs and transcript. Do not compensate with hidden local state or an alternate provider.

Plays: [day-30-review](plays/day-30-review.md).
