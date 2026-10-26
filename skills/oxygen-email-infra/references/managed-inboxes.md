# Managed inboxes

OXYGEN sells managed sending inboxes: one order buys a sending domain plus Google Workspace, Microsoft 365 or Azure mailboxes, provisioned by InboxKit and billed in OXYGEN credits. The quote returns `monthly_credits` and `one_off_credits`; an approved order reserves them and captures on provisioning, and renewals debit monthly. Insufficient funds initially pause renewal; cancellation can follow when the funding grace ends or the provider's paid term expires. Mailboxes from your own InboxKit account are imported like any other mailbox ([import and OAuth](import-and-oauth.md)).

## Address names

Choose addresses that read like the real person sending: `phil`, `philipp`, `philipph`, `philipp.hirte` or `p.hirte` for Philipp Hirte. Use that person's sender profile and display name. Do not invent other people, append numeric sequences (`philipp001` to `philipp100`), or pad a requested count with increasingly artificial aliases. Numeric names are allowed when the user explicitly chooses them.

Show the exact proposed addresses before purchase, check existing and retired addresses, and resolve collisions without adding numbers automatically. If the count exceeds credible variants, explain the constraint and agree on fewer inboxes, other real senders, or additional owned domains and their costs before ordering. The CLI takes explicit names through `--locals <names> --sender <id>` or `--mailboxes`/`--file`; the retired `--count`/`--prefix` shorthand generates nothing.

## Entra pricing and sending limits

Azure/Entra inboxes pay 25 credits ($0.25 face value) per inbox/month for Sequencer and included warm-up. Managed tenant hosting is a separate 4,000 credits ($40)/month for up to 100 inboxes: 100 inboxes total 6,500 credits ($65), before optional placement or domain charges. Imported Entra inboxes pay only their connection fee in Oxygen. Explicit infrastructure metadata identifies Entra; a crowded Microsoft domain alone does not qualify for this price.

Entra campaign sending is capped at 2 per inbox/day across Sequences, even with its ramp off. This is separate from provider warm-up: the dedicated tenant warm-up ceiling is at most 5 per inbox/day within a 250/day domain budget (2 per inbox/day at 100), including maintenance. Higher configured caps cannot override these limits. Read the actual quote and `mailboxes get` / `limits show`; daily capacity is a ceiling, not guaranteed delivery.

## Sender profiles

A sender profile is one person's sending identity: first name, last name and photo, shared by their inboxes and their LinkedIn and WhatsApp accounts. Every inbox belongs to one.

- `oxygen senders profiles list --json` lists them; `senders profiles create --name "<full name>" --first-name <first> --last-name <last>` makes one, and `senders profiles create --from-linkedin <sender_account_id>` makes one from a connected LinkedIn account, photo included.
- `senders profiles attach <other-id> --mailboxes <mailbox-id>` moves an inbox to another person. Detaching an inbox is refused (no inbox is ownerless), and deleting a profile is refused while it owns inboxes.
- A one-word display name leaves the surname blank rather than guessing, and ordering refuses it: ask the user for the real surname instead of inventing one.
- An order naming a sender refuses `sender_profile_not_found` (wrong id: `senders profiles list`), `sender_profile_archived` (`senders profiles update <id> --status active`, or pick another person) and `sender_profile_incomplete` (`senders profiles update <id> --first-name <first> --last-name <last>`).

## Order

```bash
oxygen managed-inboxes subscribe <domain> --provider google --sender <sender_profile_id> --locals ada,ada.lee --billing ./registrant.json --json
oxygen managed-inboxes subscribe <domain> --provider google --sender <sender_profile_id> --locals ada,ada.lee --billing ./registrant.json --approved --quote <quote_id> --json
```

