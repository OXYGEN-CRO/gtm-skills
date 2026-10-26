---
name: oxygen-table-tidy
description: "Tidy an OXYGEN Table: inspect duplicate columns, ordering, formatting, types, hide/archive candidates, and suspicious values; present findings by category; then apply only approved reversible fixes. This is table structure and cell formatting, not CRM record deduplication or merge."
allowed-tools: Bash(oxygen *)
---

# OXYGEN Table Tidy

Removing rows: read `oxygen skills get oxygen-tables --json`, then hydrate `oxygen commands get "tables rows remove-selection" --json`. Removal is permanent and requires approval for the exact scope.

1. Select the Table and hydrate the exact interface below. Run tidy suggestions read-only; they cost 0 credits and change nothing.
2. Present every finding category separately: duplicate/overlapping columns, order, type, formatting, hide/archive suggestions, and value sanity.
3. Ask for per-category approval; “tidy it” is not blanket permission to archive or rewrite data.
4. Apply only approved changes through native scoped primitives: hide/show, reorder, archive/restore, retype, or add a cleaned/formula column.
5. Re-describe the Table, report the reversible changes, and return its deep-link.

## CLI and MCP

CLI: `oxygen commands get "tables tidy-suggest" --json`, then
`oxygen tables tidy-suggest <table> --json`. MCP: hydrate
`oxygen_tables_tidy_suggest` with `oxygen_capabilities_schema`, then call it with
`{"table":"<table>"}`. Optional `limit` samples 1–5000 rows; `categories` is an
array of `duplicates`, `formatting`, `hide`, or `valueSanity` (CLI:
`--categories <csv>`). Omit categories for all checks.

Hydrate only the chosen fix's command or MCP schema before approval:

| Fix | CLI command | MCP tool and fields |
|---|---|---|
| Hide/show | `columns update <table> <column> --hidden-by-default` / `--no-hidden-by-default` | `oxygen_columns_update`: `table`, `column`, `hidden_by_default: true` / `false` |
| Reorder | `columns reorder <table> <column> --position <n>` | `oxygen_columns_reorder`: `table`, `column`, zero-based `position` |
| Retype | `columns retype <table> <column> --data-type <type>` | `oxygen_columns_retype`: `table`, `column`, `data_type` |
| Archive/restore | `columns archive` / `columns restore` | `oxygen_columns_archive` / `oxygen_columns_restore`: `table`, `column` |

Prefix CLI commands with `oxygen`; add `--json`. Hide/show, reorder and retype
support `--dry-run` / MCP `dry_run: true` before the approved write. Hiding does
not need archive or delete. Read back with `oxygen tables describe <table>
--json` or `oxygen_tables_describe` with `{"table":"<table>"}`; verify the changed
column's `hiddenByDefault`, position or type. Use `include_archived: true`
(CLI `--include-archived`) to inspect an archived column.

If a native MCP tool is outside the active pack, use `oxygen_capabilities_read`
for reads or `oxygen_capabilities_call` for writes with `{tool, arguments}`
after hydrating its schema. A dispatcher never supplies approval.

## Value cleanup helpers

Step 4's cleaned column is a catalog template, never a hand-written expression:
it adds a column instead of touching the source. `oxygen columns catalog
--category normalize` lists the free ones (company name, job title, email type;
`--category organize` adds text to list) and prints the exact add command. Dead
domains: `--preset domain_check`, 0.1 credits/row, cached 30 days.

MCP uses `oxygen_columns_catalog` with `category: "normalize"` or `"organize"`,
then the selected `oxygen_columns_add` schema. Load deeper column/spend guidance
only when needed: `oxygen skills get oxygen-tables --file
references/templates.md --json`, or `oxygen_skills_get` with
`{"name":"oxygen-tables","file":"references/templates.md"}`. `file` is the exact
manifest-relative path; omit it to read the selected skill's entrypoint and index.

For empty CRM enrichment fields or Open Deal / Account Stage questions, load the
`oxygen-crm` skill's `references/data-model.md` only when needed:
`oxygen skills get oxygen-crm --file references/data-model.md --json`, or
`oxygen_skills_get` with `{"name":"oxygen-crm","file":"references/data-model.md"}`.
Keep the CRM guide's preview, approval and credit ceiling before any paid repair.

## What a Table opens on

Two independent things narrow it, and a tidy pass must not confuse them:
**`hiddenByDefault`**, the workspace's curation, reported per column by `tables
describe --json` and changed with `columns update <table> <column>
--hidden-by-default` / `--no-hidden-by-default`; and the per-user empty-column
collapse. A column can be blank and still be in the opening set.

Hidden is not archived — `tables describe`, `tables query --fields`, the record
page and every API still return it, and a hidden payload is still read by the
columns derived from it. Prefer hiding to archiving.

Do not merge CRM records, delete source evidence, overwrite raw values when a derived cleaned column is safer, or run paid AI/provider cleanup without a separate preview and cap.
