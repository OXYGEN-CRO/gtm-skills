# Fields, choices, links and lookups

Everything the web column editor builds here, the CLI and MCP build the same way. Creating or editing these columns costs 0 credits and runs nothing.

## Plain fields and choice columns

A plain field is a column `type`, named as the web picker names it: `text`, `number`, `checkbox`, `date`, `json`, `markdown`, `image`, or a choice column: `select` (one choice), `multi_select` (several, stored as a list) or `status` (ordered stages that drive the kanban board).

```bash
oxygen columns add <table> --label "Stage" --type select --options "Lead,Contacted,Replied,Won" --json
oxygen columns add <table> --label "Tier" --type multi_select --options-json '[{"value":"vip","label":"VIP","color":"purple"}]' --json
```

MCP: `oxygen_columns_add` with `column: {label: "Stage", type: "select", definition: {options: [{value: "Lead"}, {value: "Won"}]}}`. `oxygen tables create --columns-json` (MCP `oxygen_tables_create`) takes the same `type` on each column, and `options` as well.

A cell stores the option's `value`; `label` is what the grid shows and colors are assigned unless you name one. Set a cell with `oxygen tables update <table> <row_id> --values-json '{"stage":"Won"}'` (a multi-select takes a list).

Replace a choice column's options with `oxygen columns update <table> <column> --options "Lead,Contacted,Won"` (MCP `oxygen_columns_update` with `options`). The list replaces the old one; cells keep the values they hold. To rename a choice, give the same `value` a new `label` with `--options-json`. To turn an existing text column into a choice column, add `--semantic-type select` (or `status`) in the same update; a multi-select stores a list, so first run `oxygen columns retype <table> <column> --data-type jsonb`.

## Link two tables

Linking makes a linked-record column on both tables, like the web's **Link to another table**. Matching values are not required, and plain tables never become CRM objects.

```bash
oxygen tables relate contacts --to accounts --json          # preview: names both columns
oxygen tables relate contacts --to accounts --live --json   # creates account on contacts, contacts on accounts
```

Running it again finds the same link instead of adding another. MCP: `oxygen_tables_relate` with `table`, `target_table` and `mode: "live"`. The result's `two_sided` is false when the target is a standard CRM object, which gets no column of its own.

Then link rows:

- One pair: `oxygen tables link contacts <row_id> --relation account --target-row-id <id> --live` (MCP `oxygen_tables_link`). Find the target row id with `oxygen tables query accounts --search "Acme" --json`.
- Every row with a matching value: `oxygen tables link contacts --to accounts --json` previews the measured match for free; add `--approved` to link them in a background run (MCP `oxygen_tables_link_bulk`). `--undo <workspace_run_id>` removes exactly what that run linked.
- Remove one link: `oxygen tables unlink contacts <row_id> --relation account --target-row-id <id> --approved`.

`oxygen tables relations list <table>` shows each link with its cardinality and link count; `oxygen tables relations update` renames one or changes its cardinality and `oxygen tables relations archive` removes it (MCP `oxygen_tables_relations` with `action`).

## Lookup columns

A lookup reads another table by a key and needs no link:

```bash
oxygen columns add <table> --label "Industry" --lookup-table accounts --lookup-match company_domain=domain --lookup-normalize domain --lookup-return industry --json
oxygen columns add <table> --label "Open deals" --lookup-table deals --lookup-match account_id=account --lookup-mode count --json
```

Modes are `first-match` (default; `--lookup-return` columns, `--lookup-order created_at:desc` to break ties), `count`, `exists` and `aggregate` (`--lookup-aggregate sum:amount`). The column's data type follows its mode. Edit one with the same flags on `oxygen columns update <table> <column>`: they apply over the saved lookup, and a new `--lookup-table` needs its `--lookup-match`. Reads resolve live from the source table.

## Bind rows to CRM records

```bash
oxygen columns add <table> --label "Company" --bind-object companies --bind-map domain=website --json
oxygen columns update <table> company --bind-map linkedin_url=company_li --no-bind-create --json
```

A bind column resolves each row to a CRM record by identity. `--bind-create` creates a record for rows with no match: a CRM write that needs an approved run.

## Bounded reads

Reads are compact by default. Raw queries return up to 20 rows within a 12,000-character envelope; follow `nextCursor` with the same selectors. A size refusal preserves the whole value: select fewer fields or use `oxygen tables rows inspect --table <table> --row <row-id> --field <key> --projection value --path /row/<key>/<nested-key> --json`, then its value cursor for continuation. MCP discovers `oxygen_table_row_inspect` through capability schema and read dispatch. Use `--full` for legacy query/run details, or query `--output <new-path>` to save a full page locally. Discover commands with `oxygen commands search <goal> --json`, hydrate the exact name, and use `oxygen formulas functions --query <term> --json` for relevant functions.