- The first command is a free priced preview with a `quote_id`; the second places the order. `--locals` gives one person several addresses on the domain; `--provider microsoft` or `azure` picks the platform. `--billing` (the registrant contact) is needed on the first order only.
- Both the preview and the receipt return `senders[]`: per person, the exact `first_name`, `last_name`, `addresses`, `profile_picture_url` and `avatar_durable` to be stamped. Read it to the customer before approval; it is the last moment anything can change.
- Items can name people per mailbox: `--mailboxes '[{"username":"ada","sender_profile_id":"<id>"},{"username":"ops","first_name":"Ada","last_name":"Bennett"}]'`. When an item names a sender, its own name and photo fields are ignored.
- A domain you already own through OXYGEN takes more inboxes with `managed-inboxes add-inboxes <domain> --sender <id> --locals <names>` (preview, then `--approved --quote <id>`); no domain is registered again. A saved per-domain limit caps it; raise or lower it with `--max-per-domain <n>` on both the preview and the approval (never above the platform cap, never below the inboxes already there).
- Inboxes need a paid plan: on Free an approved order returns `402 upgrade_required`. Relay `upgrade_url` and tell the user to subscribe, never to top up; the quote stays free on every plan.
- Approval reserves the quoted credits; `402 insufficient_credits` means top up (`oxygen billing topup`) and approve the same quote again.

## Profile pictures

The photo is fetched at provisioning, so it has to be hosted by OXYGEN; otherwise the order ships the default face with `avatar_durable: false` and a warning, and the picture cannot be changed afterwards. Make it durable before ordering: `oxygen senders profiles set-photo <sender_profile_id> --file ./ada.png --json`, or `--from-linkedin` to copy the connected LinkedIn photo. A LinkedIn-connected sender carries that account's photo automatically; an uploaded photo wins over it. `avatar_source` says where the picture came from. For a typed-name order without a sender, `managed-inboxes upload-avatar ./ada.png` returns a hosted `profile_picture_url` (PNG, JPEG or WebP, up to 8 MB).

## Existing Cloudflare domains

Google, Microsoft and Azure/Entra support existing Cloudflare domains. Azure allows up to 100 inboxes per domain; the quote charges one tenant plus each inbox's connection. Disabled and historical inboxes still count as occupied until explicitly reconciled.

For a domain in `oxygen domains list`, preview with `managed-inboxes subscribe <domain> --existing-domain --provider google --sender <id> --locals <names> --max-per-domain 2 --preview --json`. It buys mailboxes only, with no registration charge, and its `existing_domain` block shows ownership, occupied addresses, DNS scope and blockers; `executable: false` means resolve them before approval. `--max-per-domain` saves a limit with the approved order, counting existing and parked inboxes, and later `add-inboxes` orders honor it. In the app: Buy inboxes, Use Cloudflare domains.

- Read `existing_domain.connection_requirements` and `inbox_workspace` before approving. A domain in Oxygen's managed Cloudflare account that this workspace owns (bought, adopted or from an earlier order) connects with Oxygen's own credential in Oxygen's shared provider workspace; nothing to connect. A domain in your own Cloudflare account uses your connected token (Zone Read and DNS Edit) in a dedicated provider workspace for this Oxygen workspace, created by the first such approved order (`create_on_approval`); `credential_scope.zones_visible` lists every zone that token can reach. Follow the live requirement instead of asking for a new key when it already verifies.
- Leftover email DNS (MX, SPF, DKIM, DMARC, Autodiscover from an earlier provider) is listed in `existing_domain.dns.records_to_remove` and `dns.cleanup`. Approving the order's `quote_id` removes exactly those records first, then connects and buys; no separate cleanup approval is needed. Any DNS change after the preview refuses the order before anything is charged. Approve only if the domain does not receive email; a domain with existing or historical inboxes is refused. The standalone `--dns-cleanup-records` / `dns_cleanup` path remains optional and buys nothing.
- A domain already subscribed through OXYGEN grows with `add-inboxes`; a first subscription on an occupied domain waits until its existing inboxes are reconciled.
- The managed setup writes the email DNS records itself; the self-managed `domains dns plan` and `apply` are not this order's plan.

## Native sending authorization

New inboxes join the pool without sending authorization; OXYGEN requests it per inbox, usually within minutes, and nobody signs in. Warm-up neither depends on it nor proves it. Read `oxygen mailboxes oauth-health --json`:

- `oxygen_native_send.state: connected` is the only proof that this exact inbox can send natively.
- `consent_state: client_id_not_approved`: approval is still landing; OXYGEN retries by itself, so wait.
- `consent_state: client_id_refused` (`blocked: true`): no automatic retry will connect it, and the remedy becomes a per-inbox browser sign-in. Read `blocked_message` first: a Microsoft row saying the client id "belongs to the oxygen pool" is approved, and one manual run clears it.
- `consent_checked: false`: the state could not be read on this call, so a null `consent_state` is unknown.

