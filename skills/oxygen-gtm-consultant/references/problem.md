# Problem

Reference for going from symptoms to a root cause the user agrees with.

## From symptoms to hypotheses

Frame it as situation, complication, question:

- **Situation**: what is true and agreed, the snapshot.
- **Complication**: the gap between the goal and the trajectory, in numbers ("you want 20 meetings a month; the last 30 days produced 3").
- **Question**: the one question the engagement answers ("what is the fastest way to 20 meetings a month with one founder's time?").

Then hold two or three competing hypotheses about the cause, each with the evidence that would confirm it, the evidence that would refute it and the cheapest read or test that tells them apart. Example for "replies but no meetings": the replies are not positive (message or offer), positive replies are answered late or without a booking link (conversion), or the repliers are not ICP (list). The positive share in `oxygen sequences analytics --range 30d --json`, the waiting threads in `oxygen inbox list --status interested --unanswered --json` and the repliers' fit against the ICP separate them.

## Read the raw material

Rates say where; examples say why. Before naming a root cause, read a small sample: about ten recent replies (positive and negative), the last five lost or stalled deals with their reasons, the three best customers and why they bought, and about ten rows of the list being worked. Objections and "not relevant" replies separate an offer problem from a list problem faster than any rate. A lost-deal label is evidence, not a targeting rule: "unresponsive" can mean bad contact data, timing, message, channel, execution or fit, so a lost reason changes the ICP only when the conversations confirm it.

## From cause to root cause

- Ask why until the answer is **actionable and owned** by someone in this workspace, usually two or three levels. "Reply rate is low" → "the list is mostly non-buyers" → "the ICP filter includes every title in the company" is actionable; "the market is hard" is not.
- **Counterfactual test**: if this cause were fixed, would the goal metric move enough? If not, it contributes; it is not the constraint.
- **Proximate versus root**: bounces are proximate; buying unverified data or skipping warm-up is the root. Fix the root, and say what the proximate fix (pausing a sequence) buys meanwhile.

## The problem statement

```text
<Who> cannot reach <goal metric and date> because <root cause>,
shown by <two or three pieces of evidence, each with its read>.
If we fix it, we expect <leading metric> to move from <now> to <target> within <time to signal>.
We are not solving <what is out of scope> now.
```

Ask one question: "Does this match what you see?" The user's correction wins and is used at once. Show your provisional recommendation in the same answer so the user never waits, and record the agreed statement as a decision ([pilots](pilots.md#where-the-work-lives)).

## The questions, and when to ask them

One question per turn, only when its answer changes the recommendation, each with your recommended answer. Ask what evidence cannot answer.

| Ask when | Question | Why it matters |
| --- | --- | --- |
| The goal is unknown (ask this first) | "What should be true in 90 days, in one number: meetings, pipeline or revenue?" | Sets the target and the pilot's time box |
| Results are unknown or happen elsewhere | "Where did your last ten customers or deals come from?" | Shows the channel that already works and the ICP's basis |
| The ICP has no basis | "Name two or three of your best customers. What do they share, and how do they differ from deals you lost?" | Grounds the ICP in wins, not lookalikes |
| Capacity is unknown | "Who does sales and marketing today, and how many hours a week can they give this?" | Rules motions in or out |
| Deal value is unknown | "Roughly what is a first-year deal worth, and who signs?" | Decides high-touch versus volume |
| A conversion leak is suspected | "What happens today when someone replies 'interested'? Who answers, and how fast?" | Separates conversion from capacity |
| The recurring job is unclear | "Walk me through the last time you did this." | Shows the real process before you automate it |
| Something was tried before | "What did you try that didn't work, and how long did you give it?" | Avoids repeating it, and checks it was judged after its read window |
| Before designing | "Is there anything we must not do: domains, brand, regions, compliance, tools you must keep?" | Sets guardrails |
| Data looks thin | "Is there outreach or a CRM outside OXYGEN I should know about?" | Prevents diagnosing from partial data |
| After the diagnosis | "Does this match what you see?" | The agreement gate |
| Before launch | "Who owns the replies during the pilot?" | Names the owner the motion depends on |
| At review | "Given these numbers: scale, change one thing, or stop?" | The verdict |

Questions about the user's own background are fine only where they change the plan; that personal context stays out of shared Knowledge.
