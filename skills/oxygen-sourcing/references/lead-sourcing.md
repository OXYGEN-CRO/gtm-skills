# Lead sourcing and sourcing plans

Two planners turn a natural-language request into routes before any provider runs.

## `lead-sourcing plan`: ICP-first leads

For "build leads for this ICP", start here. It qualifies accounts first and delegates its people step to the people planner; it never sources contacts itself.

```bash
oxygen knowledge resolve --purpose lead_sourcing --require-ready --json
oxygen lead-sourcing plan --prompt ./icp.txt --json
```

- The account step carries a `delegate_to` block pointing at `companies search plan` (MCP `oxygen_companies_search_plan`): run it there rather than wiring an account provider by hand, or import an existing account list ([companies](companies.md)).
- Search people only at the accepted accounts, through `people search plan` with those domains as `company.domains` and intent `account_contacts` ([people](people.md)).
- The plan's phone step is the mobile phone column: run the free `enrich-column preview` in `provider_requests.phone_enrichment.handoff` for the selected rows, show its per-row prices and ceiling, and run it only after approval with `--max-credits` and `--approved`. The plan's `credit_estimate` and `chains` summarize prices per input shape; the scoped preview is the current quote.
- Audit before paid enrichment or an outbound sync: `oxygen lead-sourcing audit <table> --spec ./lead-sourcing-spec.json --json`.

## `sourcing plan`: when the starting point is unclear

When the ask is accounts, people, LinkedIn profiles, email-ready or phone-ready leads and the right primitive is not obvious:

```bash
oxygen sourcing plan --prompt "<the request>" --json
```

Read `strategy`, `context_confirmation`, `provider_routes`, `tool_access`, `cost_posture` and `enrichment_handoff`. Strategies:

- `account_first_lead_sourcing`: the account universe is unknown or ICP-driven; follow the returned lead-sourcing plan before any people search.
- `known_account_decision_maker` (one account, ordered persona priority) and `known_account_org_chart` (one account, several roles).
- `broad_persona_search`: a broad people search, with an account-quality warning.
- `linkedin_profile_lookup`: a name and company to a profile URL.
- `sales_nav_or_linkedin_list_handoff`: profile URLs, Sales Navigator or Recruiter lists.
- `email_ready_contact_sourcing` and `phone_ready_contact_sourcing`: discovery with a work-email or direct-dial handoff to enrichment.
- `niche_profile_discovery`: small companies or thin databases.

For people and profile strategies, dry-run the first runnable route (`oxygen tools run <tool_id> --mode dry_run --input-json '<json>' --json`) before any ingestion, and import provider pages only once row scope, dedupe key and mapping are clear (`table-ingestions create-tool-page`, the `oxygen-tables` skill). Email, phone, reveals, CRM writes, outreach and LinkedIn actions are each a separate live action with its own scope, estimate and ceiling.

## Search jobs

The generic `search` surface creates a bounded, table-backed job for signals, web pages, local businesses or source-specific data, with the route and its fallbacks visible. Companies go through `companies search` and people through `people search`; a request for either here answers `use_companies_search` or `use_people_search`. People:

```bash
oxygen people search plan --prompt "<goal>" --json > plan.json
oxygen people search run --plan-json ./plan.json --route-id <recommended_live_route_id> --mode dry_run --json
oxygen people search run --plan-json ./plan.json --route-id <recommended_live_route_id> --mode live \
  --max-credits <n> --max-pages 1 --upsert-key linkedin_url --approved --json
oxygen table-ingestions wait <run_id> --json
```

Live runs need `--max-credits` and a page cap. Signal searches (hiring, funding, tech, news, LinkedIn posts) are the `oxygen-signals` skill.

## Account and contact tables

Companies first, then people, unless the user already named the companies. Keep accounts and contacts in separate tables linked by `account_domain` or a row link, with source tool, source query, run id and the last-sourced time on each row. A list of companies from a source (an investor portfolio, a directory, an event): import or ingest it, resolve missing domains, then source people only at accounts with clean domains. Hand a finished seed table to enrichment (the `oxygen-enrichment` skill).
