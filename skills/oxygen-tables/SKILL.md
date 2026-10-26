---
name: oxygen-tables
description: "Build and run OXYGEN Tables: typed rows, choice fields, table links and lookups; AI, research, Classify, formula, tool, HTTP and template columns, reusable Functions, live feeds and webhooks, imports, follower orders, deduplication and folders. Covers pricing a column before it runs, one-row pilots, bounded batches and run reads."
allowed-tools: Bash(oxygen *)
---

# OXYGEN Tables

A Table is a hosted working dataset: typed rows and columns, cell state, provenance and run history. Records hold canonical CRM truth (`oxygen-crm`); a Table row is a candidate until it is promoted. Row dependencies stay chained columns; schedules, branches and approvals between steps are a hosted Workflow (`oxygen-workflow-authoring`), never a local loop.

## Pick the column

| Need | Column | Read |
| --- | --- | --- |
| Select or status fields, linked tables, lookups | `--type`, `--options`; `tables relate --to`; `--lookup-table` | [fields and links](references/fields-and-links.md) |
| Deterministic extraction, normalization, arithmetic | formula, free, evaluates on read (a bundle's fill-empty fields are stored) | [AI and formula](references/ai-columns.md) |
| Reasoning over what the row already holds: score, classify, summarize, draft | AI (`--prompt` with `{{column}}` tokens); Classify for closed labels | [AI and formula](references/ai-columns.md) |
| A fact that lives on the web, or on a page the row links to | Web Research Agent (`--kind research`, `--research-url`) | [research](references/research-columns.md) |
| A question OXYGEN already ships | template: `columns catalog`, then `--prompt-key` | [templates](references/templates.md) |
| One provider operation, or your own REST endpoint | tool column, HTTP API column, custom integration | [tool and HTTP](references/tool-columns.md) |
| Work email, phone, LinkedIn URL, company data, verification | enrichment presets and waterfalls: the `oxygen-enrichment` skill | — |
| Logic reused across tables | Function | [Functions](references/functions.md) |
| Rows that keep arriving | feed: webhook push or provider pull | [feeds](references/feeds.md) |
| Rows from a file, a link or a provider page; duplicates; folders | `tables import`, `tables dedupe`, `projects` | [import and folders](references/import-and-folders.md) |

An AI column has no web access: asked to check a website, it answers from the row and can invent. Use a research column for web facts.

## Run loop

1. Inspect: `oxygen tables describe <table> --json` for keys; `oxygen tables query <table> --fields <needed-keys> --limit 3 --json` for values. Filter with `--filter-tree-json`; `oxygen commands get "tables query" --json` retains its grammar (`is_empty`/`is_not_empty`, not `--filter-json`'s `is_null`/`is_not_null`).
2. Price for free: `oxygen tools search --for-table <table> --json` lists what this table's columns can fill, each with a per-row price and its add command; `oxygen enrichment catalog --json` is the price list by data type.
3. Add the column. `columns add` writes the definition only: it runs nothing and spends nothing.
4. Preview: `oxygen columns run <table> <column> --limit 1 --dry-run --json` quotes `expected_credits_per_row`, the worst case and `recommended_max_credits`, and for an AI column renders the prompt with one real row.
5. Pilot one row live after approval, read the cell and its `credits` receipt, then run bounded batches: `oxygen columns run <table> <column> --limit <n> --background --approved --max-credits <n> --json`. `--limit` fills next empty cells, not ranked cohorts ([selection](references/ai-columns.md#row-selection)); repeat until `row_count` is 0.
6. Wait with `oxygen table-runs wait <run_id> --json` and read `oxygen table-runs items <run_id> --status failed --json`. Read values back with `tables query <table> --fields <keys>`.

Large results: [bounded reads](references/fields-and-links.md#bounded-reads).

Balance, estimate and stop-after-pilot arithmetic: the `oxygen-gtm` skill, `guides/cost-precheck.md`. A stuck, failed or surprising run: the `oxygen-diagnostics` skill.

## Remove rows

Read the matching rows first with `tables query --filter-tree-json '<tree>'` (a text column matches with `is`, `is_not` or `contains`; `eq`, `gt` and `lt` are for numbers), then permanently delete the same scope with `oxygen tables rows remove-selection --table <table> --filter-tree-json '<tree>' --json`. The CLI takes the same tree as `tables query`; MCP `oxygen_table_rows_remove_selection` takes it as `filter_tree`. For a handful of rows, `--row-ids <id1,id2>` (MCP `row_ids`) deletes exact IDs. Removal costs 0 credits, and approval must cover that exact Table and scope. Every node of the tree must be readable, or nothing is removed. Read the survivors afterward. Deleting rows does not stop their campaign enrollment.

To add search, range or exclusions, pass `selection` with `mode: "all_matching"`, plus `filter_tree`, `search`, `range` and `excluded_row_ids`. A filtered browser view can pass its URL `f` value as `filter` (and its sort as `sort`) instead of `filter_tree`. Unqualified `all_matching` deletes every row. Removal executes immediately.

The removal answers with a compact receipt, so read it whole instead of clipping it:
- `scope`: the applied filter as a readable tree, or the exact IDs, plus `matched_row_count`.
- `effect_outcome`, `requested_row_count`, `deleted_count` and `missing_row_ids`.
- `run_id`: `oxygen runs get <run_id> --json` (MCP `oxygen_runs_get`) lists one `row_deleted` event per removed row.
- `readback`: the native reads that confirm the result.

Run the receipt's `readback` to confirm: the same filter should match nothing, and `tables preview <table> --summary-only` shows the survivors' count and fill. For a restorable copy, run `tables duplicate <table>` (0 credits) first. Removed values stay readable with `rows history <table> <row_id>` (MCP `oxygen_rows_history`).

## Gates

- **Approval and a ceiling for every paid run.** Show the row scope and the per-row estimate, get explicit approval, and pass a `--max-credits` read from the preview. A live paid run without `--approved` is refused. A ceiling is a ceiling, not a price; an unknown estimate means a one-row pilot, never "free".
- **External writes are their own approval.** An HTTP column's non-GET call, a CRM or outbound sync column and any provider write need `--approved` for that exact scope. Mirror every live external write's provider id, status and error back to the row.
- **Standing permission is bounded.** A feed's auto-run columns spend only under `--auto-run-max-credits`, a pull feed under its per-cycle `--max-credits`. Receiving rows is never permission to spend; arming a cadence or raising a ceiling asks again.
- **Own-key follower orders need a total platform-fee ceiling.** Approve placement and later paid recovery checks together under `--max-credits`; ScrapeLi bills separately. Keep the original request ID for inspection and retries. See [follower orders](references/import-and-folders.md#follower-orders) for the free preview and native status read.
- **Destructive changes preview first.** A folder delete names the tables, rows and purge deadline and needs the previewed ids; a Function delete stops every caller and cannot be restored.
- **Native, not scripted.** Loops over rows, joins, dedupes, imports, waiting and retries are Table features. A shell loop, a `jq` pipeline or a script around a command is a missing native capability: report it instead of building the workaround.

Return the table and run `web_url` with every result, and say what remains when a run covered only part of the table.
