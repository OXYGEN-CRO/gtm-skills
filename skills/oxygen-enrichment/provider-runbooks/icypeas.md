# Icypeas Runbook

Icypeas covers work email discovery, email verification, domain scans, LinkedIn profile/company URL lookup, reverse email lookup, and a people/company lead database. It follows the managed lookup in the default `find_linkedin_url` waterfall and is one of the default work-email lanes.

## The one thing that makes Icypeas different: single searches are asynchronous

Every single-search endpoint (`email_discovery`, `email_verification`, `domain_scan`, `profile_url_search`, `company_url_search`, `reverse_email_lookup`, `scrape_profile`, `scrape_company`) answers the POST with an acknowledgment, not a result:

```json
{ "success": true, "item": { "status": "NONE", "_id": "p_gfS5EB4liCGm90KDFC" } }
```

- `NONE`, `SCHEDULED`, `IN_PROGRESS` mean the search is still running.
- `FOUND` / `DEBITED` (found and charged), `NOT_FOUND` / `DEBITED_NOT_FOUND`, `BAD_INPUT`, `INSUFFICIENT_FUNDS`, `ABORTED` are terminal.
- The result is read from `icypeas.search_items_read` with `{"id":"<_id>"}` **alone**, or pushed to a per-search `custom.webhookUrl`. Do not add `mode` to a by-id read: `{"mode":"single"}` is the fetch-all filter (the 10 most recent single searches) and returns items you did not ask for.

OXYGEN does this for you: it polls the read endpoint after the acknowledgment and returns the completed item as `item`, so a normal `oxygen tools run icypeas.email_discovery` gives you the result. `meta.search_id`, `meta.search_status` and `meta.poll_attempts` show what the poll landed on. If the search is still pending when the call's time runs out, the call fails with `provider_async_pending` carrying the `search_id`: the search was started and Icypeas still debits it, so treat it as a real failure, not a no-match, and re-read the item later with `icypeas.search_items_read`.

Bulk searches are different: they return a file id, and progress/results come from `icypeas.search_files_read` and `icypeas.search_items_read` with `{"mode":"bulk","file":"<file_id>"}`. Nothing polls those for you.

## Best Fits

- `icypeas.email_discovery`: work email from first/last name plus domain or company.
- `icypeas.profile_url_search`: LinkedIn profile URL from name plus company or job title.
- `icypeas.email_verification`: a low-cost deliverability check.
- `icypeas.people_count` / `icypeas.companies_count`: free zero-credit audience sizing before any paid pull.
- `icypeas.bulk_search`: up to 5,000 rows per job for email search, verification, or domain scan — the throughput surface.
- `icypeas.profile_url_bulk_search` / `icypeas.scrape_profiles_bulk`: up to 50 rows per request.

## Operating Pattern

1. `oxygen tools search icypeas --json`, then `oxygen tools get <tool_id> --json` for the exact descriptor.
2. Dry-run first:

```bash
oxygen tools run icypeas.email_discovery --mode dry_run --input-json '{"firstname":"Jordan","lastname":"Lee","domainOrCompany":"example.com"}' --json
```

3. Size lead-database work with the free count routes before paying for `people_search` / `companies_search`.
4. Run live only after the user approves scope, row count, and credit cap.
5. Lead-database queries use Icypeas' own field names. `companySize` does not exist: use `currentCompany.headcount` (people) or `headcount` (companies) with numeric range operators. Oxygen refuses unsupported filter keys before spending anything.

## Rate Limits And Errors

- OXYGEN paces each Icypeas operation family below the vendor's per-second limits on the managed account.
- Result retrieval (`search_items_read`) is limited per minute, not per second, and every single search polls it: several rows polling at once share that budget, so keep concurrent single-search fan-out small and prefer `icypeas.bulk_search` for volume.
- Icypeas answers **HTTP 200 for validation errors** (`{"success":false,...}` or a non-empty `validationErrors` array). Oxygen fails those calls with `provider_validation_error` instead of recording a successful, billed call; fix the request payload rather than retrying.
- 401 means the API key is rejected; 429 means the rate limit was exceeded and is retried with backoff.

## Fallbacks

- Work email: `hunter.email_finder`, `leadmagic.email_finder`, `prospeo.email_finder`, or `findymail.find_from_name` on the workspace's own Findymail key.
- LinkedIn profile URL: `prospeo.enrich_person`, `contactout.people_enrich`, `leadmagic.profile_search`.
- Email verification: the native chain (`oxygen verify email`, or a `verify_email` column), which escalates catch-all addresses; a single-provider verifier skips that step.
- People search: `blitzapi.people_search`, `contactout.people_search`, `dropleads.people_search`.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `icypeas.bulk_search` | 2.495 cr | pre_authorize | paid_provider | — |
| `icypeas.companies_count` | free — not billed | no_bill | none | — |
| `icypeas.companies_search` | 2.495 cr | pre_authorize | paid_provider | — |
| `icypeas.company_url_bulk_search` | 2.495 cr | pre_authorize | paid_provider | — |
| `icypeas.company_url_search` | 2.495 cr | pre_authorize | paid_provider | — |
| `icypeas.domain_scan` | 2.494 cr | pre_authorize | paid_provider | — |
| `icypeas.email_discovery` | 2.494 cr | pre_authorize | paid_provider | — |
| `icypeas.email_verification` | 0.25 cr | pre_authorize | paid_provider | — |
| `icypeas.people_count` | free — not billed | no_bill | none | — |
| `icypeas.people_search` | 9.98 cr | pre_authorize | paid_provider | — |
| `icypeas.profile_url_bulk_search` | 2.495 cr | pre_authorize | paid_provider | — |
| `icypeas.profile_url_search` | 2.494 cr | pre_authorize | paid_provider | — |
| `icypeas.reverse_email_lookup` | 24.95 cr | pre_authorize | paid_provider | — |
| `icypeas.reverse_email_lookup_bulk` | 2.495 cr | pre_authorize | paid_provider | — |
| `icypeas.scrape_companies_bulk` | 2.495 cr | pre_authorize | paid_provider | — |
| `icypeas.scrape_company` | 2.495 cr | pre_authorize | paid_provider | — |
| `icypeas.scrape_profile` | 2.495 cr | pre_authorize | paid_provider | — |
| `icypeas.scrape_profiles_bulk` | 2.495 cr | pre_authorize | paid_provider | — |
| `icypeas.search_files_read` | free — not billed | no_bill | none | — |
| `icypeas.search_items_read` | free — not billed | no_bill | none | — |
| `icypeas.subscription_information` | free — not billed | no_bill | none | — |
<!-- END GENERATED -->
