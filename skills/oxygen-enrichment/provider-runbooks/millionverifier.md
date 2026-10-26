# MillionVerifier

MillionVerifier is OXYGEN's default email verifier for every workspace, on every surface. It answers first whenever an email needs checking: the work-email waterfall's pattern pre-step, the post-find verification leg, a `verify_email` table column, `oxygen verify email` and the `oxygen_verify_email` MCP tool all resolve to the same chain. It cannot resolve catch-all (accept-all) domains: there it answers `catch_all`, and OXYGEN escalates that address automatically to [BounceBan](./bounceban.md).

## Tools

| Tool | Use | Notes |
| --- | --- | --- |
| `millionverifier.verify_email` | Verify one known email address. | Managed by default; BYOK through the MillionVerifier connection with `credential_mode: user_api_key`. |
| `millionverifier.get_credits` | Check a key's remaining credits. | Read-only and free; used by the connection flow. |

## Routing

- To verify emails you already have, use `oxygen verify email` or the `verify_email` column, which run the full chain including the catch-all escalation ([verification](../references/verification.md)).
- To find an address, use the work-email waterfall (`oxygen enrich-column`); domain-based profiles run the pattern check through MillionVerifier before paid finder steps and verify the winner afterwards.

The verdicts (`unknown` is an absent answer, not a bad address) and sizing `--max-credits` from the dry run's all-catch-all worst case: [verification](../references/verification.md).

## Raw response

MillionVerifier's raw `result: ok` is `valid`; `disposable`, `spamtrap` and `do_not_mail` map to `invalid`. Keep the raw response in the cell or run output so later filters can read `quality`, `resultcode`, `subresult` and the credit balance fields when present.

```bash
oxygen tools get millionverifier.verify_email --json
```

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `millionverifier.get_credits` | free — not billed | no_bill | none | — |
| `millionverifier.list_files` | free — not billed | no_bill | none | — |
| `millionverifier.verify_email` | 0.225 cr | pre_authorize | paid_provider | — |
<!-- END GENERATED -->
