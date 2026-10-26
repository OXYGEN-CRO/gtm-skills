# WhiteWhale Runbook

Use this runbook when OXYGEN tool discovery returns `whitewhale.*` tools. WhiteWhale (formerly BirdDog) monitors a workspace's target accounts for custom buying signals: yes/no questions about each company, answered from news, filings, job boards, company sites and LinkedIn posts, with the sources attached. It scores each account's fit, and its Farsight finder suggests new accounts that match an ICP.

Do not use WhiteWhale to find or verify contact data, send messages or write CRM records. Its contacts read is a beta convenience; use the people-search and email-verification providers for coverage.

## Credentials

WhiteWhale runs only on the workspace's own WhiteWhale account. OXYGEN has no managed WhiteWhale key.

Connecting needs two values: the instance's API key and the email of a user in that instance. Every call acts as that user, but reads are not limited to that user's ICPs: `get_accounts`, `icp_details` and `get_all_user_data` can return the whole instance.

```bash
oxygen integrations connect whitewhale --json   # free preview of both fields; nothing stored
```

Then submit both in Connections, or `--api-key <key> --credential userEmail=<email>` for controlled noninteractive use. OXYGEN checks the pair with WhiteWhale's free user read before it stores anything. A user email WhiteWhale does not know is refused with `whitewhale_user_not_found`.

## What to call

| Goal | Tool | Notes |
| --- | --- | --- |
| Check the connection, credits, ICP ids and signals | `whitewhale.get_user_data` | Free at WhiteWhale. `icp_id_dict` maps ICP names to ids. |
| Scores and positive signals for given companies | `whitewhale.get_accounts` with `account_filter` | Domains in, one array of accounts out. |
| Every tracked account | `whitewhale.get_accounts` with `lite: true`, `status`, `limit`, `offset` | A full account can exceed 100 KB. Page with `lite` until a page has fewer than `limit` rows, then read full accounts by `account_filter`. |
| Contacts WhiteWhale matched to an account | `whitewhale.get_account_contacts` | Up to 10, by the instance's target titles. Beta. |
| Start tracking companies | `whitewhale.upload_accounts` | Farsight pre-scoring by default; `farsight: false` tracks at once. |
| Activate, archive or delete accounts | `whitewhale.change_accounts_status` | `active` spends one WhiteWhale account credit per account. |
| Add or remove signal questions | `whitewhale.add_signals`, `whitewhale.delete_signal` | Questions use `{account}`; check `whitewhale.get_signal_templates` first. |
| Configure the Farsight finder | `whitewhale.farsight_state_switch`, `whitewhale.update_farsight_constraints`, `whitewhale.update_farsight_employee_bounds`, `whitewhale.run_farsight` | Needs a rank 6 signal; one run per ICP every two hours. |
| Send account and signal events somewhere | `whitewhale.set_webhook`, `whitewhale.test_webhook` | Replaces the user's webhook URL; an empty URL removes it. |

Signal ranks: 0 disqualifies a matching account, 0.1 low, 1 normal, 6 high. Farsight only finds accounts with at least one rank 6 signal.

## Before running

```bash
oxygen tools search whitewhale --json
oxygen tools get whitewhale.get_accounts --json
oxygen tools run whitewhale.get_accounts --mode dry_run --input-json '{"account_filter":["example.com"],"signal_data":true}' --json
```

To keep WhiteWhale accounts in a Table, import one page of `whitewhale.get_accounts` at a time with `oxygen table-ingestions create-tool-page` and `--rows-path response.results`; WhiteWhale pages by `limit` and `offset`, not a cursor. Map `name` (the domain), `scaled_score` and `signal_list`, and keep `limit` small (about 25): `lite` would leave `signal_list` empty.

## Approval

Writes change the connected WhiteWhale instance and always need `approved=true` after a dry run; confirm the exact accounts, ICP or signal with the operator first. Each tool's quote (`oxygen tools get`) carries OXYGEN's own-key fee per call, and a positive fee also needs a `max_credits` ceiling. `change_accounts_status` with `delete`, `delete_signal` and `delete_user` remove data from WhiteWhale, and `delete_user` also deletes that user's ICPs. `create_user` uses a WhiteWhale seat.

Several writes answer success without checking their target: the Farsight operations accept any ICP id, and `change_accounts_status` succeeds when no listed account matched. Read the ICP or the accounts back before reporting a change.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `whitewhale.add_icp` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.add_signals` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.change_accounts_status` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.create_user` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.delete_signal` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.delete_user` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.farsight_state_switch` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.get_account_contacts` | free — not billed | no_bill | none | BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.get_accounts` | free — not billed | no_bill | none | BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.get_all_user_data` | free — not billed | no_bill | none | BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.get_signal_templates` | free — not billed | no_bill | none | BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.get_user_data` | free — not billed | no_bill | none | BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.icp_details` | free — not billed | no_bill | none | BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.industries` | free — not billed | no_bill | none | BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.location_codes` | free — not billed | no_bill | none | BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.normalize_accounts` | free — not billed | no_bill | none | BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.run_farsight` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.set_webhook` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.swap_icp` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.test_webhook` | free — not billed | no_bill | external_send | external write — live gate (approved + max_credits); BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.update_farsight_constraints` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.update_farsight_employee_bounds` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
| `whitewhale.upload_accounts` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); BYOK — runs on the org's connected `whitewhale` API key; provider-side charges may apply |
<!-- END GENERATED -->
