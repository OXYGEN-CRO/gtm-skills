# CRM import (inbound, import-first)

Five CRM directions:

- **A whole CRM object into Records** (this page, the Flow below): every HubSpot, Attio or Pipedrive record of one object becomes an OXYGEN record with provider-id provenance. It has no list or segment filter.
- **One HubSpot saved list or Pipedrive saved filter into a new working Table**, do-not-contact first: `oxygen tables hubspot import` / `oxygen tables pipedrive import` (the next section). Tables are disposable work to enrich and sequence from; Records are canonical truth matched on a natural key. The create-table picker (`oxygen tables sources`) offers both as **Import from HubSpot** and **Import from Pipedrive**.
- **OXYGEN rows mirrored out, or HubSpot and Attio kept converged:** [sync](sync.md).
- **Your own Records (an object or saved view) into a new working Table**, once or kept in sync: `oxygen tables records import` ([below](#copy-your-own-records-into-a-working-table)). The copy is free; Records stay canonical.
- **Native table rows into native contacts**, no external CRM (a CSV lead list becoming people records): [bind and promote](promote.md).

Imports read from HubSpot, Attio and Pipedrive (connected with a personal API token). Salesforce has no integration. Pipedrive persons, organizations and deals import. Import persons and organizations before deals: each deal links to its person and organization only when those are already in OXYGEN, and the import reports `links_not_imported` for the rest. Re-running the deals import after importing them adds the missing links.

## Copy your own Records into a working Table

To work a slice of the CRM you already have in OXYGEN ("turn my open-deals view into a table that stays current"), copy it rather than re-importing from HubSpot or Pipedrive:

```bash
oxygen tables records import --object deals --view "Open deals" --dry-run --json          # free: record count + columns
oxygen tables records import --object deals --view "Open deals" --refresh sync --approved --json   # create; daily@6 sync by default
oxygen tables records status <table> --json                                              # source, last sync counts, schedule
oxygen tables records sync <table> --json                                                # copy again now; keeps the schedule (--refresh once stops it)
```

- One-way: Records never change. Rows key on `record_id`. Columns are the view's chosen columns, or every field of the object when it chooses none.
- Cells edited in the Table and columns you add are kept on every sync; `preserved_cells` counts the edited copied-field cells a sync left alone.
- Arming the schedule (`--refresh sync`) is a standing charge per sync and needs `--approved` (MCP `approved: true`); a dry run and a one-time copy need none.
- A record that leaves the view stays as a row with `in_records=false`; nothing is deleted.
- The saved view is re-read on each sync; up to 20,000 records. The copy is 0 credits; each scheduled sync bills one workflow step (`credits_per_scheduled_sync` in the dry run).
- MCP: `oxygen_tables_records_import`, `oxygen_tables_records_sync`, `oxygen_tables_records_status`.
- Writing Table work back onto Records is a separate, explicit step: [bind and promote](promote.md).

## Import a CRM list into a new table (with a do-not-contact sync first)

The usual first ask, "get the people from my HubSpot list or Pipedrive filter into a table I can work, and make sure nobody who opted out is ever contacted", is one command per CRM. Both preview for free, both require an affirmative choice about suppression, and both arm a bounded durable Workflow (once, or on a schedule) that never enrolls or sends.

```bash
# HubSpot: saved contact lists. `lists` shows the ids; `import` previews, then runs with the reviewed fingerprint.
oxygen tables hubspot lists --json
oxygen tables hubspot import --list <lead_list_id> --dnc-list <dnc_list_id> --max-credits <run_cap> --json          # free dry run → fingerprint
oxygen tables hubspot import --list <lead_list_id> --dnc-list <dnc_list_id> --max-credits <run_cap> --live --approved --reviewed-fingerprint <fp> --json

# Pipedrive: saved FILTERS (Contacts → People → Filters), connected with a personal API token.
oxygen integrations connect pipedrive --api-key <token> --json     # Pipedrive → Settings → Personal preferences → API
oxygen tables pipedrive filters --json                             # quote for reading filters + fields; no provider calls before approval
oxygen tables pipedrive filters --approved --max-credits <catalog_cap> --json  # only after approval of the returned catalog quote
oxygen tables pipedrive import --filter <filter_id> --dnc-filter <unsubscribed_filter_id> --max-credits <run_cap> --json
oxygen tables pipedrive import --filter <filter_id> --dnc-filter <unsubscribed_filter_id> --max-credits <run_cap> --live --approved --reviewed-fingerprint <fp> --json
```

Rules that hold on both lanes:

- **The DNC sync happens first, and no row lands unless it fully succeeds.** "Import a DNC" means additive suppression through the shared do-not-contact ledger (`oxygen suppressions list`), never a table of DNC rows. Leaving the CRM list or filter later never un-suppresses anyone.
- **Skipping suppression is allowed but never silent:** pass `--no-dnc` (MCP: `no_dnc: true`) or the command refuses. The no-DNC preview has its own fingerprint, so approving one can never approve the other.
- **Quote external calls before approval.** A Pipedrive API token is your own key: each live provider call costs 0.05 OXYGEN credits after repricing takes effect, including filter/field discovery, DNC reads, imported pages and organization hydration. `filters` returns the current per-call fee and required catalog ceiling before any paid read. OAuth CRM calls follow their current tool quote. Live Workflow steps cost 0.05 credits each after repricing takes effect and count toward the spend ceiling then; provider billing is separate. Native Table/DNC writes within the run add no row-write fee. The CRM's API quota still applies. `--max-credits` is an OXYGEN spend ceiling, not a price or a row limit. A connection the plan does not include is refused with `upgrade_required`, naming the plan that includes it.
- **Pipedrive specifics:** a filter publishes no size, so `--max-records-per-filter` is enforced while it is read; a do-not-contact property (`marketing_status`) is not a suppression source, so save a Pipedrive filter on *Marketing status = Unsubscribed* and pass it as `--dnc-filter`; Pipedrive has no native title, domain or LinkedIn fields, so map them with `--person-linkedin-field`, `--person-title-field`, `--org-domain-field` (the `filters` output recommends keys by field name); phone numbers stored without a country code are counted, never guessed.
- **`crm sync import` takes the whole object; these lanes are segment-scoped.** "Bring in one of my HubSpot lists or Pipedrive filters so I can work it" is this lane, not the Records import. HubSpot suppresses from saved lists only: an opt-out *property* such as `hs_email_optout` is not a suppression source, so the user needs a list.
- If `tables hubspot lists` / `tables pipedrive filters` returns nothing, read its `empty_state`: it names the causes it cannot distinguish from outside (none saved, the token cannot see them, a rejected token) and the next move for each.
- MCP: `oxygen_tables_hubspot_lists|import`, `oxygen_tables_pipedrive_filters|import`. Web: `/tables/new?source=hubspot_import` and `/tables/new?source=pipedrive_import`.

## Core rule

Every imported record routes through the CRM assert path for identity dedup and a `sync_pulled` timeline entry. Objects that define `external_id` also retain a provider-ID mapping; a custom object without that definition still matches by its natural identity and retains provider evidence on the timeline. The import result reports mapping and timeline counts separately, including any entries that could not be recorded. Connected-CRM IDs require a natural identity because their IDs are local to the connected account; HubSpot and Attio IDs do not share a namespace.

Import-first is **last-write-wins**: the connected CRM is the source of truth for the fields it supplies, so each import overwrites the provider-sourced fields on the matched record, including any hand edits to those fields. There is no field-level merge on import.

## Flow

1. Confirm the CRM is connected and healthy before importing. A `needs_reconnect` or `health.status: error` connection is the most common cause of a failed import: surface it, never route around it.

```bash
oxygen integrations list --json   # hubspot/attio/pipedrive connected? status, health, reconnect_required
oxygen crm objects --projection compact --json         # the target OXYGEN object (people/companies) exists
```

If the provider is missing or in `needs_reconnect`/`error`, stop and send the user to `https://oxygen-agent.com/connections` to (re)connect before continuing.

2. Preview the import (dry run, the default). It validates the provider→object mapping and returns the approval and cap contract without pulling anything.

```bash
oxygen crm sync import hubspot --object contacts --into people --limit 200 --dry-run --json
```

The supported mappings are HubSpot `contacts`→`people`, HubSpot `companies`→`companies`, Attio `people`→`people`, Attio `companies`→`companies`, Pipedrive `persons`→`people`, Pipedrive `organizations`→`companies`, Pipedrive `deals`→`deals`. The natural identity key is `email` for people and `domain` for companies (a Pipedrive organization's domain comes from its own website or domain field, never from a person's email). A Pipedrive deal has neither, so it is keyed on `deal_key` = `pipedrive:<Pipedrive account id>:<deal id>` (Pipedrive calls its account a "company"; this is not an OXYGEN company or a Pipedrive organization), so it is scoped to the connected Pipedrive account; its title, value, currency, won/lost status and close date fill the deal.

3. Present the current pricing and approval before the live import. Own-API-key reads cost 0.05 OXYGEN credits per provider call after repricing takes effect, including each page; OAuth reads follow their tool quote. Live Workflow steps cost 0.05 credits each after repricing takes effect and count toward the spend ceiling then. Provider billing and the connected CRM's daily API quota are separate. Inspect the selected provider tool with `oxygen tools get <tool_id> --json` for its current quote. A mapping-only preview uses 0 credits on this request and reports an unknown (`estimated_credits: null`) complete-run total with current unit prices. The explicit spend ceiling is separate from that nullable estimate. A stored manifest quote is an immutable unit-price snapshot; refresh native preflight for current prices and cap coverage. The approval names:

- the provider and connected account;
- the provider object → OXYGEN object mapping and the row `--limit`;
- the provider-call and Workflow-step pricing, the `--max-credits` spend ceiling, and the separate row `--limit`;
- duplicate behavior: idempotent on the provider external id, last-write-wins;
- the web deep-link to inspect the run.

4. Run the live import after approval. It is a durable background workflow run (leased, resumable), never a request-time loop; a crash mid-import re-pulls without duplicating.

```bash
oxygen crm sync import hubspot --object contacts --into people --limit 200 --max-credits <n> --approved --live --json
```

An import started without that approval parks in `awaiting_approval` and resumes only after the matching plan-bound decision is recorded.

The customer-facing runtime is always the hosted durable Workflow. If execution reports an executor mismatch, fail closed and capture the run link and error; do not tell the customer to change an environment variable or move execution local.

5. Watch the run and inspect provenance.

```bash
oxygen crm sync status <run_id> --json                 # pulled/created/updated/skipped counts + run status
oxygen crm sync links <object> <row_id> --json         # the provider external ids mapped to one OXYGEN record
oxygen crm activity timeline <object> <row_id> --json  # the sync_pulled entry on the record's timeline
```

The run is also observable in the web app at its workflow-run URL (returned as `runUrl` / `web_url`).

## Refreshing

Edits in the connected CRM do not flow into OXYGEN by themselves: re-run the import to refresh, or keep HubSpot converged with the bidirectional [sync](sync.md). Attio syncs outbound only, so re-run the import to refresh Attio records.

## Failure handling

- A missing or ambiguous natural identity (no email or domain) on a pulled record is a graceful skip, never a run failure.
- A timeline (`sync_pulled`) write failure never fails the import: the record and its provider-id mapping are still written.
