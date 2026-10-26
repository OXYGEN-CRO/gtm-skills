# LeadMagic Runbook

Use this runbook when OXYGEN tool discovery returns `leadmagic.*` tools for account research, people discovery, email or phone lookup, hiring signals, funding, technographics, competitors, or ad intelligence.

## When To Use

- You need company-first prospecting: account enrichment, employees, role holders, hiring signals, funding, competitors, or ads.
- You have qualified people and need a work email, profile-to-email lookup, or mobile lookup.
- You want provider-credit-aware discovery where candidates can be reviewed before buying contact details.

## Before Running

```bash
oxygen tools search leadmagic --json
oxygen tools get leadmagic.email_finder --json
oxygen tools get leadmagic.people_search --json
oxygen tools run leadmagic.check_credits --mode dry_run --input-json '{}' --json
```

Inspect descriptor cost posture, required fields, fallback tools, and whether the result is discovery-only or returns contact details.

## Recommended Patterns

- For account-to-people work, run company enrichment or people discovery first, review candidates, then run email or mobile lookup only on selected rows.
- For TAM expansion from a known-good account, inspect the seed, filters and a small explicit `limit` with Oxygen dry-run first. Review returned companies after an approved live pilot with a credit cap.
- For broad company, people, or job searches, run `leadmagic.search_stats` first when the operator needs coverage or top-dimension context.
- For outbound email, validate known or newly found emails before any campaign enrollment.
- For hiring signals, resolve job-search filters or inspect catalogs before running a paid job search.
- Store raw provider output in a JSONB tool column and materialize stable fields such as email, phone, company domain, title, and status into companion columns.

## Gotchas

- v3 people discovery returns people records and availability flags by default. Raw email or phone fields require `include_contact_details: true` and `confirm_credit_charge: true`.
- `mobile_finder`, `profile_to_email`, and `email_to_profile` are higher-cost than name/domain work-email lookup. Use them for high-value rows.
- `company_lookalike` can broaden account scope quickly. Use Oxygen dry-run to inspect the request and quote. Omit `preview` on public company API calls and keep `limit` small after reviewing the seed and filters.
- Personal email lookup should be an explicit operator choice, not an automatic fallback for normal B2B outreach. The work-email column's personal email option (`columns add --capability work_email --include-personal-email`; one person: `oxygen find personal-email`) already routes this through LeadMagic's personal-email finder, its only default lane, bill-on-hit; prefer it over a hand-built `personal_email_finder` tool column.
- Treat `email_status: "valid"` as usable evidence. Treat `invalid`, `unknown`, missing status, or provider warnings as requiring review.
- LeadMagic does not send messages, enroll campaigns, or write CRM records.

## Approval

