# Functions

Use a Function when the reusable unit is one row moving through a known set of table columns and returning named values to the caller. Use a hosted workflow instead when the motion needs schedules, event triggers, branches, approvals between steps, or non-table orchestration.

A Function is a capability on an ordinary table, not a new folder or table kind. The backing table remains visible and inspectable; publishing adds a Function badge and a versioned contract.

## Start with the workspace library

`oxygen functions list --json` lists the workspace's own drafts and published Functions. Describe a relevant Function before building another: `oxygen functions describe <function> --json`. The same library appears in Tables → Functions and **+ Add column → Functions**.

Each entry carries a `credit_estimate`: `shape` is `fixed`, `estimated` (an expected average and a worst-case figure), or `variable`. Its `label` is ready to show a person. Attaching is free; preview the bound column before a paid run.

Favourites are per person: `oxygen functions favorite <function>`, `functions list --favorites`, and the Favorites tab in Tables → Functions. From MCP use `oxygen_callables_manage` with `operation=list_functions`, optionally `filter=favorites`, and `operation=favorite|unfavorite|duplicate` with `function`. Duplicating returns an editable draft with the same inputs, steps and outputs.

## Compose enrichment and qualification

Inspect the existing library before creating another Function. Keep company facts,
company fit, contact facts and persona fit as separately reusable contracts. A
priority Function consumes their saved outputs, so a rubric change does not require
buying the source data again. Record the source and assessment versions with the
result. Company size may change the route without reducing company relevance;
persona fit does not establish budget, authority or intent to buy.

Create manual caller columns for the named outputs, then bind each module with
explicit mappings. Missing identity, unknown fit, failed assessments and unresolved
reviews should remain visible holds. Do not turn missing evidence into zero fit or
make a priority tier authorize outreach. Formula-only prioritization costs zero
credits, but the Function contract still requires a positive per-item ceiling.

To avoid unnecessary enrichment, configure a formula run condition on the
enrichment column. A false condition is recorded as `run_condition_false` before
provider preparation or dispatch. Preview estimates can still cover the selected
rows; inspect run and cell outcomes for actual skips and cost.

## Draft and publish Determine ICP

First inspect the backing table. Each public input/output points to a real backing-table column; each action is an existing executable column.

For formula steps, validate representative rows before attaching or publishing. Formula string literals consume escapes: a regex backslash must be doubled in the formula source, and doubled again inside JSON. For example, the formula source `regex_replace(company_name, "\\s+", " ")` is encoded as `{"version":1,"expression":"regex_replace(company_name, \"\\\\s+\", \" \")"}` in `--definition-json`. Inspect the sample outputs; syntactic validation alone cannot establish that a pattern expresses the intended cleaning rule. A positive per-item ceiling (for example `1`) is still required for a formula-only Function, even when its estimate and actual usage are zero. A formula column computes when read, so `tables query` shows its values without a run; `columns run` skips rows that already store a value (`existing_value`), and `--force` refreshes them.

```bash
oxygen tables describe determine-icp --json

oxygen functions draft --definition-json '{
  "table":"determine-icp",
  "display_name":"Determine ICP",
  "inputs":[
    {"key":"domain","column":"company_domain","required":true},
    {"key":"company_name","column":"company_name","required":false}
  ],
  "action_columns":["determine_icp","normalize_icp_output"],
  "outputs":[
    {"key":"decision","column":"is_icp","required":true},
    {"key":"reason","column":"icp_reason","required":false}
  ],
  "default_max_credits_per_item":1,
  "default_max_items":100
}' --json

oxygen functions list --json
oxygen functions describe <function_id> --json
oxygen functions publish <function_id> --expected-draft-hash <draft_hash> --json
```

`required:true` is enforced before rows are enrolled. Optional inputs may be unmapped or empty. Outputs default to required unless explicitly marked optional. Oxygen calculates the managed-credit estimate from the current action-column/provider pricing; an unknown or variable lane stays visibly variable rather than accepting a hand-entered quote. Creating or saving a draft executes nothing and leaves the published version unchanged. Inspect the draft, contract and credit posture before publishing: use `function.draft.contentHash` from the returned data as `<draft_hash>`. Publishing updates every caller automatically for future invocations. Queued, in-flight and past runs retain the version captured when they were enrolled. Existing caller credit caps never rise automatically; an incompatible mapping or insufficient cap fails closed.

To edit later, pass the Function id to `oxygen functions draft <function_id> --definition-json '{...}' --expected-draft-hash <draft_hash> --json`, inspect it again, then publish the new draft hash. Until the first publish, the draft is addressed by its backing table id; publishing mints the Function id that bindings and runs record. Both ids keep resolving afterwards, as do the slug and display name, and the backing table remains an ordinary editable Table.

## Bind it to a caller table

Create the callback target columns first, then bind public input/output keys explicitly. An input may reference a whole column or a nested JSON value: `{"domain":"profile.company.domain"}` reads the domain inside the `profile` column. Output mappings name existing caller columns; bind rejects a missing target:

```bash
oxygen functions bind accounts <function_id> \
  --key determine_icp_function \
  --label "Determine ICP" \
  --inputs-json '{"domain":"company_domain","company_name":"company_name"}' \
  --outputs-json '{"decision":"is_icp","reason":"icp_reason"}' \
  --max-credits-per-item 1 \
  --overwrite-policy empty_only \
  --json
```

