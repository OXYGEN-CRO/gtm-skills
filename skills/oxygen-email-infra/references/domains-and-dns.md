# Domains and DNS

`oxygen domains` works on two rails. With the workspace's own Cloudflare account connected, purchases go through its Cloudflare Registrar and bill its card, and DNS lives in its zones. Without one, OXYGEN registers the domain at the registrar's cost in credits. Cloudflare DNS writes cost no Oxygen credits; DNS editing for Oxygen-bought domains is unavailable. A domain bought together with inboxes is a managed-inbox order ([managed inboxes](managed-inboxes.md)).

## Buy a domain

```bash
oxygen domains search <name> --json
oxygen domains check send-acme.com mail-acme.io --json
oxygen domains buy send-acme.com --json
oxygen domains buy send-acme.com --approved --quote <quote_id> --json
```

- Search and check are free; check prices up to 20 exact names and returns `reason: "owned"` for a domain the workspace already holds.
- Registration and renewal have separate prices. Check or preview the exact name for a nullable renewal estimate; search suggestions can leave it unknown. Dollar equivalents for credit prices are face value (100 credits = $1), while Cloudflare bills its card directly. There is no native name-free TLD rate card.
- `domains buy` is real money and non-refundable on both rails. The preview returns the price, the `registrar` (`cloudflare` bills the card, `oxygen` bills credits) and a `quote_id`; buy only with `--approved --quote <id>`. `--billing <file>` supplies the registrant contact the first time.
- An OXYGEN-registered domain renews yearly, charged in credits 30 days before expiry; a short balance starts a 7-day grace (`renewal_status: past_due`), after which the domain lapses at expiry. `domains renewal <domain> --off` stops renewing; `domains list` shows expiry and renewal status.
- The list's `renewal_credits` is the last recorded amount, not a guaranteed quote for the next renewal. The registrar cost is checked again before charging.
- Its first inboxes are an ordinary `managed-inboxes subscribe` on that domain: the preview says `domain_source: "owned"` and registers nothing again.
- `domain_purchase_unavailable`: OXYGEN cannot register right now and nothing was charged. Retry later, or connect a Cloudflare token to buy through it.

## Bring a domain registered elsewhere

`oxygen domains add acme.com --json` creates a zone in the connected Cloudflare account and returns the nameservers to set at the current registrar. Its DNS is manageable here only once those nameservers point at Cloudflare; until then every DNS check reads `checks.ns = external`, so fix the registrar before trusting any result.

Cloudflare connection: preview the setup with `oxygen integrations connect cloudflare --json` and enter the token through the returned Connections link. `cloudflare_token_missing_dns_scope` means the token can list zones but not read records: add Zone, DNS, Read (Edit for writes), reconnect, then `oxygen domains sync --json`.

## Plan and apply DNS

These edits require an authoritative Cloudflare zone. For an Oxygen-bought domain, keep its current nameservers and contact Oxygen support for DNS changes; adding a Cloudflare zone does not enable editing here.

```bash
oxygen domains dns plan send-acme.com --provider microsoft --json
oxygen domains dns apply send-acme.com --provider microsoft --approved --plan <plan_hash> --json
oxygen domains dns send-acme.com --deep --mx-provider microsoft --json
```

- `plan` is a free diff of SPF, DKIM, DMARC, MX and tracking records with a `plan_hash`. `apply` needs that fresh hash, which also pins the live records it planned against: a zone change in between returns 409 and a re-plan.
- Existing records are preserved: an existing SPF gets the provider include merged in, and a valid DMARC is kept unless `--dmarc-policy` says otherwise (`--dmarc-rua` alone adds the report mailbox). An SPF using `redirect=` is a `conflict` to merge by hand.
- Microsoft DKIM selectors derive automatically (`--no-auto-dkim` skips it, identically in plan and apply). Google DKIM comes from Zapmail for a Zapmail-provisioned domain; any other Google Workspace needs its DKIM value supplied with `--dkim-json` (identical in plan and apply) or in the web Fix DNS dialog.
- The deep check adds the SPF lookup budget, DMARC enforcement, the MX provider match and nameserver authority.

## Read a domain

`oxygen domains get <domain> --json` and `oxygen domains dns <domain> --json` are free. An OXYGEN-managed domain answers with `rail: "managed"`: registration and renewal, nameservers, the record set and a per-record verdict with the expected value beside the current one. Its DNS is held by the registrar and set for its inboxes automatically; these reads report a record that needs repair rather than repairing it. A domain hosted elsewhere answers with `rail: "external"` from public DNS.

## Web forwarding

Every managed domain forwards its web root, by default to the workspace's company website and never to itself. `domains forwarding get <domain>` reads it; `domains forwarding set <domain> --url <https-url>` previews and `--approved` applies.

## Tracking domain

`oxygen domains tracking setup send-acme.com --host track.send-acme.com --json` previews the CNAME, and `--approve` writes it. `oxygen domains tracking status send-acme.com --json` says whether send-time open and click tracking is active. Tracking stays off per Sequence until the Sequence opts in (`oxygen-sequencer`, `references/email.md`).

Deleting or archiving a domain: [wind-down](wind-down.md).

## Daily authentication monitoring

Domains with non-disabled connected sending mailboxes are checked daily using free public DNS, including paused, imported and managed mailboxes. Disabled and deleted mailboxes are excluded; a domain without eligible mailboxes is not monitored daily.

Use `oxygen domains list --authentication --json` for compact saved coverage and counts across all sending sources, or `oxygen domains list --attention --json` for issues, unverified, stale and failed evidence. `--q` narrows either view. The default domain list's zone `dns` verdict is a separate provider-cache observation; zone filters do not filter daily authentication. `unmatched_mailbox_domains` means no synced zone, not no daily coverage.

Read full stored evidence without contacting DNS or a provider with `oxygen domains dns <domain> --cached --json`. Its `monitoring` block explains eligibility, including why an empty snapshot has no scheduled check. `--authentication` saves one free public-DNS observation; it does **not** enable daily monitoring, change mailbox eligibility or enroll paid monitoring/tests. `nextCheckAt` is null when daily checks are inactive. These are the same snapshots shown in Deliverability analytics and domain/mailbox details. Only the latest successful observation and latest attempt are retained, not a daily history.

Inspect `lastAttemptFailed`, freshness, per-check evidence and next actions. A failed check retains the last successful observation. DKIM selector misses remain unverified; a published key does not prove active signing or message alignment. DMARC `p=none` is monitoring, and the policy source identifies inherited policies. DNS changes still require the separate reviewed plan/apply flow above.
