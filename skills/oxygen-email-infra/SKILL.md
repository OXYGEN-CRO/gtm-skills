---
name: oxygen-email-infra
description: "Plan, set up and run OXYGEN cold email sending infrastructure: playbooks by market (Google/Microsoft mix, inbox count sized from the TAM), lookalike domains and DNS, managed and imported mailboxes, sender profiles and photos, OAuth, warm-up, recovery, egress and wind-down; also connect a customer's own inbox for Unibox history and CRM."
allowed-tools: Bash(oxygen *)
---

# OXYGEN Email Infrastructure

Sending infrastructure sits beneath Messages and Sequences: domains, inboxes, the people they send as, their authorization, warm-up and egress. Discover with `oxygen capabilities search "email infrastructure <goal>" --json`.

## Fail closed

- The live quote is the price: treat it as pricing truth and quote its fields; never quote a prose price, including any number remembered from earlier.
- Get approval before purchases, subscriptions, writes, or recurring charges, and deep-link every write.
- Surface missing authority, consent, balance or readiness and stop there; a faked readiness step is a broken send later.
- Credentials travel only through the signed-in app or the local CLI. Keep secrets out of chat and MCP, and leave environment files alone.

## Cold email playbook (plan before buying)

Before ordering inboxes for outreach, read the [cold email playbook](references/cold-email-playbook.md) and present its plan to the user as OXYGEN's best practice: the playbook for their market, the inbox and domain count sized from the TAM, and the guided setup from LinkedIn photo and lookalike domains to warm-up and caps.

## Readiness chain

1. Inspect saved daily DNS health: `oxygen domains list --authentication --json` (use `--attention` for issues, unverified, stale or failed checks; see **Daily authentication monitoring** in [domains and DNS](references/domains-and-dns.md)). For zone inventory, use `oxygen domains list --json`, `oxygen mailboxes list` (the readable pool: counts first, then every mailbox that owes an action), `oxygen mailboxes compatibility --json`.
2. Acquire inboxes sized by the playbook. Choose natural address variants of the real person (for example `phil`, `philipp`, `philipph`, `philipp.hirte`, `p.hirte`); never generate numeric suffixes unless the user explicitly requests them. Review the exact addresses before purchase. Every inbox belongs to a sender profile, the person it sends as; the name and photo stamped on a managed inbox are permanent, so read back the preview's `senders[]` and stop at `avatar_durable: false`. Managed inboxes: [managed inboxes](references/managed-inboxes.md). Existing inboxes: [import and OAuth](references/import-and-oauth.md). Domains: [domains and DNS](references/domains-and-dns.md).
3. DNS: verify nameserver authority first, then SPF, DKIM, DMARC, MX and tracking ([domains and DNS](references/domains-and-dns.md)).
4. Sending authorization: `oxygen mailboxes oauth-health --json`. An `automatic` repair waits for `next_attempt_at`; otherwise follow the row's remedy. Microsoft dedicated sending tenants use one administrator grant for exact addresses; other mailboxes use individual OAuth.
5. Warm-up: read `warmupTruth` from `oxygen mailboxes warmup status --json` or `mailboxes list` ([warm-up](references/warmup.md)). A managed order warms its inboxes automatically only when its quote carries `warmup_activation.automatic_after_provisioning=true`. Warm-up authority never authorizes sending.
6. Health and limits: `mailboxes health`, caps and ramps, [egress IPs](references/egress.md). Triage of bounces, reputation and placement: the `oxygen-deliverability` skill.
7. Attach the senders to a Sequence (`oxygen-sequencer`).

## Where things live

| Goal | Reference |
| --- | --- |
| Pick a playbook, size inboxes from the TAM, set up lookalike domains, inboxes, photos and warm-up | [cold email playbook](references/cold-email-playbook.md) |
| Buy or recover managed inboxes, sender profiles and photos, native sending authorization, existing Cloudflare domains | [managed inboxes](references/managed-inboxes.md) |
| Import inboxes from another provider or a file, OAuth consent modes, Zapmail | [import and OAuth](references/import-and-oauth.md) |
| Connect the customer's own Gmail or Microsoft 365 inbox for history and CRM | [connect a mailbox](references/connect-mailbox.md) |
| Buy or add a domain, DNS plan and apply, forwarding, tracking domain | [domains and DNS](references/domains-and-dns.md) |
| Warm-up enrollment, status and repair | [warm-up](references/warmup.md) |
| Dedicated sending IP | [egress](references/egress.md) |
| Delete mailboxes or domains, move a domain out, leave a workspace | [wind-down](references/wind-down.md) |
| Mailbox monitoring and placement tests | `oxygen-deliverability` skill |

Open a reference with `oxygen skills get oxygen-email-infra --file references/<name>.md --json` (MCP `oxygen_skills_get` with that `file`).

Plays: [email-infra-setup](plays/email-infra-setup.md).