The same bind is a row in the web app under **+ Add column → Functions**: pick your Function, use the column reference picker to select a column or nested JSON value for each input, and choose where each output lands (a new column by default). The web configuration has no credit-cap field; the Function's existing per-row limit remains enforced. Adding runs nothing and opens the column editor, where you can choose **Run for first 10 rows**. `oxygen tools search --for-table <table> --json` lists every published workspace Function as a `function:<id>` entry with its per-row price, its `inputs`, its `outputs` and the publisher's `default_max_credits_per_item`, which is everything the flags above need.

The binding is stored as a tool column and appears with a **Function** label in the web Table. Inspecting it shows the Function name and destination columns for its outputs; run details show the Function identity and version captured for that run. It follows the Function’s published version for future invocations, maps caller columns to named inputs, maps named outputs back to exact caller columns, and stores the per-enrolled-row cap. Each invocation captures its own immutable version; publishing a draft does not rewrite that history. `empty_only` protects human-entered callback targets; use `overwrite` only when the user explicitly wants the function to replace existing values.

## Preview and run

The normal column-run surface executes the binding. Always dry-run first:

```bash
oxygen columns run accounts determine_icp_function --limit 1 --dry-run --json
```

The preview returns selected item count, estimated total and per-item managed credits, variable-pricing posture, total cap, per-item cap, mappings, and whether approval is required.

For a paid function, obtain explicit approval for the shown scope and cap, then run:

```bash
oxygen columns run accounts determine_icp_function \
  --limit 1 \
  --background \
  --approved \
  --max-credits <recommended_max_credits> \
  --json
```

Oxygen creates one backing-table row per caller row and runs the Function’s captured action columns over those rows. Each invocation records both rows so its named outputs return to the correct caller. Inspect the run to see its captured version, progress, cost and any failed callback.

A run condition on the binding column is enforced at enrollment: caller rows whose condition is false are never enrolled or billed, and the preview and run responses report them as `skipped_run_condition` next to the `run_condition` expression that excluded them. Gate a second Function on the first one's output this way (for example `company_qualified = "qualified"` on a person-qualification binding). A selection where every row is skipped fails with `empty_callable_selection` and that count.

The call is visible from the caller table itself. Its Runs history (`oxygen table-runs list --table <caller> --status all --json`, or the table's Runs page) lists every Function run launched from that table, including runs made before this history existed, and each run's link opens under the caller table's URL. The binding column's own cell receives an outcome envelope — `status`, `function`, `outputs`, `credits_used`, `invocation_id`, `action_run_id`, `written_columns`, `overwrite_policy`, `overwritten_columns` (filled cells the run replaced), `kept_columns` (filled cells `empty_only` left as they were), and `error` when the call failed — so `oxygen tables query <caller> --fields <binding_column>` and the grid show what ran, not only the mapped output columns. To list exactly the rows one run touched, filter on a key inside that cell: `oxygen tables query <caller> --filter-tree-json '{"type":"group","conjunction":"and","children":[{"type":"leaf","columnKey":"<binding_column>","path":"action_run_id","operator":"is","value":"<run_id>"}]}' --json` (use `path` `outputs.decision` to filter on a returned value).

Both ceilings are enforced: `max_credits` for the invocation and `max_credits_per_item` across all ordered steps for one enrolled row. A callback also fails closed if a required output is missing or the recorded row spend exceeds its cap.

Inspect the returned table-run deep-link, or use:

```bash
oxygen table-runs get <action_run_id> --json
oxygen cells history accounts <source_row_id> determine_icp_function --json
oxygen functions describe <function_id> --json
oxygen functions runs <function_id> --json
```

## Rename or remove a Function

The Functions library has a three-dot menu with **Edit draft**, **Rename**, and **Delete**. CLI equivalents:

```bash
oxygen functions rename <function_id> "Enrich company" --json
oxygen functions delete <function_id> --json
oxygen functions delete <function_id> --yes --json
```

Rename preserves the Function identity, callers and published execution. Inspect a fresh draft hash before saving or publishing again. Delete without `--yes` previews removal and names every column that calls the Function. Callers do not block deletion: after it, each of them fails its next run with `function_deleted` and keeps the values it already wrote, so tell the user which columns stop running before confirming. Only the Function's own active runs block deletion; wait for them to finish. Deletion removes the Function from the reusable library and preserves its backing table, rows and captured run history. Deleting a Function you authored is final: there is no restore command for it, unlike `tables delete` and `tables restore`. To reuse the logic, duplicate the backing Table with `oxygen tables duplicate` and draft a new Function from the copy.

From MCP, inspect `oxygen_callables_manage` (compatibility identifier, titled **Manage Functions**). `list_functions`, `describe` and `runs` read without executing; `create_draft|save_draft|publish|bind|rename|delete|set_status` mutate configuration. Read with `oxygen_capabilities_read` and `{tool:"oxygen_callables_manage",arguments:{operation:"runs"}}` (also `list_functions` and `describe`); every other operation goes through `oxygen_capabilities_call`, because the combined tool carries write annotations. Each `runs` entry carries `binding`: the overwrite policy, output mapping and run condition that run captured, which can differ from the column's current definition. Functions belong to the `tables` pack. Pass `function` for an existing Function, `display_name` for rename, and `approved:true` to confirm a reviewed deletion. Publish requires `expected_draft_hash` from inspection. Run a binding with `oxygen_columns_run` after its dry run and approval. Legacy `oxygen callables` commands and MCP `operation=list` / `callable` arguments remain supported.
