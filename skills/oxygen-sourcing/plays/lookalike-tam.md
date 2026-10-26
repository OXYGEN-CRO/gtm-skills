# Lookalike TAM

## When

The user has three or more paying, retained customers and wants more companies like them.

## Numbers

- **3 to 5 seeds.** Each seed returns at most 25 companies, so a run lands at most 125: a sample to learn the market's words from, not the TAM.
- **Seeds are paying, retained customers from different sub-segments.** Never a competitor (its lookalikes are competitors) and never the user's own domain.
- **The plan shown before approval covers every step through grading:** a sample per seed, then each phrase at 5 pages, merged by domain and graded once; not only the first live run.
- **Each mined phrase must clear the buyer bar** in the [playbook](../references/playbook.md)'s kill lines before it scales.

## Steps

1. Choose the seeds with the user. Their customers are on the CRM's companies table: `oxygen tables query companies --filter-tree-json '{"type":"group","conjunction":"and","children":[{"type":"leaf","columnKey":"lifecycle_stage","operator":"is","value":"customer"}]}' --fields name,domain --json` (stage names vary: `oxygen crm describe companies --field lifecycle_stage --json`). Confirm 3 to 5, one per sub-segment.
2. Plan (free): `oxygen companies search plan --prompt "Companies like our customers" --source-intent lookalike --filters-json '{"lookalike_domains":["a.com","b.com","c.com"]}' --json > plan.json`. Note `recommended_live_route_id`.
3. Price it (free): `oxygen companies search run --plan-json ./plan.json --route-id <recommended_live_route_id> --mode dry_run --json`. Read `fan_out.calls` (one per seed) and `recommended_max_credits`.
4. After approval of that ceiling:
   ```bash
   oxygen companies search run --plan-json ./plan.json --route-id <recommended_live_route_id> --upsert-key domain --table-name "Lookalikes - <segment>" --mode live --max-credits <recommended_max_credits> --approved --json
   oxygen table-ingestions wait <run_id> --json
   ```
5. Mine the words (free): `oxygen tables query <table> --fields company_name,industry,employee_count,location,evidence --limit 125 --json`. From `evidence`, take the 3 to 5 phrases the lookalike companies use for their own business (never words for what the user sells), and the size band and countries they share.
6. Test each phrase on the structured search (free): `oxygen companies search preview --filters-json '{"keywords":{"include":["<phrase>"],"exclude":["<competitor words>"]},"employee_count":{"min":<min>,"max":<max>},"hq":{"country_code":["<CC>"]}}' --json`. Count the buyers in the 50 rows and read `total_results`.
7. Scale each phrase that clears the bar with the preview's `next_step` command (`oxygen companies search run --source company_search --source-filters-json '<the same filters>'`) plus `--max-pages 5`: first as the free dry run, then, once approved, with `--mode live --max-credits <recommended_max_credits> --approved`. Merge the runs and the lookalike table by domain ([playbook](../references/playbook.md), merge and dedupe).
8. Grade the merged table once, then source people at the accounts that pass.

## Kill and scale

- **Fewer than half of the lookalike rows are buyers:** a seed is wrong (a competitor, an outlier customer, a holding company). Replace it once and rerun; if the second run also misses, use the structured TAM avenue with the user's own words.
- **No mined phrase clears the bar:** follow the playbook's kill lines.
- **Scale by adding phrases, not pages.** To keep the TAM refilling, bind the structured route as a feed ([companies](../references/companies.md), Live TAM); the cadence is its own approval.
