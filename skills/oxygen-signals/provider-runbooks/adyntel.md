# Ads: Adyntel

Ads in OXYGEN is competitor ad intelligence: the ads a company is running on LinkedIn, Meta (Facebook and Instagram), Google and TikTok, and a domain's paid-versus-organic search keyword picture. Adyntel supplies it on OXYGEN's key by default. Every operation is a paid call except `adyntel.google_shopping_status`, which is free. Prices are in the generated table at the end. Owned-audience activation (pushing your lists to ad platforms) is not part of Ads today; do not promise it.

## Saved searches

A reusable search definition is free to save and runs nothing: `oxygen ads searches save --name "<name>" --platform <platform> --company-domain <domain> --json` (or `--keyword`, `--country-code`, `--tags`), then `oxygen ads searches list --json`. Running the provider operation behind it is the normal paid read below. Tag a saved search to group it with a campaign (`tags attach`).

## Discover

```bash
oxygen tools search --provider adyntel --all --json
oxygen tools get adyntel.linkedin_ads --json   # inputs, typed output, example output, current price
```

## Put it in a Table

One row per company with a **bare domain** column (`clay.com`, not `https://www.clay.com/`: a URL or `www.` is refused before any request, so nothing is charged). Create the table with its tool columns in one call, then price before you run:

```bash
oxygen tables create "Competitor ads" --json --columns-json '[
  {"key":"domain","label":"Domain","dataType":"text"},
  {"key":"linkedin_ads","label":"LinkedIn ads","dataType":"jsonb","kind":"tool",
   "definition":{"toolId":"adyntel.linkedin_ads",
                 "inputMapping":{"company_domain":{"type":"column","columnKey":"domain"}}}}]'
oxygen columns run <table> linkedin_ads --dry-run --limit 1 --json
oxygen columns run <table> linkedin_ads --limit 1 --approved --max-credits <quote> --json
```

The same shape works with `oxygen columns add <table> --kind tool --data-type jsonb --definition-json '{...}'`. The input name differs per operation (`company_domain`, `keyword`, `id`); `oxygen tools get <tool_id>` lists it.

For one row per LinkedIn ad, use native paged ingestion into a Table with text columns `ad_id` and `advertiser`. After approval, the following run follows continuation pages and upserts by ad ID; each page is paid. Set a bounded page limit and approved credit cap:

```bash
oxygen table-ingestions create-tool-page <table> --tool adyntel.linkedin_ads \
  --request-json '{"company_domain":"example.com"}' --rows-path response.ads \
  --row-mapping-json '{"ad_id":"ad_id","advertiser":"advertiser.name"}' --upsert-key ad_id \
  --cursor-path response.continuation_token --cursor-request-key continuation_token \
  --max-pages <page-limit> --max-credits <approved-cap> --json
```

Read the ingestion run and its items before calling the library complete. `has_next_cursor:true` means more pages remain even when the bounded run has finished; `stopped_by:provider_exhausted` records an exhausted provider cursor. Failed items leave the run failed or completed with errors. A local persistence retry reuses the staged page.

Use `oxygen table-ingestions items <run-id> --json` (MCP `oxygen_table_ingestions_items`) to read the last completed item's `nextCursor`. If a successful bounded run stops with a non-null cursor, request approval for another bounded run. Repeat `create-tool-page` into the same Table with the same company, mapping and `--upsert-key`, adding `"continuation_token":"<nextCursor>"` to `--request-json`. Set the new approved page and credit caps. This starts at the saved next page; restarting with the original request would fetch page one again. Do not call the library complete while a cursor remains. Inspect failed items before starting another run; do not automatically retry an unknown provider outcome. For a failed local write, use `table-ingestions retry-failed` on the existing run to reuse its staged page.

For MCP, call `oxygen_table_ingestions_create` after approval with this equivalent bounded payload (replace the Table and caps):

