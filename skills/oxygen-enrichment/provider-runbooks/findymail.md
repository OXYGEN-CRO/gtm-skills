# Findymail Runbook

> **Runs only on the workspace's own Findymail key**, and is in no default chain. Connect it with
> `oxygen integrations connect findymail --api-key <key>`, then select it with `--tool-id` or `--route-id` on a search run, or
> `--provider-order` on an enrichment column.
> A call on your key spends your Findymail credits; OXYGEN's per-call BYOK platform fee, when it applies, shows in the preview and in
> `oxygen billing usage --meter byok_calls --json`. The generated table lists OXYGEN's
> rates for reference.

Use Findymail for focused contact-data steps where the row already has enough identity to keep the provider call bounded: name plus domain for work email, email for verification or reverse lookup, LinkedIn profile for phone, and company domain/name/LinkedIn URL for company enrichment.

## Best Fits

- `findymail.find_from_name`: known person and company domain, missing work email.
- `findymail.verify_email`: final deliverability check before outbound activation.
- `findymail.find_phone`: approved direct-phone lookup from a person LinkedIn URL.
- `findymail.enrich_company`: lightweight company enrichment from domain, name, or company LinkedIn URL.
- `findymail.search_employees`: small contact pulls from a known company website, ideally with job-title constraints.
- `findymail.reverse_email_lookup`: repair thin contact rows that have an email but lack person context.
- `findymail.intellimatch_search`: bounded lead-search pilot from natural-language intent.

## Operating Pattern

1. Use `oxygen tools search findymail --json` and inspect the exact descriptor with `oxygen tools get <tool_id> --json`.
2. Prefer dry-run first:

```bash
oxygen tools run findymail.find_from_name --mode dry_run --input-json '{"name":"Jordan Lee","domain":"example.com"}' --json
```

3. For table work, add a provider action column and pilot one row before a batch.
4. Run any live Findymail action only after the user approves scope, row count, and credit cap. Phone lookup and Intellimatch require extra scrutiny because they can be higher-cost or broader-scope than a single email lookup.
5. Write provider status, credits, and returned evidence back into table columns; do not jump from provider output to outbound enrollment.

## Cost And Safety

- Email finder, company enrichment, reverse lookup, employee search, verification, phone lookup, and Intellimatch are paid provider calls when a result is found or a provider-side billable search is accepted.
- Phone lookup costs materially more provider credits than email lookup and should not be a first-pass enrichment step.
- Verification is a paid provider call; use it where it changes an outbound decision.
- Treat EU/GDPR phone coverage as out of scope unless the user supplies an approved compliance basis.

## Fallbacks

- Missing work email: try `hunter.email_finder`, `leadmagic.email_finder`, or `icypeas.email_discovery`.
- Email verification: the native chain (`oxygen verify email`, or a `verify_email` column), which escalates catch-all addresses; a single-provider verifier skips that step.
- Phone lookup: try `leadmagic.mobile_finder` or `contactout.people_enrich` after approval.
- Company enrichment: try `leadmagic.company_enrichment` or `apollo.organization_enrich`.
- People search from a known account: try `blitzapi.people_search`, `leadmagic.people_by_title`, or `icypeas.people_search`.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `findymail.enrich_company` | 9.9 cr (example payload; estimate 0–20 cr) | pre_authorize | paid_provider | — |
| `findymail.find_from_name` | 9.9 cr | pre_authorize | paid_provider | — |
| `findymail.find_phone` | 99 cr | pre_authorize | paid_provider | — |
| `findymail.intellimatch_search` | 9.9 cr (example payload; estimate 0–200 cr) | pre_authorize | paid_provider | — |
| `findymail.reverse_email_lookup` | 9.9 cr (example payload; estimate 0–40 cr) | pre_authorize | paid_provider | — |
| `findymail.search_employees` | 9.9 cr (example payload; estimate 0–20 cr) | pre_authorize | paid_provider | — |
| `findymail.verify_email` | 9.9 cr (example payload; estimate 0–20 cr) | pre_authorize | paid_provider | — |
<!-- END GENERATED -->
