# Domain verdicts: watch, rest, retire

Bands, caps, windows, triggers and spares here are OXYGEN's recommended defaults; code enforces only bounce auto-pause and the 8-probe `lowSample` floor. Sizing and caps: `oxygen-email-infra`.

## Unit

Judge a **sending domain × receiver provider**, never one inbox or a blend. A test settles about 4 seeds per provider, so a reading adds sides `a` and `b` of `oxygen mailboxes deliverability compare <previous-test> <latest-test> --json` per provider (8 probes); `evidence` blends its whole window.

## Verdicts, per receiver provider

- **Healthy**, ≥85% (7–8 of 8): raise caps only after two consecutive Healthy readings.
- **Watch**, 60–84% (5–6 of 8): lower caps above 10 to 10 (`oxygen mailboxes cap set <mailbox> --daily-cap 10`, settings write); test again in 7 days.
- **Rest**, <60% on two consecutive readings, or 0 of 8 once, at both providers (settings write).
- **Retire** on a retire trigger (deletion preview, then confirmation).

One provider failing, the other not: don't rest. Route its recipients to the other provider's inboxes, keeping each sending provider at ≥30% of sends: `oxygen sequences update <sequence> --esp-routing-file routes.json` (`oxygen-sequencer`).

## Triggers

- **Bounce auto-pause** (thresholds and Sequence pauses: `oxygen-sequencer`; inbox pauses: `campaignAutoPause` in `oxygen mailboxes list --status paused --json`): re-verify the remaining list (`oxygen-enrichment`) before resuming.
- **Two inboxes of one domain auto-paused within 7 days**: rest the domain.
- **Policy rejection** (`5.7.708`, `5.7.515`, `provider_rejected_by_google`) from ≥2 recipient organisations in 7 days: that provider is failing. Codes: `signals.dsnCodes7d` in `oxygen mailboxes health --mailboxes <id> --json`, warm-up included; organisations only in the bounce emails.
- **Domain-kind listing** (DBL, SURBL, URIBL) on the sending or a link domain (`blacklist.<zone>` findings): pause its inboxes, request delisting, apply the retire triggers.
- **Missing MX, failing SPF or DMARC** (`oxygen domains list --authentication --attention --json`): pause its inboxes until fixed. Google without custom DKIM: warn only.
- **Reply rate at or below the bottom quartile** (`oxygen-gtm-consultant` assessment) over ≥500 sends, list and copy unchanged (`by_domain` in `oxygen sequences variants <sequence> --json`): test.

## Rest

1. Note each inbox's cap (`oxygen mailboxes get <mailbox> --json`), then pause each (`oxygen mailboxes status <mailbox> --status paused --json`); warm-up enrollment stays. Not standby: a ready standby inbox can be promoted elsewhere.
2. After 14 days, run two tests with the real Sequence copy and the approved `--allow-paused-probe` ([placement](placement.md)).
3. At ≥60%, `cap set` 5, then `--status active`, adding 5 every 2 sending days up to the noted cap (10 under Watch); `mailboxes ramp set` cannot restart a ramp. Under 60%: retire.
4. Record dates and test ids on the domain's Knowledge page; OXYGEN stores no rest state.

## Retire

Retire the domain on any of: a listing not cleared within 7 days; a relisting within 90 days; under 60% after a rest; a second rest due within 90 days. Never rotate on a calendar.

1. Promote a ready spare: `oxygen mailboxes standby set --mailbox <spare> --role outreach --json`, then with `--approved --plan <plan>`; add it to any Sequence `--mailboxes` allowlist.
2. Preview `oxygen domains delete <domain> --json`; order replacements 4 weeks ahead.

## Cadence

Two baseline tests per domain before its first cold send, then one per domain per week from the included tests, spread across its inboxes (`pricing` in `oxygen deliverability placement-test list --json`). A 1-inbox domain or a 5-week month exceeds the included tests; Microsoft inboxes (no monitoring) pay for every test. Extra tests only after new copy, a new domain, Watch or the reply trigger.

## Spares

Keep warm standby of about 20% of active domains per provider, at least one 2-inbox domain each, with Sequences opted in (`oxygen-email-infra` warm-up). Replace an inbox, not the list, only when bounce-paused on a clean list or provider-suspended.

## Not a signal

- Vendor health score: two domains scored 64; one inboxed 0 of 4 Gmail seeds, the other 4 of 4.
- IP blocklists: Gmail API and Graph recipients never see OXYGEN's egress IP.
- Google's 0.3% complaint line excludes Workspace recipients; OXYGEN's 0.08%/0.3% limits gate only bulk sending-domain release slices.
