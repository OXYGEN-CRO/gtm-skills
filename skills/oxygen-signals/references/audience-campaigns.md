# Audience to campaign

Use after choosing an audience play (own, competitor, creator or keyword post engagers; company-page or own followers), read with `oxygen recipes show <slug> --json`. Verify identity and preserve the selected play. Resolve company and ICP facts; ask only for a missing source, channel or sender. A draft without sender or audience is incomplete: name the blockers and the next input.

## Source and inspect

- Own, competitor or creator profiles: the play's `linkedin-profile-engager-monitor` Blueprint. Pilot with one confirmed /in/ profile, two posts, one page per engagement type and five enrichments. Preflight fetches current prices; apply installs it disabled, for free.
- Keywords: preflight and apply `linkedin-keyword-engager-monitor` with one topic, bounded recent posts and a per-cycle ceiling. Inspect the keyword and post provenance and the actual people. The content-outlier miner researches content; it does not collect audiences.
- Company followers: `tables followers check` quotes a /company/ URL and at least 100 records; order only after the scope and cap are approved ([public research](public-research.md)). Keep the order and ingestion receipts and inspect delivered rows before claiming success. The ongoing company-follower-snapshot uses the same destination Table, waits for actual landing before a new purchase and merges LinkedIn identities. Promise no delivery time.
- Own followers: inspect `oxygen followers status --account <confirmed-account> --json` first and reuse its captured audience when available. `oxygen followers import --account <confirmed-account> --table <audience-table> --json` is free, paced and refreshes itself. A new destination retargets that account's existing import job: keep active captures unless the user approved moving them. The day's read allowance may already be spent; started is not completed.

Inspect the source Table and its column keys with `oxygen tables describe <table> --json`, and sample with `oxygen tables query <table> --fields <confirmed-keys> --limit 5 --json`. For the LinkedIn Network table, include `profile_url`, `is_follower` and `source_account`, and verify follower status and source account before using a row. Preserve the selected source's attribution. A small page does not prove complete capture. Find other reads with `oxygen commands search "table rows" --limit 5 --json` and hydrate exact flags with `oxygen commands get "tables query" --json`; prefer native projections and filters over broad dumps piped through grep. Engagement stays out of CRM until the normal promotion gate.

## Qualify and choose a channel

Add a reusable native qualification Column or Function grounded in the workspace ICP and real person and company evidence; the company-fit and person-fit rubric is in [qualification](qualification.md). Its `audience_qualification` output is `{eligible:boolean, rule_version:string, evidence:string[], reason:string}`. Missing evidence, a missing rule or do-not-contact never qualifies. Preserve the source post, profile, keyword, company and account evidence; a like or a follow does not prove buying intent.

Acquire the person and company evidence the ICP needs before qualification, using the native enrichment catalog and `person_enrich` / `company_enrich` where needed. Find an email or phone only for eligible pilot rows, after inspecting exact prices and dry runs. Set native `tables auto-run` for the chosen preparation columns with a positive batch ceiling and sources `insert,upsert,import`; the default `force=false` skips filled cells. Use dependency bindings and run conditions so evidence enrichment precedes qualification and contact finding runs only on eligible people. Verify that one newly captured row qualifies and enriches before enabling routing.

Map contact outputs into the router's canonical `linkedin_url`, `email`, `email_status` and `phone` cells with native bindings or formula columns. The LinkedIn Network table stores the URL as `profile_url`; a nested work-email result also needs its address and verification verdict projected into the canonical cells. Run free formula columns before routing and inspect the stored values: a populated alias or an ungraded email is not a ready contact.

| Channel | Native Sequence steps | Prerequisites |
| --- | --- | --- |
| Email | `email_send` with `subject_template` and `body_template` | Verified email; ready mailbox and sender profile |
| LinkedIn DM | `message`, or `invite`, `wait_for_connection`, `message` | Real /in/ identity; connected sender; the Sequence handles reachability |
| Connection request | `invite`; optional `wait_for_connection` and `message` | Real /in/ identity; approved sender and pace |
| WhatsApp | `whatsapp_message` | Reachable E.164 phone; connected account; the Sequence's WhatsApp opt-in |

Senders: `oxygen senders list`, `oxygen mailboxes list` and `oxygen whatsapp accounts`. Choose one ready channel; its rules are in the `oxygen-sequencer` skill. Copy may reference the public topic the person engaged with; a scraped signal is not a relationship.

## Reviewable pilot

Create one native draft Sequence, bind the source Table and sender, stage a few qualified recipients and preview the exact copy, readiness and suppressions. Preparation sends nothing. Return the source evidence, the Table, Sequence and Workflow links and the remaining approval.

Name the exact qualified row ids and their count before enrollment, and enroll only those: `--from-table` takes every remaining row regardless of qualification (`oxygen-sequencer`, Enrollment). Prefer the bounded qualification router for an ongoing audience. Keep an empty draft with explicit blockers when no row qualifies. Launch through the Sequence's own ladder and ceilings (`oxygen-sequencer`, Launch ladder).

## Ongoing launch

Approval binds the sources, qualification rule and version, enrichment, channel and Sequence, sender, copy, schedule and timezone, recipient limits and credit ceilings. State that future qualified people enroll automatically under that standing grant. Installing a kit or approving capture alone never authorizes outreach.

Start the Sequence through its normal preview and approval. Preflight and apply the `qualified-audience-router` Blueprint against the existing audience Table, Sequence, channel, exact `qualification_rule`, `rule_version` and existing `evidence_columns`. Choose every mandatory evidence column: qualification waits until each is present, including profile and company enrichment where the rule needs it. Include approved `personalization_columns` for copy variables, and use `engager_key` for keyword audiences. Its qualification, contact and receipt columns graft onto the existing Table, and it installs disabled. Run one approved bounded cycle, inspect the exact enrollment ids, then enable capture, enrichment and routing within the approved scope. Defaults: daily engager capture and routing, weekly company snapshots; own followers keep their native pacing. Pace first touches with the Sequence's daily new-enrollment limit as well as sender and channel limits. The Sequence's suppressions, prior-contact exclusion, reply-stop and sender caps stay authoritative.

Every inspected row gets a decision. `queued_for_enrollment` without a receipt is ambiguous: reconcile the Sequence before clearing or retrying. Rows missing channel contact details stay held. Repeated captures and snapshots dedupe stable identities and keep their routing receipts.

Pause the collector and router separately with `workflows disable`, and outreach with `sequences pause`. Review changed sources, rules or channel before broadening standing scope. Keep runs observable; hosted automation does the work, not a local cron or script.

The qualification column binds the approved rule, evidence, stable source key, channel and Sequence, so reapplying a changed scope to that column fails preflight. Choose a fresh versioned `qualification_column` (for example `campaign_v2_qualification`), review and configure its preparation subscription, and inspect its separate routing receipts before enabling the new scope. The old qualification and receipts stay intact. Required evidence is checked again immediately before enrollment, even when `force=false` skipped a previously filled qualification cell.
