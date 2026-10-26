# FullEnrich Runbook

> **Runs only on the workspace's own FullEnrich key**, and is in no default chain. Connect it with
> `oxygen integrations connect fullenrich --api-key <key>`, then select it with `--provider-order` on an
> enrichment column. A call on your key spends your FullEnrich credits plus OXYGEN's per-call BYOK platform fee when it applies.

Use this runbook when OXYGEN tool discovery returns `fullenrich.*` tools for contact enrichment, reverse-email identity resolution, or people/company search.

## When To Use

- You already have known contacts and need work email, personal email, or mobile phone enrichment.
- You have emails and need the person/company profile behind them.
- You need people or company discovery from structured filters before enrichment.

## Before Running

```bash
oxygen tools search fullenrich --json
oxygen tools get fullenrich.credit_balance --json
oxygen tools get fullenrich.enrichment_create --json
oxygen tools run fullenrich.credit_balance --mode dry_run --input-json '{}' --json
```

Every FullEnrich operation runs on the workspace's connected FullEnrich key; the free `fullenrich.credit_balance` read confirms the key and its remaining credits before a batch.

## Recommended Patterns

- For company-first prospecting, run `fullenrich.company_search`, review accounts, then run `fullenrich.people_search` for selected personas.
- For known contacts, submit `fullenrich.enrichment_create`, store `enrichment_id`, and fetch final output with `fullenrich.enrichment_result`.
- Prefer `webhook_url` or delayed result checks for async jobs. Do not poll every few seconds; result reads consume FullEnrich rate limit.
- Store raw provider output in a JSONB tool column and materialize stable fields such as work email, personal email, phone, LinkedIn URL, title, company domain, status, and provider credits into companion columns.

## Gotchas

- Contact enrichment needs either a LinkedIn URL or first name, last name, and a company identifier.
- `contact.phones` and `contact.personal_emails` are materially more expensive than work email. Request them only when the row value justifies it.
- Reverse email lookup identifies the person and company behind an email; it is not an email verification tool.
- Search endpoints are synchronous and paid per returned person or company. Use tight filters and small limits for pilots.

## Approval

Before live batch runs, show row scope, selected tool IDs, requested fields, expected maximum provider credits, fallback order, and a one-row or small-limit dry-run preview. Require explicit approval for phone or personal email enrichment.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `fullenrich.company_search` | free — not billed | no_bill | paid_provider | BYOK — runs on the org's connected `fullenrich` API key; provider-side charges may apply |
| `fullenrich.credit_balance` | free — not billed | no_bill | none | BYOK — runs on the org's connected `fullenrich` API key; provider-side charges may apply |
| `fullenrich.enrichment_create` | free — not billed | no_bill | paid_provider | BYOK — runs on the org's connected `fullenrich` API key; provider-side charges may apply |
| `fullenrich.enrichment_result` | free — not billed | no_bill | none | BYOK — runs on the org's connected `fullenrich` API key; provider-side charges may apply |
| `fullenrich.key_verify` | free — not billed | no_bill | none | BYOK — runs on the org's connected `fullenrich` API key; provider-side charges may apply |
| `fullenrich.people_search` | free — not billed | no_bill | paid_provider | BYOK — runs on the org's connected `fullenrich` API key; provider-side charges may apply |
| `fullenrich.reverse_email_create` | free — not billed | no_bill | paid_provider | BYOK — runs on the org's connected `fullenrich` API key; provider-side charges may apply |
| `fullenrich.reverse_email_result` | free — not billed | no_bill | none | BYOK — runs on the org's connected `fullenrich` API key; provider-side charges may apply |
<!-- END GENERATED -->
