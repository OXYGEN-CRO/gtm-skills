# Dropleads Runbook

> **The people planners use its free count and its people search as routes; it is not in the default
> email, phone or LinkedIn URL chains.** Select it explicitly with `--tool-id` or `--route-id` on a search
> run, or `--provider-order` on an enrichment column.

Use Dropleads for masked people discovery from structured lead filters and as a domain-based work-email fallback after higher-priority waterfall steps. The Prime DB search and count endpoints are planning and sourcing steps; they do not reveal email or phone values.

## Best Fits

- `dropleads.people_count`: estimate the number of matching leads before pulling rows.
- `dropleads.people_search`: retrieve masked lead rows from persona, company, geography, and firmographic filters.
- `dropleads.email_finder`: find a work email from first name, last name, and company identity.
- `dropleads.email_verifier`: verify a candidate email address.

## Operating Pattern

1. Inspect the descriptor before writing payloads:

```bash
oxygen tools search dropleads --json
oxygen tools get dropleads.people_count --json
oxygen tools get dropleads.people_search --json
oxygen tools get dropleads.email_finder --json
oxygen tools get dropleads.email_verifier --json
```

2. Run `dropleads.people_count` before broad searches.
3. For people at selected accounts, pass exact company domains where possible.
4. Page through small batches and ingest results into a Contacts table with `source_tool`, `source_query`, and raw provider output.
5. Treat returned people as candidates until identity and account matching pass local validation.

## Cost And Safety

- Count and search are no-reveal operations in the public Dropleads Prime DB docs.
- Email enrichment is a paid action and should run only after row review, row cap, and approval unless it is part of the approved work-email column run.
- Keep broad title filters under control with account-domain, seniority, department, geography, or employee-range constraints.

## Fallbacks

- If the count is too broad, tighten account domains or seniority before search.
- If coverage is weak, try `blitzapi.people_search`, `wiza.people_search`, or `contactout.people_search`.
- For paid contact data after review, use the approved email or phone waterfall rather than revealing every sourced row.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `dropleads.email_finder` | 3.1 cr (example payload; estimate 2–10 cr) | pre_authorize | paid_provider | — |
| `dropleads.email_verifier` | 0.31 cr (example payload; estimate 2–4 cr) | pre_authorize | paid_provider | — |
| `dropleads.people_count` | free — not billed | no_bill | none | — |
| `dropleads.people_search` | free — not billed | no_bill | none | — |
<!-- END GENERATED -->
