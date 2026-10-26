# BounceBan

BounceBan is Oxygen's **catch-all escalation verifier**. It runs automatically, and only on the addresses that need it.

Most email verifiers can tell you a mailbox exists or does not. What they cannot do is answer for a **catch-all (accept-all) domain** — a domain configured to accept mail for every address, so a probe of `anything@domain.com` succeeds whether or not the mailbox is real. [MillionVerifier](./millionverifier.md), Oxygen's default first pass, can only label those `catch_all`. BounceBan resolves a large share of them, including addresses behind secure email gateways.

## When it runs

You do not configure this. In the default chain:

1. MillionVerifier verifies the address.
2. If the verdict is `catch_all`, Oxygen escalates that address to `bounceban.verify_single_waterfall`.
3. BounceBan's verdict is final.

It fires **only** on a `catch_all` verdict. It does not fire on `unknown` — an inconclusive first pass is a verifier hiccup, not evidence of a catch-all domain, and re-asking the expensive provider would not answer it.

Because escalation is per-address and conditional, the cost of verifying a list depends on how many of its domains are catch-all. A list with no catch-all domains never touches BounceBan at all.

## Tools

| Tool | Use | Notes |
| --- | --- | --- |
| `bounceban.verify_single_waterfall` | Resolve one catch-all / SEG-protected address. | The escalation step in the default chain. Managed by default; BYOK supported through the BounceBan connection. |
| `bounceban.verify_single` | Single verification without the provider-side waterfall. | Cheaper path, lower catch-all resolution rate. |
| `bounceban.verify_bulk` | Batch verification. | Billed per email in the batch. |
| `bounceban.check` | Check email/domain syntax and address/domain type. | Paid provider call; hydrate the current quote before running. |

## Output handling

- `deliverable` → `valid`, including when `is_accept_all` is true: the specialist has resolved the mailbox.
- `is_accept_all` describes the domain. It does not override a final mailbox verdict or supply a missing one. Missing, pending or unrecognized results remain `unknown` and unverified.
- `risky` → BounceBan's word for an unresolved accept-all; Oxygen maps it to `catch_all`.
- `undeliverable` → `invalid`.
- `unknown` → BounceBan refunds these vendor-side, and Oxygen only charges you when a real verdict comes back.

## Previewing readiness

The free dry run (`oxygen verify email <address> --json`) reports whether the escalation can run; how to read `catch_all_escalation_available`: [verification](../references/verification.md). A configured route is not spend authorization: a live check still needs approval and an explicit credit ceiling.

## Reading `escalation_skipped`

When a catch-all address comes back without an escalation, read the reason before retrying:

| `escalation_skipped` | What it means | What to do |
|---|---|---|
| `budget_exhausted` | The run's remaining `--max-credits` could not cover an escalation call, so it was never dialled. **Nothing is wrong with the provider**, and nothing was charged. | Re-run those addresses with a higher ceiling — use `estimate.recommended_max_credits` from the dry run. |
| `escalation_unavailable` | Escalation could not run or could not answer. A known account refusal or staff hold can stop it before any provider call. Read `escalation_unavailable_reason`. | See the next table. |
| `not_configured` | Escalation was explicitly disabled for this run. | Nothing, if intended. |

Whatever the reason, the address **keeps `catch_all` and is recorded as unconfirmed** — never as verified. Every skipped escalation also carries a `next_action` sentence on the result (and the most serious one at the top of the envelope); read it before deciding to retry.

| `escalation_unavailable_reason` | What it means | What to do |
|---|---|---|
| `provider_account_dry` | The BounceBan account this call bills against has no provider credits left (HTTP 402, or a 403 whose body carries `credits_remaining: 0`). On the default **managed** lane that is **Oxygen's** BounceBan balance, not the workspace's Oxygen credits, and the customer was **not** charged for the escalation. | Nothing customer-side fixes it: Oxygen staff must top the managed BounceBan account up. Retrying before that fails identically. Re-run the affected addresses after the top-up. On a BYOK connection the dry account is the customer's own — they top up BounceBan, then re-run. |
| `provider_account_held` | Oxygen staff has placed a hold on the managed account. The escalation was not charged; an earlier first-pass verification may still have cost credits. | Oxygen staff must review and release the hold. Funding the wallet or waiting for a retry interval alone does not release it. Keep the address unconfirmed. |
| `not_configured` | No usable BounceBan credential for this workspace. Nothing was dialled or charged. | `oxygen integrations connect bounceban --api-key <key>` for BYOK, or ask Oxygen support to enable the managed lane. |
| `outcome_unknown` | BounceBan was dialled but never confirmed a result (`provider_outcome_unknown` or `provider_verification_pending`). Its credits are held, not charged, until the outcome settles. | Do not re-run the address yet; a repeat could be charged twice. Inspect the hold with `oxygen billing usage --meter holds`. |
| `provider_error` | BounceBan was dialled and returned an error or timed out. The failed leg is not counted in `credits_used`. | Usually transient — re-run later. The attempt's `provider_message` carries BounceBan's own words; the attempt's `message` is Oxygen's classification of them. |

A ceiling sized as "N addresses × first pass" runs out after a few catch-all addresses and leaves the rest unescalated; size it from the dry run's worst case ([verification](../references/verification.md)).

## Commands

Use `oxygen` in the authenticated environment. Do not switch environments to resolve a provider refusal.

```bash
# The escalation runs inside the normal verify path — you do not call it directly.
oxygen verify email someone@catchall-domain.com --mode live --max-credits <estimate.recommended_max_credits> --json

# Inspect the tool itself.
oxygen tools get bounceban.verify_single_waterfall --json
```

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `bounceban.check` | 1.7 cr (example payload; estimate 0–1.7 cr) | pre_authorize | paid_provider | — |
| `bounceban.destroy_bulk` | free — not billed | no_bill | external_send | external write — live gate (approved + max_credits) |
| `bounceban.export_bulk` | free — not billed | no_bill | none | — |
| `bounceban.get_account` | free — not billed | no_bill | none | — |
| `bounceban.get_bulk_dump` | free — not billed | no_bill | none | — |
| `bounceban.get_bulk_emails` | free — not billed | no_bill | none | — |
| `bounceban.get_bulk_status` | free — not billed | no_bill | none | — |
| `bounceban.get_single_status` | free — not billed | no_bill | none | — |
| `bounceban.verify_bulk` | 3.4 cr (example payload; estimate 0–1.7 cr) | pre_authorize | paid_provider | async — returns a job handle; poll for completion |
| `bounceban.verify_bulk_file` | 1.7 cr (example payload; estimate 0–1.7 cr) | pre_authorize | paid_provider | async — returns a job handle; poll for completion |
| `bounceban.verify_single` | 1.7 cr (example payload; estimate 0–1.7 cr) | pre_authorize | paid_provider | async — returns a job handle; poll for completion |
| `bounceban.verify_single_waterfall` | 1.7 cr (example payload; estimate 0–1.7 cr) | pre_authorize | paid_provider | — |
<!-- END GENERATED -->
