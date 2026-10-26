# Trace One Cell Or Row

**Answers one question: "Why is this cell/row wrong, empty, or stuck — and where did this value come from?"**

Use this when the user points at a *specific* cell or row ("this company's revenue is blank", "why does this contact show the wrong title", "this row never enriched"). You are tracing provenance for one value, not sweeping a whole table — that is [error-sweep.md](error-sweep.md).

Work from the value outward: inspect the cell, read its history, then follow it back to the run that wrote (or failed to write) it.

## 1. Inspect the cell (read-only, free)

Start here. One call returns the current value, the column's kind/type, the row's other fields for context, recent change history, and — when the row arrived via a table webhook — its inbound provenance:

```bash
oxygen cells inspect <table> <row_id> <column> --json
```

Read the envelope in this order:

| Field | What it tells you |
| --- | --- |
| `cell.value` | What is actually stored right now (null/empty is a real answer — the value was never written). |
| `column.kind` / `column.data_type` | Whether this is a manual, formula, AI, or tool/enrichment column. A blank *tool* column points at a run; a blank *formula* column points at its inputs. |
| `row.context` | The row's other columns — check that the **inputs** a formula/enrichment needs (e.g. `linkedin_url`, `company_domain`) are present and well-formed. A missing input is the most common cause of a blank output. |
| `history` | Recent changes to this cell, newest first — did a value ever land and get overwritten, or was it never set? |
| `row.webhook_provenance` | Present only when the row came from a table webhook: the delivery that created it. |
| `deep_link` | `https://oxygen-agent.com/tables/<table>?cell=<row_id>:<column_key>` — open the cell in the web app. |

**What `cells inspect` cannot tell you:** which provider attempt produced the value, how many credits it cost, or why a run failed. It shows the *what*, not the *run*. For that, continue to step 3.

## 2. Widen to the row (optional)

If more than one cell on the row looks wrong, or the row itself seems stale, read the row's change history:

```bash
oxygen rows history <table> <row_id> --json
```

This shows every recorded change to the row over time — useful for "was this row ever touched by a run?" and "did an import or sync overwrite it?". For a single cell's timeline specifically, `oxygen cells history <table> <row_id> <column> --json` is the narrower view.

## 3. Follow it back to the run

A blank or wrong value on a tool/enrichment/AI column was produced (or should have been) by a **table action run**. Find and open that run:

```bash
# The run id usually comes from the column's last run, the session output, or a table-runs listing.
oxygen table-runs get <run_id> --json
```

Then pinpoint what happened to *this row* inside the run:

```bash
oxygen table-runs items <run_id> --status failed --json     # did this row's item fail?
oxygen table-runs provider-summary <run_id> --json          # provider attempts, upstream events, credit capture/release
```

- `table-runs get` gives run status, selection, counts, and the run `web_url` (`https://oxygen-agent.com/tables/<table>/runs/<run_id>`).
- `table-runs items --status failed` lists the row items that errored, with the per-item error text — this is where "stuck" resolves into a concrete failure code.
- `table-runs provider-summary` is the money view: which provider was tried, whether the upstream call succeeded, and whether credits were reserved, captured, or released. A released reservation with no value means the provider returned no match — not a bug.

**Epistemic honesty:** if the item is `completed` but the value is still empty, the provider genuinely found nothing for that row's inputs — retrying the same inputs will not help. If the item `failed` with a transient/5xx code, [error-sweep.md](error-sweep.md) covers requeuing.

## Deep-link guidance

Always hand the user a link so they can see it themselves:

- **The cell** → the `deep_link` field from `cells inspect` (`.../tables/<table>?cell=<row_id>:<column_key>`).
- **The run that wrote it** → the run `web_url` from `table-runs get` (`.../tables/<table>/runs/<run_id>`).
- **The table** → `https://oxygen-agent.com/tables/<table>`.

Do not fabricate a link — surface the one the envelope returned.

## MCP equivalents

Every step here has an MCP twin, same arguments, same envelope:

| CLI | MCP tool |
| --- | --- |
| `oxygen cells inspect` | `oxygen_tables_cell_inspect` |
| `oxygen cells history` | `oxygen_tables_cell_history` |
| `oxygen rows history` | `oxygen_rows_history` |
| `oxygen table-runs get` | `oxygen_table_runs_get` |
| `oxygen table-runs items` | `oxygen_table_runs_items` |
| `oxygen table-runs provider-summary` | `oxygen_table_runs_provider_summary` |

## Combines with

- **[error-sweep.md](error-sweep.md)** — when the same failure repeats across many rows, stop tracing one cell and sweep the whole table.
- **[optimize-credits.md](optimize-credits.md)** — when the trace shows the value cost more than expected, or a provider was retried repeatedly.
- **[runs-and-limits.md](runs-and-limits.md)** — ingestion runs, plan and credit refusals, limits and spend ceilings.
