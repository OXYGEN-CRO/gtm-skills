# Cost pre-check, pilots and honest reporting

Run this arithmetic **before** proposing any credit-consuming run, as part of the approval you present at the operating loop's `AWAIT_APPROVAL` stop, not after a run stalls. The server enforces the spend gates either way; this pre-check makes sure the plan you present is one the balance can complete.

## The three numbers

1. **Balance**: `oxygen billing balance --json` (MCP `oxygen_billing_balance`), the available credits minus anything reserved by in-flight runs.
2. **Unit estimate**, from where the per-item cost lives:
   - **Data types first.** `oxygen enrichment catalog --json` (MCP `oxygen_enrichment_catalog`; filter with `--intent`, `--group`, `--region`, `--status`) is the price list: one row per data type with `status`, `credit_estimate.credits_per_row` (expected, modelled on hit rates) next to `worst_case_credits_per_row` (up to), `coverage` and the add command. Name the data, never a provider. A `coming_soon` or `no_default` row has no add command on purpose.
   - **Then this table.** `oxygen tools search --for-table <table> --json` narrows the same list to what the table's identity columns can fill. Read each entry's `pricing_kind`: `fixed` is a list price every row pays; `estimated` with `estimate_basis: expected` is an average across a cascade; `ceiling` is the worst case (most rows pay less); `floor` is a lower bound across modes; `default_request` quotes the defaults for empty input. A Table row is one tool invocation, not one returned person.
   - **Provider tools.** `oxygen tools get <tool> --json` → the `cost` block (`pricing_model`, `managed_credit_estimate.min/max`, `billing_mode`, `scales_with`; `max: null` means no schema-bounded upper quote; with `quote_basis: default_request`, read `default_request_credits`). `cost_hint` is provider-native consumption with `customer_charge: false`. Quote the actual request with `oxygen tools run <tool> --mode dry_run --input-json '{...}'`, never `min`. BYOK tools bill the user's own key, so the external spend is real; read OXYGEN's current BYOK platform fee from the preview and `oxygen billing usage --meter byok_calls --json`.
   - **Waterfalls.** `oxygen enrich-column preview` (free) returns the per-row chain and credits. `credits_quote_basis: routed_lanes_blocked` means no lane can run now and the figures quote the column once the block lifts: never "0 credits" for a paid waterfall; name the block from `blocked_providers` as the thing to fix first.
   - **Search and sourcing.** The plan commands (`oxygen companies search plan`, `oxygen people search plan`) return per-route estimates before any live run.
   - **Table runs.** A `--limit 1` pilot's envelope carries a real `credits` receipt: the honest unit cost.
3. **Scope**: the row count the run will touch (a `tables query` count, or the plan's row estimate).

## The rule

`estimate = unit_estimate_max × scope`, compared with the balance **before** you present the approval:

- **Sufficient**: quote the arithmetic in the approval ("~0.4cr × 250 rows ≈ 100cr, balance 7,663cr") and propose `--max-credits` from the preview's `recommended_max_credits` (or about estimate × 1.5 when there is none).
- **Partial**: when the estimate exceeds the balance or the remaining standing budget (`oxygen budget list`), **stop and tell the user** instead of starting a run that will only partly complete. Offer the honest options: run the affordable slice now (state how many rows), top up first (`billing_url` from any paid envelope), or trim to cheaper lanes.
- **Unknown**: an undefined estimate or an unclear `pricing_model` does **not** mean free. Run a one-row pilot, read the receipt and scale from the real number.

## Standing caps stack with per-run caps

`--max-credits` caps one run; `oxygen budget list` shows org and table daily or monthly hard blocks on top. A run can be within its own cap and still blocked by a standing budget: check both for recurring work.

## Queued is not spent

A `queued` or `not_started` run has reserved and captured nothing; credits are touched only once a worker starts it. Cancel before pickup (`oxygen table-runs cancel <run_id>`) and the spend stays 0. That is also why approval sits at enqueue time: approving a run approves the spend that begins at pickup.

## Pilot, then decide

- **Pilot one row, always** (`--limit 1` or `--row-id`) before any live batch, and quote its result in the approval for the batch.
- **Stop and report instead of scaling** when the pilot or first small batch resolves well under the coverage you priced, when its values do not obviously belong to the intended person or company, or when credits per usable row land materially above the approved estimate. Scaling past a bad pilot turns one wasted credit into hundreds; the user makes that call.
- **Never retry-patch misses.** Re-running enrichment on the rows that missed re-bills the same misses. Filter them out, or backfill only with a different provider that plausibly covers them.
- **Read the receipt** after the pilot and after each batch: dry runs carry `estimated_credits`, live runs `credits_used`, `credits_remaining` and `billing_url`. Surface the running total on long runs, and when actuals run meaningfully over the estimate, say so before the next batch (`oxygen table-runs provider-summary <run_id>` shows which lanes paid).

## Report honestly

- **Say what OXYGEN cannot do, plainly.** A missing or unhealthy integration is a blocker to surface with its reconnect link, never something to route around. A missing capability is reported (and, with the user's consent, filed through the `oxygen-feedback` skill), never faked with another tool.
- **Report what you observed.** Never imply full coverage after a sample: "I checked the first 20 rows" is honest, "the table is clean" after 20 rows is not. When a command cannot confirm something, say so.
- **Summarize, do not dump.** Turn envelopes into a short takeaway (counts, the number that matters, the link); paste raw JSON or row dumps only when asked.
- **Deep-link every change.** Every state-changing action returns a `web_url`; hand it over with the result.

## Combines with

- `SKILL.md`: the operating loop and its `AWAIT_APPROVAL` stop.
- `oxygen-diagnostics` (`optimize-credits.md`): explaining spend after the fact; each `suggestions` entry there carries its own `label`, `price_label`, `providers` and `provider_count`.
- `oxygen-gtm-consultant` (`references/craft.md`): sizing defaults such as over-provisioning and pay-on-match when designing a motion.
