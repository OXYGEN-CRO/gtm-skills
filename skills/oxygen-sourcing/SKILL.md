---
name: oxygen-sourcing
description: "Find companies and people that are not in the workspace yet and land them in OXYGEN Tables: account and TAM lists, lookalikes, hiring companies, local businesses, personas and contacts at named accounts, through free previews, typed plans, priced dry runs and approved live runs."
allowed-tools: Bash(oxygen *)
---

# OXYGEN Sourcing

Sourcing finds companies and people the workspace does not have yet and lands them in a Table, with every page, route and cost inspectable. Enriching rows you already have is the `oxygen-enrichment` skill. Hiring, funding, tech and news signals, public LinkedIn posts and their engagers, and daily profile watchers are the `oxygen-signals` skill (public LinkedIn research: `references/public-research.md` there).

## Start from the planner

| Ask | Free first | Read |
| --- | --- | --- |
| Accounts by firmographics, technology, lookalikes, a TAM | `companies search preview`, then `companies search plan` | [companies](references/companies.md) |
| Who is hiring for a role | `companies search preview --source hiring` | [companies](references/companies.md) |
| Local businesses | `companies search preview --source google_maps` | [companies](references/companies.md) |
| Company names to websites | `companies search plan --source-intent url_recovery` | [companies](references/companies.md) |
| People by persona, or at up to 50 named companies | `people search preview`, then `people search plan` | [people](references/people.md) |
| People at every company in a table | `people search plan --from-table <table>` | [people](references/people.md) |
| "Build leads for this ICP", or the right start is unclear | `lead-sourcing plan`, `sourcing plan` | [lead sourcing](references/lead-sourcing.md) |
| Every way a table can start | `tables sources` | — |

Before choosing an avenue, merging sources, setting contacts per account or deciding when to stop, open the [playbook](references/playbook.md); its plays cover [lookalike TAMs](plays/lookalike-tam.md) and [local businesses](plays/local-business-maps.md).

Discover the exact grammar with `oxygen commands get "companies search plan" --json` before writing filters, and resolve context first: `oxygen knowledge resolve --purpose lead_sourcing --json`.

## Loop

1. Preview or plan, free. A preview shows up to 50 real rows, the total that match and a priced `next_step` that saves all of them; a plan names the routes, what each applies and drops, the gates, availability, the match estimate and `recommended_live_route_id`.
2. Dry-run the chosen route: the request it will send, its size, its pages and its price. The dry-run request is the provider contract; never rewrite a payload from memory or pick providers from memory.
3. Show the rows, the route, the dropped filters, the size and the ceiling; get approval.
4. Run live with `--approved` and `--max-credits` at that size. The free preview is the quality check; a route with no free preview runs `--max-pages 1` first, and once those rows look right, the rest.
5. Wait on the ingestion (`oxygen table-ingestions wait <run_id> --json`) and read the table.
6. Companies first, then people at the accepted accounts; enrich only the rows that survive.

## Gates

- **Source every match by default.** Leave `--target-count` unset, or copy the preview's `next_step`, unless the user named a number; then pass theirs. An unnamed size takes every match, up to what one query reaches and a tenth of the workspace's spendable credits, so a free workspace keeps most of its grant; `target_count_default` says which bound applied. The dry run reads the source's own free count, so its quote is the real audience; `no_matches` means nothing matched and nothing was created or charged. Never shrink a run to a sample or one page on your own; a play's own size wins (the lookalike learning sample, 5 pages per keyword phrase).
- **Approval and a ceiling for every live run.** Quote the ceiling in the same sentence as the action and send exactly that number.
- **Never invent a match count.** Quote a number only when its `basis` is `provider_count`, naming the probe; otherwise say the provider publishes no free count. A target or a sample length is never a market size.
- **A dropped filter is never applied.** Report each one; a live cascade never advances to a provider that drops the account scope.
- **Refusals are answers.** A `no_default_provider_chain`, a benched provider or a preview-only route is reported as it is, without a silent substitute or a fallback to a pricier provider.
- **A sourcing approval covers the pull only.** Enrichment, reveals, CRM writes, outreach and LinkedIn actions on the landed rows are each their own approved action.
- **Recurring spend is a second approval.** Binding a source as a feed (`--bind-feed`, `feeds bind --every`) is a standing purchase separate from the first run; changing its cadence or ceiling asks again.
- **Native, not scripted.** Loops over pages, joins, dedupes and waiting are product features; a script around them is a missing native capability to report.

Return the table and run links, and say how much of the target landed.

## Provider runbooks

Load one after `oxygen tools get <tool_id> --json`: [Blitz](provider-runbooks/blitzapi.md) (people and company search, enums, the result ceiling), [Dropleads](provider-runbooks/dropleads.md), [Exa](provider-runbooks/exa.md), [Serper](provider-runbooks/serper.md) (search and Maps), [Firecrawl](provider-runbooks/firecrawl.md), [Linkup](provider-runbooks/linkup.md), [Parallel](provider-runbooks/parallel.md), [Apify](provider-runbooks/apify.md), [OpenWebNinja](provider-runbooks/openwebninja.md).

Plays: [icp-to-account-map](plays/icp-to-account-map.md), [lookalike-tam](plays/lookalike-tam.md), [local-business-maps](plays/local-business-maps.md).
