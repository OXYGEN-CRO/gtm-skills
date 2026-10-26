# Web research columns

Use a Web Research Agent column for anything whose answer is on the web: what a company sells, whether it raised, who its CEO is. One column type, two modes:

| Mode | What lands in the cell | Add it |
| --- | --- | --- |
| **Agent** (default) | An answer with its sources: `{answer, found, confidence, sources}` | `oxygen columns add <table> --kind research --label "<label>" --prompt "<question with {{column}} tokens>"` |
| **Keyword search** | The search results (title, link, snippet), no AI | `oxygen columns add <table> --label "Keyword search" --kind tool --definition-json '{"toolId":"serper.search","inputMapping":{"q":{"type":"template","value":"{{company_name}} funding"}}}'` |

Keyword search is cheaper; use it when a person or a later column picks from the results. Narrow it by country (`gl`), language (`hl`) and time range (`tbs`) as literals in `inputMapping`, such as `"gl":{"type":"literal","value":"de"}`; `oxygen tools enums get serper country --query germany --json` finds a code. Web: Add column, Web search, with the mode toggle at the top of the editor. A question OXYGEN already ships is a template with no prompt to write ([templates](templates.md)).

## Agent mode

```bash
oxygen columns add leads --kind research --label "What they sell" \
  --prompt "What does {{company_name}} ({{company_website}}) sell, and to whom?" --json
```

`--kind research` implies the web search, a jsonb cell and OXYGEN's defaults: no model or engine to pick.

```json
{ "answer": "Payroll and compliance software for European SMBs", "found": true, "confidence": "high",
  "sources": [{ "title": "Acme — Pricing", "url": "https://acme.example/pricing", "engine": "serper", "read_by": "web" }] }
```

- `sources` is built from what OXYGEN retrieved, never from the model, so a cell cannot invent a URL. A source with `read_by` was opened and read in full; one without it is a search result.
- Each source's `citation_index` retains its original evidence number, so inline citations such as `[3, 5]` still identify the saved URLs. Older cells may lack this field.
- No web evidence fails closed: the cell errors `grounding_unavailable`, only the searches that ran are billed, and the model is never called. Usually that is a query problem: set `--research-query`.
- **`found: false` means unknown, never no.** A page that does not mention an enterprise plan is not proof there is none. Filter on `found` and `confidence` before acting on a negative.
- Pull the answer into a text column with a formula: `path(what_they_sell, "answer")`.
- Several fields: ask for them in one prompt with named sections; each lands under `answer.<section>` for one read and one charge. A second research column over the same page pays for the same search again.

Tuning, in the order worth reaching for:

- `--research-query <template>`: the per-row search query, separate from the question. The biggest lever on quality.
- `--research-domains` / `--research-exclude-domains`: scope the search to sources you trust.
- `--research-mode strict` quotes figures and identifiers verbatim; `estimate` reasons to a number (revenue, headcount); the default may summarize across sources.
- `--research-results <n>`: evidence per row, 1-25 (default 5).
- `--research-depth quick|standard|deep`: one search and one page read, an agent planning a few searches (the default for new columns), or more searches plus subpages. `oxygen columns update <table> <column> --research-depth <depth>` changes it and keeps the query and domains. A row that runs out of time or budget answers `found: false` from what it found, with `validation.fallback` saying why.
- `--reasoning-level`: raise it for judgement across sources; it prices `quick` rows only.

One row wrong: re-run only that row with `columns run <table> <column> --row-id <row_id> --force` after raising the depth, or read the exact page with `--research-url`. Editing the prompt and forcing every row re-rolls the answers that were right and pays for them again. In the app these settings sit in the column editor's JSON under `webSearch`.

An AI column cannot search: `oxygen columns convert <table> <column> --to agent --yes` turns it into a research column under the same key, position and prompt and clears its results (without `--yes` it prints the plan and the per-row price before and after; `--to ai` goes back). A column the table's auto-run runs is refused until `tables auto-run disable <table>`, so it never runs at its new price unasked.

## Read one exact page per row

When a column holds the URL (a pricing page, a job post, an event page, a filing), point the research column at it and it reads that page instead of searching. The page is the only evidence, and a row without a URL fails closed.

```bash
oxygen columns add competitors --kind research --label "Plan count" \
  --prompt "How many pricing plans does this page list? Return the count and the plan names." \
  --research-url pricing_url --json
```

Fetch mode is strict by default; `--research-mode estimate` relaxes it for a figure the page implies. `--research-engine` pins the reader: `firecrawl` (default, JS and anti-bot pages) or `exa` (cached index, cheaper) in fetch mode; `serper` (default) or `exa` (semantic) in search mode.

## Cost

Do not quote a number from a page: it moves with the model tier, the engine and provider prices. Price YOUR column, free:

```bash
oxygen columns run leads what_they_sell --limit 1 --dry-run --json
```

- `expected_credits_per_row`: what a row usually costs. Budget with this.
- `estimated_credits` / `worst_case_credits_per_row`: the ceiling if every row falls through to the dearest lane. Multiplying it by the row count overstates a normal run.
- `recommended_max_credits`: the estimate plus headroom, for `--max-credits`. Unused credits are never spent.
- A lane on the customer's own key bills their provider plus OXYGEN's per-call BYOK platform fee when one applies (`oxygen billing usage --meter byok_calls`), whether or not it finds anything; all three numbers include it.

`oxygen tools search web --json` shows the Web Research Agent entry with each mode's live per-row price. Then run bounded batches after approval, repeating until `row_count` is 0:

```bash
oxygen columns run leads what_they_sell --limit 25 --approved --max-credits <recommended_max_credits> --json
```
