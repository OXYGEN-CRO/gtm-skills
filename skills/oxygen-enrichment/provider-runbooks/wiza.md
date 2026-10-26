# Wiza Runbook

Use Wiza for preview-first people discovery and single-contact reveal workflows. Wiza search returns prospect previews; reveals are the paid step for profile, email, or phone data.

## Best Fits

- `wiza.people_search`: sample or size a persona segment from Wiza filters before enrichment.
- `wiza.person_reveal`: enrich one reviewed contact from a LinkedIn URL, a full name plus company or domain, or an email. It waits for the reveal and returns the finished result.
- `wiza.person_reveal_get`: read a reveal by id (free), for a reveal that came back pending.

## Operating Pattern

1. Discover the current schema:

```bash
oxygen tools search wiza --json
oxygen tools get wiza.people_search --json
oxygen tools get wiza.person_reveal --json
```

2. Start with a preview search and a small `size`.
3. Write preview rows into a Contacts table with `source_tool`, `source_query`, and raw provider output.
4. Reveal only rows that pass `account_fit`, `title_fit`, dedupe, and user approval.
5. Store the reveal id, status, requested level, final credits, email status, phone fields, and provider response in table columns or run provenance.

## Cost And Safety

- `wiza.people_search` is a no-reveal discovery step.
- `wiza.person_reveal` is paid provider work. Lower-cost email pilots should avoid phone or full reveal unless the user approved phone spend.
- Put the identity under `individual_reveal`, one shape per call: `{"profile_url": ...}` (best), `{"full_name": ..., "domain": ...}` or `{"email": ...}`. `enrichment_level` is `partial` (email), `phone`, `full` (both) or `none` (profile only).
- Reveals are asynchronous at Wiza. OXYGEN waits for the result (up to about a minute) and returns it with `meta.outcome` `found`, `no_match` or `failed`.
- A slower reveal returns `meta.outcome: "pending"` with its id. In a table the cell fills in by itself when Wiza finishes; for a one-off call, read it with `wiza.person_reveal_get`. The credits stay held until then.
- You are charged only when Wiza returns the requested data: a valid email, a phone, or a matched profile. Risky or missing emails, failed reveals and reveals that never finish (released after 30 minutes) cost nothing.

## Fallbacks

- Preview search alternatives: `blitzapi.people_search`, `dropleads.people_search`, `contactout.people_search`.
- Email reveal alternatives: `contactout.people_enrich`, `hunter.email_finder`, or `findymail.find_from_name` on the workspace's own Findymail key.
- Phone reveal alternatives: `leadmagic.mobile_finder`, `contactout.people_enrich`, or `lusha.person_enrich` on the workspace's own Lusha key.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `wiza.people_search` | free — not billed | no_bill | none | — |
| `wiza.person_reveal` | 25 cr (example payload; estimate 0–25 cr) | pre_authorize | paid_provider | async — returns a job handle; poll for completion |
| `wiza.person_reveal_get` | free — not billed | no_bill | none | — |
<!-- END GENERATED -->
