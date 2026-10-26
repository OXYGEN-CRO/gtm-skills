# Sweep Table-Wide Failures

**Answers one question: "What failed across this table, or why did my run fail?"**

Use this when the problem is not one cell but a pattern: "half my rows didn't enrich", "the run says completed with errors", "nothing is happening". You are triaging a run or a whole table, then deciding whether to requeue. For a single suspicious value, use [table-trace.md](table-trace.md) instead.

Move from the run, to the failed items, to the cause, to the fix.

## 1. Find the run and its verdict

List recent runs for the table and read their status:

```bash
oxygen table-runs list --table <table> --status failed --json
oxygen table-runs list --table <table> --status completed_with_errors --json
```

`--status` accepts `active`, `queued`, `running`, `paused`, `completed`, `completed_with_errors`, `failed`, `canceling`, or `canceled` (it defaults to `active`, so pass the status you are hunting explicitly). Then open the run:

```bash
oxygen table-runs get <run_id> --json
```

Read the counts: `completed` vs `failed` vs `skipped`. A run that is `completed_with_errors` did most of its work — only the failed items need attention. A run that is wholly `failed` usually points at one systemic cause (bad credentials, an unhealthy integration, a wrong input column), not per-row bad luck.

For a Function batch, inspect each caller's Function cell as well as the child
run. Successful rows write their mapped outputs even when another row fails.
A failed row writes an error receipt with its child run, Function row and bounded
failed-item references; populated default outputs such as `no_match` do not
override failed execution. Items canceled with `prior_step_failed` are blocked
dependencies, while an explicit batch cancellation remains authoritative.
Historical terminal callbacks keep their original outcomes: retrying child items
does not reopen already-settled caller callbacks. When those need recovery, preview
a new invocation of the calling Function column scoped to the affected signup rows.

## 2. List the failed items and read the cause

```bash
oxygen table-runs items <run_id> --status failed --json
```

Each failed item carries the row id and the error. Group the errors in your head before acting:

| Error shape | Meaning | Right move |
| --- | --- | --- |
| Same provider/transient/5xx across many rows | A provider blip or rate limit during the run | Requeue (step 3) — the inputs are fine. |
| `no match` / empty result, item `completed` not `failed` | Provider genuinely found nothing for those inputs | Not a failure to retry — the data isn't out there for those rows. |
| Missing/malformed input on every failed row | The source column (e.g. `linkedin_url`, `company_domain`) is empty or wrong | Fix the inputs first; requeuing without inputs just re-fails. |
| `approval_required` / `spend_cap_required` (exit 7) | The run hit the spend gate | A user decision, not a bug — re-run with `--approved --max-credits <n>`. |
| `effect_unknown_approval_required` (exit 7) | An external write may already have landed even though Oxygen did not receive confirmation | Inspect `details.effect_unknown_items`, verify every destination with the user, and never auto-retry. Only after confirmation use `--approved-effect-unknown`. |

## 3. Requeue only the failed items

When the failures were transient and the inputs are sound, requeue just the failed rows — this does **not** re-run the rows that already succeeded:

```bash
oxygen table-runs retry-failed <run_id> --json
```

Requeuing a paid run reserves credits again for the retried rows, so confirm scope with the user first if the run spends. If the same items fail a second time with the same cause, stop retrying — the cause is not transient; treat it as an input or integration problem.

If the command returns `effect_unknown_approval_required`, stop. Its details
return the exact count plus a bounded ambiguous item/row/step/context sample;
inspect the run's full failed-item list too. After a human verifies each
external destination and confirms replay is safe, re-run once with:

```bash
oxygen table-runs retry-failed <run_id> --approved-effect-unknown --json
```

The server records that acknowledgement in the run event stream. Do not infer
approval from the original spend cap and do not add this flag to unattended code.

## 4. Widen to the whole workspace

If failures span more than one table or run — "everything is stuck" — check the background worker's failure feed for the org:

```bash
oxygen worker failures --json
oxygen worker failures --queue actions --json      # or: ingestions
```

This lists failed background action and ingestion items across the organization, not just one run. A pile-up here (many stale/failed items) is a worker- or integration-level problem, not a per-run one.

## 5. Read the operational event log

For the "why" behind failures — including provider request failures that a run summary abstracts away — read the redacted operation events:

```bash
oxygen observability events --status failed --json
oxygen observability events --run-id <run_id> --json          # scope to one run
oxygen observability events --type provider_request --status error --json
```

`--source` (`cli`, `web`, `mcp`, `provider`), `--trace-id`, and `--type` (`operation` or `provider_request`) narrow further. This is the closest thing to a server-side log the product exposes to a customer.

**Epistemic honesty:** `observability events` is *redacted* — it shows operation shape, status, provider, and trace ids, not full request/response bodies or secrets. It answers "what class of thing failed and how often", not "paste me the raw upstream error". If that isn't enough to resolve a genuine product bug, file it: `oxygen support file` / `oxygen_support_ticket_create`.

## Deep-link guidance

- **A run** → the `web_url` from `table-runs get` (`https://oxygen-agent.com/tables/<table>/runs/<run_id>`) — the web view shows per-item status and errors visually.
- **The table** → `https://oxygen-agent.com/tables/<table>`.

Surface the returned link; don't hand-assemble one you didn't get back.

## MCP equivalents

| CLI | MCP tool |
| --- | --- |
| `oxygen table-runs get` | `oxygen_table_runs_get` |
| `oxygen table-runs items` | `oxygen_table_runs_items` |
| `oxygen table-runs retry-failed` | `oxygen_table_runs_retry_failed` |
| `oxygen worker failures` | `oxygen_worker_failures` |
| `oxygen observability events` | `oxygen_observability_events` |

(`table-runs list` has no MCP twin — list runs from the table view or a `table-runs get` on a known run id when driving over MCP.)

## Combines with

- **[table-trace.md](table-trace.md)** — once the sweep isolates one representative failing row, trace that single cell/row end to end.
- **[optimize-credits.md](optimize-credits.md)** — when requeuing repeatedly is burning credits, switch to the cost lens before you retry again.
- **[runs-and-limits.md](runs-and-limits.md)** — when the failure is a plan, credit or rate-limit refusal rather than a provider error. A repeatable product failure becomes a report through the `oxygen-feedback` skill.
