# Runs, Refusals And Limits

**Answers: "Why was this refused, what are my limits, and what is this run doing?"**

Use this for a plan or credit refusal, a rate limit, a spend ceiling an Agent or trigger hit, a durable ingestion, or a row count that disagrees with its source. For one wrong cell use [table-trace.md](table-trace.md); for many failures, [error-sweep.md](error-sweep.md); for spend, [optimize-credits.md](optimize-credits.md).

## Operating loop

1. Confirm the workspace (`oxygen whoami --json`, `oxygen db status --json`) and the target's schema (`tables describe`).
2. Run the smallest useful pilot; for durable work inspect the run, its failed items and the billing.
3. Retry only after fixing the bad mapping, credential or input; cancel clearly wrong runs.
4. Report totals, completed, failed, skipped and canceled items, provider attempts, captured and released credits, a sample failure and the next action.

## Durable ingestions

Imports and paged provider reads run as ingestions where every page and item is inspectable. To find a table's ingestion run ids, or everything else that ran on it (column runs, row writes), start with `runs list --table`; `table-runs list` covers action runs only:

```bash
oxygen runs list --table <table> --json
oxygen table-ingestions get <run_id> --json
oxygen table-ingestions items <run_id> --status failed --limit 100 --json
oxygen table-ingestions wait <run_id> --timeout-seconds 600 --json
oxygen table-ingestions retry-failed <run_id> --json
oxygen table-ingestions cancel <run_id> --json
```

Inspect failed items before any retry and fix the descriptor mapping, cursor fields, credentials or row schema first. Table action runs have the same shape (`table-runs list --table <table> --status running`, `get`, `wait`, `pause`, `resume`, `cancel`, `provider-summary`); `table-runs get`, `wait` and `cancel` accept the action run id or its parent workspace run id. A response's trace id narrows the redacted event log: `oxygen observability events --trace-id <trace_id> --json`.

## Plan and credit refusals

Two refusals look alike and are fixed differently:

- `upgrade_required`: the plan lacks the capability, and credits will not help. Every sending account connects only on a plan (`details.capability` `linkedin_connect` for LinkedIn, `sender_connect` for a mailbox, WhatsApp number, X account or phone number): tell the user to subscribe. Relay `details.upgrade_url` (`details.minimum_plan` names the smallest plan for your own provider keys), or, once the human names a plan, run `oxygen billing change --to <plan>` and relay its `approval_url`, the checkout where they pay. Before they choose, read `first_month_offer` from `oxygen billing balance --json`: while it is present, propose its `default_plan` at its first-month price (the $99 plan, $49 for the first month), as the web does. The offer covers monthly plans from $99 up, never the $49 plan or yearly; `billing change` honours the plan named and its `first_month_offer` says whether the offer applies (`applies`) and which `plan` it covers; relay that before they pay. A run on the workspace's own key refused with `byok_requires_paid_plan` is the same answer; on the free plan, keys left from an earlier plan keep running for a grace period (`details.byok_grace_until`).
- `insufficient_credits`: the balance cannot cover the run. With `details.reservation_credits`, it cannot carry a connected account's monthly reservation: relay `details.next_step`, the exact top-up.
- `budget_policy_exceeded` (HTTP 402): a standing budget cap blocked it, with the scope, window, cap, spent and projected amounts. Budgets: [optimize-credits.md](optimize-credits.md).

## What can spend without asking

`oxygen limits show --json` names the workspace's `plan_band` and lists every plan size's limits in `plan_bands` (API rates, storage, default spend ceilings; the `current` row is yours), so "what would a bigger plan change?" is one read. Its `web_url` opens the same view in Settings, Plan limits.

- `spend_safety_defaults`: `trigger_run_credit_ceiling` and `auto_run_batch_credit_ceiling` bound one unattended delivery armed without `--max-credits`. An Agent run spends at most the smaller of its approved `--max-credits` (a trigger's applies per delivery) and the default `agent_run_max_total_credits`.
- **A `--max-credits` above that default is refused with `approval_required`** (`details.approval_kind: agent_ceiling_above_default`) until the user approves the higher number for that one run or trigger. Ask them, then re-run with `--approve-above-default` (MCP `approve_above_default: true`); never set it on your own. `agent_run_approved_max_credits` is the most any approval allows.
- `org_daily_spend_guard` is the daily runaway backstop, also shown by `oxygen budget list --json`.
- Storage: each plan size's `storage.status` is `in_force`, `scheduled` (with `effective_at` and `storage.target`) or `awaiting_capacity_test`; `storage_capacity.usage.largest_table` names the table that fills first, and a `table_row_capacity_exceeded` refusal names the full table.

## Rate limits

`limits show --json` → `api_rate_limits` gives the per-key and per-workspace rates and the tighter limits for table reads, table writes and live tool or AI calls. A call over a limit fails with `rate_limit_exceeded` (HTTP 429, CLI exit 6): wait `error.details.retry_after_seconds` and retry once; `error.details.bucket` names the limit. A spent row budget refuses only multi-row requests until `error.details.reset_at`. Move row-by-row loops into a table run instead of pacing them by hand.

## A monthly cost before building

`oxygen billing estimate --leads <n> --enrich <id> --email-steps <n> --linkedin-steps <n> --mailboxes <n> --linkedin-accounts <n> --json` (MCP `oxygen_billing_estimate`; enrichment ids from `oxygen enrichment catalog --json`) prices a planned motion in one free read. Quote `totals` (expected and worst-case credits, plus any dollar seats), `recommended_plan` (its `monthly_usd` already includes seats) and `limits_hit` with `senders_needed`. Steps count per channel; `summary` restates what was priced, so check it against the request. Its `web_url` opens the same estimate in Settings.

## Charged or reused, per cell

`oxygen tables preview <table> --include-cell-states --json` returns each billed cell's `billing`: `{ creditsUsed, creditsSaved, charged, cacheHit, reusedFrom }`. `charged: false` with `cacheHit: true` means the value was reused from a recent enrichment and billed 0; `creditsSaved` is what reuse avoided.

## Row counts

Prefer table reads for anything user-facing; use tenant SQL only for read-only checks such as exact counts: `oxygen db query --sql 'select count(*) from "workspace"."<physical_table>"' --json` (the physical name is in `tables describe`). When the table and its source disagree, stop and fix or report the import before any enrichment.
