# Column templates

A template carries a maintained prompt, a typed answer, its grounding (a search, one fetched page, or the row's own text) and a per-row price, so adding it is one command with no prompt to write. Check the catalog before writing a research prompt.

```bash
oxygen columns catalog --category extract --json        # also: people, company, normalize, organize, summarize
oxygen columns catalog --search pricing --json          # templates and bundles match the same filter
oxygen columns add competitors --prompt-key pricing_plan_summary_v1 --input url=pricing_url --json
oxygen columns run competitors pricing_plan_summary --limit 1 --dry-run --json
```

- `--input <name>=<column>` binds each input the template declares (the catalog prints them); `--input-mapping '{"location":{"literal":"Berlin"}}'` pins a fixed value where a key allows one. OXYGEN infers nothing: bind every input.
- A template column is keyed from its title (`skill_set`, `full_name_from_profile`), not from the template key, unless you pass `--key`; the add response prints the key that `columns run` and other templates' `--input` take.
- A research or fetch template writes the same `{answer, found, confidence, sources}` cell as a research column, so `{{pricing_plan_summary.answer.plan_count}}` reads one field. A search template is a managed web-search tool column with a fixed price and no model (the first result's URL, or the result list). The catalog's credit label is the reserved ceiling; the `--dry-run` figure is authoritative for your rows.
- Web: Add column, Templates (and the Company research, Normalize and Organize groups). MCP: `oxygen_columns_catalog`, then `oxygen_columns_add` with `prompt_key`.

## Families

| Category | Reads | Examples |
| --- | --- | --- |
| `extract` | a page URL, a search by company, or row text | pricing pages (`pricing_plan_summary_v1` returns count, range, top plan and enterprise plan in one fetch), job posts (`job_posting_summary_v1`), event pages, the latest 10-K (`filing_10k_locator_v1`, then `filing_10k_initiatives_v1`), website facts, `site_seo_keywords_v1` (no model, fetch only), market and news questions, an investor's portfolio page, text extraction from an address or description |
| `people` | the `person_enrich` payload, or a full name | skills, graduate school, location, current employer domain, industry or company tested, job fit; public appearances (podcasts, talks, keynotes) in the last 12 months; a GitHub profile tied to the person |
| `company` | a domain or company name | web presence (LinkedIn, Crunchbase, careers page, domain from name), corporate structure (founders, parent, subsidiaries, stealth, ever sold), funding, footprint (HQ in a location, states, cities, store count), business model (SaaS, B2B, demos), tech (cloud provider, CRM from a tech-stack column), market (industry, NAICS, competitors in a region) |
| `normalize`, `organize` | row text, free | `clean_company_name_v1`, `clean_job_title_v1`, `email_type_v1`, `list_from_text_v1` |
| `summarize` | the row's own fields | `company_b2b_b2c_classification_v1` answers `B2B`, `B2C`, `B2B_and_B2C` or `unknown` with the wording it relied on |

- **People questions read one paid profile lookup.** Add the `person_enrich` bundle once (the `oxygen-enrichment` skill), then bind every people template to its payload: `--input profile=person_enrich`. Ten questions still cost one lookup plus each template's model call. `person_full_name_v1` is a 0-credit formula that lifts the name out for the appearance templates.
- **Appearance templates use strict web evidence**: a person with no verifiable dated item is `found: false`, never a guess. The 12-month window is part of the prompt (`ai.prompt_preview` in the dry run shows it); for another window write your own research column.
- **Funding, revenue, hiring and tech stack** have provider-data bundles that read data vendors rather than the web (`--preset company_funding` and siblings, `oxygen-enrichment`); prefer them to the web-research funding keys.
- A LinkedIn URL from a name and company is not a template: it is the identity-validated `linkedin_url` waterfall (`oxygen-enrichment`).
- `company_revenue_estimate_v1` and `company_valuation_estimate_v1` are labelled estimates with a range and the signals used; no provider sells private revenue or valuation.

## Website contacts

When the row holds each company's website, read the page instead of searching the web for it:

```bash
oxygen columns add leads --prompt-key website_contacts_v1 --input website=website --json
oxygen columns run leads website_contacts --limit 1 --dry-run --json
```

Per row: `emails[]` (each `verification: "unverified"`; add email verification to grade them), `phones[]` with a digits-only `normalized`, `keywords[]`, `social_profiles`, `page_title`, `source_url`, and `fetch` (which reader ran, its cost and every attempt). Extraction is free; you pay one fetch per row, and an empty page is a successful empty result. Only the page you point at is read, so map the contact page when you have it. A sequencer cannot read the jsonb cell: before `sequences push-external` or `sequences enroll`, add a free formula column such as `path(first(path(website_contacts, "emails")), "email")` so the table carries a scalar email.

## Cleanups before paid work

The `normalize` and `organize` templates add a clean sibling column, cost 0 credits and evaluate on read; `--preset domain_check` (paid, cached 30 days per domain) marks dead and parked domains before you enrich them. The tidy pass that applies them, with per-category approval, is the `oxygen-table-tidy` skill.
