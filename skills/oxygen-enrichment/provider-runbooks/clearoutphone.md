# ClearoutPhone Runbook

Use ClearoutPhone to validate an existing phone number with `oxygen tools run clearoutphone.validate_phone`, or as a configured optional verifier after a phone source provider returns a candidate.

## Tools

- `clearoutphone.validate_phone`: real-time validation, one number per call, on OXYGEN's managed account or the workspace's connected ClearoutPhone key. The generated table below is its price; each live validation requires approval and a credit ceiling. You can validate a supplied number directly; optional waterfall verification checks a number returned by a source lane.
- `clearoutphone.get_credits`: free; checks a key and its remaining balance.
- `clearoutphone.bulk_status`: free progress read for a bulk job you created in your own ClearoutPhone account. OXYGEN does not create or download ClearoutPhone bulk jobs.

## Response Handling

The optional waterfall verifies a candidate only when `response.data.status` is `valid` and the response supplies a usable formatted number. An explicit `invalid` verdict rejects it. Unknown, missing or incomplete verdicts keep the original number as unverified, without replacing it with response formats or claiming carrier/line-type metadata.

Preferred normalized phone fields:

1. `data.e164_format`
2. `data.international_format`
3. `data.local_format`

When validation is enabled and ClearoutPhone returns `invalid`, the waterfall tries the next source. The saved verification attempt distinguishes `phone_verdict: valid | invalid | unknown` and retains actual billing. Successful validation responses are billed per call, including invalid and unknown verdicts; verifier failures preserve the candidate and follow the tool runner's error/uncertain-outcome accounting.

## Gotchas

- Errors arrive as `{"status":"failed","error":{"code":<n>,"message":"..."}}`, sometimes with HTTP 200. OXYGEN puts the vendor code in the error message (for example `[1030] ...`); read that code, not the HTTP status.
- Test numbers ClearoutPhone documents can smoke-test validation without consuming credits.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `clearoutphone.bulk_status` | free — not billed | no_bill | none | — |
| `clearoutphone.get_credits` | free — not billed | no_bill | none | — |
| `clearoutphone.validate_phone` | 1.75 cr | pre_authorize | paid_provider | — |
<!-- END GENERATED -->
