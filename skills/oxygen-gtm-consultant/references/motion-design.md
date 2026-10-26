# Motion design

Reference for designing a custom GTM motion once the problem is agreed.

## The motion canvas

A motion is the loop OXYGEN runs (source or observe, qualify, enrich, act, handle replies, keep Records true, learn), filled in for this company. Each stage names the building block that owns it. Leave out any stage the motion does not need: the canvas is a checklist, not a template.

| Stage | The decision for this company | Owning building block | Typical commands | Plays to borrow from |
| --- | --- | --- | --- | --- |
| Goal and definition of good | Target metric, date, what counts as good | Knowledge (`metrics`, `decisions`) | `oxygen knowledge log append --event decision --summary "<goal and definition of good>" --json` | `day-30-review` |
| Segment and trigger | One ICP slice and the event that puts it in market now | Knowledge (`icp`), Signals | `oxygen knowledge page get icp --json`; `oxygen signals search preview --keywords "<the buyer's problem>" --json`; `oxygen companies search preview --source hiring --filters-json '<roles>' --json` | `daily-warm-lead-queue` |
| Source | Where names come from: CRM, network, engagers, visitors or the wider market | Records, Signals, Tables | `oxygen crm pipeline --json`; `oxygen linkedin network status --json`; `oxygen people search preview --filters-json '<ICP filters>' --json` | `inbound-led-outbound`, `icp-to-account-map`, `website-visitor-outreach` |
| Qualify | The fit rule and which band moves on | Tables (an AI fit column); Records at the warm-lead gate | `oxygen columns add <table> --label "ICP fit" --score "weak,possible,strong" --prompt "<fit rule>" --grounding workspace --json`, then `oxygen columns run <table> <column> --dry-run --json` | `inbound-led-outbound` |
| Enrich | Only the contact data the chosen channel needs | Tables (tool and waterfall columns) | A column dry run, then live with a cap from its preview | `outbound-pilot-50` |
| Act | Channel, sender, angle, cadence, daily caps | Sequences for net-new outreach, Messages for existing threads, Publishing for posts | `oxygen sequences create ... --max-new-enrollments-per-day 10 --exclude-contacted --json` | `outbound-pilot-50`, `founder-posting-system` |
| Respond | Who answers, how fast, with which link | Messages (Unibox); the AI Sales Agent drafts replies for approval | `oxygen inbox list --status interested --unanswered --json` | `reply-to-meeting`, `speed-to-lead` |
| Record | Which stages move on replies, meetings and deals | Records | Arming a CRM automation (`oxygen crm automation set <automation> --dry-run --json` first) only after the user approves it | `reply-to-meeting` |
| Orchestrate | What runs on a schedule or an event | Workflows (deterministic) or Agents (adaptive) | Through the `oxygen-workflow-authoring` skill; installs land disabled | — |
| Learn | The review cadence and the one rule that may change per loop | Knowledge, Observability, Dashboards | `oxygen sequences analytics --range 30d --json`; `oxygen knowledge synthesize --kind campaign_learnings --sequence <id> --json` | `day-30-review` |
| Owners and guardrails | Who does what each week; caps; approvals | People, plus each building block's gates | Previews, and `--max-credits` read from them | `daily-warm-lead-queue` |

Choose the mechanism by the least autonomy that works: a table column when a rule over rows does it, a workflow when it needs a trigger, branching, waiting or retries, an agent only when the job needs judgment across many steps. One owner per fact: Records hold truth, Tables hold work, Signals record that something happened, Sequences own net-new outreach.

## Plays as inspiration

1. Search by the **constraint**, not the channel: `oxygen recipes list "<the constraint in plain words>" --view summary --limit 6 --json`. Open at most two with `oxygen recipes show <slug> --json`.
2. Take only what transfers: the stage order, the gate rule, the calibration ranges, the failure modes. Plays carry these as data: a leading metric, labelled benchmark ranges, prerequisites with check commands, approval gates and an installable kit.
3. Change what is specific to this company: the segment, the trigger, the channel mix, the angle, the sender, the volume and the weekly hours.
4. Write a **borrowed / changed / why** table into the motion page, for example: "borrowed the tier gate from `inbound-led-outbound`; changed the source from post engagers to webinar attendees, because the user's posts reach peers, not buyers".
5. Install a kit only when it fits the design (`oxygen recipes install <slug> --json` installs with every workflow disabled), and install only the stages the motion uses. Installing is never permission to run, enable, enroll, send or spend.

## Where plays help, by constraint

A designed motion usually crosses two of these, for example a warm source plus the reply handling that converts it; that combination is the point of a custom motion.

| Constraint | Plays to read for inspiration |
| --- | --- |
| Demand on hand | `reply-to-meeting`, `speed-to-lead` |
| Market and ICP; volume | `icp-to-account-map`, `outbound-pilot-50` |
| Warm sources | `day-1-first-win`, `daily-warm-lead-queue`, `website-visitor-outreach`, `inbound-led-outbound` |
| Offer and positioning | No play: work from the company profile (`oxygen context profile get --json`) |
| List and data | `daily-warm-lead-queue`, `migrate-from-clay` |
| Channel and deliverability | `email-infra-setup` |
| Volume through content | `founder-posting-system` |
| Capacity and operations | `daily-warm-lead-queue` |
| Measurement | `day-30-review` |
| Agencies | `client-workspace-launch` |

## Options and the recommendation

Generate two to four options that each address the binding constraint and **differ in kind**: a different source or channel, not the same idea reworded. Each option names its likely miss. Compare them in one table, with high, medium or low and a reason, never invented weights:

| Option | Impact on the constraint | Confidence (evidence) | Setup and weekly hours | Time to signal | Cost (from a preview) | Reversibility |
| --- | --- | --- | --- | --- | --- | --- |
| *Illustrative:* answer interested replies the same day with a booking link | High: the leak is reply to meeting | Medium: 6 waiting threads | Low: 1 hour setup, 2 hours a week | About 2 weeks | Free reads and drafts | Fully reversible |
| *Illustrative:* a 50-lead pilot on a hiring-trigger segment | Medium: adds volume, not conversion | Low: no customers in that segment yet | Medium: 1 hour setup, 1 hour a week | 14+ days after the first send | From the column and search previews | Reversible; domain reputation at stake |

**The decision rule:** among options with at least medium impact and medium confidence, choose the shortest time to signal; break ties by reversibility, then by weekly hours. Recommend one primary motion and at most one enabling task, such as warm-up running in parallel. Cost always comes from a live preview, never from prose.

**The red-team line:** every recommendation states the strongest case against it and the assumption most likely to be wrong, rated validated, reasonable, unproven or risky. Where a free read can test that assumption, run it before asking the user to approve anything.
