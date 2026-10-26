# Forager Runbook

> **Runs only on the workspace's own Forager key**, and is in no default chain. Connect it with
> `oxygen integrations connect forager --api-key <key>` (its free `_totals` counts
> need the key too), then select it with `--tool-id` or `--route-id` on a search run, or
> `--provider-order` on an enrichment column.
> A call on your key spends your Forager credits; OXYGEN's per-call BYOK platform fee, when it applies, shows in the preview and in
> `oxygen billing usage --meter byok_calls --json`. The generated table lists OXYGEN's
> rates for reference.

Use Forager for LinkedIn-identity contact data: verified work emails, personal emails, and mobile numbers keyed on a LinkedIn slug or Forager person id, reverse person lookup from an email or phone number, and structured person/company/job search. Oxygen resolves the Forager account id from the API key automatically, so requests never need an `account_id`.

## Best Fits

- `forager.work_emails_lookup`: row has a person LinkedIn URL, missing work email. Every result carries a `validation_status` (valid/risky/invalid/unknown).
- `forager.personal_emails_lookup`: personal (non-work) email plays such as ad audiences. The `personal_email` waterfall capability runs LeadMagic only by default; name Forager with `--provider-order` to add it, bill-on-hit.
- `forager.phone_numbers_lookup`: approved mobile lookup from a person LinkedIn URL; a premium step in the phone waterfall.
- `forager.person_reverse_lookup_by_email` / `_by_phone`: identify signups, reply senders, or inbound callers from a bare email/phone.
- `forager.person_role_search`: find people by role, skills, company domains; free `_totals` sizing first.
- `forager.organization_search` / `forager.job_search`: firmographic accounts and hiring signals; free `_totals` sizing first.
- `forager.autocomplete_*`: resolve the integer filter ids (industries, locations, skills, technologies, organizations) that the search endpoints require.
- `forager.account_info`: free key validation plus remaining Forager credit balance before a batch run.

## Operating Pattern

1. Connect BYOK with `oxygen integrations connect forager --api-key <key>`, using an API key from the Forager account.
2. Use `oxygen tools search forager --json` and inspect exact descriptors with `oxygen tools get <tool_id> --json`.
3. Prefer dry-run first:

```bash
oxygen tools run forager.work_emails_lookup --mode dry_run --input-json '{"linkedin_url":"https://linkedin.com/in/example"}' --json
```

4. Contact lookups accept a full LinkedIn URL or bare slug (`linkedin_public_identifier`); Oxygen extracts the slug. A `person_id` from a prior Forager search also works.
5. For table work, the default email and phone waterfalls do not include Forager; add it to a waterfall column with `--provider-order`, and use direct action columns for reverse lookups and searches.
6. Distinguish the two miss shapes: `[]` means the person exists without that contact data (not charged); HTTP 404 means the person is not in Forager's dataset at all.

## Cost And Safety

- Forager bills its own credits per data retrieval, and misses are not charged. A phone or a reverse-phone lookup costs about three times an email lookup.
- Phone lookup is a premium step; keep it behind the waterfall tail or explicit approval rather than first-pass enrichment.
- Search endpoints bill per page; always run the free `_totals` op before paging a broad query.
- Autocomplete and `account_info` are free reads.

## Fallbacks

- Missing work email: try `prospeo.enrich_person`, `contactout.people_enrich`, or `hunter.email_finder`.
- Personal email: try `contactout.contact_info_linkedin`.
- Phone lookup: try `leadmagic.mobile_finder` or `contactout.people_enrich` after approval.
- Reverse email lookup: try `contactout.email_profile_enrich` or `peopledatalabs.person_enrich`.
- People search: try `blitzapi.people_search` or `peopledatalabs.person_search`.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `forager.account_info` | free — not billed | no_bill | none | — |
| `forager.autocomplete_industries` | free — not billed | no_bill | none | — |
| `forager.autocomplete_locations` | free — not billed | no_bill | none | — |
| `forager.autocomplete_organization_keywords` | free — not billed | no_bill | none | — |
| `forager.autocomplete_organizations` | free — not billed | no_bill | none | — |
| `forager.autocomplete_person_skills` | free — not billed | no_bill | none | — |
| `forager.autocomplete_web_technologies` | free — not billed | no_bill | none | — |
| `forager.credit_usage_totals` | free — not billed | no_bill | none | — |
| `forager.job_search` | 20 cr (example payload; estimate 2–10 cr) | pre_authorize | paid_provider | — |
| `forager.job_search_totals` | free — not billed | no_bill | none | — |
| `forager.organization_search` | 10 cr (example payload; estimate 2–10 cr) | pre_authorize | paid_provider | — |
| `forager.organization_search_totals` | free — not billed | no_bill | none | — |
| `forager.person_detail_lookup` | 10 cr (example payload; estimate 2–20 cr) | pre_authorize | paid_provider | — |
| `forager.person_reverse_lookup_by_email` | 50 cr | pre_authorize | paid_provider | — |
| `forager.person_reverse_lookup_by_phone` | 150 cr | pre_authorize | paid_provider | — |
| `forager.person_role_search` | 10 cr (example payload; estimate 2–10 cr) | pre_authorize | paid_provider | — |
| `forager.person_role_search_totals` | free — not billed | no_bill | none | — |
| `forager.personal_emails_lookup` | 50 cr | pre_authorize | paid_provider | — |
| `forager.phone_numbers_lookup` | 150 cr | pre_authorize | paid_provider | — |
| `forager.website_detail_lookup` | 10 cr (example payload; estimate 2–10 cr) | pre_authorize | paid_provider | — |
| `forager.work_emails_lookup` | 50 cr | pre_authorize | paid_provider | — |
<!-- END GENERATED -->
