# Turn your ICP into a scored account map

## The Play

You get a table of about 25 real companies that fit your ICP (ideal customer profile), each graded low, medium or high with a one-line reason, so you can see which kinds of companies fit before you contact anyone. OXYGEN finds them from a short description of who buys from you, or grades a list you already have: a spreadsheet, a CRM export, a VC portfolio, a partner directory or an event's exhibitor page. The first page costs about 3 credits, and the graded table is where your outreach (outbound-pilot-50) starts. With three or more paying, retained customers to use as seeds, use lookalike-tam instead.

## Before You Start

- **Who you sell to is saved.** Check with `oxygen context profile get --json` (free, no monthly cost): `company` and `icp` are filled. If `icp` is empty, ask the founder one question, "Which companies buy from you: what they do, how many people, which countries, and who do you never sell to?", and save the answer (free): `oxygen knowledge profile update --data-json '{"icp":{"segment":"<who buys>","geography":["<countries>"],"exclusions":["<who they never sell to>"]}}' --json`.
- **About 5 credits.** Check with `oxygen billing balance --json` (free) and read `spendable_credits`; it comes after the `available_plans` price list. A graded page costs about 3 credits; nothing here connects an account or adds a monthly charge. If short, tell the founder: "This needs about 5 credits and you have N; you can add credits at https://oxygen-agent.com/billing."
- **Optional: their own list.** A CSV or Excel file, a Google Sheet shared by link, or a public page URL. Nothing to check. Without one, search (step 3A).

## Steps

1. Find the exact industry name for the buyers (free): `oxygen tools enums get blitzapi industry --query software --json`, with the founder's own word in place of `software`. Use a returned value verbatim, for example `Software Development`.
   Tell the founder: "I'm turning your description into search filters; nothing is spent yet."
2. Plan the search (free). The prompt says only who buys; every filter, exclusions included, goes in `--filters-json`, because the planner turns an "exclude …" sentence into include keywords. Keep `--source-intent structured`: without it the planner picks the kind of search from words in the prompt (early-stage, niche, hiring, using, size) and can switch to a smaller search that ignores your exclusions and size range.
   ```bash
   oxygen companies search plan --prompt "<who buys, in plain words>" --target-count 25 --source-intent structured --filters-json '{"industries":{"include":["Software Development"]},"keywords":{"include":["B2B SaaS"],"exclude":["staffing","recruiting","consumer"]},"employee_count":{"min":11,"max":50},"geo":{"countries":["US","GB","DE"]}}' --json > plan.json
   ```
   Keywords are the words buyers use for their own business, never words for what the founder sells (those pull in competitors). Countries are two-letter codes (the UK is `GB`). Replace every value in the example with the founder's own: the industry from step 1, the words their buyers use, the kinds of business they never sell to (`keywords.exclude` drops every company whose description contains the word, so leave out a group defined by size, such as large enterprises: the size range already excludes it), their size range as they gave it (5-50 people is `{"min":5,"max":50}`) and their countries. Only a value the ICP lacks defaults to 11-50 employees and the founder's own country; say so. Read back, from the whole saved file (one line of JSON, about 5 KB): `intent` is `structured_accounts`, `filters` holds each exclusion under `keywords.exclude`, the recommended route's `filter_application.dropped` is empty, and note `recommended_live_route_id` and that route's `estimated_credits`. Quote `estimated_match_count` only when its `basis` is `provider_count`.
   Tell the founder: "I'll search for <the filters in plain words>; one page of 25 costs about 1 credit."
   See the companies before paying (free): `oxygen companies search preview --filters-json '<the recommended route's request.company from plan.json>' --json > preview.json` runs the same search as step 3A at 0 credits and returns up to 50 companies (about 100 KB: every row carries `raw_source`). Read `total_results` (how many companies match) and, for all 50 rows, `company_name`, `domain`, `employee_count`, `location` and what the company does (`raw_source.about`). Count the buyers: a company that sells what the founder sells is a competitor, and a page whose `about` says it was acquired or "is now" another company, or whose `domain` belongs to another company, is not a buyer. If fewer than half are buyers, change the keywords and plan again (free) before asking for approval.
   Tell the founder: "About <total_results> companies match; <k> of the first 50 look like your buyers, for example <names>. Saving 25 of them as a graded table costs about 3 credits."
