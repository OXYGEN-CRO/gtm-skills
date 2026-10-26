# Public LinkedIn research and monitoring

Anyone else's profiles, posts, companies and engagers are read cookieless through the managed scraper: no connected account is used, and each read costs credits. Relay the scraper disclosure sentence before the first paid read; it and the whose-data-it-is choice between scraper, connected account and send surfaces live in the `oxygen-sequencer` skill (`references/linkedin.md`). Prices are runtime data: read them from the live preview or descriptor (`oxygen tools get <tool_id> --json`), never from memory.

## Who owns what

| Request | Owner |
| --- | --- |
| A public person or company, their recent posts, one known post, post search | managed `scraper.*` operations (descriptor details: the `oxygen-enrichment` skill, `provider-runbooks/scraper.md`) |
| A public post's reactors or commenters | `engagement harvest --source cookieless`, or `scraper.linkedin_post_reactions` / `scraper.linkedin_post_comments` |
| Your own connections, followers, viewers, inbox, Sales Navigator or Recruiter data | the connected account ([LinkedIn captures](linkedin.md)) |
| Indexed market data or watchers the scraper cannot give | Crustdata on the workspace's own key, for that distinct need only |

**No automatic fallback.** Bright Data post collection (priced per record; `limit` bounds a discovery call) and Crustdata are explicit alternatives only. When the native scraper is unavailable, surface the availability error and its remediation instead of spending through another provider or a connected account's quota.

## Daily watcher of public profiles

Professional Network Post Engagers watches one to ten public profiles and keeps everyone who reacts to or comments on their posts in one editable table, with paired profile and post history and current employers. Web: New table, LinkedIn, Professional Network Post Engagers.

1. Ask the user for the real public profile URLs. With none supplied, the watcher waits for that input; a placeholder watcher is never created.
2. Preview, free and without provider calls or writes: `oxygen tables watcher preview --name "Professional Network Post Engagers" --profiles-json '["<real-profile-url>"]' --json`. Omit `--max-credits` for a recommendation.
3. Show `preview.profiles`, `schedule` (daily at 07:00 UTC), `lookback_days`, `coverage_note`, `estimated_credits_per_cycle`, `max_credits_per_cycle` and every `issues` item. The cap applies to each daily cycle, not to a month. Explain the recurring spend and ask for explicit approval; a different cap means a new preview and `preview_hash`. At a zero-credit ceiling, stop at this review.
4. After approval: `oxygen tables watcher create --name "Professional Network Post Engagers" --profiles-json '["<real-profile-url>"]' --max-credits <approved-cap> --preview-hash <preview-hash> --request-id <stable-uuid> --approved --json`. Create starts collecting now and arms the daily cycle; it is not a draft.
5. On an uncertain response, retry with the same `--request-id` and configuration; a second installation is never the recovery. Read it back with `oxygen tables watcher get <table> --json` and open `watcher.web_url`.

- Edit the profiles or cap: `tables watcher preview --table <table>` with the change, then `tables watcher update --table <table> ... --preview-hash <hash> --approved`.
- `tables watcher pause --table <table>` stops it at once and keeps the rows. `tables watcher resume` takes a fresh preview and approval, and resumes the stored settings; changes go through `update`.
- `--credential-mode user_api_key` runs every call on the workspace's own Up2Data key: the supplier bills it and the preview quotes 0 credits; a missing key is an `integration_not_connected` issue before anything is created.
- Coverage is bounded by pagination, provider availability and the cap; `coverage_gaps` stays visible, so report partial coverage as partial.
- MCP: `oxygen_tables_watcher` with `action: preview|create|get|update|pause|resume`.

The watcher collects; it never enrolls or messages anyone. Scoring and outreach are separate, approved steps.

The portable alternative is the `linkedin-profile-engager-monitor` Blueprint: `oxygen blueprints describe linkedin-profile-engager-monitor --json`, then `blueprints preflight` (free, current prices) and `blueprints apply`, which installs three tables and a disabled workflow. Enabling that workflow is its standing-spend approval. If preflight reports a collision, inspect `oxygen workflows get template-linkedin-profile-engager-monitor --json` and reuse the installed monitor.

## One post's engagers, once

`oxygen engagement harvest --post <public-post-url> --source cookieless --max-credits <n> --json` collects a third party's post engagers into a table under that ceiling; `engagement status` shows progress. Your own posts read free through the account ([LinkedIn captures](linkedin.md)).

- Reactions and comments are separate collections: include both only when asked, and both scopes in the estimate. Deduplicate people on their profile URL in the table.
- For direct `scraper.*` calls, `max_results` caps the **entire** scrape (default 25), not each page; `per_page` only sizes a page, and paging a scrape started with the default never makes it unlimited. Later pages need the returned `pagination_token`.
- `response.raw.pagination.truncated: true` means incomplete even without a next-page token. A successful harvest is not proof of the whole audience: more needs a newly scoped preview and approval.

## Posts about a topic

