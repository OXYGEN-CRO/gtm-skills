# Serper

Use Serper for Google-style web discovery and local or maps discovery when the agent needs URLs or local business rows before scraping or enrichment.

## Discover

```bash
oxygen tools search serper --json
oxygen tools get serper.search --json
oxygen tools get serper.maps --json
oxygen tools get serper.places --json
```

## Use

- `serper.search`: recover unknown URLs, source lists, news-like public evidence and public pages. It is also the default first lane of research-column web grounding: a research column discovers with Serper, then reads the top result for page text.
- `serper.maps`: build local or SMB account lists from a category plus a place. It is the engine behind the Google Maps businesses table source (free sample: `oxygen companies search preview --source google_maps --filters-json '{"q":"dentists in Berlin"}'`; paid import: `companies search run --source google_maps --source-filters-json` with the same filters, dry run then approved live). Rows carry title, address, phoneNumber, website, rating, ratingCount, type, latitude and longitude, cid and placeId. It is also the tool for one known business's listing per row: a tool column whose `q` is the business name plus its city returns that listing first.
- `serper.places`: lighter local results with title, address, website, cid and coordinates, but no Google place id, and phone, rating and category often missing. Use `serper.maps` when you need a listing's phone, rating or place id.

## Read a Serper table column

A Serper tool column stores the whole run envelope (`meta`, `request`, `provider`, `response`), and Serper's answer sits under `response.raw`: `response.raw.organic.0.link` for Search, `response.raw.places.0.phoneNumber` for Maps or Places. Copy fields into ordinary columns with `oxygen columns materialize <table> <column> --mappings-json '[{"source_path":"response.raw.places.0.phoneNumber","target_column":"phone"}]'`, free and with no provider call.

## Guardrails

- If the URL is already known, use a scrape or content route instead of a search.
- Serper has no domain parameter: scoping rides as `site:` / `-site:` operators inside `q`, which the ranker may ignore. A grounded column records that as `domainFilter: "advisory"`; Exa's `includeDomains` is a provider-side filter and records `"applied"`. Prefer Exa when an allowlist must hold.
- Serper bills every successful response, including an empty result set, so an empty page is a paid attempt the ceiling must absorb; an error response costs nothing. On your own Serper key, the `credits` field in each response is what that call cost your Serper account, a figure separate from OXYGEN credits, and an account out of Serper credits answers HTTP 400 "Not enough credits".
- `serper.maps` and `serper.places` page by an integer `page`; Maps refuses page 2 and later without an `ll` map anchor (`@<lat>,<lng>,<zoom>z`), Places does not need one. Table ingestion pages for you: a full page yields a `response.cursor` of `<page>|<ll>`, and a short page ends the run. Calling the tool directly, pass that cursor back as `request.cursor`, or `page` plus `ll` for Maps.
- A null `response.cursor` with `response.pagination: {state: "blocked", reason: "missing_map_anchor"}` means the page was full but Serper returned no usable map anchor: more places exist. The import stops with `stopped_by: "missing_map_anchor"` and keeps the paid rows; for a Google Maps import, set the map center (`"ll":"@30.2672,-97.7431,12z"` in the filters) and search again (a new paid run from page 1; rows upsert on `cid`).
- OXYGEN refuses before any provider call, at no charge, with `invalid_provider_request` naming `field`: a malformed cursor (`cursor`), a page that is not a positive whole number (`page`), or a Maps page after the first without a valid `ll` (`ll`).
- Maps accepts `q`, `hl`, `ll`, `placeId`, `cid` and `page`. Country (`gl`), `location` and `num` are not Maps parameters: name the area in `q` or set the center in `ll`.
- The Maps preview costs no workspace credits; the import is paid. Use the native `companies search run --source google_maps` dry-run quote, then `--mode live --approved --max-credits <quote>`. An import can request up to 50,000 rows and stops when the source runs out; the target and the sample length are never an available-match count.
- Keep the result URL, title or name, address, phone, website, rating, query and source payload where returned.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `serper.maps` | 0.5 cr | pre_authorize | paid_provider | — |
| `serper.places` | 0.5 cr | pre_authorize | paid_provider | — |
| `serper.search` | 0.5 cr | pre_authorize | paid_provider | — |
<!-- END GENERATED -->
