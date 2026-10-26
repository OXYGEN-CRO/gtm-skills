# Local businesses from Google Maps

## When

The buyer is a business with a physical location or a service area (clinics, restaurants, trades, local agencies, offices by city), so a database of companies by firmographics misses most of them.

## Numbers

- **One query per category per city:** `"<category> in <city>"`.
- **Preview each query once:** the free preview still calls the supplier.
- **At most 5 pages a query** (`--max-pages 5`, 20 listings a page) on the dry run and the live run; without it the dry run prices every page the query reaches.
- **Website share decides the channel.** If fewer than 40% of the preview listings have a website, email cannot carry the list: switch to phone or WhatsApp, or drop the avenue.
- **Maps repeats listings across pages**, so expect 5 to 10% fewer unique rows than pages × 20; when the user names a number, pass `--target-count` about 10% above it.
- **A review-count band the user sets** separates the businesses they sell to from one-person shops and large operators. There is no default; ask.

## Steps

1. Build the grid with the user: the categories (as a searcher would type them) and the cities. Each pair is one query.
2. Preview each query (free): `oxygen companies search preview --source google_maps --filters-json '{"q":"<category> in <city>"}' --json`. Count the rows with a `website` and read `review_count` against the band.
3. Price it (free): `oxygen companies search run --source google_maps --source-filters-json '{"q":"<category> in <city>"}' --max-pages 5 --mode dry_run --json`. Read `output_columns` and `recommended_max_credits`.
4. After approval of that ceiling, run each query live: the first with `--table-name "<category> - <region>"`, the rest with `--table <that table>`, each with `--max-pages 5 --mode live --max-credits <recommended_max_credits> --approved --json`, then `oxygen table-ingestions wait <run_id> --json`.
5. Find chains and multi-site firms (free, read-only): `oxygen tables dedupe <table> --on domain --normalize domain --json` previews the listings that share one website. Leave out a group of several listings unless the user sells to chains; never run it with `--apply`, which would delete branches.
6. Read the qualified list (free): `oxygen tables query <table> --filter-tree-json '{"type":"group","conjunction":"and","children":[{"type":"leaf","columnKey":"website","operator":"is_not_empty"},{"type":"leaf","columnKey":"review_count","operator":"gte","value":<min>},{"type":"leaf","columnKey":"review_count","operator":"lte","value":<max>}]}' --fields name,category,website,review_count,address --json`.
7. Grade the qualified listings once, naming the band and the chains to leave out in the grade's prompt, then find the owner or manager at the ones that pass with the decision-makers column from `oxygen enrichment catalog --json` (the `oxygen-enrichment` skill). Merging with another source follows the [playbook](../references/playbook.md); a listing without a website stays keyed on `cid` and never joins it.

## Kill and scale

- **The first two queries miss the website share:** stop the email list; offer phone or WhatsApp, or another avenue.
- **Most listings fall outside the band or are chains:** the category is wrong. Rename it as a searcher would (one rewrite), then stop.
- **Scale by adding cities and categories, not pages.**
