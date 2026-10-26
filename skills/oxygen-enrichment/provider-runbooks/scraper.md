# Professional Network Data and HarvestAPI BYOK

OXYGEN's managed `scraper.*` provider reads public LinkedIn profiles, companies, posts and engagers without a connected LinkedIn account or a provider key. The managed data comes from the supplier named in its label ("Professional Network Data · supplied by …") and in each operation's `data_sourcing`; OXYGEN is moving it from Up2Data to HarvestAPI without changing any operation. Your own HarvestAPI key is a separate option under the same operation ids. The descriptor is the authority for supported inputs, output fields, availability and price.

Which surface owns which LinkedIn job (public research, your own network, writes) and the research workflows (post engagers, keyword post search, watchers, research columns): the `oxygen-signals` skill, `references/public-research.md`. This runbook is the provider underneath.

## Discover by intent

`oxygen tools search` (MCP `oxygen_tools_search`) finds provider operations such as `scraper.linkedin_post_reactions`; `oxygen_capabilities_search` finds callable MCP tools. Inspect the winning descriptor every time: its input schema, `when_to_use`, `when_not_to_use`, `prefer_over`, current price, availability, pagination and output shape.

```bash
oxygen tools search "public LinkedIn profile" --json
oxygen tools search "cookieless LinkedIn company lookup" --json
oxygen tools get scraper.linkedin_profile --json
```

## Person and company enrichment

- Managed person enrichment takes a public profile URL, `public_identifier`, or `profile_id` (a member ID or URN from search or engagement). A public URL takes precedence when supplied with an ID. Keep opaque IDs in `profile_id`, with their original case.
- Managed company enrichment takes a website `domain`, or an exact LinkedIn company URL, slug or id. A company-name `search` needs HarvestAPI BYOK.

```bash
oxygen tools run scraper.linkedin_profile --input-json '{"url":"https://www.linkedin.com/in/satyanadella/"}' --credential-mode managed --mode dry_run --json
oxygen tools run scraper.linkedin_company --input-json '{"domain":"microsoft.com"}' --credential-mode managed --mode dry_run --json
```

A dry run validates and prices the request and proves `meta.provider_call: false`; it does not fetch the record or guarantee a match. Read `output_schema` before building a Table or Workflow on it. One known record can use the tool directly; repeated rows belong in a tool column (or the `person_enrich` and `company_enrich` presets), and multi-page work in a table-backed run, so credits, pagination, retries and provenance stay inspectable. MCP: `oxygen_tools_run_dry` with the same `input` and `credential_mode: "managed"`, then `oxygen_tools_run_live` with the approved ceiling.

## Managed-mode limits

A descriptor field whose description starts `HarvestAPI BYOK only.` is refused in managed mode before any spend; the description names the managed replacement when there is one. Managed lead search filters location by `geo_ids` (numeric LinkedIn geo ids) or a pasted `sales_nav_url`; its `locations` text is HarvestAPI BYOK only, as is geo-id search. Managed comments accept only `sort_by: "date"`. Ad lookup and search, group lookup and search, service search, comment replies and comment reactions need HarvestAPI BYOK. Report an unsupported managed filter; never drop it silently to make a request run.

## HarvestAPI BYOK

```bash
oxygen integrations connect scraper --json
oxygen tools run scraper.linkedin_profile --input-json '{"url":"https://www.linkedin.com/in/satyanadella/"}' --credential-mode user_api_key --mode dry_run --json
```

The credential-less connect call is a free `needs_api_key` preview: open its `web_url` and supply a direct HarvestAPI key under Connections, Professional Network Data, HarvestAPI API key (an Apify token is not a HarvestAPI key). The key is encrypted and workspace-scoped, and BYOK needs a paid plan. Select `user_api_key` explicitly for both the preview and the live call (MCP `credential_mode: "user_api_key"`). HarvestAPI calls consume the customer's HarvestAPI balance; missing or invalid BYOK credentials fail instead of falling back to managed, and managed mode never uses the customer's HarvestAPI key.

## Approval

Every live `scraper.*` call is an external provider read. Before it runs, show the exact tool ids, the identifiers or URLs, the credential mode, the row, page and result scope, a dry run and a ceiling derived from the descriptor, and get explicit approval; a request to research or plan is not approval. A HarvestAPI call still consumes the customer's upstream balance when OXYGEN charges nothing for it.

Never copy scraper prices into prompts, workflow definitions or notes: vendor costs change independently of skills. Fetch the current descriptor with `oxygen tools get <scraper.tool_id> --json` and dry-run the exact request before proposing a ceiling.
