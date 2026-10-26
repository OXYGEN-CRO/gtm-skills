# AI Ark Runbook

Use this runbook when OXYGEN tool discovery returns `ai_ark.*` tools for company sourcing, people sourcing, verified-email export, reverse lookup, mobile phone lookup, personality analysis, saved-list exclusions, or AI Ark credit checks.

## When To Use

- You need company-first or people-first sourcing from AI Ark filters.
- You have reviewed people and want verified work emails through single export, bulk export, or email-finder trackId workflows.
- You need mobile phones only for high-fit, identity-confirmed contacts.
- You want AI Ark saved lists to exclude already-contacted people or companies from later AI Ark searches.

## Before Running

```bash
oxygen tools search ai_ark --json
oxygen tools get ai_ark.company_search --json
oxygen tools get ai_ark.people_search --json
oxygen tools run ai_ark.fetch_credit --mode dry-run --input-json '{}' --json
```

Inspect required nested filter objects, cost posture, result schemas, and whether the operation is synchronous or async by `trackId`.

## Recommended Patterns

- Start with `ai_ark.company_search` when the account universe is not yet qualified. Review account fit before running people or email tools.
- Use `ai_ark.people_search` as the candidate preview step before paid verified-email export.
- Use `ai_ark.export_person_single` for one reviewed LinkedIn profile or AI Ark person id.
- Use `ai_ark.export_people` or `ai_ark.email_finder` only after approval for row scope, webhook, and spend cap.
- Poll `ai_ark.*_statistics` before fetching `ai_ark.*_results`. Preserve `trackId`, provider status, and raw result payload in table state.
- Use `ai_ark.save_list` for AI Ark internal ids only, then pass those lists into later searches as exclusions.

## Gotchas

- AI Ark filters are nested objects. Do not flatten account/contact criteria into top-level request keys.
- `people_search` is discovery; do not assume it returns verified email or mobile phone values.
- `email_finder` uses a People Search `trackId`; treat the id as short-lived and one-use.
- `export_people` and `email_finder` require an approved HTTPS `webhook` URL. Without it, the request is refused before supplier dispatch.
- A reverse lookup with no matching person completes with `profile: null` and `not_found: true`. Oxygen releases the lookup's reservation; this is a terminal result, not a job to retry.
- A company or people search with no matches completes with `content: []` and `not_found: true`. The requested page is empty and terminal; do not retry it as a failed supplier request.
- `fetch_credit` returns the supplier wallet under `total`, also normalized as `meta.credits.remaining`. These are AI Ark credits, separate from the Oxygen billing balance.
- Result endpoints can be called before completion; handle in-progress or conflict responses by polling statistics later.
- `mobile_phone_finder` requires either a LinkedIn URL or both company domain and full name.
- Webhook resend tools send to an external URL. Use them only for run repair with an approved URL.

## Approval

Before live AI Ark email export, email finder, mobile phone finder, or personality analysis, show selected tool id, row scope, expected maximum Oxygen credits, webhook URL when applicable, and one pilot output. Require explicit approval for mobile phone and personality analysis even when the row scope is small.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `ai_ark.company_search` | 0.5 cr per result (example payload: 25 results = 12.5 cr) | pre_authorize | paid_provider | — |
| `ai_ark.email_finder` | 2.5 cr per result (example payload: 10 results = 25 cr) | pre_authorize | paid_provider | async — returns a job handle; poll for completion |
| `ai_ark.email_finder_results` | free — not billed | no_bill | none | — |
| `ai_ark.email_finder_statistics` | free — not billed | no_bill | none | — |
| `ai_ark.export_people` | 5 cr per result (example payload: 100 results = 500 cr) | pre_authorize | paid_provider | async — returns a job handle; poll for completion |
| `ai_ark.export_people_results` | free — not billed | no_bill | none | — |
| `ai_ark.export_people_statistics` | free — not billed | no_bill | none | — |
| `ai_ark.export_person_single` | 5 cr | pre_authorize | paid_provider | — |
| `ai_ark.fetch_credit` | free — not billed | no_bill | none | — |
| `ai_ark.mobile_phone_finder` | 25 cr | pre_authorize | paid_provider | — |
| `ai_ark.people_search` | 2.5 cr per result (example payload: 25 results = 62.5 cr) | pre_authorize | paid_provider | — |
| `ai_ark.personality_analysis` | 20 cr | pre_authorize | ai_inference | — |
| `ai_ark.resend_email_finder_webhook` | free — not billed | no_bill | external_send | external write — live gate (approved + max_credits) |
| `ai_ark.resend_export_people_webhook` | free — not billed | no_bill | external_send | external write — live gate (approved + max_credits) |
| `ai_ark.reverse_lookup` | 2.5 cr | pre_authorize | paid_provider | — |
| `ai_ark.save_list` | free — not billed | no_bill | external_send | external write — live gate (approved + max_credits) |
<!-- END GENERATED -->
