# Import, deduplicate and organize

## Where a table can start

`oxygen tables sources --json` lists every way a table can start (imports, company, people and signal sources, webhooks, Functions) with the provider count and per-row credit estimate behind each, free. Searches and planners belong to the `oxygen-sourcing` and `oxygen-signals` skills; a HubSpot list or Pipedrive filter import, and a copy of your own Records object or saved view (`tables records import`), are in `oxygen-crm`.

## Import a file or a link

```bash
oxygen tables import --file ./accounts.xlsx --create "Target Accounts" --background --json
oxygen tables import target-accounts --file ./accounts.csv --upsert-key domain --background --json
oxygen tables import --create "Event list" --url <https-link> --preview --json
```

- `--create` infers column types from the file (CSV, JSON, JSONL, XLSX; `--sheet` picks a sheet). `--url` imports a public CSV, JSON or XLSX link or a Google Sheet; `--preview` shows it first for 0 credits. `--project <folder>` chooses where a new table lands.
- `--upsert-key` writes every column the file carries, so a blank cell clears the stored value. For a partial update in one file, add `--skip-blank-cells` (MCP `skip_blank_cells` on `oxygen_tables_import_staged` and `oxygen_tables_import_csv`): a blank cell then leaves the existing value alone. It works on `--file` imports, not `--url`.
- In Claude Desktop, call `oxygen_cli_file_import_prepare` on the local path and run the command it returns; never stream file rows through MCP.
- A background import returns an ingestion run: read it with `oxygen table-ingestions get <run_id> --json` before any enrichment.
- **Verify the row count against the source before anything paid.** A short table is a partial import: retry with a smaller `--batch-size` or `--background`, or report it. The table is the system of record; a CSV is only a staging or export file, and a CSV-only enrichment phase hides work from runs and provenance.

Moving a spreadsheet-style export from another tool: import the rows without changing the source columns, add OXYGEN columns beside them, pilot one row per mapped action, compare the pilot with the source values, then run bounded batches. Promise no parity with the source system until a representative pilot was compared. Clay has its own walkthrough: the `oxygen-clay-migration` skill.

## From a provider page

When a provider operation returns rows with a cursor, import its pages as a durable ingestion so every page and item stays inspectable:

```bash
oxygen tools run blitzapi.company_search --mode dry_run --input-json '{"company":{"hq":{"country_code":["US"]}},"max_results":50}' --json
oxygen table-ingestions create-tool-page accounts --tool blitzapi.company_search \
  --request-json '{"company":{"hq":{"country_code":["US"]}},"max_results":50}' --rows-path response.results \
  --row-mapping-json '{"company_name":"name","domain":"domain","linkedin_url":"linkedin_url"}' \
  --max-pages 1 --max-credits <estimate_x_pages> --upsert-key domain --json
oxygen table-ingestions wait <run_id> --timeout-seconds 600 --json
oxygen table-ingestions items <run_id> --status failed --json
```

A paid tool needs `--max-credits`; without it the import is refused before anything runs and the refusal names the estimate. Prefer the company and people planners when one fits: they choose the route, keep fallbacks and create the table for you.

## Follower orders

`oxygen tables followers check --company <linkedin_company_url> --credential-mode user_api_key --json` previews for free; when the platform fee is positive, it leaves the follower count unknown. On your key, the placement fee is separate from later paid polls and result pages; ScrapeLi bills its provider cost separately. The quoted `max_*` fields describe the nominal recovery schedule, while your approved total ceiling is the hard bound. Failed or interrupted attempts retain allocation and may consume more than the nominal schedule.

After approval, place one order with `oxygen tables followers order --company <linkedin_company_url> --credential-mode user_api_key --request-id <uuid> --approved --max-credits <chosen_total_ceiling> --json`. A ceiling equal to the placement fee is accepted but stops before the first paid recovery call. Exhaustion stops automatic recovery; it does not increase authority or refund an allocation. Budget exhaustion lands no partial rows. A later attempt can refetch paid pages and consume more of the same approved ceiling.

For fee-budgeted own-key orders, inspect without a provider call using `oxygen tables followers status --request-id <original_uuid> --json`. Add `--table-id <saved_table_id>` to verify its Table binding. MCP uses `oxygen_tables_followers` with `action: status`, the same original `request_id`, and optional `table_id`. Both use the workspace-scoped GET read, including interrupted setup before a Table exists. Read allocated attempts, recorded fees and unconfirmed calls separately; recorded fees settle through the normal billing cycle.

Keep the identical payload and original request ID after a timeout or failed setup. Rotating the saved key stops recovery pinned to that credential; an interrupted setup claim can remain unavailable. A saved Table or ingestion run alone does not prove provider acceptance. A new request ID can buy the audience again; inspect the original order before explicitly starting another. A duplicated Table retains provenance and does not inherit the original order's fee budget.

## Duplicates

```bash
oxygen tables dedupe <table> --on email --normalize email --json
oxygen tables dedupe <table> --on email --normalize email --keep most-complete --merge-values fill-empty --apply --approved --json
oxygen tables auto-dedupe set <table> --on email --normalize email --json
```

The first call previews; `--apply --approved` removes duplicates (deleted rows stay in row history; `--keep oldest|newest|most-complete` picks the survivor). Auto-dedupe scrubs every future write (insert, import, webhook) before any enrichment can spend on a duplicate; `tables describe` shows it under `standing.auto_dedupe`. Enriching a duplicate costs the same as enriching a real row, so dedupe first.

## Link two tables

`oxygen tables link` adds a relation between two tables (a contact row to its account row) so prompts and filters can read across it; linking plain tables never registers CRM objects. Keep people in a Contacts table linked to an Accounts table by `account_domain` or a row link, one-to-many or historical facts (signals, events) in their own table, and only current per-account summaries on the account row. Upsert on a stable key: `domain` for accounts, `linkedin_url` or `email` for people, and a deterministic key column (a formula over domain, type, date and source URL) for events.

## Folders

Table folders are `projects`. Create one with `oxygen projects create`, list them with `oxygen projects list --json` (each carries `tableCount`), and read one with `oxygen tables list --project <folder>`. `oxygen tables move <table> [<table>...] --project <folder> --json` moves several tables in one call; rows, columns, runs and provenance stay with each table.

**Deleting a folder deletes its tables.** Preview `oxygen projects delete <folder> --json`, quote the loss (`row_count` across `tables`) and the deadline (`purge_scheduled_at`), and after approval pass `--live --confirm --expected-table-ids <comma-separated preview ids>`; changed contents need a new preview. Until `purge_scheduled_at`, `oxygen tables restore <table>` brings a table back with its folder. General and CRM-backed tables stay protected.

## Registering the result

`oxygen session output --table <table> --label "<what it is>" --json` registers the table as the deliverable of the session, so the table, not a file, is what the user opens.
