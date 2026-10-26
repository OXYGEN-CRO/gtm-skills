# RocketReach Runbook

> **Runs only on the workspace's own RocketReach key**, and is in no default chain. Connect it with
> `oxygen integrations connect rocketreach --api-key <key>` (or the RocketReach card on the
> Connections page; a key RocketReach rejects is refused), then select it with `oxygen tools run rocketreach.<operation>`, or
> `--provider-order` on an enrichment column.
> A call on your key spends your RocketReach credits; OXYGEN's per-call BYOK platform fee, when it applies, shows in the preview and in
> `oxygen billing usage --meter byok_calls --json`. The generated table lists OXYGEN's
> rates for reference.

Use RocketReach as a fallback people database for approved search and lookup work, and as an early work-email waterfall step when a row has a strong person identifier. Search returns candidate profiles without contact details; lookup is the paid enrichment step for one known person.

## Best Fits

- `rocketreach.people_search`: find candidate profiles by title, company, location, keyword, or other search filters.
- `rocketreach.person_lookup`: retrieve contact data for a reviewed person by id, LinkedIn URL, email, or name plus employer.

## Operating Pattern

1. Connect the key and inspect the descriptors:

```bash
oxygen integrations connect rocketreach --json    # lists the key field; stores nothing
oxygen tools search rocketreach --json
oxygen tools get rocketreach.people_search --json
oxygen tools get rocketreach.person_lookup --json
```

   `rocketreach.account` is free and shows the connected account's credit usage per type.
   Run `oxygen integrations test rocketreach` after rotating the key.
2. Use `people_search` with small `page_size` values and tight filters.
3. Store candidate rows in a Contacts table before lookup.
4. Lookup only rows that have a strong identifier and passed dedupe.
5. Persist provider ids, request status, contact fields, and error details for retries or fallback decisions.

## Cost And Safety

- RocketReach search and lookup consume your RocketReach credits. Require approval, row scope, and a credit cap before live runs.
- RocketReach stays registered in the work-email waterfall for an explicit `--provider-order`, and runs there only on the workspace's connected key (see banner above).
- Search does not return contact details. Do not treat a search result as outreach-ready.
- Prefer webhooks or slower status checks when a lookup is asynchronous for the provider account.

## Fallbacks

- Search alternatives: `blitzapi.people_search`, `dropleads.people_search`, `wiza.people_search`.
- Lookup alternatives: `contactout.people_enrich`, `wiza.person_reveal`, or `lusha.person_enrich` on the workspace's own Lusha key.
- If exact identity is uncertain, resolve LinkedIn URL first before paid lookup.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `rocketreach.account` | free — not billed | no_bill | none | — |
| `rocketreach.people_search` | 50 cr (example payload; estimate 2–50 cr) | pre_authorize | paid_provider | — |
| `rocketreach.person_lookup` | 50 cr | pre_authorize | paid_provider | — |
<!-- END GENERATED -->