To run it now, preview then approve (both 0 credits): `oxygen mailboxes connect-oauth --provider google --vendor inboxkit --json`, then the same with `--approved --plan-hash <plan_hash>`; `--status <run_id>` polls. `--provider microsoft` covers Microsoft and Azure; `--domains` narrows the run. The preview lists exact consent candidates, skipped reasons and domain/client approvals. Client approval requests are a separate phase: they authorize no mailbox, so preview again after approval lands. An empty executable scope is a no-op.

Microsoft needs two consent screens: the first authorizes reading, the second sending. A refused second screen reads `transport_reason: smtp_not_consented`, and sends fail `native_email_smtp_not_consented`. Re-run the per-inbox grant and finish both screens: `oxygen mailboxes connect-oauth --vendor oxygen --provider microsoft --mailboxes <address> --approved --json`. Tenant admin consent does not cover this.

## Warm-up

A fresh order includes OXYGEN Warm-up by default ([warm-up](warmup.md)): approving the order approves warm-up for exactly those addresses, so skip a second warm-up preview. An order with `--no-warmup`, or a later enrollment, uses `mailboxes warmup enable`. Managed inboxes need no password or warm-up login.

## Cancel or move

`managed-inboxes cancel` ends an order and `managed-inboxes exit` moves a domain to another provider: [wind-down](wind-down.md).

## Recover canceled inboxes

Inspect `oxygen managed-inboxes list --status cancelled --json`, then preview recovery of the existing domain:

```bash
oxygen managed-inboxes recover <domain> --json
oxygen managed-inboxes recover <domain> --approved --quote <quote_id> --max-credits <upfront_credits> --json
```

The first command is read-only and costs zero credits. Show the exact original addresses, provider eligibility, upfront credits, recurring hosting and connection costs before approving the second command. Hosted MCP uses `oxygen_managed_inboxes_recover` with the same domain, quote, ceiling and approval. Recovery preserves the original domain, addresses, sender profiles and history; eligibility depends on the provider's remaining recovery window.

The same command adopts inboxes the provider revived on an order that had failed (`managed-inboxes verify` reports `vendor_revived_mailboxes`): the preview lists the exact provider mailboxes and the normal monthly price, and its approval reopens the order for them. Warm-up and billing then follow the order as usual.

If Microsoft requires replacement licenses, request a fresh preview with `--rebuy` and separately approve that quoted scope and ceiling. Recovery waits while an earlier cancellation is pending or uncertain. Interrupted provider attempts are reconciled before any repeat; keep partial receipts for support. After provider restoration, verify each mailbox's sending authorization and warm-up, then resume only healthy senders under their existing bounce protections and ramp limits. Provider recovery alone does not prove sending or warm-up progress.

## Troubleshooting

| Symptom | Meaning |
| --- | --- |
| `409 inbox_pricing_unsigned` on the quote | A mailbox type cannot be priced now. Nothing was ordered; retry later or choose another platform. |
| `409 quote_mismatch` on approval | The approval differs from its preview; `details.changed` names what (`price`, `addons`, `addresses` or `order`). Nothing was ordered: preview the exact order again and approve that `quote_id`. |
| `402 upgrade_required` on approval or recovery | The workspace is on Free, and inboxes need a paid plan. Relay `upgrade_url`; credits do not help. |
| `402 insufficient_credits` on approval | The quote exceeds the balance. Top up, then approve the same quote. |
| `503 inboxkit_wallet_insufficient` | OXYGEN's own supplier capacity is short. Nothing was ordered or charged; tell the customer and contact support. |
| Order stays `pending` | The supplier is still provisioning; `managed-inboxes get <domain>` shows the state. Contact support after a day. |
| Imported but not sending | Read `mailboxes oauth-health --json` and follow its `consent_state`. |
| Microsoft send fails `native_email_smtp_not_consented` | The second Microsoft consent screen was skipped: re-run the per-inbox grant. |
| Warm-up preview reports a vendor warm-up | One inbox warms on one network only: contact support to cancel the other, then preview again. |
