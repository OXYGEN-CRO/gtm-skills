# Pilots

Reference for running a designed motion as a pilot, judging it, and leaving the work where anyone can resume it. The defaults behind a pilot's numbers and words (list sizing, copy contracts and the QA gate before a send, journey shapes, migration parity bars): [craft](craft.md).

## The pilot

Every recommended motion starts as a pilot. Write it out before the first draft or send, while nobody is invested:

```text
Pilot: <name>                                   Owner: <person>   Decision date: <date>
Hypothesis:        If we <change>, <leading metric> moves from <baseline> to <target>.
One variable:      <the one thing that differs from today>; everything else is held.
Scope:             <N accounts or people>, <segment>, <channel and sender>.
Duration:          <time box>, at least the channel's read window.
Success:           <leading metric ≥ bar> by <date>  → SCALE: raise one cap or widen one scope.
Revise:            <metric in the typical band>      → change ONE variable and rerun.
Kill:              <the literal reversal condition>  → stop, disable or delete, log why.
Guardrails:        <daily caps, max credits from the preview, suppression, approvals>.
Guardrail metrics: <stopped share, opt-outs, cost per positive reply>; breaching one stops the pilot even when the leading metric looks good.
Kill switch:       <the person who may stop it, and the command they run>.
Read with:         <the exact OXYGEN reads that produce each number>.
Check-ins:         <dates>, and what the user does at each.
```

Choose the leading metric closest to revenue that the read window can show, and promise nothing a short pilot cannot prove. Every kill line names the read that measures it; a criterion nobody can read is not a criterion. At founder-scale volumes small rate differences are not measurable, so prefer large-effect kill lines (such as zero positive replies after 40 sends) and compare the workspace with its own history before any vendor panel.

The verdict, logged when the read window closes:

```text
<SCALE|REVISE|KILL> <pilot>: <the number that decided it> — <the single next action>
```

## Read windows

Judge a pilot no earlier than this. The windows come from OXYGEN's plays and are estimates.

| Motion | Earliest honest read | Meanwhile, read |
| --- | --- | --- |
| Cold email or LinkedIn outreach | 14 days after the first send (replies lag sends) | Verification rate and draft quality |
| New sending domains | 14+ days of warm-up before volume | Bounces and placement during warm-up |
| A portfolio of running plays | 30 days | — |
| Founder posting | 2-3 posts a week for 4+ weeks | Who reaches out, not reach |
| LinkedIn network capture | About two weeks for a 2,000-person network | Rows captured so far |
| Inbound-led outbound | One profile, one cycle; judge by the quality of the top tier | The tier split of the first 40 enriched |
| Nurture | One to two quarters | — |

## Kill lines

Calibration from OXYGEN's plays, all estimates (open the play with `oxygen recipes show <slug> --json` to see its full ranges):

| Condition | Verdict and the next variable | From the play |
| --- | --- | --- |
| Zero positive replies after 40+ sends with drafts the user would send | Kill this angle; change the segment or the offer angle, one at a time | `outbound-pilot-50` |
| Cold email reply rate in the bottom band after 1,000 contacted | Fix placement and the list, not the copy | `oxygen skills get oxygen-sequencer --file plays/whole-tam-email.md` |
| Verified-email rate under 50% | Stop; fix the list source or filters first | `outbound-pilot-50` |
| Stopped share above 15% | Stop; it is the list or deliverability, not the message | `day-30-review` |
| Under ~40% plausible fit on the first page | Stop sourcing; the ICP filters are too loose | `icp-to-account-map` |
| Enrichment coverage well under what was priced, or a wrong-match smell | Stop after the pilot and report | `outbound-pilot-50` |
| Cost per positive reply known but rising | Revise; do not scale | `day-30-review` |
| A signal source fires constantly and converts nothing | Mute it next cycle | `day-30-review` |
| Many likes and no ICP replies from posting | Change the topic or audience before posting more | `founder-posting-system` |

## Where the work lives

Leave every conclusion where the next session, a teammate or a later agent will find it. A new workspace already has the pages these go on.

| Artifact | Where it lives | Gate |
| --- | --- | --- |
| The snapshot | In the conversation, and copied into the diagnosis note | None |
| The diagnosis: question, reads run, findings with their reads, the binding constraint, the runner-up, what would change your mind | A dated research note linked from the `research` page, tagged `agent-derived` until the user confirms it | Working page; saves as a logged, revertible revision |
| The agreed problem statement | A `decisions` entry with its rationale and a reversal condition, plus `oxygen knowledge log append --event decision --summary "<the problem, agreed>" --json` | None; `oxygen knowledge lint --json` flags a decision without a reversal condition |
| The motion design: the canvas, borrowed / changed / why, the options table | One page per motion, linked from the `playbooks` page | Working page; pinning it as canonical is a proposal the user approves |
| The pilot | A section of the motion page, plus a launch entry in `decisions` whose reversal condition is the kill line | Each launch step keeps its own preview, cap and approval |
| Targets | The `metrics` page: definition, target and where the live number comes from; moving a target is a decision | None |
| Company facts and corrections | The typed profile, through the onboarding skill's save steps | An explicit correction authorises the patch; canonical positioning and voice stay behind a proposal |
| What the pilot taught | `campaign-learnings`, through `oxygen knowledge synthesize --kind campaign_learnings --sequence <id> --json` | The synthesis preview is metered and needs approval |
| Verdicts | `oxygen knowledge log append --event decision --summary "<verdict line>" --json` | A kill that deletes something previews the deletion first |

## Follow-up

A skill cannot wake itself. Write the check-in date and the exact reads into the pilot's decision entry. Offer the `day-30-review` play as the standing review, and offer a scheduled digest or agent only as a separate, capped, approved step. Every later session opens with pending approvals (`oxygen observability approvals --json` and `oxygen workflows approvals --json`), the decision log (`oxygen knowledge log list --json`), the motion page and the pilot's due reads, then one sentence of status and one recommendation: continue, stop on a fired kill line, or review.