Before live batch runs, show row scope, selected tool IDs, expected maximum provider credits, fallback order, and a one-row pilot output. For mobile or personal email runs, require explicit approval even when the row scope is small.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `leadmagic.analytics_dashboard` | free — not billed | no_bill | none | — |
| `leadmagic.b2b_ad_details` | 24.5 cr (example payload; estimate 0–40 cr) | pre_authorize | paid_provider | — |
| `leadmagic.b2b_ads_search` | 24.5 cr (example payload; descriptor hint 134.75 cr) | pre_authorize | paid_provider | — |
| `leadmagic.check_credits` | free — not billed | no_bill | none | — |
| `leadmagic.company_enrichment` | 12.25 cr (example payload; descriptor hint 612.5 cr) | pre_authorize | paid_provider | — |
| `leadmagic.company_funding` | 49 cr | pre_authorize | paid_provider | — |
| `leadmagic.company_lookalike` | 61.25 cr | pre_authorize | paid_provider | — |
| `leadmagic.company_search` | 12.25 cr (example payload; descriptor hint 612.5 cr) | pre_authorize | paid_provider | — |
| `leadmagic.competitors_search` | 61.25 cr | pre_authorize | paid_provider | — |
| `leadmagic.email_finder` | 12.25 cr | pre_authorize | paid_provider | — |
| `leadmagic.email_to_profile` | 122.5 cr | pre_authorize | paid_provider | — |
| `leadmagic.email_validation` | 3.062 cr | pre_authorize | paid_provider | — |
| `leadmagic.employee_finder` | 0.612 cr (example payload; estimate 0–20 cr) | pre_authorize | paid_provider | — |
| `leadmagic.google_ads_search` | 12.25 cr (example payload; descriptor hint 122.5 cr) | pre_authorize | paid_provider | — |
| `leadmagic.job_change_detector` | 36.75 cr | pre_authorize | paid_provider | — |
| `leadmagic.job_company_types` | free — not billed | no_bill | none | — |
| `leadmagic.job_countries` | free — not billed | no_bill | none | — |
| `leadmagic.job_industries` | free — not billed | no_bill | none | — |
| `leadmagic.job_regions` | free — not billed | no_bill | none | — |
| `leadmagic.job_search` | 12.25 cr (example payload; estimate 0–200 cr) | pre_authorize | paid_provider | — |
| `leadmagic.job_search_catalogs` | free — not billed | no_bill | none | — |
| `leadmagic.job_search_companies` | free — not billed | no_bill | none | — |
| `leadmagic.job_search_job_board_stats` | free — not billed | no_bill | none | — |
| `leadmagic.job_search_locations` | free — not billed | no_bill | none | — |
| `leadmagic.job_search_occupation_taxonomy` | free — not billed | no_bill | none | — |
| `leadmagic.job_search_resolve` | free — not billed | no_bill | none | — |
| `leadmagic.job_search_stats` | free — not billed | no_bill | none | — |
| `leadmagic.job_search_tags` | free — not billed | no_bill | none | — |
| `leadmagic.job_search_titles` | free — not billed | no_bill | none | — |
| `leadmagic.job_types` | free — not billed | no_bill | none | — |
| `leadmagic.jobs_finder` | 12.25 cr (example payload; estimate 0–20 cr) | pre_authorize | paid_provider | — |
| `leadmagic.meta_ads_search` | 12.25 cr (example payload; descriptor hint 122.5 cr) | pre_authorize | paid_provider | — |
| `leadmagic.mobile_finder` | 61.25 cr | pre_authorize | paid_provider | — |
| `leadmagic.people_by_title` | 12.25 cr (example payload; estimate 0–20 cr) | pre_authorize | paid_provider | — |
| `leadmagic.people_employees` | 12.25 cr (example payload; estimate 0–20 cr) | pre_authorize | paid_provider | — |
| `leadmagic.people_icp_search` | 12.25 cr (example payload; estimate 0–20 cr) | pre_authorize | paid_provider | — |
| `leadmagic.people_lookalike` | 12.25 cr (example payload; estimate 0–20 cr) | pre_authorize | paid_provider | — |
| `leadmagic.people_mixed_search` | 12.25 cr (example payload; estimate 0–20 cr) | pre_authorize | paid_provider | — |
| `leadmagic.people_search` | 12.25 cr (example payload; estimate 0–20 cr) | pre_authorize | paid_provider | — |
| `leadmagic.personal_email_finder` | 24.5 cr | pre_authorize | paid_provider | — |
| `leadmagic.profile_search` | 12.25 cr (example payload; estimate 0–20 cr) | pre_authorize | paid_provider | — |
| `leadmagic.profile_to_email` | 61.25 cr | pre_authorize | paid_provider | — |
| `leadmagic.role_finder` | 24.5 cr (example payload; estimate 0–40 cr) | pre_authorize | paid_provider | — |
| `leadmagic.search_stats` | free — not billed | no_bill | none | — |
| `leadmagic.technographics` | 12.25 cr | pre_authorize | paid_provider | — |
<!-- END GENERATED -->
