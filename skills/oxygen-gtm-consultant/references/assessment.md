# Assessment

Reference for the consultant's current-state read and the search for the binding constraint. Every read below is free; run each as its own command (or tool call), add `--json` and read the result whole. Rerun a read that fails; a read you did not run is "unknown" in the snapshot, never zero. In MCP, reach any read your tool list lacks through `oxygen_capabilities_read`.

## The current-state reads

| Lens | Reads | What it answers |
| --- | --- | --- |
| What is known and decided | `oxygen knowledge resolve --purpose onboarding --json`; `oxygen knowledge profile --json`; `oxygen knowledge page get icp --json`, then the same read for `offers`, `customers`, `metrics`, `decisions` and `campaign-learnings`; `oxygen knowledge log list --json`; `oxygen knowledge lint --json` | Offer and ICP confirmed or hypothesis; earlier decisions and targets; which pages are still stubs |
| The funnel | `oxygen dashboards summary --range 30d --json` and `--range 90d` | Touches, replies, positive replies, meetings, deals and wins, revenue, the channel split; `--cold-deal-days` sets when an open deal counts as cold |
| Pipeline | `oxygen crm pipeline --json`; `oxygen crm describe companies --field lifecycle_stage --json` | Open, stalled and lost deals by stage. Deals with `sample: true` are seeded examples, not evidence: `totals` leaves them out and `samples` counts them |
| Outbound | `oxygen sequences list --stats --json`; `oxygen sequences analytics --range 30d --json` (add `--sequence <id>` for one); `oxygen sequences enrollments <sequence> --status stopped --json`; `oxygen sequences get <sequence> --readiness --json` | Volume, reply and positive rates by sequence, sender and variant; the stopped (bounce or opt-out) share; readiness blockers |
| Demand on hand | `oxygen inbox list --status interested --unanswered --json`; `oxygen crm signals leads-today --within-days 30 --json` | Replies showing buying interest that wait on the user; people with recent warm signals |
| Sources | `oxygen signals registry --json`; `oxygen signals list --since 30 --json`; `oxygen linkedin network status --json` | Which signal sources are armed and delivering; network capture state |
| Sending infrastructure | `oxygen mailboxes health --json`; `oxygen domains list --json`; `oxygen senders list --json`; `oxygen deliverability placement-test list --json` | Whether every email and LinkedIn number above is valid |
| Content | `oxygen publishing posts list --json`; `oxygen publishing analytics summary --channel linkedin --json` | Posting cadence and who engages |
| Automation and unattended spend | `oxygen workflows list --json`; `oxygen workflows failures --json`; `oxygen agent list --json`; `oxygen tables list --json`; `oxygen tables auto-run get <table> --json`; `oxygen tables schedule list <table> --json` | What runs without a person, what fails silently, what spends on a schedule |
| Cost and limits | `oxygen billing balance --json`; `oxygen billing usage --days 30 --json`; `oxygen limits show --json`; `oxygen budget list --json` | The month's cost; cost per positive reply when combined with sequence analytics |
| Waiting on the user | `oxygen observability approvals --json`; `oxygen workflows approvals --json` | Decisions already pending, shown before anything new is proposed |
| Connections | `oxygen integrations list --json` | Which CRM and data sources feed the workspace, and what OXYGEN cannot see |

**In MCP**, run each read through `oxygen_capabilities_read` with the tool named after its command, for example `oxygen_dashboard_summary` (singular, with `range`), `oxygen_crm_pipeline`, `oxygen_inbox_list`, `oxygen_signals_leads_today`, `oxygen_sequences_analytics`, `oxygen_senders_list`, `oxygen_mailboxes_health` and `oxygen_billing_usage`; `oxygen_capabilities_search` finds any other. A page that comes back `truncated` (`truncationReason: "result_window"`) continues with its `nextCursor`; a single row refused as too large (`table_query_result_too_large`) reruns with fewer `fields`.

Two commands look like reads but change state; keep them out of an assessment: `oxygen mailboxes warmup status` syncs warm-up state, and `oxygen inbox analyze` writes a status and a draft. `oxygen home --json` (MCP `oxygen_home_standup`) is a pure read of the workspace standup; only its plain view shown in an interactive terminal moves the user's Home "last seen" marker, so run it with `--json`. Reading post engagers or comments spends the LinkedIn sender's read allowance.

## The snapshot

Show this once, before any recommendation. Every field is a read result or "unknown"; nothing is estimated silently.

```text
GTM snapshot: <company>, <date>              Context: strong | partial | weak (why)
Goal:            <number and date, or "unknown, asking">
Running now:     <sequences, workflows, agents, armed signal sources, scheduled posts>
Last 30 days:    contacted <n> | replied <n> (<%>) | positive <n> | meetings <n> | won <n>
                 cost <credits> | cost per positive reply <n or "unknown">
Infrastructure:  mailboxes <n, health> | domains <n> | LinkedIn senders <n> | stopped share <%>
Demand on hand:  open or stalled deals <n> | interested replies waiting <n> | warm signals 7d <n>
Data:            records <n> | tables <n> | LinkedIn network captured <yes/no>
Knowledge:       offer <confirmed/hypothesis/missing> | ICP <...> | decisions logged <n>
Blind spots:     <what OXYGEN cannot see: outreach elsewhere, another CRM, calls, events>
```

