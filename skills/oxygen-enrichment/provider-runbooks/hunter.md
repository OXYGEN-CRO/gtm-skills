# Hunter Runbook

> **Not in the default chains.** Select it explicitly with `--tool-id` or `--route-id` on a search
> run, or `--provider-order` on an enrichment column.

Use this runbook when OXYGEN tool discovery returns `hunter.*` tools for company discovery, domain-level contact discovery, work-email lookup, email verification, or Hunter account credit checks.

## When To Use

- You need a domain-first contact list for a known company.
- You have a specific person and need a likely work email from name plus domain, company, or LinkedIn handle.
- You need to validate a known email before outbound activation.
- You want a free domain count or account-credit read before deciding whether to spend Hunter credits.

## Before Running

```bash
oxygen tools search hunter --json
oxygen tools get hunter.domain_search --json
oxygen tools get hunter.email_finder --json
oxygen tools get hunter.email_verifier --json
oxygen tools run hunter.email_count --mode dry_run --input-json '{"domain":"example.com"}' --json
```

Inspect required identity fields, cost posture, result limits, and fallback tools before running a batch.

## Recommended Patterns

- For one known account, run `hunter.email_count` first, then `hunter.domain_search` only when the domain has enough relevant volume.
- For many contacts at one company, prefer `hunter.domain_search` over repeated single-person email finder calls.
- For one high-value person, use `hunter.email_finder` with the most precise identity available: LinkedIn handle, or name plus domain.
- For outbound readiness, run `hunter.email_verifier` on selected email candidates before CRM writes or campaign enrollment.
- Store the raw provider response in a JSONB tool column and materialize stable fields such as email, verification status, score, source domain, title, and credit usage into companion columns.

## Gotchas

- Hunter search and verification endpoints can consume Hunter credits. Use dry runs and row scopes before live execution.
- `hunter.email_verifier` may return an in-progress response. Treat that as pending state, not a final deliverability decision.
- `hunter.domain_search` can return many people for a domain. Set `limit`, `offset`, department, seniority, and verification filters intentionally.
- `hunter.discover` is for company discovery by filters, not for resolving one known domain.
- Hunter does not send messages, enroll campaigns, or write CRM records. Use dedicated CRM or outbound providers for external writes after approval.

## Approval

Before live Hunter batches, show row scope, selected tool IDs, expected maximum provider credits, credential mode, fallback order, and one dry-run preview. Require explicit approval before live verification or search-credit-consuming runs.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `hunter.account` | free — not billed | no_bill | none | — |
| `hunter.combined_find` | 8.5 cr (example payload; estimate 0–8.5 cr) | pre_authorize | paid_provider | — |
| `hunter.companies_find` | 8.5 cr (example payload; estimate 0–8.5 cr) | pre_authorize | paid_provider | — |
| `hunter.discover` | free — not billed | no_bill | none | — |
| `hunter.domain_search` | 8.5 cr (example payload; estimate 0–200 cr) | pre_authorize | paid_provider | — |
| `hunter.email_count` | free — not billed | no_bill | none | — |
| `hunter.email_finder` | 8.5 cr | pre_authorize | paid_provider | — |
| `hunter.email_verifier` | 4.25 cr | pre_authorize | paid_provider | — |
| `hunter.people_find` | 8.5 cr (example payload; estimate 0–8.5 cr) | pre_authorize | paid_provider | — |
<!-- END GENERATED -->
