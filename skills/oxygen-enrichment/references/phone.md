# Mobile phone

This finds phone numbers, a paid enrichment. It calls nobody: dialing is a Sequence call task (`oxygen voice --help`, the `oxygen-sequencer` skill).

Phone lookup is a high-scrutiny paid action: preview, show the lane order and the ceiling, then pilot one row before any batch, and only on reviewed, qualified rows.

## Preview

The best identity input is a person LinkedIn URL, then a known work email, then a full name plus company domain or name. The column detects a `linkedin_url` (or email) source column itself; when it cannot, the error names the flags to pass (`--source-column`, `--email-column`) and lists the table's columns.

```bash
oxygen enrich-column preview <contacts_table> --capability mobile_phone \
  --source-column linkedin_url --target-column mobile_phone_enrichment --json
```

The preview shows provider preflight, input coverage, per-lane managed credits, the row estimate, the recommended ceiling and the table link. Read the two credit figures differently: a waterfall bills on success and stops at the first lane that returns a number, so a row pays for one lane, not the chain.

| Field | Meaning |
| --- | --- |
| `expected_credits_per_row` / `expected_credits` | The average: each lane weighted by how often it is the one that resolves a row. Quote this. |
| `estimated_credits_per_row` / `estimated_credits` | The worst case: the dearest source lane on every row. Report it as "up to". |
| `recommended_max_credits` | Pass this as `--max-credits`: the average plus a variance band that covers unlucky rows. Sizing the cap from the worst case overstates realistic spend several times. |
| `expected_hit_rate` / `expected_match_rate` | The modelled share of rows the chain resolves, and the same figure as a band. |
| `expected_credits_hit_rates_assumed` | `true` while the per-lane rates are assumptions; say so when quoting the average. |

Both `expected_*` fields are null when a managed lane has no resolvable price. Nothing is held against the balance when the run is created: each provider call reserves before it runs, captures on a hit and releases on a miss. A run that reaches its ceiling keeps the rows it completed and finishes `completed`; a plain re-run resumes the unfilled rows.

## Lanes

The lanes run cheapest first. The first lane is LinkedIn-keyed and covers US numbers only, so rows without a LinkedIn URL and non-US numbers start at the managed lanes behind it and cost more per row; the broad aggregator lane runs last, only after the cheaper lanes miss. The preview names every lane and its price; `oxygen tools get <tool_id> --json` quotes one. Other providers stay selectable with `--provider-order`; some run only on the workspace's own key (each provider runbook says which), and the preview reports a lane it cannot run. Add one only when a bounded pilot proves extra coverage for the target region and input shape.

## Pilot and batch

Without `--approved` the server refuses with `approval_required` (exit 7); `oxygen table-runs cancel <run_id>` before pickup spends nothing.

```bash
oxygen enrich-column run <contacts_table> --capability mobile_phone \
  --source-column linkedin_url --target-column mobile_phone_enrichment \
  --limit 1 --approved --max-credits <recommended_max_credits> --json
```

The first-class phone verification column stays `coming_soon`; this workflow performs source enrichment. Direct validation of an existing number is available through [ClearoutPhone](../provider-runbooks/clearoutphone.md). A configured optional waterfall verifier is separate from this source-only workflow; unknown or incomplete verdicts keep the original number unverified, while explicit invalid rejects it. A source-only run on an existing column clears any legacy phone verifier so it cannot make an unquoted call. Approval for a batch names the table, the row scope, the lane order, the expected and up-to credits, the ceiling, the pilot output and the run link.

## QA

- Keep the raw jsonb payload apart from the normalized `mobile_phone_e164`, with the provider, status, enrichment time, cost and run provenance.
- Stop when the preflight shows no lane can run from the mapped inputs.
- A found number is not permission to call or to write it to a CRM: those are separate approvals.
