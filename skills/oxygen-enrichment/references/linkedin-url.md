# LinkedIn URL

Resolve a person's LinkedIn profile URL from a name and company, or from a known email. Identity validation is built in: every provider hit is checked against the source name and company, so a namesake's profile is rejected rather than written.

## Inputs

- Primary: `full_name_column` (or `first_name_column` plus `last_name_column`) with `company_domain_column` or `company_name_column`. A domain gives the highest precision; mapping both domain and name lets providers that prefer either one run.
- `email_column`, for email-to-profile providers.

## Preview, pilot, batch

`oxygen columns add <table> --capability linkedin_url --json` creates the column without running it. Preview with `oxygen enrich-column preview <table> --capability linkedin_url --json` (MCP `oxygen_enrich_column_preview` with `capability: "linkedin_url"` and the column names), free, and read:

- `selected_providers` and `provider_input_coverage`: which lanes run for this workspace and whether the mapped inputs satisfy each.
- `estimated_credits_per_row`, `estimated_credits`, `credit_posture`, `recommended_max_credits`.
- `normalized_outputs`: the jsonb target (default `linkedin_url_enrichment`) and the normalized text column (default `linkedin_url`).

Run a small pilot with the preview's ceiling after approval (`oxygen_enrich_column_run`, or `enrich-column run` with `--limit` and `--max-credits`), inspect `oxygen table-runs items <run_id> --status failed --json` and the run link, then batch only the rows still missing a URL (`only_missing: true`, or a filter on `linkedin_url` is null).

## What lands

- `linkedin_url` (text, semantic type `person.linkedin_url`): the normalized `https://www.linkedin.com/in/<slug>` from the first lane that returned an accepted hit.
- `linkedin_url_enrichment` (jsonb): `value`, `confidence`, `hit_provider`, `providers_attempted` and per-row `identity_match` evidence (name score, nickname notes, the kind of company evidence).
- `linkedin_url_provider`, `linkedin_url_status`, `linkedin_url_enriched_at` for filters.

## How validation decides

- `verified`: the name matches (nicknames and diacritics tolerated) and company evidence corroborates it (domain equality, the domain root in the handle, or a fuzzy company-name match).
- `guessed`: the name matches strongly but no company evidence came back.
- `unverified`: a URL came back but the source name was missing, or only partial name evidence.
- `rejected`: the name did not match; the URL is discarded and the next lane runs.

Sales Navigator (`/sales/`), Recruiter (`/recruiter/`), search-result, company and member-id (`/in/ACwAA…`) URLs are rejected before validation: none is the person's public profile URL.

## Cost and order

The managed LinkedIn lookup runs first: it finds the company, searches its people by name, and makes one more profile read when the match carries only a member id. It bills only for a URL that matches the person; a miss and a failed extra read cost nothing, and the row moves to the next lane. The preview quotes the current price and the lane order; `provider_order` replaces the order, for example to name a provider that runs only when asked or on your own key.

Once the URL is known, `oxygen find person --linkedin-url <url> --json` (dry run first, then `--mode live --max-credits <estimate.recommended_max_credits>`) returns the whole profile in one managed lookup, or add the `person_enrich` preset to the table.

When the chain cannot meet the precision a segment needs (name-only rows with no company), a research column plus an AI validation column is a custom override, not the default path.