## The bottleneck tree

Pipeline is a product of stages: reachable ICP accounts × people reached × reply rate × positive share × meeting rate × win rate × deal value, held together by capacity and measurement. Each branch lists the evidence that shows it is the constraint. Thresholds come from the calibration of OXYGEN's plays (open one with `oxygen recipes show <slug> --json`); all are estimates, so say so when you quote one.

| Branch | Symptoms the user reports | Evidence that it is the constraint | Usual false diagnosis |
| --- | --- | --- | --- |
| **A. Demand on hand is unworked** | "We need more leads" while replies and deals sit | Interested replies waiting on the user; deals with no activity for 21+ days. The `reply-to-meeting` play estimates that a same-day reply with a booking link books 15-30% of positive replies, and that waiting a day roughly halves that | Buying more volume |
| **B. Market and ICP** | "Not relevant" and "wrong person" replies; every segment equally lukewarm | Fewer than half of a free preview's first page plausibly fits; the `icp-to-account-map` play calls under ~40% plausible fit too loose; signal sources produce nothing; the ICP has no basis in real customers | Rewriting the copy |
| **C. Offer and positioning** | Polite "no need", "we already use X", price objections | Zero positive replies after 40+ sends with drafts the user would send (the `outbound-pilot-50` play's line for changing the segment or angle); offer lines with no number or named customer; objections clustering in the reply sample | Blaming deliverability |
| **D. List and data quality** | Bounces, wrong people, duplicates | Verified-email rate under 50%; stopped share above 15% (the `day-30-review` play's weak band); duplicate candidates on a first CRM hygiene pass; enrichment coverage well under what was priced | Judging the message on a broken list |
| **E. Channel and deliverability** | Replies collapse, a sequence auto-pauses, LinkedIn invites stall | Bounce rate above 2%; a hard-bounce auto-pause; more than 20-40 sends per mailbox a day; a new LinkedIn sender still on its ramp. Placement tests are advisory; the bounce auto-pause is authoritative | Rewriting copy, or buying domains instead of warming them |
| **F. Message** | Replies arrive but few are positive; drafts read generic | Fewer than 3 in 10 drafts the user would send as they are; the `icp`, `offers` or `positioning` pages are still stubs, so AI drafts have nothing to ground on | Changing list, angle and cadence at once |
| **G. Volume and coverage** | Every rate is healthy and the pipeline is still too small | Back-solve the goal: meetings needed ÷ observed meeting rate = people to reach; compare with weekly sends and with the reachable ICP from a free search preview | Optimising copy that already works |
| **H. Capacity and operations** | "We don't have time"; replies go to nobody; things break silently | Nobody owns replies or follow-up (ask; data rarely shows it); failed runs left uninspected (`oxygen table-runs list --table <table> --status failed --json`, `oxygen workflows runs --status failed --json`); the motion needs more weekly hours than the team has | Adding automation before naming an owner |
| **I. Measurement and learning** | "We can't tell what works" | Cost per positive reply unknown; no written definition of good; no decisions in the log; no learnings synthesised | Launching a new play to see what happens |

**Directional outside benchmarks** (vendor panels, never a promise): Smartlead's 2026 sender panel puts the median cold-email reply rate near 0.74% and the top quartile near 1.4%; a campaign at or below the bottom quartile (about 0.37%) is usually a deliverability or targeting problem, not a copy problem. Its best-case funnel runs about 6.2% replied, 3.5% positive and 1.2% booked. Steer by what is closest to revenue: won revenue, then meetings, then positive replies, then replies. Open rates are not evidence. A workspace's own history beats any panel.

**Silent failures to check every time**: a signal feed that stopped collecting while its sequence looks healthy; monthly infrastructure charges that exceed the plan's grant; schedules enabled with no per-run cost cap; one recipient provider replying far less than another from the same senders.

If the symptom sits below go-to-market (customers churn soon after they win), say the constraint is the product, not the outbound.

## Reading order

1. **Can you see?** If the funnel or the cost per positive reply cannot be read, the first finding is measurement. Note the blind spots and ask for the numbers that live outside OXYGEN.
2. **Validity**: deliverability, then list quality. A failure here invalidates every rate downstream.
3. **The funnel, top to bottom**: mark each stage weak, typical or strong. The binding constraint is the most upstream weak stage, unless real demand already in the workspace is unworked, which always goes first. Seeded sample records (`_sample: true` on record and table reads, `sample: true` on pipeline deals) are never demand; pipeline and dashboard totals already leave them out and say how many (`samples`, `caveats.sampleRecordsExcluded`).
4. **Capacity, last but always**: a motion the team cannot staff is not a motion.
5. **Pick one**: name the binding constraint, the runner-up and what would change the call.
