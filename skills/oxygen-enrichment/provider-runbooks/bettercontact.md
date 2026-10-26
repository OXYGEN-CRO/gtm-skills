# BetterContact Runbook

Use this runbook when OXYGEN tool discovery returns `bettercontact.*` tools for lead discovery, work-email enrichment, or mobile-phone enrichment.

## When To Use

- You need email or phone enrichment for known contacts and want BetterContact's async waterfall.
- You need lead discovery from company, people, title, seniority, location, or technology filters.
- You want provider-reported `credits_consumed` and `credits_left` visible on the terminal result.

## Before Running

```bash
oxygen tools search bettercontact --json
oxygen tools get bettercontact.enrich_lead --json
oxygen tools get bettercontact.enrichment_create --json
oxygen billing balance --json
```

Inspect the descriptor for required inputs, credit posture, and whether the caller wants a single-row create-and-poll call or explicit async create/result calls.

## Limits

- BetterContact publishes a shared account/API-key limit of 60 requests per minute across all endpoints.
- BetterContact enrichment create accepts 1-100 contacts per request. OXYGEN table enrichment rows currently use `bettercontact.enrich_lead`, which submits one lead and polls for the terminal result.
- OXYGEN paces BetterContact jobs on the managed account; result polling still counts against the provider's request limit.

## Recommended Patterns

- For table columns, prefer `bettercontact.enrich_lead` when each row needs a self-contained result.
- For bulk workflows where batching is acceptable, use `bettercontact.enrichment_create` with up to 100 contacts and then `bettercontact.enrichment_result`.
- For phone enrichment, prefer rows with a LinkedIn URL and company domain to improve match quality.
- Store raw provider output in a JSONB tool column and materialize stable fields such as email, phone, status, provider, credits consumed, and request id into companion columns.

## Gotchas

- BetterContact is async. A low in-flight cap serializes the whole waterfall, not just request starts.
- Result polling consumes request budget. Large runs should avoid tight polling loops.
- Phone results are materially more expensive than work-email results. Show row scope and maximum credits before live phone enrichment.
- Do not treat `not_found`, `undeliverable`, or missing contact fields as usable outbound data without human review.

## Requested fields and billing

BetterContact is one supplier with an internal waterfall. Compare its email and
phone routes with alternatives returning the same fields and quality. Email
statuses `deliverable`, `valid`, and `verified` are verified; `catch_all_safe`
remains catch-all quality. A person identity in the request does not promise a
complete person profile in the output.

Preview the exact field flags and row count before approving a call. Managed
`enrich_lead` holds that quote until completion, then settles the returned-field
share; no-hits and terminal failures release the hold. Pending or uncertain
outcomes retain it. Resume the recorded request ID through the free result
endpoint rather than submitting the lead again. Polling still consumes quota.

Expected cost depends on hit probabilities; a default quote is a reservation,
not a measured average. Extra Oxygen verification is a separate route and charge.

## Approval

For live batch enrichment, show row scope, selected tool ID, expected maximum provider credits, provider order or fallback position, and a one-row pilot output before running at scale.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `bettercontact.account` | free — not billed | no_bill | none | — |
| `bettercontact.enrich_lead` | 24.5 cr | pre_authorize | paid_provider | async — returns a job handle; poll for completion |
| `bettercontact.enrichment_create` | 24.5 cr | pre_authorize | paid_provider | async — returns a job handle; poll for completion |
| `bettercontact.enrichment_result` | free — not billed | no_bill | none | — |
| `bettercontact.lead_finder_create` | 612.5 cr (example payload; estimate 2–400 cr) | pre_authorize | paid_provider | async — returns a job handle; poll for completion |
| `bettercontact.lead_finder_result` | free — not billed | no_bill | none | — |
<!-- END GENERATED -->

If a Table column requires additional verification, an async supplier result stays incomplete with `verification_required`. Missing original email policy reports `verification_policy_unknown`. After managed settlement, recovery stops with a terminal blocker. `oxygen tables recover-pending <table> --json` retains its `blocked_results`, including the candidate, reason and settled credits; `blocked_results_truncated` identifies a bounded result. The candidate is not a published Table value. Recovery preserves the existing personal-email result. Automatic verification continuation is currently unavailable; do not treat the supplier candidate as a completed verified row.
