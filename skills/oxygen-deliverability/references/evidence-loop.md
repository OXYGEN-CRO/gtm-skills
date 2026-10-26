# Deliverability evidence loop

OXYGEN stores every deliverability check and every placement probe in the workspace. Read the stored evidence before you run another test, and draw conclusions from history, not from one command's reply. Every read below costs 0 credits and runs nothing.

## What is stored

- **Check runs:** one per execution. Kinds: `dns_auth`, `bimi`, `tracking_cname`, `blacklist`, `content_score` and `header_proof`. Each run has a subject (domain, mailbox or copy hash), a trigger, a status (`succeeded`, `partial`, `failed` or `unknown`) and an error code when it did not finish.
- **Findings:** typed rows on a run with stable codes such as `dns_auth.spf_lookup_budget`, `dns_auth.dmarc_policy`, `bimi.record`, `tracking_cname.target`, `blacklist.<zone>` and `content.rule.<symbol>`. Each finding is `pass`, `warn`, `fail` or `unknown`.
- **Placement observations:** one per probe from workspace copy tests, cross-workspace tests and placement tests: sender, receiver label and provider, folder and tab, copy hash, sent and observed times. Copy tests also record the receiver's header proof (SPF, DKIM `d=` and selector, DMARC, alignment, sending IP); placement tests record folder and tab only, so their empty header proof means not measured, not failed. Cross-workspace receivers stay anonymous labels, and their header proof shows a sending IP or signing domain only when it belongs to your own domain. Placement sources read `workspace`, `network`, `oxygen_deliverability`, `zapmail` or `oxygen_placement`.
- History is kept for 400 days and starts when OXYGEN began storing it: a domain checked before then has one run for its latest earlier check, so a short history means few checks ran, not that nothing changed before. The daily domain check writes DNS, BIMI, tracking-host and blacklist runs for active sending domains; copy scoring writes `content_score` runs; placement results write observations when they settle.

## Reads

| Question | CLI | MCP |
| --- | --- | --- |
| Which checks ran, and which failed? | `oxygen mailboxes deliverability checks list --subject acme.com --finding-status fail --json` | `oxygen_mailboxes_deliverability_checks_list` |
| What exactly did one run find? | `oxygen mailboxes deliverability checks get <run-id> --json` | `oxygen_mailboxes_deliverability_checks_get` |
| Where did each probe land? | `oxygen mailboxes deliverability observations list --sender-domain acme.com --json` | `oxygen_mailboxes_deliverability_observations_list` |
| What changed, and what did placement do? | `oxygen mailboxes deliverability evidence --sender-domain acme.com --since 28d --json` | `oxygen_mailboxes_deliverability_evidence` |
| How do two runs differ? | `oxygen mailboxes deliverability compare <a> <b> --json` | `oxygen_mailboxes_deliverability_compare` |
| How does this copy score? | `oxygen mailboxes deliverability score-copy --subject … --body-file copy.txt --json` | `oxygen_mailboxes_deliverability_score_copy` |

Dashboards can chart the same evidence with the deliverability evidence widget.

## Reading rules

- Lists are newest first. Follow `next_cursor` with the same filters until `has_more` is false; `since`/`until` take ISO times from the year 2000 on, or `7d`/`24h`.
- Observations are windowed and ordered by placement time (sent, else observed, else recorded), the same time evidence buckets on.
- Evidence names one subject: `--sender-domain`, `--sender-mailbox-id`, `--content-hash` or `--receiver-provider`. It defaults to the last 28 days in UTC day buckets; a window holds at most 120 day buckets or 60 week buckets (`--bucket week`), so the longest relative day window is `--since 119d`. Empty buckets are zeros.
- Every rate carries `numerator`, `denominator` and `lowSample`. Treat a low sample as no conclusion yet and say how many probes a claim rests on.
- `unknown` is not `pass`, and `never_run` means no run exists. A blacklist run that could not query any list is stored as exactly that, never as "not listed"; some licensed lists are not enabled yet.
- `compare` takes two placement test ids or two check run ids of one kind. A comparison across different copy, senders or receiver providers changes more than one thing; say so.
- Placement and scores are directional. They never pause or change a sender; only bounce auto-pause and the warm-up breaker pause anything.

## Scoring copy

`score-copy` scores one copy on OXYGEN's own scorer and stores a `content_score` run: content hash, score against the required score, every fired rule as a `content.rule.<name>` finding, and the link domains. It sends nothing and costs 0 credits, but it is a write because the run is stored. The content hash joins the score to placement observations of the same copy. Pass `--from` to score the real sender domain and `--request-id` so a retry returns the stored score. `content_score_not_configured` means scoring is not set up in this environment and nothing was stored; `content_score_unavailable` names the stored failed run; while `retryable` is true, retry later with the same request id. One request id gets 5 attempts; with `attempts_exhausted` true, use a new request id.

## The loop

1. **Hypothesis:** name one variable and the expected outcome, for example "removing the tracking link moves Gmail from Promotions to Primary".
2. **Read first:** read `evidence` and the relevant `checks` before testing anything.
3. **Test:** run the cheapest test that can answer it. `score-copy` sends nothing; a [workspace copy test](workspace-copy-tests.md) or a [placement test](placement.md) sends mail and needs its preview and approval.
4. **Read the stored result** by run id, then `compare` it with the earlier run. Quote rates with their sample sizes and name every other variable that changed.
5. **Record the lesson** in the Knowledge Graph: what was tested, the run ids and the result. Search first with `oxygen knowledge search` and update an existing page instead of creating a near-duplicate.
6. **Propose an action** (rotate a sender, fix copy, fix DNS, investigate a listing) with its preview, cost and approval class. Change nothing before approval.

Stop when the evidence answers the question or the next test would cost more than the decision is worth.

## Daily loop blueprint

The `deliverability-evidence-loop` blueprint installs a daily Workflow that does the reading half of this loop. Preview it with `oxygen blueprints preflight deliverability-evidence-loop --json`; `oxygen blueprints apply deliverability-evidence-loop --json` installs it disabled, and enabling it needs one standing approval.

Each cycle scores the current copy of every active email Sequence step as it is sent (free; one stored score per distinct copy; variants the A/B auto-winner paused are skipped), compares placement by sending domain and receiver provider over the last 7 days against the 7 days before, and reads the latest DNS, BIMI, tracking-host and blacklist findings. Its `review` step output holds the summary, the evidence, `evidence_gaps` and the proposals: list runs with `oxygen workflows runs --workflow <workflow> --json` and read one with `oxygen workflows runs --run-id <run_id> --json`.

A proposal is raised for an inbox-rate drop of at least 25 points with at least 8 settled probes in both windows, a failing DNS authentication or tracking check, a new blacklist listing, or a copy scoring at or above the spam threshold. While the threshold stays crossed, an earlier proposal is listed under `suppressed_proposals` for 7 days, then raised again. The loop never sends email, starts a copy test, pauses or changes a sender, or waits on a decision. A Google or Microsoft drop recommends a workspace copy test of the named copy (senders × receivers × variants, at most 50 messages); a Yahoo or other-provider drop cannot be tested with connected receivers, so review the evidence instead; a DNS failure points to `oxygen domains dns <domain> --cached --json` (`--deep` re-checks live records).

## Standing triggers

A `placement_changed` Signal fires when a sender domain's inbox rate at one receiver provider drops or Gmail Primary shifts to Promotions. The `deliverability / blacklist_listing_changed` workspace event fires when a listing starts or ends; a listing stays listed until a later check answers for that zone. Both can start a Workflow (`oxygen workflows events list`). Neither changes a sender.
