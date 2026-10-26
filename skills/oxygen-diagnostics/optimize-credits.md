# Optimize Credit Spend

**Answers one question: "Why did this cost so much, and how do I spend less?"**

Use this when the user is surprised by a credit balance, wants to understand where credits went, or wants the *same* result for fewer credits. This is the cost lens. For a value that's wrong or missing, use [table-trace.md](table-trace.md); for failures, [error-sweep.md](error-sweep.md).

Two halves: **explain the spend that already happened**, then **spend less next time**.

## Part A — Explain where credits went

### 1. Group the spend

`billing audit` summarizes the ledger — grouped, by default, by provider and source (operation):

```bash
oxygen billing audit --json
oxygen billing audit --group-by provider --json
oxygen billing audit --days 30 --provider <provider> --json
```

This answers "which providers and which operations ate the credits" in one call, and every result also carries `spend_by_category`: each spend area's credits and share of the window's spend, largest first, whatever the grouping. Read that first for "where did my credits go". When `groups_truncated` is true, `--limit` cut operation rows and `managed_credits_spent_outside_groups` says how much they carried. Grouping keys default to `provider,source`; other keys are `day`, `type`, `category`, `tool`, `model`, `run`, and `workspace`. Narrow with `--type` (`grant`, `reserve`, `capture`, `release`, `refund`, `adjustment`, `byok_usage` — alias `byok`) or `--category` (`free`, `trial`, `subscription`, `purchase`, `managed_ai`, `managed_enrichment`, `managed_domain`, `managed_mailbox`, `managed_inbox`, `managed_seat`, `linkedin_action`, `automation`, `byok`, `admin`).

For agency and multi-workspace accounts, run `oxygen billing usage --group-by workspace --json` from the billing-owner workspace: `by_workspace` names each workspace on the shared credit pool and the credits it spent (`credits_spent`), and `--workspace <id|slug>` narrows the ledger events to one client (MCP `oxygen_billing_usage` with `group_by: "workspace"` / `workspace`). The same transparent breakdown — by category, provider, time, and sub-workspace — is also in the web app at **Settings → Billing & credits**, below the plan.

### 2. Read the individual ledger events

When a grouped total looks wrong, drop to the raw ledger:

```bash
oxygen billing usage --limit 50 --json
oxygen billing usage --provider <provider> --nonzero --json
oxygen billing usage --run-id <run_id> --json          # every credit event for one run
```

`billing usage` shows individual `reserve` / `capture` / `release` events. The key insight: a **reserve** is a hold, a **capture** is the actual charge, and a **release** returns an unused hold. If you see large reserves but small captures, you over-provisioned `--max-credits` — the run only spent a fraction of the ceiling. That is not lost money, but it tells you the cap can be lower next time.

### 3. Attribute spend to one run

To see the per-provider credit story for a specific run — reserved vs captured vs released, per provider attempt:

```bash
oxygen table-runs provider-summary <run_id> --json
```

This is the sharpest "why did *this run* cost that much" view: it ties each provider attempt to its credit capture/release, so a run that retried an expensive provider many times is immediately visible.

**Epistemic honesty:** the ledger records credits, not upstream dollar invoices. For BYOK providers billed on your own key, `billing usage` shows `byok_usage` events for accounting but the actual charge lives on the provider's bill, not Oxygen's balance.

## Part B — Spend less next time

### 4. Preview before you pay (free dry-run)

Never queue a paid enrichment blind. The preview estimates rows, resolved provider order, and credits **without any provider call or credit spend**:

```bash
oxygen enrich-column preview <table> --json
```

Read the estimate, then run the real thing with an explicit ceiling:

```bash
oxygen enrich-column run <table> --max-credits <n> --json
```

The preview is the single best cost-control habit: it turns "I hope this is cheap" into a number you can show the user before approval.

### 5. Choose the cheapest tool that clears the bar

Before wiring a provider into a column, read its cost model — this is grounded, not guessed:

```bash
oxygen tools get <tool> --json
```

The descriptor's `cost` object exposes:

| Field | Use it to |
| --- | --- |
| `cost.pricing_model` | `no_bill` = free (route to these first); `fixed` / `per_result` / `provider_usage` = billed. |
| `cost.managed_credit_estimate` | `{ min, max }` credits per call from the billing resolver — the number to compare across candidate providers. `min` is an empty request; `min` = `max` means the price does not depend on the request. `scales_with` names the fields (records, limit, pages) a bigger request pays more for, and `max: null` means no upper bound — dry-run the real request before comparing. |
| `cost.billing_mode` | `pre_authorize` (reserved up front) vs `post_deduct` vs `no_bill`. |
| `cost.provider_price_per_unit` | The raw provider price when present, for BYOK math. |

**Cheapest-first waterfall discipline:** order providers so the free/cheap, high-fit tool runs first and the expensive one is only reached for rows the cheap tool missed. The `enrich-column` waterfalls already default to a cost-aware order; when you set `--provider-order` by hand, put the lowest `managed_credit_estimate.max` that can satisfy the row's inputs first. `--allow-premium-lanes` gates managed lanes over 50 credits/call, and only `linkedin_url` has one; work email and phone bill on a hit, so their expensive tail always runs and the flag is a no-op there.

### 6. Put a standing cap under the whole thing

`--max-credits` caps one run. A **budget** is a standing hard-block that survives every run, so a forgotten loop or a webhook auto-run can't quietly drain the balance:

```bash
oxygen budget list --json
oxygen budget set --scope org --window daily --max-credits <n> --json
oxygen budget set --scope table --scope-id <table> --window monthly --max-credits <n> --json
```

Scopes: `org`, `table`, `workflow_trigger`, `monitor`. Windows: `per_run`, `daily`, `monthly`. Action defaults to `hard_block` (use `--action warn` for a soft alert). A per-table monthly cap is the usual safety net for an always-on enrichment table.

## Deep-link guidance

- **Billing** → `https://oxygen-agent.com/billing` (balance, ledger, plan).
- **A run's cost** → the run `web_url` from `table-runs get` (`https://oxygen-agent.com/tables/<table>/runs/<run_id>`).

## MCP equivalents

| CLI | MCP tool |
| --- | --- |
| `oxygen billing usage` | `oxygen_billing_usage` |
| `oxygen billing audit` | `oxygen_billing_audit` |
| `oxygen table-runs provider-summary` | `oxygen_table_runs_provider_summary` |
| `oxygen enrich-column preview` | `oxygen_enrich_column_preview` |
| `oxygen tools get` | `oxygen_tools_get` |
| `oxygen budget list` / `oxygen budget set` | `oxygen_budget_list` / `oxygen_budget_set` |

## Combines with

- **[table-trace.md](table-trace.md)** — when a specific pricey value needs its provider attempt traced.
- **[error-sweep.md](error-sweep.md)** — repeated retries of an expensive provider are a cost problem *and* a failure problem; sweep the failures so you stop paying to re-fail.
- **`oxygen-gtm`** — [cost-precheck](../oxygen-gtm/guides/cost-precheck.md): balance against estimate before a run, and the stop-after-pilot rules.
- **[runs-and-limits.md](runs-and-limits.md)** — plan, credit and rate-limit refusals, `limits show` and a monthly cost estimate before building.