```json
{
  "table": "<table>", "source_type": "tool_page", "mode": "upsert", "upsert_key": "ad_id",
  "max_credits": 5,
  "items": [{"position": 0, "payload": {
    "tool_id": "adyntel.linkedin_ads", "request": {"company_domain": "example.com"},
    "rows_path": "response.ads", "row_mapping": {"ad_id": "ad_id", "advertiser": "advertiser.name"},
    "cursor_path": "response.continuation_token", "cursor_request_key": "continuation_token", "max_pages": 1
  }}]
}
```

Read the run with `oxygen_table_ingestions_get` and items with `oxygen_table_ingestions_items`. To continue after a bound, create a newly approved bounded run into the same Table with the last completed item's `nextCursor` in `items[0].payload.request.continuation_token`; keep the same company and upsert key.

| You want | Operation | Input |
|---|---|---|
| LinkedIn ads for a company | `adyntel.linkedin_ads` | `company_domain` (or `linkedin_page_id`) |
| Facebook and Instagram ads | `adyntel.facebook_ads` | `company_domain` or `facebook_url` |
| Google search, image and video ads | `adyntel.google_ads` | `company_domain` |
| Google Shopping ads (two steps) | `adyntel.google_shopping`, then `adyntel.google_shopping_status` | `company_domain`, then the returned `id` |
| Paid versus organic keywords, traffic, budget | `adyntel.domain_keywords` | `company_domain` |
| Ads in an ad library by keyword | `adyntel.facebook_ad_search`, `adyntel.linkedin_keyword_search`, `adyntel.tiktok_search` | `keyword` |
| One TikTok ad in detail | `adyntel.tiktok_ad_details` | `id` from a TikTok search result |

## Read the result