```bash
oxygen signals search preview --keywords "cold email,cold outreach" --exclude-keywords hiring --last-days 7 --ai-filter "founders describing a deliverability problem" --json
oxygen signals search run --family linkedin_posts --prompt "cold email deliverability" --keywords "cold email,cold outreach" --exclude-keywords hiring --last-days 7 --ai-filter "founders describing a deliverability problem" --mode dry_run --json
```

- Keyword rules match the post text, ignoring case: `--keywords` (at least one; each is its own LinkedIn search, at most 5), `--all-keywords` (every one), `--exclude-keywords` (drop on any). `--last-days` takes 1 (last 24 hours) up to 30, above 30 is any time; `--posted-by <profile or company URL>` restricts the author; `--sort recent|relevance|top`; `--min-reactions <n>`. A keyword matches its exact words, so use two or three short terms and let `--ai-filter` judge the meaning, describing the topic ("posts about the Clay GTM tool"), never the keyword itself.
- Mentions of a member or company, the author's industry or title and the content type are not filters the managed search supports.
- **Search is free; it is not unlimited.** Managed post searches share OXYGEN's capacity, and every keyword is one search in every preview and run. Spent capacity answers `rate_limit_exceeded` with a retry time; a preview that ran only some searches says so under `incomplete`. With the workspace's own Up2Data key saved (`oxygen integrations connect up2data --api-key <key>`), `--credential-mode user_api_key` uses that account's quota instead, and a bound feed keeps using it.
- With an AI filter, the preview reads up to 200 posts and shows the first 25 that pass; the table's **Why it matches** column then fills for every kept post at the per-post price the dry run quotes under `ai_filter_reasons`, as the table fills and on every refresh, so the live run needs that `--max-credits` (an OpenRouter key on the workspace pays instead). A reason starts `Main topic:`, `Brief mention:` (kept on purpose; tighten the filter for fewer) or `Not a match:` (a filter mistake, safe to delete). **Matches filter** is `true` for a match and blank for a post the classifier could not judge (kept, never silently dropped).
- `--mode live --approved` creates the table: one row per post with author photo, author, headline, text, reactions, comments, reposts, date, URL, the keywords matched and the filter columns. `--bind-feed --every every_6h` (or `daily@9`, `weekly@mon9`) keeps collecting; each refresh reads the last day and never adds a post twice. Its `--help` lists every flag.
- Next step from a post to its people: pass its URL to `oxygen engagement harvest`. Hiring, funding, tech and news families: [signal searches](signal-feeds.md).

## A company page's followers

`oxygen tables followers check --company <page-url> --records <n> --json` quotes the order for free; fee-positive own-key previews leave the follower count unknown (at least 100 records; `orderable: false` means no order yet). `tables followers order --company <page-url> --records <n> --max-credits <quote-or-more> --request-id <stable-uuid> --approved` places the order; retry the identical payload and request ID after an uncertain response. Rows land when the supplier delivers: inspect the delivered rows before reporting success, and promise no delivery time. With the workspace's own ScrapeLi key saved (`oxygen integrations connect scrapeli --api-key <key>`), `--credential-mode user_api_key` runs the order on it where supported. ScrapeLi bills separately; choose a TOTAL Oxygen placement/recovery platform-fee ceiling, not just the placement quote. Placement-only cannot recover rows; budget exhaustion lands no partial rows, and paid pages may be refetched within that ceiling. Inspect a fee-budgeted own-key order without a provider call with `oxygen tables followers status --request-id <original_uuid> --json`; optional `--table-id <saved_table_id>` verifies its binding. A Table or run alone does not prove provider acceptance. See the oxygen-tables skill, references/import-and-folders.md, for allocation and recorded-fee meanings.

## Research columns on a lead table

```bash
oxygen tools get scraper.linkedin_profile --json
oxygen columns add <table> --label "LI Profile" --kind tool --data-type jsonb --definition-json '{"toolId":"scraper.linkedin_profile","inputMapping":{"url":{"type":"column","columnKey":"linkedin_url"}}}' --json
oxygen columns run <table> li_profile --limit 1 --dry-run --json
oxygen columns run <table> li_profile --limit 1 --approved --max-credits <recommended_max_credits> --json
oxygen cells inspect <table> <row_id> li_profile --json
```

- Inspect each descriptor first: `scraper.linkedin_profile_posts` maps `profile`, `scraper.linkedin_company` maps `company` or `domain`, and `scraper.linkedin_company_posts` maps `company` plus `posted_limit`.
- Pilot one row, inspect the cell and the returned estimate, then present per-row cost times eligible rows. Run the batch as `columns run <table> <column> --all --background --approved --max-credits <n>`.
- Posts columns add a paid call per row: run them only on qualified rows, with a run condition on the column (`columns add|update --run-condition`) or a `--filter-json` run.
- The scraper reads public data only: private profiles and the user's own viewers and relations are connected-account captures ([LinkedIn captures](linkedin.md)).
- A thin posts result means the person rarely posts; rerunning will not add more.
