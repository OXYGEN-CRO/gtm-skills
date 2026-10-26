# Scalelist Runbook

> **Runs only on the workspace's own Scalelist key**, and is in no default chain. Connect it with
> `oxygen integrations connect scalelist --api-key <key>`, then select it with `--tool-id` or `--route-id` on a search run, or
> `--provider-order` on an enrichment column.
> A call on your key spends your Scalelist credits; OXYGEN's per-call BYOK platform fee, when it applies, shows in the preview and in
> `oxygen billing usage --meter byok_calls --json`. The generated table lists OXYGEN's
> rates for reference.

Use Scalelist as a result-billed work-email and mobile-phone enrichment fallback: Scalelist bills your account only when it finds a work email or a mobile number, and a phone costs many times an email.

## Best Fits

- `scalelist.email_finder`: find a work email from full name or first/last name plus company website or company name.
- `scalelist.phone_finder`: find a mobile number from LinkedIn URL, LinkedIn id, email, or name plus company identity.
- `scalelist.domain_email_finder`: find several emails for a company domain with an explicit limit.
- `scalelist.bulk_email_create` / `scalelist.bulk_email_result`: async email batches after row ids and polling are modeled.
- `scalelist.bulk_phone_create` / `scalelist.bulk_phone_result`: async phone batches after explicit approval and spend caps.

## Operating Pattern

1. Inspect the tool schema before hand-writing payloads:

```bash
oxygen tools search scalelist --json
oxygen tools get scalelist.email_finder --json
oxygen tools get scalelist.phone_finder --json
```

2. For row-level use, name Scalelist in a work-email or phone waterfall column (`--provider-order scalelist`); the default waterfalls do not include it.
3. Pass `company_website`/`company_domain` when available; use `company_name` only as a fallback.
4. For phone, prefer `linkedin_profile_url`, then email, then name plus company.
5. Treat `Valid` email status as verified. Treat `Risky` as unverified unless the workflow explicitly allows risky emails.

## Cost And Safety

- Found emails and found phones are billed to your Scalelist account; misses cost nothing there.
- Phone enrichment requires explicit approval, row scope, and spend cap before live runs.
- Bulk jobs are for list exports; row-level waterfalls use the single-lookup operations.

## Fallbacks

- Email fallbacks: `dropleads.email_finder`, `bettercontact.enrich_lead`.
- Phone fallbacks: `leadmagic.mobile_finder`, `contactout.people_enrich`, `bettercontact.enrich_lead`.
- If Scalelist misses by name/company, try a LinkedIn-first provider after resolving the profile URL.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `scalelist.account` | free — not billed | no_bill | none | — |
| `scalelist.bulk_email_create` | 9.9 cr (example payload; estimate 0–1000 cr) | pre_authorize | paid_provider | async — returns a job handle; poll for completion |
| `scalelist.bulk_email_result` | free — not billed | no_bill | none | — |
| `scalelist.bulk_phone_create` | 198 cr (example payload; estimate 0–20000 cr) | pre_authorize | paid_provider | async — returns a job handle; poll for completion |
| `scalelist.bulk_phone_result` | free — not billed | no_bill | none | — |
| `scalelist.domain_email_finder` | 99 cr (example payload; estimate 0–1000 cr) | pre_authorize | paid_provider | — |
| `scalelist.email_finder` | 9.9 cr (example payload; estimate 0–10 cr) | pre_authorize | paid_provider | — |
| `scalelist.phone_finder` | 198 cr (example payload; estimate 0–200 cr) | pre_authorize | paid_provider | — |
<!-- END GENERATED -->
