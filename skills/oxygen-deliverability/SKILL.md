---
name: oxygen-deliverability
description: "Triage email deliverability, warmup and bounce evidence; compare workspace copies using Gmail Primary/categories and Microsoft Focused/Other; run approval-gated placement tests and manage monitoring. Results are directional; bounce auto-pause is authoritative."
allowed-tools: Bash(oxygen *)
---

# OXYGEN Deliverability

Start read-only. Placement and reputation evidence is advisory: it informs a recommendation and never changes a sender by itself. Web: Analytics, Deliverability (`/analytics/deliverability`) charts the same evidence and starts placement tests with the same preview and approval.

Domain authentication is a separate free daily DNS check. `oxygen domains list --authentication --json` reads compact saved health and coverage; `--attention` narrows issues, unverified, stale and failed evidence. Daily checks cover non-disabled sending mailboxes, including paused mailboxes; disabled/deleted mailboxes are excluded. Use `oxygen domains dns <domain> --cached --json` for saved SPF, DKIM, DMARC, MX and nameserver evidence without external calls; `--authentication` runs a free public recheck and saves its observation. A manual check does not enable daily monitoring or paid services. The saved `monitoring` block explains eligibility. DNS evidence does not verify active signing or prove inbox placement. Details: `oxygen-email-infra`, `references/domains-and-dns.md`.

## Triage loop

1. Choose the scope: `oxygen mailboxes health --view fleet --json` gives compact fleet totals; `oxygen mailboxes health --mailboxes <id-or-address> --json` gives full evidence for one inbox by default. Fleet totals and `health_coverage` remain unfiltered; `domain_context` covers the inbox's whole domain. Coverage counts actually scored inboxes. Only `coldSends7d` counts sequence sends; delivery notifications include all send sources. Zero recorded sequence sends means no measured campaign exposure in that window; zero recorded rejections is not a health or placement clearance.
   Read `healthFreshness` and `healthEvidenceAt` alongside `healthSyncStatus`/`healthSyncReason`: a recent `healthPolledAt` is not a new measurement. Freshness is `current` for trusted measurement evidence at most 24 hours old, `stale` for older evidence, or `unmeasured` when no trusted measurement timestamp exists.
   Sync status is `ok` for a successful read (including an empty result), `blocked` for a plan refusal, `failed` for a failed read, or `unknown` when no recognized refresh outcome is recorded. Older readings can have `unknown`; it establishes neither success nor a blocker. `blocked` with `byok_requires_paid_plan` means the workspace plan prevents refreshes. Eligibility is rechecked automatically; reconnecting the provider is not the remedy.
   Background health sync checks due inboxes every three minutes in bounded batches, normally after a 24-hour interval since their last successful poll. Queue work, provider backoff and missing connections can delay reads; this schedule does not guarantee a new measurement. Mailbox get/list expose the same fields under `deliverability` as `health_freshness`, `health_evidence_at`, `health_sync_status`, and `health_sync_reason`.
2. Silent or stopped inboxes: `oxygen mailboxes list --stalled` and `mailboxes list --next-action <code>`; warm-up readings are in the `oxygen-email-infra` skill (`references/warmup.md`).
3. Effective cap and connection: `oxygen mailboxes get <address> --json` (status, cap, ramp, auth mode, transport). `oxygen mailboxes deliverability evidence --sender-mailbox-id <id> --since 7d --json` reads stored campaign activity, domain checks and placement with their sample sizes; missing evidence is not a clean result. Authentication: `oxygen domains dns <domain> --deep --json`.
4. Read the relevant Sequence and run timeline (`sequences stats`, `sequences events <sequence> --kind bounced`) before naming a cause.
5. Test realistic prospect outreach, preferably actual Sequence copy; never use delivery-check or no-reply text. For Gmail Primary or Microsoft Focused in connected receivers, use [workspace copy tests](references/workspace-copy-tests.md). For external seeds, run only when the result changes a decision: [placement](references/placement.md). Show the exact copy and cost before approval.
6. Every check and probe result is stored. Read and compare it before testing again, and score copy for 0 credits: [stored evidence](references/evidence-loop.md).
7. Weigh the evidence: OXYGEN bounce auto-pause and authenticated provider telemetry outrank a single seed test.
8. Label each proposed next step: read, free preview, settings write, external send, or paid enrollment or test. Quote paid previews; a zero-credit action can still change settings or send mail.
9. Apply a change (`mailboxes status <address> --status paused`, `mailboxes cap set`, `sequences pause`) only after explicit approval, and return the affected deep-links.

## Evidence loop

Every check and placement probe is stored as typed evidence for 400 days. To learn what changed and why, loop: hypothesis, the cheapest test, read the stored result, compare it with earlier runs, record the lesson, then propose an approval-gated action. Read stored runs and observations rather than one test's output: [evidence loop](references/evidence-loop.md).

## Verdicts

Before proposing a cap change, rest, rotation, domain retirement or another placement test, open [domain verdicts](references/lifecycle.md). Verdicts are recommendations a person approves.

## What pauses automatically

Two things pause sending by themselves: bounce auto-pause (a Sequence above its hard-bounce rate, and an inbox above its own) and OXYGEN Warm-up's runaway-dispatch breaker. Reputation scores and placement results never pause anything; a person acts on them through `mailboxes status`. Resume a bounce-paused inbox or Sequence after the cause is fixed and the list is clean; a healthy-looking external test is not that fix.

## Boundaries

- Placement is directional: it estimates inbox-versus-spam landing for the tested seeds and content, never a guarantee.
- Warm-up is a health filter, not proof that production volume is safe.
- Test only the user-approved sender set and budget. A paused inbox needs the separately approved diagnostic opt-in in [placement](references/placement.md); preserve the pause, and keep disabled or unauthorized senders blocked.
- Pacing, caps and sender binding are Sequence controls (`oxygen-sequencer`).
- Mailbox monitoring seats, standing auto-enrollment and disconnection: [OXYGEN deliverability monitoring](references/monitoring.md).
- Recipient email verification: `oxygen verify email --help`.
