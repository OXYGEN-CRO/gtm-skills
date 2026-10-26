# People Data Labs Runbook

> **Company funding and revenue fall back to it; it is not in the default email, phone or LinkedIn URL
> chains.** Select it explicitly with `--tool-id` or `--route-id` on a search run, or `--provider-order`
> on an enrichment column.

Use People Data Labs when a workflow needs a broad structured data fallback for company, person, or contact enrichment after more purpose-built providers miss.

## Best Fits

- `peopledatalabs.company_search`: search companies with explicit structured criteria.
- `peopledatalabs.company_enrich`: enrich one known company from domain, name, profile URL, ticker, or PDL id.
- `peopledatalabs.person_search`: search people with explicit structured criteria.
- `peopledatalabs.person_enrich`: enrich one known person from email, profile URL, phone, or name plus company.
- `peopledatalabs.autocomplete`: discover valid field values before building exact searches.

## Operating Pattern

1. Inspect descriptors before composing provider-native filters:

```bash
oxygen tools search peopledatalabs --json
oxygen tools get peopledatalabs.person_enrich --json
oxygen tools get peopledatalabs.company_search --json
```

2. Use company or person search only after the row scope is narrow and the requested fields justify PDL.
3. For work-email enrichment, prefer profile URL, known email, or full name plus company in that order.
4. Persist provider ids, raw result pointers, status, and errors to table/run provenance.

## Cost And Safety

- PDL is a metered fallback in the work-email waterfall. Use preview, row scope, and a credit cap before live runs.
- Search payloads can become broad quickly; use small pilots before large pulls.
- Autocomplete is a planning step and should not be treated as contact enrichment.

## Fallbacks

- For work email, prefer the high-level `work_email` enrichment column before direct PDL calls.
- If profile URL is missing, resolve it first or use name+domain providers before PDL.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `peopledatalabs.autocomplete` | free — not billed | no_bill | none | — |
| `peopledatalabs.company_enrich` | 16 cr | pre_authorize | paid_provider | — |
| `peopledatalabs.company_search` | 16 cr | pre_authorize | paid_provider | — |
| `peopledatalabs.person_enrich` | 44.8 cr | pre_authorize | paid_provider | — |
| `peopledatalabs.person_search` | 44.8 cr | pre_authorize | paid_provider | — |
<!-- END GENERATED -->