> APPROVAL GATE — sourcing-live: show where the companies come from (the filters in plain words, or the page URL), one page of 25 companies, and the cap: 2 credits for a search, 1 credit for reading a page. Importing the founder's own file (B) spends nothing and needs no approval.
3. Get the companies, one way:
   - A. Search (default, about 1 credit). Leave out `--table`: OXYGEN creates a table that fits the results.
     ```bash
     oxygen companies search run --plan-json ./plan.json --route-id <recommended_live_route_id> --upsert-key domain --table-name "Target accounts - <segment>" --mode live --max-pages 1 --max-credits 2 --approved --json
     oxygen table-ingestions wait <ingestion_run.id> --json
     ```
     The table's columns: `company_name`, `domain`, `website`, `linkedin_url`, `location`, `employee_count`, `industry`, `evidence` (what the company does).
   - B. A file or a shared Google Sheet (free): `oxygen tables import --create "Target accounts - <source>" --file ./<file> --json`, or the sheet's link as `--url` in place of `--file`. The response lists the column keys.
   - C. A public page: VC portfolio, partner directory, event exhibitors (about 0.5 credit). OXYGEN cannot yet turn a page into one row per company on its own, so read the page, then write the rows it shows:
     ```bash
     oxygen tools run exa.contents --mode live --approved --max-credits 1 --input-json '{"urls":["<page url>"],"text":{"maxCharacters":40000}}' --json
     oxygen tables create "Target accounts - <source>" --columns-json '[{"key":"company_name","label":"Company","dataType":"text"},{"key":"website","label":"Website","dataType":"text"},{"key":"description","label":"Description","dataType":"text"}]' --json
     oxygen tables insert <table> --rows-json '[{"company_name":"<as shown>","website":"<as shown, or empty>","description":"<as shown>"}]' --json
     ```
     Copy only what the page shows and leave a website empty rather than guess it. A page that loads more as you scroll returns only its first part; say which part you graded.
   Tell the founder: "Your companies are in a table: <web_url>."
4. Add the fit grade (free to add). Name every column the grade should read, since unnamed columns are not sent; a list from B or C uses its own keys (`oxygen tables describe <table> --json`). If the list holds companies that sell what the founder sells, ask once whether they count as competitors (graded low, the default) or as possible customers.
   ```bash
   oxygen columns add <table> --label "ICP fit" --key icp_fit --score 'low,medium,high' --grounding workspace --prompt 'How well does {{company_name}} ({{domain}}) fit our ideal customer? What they do: {{evidence}}. Industry: {{industry}}. Employees: {{employee_count}}. Location: {{location}}. Companies that sell what we sell are competitors: grade them low. Do not infer missing facts.' --json
   ```
   Tell the founder: "I added a fit grade that reads your saved ideal customer; adding it is free."
5. Price the grade (free): `oxygen columns run <table> icp_fit --limit 25 --dry-run --json`. Expect about 0.075 credits a company, about 2 for 25.
   Tell the founder: "Grading all 25 costs about 2 credits."
> APPROVAL GATE — scoring-run: show the 25 companies, the dry-run estimate and the cap of 5 credits.
6. Grade them and show the result (about 2 credits, then free reads):
   ```bash
   oxygen columns run <table> icp_fit --limit 25 --approved --max-credits 5 --json
   oxygen table-runs wait <run_id> --json
   oxygen tables query <table> --fields company_name,domain,industry,employee_count,location,icp_fit --limit 25 --json
   ```
   Count each row's `icp_fit.level` (high, medium, low) and name the industries, sizes and places the high grades share: that is the segment that fits best.
   Tell the founder: "<N> of 25 fit well, mostly <kind of company>. Table: <web_url>. Spent about 3 credits."
7. Offer the next step (no spend yet): another kind of company (for example agencies) repeats steps 2-6 with its own filters and `--table-name`, about 3 credits; the people at the high-fit companies come from outbound-pilot-50, which reads `company_name`, `linkedin_url` and `icp_fit` (a list from B or C has no `linkedin_url` yet; filling it costs about 1 credit a company).
   Tell the founder: "Shall I try <second group> for about 3 credits, or find the people at your best fits?"

## If It Goes Wrong

- `invalid_provider_enum_value` → an industry is free text; use the exact value from step 1.
- `invalid_filters` → a filter has the wrong shape: a range is `{"min":11,"max":50}` and countries sit in `geo.countries`; `hq.country_code` and `industry.include` are the free preview's spelling, not the planner's.
- An excluded group shows under `keywords.include`, or the plan's `intent` is not `structured_accounts` → the prompt carried an exclusion, another goal, or a word the planner reads as another kind of search (early-stage, niche, hiring, using, size); cut it to who buys, keep exclusions in `keywords.exclude`, and plan again with `--source-intent structured` (free). On such a plan `filter_application.dropped` can read empty even though the search ignores your exclusions and size range.
- `search_table_missing_columns`, or the ingestion ends `failed` with `invalid_cell_value` ("Fix the filters or the target table's columns") → a `--table` was passed; run again without it. The failed run may still have cost about 1 credit.
- The grade's dry run quotes about 4 credits a company → that is a full AI column, not the `--score` grade; add the step-4 column and run that instead.
- `invalid_prompt_column` when adding the grade → a `{{token}}` is not a column of this table; `oxygen tables describe <table> --json` lists the keys.
- Most companies grade low → the keywords describe what the founder sells rather than what buyers do, or competitors slipped in; fix the keywords, search one more page (about 1 credit) and grade it (about 2).
- The page read finds nothing or a 404 → the link moved (the audit's portfolio had moved from `/portfolio` to `/companies`); ask the founder for the link that works in their browser.
- The same company grades differently in two tables (seen in the audit) → a grade is a model judgment; read its reason before acting on it.
