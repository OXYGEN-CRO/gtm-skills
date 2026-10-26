# Signal searches and live signal tables

Hiring, technology adoption, funding, acquisitions and news about companies are signal search families. LinkedIn posts by keyword are the same command with `--family linkedin_posts` ([public research](public-research.md)). The shape is always three moves:

1. **Plan it for free.** The plan names the provider chain, the filters each route applies or drops, the price of each route and the table blueprint.
2. **Fill it once, priced and approved.** The run creates the table and harvests the first pages under an explicit ceiling.
3. **Bind it as a feed, only if it can be armed** and the user wants recurring spend. The cadence replays the frozen request and advances a cursor or date window.

## Plan, dry run, run

`--scope market` watches any company matching the filters (keywords, countries, recency); `--scope watch_list` watches only the accounts in `--domains`.

```bash
oxygen signals search plan --prompt "Series A fintechs hiring backend engineers" --family hiring --scope market --keywords "backend engineer,golang" --countries US --last-days 30 --estimate --json
oxygen signals search run --plan-json ./plan.json --mode dry_run --json
oxygen signals search run --plan-json ./plan.json --mode live --approved --max-credits <n> --max-pages 3 --json
```

Read the plan back before spending: `routes[]` (who is called, in what order, at what price per page), `filter_application` per route (`applied` against `dropped`, with the reason; never describe a dropped filter as applied), `estimated_match_count` and its `basis`, and the `table_blueprint`. **Quote a match count only when `basis` is `provider_count`, naming the probe**; otherwise say the provider publishes no free count. The run returns an ingestion, not rows: `oxygen table-ingestions wait <run_id> --json`, then `oxygen tables preview <table> --limit 10 --json`.

## Arm it

Binding is one flag on the run, so the plan you inspected is the plan that gets armed:

```bash
oxygen signals search run --plan-json ./plan.json --mode live --approved --max-credits <n> --max-pages 3 --bind-feed --every every_6h --max-credits-per-cycle <n> --max-rows-per-cycle 500 --json
oxygen feeds list --table <table> --json
oxygen feeds run <feed> --mode dry_run --json
```

- The plan carries `schedulable`, per plan and per route. Read it before promising a live table; where it is false, deliver the one-shot list and say why it cannot resume. A source with no resumption point is refused with `feed_not_incremental`.
- Market-wide funding and acquisition searches are one-shot (their discovery accepts no date filter); hiring, tech adoption, LinkedIn posts, per-account news and watch lists can be armed.
- **`--bind-feed` is a second, separate consent**: the first run is one purchase, the cadence a standing one. Raising `--max-credits-per-cycle` or changing `--every` later asks again. Feed mechanics (pause, resume, deliveries, unbind): the `oxygen-tables` skill, `references/feeds.md`.

## The AI filter on items

When a plan returns an `ai_filter` block (`available`, `billing: "charged"`, `credits_per_item`), `--ai-filter "<what to keep>"` works on that family (hiring, news and funding included): it reads each job posting, news item or funding event, keeps the matches and charges `credits_per_item` for every item it reads. The dry run quotes the total under `ai_filter`; the live run needs a `--max-credits` that covers it, and a bound feed a `--max-credits-per-cycle` of at least the quote's `min_max_credits_per_cycle`. Kept rows gain **Match score** (0-1) and **Match strength** (passing mention, one topic among several, main topic). On `hiring` the filter is strict: a posting must meet the whole description, exclusions included, and an agency hiring for a client is dropped unless the description asks for agencies. An item it cannot judge stays in with a blank **Matches filter** and costs nothing. Totals report `kept_matched`, `kept_unjudged`, `dropped` and `credits_charged` in `oxygen table-ingestions get <run_id> --json` under `ai_filter`. Without that block, `--ai-filter` applies to posts only and the plan lists it under `dropped` on other families.

## Rules

- Plan before you run: the plan is free and is the only place the chain and the dropped filters are visible.
- Every live run needs `--approved` and an explicit `--max-credits`; quote the ceiling in the same sentence as the action and send exactly that number.
- A signal table is a **table**, not the Signals stream: nothing subscribes to these rows by type. Enrich, score and enroll from the table, and do not tell the user a workflow will trigger off them.
- Refusals are answers: `no_default_provider_chain` means no routed provider exists for that family and scope (market-wide job changes, for instance). Report it rather than substitute a provider.
- The browser equivalent is the new-table wizard at `/tables/new`; the plan, the priced button and the cadence step call the same routes.