- The cell is one JSON object: `provider`, `operation`, `request`, `response` (Adyntel's body) and `meta`. The ads are under `response`: `response.ads` for LinkedIn and Google, `response.results` for Meta (each entry is an array of ad variants). The totals are `response.total_ads`, `response.total_ad_count` and `response.number_of_ads`; they count the advertiser's whole library, not the page you got.
- A page can be large (a Meta page was about 82 KB). Pull what you need with a free formula column instead of reading the cell: `--kind formula --definition-json '{"expression":"path(linkedin_ads, \"response.total_ads\")"}'`, or `path(first(path(linkedin_ads, \"response.ads\")), \"headline.description\")` for the first ad's headline. Check an expression on real rows with `oxygen formulas validate <table> --expression '...'`.
- `facebook_ads`, `linkedin_ads`, `google_ads`, `facebook_ad_search` and `linkedin_keyword_search` return synchronous pages. An unexpected job acknowledgment, unusable pagination state or HTTP 204 fails with `provider_outcome_unknown`, is not automatically retried, and returns its managed credits. HTTP 204 cannot prove an empty or exhausted library; Meta can return it when the source cannot be scraped. `meta.outcome:pending` belongs to Google Shopping job acknowledgments (HTTP 200 or 202): resume with `google_shopping_status` and the existing `id`, without another start call. That separate status lookup retains `no_content` (204) with `response:null` for an unknown job reference.

## Guardrails

- One call returns one page. Send the response's `continuation_token` back with the same inputs for the next page; each page is a billed request. A page that repeats the token you sent fails instead of billing the same page again. These five operations refuse `all_ads=true` or a non-empty `webhook_url` before any provider call: Oxygen cannot receive or resume those webhook jobs. Use bounded paged Table ingestion with `continuation_token` instead.
- Google Shopping: the default lookup starts a job. Start it once through `tools run` or a tool column and keep its `id` (HTTP 200 or 202, `meta.outcome:pending`). Paged Table ingestion refuses this asynchronous start before spending because it cannot resume the job. The explicit `shopping:true` variant requests synchronous results and can be ingested with `rows_path=response.ads`, upserting by `creative_id`. Only HTTP 200 with an `ads` array proves a finished collection, including an empty array; an acknowledgment, pending 202 or ambiguous 204 fails without another start. A start that returns HTTP 5xx, or neither an `id` nor an `ads` array, fails with `provider_outcome_unknown` and is never resubmitted; its managed credits are returned. Inspect the run before starting another paid lookup. If that synchronous request unexpectedly returns a job, read `lastError.provider_request_id` from `table-ingestions items` for recovery; its uncertain paid effect remains protected from replay.
- Read an existing Shopping job through `tools run adyntel.google_shopping_status` with its original id and **explicit original credential mode**. For `user_api_key`, also retain the original `--connection-id` when used. Preview that exact status read, then use its quoted cap and approval. A managed status read costs zero Oxygen credits, but the managed account can still refuse it when its vendor wallet is empty. `table-ingestions create-tool-page` has no credential-mode flag and can select an existing BYOK connection; it cannot safely recover a managed-account job in that workspace. Use the explicit status read and JSON import below instead. A pending or unknown response never becomes an empty import.
- Keyword searches (`*_ad_search`, `linkedin_keyword_search`, `tiktok_search`) are not scoped to one company. TikTok's `country_code` takes European codes or `ALL`; `US` is not a supported filter.
- LinkedIn results can include promoted posts by individuals, so `advertiser.name` may be a person.
- `domain_keywords` for a domain with no paid keywords has `paid.count` 0 and no `estimated_avg_cpc`: there is no CPC to read.
- A refusal that names credits or an account is a funding problem on Oxygen's side (managed) or on your own key (BYOK): report it instead of retrying in a loop.

## Recover a managed Shopping job into a Table

Use the id and domain from the original managed start. These commands read that job; they never start another lookup. Keep the preview and approval steps even though the managed status read is free:

```bash
set -e
oxygen tools run adyntel.google_shopping_status --mode dry-run --credential-mode managed \
  --input-json '{"id":"<original-id>"}' --json
oxygen tools run adyntel.google_shopping_status --mode live --approved --max-credits 0 --credential-mode managed \
  --input-json '{"id":"<original-id>"}' --json > shopping-status.json
jq -e --arg domain '<original-domain>' --arg job '<original-id>' '
  select(.ok == true and .data.result.meta.status == 200 and .data.result.meta.outcome == "ok")
  | .data.result.response.ads | select(type == "array")
  | map({creative_id, title, url, company_domain: $domain, job_id: $job})
' shopping-status.json > shopping-rows.json
if jq -e 'length > 0' shopping-rows.json > /dev/null; then
  oxygen tables import <table> --file shopping-rows.json --upsert-key creative_id --json
  oxygen tables query <table> --fields creative_id,title,url,company_domain,job_id --json
else
  printf '%s\n' 'The job is ready with no ads; no import is needed.'
fi
```

Only continue to the import when the status read and extraction succeed. The destination needs those five text columns. Compare distinct creative IDs and persisted row IDs on readback; upserting the same ready rows again must not add duplicates. An explicit empty ads array proves no rows to import. For an original BYOK job, keep `user_api_key` and the same connection on both status commands, and replace the zero cap with its dry-run quote.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `adyntel.domain_keywords` | 5 cr | pre_authorize | paid_provider | — |
| `adyntel.facebook_ad_search` | 5 cr | pre_authorize | paid_provider | — |
| `adyntel.facebook_ads` | 5 cr | pre_authorize | paid_provider | — |
| `adyntel.google_ads` | 5 cr | pre_authorize | paid_provider | — |
| `adyntel.google_shopping` | 5 cr | pre_authorize | paid_provider | — |
| `adyntel.google_shopping_status` | free — not billed | no_bill | none | — |
| `adyntel.linkedin_ads` | 5 cr | pre_authorize | paid_provider | — |
| `adyntel.linkedin_keyword_search` | 5 cr | pre_authorize | paid_provider | — |
| `adyntel.tiktok_ad_details` | 5 cr | pre_authorize | paid_provider | — |
| `adyntel.tiktok_search` | 5 cr | pre_authorize | paid_provider | — |
<!-- END GENERATED -->
